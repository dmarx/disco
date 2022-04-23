//
//     Copyright © 2011-2022 Cambridge Intelligence Limited.
//     All rights reserved.
//
//     Sample Code
//
//!    Use donuts to visualise relative volumes of email.

import { data } from './emailtraffic-data.js';

// The radius of a node, in world coordinates, without enlargement
const BASE_NODE_RADIUS = 27;

// The distance the tooltip arrow protrudes from the tool tip box
const TOOLTIP_ARROW_SIZE = 11;

const colourToRoles = {
  '#FF1529': 'Admin', // red - admin
  '#FF8027': 'Sales', // orange - sales
  '#CA62C4': 'Other', // purple - other
  '#44D161': 'Ops', // green - ops
  '#29A1E7': 'Tech', // blue - tech
  '#F781BF': 'Marketing', // pink - marketing
  '#CB623C': 'Support', // brown - support
  '#C4C4C4': 'External', // grey - external
};

const highlightColours = {
  '#D22432': '#FF1529', // red - admin
  '#DD6800': '#FF8027', // orange - sales
  '#984ea3': '#CA62C4', // purple - other
  '#4daf4a': '#44D161', // green - ops
  '#377eb8': '#29A1E7', // blue - tech
  '#E77BB0': '#F781BF', // pink - marketing
  '#a65628': '#CB623C', // brown - support
  '#aaaaaa': '#C4C4C4', // grey - external
};

let chart;
let showDonuts = true;
let showNodesWithOneLink = true;
let layoutName = 'structural';
let brightSegment = {
  id: null,
  donutId: null,
  originalColour: null,
};

const interactionFormElement = document.getElementById('rhsForm');

/* HELPER FUNCTIONS FOR TOOLTIP BEGIN */
const tooltipElement = document.getElementById('tooltip');

// Determines which (45 degree rotated) quadrant a position lies within
function findQuadrant(item, x, y) {
  // Calculate vector from item centre to position
  const itemCentre = chart.viewCoordinates(item.x, item.y);
  const toPositionCoords = {
    x: x - itemCentre.x,
    y: y - itemCentre.y,
  };

  // Determine quadrant using gradient. The dividing lines between quadrants have gradient +/-1
  const gradient = Math.abs(toPositionCoords.y / toPositionCoords.x);
  if (gradient <= 1 && toPositionCoords.x >= 0) return 'right';
  if (gradient <= 1 && toPositionCoords.x < 0) return 'left';
  if (gradient > 1 && toPositionCoords.y >= 0) return 'bottom';
  return 'top';
}

// Calculates the radial distance between the node centre and the donut segment centre
function distanceToTooltip(node) {
  return (BASE_NODE_RADIUS + node.donut.bw + (node.donut.w / 2)) * (node.e || 1);
}

// Returns the hover position shifted radially to the segment centre
function shiftToSegmentCentre(hoverX, hoverY, node) {
  // Calculate vector from node centre to hover event position
  const nodeCentre = chart.viewCoordinates(node.x, node.y);
  const toHoverCoords = {
    x: hoverX - nodeCentre.x,
    y: hoverY - nodeCentre.y,
  };

  const initialLength = Math.sqrt((toHoverCoords.x ** 2) + (toHoverCoords.y ** 2));
  const scaleFactor = distanceToTooltip(node) / initialLength;

  // The correction vector from the hover event position to the segment centre
  const toCorrectedCoords = {
    x: toHoverCoords.x * scaleFactor,
    y: toHoverCoords.y * scaleFactor,
  };

  return chart.viewCoordinates(node.x + toCorrectedCoords.x, node.y + toCorrectedCoords.y);
}

// Offsets the position such that the tooltip arrow aligns correctly
function compensatePosition(tooltip, quadrant, position) {
  const newPosition = {};
  switch (quadrant) {
    case 'right':
      newPosition.x = position.x + TOOLTIP_ARROW_SIZE;
      newPosition.y = position.y - (tooltip.clientHeight / 2);
      break;
    case 'left':
      newPosition.x = position.x - (tooltip.clientWidth + TOOLTIP_ARROW_SIZE);
      newPosition.y = position.y - (tooltip.clientHeight / 2);
      break;
    case 'bottom':
      newPosition.x = position.x - (tooltip.clientWidth / 2);
      newPosition.y = position.y + TOOLTIP_ARROW_SIZE;
      break;
    case 'top':
      newPosition.x = position.x - (tooltip.clientWidth / 2);
      newPosition.y = position.y - (tooltip.clientHeight + TOOLTIP_ARROW_SIZE);
      break;
    default:
      break;
  }
  return newPosition;
}

// Populates the tooltip with hover information
function populateTooltip(label, percentage, direction) {
  // Reset the tooltip class list and append the current direction
  tooltipElement.className = 'popover';
  tooltipElement.classList.add(`${direction}`);

  // Fill in label and percentage text
  document.getElementById('tooltip-label').innerText = `${label}:`;
  document.getElementById('tooltip-percentage').innerText = `${percentage}%`;
}

// Fills the tooltip with relevant details and subsequently positions it
function populateAndPositionTooltip(x, y, item, donutId) {
  const total = item.donut.v.reduce((a, b) => a + b, 0);
  const percentage = Math.round((item.donut.v[donutId] / total) * 100);
  const quadrant = findQuadrant(item, x, y);

  // Add label, percentage and quadrant information to tooltip HTML
  populateTooltip(colourToRoles[item.donut.c[donutId]], percentage, quadrant);

  // Get position of hover when snapped to segment centre
  const segmentCentrePosition = shiftToSegmentCentre(x, y, item);

  // Tweak position to ensure tooltip arrow points to segmentCentrePosition
  const position = compensatePosition(tooltipElement, quadrant, segmentCentrePosition);

  // Update tooltip position with calculated values
  tooltipElement.style.left = `${position.x}px`;
  tooltipElement.style.top = `${position.y}px`;
}

// Hides the tooltip by setting the visibility to hidden
function closeTooltip() {
  if (tooltipElement) tooltipElement.style.visibility = 'hidden';
}

// Shows the tooltip by setting the visibility to visible
function openTooltip() {
  if (tooltipElement) tooltipElement.style.visibility = 'visible';
}
/* HELPER FUNCTIONS FOR TOOLTIP END */

// Performs a layout
async function doLayout() {
  await chart.layout(layoutName);
}

// Reveals or hides donuts on all nodes
async function showHideDonuts() {
  const updatedProperties = [];
  chart.each({ type: 'node' }, (node) => {
    updatedProperties.push({
      id: node.id,
      donut: {
        w: showDonuts ? node.d.w : 0,
        bw: showDonuts ? 2 : 0,
      },
    });
  });

  await chart.animateProperties(updatedProperties, { time: 250 });
}

// Filters the nodes based on selected options
async function filterNodes() {
  if (showNodesWithOneLink) {
    // Reveal all nodes
    await chart.filter(() => true);
  } else {
    // Filter out nodes with a degree less than or equal to 1
    const degrees = chart.graph().degrees();
    await chart.filter(node => degrees[node.id] > 1, { type: 'node' });
  }
  await doLayout();
}

// Replaces the colour of the desired donut segment with a highlight counterpart
function makeSegmentBrighter(item, donutId) {
  const donut = item.donut;
  const originalColour = donut.c[donutId];
  brightSegment = { id: item.id, donutId, originalColour };
  donut.c[donutId] = highlightColours[originalColour];
  chart.setProperties({ id: item.id, donut });
}

// Reverts the previously brightened donut segment (if any)
function clearBrightening() {
  const item = chart.getItem(brightSegment.id);
  if (item) {
    const donut = item.donut;
    donut.c[brightSegment.donutId] = brightSegment.originalColour;
    chart.setProperties({ id: brightSegment.id, donut });
  }
}

// If the provided sub item is a donut segment, it is brightened and a tooltip is shown
function highlightSegmentAndShowTooltip({ id, x, y, subItem }) {
  clearBrightening();
  const item = chart.getItem(id);
  if (item && subItem.type === 'donut') {
    makeSegmentBrighter(item, subItem.index);
    populateAndPositionTooltip(x, y, item, subItem.index);
    openTooltip();
  } else {
    closeTooltip();
  }
}

// Enables or disables interaction with the chart controls
function disableInteraction(disable) {
  interactionFormElement.style.pointerEvents = disable ? 'none' : 'auto';
}

// Toggles any number of classes on a given element
function toggleClasses(element, ...classes) {
  classes.forEach(c => element.classList.toggle(c));
}

// Inverts the active class name for all buttons in a parent container
function swapButtons(parentId) {
  const btns = document.getElementById(parentId).getElementsByClassName('btn');
  Array.from(btns).forEach(btn => toggleClasses(btn, 'active', 'btn-kl'));
}

// Handler for donut visibility button group
async function onDonutInputChange(shouldShow) {
  if (shouldShow !== showDonuts) {
    disableInteraction(true);
    showDonuts = !showDonuts;
    swapButtons('donut-btns');
    await showHideDonuts();
    disableInteraction(false);
  }
}

// Handler for single link visibility button group
async function onOneLinkInputChange(shouldShow) {
  if (shouldShow !== showNodesWithOneLink) {
    disableInteraction(true);
    showNodesWithOneLink = !showNodesWithOneLink;
    swapButtons('onelink-btns');
    await filterNodes();
    disableInteraction(false);
  }
}

// Handler for layout selection button group
async function onLayoutInputChange(newLayout) {
  if (newLayout !== layoutName) {
    disableInteraction(true);
    layoutName = newLayout;
    swapButtons('layout-btns');
    await doLayout();
    disableInteraction(false);
  }
}

function foregroundSelectedItems() {
  const selection = chart.selection();
  // If applicable, foreground the items neighbouring the selection
  if (selection.length > 0) {
    const nodesToForeground = chart.graph().neighbours(selection).nodes.concat(selection);
    chart.foreground(node => nodesToForeground.includes(node.id));
  } else {
    chart.foreground(() => true);
  }
}

function attachEventHandlers() {
  // Attach event listeners for button pairs
  document.getElementById('btn-show-donuts').addEventListener('click', () => onDonutInputChange(true));
  document.getElementById('btn-hide-donuts').addEventListener('click', () => onDonutInputChange(false));
  document.getElementById('btn-show-onelink').addEventListener('click', () => onOneLinkInputChange(true));
  document.getElementById('btn-hide-onelink').addEventListener('click', () => onOneLinkInputChange(false));
  document.getElementById('btn-organic-layout').addEventListener('click', () => onLayoutInputChange('organic'));
  document.getElementById('btn-structural-layout').addEventListener('click', () => onLayoutInputChange('structural'));

  // Attach handler to selection change event
  chart.on('selection-change', foregroundSelectedItems);
  // Attach handler to pointer-move, so when  pointer is over a donut segment,
  // we highlight and show a tooltip
  chart.on('pointer-move', highlightSegmentAndShowTooltip);
  // Close the tooltip to prevent it from pointing to the wrong position
  chart.on('view-change', closeTooltip);
}

async function loadKeyLines() {
  KeyLines.promisify();
  const options = {
    logo: { u: 'images/Logo.png' },
    iconFontFamily: 'Font Awesome 5 Free Solid',
    handMode: true,
    hover: 5, // Trigger the hover event with a 5ms delay
  };
  chart = await KeyLines.create({ container: 'klchart', options });
  chart.load(data);
  doLayout();
  attachEventHandlers();
}

function loadFontsAndStart() {
  WebFont.load({
    custom: {
      families: ['Font Awesome 5 Free Solid'],
    },
    active: loadKeyLines, // Start KeyLines if all the fonts have been successfully loaded
    inactive: loadKeyLines, // Start KeyLines otherwise
    timeout: 3000,
  });
}

window.addEventListener('DOMContentLoaded', loadFontsAndStart);
