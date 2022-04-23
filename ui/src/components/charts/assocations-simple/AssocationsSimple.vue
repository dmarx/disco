<template>
  <KlChart
    :containerClass="'chart-container'"
    :id="'kl-chart-mafia'"
    ref="visibleChart"
    :data="chartData"
    :options="chartOptions"
    @kl-ready="onKlReady"
    @kl-selection-change="onSelectionChange"
  ></KlChart>
  <div class="controloverlay">
    <ul>
      <li>
        <a id="home" rel="tooltip" title="Home">
          <i class="fa fa-home"></i>
        </a>
      </li>
      <li>
        <a id="layout" rel="tooltip" title="Layout chart">
          <i class="fa fa-random"></i>
        </a>
      </li>
      <li>
        <a id="changeMode" rel="tooltip" title="Drag mode">
          <i class="fa fa-arrows-alt" id="iconMode"></i>
        </a>
      </li>
      <li>
        <a id="zoomIn" rel="tooltip" title="Zoom in">
          <i class="fa fa-plus-square"></i>
        </a>
      </li>
      <li>
        <a id="zoomOut" rel="tooltip" title="Zoom out">
          <i class="fa fa-minus-square"></i>
        </a>
      </li>
    </ul>
  </div>
  <div style="display:none">
    <KlChart
      :containerClass="'chart-container'"
      :id="'kl-chart-hidden'"
      ref="hiddenChart"
      :data="chartData"
      :options="chartOptions"
    ></KlChart>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";

import KlChart from "keylines/vue/Chart.vue";
import { data } from './mafia-data.js';
import Dropdown2 from "@/components/dropdown/Dropdown2.vue";

export default defineComponent({
  name: "chart-mafia-map",
  // props: {
  //   cardClasses: String,
  // },
  components: {
    KlChart,
    Dropdown2
  },
  // mounted(){

  // },
  setup() {
    // const chart = ref();

    var visibleChart = ref();
    let hiddenChart = ref();
    let savedChartItems;
    let nodeSelection: any[] = [];
    let nodeIdsRemovedBySlider: any[] = [];
    let allNodeIds: any[] = [];
    const familyIdsCache = {};
    const allNodeIdsLookup = {};
    // Stacks to maintain the order of items filtered by manual selection and the slider
    let manuallyRemovedStack: any[] = [];
    let sliderStack: any[] = [];
    // Get elements from the UI


    const familyCheckBoxesEls: any[] = [];
    const largestCompSizeEl = ref();//document.getElementById('lcc');

    console.log(familyCheckBoxesEls);
    const chartData = data;

    const chartOptions = {
      backColour: "transparent",
      fontFamily: "Spartan, sans-serif",
      fontSize: 10,
      fontColor: "#000000",
      animate: true,
      time: 800,
      transition: "layout",
      arrows: 'normal',
      handMode: true,
      navigation: { shown: false },
      overview: { icon: false },
      // selectedNode: {
      //   c: colours.selected,
      //   b: colours.selected,
      //   fbc: colours.selected,
      // },
      // selectedLink: {
      //   c: colours.selected,
      // },
    };

    return {
      // chart,
      chartOptions,
      chartData,

      visibleChart,
      hiddenChart,
      savedChartItems,
      nodeSelection,
      nodeIdsRemovedBySlider,
      allNodeIds,
      familyIdsCache,
      allNodeIdsLookup,
      manuallyRemovedStack,
      sliderStack,
      familyCheckBoxesEls,
      largestCompSizeEl,
    };
  },
  async mounted() {

    let checkboxes: any[] = (document.getElementsByClassName('checkbox-mafia') as any);//('input[type=checkbox]') as any);
    console.log(checkboxes);
    this.familyCheckBoxesEls = [...checkboxes];

    this.initialiseInteractions();



    // this.runLayout(true, 'full');
    // Chart overlay
    // this.registerClickHandler('home', () => {
    //   this.doZoom('fit');
    // });
    // this.registerClickHandler('zoomIn', () => {
    //   this.doZoom('in');
    // });
    // this.registerClickHandler('zoomOut', () => {
    //   this.doZoom('out');
    // });
    // this.registerClickHandler('changeMode', () => {
    //   const hand = !!this.chart.options().handMode; // be careful with undefined
    //   this.chart.options({ handMode: !hand });

    //   const icon = document.getElementById('iconMode');
    //   (icon as any).classList.toggle('fa-arrows-alt');
    //   (icon as any).classList.toggle('fa-edit');
    // });
    // this.registerClickHandler('layout', () => {
    //   this.runLayout(true, 'full');
    // });


    // KeyLines.promisify();
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
    // [this.visibleChart, this.hiddenChart] = await KeyLines.create([
    //   { container: 'klchart', options },
    //   { container: 'hiddenChart' }]);
    // this.visibleChart.load(data);
    // this.hiddenChart.load(data);
    // Set the size of each node by normalized degree score



  },
  updated() {
    console.log('updated');
  },
  methods: {

    setButtonAvailability(element, available) {
      element.classList[available ? 'add' : 'remove'](['active', 'btn-kl']);
      element.disabled = !available;
    },

    setLargestComponentSize() {
      const components = this.visibleChart.component.graph().components();
      this.largestCompSizeEl.innerText = components.length
        ? components.reduce((a, b) => ((b.nodes.length < a.nodes.length) ? a : b)).nodes.length
        : 0;
    },
    setNodeState(nodeIds, property, state) {
      nodeIds.forEach((id) => {
        this.allNodeIdsLookup[id][property] = state;
      });
    },
    setNodesManuallySelected(newSelectedNodes) {
      // Clear the previously selected nodes
      if (this.nodeSelection.length) {
        this.setNodeState(this.nodeSelection, 'filterState', true);
        this.nodeSelection = [];
      }
      if (newSelectedNodes.length) {
        // Prepare selected nodes to be removed
        this.nodeSelection = newSelectedNodes;
        this.setNodeState(newSelectedNodes, 'filterState', false);
        // Highlight neighbours of selected items
        const neighbours = this.visibleChart.component.graph().neighbours(newSelectedNodes).nodes;
        this.visibleChart.component.foreground(node => newSelectedNodes.includes(node.id)
          || neighbours.includes(node.id));
        // Allow selected nodes to be removed
      } else {
        // No nodes selected
        this.visibleChart.component.selection([]);
        this.visibleChart.component.foreground(() => true);
      }
    },
    async pingNodes(allNodeIdsToRemove, primaryNodeIds) {
      const collateralNodeIdsToRemove = allNodeIdsToRemove.filter(id => !primaryNodeIds.includes(id));
      if (collateralNodeIdsToRemove.length) {
        // Primary removed nodes ping blue
        this.visibleChart.component.ping(allNodeIdsToRemove, { time: 1200, c: '#5d81f8' });
        // Collateral nodes ping red
        await this.visibleChart.component.ping(collateralNodeIdsToRemove, { time: 1200, c: '#FF0000' });
      } else {
        await this.visibleChart.component.ping(allNodeIdsToRemove, { time: 1200, c: '#5d81f8' });
      }
    },
    async getItemsFromFilter() {
      const matchFilter = (node: any) => {
        return this.allNodeIdsLookup[node.id].familyCheckbox && this.allNodeIdsLookup[node.id].filterState;
      }
      // Filter the hidden chart and return the items to be removed or expanded into visible chart
      const { shown, hidden } = await this.visibleChart.component.filter(matchFilter, { type: 'node', animate: false, hideSingletons: true });
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
    },
    async doFiltering(filteredBy: any = "") {
      // Disable the UI while visible chart is updated
      // Get items to be expanded or removed
      const {
        nodesShown: nodeIdsToExpand,
        nodesHidden: nodeIdsToRemove,
        itemsShown: itemIdsToExpand,
        itemsHidden: itemIdsToRemove,
      } = await this.getItemsFromFilter();
      if (itemIdsToExpand.length) {
        // Allow expanded items to be available for filtering on the slider
        this.setNodeState(nodeIdsToExpand, 'sliderAvailability', true);
        // Retrieve saved item so we can expand with the correct node size
        const itemsToExpand = this.savedChartItems.filter(item => itemIdsToExpand.includes(item.id));
        await this.visibleChart.expand(itemsToExpand, { layout: { name: 'organic', fit: true } });
      } else if (itemIdsToRemove.length) {
        let primaryNodesToHide;
        // Check which filter was used and identify primary nodes for correct ping colour
        if (filteredBy === 'selected') {
          this.manuallyRemovedStack.push(nodeIdsToRemove);
          primaryNodesToHide = this.nodeSelection;
          // Remove the node selection so that the remove animation is consistent with other filters
          this.nodeSelection = [];
          this.setNodesManuallySelected([]);
        } else if (['batanesi', 'mistretta', 'none'].includes(filteredBy)) {
          primaryNodesToHide = this.familyIdsCache[filteredBy];
        } else if (filteredBy === 'slider') {
          primaryNodesToHide = this.nodeIdsRemovedBySlider;
        }
        // Make removed nodes unavailable to the slider
        this.setNodeState(nodeIdsToRemove, 'sliderAvailability', false);
        // Ping nodes to be removed
        await this.pingNodes(nodeIdsToRemove, primaryNodesToHide);
        // Remove items from the visible chart
        await this.visibleChart.component.removeItem(nodeIdsToRemove);
        // Layout items
        await this.visibleChart.component.layout('organic', { mode: 'adaptive' });
      }
      // Update the slider for the nodes remaining on the visible chart
      // Update the largest component indicator
      this.setLargestComponentSize();
      // Enable the UI after the visible chart has been updated
    },
    initialiseInteractions() {
      const sliderValueEl = document.getElementById('sliderValue');
      // Filter the chart when any checkbox is changed
      this.familyCheckBoxesEls.forEach((checkbox) => {
        checkbox.addEventListener('click', (event) => {
          let familyIdsToBeFiltered;
          const familyName = event.target.id;
          const familyChecked = event.target.checked;
          this.setNodesManuallySelected([]);
          // Check if family has been filtered before
          if (this.familyIdsCache[familyName]) {
            familyIdsToBeFiltered = this.familyIdsCache[familyName];
          } else {
            // Get the family ids and cache the ids for later use
            familyIdsToBeFiltered = this.allNodeIds
              .filter(id => this.allNodeIdsLookup[id].family === familyName);
            this.familyIdsCache[familyName] = familyIdsToBeFiltered;
          }
          this.setNodeState(familyIdsToBeFiltered, 'familyCheckbox', familyChecked);
          this.doFiltering(familyName);
        });
      });
      // this.visibleChart.component.on('selection-change', () => {
      //   const selectedItems = this.visibleChart.component.selection();
      //   // Filter selection to include only nodes
      //   const newSelectedNodes = selectedItems.filter(id => !id.match(/-/));
      //   this.setNodesManuallySelected(newSelectedNodes);
      // });
      // Remove manually selected nodes


    },
    // Set the lookup for the ranking and availability of each node for the slider
    setNodesIdsLookup(sizedNodes) {
      // All node ids sorted by degree score
      this.allNodeIds = sizedNodes
        .sort((nodeA, nodeB) => nodeB.e - nodeA.e)
        .map(node => node.id);
      this.allNodeIds.forEach((id, index) => {
        this.allNodeIdsLookup[id] = {
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
      this.savedChartItems.forEach((item) => {
        if (item.type === 'node') {
          this.allNodeIdsLookup[item.id].family = item.d.family;
        }
      });
    },
    // Helper to normalize degrees score
    getResizeArray(values) {
      const valuesArray: number[] = Object.values(values);
      const max = Math.max.apply(null, valuesArray);
      const min = Math.min.apply(null, valuesArray);
      const resizeArray = Object.keys(values).map(id => ({
        id,
        e: (values[id] - min) / (max - min) * 2 + 1,
      }));
      return resizeArray;
    },
    doZoom(name) {
      this.visibleChart.component.zoom(name, { animate: true, time: 350 });
    },
    async setNodesSize() {
      console.log('setNodeSize', this.visibleChart, this.visibleChart.component)
      const degreeScores = await this.visibleChart.component.graph().degrees({ value: 'total' });
      const resizeValues = this.getResizeArray(degreeScores);
      this.visibleChart.component.setProperties(resizeValues);
      // Save the chart to retrieve nodes sizes when filtering them back in.
      this.savedChartItems = this.visibleChart.component.serialize().items;
      return resizeValues;
    },
    async runLayout(inconsistent, mode) {
      const packing = mode === 'adaptive' ? 'adaptive' : 'circle';
      return this.visibleChart.component.layout('organic', {
        time: 500, tightness: 4, consistent: !inconsistent, packing, mode,
      });
    },
    fit() {
      this.visibleChart.component.zoom('fit', { animate: true }).then(this.runLayout);
      // this.doZoom('in');
      // this.doZoom('in');
    },
    // async startKeyLines() {
    //   KeyLines.promisify();
    //   const options = {
    //     logo: {
    //       u: 'images/Logo.png',
    //     },
    //     selectedNode: {
    //       ha0: {
    //         c: '#5d81f8',
    //         r: 35,
    //         w: 15,
    //       },
    //     },
    //     selectedLink: {},
    //   };
    //   [this.visibleChart, this.hiddenChart] = await KeyLines.create([
    //     { container: 'klchart', options },
    //     { container: 'hiddenChart' }]);
    //   this.visibleChart.load(data);
    //   this.hiddenChart.load(data);
    //   // Set the size of each node by normalized degree score
    //   const nodesSizedByDegree = await this.setNodesSize();
    //   // Set the order of nodes ids to be filtered for the slider
    //   this.setNodesIdsLookup(nodesSizedByDegree);
    //   // Set nodes to be filtered by the slider
    //   this.setIdsForSliderStack();
    //   this.visibleChart.layout('organic', { consistent: true, packing: 'adaptive' });
    //   this.initialiseInteractions();
    //   this.setLargestComponentSize();
    // },





    onSelectionChange() {
      const selectedItems = this.visibleChart.component.selection();
      // Filter selection to include only nodes
      const newSelectedNodes = selectedItems.filter(id => !id.match(/-/));
      this.setNodesManuallySelected(newSelectedNodes);
    },

    registerClickHandler(id, fn) {
      document.getElementById(id)!.addEventListener('click', fn);
    },


    async onKlReady(charts) {


      const nodesSizedByDegree = await this.setNodesSize();
      // Set the order of nodes ids to be filtered for the slider
      this.setNodesIdsLookup(nodesSizedByDegree);
      // Set nodes to be filtered by the slider
      this.visibleChart.component.layout('organic', { consistent: true, packing: 'adaptive' });
      // this.setLargestComponentSize();
      //[this.chart, this.miniChart] = charts;





      this.registerClickHandler('home', () => {
        this.doZoom('fit');
      });
      this.registerClickHandler('zoomIn', () => {
        this.doZoom('in');
      });
      this.registerClickHandler('zoomOut', () => {
        this.doZoom('out');
      });
      this.registerClickHandler('changeMode', () => {
        const hand = !!this.visibleChart.component.options().handMode; // be careful with undefined
        this.visibleChart.component.options({ handMode: !hand });

        const icon = document.getElementById('iconMode');
        icon!.classList.toggle('fa-arrows-alt');
        icon!.classList.toggle('fa-edit');
      });
      this.registerClickHandler('layout', () => {
        this.runLayout(true, 'full');
      });


      // this.chart.component.load(data);
      // console.log('loading', data, this.chart);
      // this.chart.component.zoom('fit', { animate: true }).then(() => {
      //   this.runLayout(true, 'full');
      // });
      // this.runLayout();

      // On selection change:
      //   1) add styles to the targeted and neighbouring items
      //   2) copy the selected item and its neighbours to the miniChart
      // this.chart.on('selection-change', () => {

      // });

      // data is defined in filtermap-data.js
      // console.log("chart");
      // console.log(this.chart);
      // console.log(this.chart.component);


      // const baseOpts = {
      //   arrows: 'normal',
      //   handMode: true,
      //   navigation: { shown: false },
      //   overview: { icon: false },
      //   selectedNode: {
      //     c: colours.selected,
      //     b: colours.selected,
      //     fbc: colours.selected,
      //   },
      //   selectedLink: {
      //     c: colours.selected,
      //   },
      // };

      // const mainChartConfig = {
      //   container: 'klchart',
      //   options: Object.assign({}, baseOpts, {
      //     drag: {
      //       links: false,
      //     },
      //     logo: { u: 'images/Logo.png' },
      //   }),
      // .chart - container {
      //   height: 100 %;
      // }
      //   container: 'minikl',
      //   options: baseOpts,
      // };


    },
  },
});
</script>

<style scoped>
.chart-container {
  height: 100%;
}

.sliderContainer {
  width: 100%;
}
dl {
  margin: 0px;
}
dl dt {
  color: #fff;
  float: left;
  font-weight: bold;
  margin-left: 0px;
  margin-right: 10px;
  margin-block-start: 0em;
  padding: 3px;
  width: 22px;
  height: 22px;
  border-radius: 22px;
  line-height: 12px;
  border: 0;
}
dl dd {
  margin: 2px 0;
  padding: 5px 0;
  line-height: 12px;
  font-size: 12px;
}
.batanesi dt {
  background-color: #03d8ae;
}
.mistretta dt {
  background-color: #0e0e0e;
}
.none dt {
  background-color: white;
}
.controloverlay {
    position: absolute;
    right: 8px;
    bottom: 0;
    padding: 12px;
    /* margin: 0; */
    font-size: 28px;
    z-index: 9001;
    background-color: rgba(250, 250, 250, 0.8);
    border: NONE;
    /* box-shadow: 1px 1px 0px rgb(0 0 0 / 10%); */
    border-left: 0;
    border-top: 0;
    border-radius: 8px;
    left: auto;
    top: auto;
}

</style>
