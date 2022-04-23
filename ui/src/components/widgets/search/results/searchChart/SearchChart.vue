<template>
  <div class="row gy-5 gx-xl-8" style="height:100%;">
    <div class="col-xxl-9">
      <div
        class="card"
        style="background:url(/media/patterns/graph-bg.jpg) repeat;     background-size: 48px;"
      >
        <div class="card-body pt-2">
          <div class="chart-wrapper h-100">
            <KlChart
              :containerClass="'chart-container-big'"
              :id="'kl-chart-mafia'"
              ref="visibleChart"
              :data="chartData"
              :options="chartOptions"
              @kl-ready="onKlReady"
              @kl-selection-change="onSelectionChange"
              @kl-drag-move="onDragMove"
              @kl-hover="onHover"
              @kl-view-change="onViewChange"
            ></KlChart>
            <div id="tooltip-container" ref="tooltipContainer" style="position:absolute">
              <div
                class="popover right"
                id="tooltip"
                style="margin:0px; transform-origin:left;position: absolute; min-width: 70px; pointer-events: none;"
              >
                <div class="arrow"></div>
                <h2 class="popover-title">
                  <strong>{{ tooltipState.label }}</strong>
                </h2>
                <div class="popover-content" v-html="tooltipState.content"></div>
              </div>
            </div>
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
          </div>
        </div>
      </div>
    </div>
    <div class="col-xxl-3 h-100">
      <div class="card">
        <div class="card-header border-0">
          <h3 class="card-title fw-bolder text-dark">Options</h3>

          <div class="card-toolbar">
            <button
              type="button"
              class="btn btn-sm btn-icon btn-color-primary btn-active-light-primary"
              data-kt-menu-trigger="click"
              data-kt-menu-placement="bottom-end"
              data-kt-menu-flip="top-end"
            >
              <span class="svg-icon svg-icon-2">
                <inline-svg src="media/icons/duotune/general/gen024.svg" />
              </span>
            </button>
            <Dropdown2></Dropdown2>
          </div>
        </div>
        <div class="card-body pt-2">
          <div class="cicontent">
            <p>See options for the search and expansion below.</p>
            <!--   <fieldset>
              <legend>Categories</legend>
              <div class="form-check form-check-custom form-check-solid form-check-sm">
                <input
                  class="form-check-input checkbox-mafia"
                  type="checkbox"
                  id="batanesi"
                  checked
                />
                <label class="form-check-label" for="batanesi">People</label>
              </div>
              <div class="form-check form-check-custom form-check-solid form-check-sm">
                <input
                  class="form-check-input checkbox-mafia"
                  type="checkbox"
                  id="mistretta"
                  checked
                />
                <label class="form-check-label" for="mistretta">Objects</label>
              </div>
              <div class="form-check form-check-custom form-check-solid form-check-sm">
                <input class="form-check-input checkbox-mafia" type="checkbox" id="none" checked />
                <label class="form-check-label" for="none">Locations</label>
              </div>
            </fieldset>
            <br />-->
            <fieldset>
              <legend>
                Actions
                <br />
                <el-select
                  style="width:100%"
                  v-model="expandValue"
                  filterable
                  default-first-option
                  :reserve-keyword="false"
                  placeholder="Choose expand option..."
                >
                  <el-option
                    v-for="item in expandOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  ></el-option>
                </el-select>
                <br />
                <br />
                <input
                  class="btn btn-block btn-sm btn-primary"
                  type="button"
                  value="Expand Search"
                  id="expand"
                  ref="btnExpandSearch"
                  @click="expandSearch"
                  :disabled="expandValue == null"
                />&nbsp;
                <!-- <input
                  class="btn btn-block btn-sm btn-primary"
                  type="button"
                  value="Undo"
                  disabled
                  id="restore"
                  ref="restoreItemsButtonEl"
                />-->
              </legend>
            </fieldset>
            <br />
            <fieldset v-if="selectedItem">
              <legend>
                Selected
                <json-viewer :value="selectedItem.data" v-if="selectedItem.data"></json-viewer>
              </legend>
            </fieldset>
            <br />
            <!-- <fieldset>
              <legend>
                Remove
                <strong class="lead" id="sliderValue">0</strong>&nbsp;
                <strong class="lead">largest</strong>&nbsp;
                <strong class="lead">nodes</strong>
              </legend>
              <div>
                (based on degrees score)
                <div class="sliderGroup">
                  <div class="sliderContainer">
                    <input
                      id="slider"
                      ref="sliderEl"
                      type="range"
                      min="0"
                      max="20"
                      step="1"
                      value="0"
                    />
                  </div>
                </div>
              </div>
            </fieldset>
            <br />
            <div class="lead">
              Largest sub-network size:
              <strong class="lead" id="lcc" ref="largestCompSizeEl"></strong>
            </div>
            <br />-->
            <input
              class="span2 btn btn-kl btn-sm btn-primary"
              type="button"
              value="Reset network"
              id="resetAll"
              ref="resetAllEl"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, reactive, ref } from "vue";
import "leaflet/dist/leaflet.css";

import KlChart from "keylines/vue/Chart.vue";
import { data } from './mafia-data.js';
import L from "leaflet";
import Dropdown2 from "@/components/dropdown/Dropdown2.vue";
import JsonViewer from 'vue-json-viewer'

export default defineComponent({
  name: "chart-search",
  props: {
    resultsData: Object,
  },
  components: {
    KlChart,
    Dropdown2,
    JsonViewer
  },
  setup(props) {
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
    const selectedItem = reactive({ data: null });

    const templateHtml = "";
    const familyCheckBoxesEls: any[] = [];
    const largestCompSizeEl = ref();//document.getElementById('lcc');
    const btnExpandSearch = ref();//document.getElementById('restore');
    const restoreItemsButtonEl = ref();//document.getElementById('restore');
    const removeItemsButtonEl = ref();// document.getElementById('remove');
    const sliderEl = ref();//document.getElementById('slider');
    const resetAllEl = ref();//document.getElementById('resetAll');
    const tooltipContainer = ref();

    const chartData = {
      "type": "LinkChart",
      "items": []
    };

    // console.log(familyCheckBoxesEls);

    // const tooltipContainer = null;
    const tooltip = {
      itemId: null,
      element: null,
    };


    const expandValue = ref<string>();
    const expandOptionsAll: any[] = [
      {
        value: 'twitter_user',
        label: 'Twitter Find User',
      },
      {
        value: 'facebook_user',
        label: 'Facebook Find User',
      },
      {
        value: 'linkedin_user',
        label: 'LinkedIn Find User',
      },
    ];
    const expandOptions: any[] = [

    ];


    // Create the HTML code that is going to fill the tooltip
    const tooltipState = reactive({ label: "", content: "" });

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
      selectedItem,
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
      restoreItemsButtonEl,
      btnExpandSearch,
      removeItemsButtonEl,
      sliderEl,
      resetAllEl,

      templateHtml,
      tooltip,
      tooltipContainer,
      tooltipState,

      expandValue,
      expandOptions,
      expandOptionsAll
    };
  },
  async mounted() {
    this.chartData.items = this.getResultItemsFromData(this.$props.resultsData as any[])

    let checkboxes: any[] = (document.getElementsByClassName('checkbox-mafia') as any);//('input[type=checkbox]') as any);
    // console.log(checkboxes);
    this.familyCheckBoxesEls = [...checkboxes];

    this.initialiseInteractions();

    // this.templateHtml = (this.tt_html as any).innerHTML;
    // this.tooltipContainer = (this.tooltip_container);
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
    console.log('chart updated', this.$props.resultsData);
    //console.log('updated', this.$props.resultsData?.data, this.$props.resultsData?.data[0].id.toString(), this.chartData.items[0]['t']);
    const newItems = this.getResultItemsFromData(this.$props.resultsData as any[])

    if (newItems[0].id.toString() != this.chartData.items[0]['id']) {
      this.chartData.items = newItems;

      // this.runLayout(true, 'full');
      this.visibleChart.component.clear();
      this.visibleChart.component.expand(this.chartData.items, { layout: { name: 'organic', fit: true } });
    }

    console.log('chart updated finsihed', this.selectedItem);


  },
  methods: {

    getResultItemsFromData(results) {
      // var results = this.$props.resultsData as any[];
      if ((results[0]).pdl) {
        // console.log('Detected PDL data', results);
        return results.map(x => {
          var node = {
            "id": x.id.toString(),
            "type": "node",
            "tc": false,
            "c": "#94a1d1",
            "u": x.image_url != null ? x.image_url : "/media/icons/g-av-grey.png",
            "d": {
              "family": "none"
            },
            "fbc": "rgba(0,0,0,0)",
            "t": x.full_name,
            "fs": 10,
            "ci": true,
            "fc": "#000000"
          };
          return node;
        }) as any;
      } else if (this.$props.resultsData?.data != null) {
        // console.log('Detected SD data');
        return this.$props.resultsData.data.map(x => {
          var node = {
            "id": x.id.toString(),
            "type": "node",
            "tc": false,
            "c": "#94a1d1",
            "u": x.image_url != null ? x.image_url : "/media/icons/g-av-grey.png",
            "d": {
              "family": "none"
            },
            "fbc": "rgba(0,0,0,0)",
            "t": x.name,
            "fs": 10,
            "ci": true,
            "fc": "#000000"
          };
          return node;
        });
      }

    },
 
 
    expandSearch() {
      console.log('expanding', this.selectedItem);

      var myHeaders = new Headers();
      myHeaders.append("Authorization", "Token j2vtTtDVaChVhVex9GUsAyh3m8kUMFqWgHbMTnhEDTG");

      let url = ""
      let item = this.selectedItem.data as any;
      try {
        switch (this.expandValue) {
          case "twitter_user":
            url = "twitter/search?q=" + item.twitter_username + "&limit=25"
            // url = "twitter/users/" + item.twitter_username;
            break;
          case "facebook_user":
            url = "facebook/search?q=" + item.facebook_username + "&limit=25"
            // url = "facebook/users/" + item.facebook_username;
            break;
          case "linkedin_user":
            url = "linkedin/search?q=" + item.linkedin_username + "&limit=25"
            // url = "linkedin/users/" + item.linkedin_username;
            break;
        }
      }
      catch (e) { }

      fetch("https://api.socialnet.shadowdragon.io/" + url, {
        // fetch("https://api.socialnet.shadowdragon.io/facebook/users/123/friends?limit=25", {
        // fetch("https://api.socialnet.shadowdragon.io/facebook/users/1039861562", {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
      })
        .then(response => response.text())
        .then(result => {
          // console.log(result))

          console.log('got new items', this.selectedItem, result);
          //   this.chartData.items.forEach(x => {
          //     //if (x['id'] != newSelectedNodes[0]) {
          //     this.visibleChart.component.removeItem(x['id']);
          //     // }
          //   });


          //   var newData = JSON.parse((result as any));
          //   console.log(newData);
          //   var newItems = newData.data.map(x => {
          //     var node = {
          //       "id": x.id.toString(),
          //       "type": "node",
          //       "tc": false,
          //       "c": "#94a1d1",
          //       "u": x.image_url != null ? x.image_url : "/media/icons/g-av-grey.png",
          //       "d": {
          //         "family": "none"
          //       },
          //       "fbc": "rgba(0,0,0,0)",
          //       "t": x.name,
          //       "fs": 10,
          //       "ci": true,
          //       "fc": "#000000"
          //     };
          //     return node;
          //   });

          //   // this.runLayout(true, 'full');
          //   // this.visibleChart.component.clear();
          //   this.visibleChart.component.expand(newItems, { layout: { name: 'organic', fit: true } });
          //   console.log('bound new items', this.selectedItem);


        })
        .catch(error => console.log('error', error));

    },

    expandUsingSD(newSelectedNodes) {

      var myHeaders = new Headers();
      myHeaders.append("Authorization", "Token j2vtTtDVaChVhVex9GUsAyh3m8kUMFqWgHbMTnhEDTG");

      fetch("https://api.socialnet.shadowdragon.io/facebook/users/123/friends?limit=25", {
        // fetch("https://api.socialnet.shadowdragon.io/facebook/users/1039861562", {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
      })
        .then(response => response.text())
        .then(result => {
          // console.log(result))

          this.chartData.items.forEach(x => {
            if (x['id'] != newSelectedNodes[0]) {
              this.visibleChart.component.removeItem(x['id']);
            }
          });


          var newData = JSON.parse((result as any));
          console.log(newData);
          var newItems = newData.data.map(x => {
            var node = {
              "id": x.id.toString(),
              "type": "node",
              "tc": false,
              "c": "#94a1d1",
              "u": x.image_url != null ? x.image_url : "/media/icons/g-av-grey.png",
              "d": {
                "family": "none"
              },
              "fbc": "rgba(0,0,0,0)",
              "t": x.name,
              "fs": 10,
              "ci": true,
              "fc": "#000000"
            };
            return node;
          });

          // this.runLayout(true, 'full');
          // this.visibleChart.component.clear();
          this.visibleChart.component.expand(newItems, { layout: { name: 'organic', fit: true } });


        })
        .catch(error => console.log('error', error));

    },



    setButtonAvailability(element, available) {
      element.classList[available ? 'add' : 'remove'](['active', 'btn-kl']);
      element.disabled = !available;
    },
    setUIAvailability(available) {
      if (this.manuallyRemovedStack.length) {
        this.setButtonAvailability(this.restoreItemsButtonEl, available);
      }
      this.familyCheckBoxesEls.forEach((radio) => {
        radio.disabled = !available;
      });
      // this.sliderEl.disabled = !available;
      // this.resetAllEl.disabled = !available;
    },
    // Update order of available nodes for the slider
    // setIdsForSliderStack() {
    //   const sortedAvailableNodeIds = this.allNodeIds
    //     // Available nodes are those on the visible chart
    //     .filter(nodeId => this.allNodeIdsLookup[nodeId].sliderAvailability
    //       && this.allNodeIdsLookup[nodeId].filterState)
    //     .sort((idA, idB) => this.allNodeIdsLookup[idB].index - this.allNodeIdsLookup[idA].index);
    //   // Append items already filtered by the slider to the end of the stack, in order they were removed
    //   this.sliderStack = sortedAvailableNodeIds.concat((this.nodeIdsRemovedBySlider));
    // },
    // setLargestComponentSize() {
    //   const components = this.visibleChart.component.graph().components();
    //   this.largestCompSizeEl.innerText = components.length
    //     ? components.reduce((a, b) => ((b.nodes.length < a.nodes.length) ? a : b)).nodes.length
    //     : 0;
    // },
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
        //this.setButtonAvailability(this.removeItemsButtonEl, true);
      } else {
        // No nodes selected
        this.visibleChart.component.selection([]);
        this.visibleChart.component.foreground(() => true);
        //this.setButtonAvailability(this.removeItemsButtonEl, false);
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
      this.setUIAvailability(false);
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
      // this.setIdsForSliderStack();
      // // Update the largest component indicator
      // this.setLargestComponentSize();
      // Enable the UI after the visible chart has been updated
      this.setUIAvailability(true);
    },
    initialiseInteractions() {
      // const sliderValueEl = document.getElementById('sliderValue');
      // // Filter the chart when any checkbox is changed
      // this.familyCheckBoxesEls.forEach((checkbox) => {
      //   checkbox.addEventListener('click', (event) => {
      //     let familyIdsToBeFiltered;
      //     const familyName = event.target.id;
      //     const familyChecked = event.target.checked;
      //     this.setNodesManuallySelected([]);
      //     // Check if family has been filtered before
      //     if (this.familyIdsCache[familyName]) {
      //       familyIdsToBeFiltered = this.familyIdsCache[familyName];
      //     } else {
      //       // Get the family ids and cache the ids for later use
      //       familyIdsToBeFiltered = this.allNodeIds
      //         .filter(id => this.allNodeIdsLookup[id].family === familyName);
      //       this.familyIdsCache[familyName] = familyIdsToBeFiltered;
      //     }
      //     this.setNodeState(familyIdsToBeFiltered, 'familyCheckbox', familyChecked);
      //     this.doFiltering(familyName);
      //   });
      // });
      // // this.visibleChart.component.on('selection-change', () => {
      // //   const selectedItems = this.visibleChart.component.selection();
      // //   // Filter selection to include only nodes
      // //   const newSelectedNodes = selectedItems.filter(id => !id.match(/-/));
      // //   this.setNodesManuallySelected(newSelectedNodes);
      // // });
      // // Remove manually selected nodes
      // this.removeItemsButtonEl.addEventListener('click', async () => {
      //   this.setButtonAvailability(this.removeItemsButtonEl, false);
      //   await this.doFiltering('selected');
      //   this.setButtonAvailability(this.restoreItemsButtonEl, true);
      // });
      // // Restore previously removed nodes
      // this.restoreItemsButtonEl.addEventListener('click', () => {
      //   this.setNodesManuallySelected([]);
      //   // Update state of nodes to be restoreed
      //   this.setNodeState(this.manuallyRemovedStack.pop(), 'filterState', true);
      //   // Disable the restore button if stack is empty
      //   if (this.manuallyRemovedStack.length === 0) {
      //     this.setButtonAvailability(this.restoreItemsButtonEl, false);
      //   }
      //   this.doFiltering();
      // });
      // // Update the slider value before the change event if it is dragged
      // this.sliderEl.addEventListener('input', () => {
      //   sliderValueEl!.innerText = (+this.sliderEl.value).toString();
      // });
      // // Filter the chart once the slider value has been changed
      // this.sliderEl.addEventListener('change', () => {
      //   this.setNodesManuallySelected([]);
      //   const sliderValue = +this.sliderEl.value;
      //   const availableNodes = this.sliderStack.length;
      //   const nodesToRemove = Math.min(sliderValue, availableNodes);
      //   this.nodeIdsRemovedBySlider = this.sliderStack.slice(availableNodes
      //     - nodesToRemove, availableNodes);
      //   // Update filter state of nodes on the stack
      //   this.sliderStack.forEach((id) => {
      //     this.allNodeIdsLookup[id].filterState = !this.nodeIdsRemovedBySlider.includes(id);
      //   });
      //   this.doFiltering('slider');
      // });
      // this.resetAllEl.addEventListener('click', async () => {
      //   // Clear all filters and reset the UI
      //   this.setNodesManuallySelected([]);
      //   this.manuallyRemovedStack = [];
      //   this.nodeIdsRemovedBySlider = [];
      //   this.setButtonAvailability(this.restoreItemsButtonEl, false);
      //   this.sliderEl.value = 0;
      //   sliderValueEl!.innerText = "0";
      //   this.familyCheckBoxesEls.forEach((checkbox) => {
      //     checkbox.checked = true;
      //   });
      //   // Update state of all nodes and filter the chart
      //   this.setNodeState(this.allNodeIds, 'filterState', true);
      //   this.setNodeState(this.allNodeIds, 'familyCheckbox', true);
      //   await this.doFiltering();
      //   this.visibleChart.component.layout('organic', { mode: 'adaptive' });
      // });
      // this.setButtonAvailability(this.restoreItemsButtonEl, false);
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
    async setNodesSize() {
      // console.log('setNodeSize', this.visibleChart, this.visibleChart.component)
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

    onDragMove() {
      this.updateTooltipPosition();
    },
    onHover(e) {
      //console.log("hover", e)
      this.handleTooltip(e);
    },
    onViewChange() {
      let { width, height } = this.visibleChart.component.viewOptions();
      const { width: newWidth, height: newHeight } = this.visibleChart.component.viewOptions();
      if (width !== newWidth || height !== newHeight) {
        this.closeTooltip();
        width = newWidth;
        height = newHeight;
      }
      this.updateTooltipPosition();
    },
    onSelectionChange() {
      const selectedItems = this.visibleChart.component.selection();
      // Filter selection to include only nodes
      const newSelectedNodes = selectedItems.filter(id => !id.match(/-/));
      this.setNodesManuallySelected(newSelectedNodes);


      this.selectedItem.data = this.resultsData?.filter(x => x.id == newSelectedNodes[0])[0];
      console.log("onSelectionChange", this.resultsData, this.selectedItem);


      this.expandOptions = [];
      let item = this.selectedItem.data as any;
      if (item.linkedin_username?.length > 0) {
        this.expandOptions.push(this.expandOptionsAll.find(x => x.value == "linkedin_user"));
        //this.expandUsingSD(newSelectedNodes);
      }
      if (item.twitter_username?.length > 0) {
        this.expandOptions.push(this.expandOptionsAll.find(x => x.value == "twitter_user"));
        //this.expandUsingSD(newSelectedNodes);
      }
      if (item.facebook_username?.length > 0) {
        this.expandOptions.push(this.expandOptionsAll.find(x => x.value == "facebook_user"));
        //this.expandUsingSD(newSelectedNodes);
      }
    },
    doZoom(name) {
      this.visibleChart.component.zoom(name, { animate: true, time: 350 });
    },

    registerClickHandler(id, fn) {
      document.getElementById(id)!.addEventListener('click', fn);
    },

    async onKlReady(charts) {

      const nodesSizedByDegree = await this.setNodesSize();
      // Set the order of nodes ids to be filtered for the slider
      this.setNodesIdsLookup(nodesSizedByDegree);
      // Set nodes to be filtered by the slider
      // this.setIdsForSliderStack();
      this.visibleChart.component.layout('organic', { consistent: true, packing: 'adaptive' });
      //this.setLargestComponentSize();
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

    updateTooltipPosition() {
      var nodeBaseSize = 26;
      if (this.tooltip.itemId) {
        var itemId = this.tooltip.itemId;
        var element = this.tooltipContainer;
        // console.log('upel', element)
        const item = this.visibleChart.component.getItem(itemId);
        const coordinates = this.visibleChart.component.viewCoordinates(item.x, item.y);
        const x = coordinates.x;
        const y = coordinates.y;
        const zoom = this.visibleChart.component.viewOptions().zoom;
        const arrowTipOffset = 20;
        // get the size of the node on screen
        const nodeSize = nodeBaseSize * (item.e || 1) * zoom;
        (element as any).style.opacity = 0;
        // allow fade in and out to animate
        (element as any).style.transition = 'opacity 0.3s ease';
        // scale the size of the tooltip depending on zoom level
        (element as any).style.transform = `scale(${Math.max(0.75, Math.min(2, zoom))}`;
        const top = y - ((element as any).clientHeight / 2);
        (element as any).style.left = `${x + arrowTipOffset + nodeSize}px`;
        (element as any).style.top = `${top}px`;
        (element as any).style.opacity = 1;
      }
    },
    closeTooltip() {
      if (this.tooltip.element) {
        (this.tooltip.element as any).style.opacity = 0;
        this.tooltip.itemId = null;
        this.tooltip.element = null;
      }
    },
    handleTooltip(e) {
      console.log("handle", e.id);
      const item = this.visibleChart.component.getItem(e.id);
      // this.tooltip.element = (document.getElementById('tooltip') as any);
      // console.log(item,this.tt_html.innerHTML);
      if (item && item.type === 'node') {
        // const html = (this.templateHtml as any).replace(/{{label}}/, item.t)
        //   .replace(/{{gender}}/, item.d.g)
        //   .replace(/{{name}}/, item.d.fn)
        //   .replace(/{{surname}}/, item.d.ln);

        // console.log("asdasd,", this.templateHtml);
        // const html = (this.templateHtml as any).replace(/{{label}}/, item.t)
        //   .replace(/{{content}}/, this.chartData.items.find(x => (x as any).id.toString() == item.id.toString()));
        console.log('tooltip', this.$props.resultsData);
        var resultsData: any = this.$props.resultsData;
        var dataItem = resultsData.find(x => (x as any).id.toString() == item.id.toString());

        console.log(dataItem);
        this.tooltipState.label = item.t;
        this.tooltipState.content = this.jsonToTable(dataItem);
        // Add it to the DOM
        console.log(this.tooltipState.content)

        // console.log("tc", this.tooltipContainer);
        // (this.tooltipContainer as any).innerHTML = html;
        this.tooltip.itemId = e.id;
        this.tooltip.element = this.tooltipContainer;
        this.updateTooltipPosition();
      } else if (this.tooltip.element) {
        this.closeTooltip();
      }
    },

    jsonToTable(data) {
      var keys: any[] = [];
      // console.log("json", data, Object.keys(data));
      for (var k in Object.keys(data).slice(0, 10)) {
        keys.push(Object.keys(data)[k]);
      }

      // Create a table element
      var table = document.createElement("table");

      // Create table row tr element of a table
      // console.log("keys", keys);
      for (var i = 0; i < keys.length; i++) {
        if (data[keys[i]]?.length > 0) {
          var tr = table.insertRow(-1);


          // Create the table header th element
          var cell = tr.insertCell(-1);
          cell.innerHTML = keys[i];

          cell = tr.insertCell(-1);
          cell.innerHTML = data[keys[i]];
        }

      }

      // // Adding the data to the table
      // for (var i = 0; i < data.length; i++) {

      //   // Create a new row
      //   var trow = table.insertRow(-1);
      //   for (var j = 0; j < cols.length; j++) {
      //     var cell = trow.insertCell(-1);

      //     // Inserting the cell at particular place
      //     cell.innerHTML = data[i][cols[j]];
      //   }
      // }

      // Add the newly created table containing json data
      // var el = document.getElementById("table");
      // el.innerHTML = "";
      // el.appendChild(table);

      return table.outerHTML;
    }

  },
});
</script>

<style scoped>
.chart-container {
  height: 100%;
}

.chart-container-big {
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

/* Tooltip styling */
.popover {
  z-index: 1000;
  background: white;
}
:fullscreen .popover {
  margin-top: -70px;
}
#tooltip .popover-title {
  font-size: 16px;
  padding: 8px 14px;
  margin: 0px;
  line-height: 20px;
  top: 0px;
}
#tooltip .popover-content {
  font-size: 12px;
  border: 1px solid gray;
}
#tooltip .popover-content .td {
  border: 1px solid gray;
  max-height: 20px;
}
#tooltip .arrow {
  background-color: white;
  border-bottom: 1px solid gray;
  border-left: 1px solid gray;
  transform: translate(-5px, 60px) rotateZ(45deg);
  width: 10px;
  height: 10px;
  position: absolute;
}
.popover-content {
  padding: 9px 14px;
}
.klchart {
  overflow: hidden;
}
#tooltip {
  background: white;
  border: black;
  transition: opacity 0.3s ease;
}
</style>
