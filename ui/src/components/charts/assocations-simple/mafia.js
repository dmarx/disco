//
//     Copyright © 2011-2022 Cambridge Intelligence Limited.
//     All rights reserved.
//
//     Sample Code
//
//!    Disrupt a resilient mafia network through social network analysis.

import { data } from './mafia-data.js';

let visibleChart;
let hiddenChart;
let savedChartItems;
let nodeSelection = [];
let nodeIdsRemovedBySlider = [];
let allNodeIds = [];
const familyIdsCache = {};
const allNodeIdsLookup = {};

// Stacks to maintain the order of items filtered by manual selection and the slider
let manuallyRemovedStack = [];
let sliderStack = [];

// Get elements from the UI
const familyCheckBoxesEls = [...document.querySelectorAll('input[type=checkbox]')];
const largestCompSizeEl = document.getElementById('lcc');
const restoreItemsButtonEl = document.getElementById('restore');
const removeItemsButtonEl = document.getElementById('remove');
const sliderEl = document.getElementById('slider');
const resetAllEl = document.getElementById('resetAll');

function setButtonAvailability(element, available) {
  element.classList[available ? 'add' : 'remove'](['active', 'btn-kl']);
  element.disabled = !available;
}

function setUIAvailability(available) {
  if (manuallyRemovedStack.length) {
    setButtonAvailability(restoreItemsButtonEl, available);
  }
  familyCheckBoxesEls.forEach((radio) => {
    radio.disabled = !available;
  });
  sliderEl.disabled = !available;
  resetAllEl.disabled = !available;
}

// Update order of available nodes for the slider
function setIdsForSliderStack() {
  const sortedAvailableNodeIds = allNodeIds
    // Available nodes are those on the visible chart
    .filter(nodeId => allNodeIdsLookup[nodeId].sliderAvailability
      && allNodeIdsLookup[nodeId].filterState)
    .sort((idA, idB) => allNodeIdsLookup[idB].index - allNodeIdsLookup[idA].index);

  // Append items already filtered by the slider to the end of the stack, in order they were removed
  sliderStack = sortedAvailableNodeIds.concat((nodeIdsRemovedBySlider));
}

function setLargestComponentSize() {
  const components = visibleChart.graph().components();
  largestCompSizeEl.innerText = components.length
    ? components.reduce((a, b) => ((b.nodes.length < a.nodes.length) ? a : b)).nodes.length
    : 0;
}

function setNodeState(nodeIds, property, state) {
  nodeIds.forEach((id) => {
    allNodeIdsLookup[id][property] = state;
  });
}

function setNodesManuallySelected(newSelectedNodes) {
  // Clear the previously selected nodes
  if (nodeSelection.length) {
    setNodeState(nodeSelection, 'filterState', true);
    nodeSelection = [];
  }
  if (newSelectedNodes.length) {
    // Prepare selected nodes to be removed
    nodeSelection = newSelectedNodes;
    setNodeState(newSelectedNodes, 'filterState', false);

    // Highlight neighbours of selected items
    const neighbours = visibleChart.graph().neighbours(newSelectedNodes).nodes;
    visibleChart.foreground(node => newSelectedNodes.includes(node.id)
      || neighbours.includes(node.id));

    // Allow selected nodes to be removed
    setButtonAvailability(removeItemsButtonEl, true);
  } else {
    // No nodes selected
    visibleChart.selection([]);
    visibleChart.foreground(() => true);
    setButtonAvailability(removeItemsButtonEl, false);
  }
}

async function pingNodes(allNodeIdsToRemove, primaryNodeIds) {
  const collateralNodeIdsToRemove = allNodeIdsToRemove.filter(id => !primaryNodeIds.includes(id));
  if (collateralNodeIdsToRemove.length) {
    // Primary removed nodes ping blue
    visibleChart.ping(allNodeIdsToRemove, { time: 1200, c: '#5d81f8' });

    // Collateral nodes ping red
    await visibleChart.ping(collateralNodeIdsToRemove, { time: 1200, c: '#FF0000' });
  } else {
    await visibleChart.ping(allNodeIdsToRemove, { time: 1200, c: '#5d81f8' });
  }
}

async function getItemsFromFilter() {
  function matchFilter(node) {
    return allNodeIdsLookup[node.id].familyCheckbox && allNodeIdsLookup[node.id].filterState;
  }

  // Filter the hidden chart and return the items to be removed or expanded into visible chart
  const { shown, hidden } = await hiddenChart.filter(matchFilter, { type: 'node', animate: false, hideSingletons: true });
  const nodesShown = shown.nodes;
  const nodesHidden = hidden.nodes;
  const itemsShown = nodesShown.length ? nodesShown.concat(shown.links) : [];
  const itemsHidden = nodesHidden.length ? nodesHidden.concat(hidden.links) : [];
  return {
    nodesShown,
    nodesHidden,
    itemsShown,
    itemsHidden,
  };
}

async function doFiltering(filteredBy) {
  // Disable the UI while visible chart is updated
  setUIAvailability(false);

  // Get items to be expanded or removed
  const {
    nodesShown: nodeIdsToExpand,
    nodesHidden: nodeIdsToRemove,
    itemsShown: itemIdsToExpand,
    itemsHidden: itemIdsToRemove,
  } = await getItemsFromFilter();

  if (itemIdsToExpand.length) {
    // Allow expanded items to be available for filtering on the slider
    setNodeState(nodeIdsToExpand, 'sliderAvailability', true);

    // Retrieve saved item so we can expand with the correct node size
    const itemsToExpand = savedChartItems.filter(item => itemIdsToExpand.includes(item.id));
    await visibleChart.expand(itemsToExpand, { layout: { name: 'organic', fit: true } });
  } else if (itemIdsToRemove.length) {
    let primaryNodesToHide;

    // Check which filter was used and identify primary nodes for correct ping colour
    if (filteredBy === 'selected') {
      manuallyRemovedStack.push(nodeIdsToRemove);
      primaryNodesToHide = nodeSelection;

      // Remove the node selection so that the remove animation is consistent with other filters
      nodeSelection = [];
      setNodesManuallySelected([]);
    } else if (['batanesi', 'mistretta', 'none'].includes(filteredBy)) {
      primaryNodesToHide = familyIdsCache[filteredBy];
    } else if (filteredBy === 'slider') {
      primaryNodesToHide = nodeIdsRemovedBySlider;
    }

    // Make removed nodes unavailable to the slider
    setNodeState(nodeIdsToRemove, 'sliderAvailability', false);

    // Ping nodes to be removed
    await pingNodes(nodeIdsToRemove, primaryNodesToHide);

    // Remove items from the visible chart
    await visibleChart.removeItem(nodeIdsToRemove);

    // Layout items
    await visibleChart.layout('organic', { mode: 'adaptive' });
  }

  // Update the slider for the nodes remaining on the visible chart
  setIdsForSliderStack();

  // Update the largest component indicator
  setLargestComponentSize();

  // Enable the UI after the visible chart has been updated
  setUIAvailability(true);
}

function initialiseInteractions() {
  const sliderValueEl = document.getElementById('sliderValue');

  // Filter the chart when any checkbox is changed
  familyCheckBoxesEls.forEach((checkbox) => {
    checkbox.addEventListener('click', (event) => {
      let familyIdsToBeFiltered;
      const familyName = event.target.id;
      const familyChecked = event.target.checked;
      setNodesManuallySelected([]);

      // Check if family has been filtered before
      if (familyIdsCache[familyName]) {
        familyIdsToBeFiltered = familyIdsCache[familyName];
      } else {
        // Get the family ids and cache the ids for later use
        familyIdsToBeFiltered = allNodeIds
          .filter(id => allNodeIdsLookup[id].family === familyName);
        familyIdsCache[familyName] = familyIdsToBeFiltered;
      }

      setNodeState(familyIdsToBeFiltered, 'familyCheckbox', familyChecked);
      doFiltering(familyName);
    });
  });

  visibleChart.on('selection-change', () => {
    const selectedItems = visibleChart.selection();

    // Filter selection to include only nodes
    const newSelectedNodes = selectedItems.filter(id => !id.match(/-/));
    setNodesManuallySelected(newSelectedNodes);
  });

  // Remove manually selected nodes
  removeItemsButtonEl.addEventListener('click', async () => {
    setButtonAvailability(removeItemsButtonEl, false);
    await doFiltering('selected');
    setButtonAvailability(restoreItemsButtonEl, true);
  });

  // Restore previously removed nodes
  restoreItemsButtonEl.addEventListener('click', () => {
    setNodesManuallySelected([]);

    // Update state of nodes to be restoreed
    setNodeState(manuallyRemovedStack.pop(), 'filterState', true);

    // Disable the restore button if stack is empty
    if (manuallyRemovedStack.length === 0) {
      setButtonAvailability(restoreItemsButtonEl, false);
    }
    doFiltering();
  });

  // Update the slider value before the change event if it is dragged
  sliderEl.addEventListener('input', () => {
    sliderValueEl.innerText = +sliderEl.value;
  });

  // Filter the chart once the slider value has been changed
  sliderEl.addEventListener('change', () => {
    setNodesManuallySelected([]);
    const sliderValue = +sliderEl.value;
    const availableNodes = sliderStack.length;
    const nodesToRemove = Math.min(sliderValue, availableNodes);
    nodeIdsRemovedBySlider = sliderStack.slice(availableNodes
        - nodesToRemove, availableNodes);

    // Update filter state of nodes on the stack
    sliderStack.forEach((id) => {
      allNodeIdsLookup[id].filterState = !nodeIdsRemovedBySlider.includes(id);
    });
    doFiltering('slider');
  });

  resetAllEl.addEventListener('click', async () => {
    // Clear all filters and reset the UI
    setNodesManuallySelected([]);
    manuallyRemovedStack = [];
    nodeIdsRemovedBySlider = [];
    setButtonAvailability(restoreItemsButtonEl, false);
    sliderEl.value = 0;
    sliderValueEl.innerText = 0;
    familyCheckBoxesEls.forEach((checkbox) => {
      checkbox.checked = true;
    });

    // Update state of all nodes and filter the chart
    setNodeState(allNodeIds, 'filterState', true);
    setNodeState(allNodeIds, 'familyCheckbox', true);
    await doFiltering();
    visibleChart.layout('organic', { mode: 'adaptive' });
  });
}

// Set the lookup for the ranking and availability of each node for the slider
function setNodesIdsLookup(sizedNodes) {
  // All node ids sorted by degree score
  allNodeIds = sizedNodes
    .sort((nodeA, nodeB) => nodeB.e - nodeA.e)
    .map(node => node.id);

  allNodeIds.forEach((id, index) => {
    allNodeIdsLookup[id] = {
      // Ranking of node by size
      index,

      // Availability of node to be filtered by the slider
      sliderAvailability: true,

      // Check for whether node should be filtered from the chart
      filterState: true,

      // If a family checkbox is unchecked, this state ensures nodes won't be expanded
      // back in if they have already been removed by the other filters
      familyCheckbox: true,
    };
  });

  // Add family property to the lookup
  savedChartItems.forEach((item) => {
    if (item.type === 'node') {
      allNodeIdsLookup[item.id].family = item.d.family;
    }
  });
}

// Helper function to normalize degrees score
function getResizeArray(values) {
  const valuesArray = Object.values(values);
  const max = Math.max.apply(null, valuesArray);
  const min = Math.min.apply(null, valuesArray);
  const resizeArray = Object.keys(values).map(id => ({
    id,
    e: (values[id] - min) / (max - min) * 2 + 1,
  }));
  return resizeArray;
}

async function setNodesSize() {
  const degreeScores = await visibleChart.graph().degrees({ value: 'total' });
  const resizeValues = getResizeArray(degreeScores);
  visibleChart.setProperties(resizeValues);

  // Save the chart to retrieve nodes sizes when filtering them back in.
  savedChartItems = visibleChart.serialize().items;
  return resizeValues;
}

async function startKeyLines() {
  KeyLines.promisify();


  const options = {
    logo: {
      u: 'images/Logo.png',
    },
    selectedNode: {
      ha0: {
        c: '#5d81f8',
        r: 35,
        w: 15,
      },
    },
    selectedLink: {},
  };

  [visibleChart, hiddenChart] = await KeyLines.create([
    { container: 'klchart', options },
    { container: 'hiddenChart' }]);


  visibleChart.load(data);
  hiddenChart.load(data);

  // Set the size of each node by normalized degree score
  const nodesSizedByDegree = await setNodesSize();

  // Set the order of nodes ids to be filtered for the slider
  setNodesIdsLookup(nodesSizedByDegree);

  // Set nodes to be filtered by the slider
  setIdsForSliderStack();

  visibleChart.layout('organic', { consistent: true, packing: 'adaptive' });
  initialiseInteractions();
  setLargestComponentSize();
}

window.addEventListener('DOMContentLoaded', startKeyLines);
