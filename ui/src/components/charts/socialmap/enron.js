//
//     Copyright © 2011-2022 Cambridge Intelligence Limited.
//     All rights reserved.
//
//     Sample Code
//!    Investigate social structures and relations in complex email data.

import { data, colours } from './enron-data.js';

let chart;
let miniChart;
let restoreIds = [];

// Track UI state
const state = {
  sizeBy: 'same',
  volume: 'off',
  direction: 'any',
};

const colourMap = {};

/**
 * debounce - This function delays execution of the passed "fn" until "timeToWait" milliseconds
 * have passed since the last time it was called.  This ensures that the function
 * runs at the end of a particular action to keep performance high.
 */
function debounce(fn, timeToWait = 100) {
  let timeoutId;
  return function debouncedFn(...args) {
    const timeoutFn = () => {
      timeoutId = undefined;
      fn.apply(this, args);
    };
    if (timeoutId !== undefined) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(timeoutFn, timeToWait);
  };
}

// ensure that this doesn't get called too often when dragging the selection
// marquee
const loadMiniChart = debounce((items) => {
  miniChart.load({
    type: 'LinkChart',
    items,
  });
  miniChart.layout('organic', { consistent: true });
});

function isLink(id) {
  return id.match('-');
}

function updateHighlight(itemIds) {
  const props = [];

  // Remove previous styles
  if (restoreIds) {
    props.push(
      ...restoreIds.map((id) => {
        const colour = colourMap[id] || (isLink(id) ? colours.link : colours.node);
        return {
          id,
          c: colour,
          b: colour,
          ha0: null,
        };
      }),
    );
    restoreIds = [];
  }

  // Add new styles
  if (itemIds.length) {
    // Find the neighbours of the provided items
    const toHighlight = [];
    itemIds.forEach((id) => {
      if (isLink(id)) {
        const link = chart.getItem(id);
        toHighlight.push(id, link.id1, link.id2);
      } else {
        const neighbours = chart.graph().neighbours(id);
        toHighlight.push(id, ...neighbours.nodes, ...neighbours.links);
      }
    });

    // For each neighbouring item, add some styling
    toHighlight.forEach((id) => {
      // Cache the existing styles
      restoreIds.push(id);

      // Generate new styles
      const style = {
        id,
      };
      if (isLink(id)) {
        // For links, just set the colour
        style.c = colours.selected;
      } else {
        // For nodes, add a halo
        style.ha0 = {
          c: colours.selected,
          r: 34,
          w: 6,
        };
      }
      props.push(style);
    });
  }

  chart.setProperties(props);
}

async function runLayout(inconsistent, mode) {
  const packing = mode === 'adaptive' ? 'adaptive' : 'circle';
  return chart.layout('organic', {
    time: 500, tightness: 4, consistent: !inconsistent, packing, mode,
  });
}

function klReady(charts) {
  [chart, miniChart] = charts;


  chart.load(data);
  chart.zoom('fit', { animate: false }).then(runLayout);

  // On selection change:
  //   1) add styles to the targeted and neighbouring items
  //   2) copy the selected item and its neighbours to the miniChart
  chart.on('selection-change', () => {
    const ids = chart.selection();

    updateHighlight(ids);

    const miniChartItems = [];

    if (ids.length > 0) {
      const { nodes, links } = chart.graph().neighbours(ids);

      chart.each({ type: 'node' }, (node) => {
        if (ids.includes(node.id) || nodes.includes(node.id)) {
          // Clear hover styling and position
          node.x = 0;
          node.y = 0;
          delete node.ha0;
          miniChartItems.push(node);
        }
      });

      chart.each({ type: 'link' }, (link) => {
        if (ids.includes(link.id) || links.includes(link.id)) {
          link.c = colours.link;
          miniChartItems.push(link);
        }
      });
    }
    loadMiniChart(miniChartItems);
  });
}

// this function picks a colour from a range of colours based on the value
function colourPicker(value) {
  const { bands, node } = colours;
  if (value > 0.75) {
    return bands[2];
  }
  if (value > 0.5) {
    return bands[1];
  }
  if (value > 0.25) {
    return bands[0];
  }
  return node;
}

function normalize(max, min, value) {
  if (max === min) {
    return min;
  }

  return (value - min) / (max - min);
}

function miniChartFilter(items) {
  return items.filter(({ id }) => miniChart.getItem(id));
}

async function animateValues(values) {
  const valuesArray = Object.values(values);

  const max = Math.max(...valuesArray);
  const min = Math.min(...valuesArray);

  const items = Object.entries(values).map(([id, value]) => {
    // Normalize the value in the range 0 -> 1
    const normalized = normalize(max, min, value);

    // enlarge nodes with higher values
    const e = Math.max(1, normalized * 5);

    // Choose a colour (use bands if there is a range of values)
    const c = max !== min ? colourPicker(normalized) : colours.node;
    colourMap[id] = c;

    return { id, e, c, b: c };
  });

  await chart.animateProperties(items, { time: 500 });
  await runLayout(undefined, 'adaptive');

  const miniItems = miniChartFilter(items);
  await miniChart.animateProperties(miniItems, { time: 500 });
  return miniChart.layout('organic', { consistent: true });
}

function same() {
  return new Promise((resolve) => {
    const sizes = {};
    chart.each({ type: 'node' }, (node) => {
      sizes[node.id] = 0;
    });
    resolve(sizes);
  });
}

function wrapCallback(fn) {
  return options => new Promise(resolve => resolve(fn(options)));
}

function getAnalysisFunction(name) {
  if (name.match(/^(degrees|pageRank|eigenCentrality)$/)) {
    return wrapCallback(chart.graph()[name]);
  }
  if (name.match(/^(closeness|betweenness)$/)) {
    return chart.graph()[name];
  }
  return same;
}

async function analyseChart() {
  const { sizeBy, volume } = state;

  const options = {};
  // Configure weighting
  if (volume === 'on') {
    if (sizeBy.match(/^(betweenness|closeness)$/)) {
      options.weights = true;
    }
    options.value = 'count';
  }
  // Configure direction options
  if (sizeBy.match(/^(betweenness|pageRank)$/)) {
    options.directed = state.direction !== 'any';
  } else {
    options.direction = state.direction;
  }

  const analyse = getAnalysisFunction(sizeBy);
  const values = await analyse(options);
  return animateValues(values);
}

function calculateLinkWidths(showValue) {
  const links = [];
  chart.each({ type: 'link' }, (link) => {
    const linkcount = link.d.count;
    let width = 1;
    if (showValue) {
      if (linkcount > 300) {
        width = 36;
      } else if (linkcount > 200) {
        width = 27;
      } else if (linkcount > 100) {
        width = 18;
      } else if (linkcount > 50) {
        width = 9;
      }
    }
    links.push({ id: link.id, w: width });
  });
  return links;
}

function doZoom(name) {
  chart.zoom(name, { animate: true, time: 350 });
}

function registerClickHandler(id, fn) {
  document.getElementById(id).addEventListener('click', fn);
}

function updateActiveState(nodes, activeValue) {
  nodes.forEach((node) => {
    if (node.value === activeValue) {
      node.classList.add('active');
    } else {
      node.classList.remove('active');
    }
  });
}

function registerButtonGroup(className, handler) {
  const nodes = document.querySelectorAll(`.${className}`);
  nodes.forEach((node) => {
    node.addEventListener('click', () => {
      const { value } = node;
      updateActiveState(nodes, value);

      handler(value);
    });
  });
}

function initUI() {
  // Chart overlay
  registerClickHandler('home', () => {
    doZoom('fit');
  });
  registerClickHandler('zoomIn', () => {
    doZoom('in');
  });
  registerClickHandler('zoomOut', () => {
    doZoom('out');
  });
  registerClickHandler('changeMode', () => {
    const hand = !!chart.options().handMode; // be careful with undefined
    chart.options({ handMode: !hand });

    const icon = document.getElementById('iconMode');
    icon.classList.toggle('fa-arrows-alt');
    icon.classList.toggle('fa-edit');
  });
  registerClickHandler('layout', () => {
    runLayout(true, 'full');
  });

  // Right hand menu
  registerButtonGroup('volume', async (volume) => {
    state.volume = volume;

    const links = calculateLinkWidths(volume === 'on');
    await chart.animateProperties(links);
    await analyseChart();

    const miniItems = miniChartFilter(links);
    miniChart.animateProperties(miniItems, { time: 500 }); // fire and forget
  });

  registerButtonGroup('size', (sizeBy) => {
    state.sizeBy = sizeBy;
    analyseChart();
  });

  registerButtonGroup('direction', (direction) => {
    state.direction = direction;
    analyseChart();
  });
}

function loadKeyLines() {
  initUI();

  KeyLines.promisify();

  const baseOpts = {
    arrows: 'normal',
    handMode: true,
    navigation: { shown: false },
    overview: { icon: false },
    selectedNode: {
      c: colours.selected,
      b: colours.selected,
      fbc: colours.selected,
    },
    selectedLink: {
      c: colours.selected,
    },
  };

  const mainChartConfig = {
    container: 'klchart',
    options: Object.assign({}, baseOpts, {
      drag: {
        links: false,
      },
      logo: { u: 'images/Logo.png' },
    }),
  };

  const miniChartConfig = {
    container: 'minikl',
    options: baseOpts,
  };

  KeyLines.create([mainChartConfig, miniChartConfig]).then(klReady);
}

window.addEventListener('DOMContentLoaded', loadKeyLines);
