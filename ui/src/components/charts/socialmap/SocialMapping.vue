<template>
  <div class="row gy-5 gx-xl-8" style="height:100%;">
    <div class="col-xxl-9">
      <div
        class="card"
        style="background:url(/media/patterns/graph-bg.jpg) repeat;     background-size: 48px;"
      >
        <!-- <div class="card-header border-0">
          <h3 class="card-title fw-bolder text-dark">Social Network</h3>
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
        </div>-->
        <div class="card-body pt-2">
          <div class="chart-wrapper h-100">
            <KlChart
              :containerClass="'chart-container-big'"
              :id="'kl-chart-social'"
              ref="chart"
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
          </div>
        </div>
      </div>
    </div>
    <div class="col-xxl-3 h-100">
      <div class="card">
        <div class="card-header border-0">
          <h3 class="card-title fw-bolder text-dark">Filters</h3>

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
          <div class="chart-wrapper" style="height: 300px">
            <KlChart
              :containerClass="'chart-container'"
              :id="'kl-mini-chart'"
              ref="miniChart"
              :data="chartData"
              :options="miniChartOptions"
              @kl-ready="onKlReady"
            ></KlChart>
          </div>
          <br />
          <div class="form-inline">
            <div class="btn-row">
              <div class="pull-left" style="width: fit-content; ">
                <p>Email Volumes:</p>
              </div>
              <div class="btn-group pull-right">
                <button
                  class="volume btn btn-sm btn-primary pull-left active"
                  type="button"
                  value="off"
                  id="volumeOff"
                >Off</button>
                <button
                  class="volume btn btn-sm btn-primary pull-left"
                  type="button"
                  value="on"
                  id="volumeOn"
                >On</button>
              </div>
            </div>
            <br />
            <div class="btn-row" style="margin-top:10px;">
              <div class="pull-left">
                <p>Size:</p>
              </div>
              <div class="btn-group size-btn pull-right">
                <button
                  class="size btn btn-sm btn-primary pull-left active"
                  type="button"
                  value="same"
                  id="same"
                >Same</button>
                <button
                  class="size btn btn-sm btn-primary pull-left"
                  type="button"
                  value="degrees"
                  id="degree"
                >Degree</button>
                <button
                  class="size btn btn-sm btn-primary pull-left"
                  type="button"
                  value="closeness"
                  id="closeness"
                >Closeness</button>
              </div>
              <br />
              <br />
              <div class="btn-group size-btn pull-right">
                <button
                  class="size btn btn-sm btn-primary"
                  type="button"
                  value="betweenness"
                  id="betweenness"
                >Between</button>
                <button
                  class="size btn btn-sm btn-primary pull-left"
                  type="button"
                  value="pageRank"
                  id="pagerank"
                >PageRank</button>
                <button
                  class="size btn btn-sm btn-primary pull-left"
                  type="button"
                  value="eigenCentrality"
                  id="eigenvector"
                >Eigen</button>
              </div>
            </div>
            <br />
            <div class="btn-row" id="analysis-control">
              <div class="pull-left">
                <p>Analyse:</p>
              </div>
              <div class="btn-group pull-right">
                <button
                  class="direction btn btn-sm btn-primary pull-left"
                  type="button"
                  value="from"
                  id="sending"
                >Sent</button>
                <button
                  class="direction btn btn-sm btn-primary pull-left"
                  type="button"
                  value="to"
                  id="receiving"
                >Received</button>
                <button
                  class="direction btn btn-sm btn-primary pull-left active"
                  type="button"
                  value="any"
                  id="any"
                >All</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import "leaflet/dist/leaflet.css";

import KlChart from "keylines/vue/Chart.vue";
import { data, colours } from './enron-data.js';
import L from "leaflet";
import Dropdown2 from "@/components/dropdown/Dropdown2.vue";

export default defineComponent({
  name: "chart-social-mapping",
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
    const chart = ref();
    const miniChart = ref();



    let restoreIds: any[] = [];

    // Track UI state
    const state = {
      sizeBy: 'same',
      volume: 'off',
      direction: 'any',
    };

    const colourMap = {};

    const chartData = data;

    // const chartOptions = {
    //   backColour: "transparent",
    //   fontFamily: "Spartan, sans-serif",
    //   fontSize: 10,
    //   fontColor: "#FFFFFF",
    //   animate: true,
    //   time: 800,
    //   transition: "layout",
    // };


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
      selectedNode: {
        c: colours.selected,
        b: colours.selected,
        fbc: colours.selected,
      },
      selectedLink: {
        c: colours.selected,
      },
    };

    // const mainChartConfig = {
    //   container: 'klchart',
    //   options: Object.assign({}, baseOpts, {
    //     drag: {
    //       links: false,
    //     },
    //     logo: { u: 'images/Logo.png' },
    //   }),
    // };

    const miniChartOptions = Object.assign({}, chartOptions, {
      navigation: { shown: false },
      drag: {
        links: false,
      },
      // logo: { u: 'images/Logo.png' },
    });


    return {
      chart,
      miniChart,
      chartOptions,
      miniChartOptions,
      restoreIds,
      state,
      colourMap,
      chartData,
      colours,

    };
  },
  mounted() {
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


    // Right hand menu
    this.registerButtonGroup('volume', async (volume) => {
      this.state.volume = volume;

      const links = this.calculateLinkWidths(volume === 'on');
      await this.chart.component.animateProperties(links);
      await this.analyseChart();

      const miniItems = this.miniChartFilter(links);
      this.miniChart.component.animateProperties(miniItems, { time: 500 }); // fire and forget
    });

    this.registerButtonGroup('size', (sizeBy) => {
      this.state.sizeBy = ((sizeBy as any).id);
      this.analyseChart();
    });

    this.registerButtonGroup('direction', (direction) => {
      this.state.direction = direction;
      this.analyseChart();
    });

  },
  updated() {

    console.log('updated');
  },
  methods: {

    loadMiniChart(items) {
      // this.debounce((items) => {
      console.log('bounced', items);
      this.miniChart.component.load({
        type: 'LinkChart',
        items,
      });
      this.miniChart.component.layout('organic', { consistent: true });
      // });
    },

    debounce(fn, timeToWait = 100) {
      let timeoutId;
      return (...args) => {
        const timeoutFn = () => {
          timeoutId = undefined;
          console.log('apply');
          fn.apply(this, args);
        };
        if (timeoutId !== undefined) {
          console.log('clear');
          clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(timeoutFn, timeToWait);
      };
    },

    // debounce(fn: Function, ms = 300) {
    //   let timeoutId: ReturnType<typeof setTimeout>;
    //   return function (this: any, ...args: any[]) {
    //     clearTimeout(timeoutId);
    //     timeoutId = setTimeout(() => fn.apply(this, args), ms);
    //   };
    // },
    // // debounce(fn, timeToWait = 100) {
    //   let timeoutId;
    //   return debouncedFn(...args)=> {
    //     const timeoutFn = () => {
    //       timeoutId = undefined;
    //       fn.apply(this, args);
    //     };
    //     if (timeoutId !== undefined) {
    //       clearTimeout(timeoutId);
    //     }
    //     timeoutId = setTimeout(timeoutFn, timeToWait);
    //   };
    // },

    isLink(id) {
      return id.match('-');
    },

    updateHighlight(itemIds) {
      const props: any[] = [];

      // Remove previous styles
      if (this.restoreIds) {
        props.push(
          ...this.restoreIds.map((id) => {
            const colour = this.colourMap[id] || (this.isLink(id) ? this.colours.link : this.colours.node);
            return {
              id,
              c: colour,
              b: colour,
              ha0: null,
            };
          }),
        );
        this.restoreIds = [];
      }

      // // Add new styles
      if (itemIds.length) {
        // Find the neighbours of the provided items
        const toHighlight: any[] = [];
        itemIds.forEach((id) => {
          if (this.isLink(id)) {
            const link = this.chart.component.getItem(id);
            toHighlight.push(id, link.id1, link.id2);
          } else {
            const neighbours = this.chart.component.graph().neighbours(id);
            toHighlight.push(id, ...neighbours.nodes, ...neighbours.links);
          }
        });

        // For each neighbouring item, add some styling
        toHighlight.forEach((id) => {
          // Cache the existing styles
          this.restoreIds.push(id);

          // Generate new styles
          const style = {
            id,
          };
          if (this.isLink(id)) {
            // For links, just set the colour
            (style as any).c = colours.selected;
          } else {
            // For nodes, add a halo
            (style as any).ha0 = {
              c: colours.selected,
              r: 34,
              w: 6,
            };
          }
          props.push(style);
        });
      }

      this.chart.component.setProperties(props);
    },

    async runLayout(inconsistent, mode) {
      const packing = mode === 'adaptive' ? 'adaptive' : 'circle';
      return this.chart.component.layout('organic', {
        time: 500, tightness: 4, consistent: !inconsistent, packing, mode,
      });
    },
    fit() {
      this.chart.component.zoom('fit', { animate: true }).then(this.runLayout);
    },


    // klReady(charts) {
    //   [this.chart, this.miniChart] = charts;

    //   this.chart.load(data);
    //   console.log('loading');
    //   this.chart.zoom('fit', { animate: true }).then(this.runLayout);

    //   // On selection change:
    //   //   1) add styles to the targeted and neighbouring items
    //   //   2) copy the selected item and its neighbours to the miniChart
    //   // this.chart.on('selection-change', () => {

    //   // });
    // },

    // this picks a colour from a range of colours based on the value
    colourPicker(value) {
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
    },

    normalize(max, min, value) {
      if (max === min) {
        return min;
      }

      return (value - min) / (max - min);
    },

    miniChartFilter(items) {
      return items.filter(({ id }) => this.miniChart.component.getItem(id));
    },

    async animateValues(values) {
      const valuesArray = <number[]>Object.values(values);

      const max = Math.max(...valuesArray);
      const min = Math.min(...valuesArray);

      const items = Object.entries(values).map(([id, value]) => {
        // Normalize the value in the range 0 -> 1
        const normalized = this.normalize(max, min, value);

        // enlarge nodes with higher values
        const e = Math.max(1, normalized * 5);

        // Choose a colour (use bands if there is a range of values)
        const c = max !== min ? this.colourPicker(normalized) : colours.node;
        this.colourMap[id] = c;

        return { id, e, c, b: c };
      });

      await this.chart.component.animateProperties(items, { time: 500 });
      await this.runLayout(undefined, 'adaptive');

      const miniItems = this.miniChartFilter(items);
      await this.miniChart.component.animateProperties(miniItems, { time: 500 });
      return this.miniChart.component.layout('organic', { consistent: true });
    },

    same() {
      return new Promise((resolve) => {
        const sizes = {};
        this.chart.component.each({ type: 'node' }, (node) => {
          sizes[node.id] = 0;
        });
        resolve(sizes);
      });
    },

    wrapCallback(fn) {
      return options => new Promise(resolve => resolve(fn(options)));
    },

    getAnalysisFunction(name) {
      if (name.match(/^(degrees|pageRank|eigenCentrality)$/)) {
        return this.wrapCallback(this.chart.component.graph()[name]);
      }
      if (name.match(/^(closeness|betweenness)$/)) {
        return this.chart.component.graph()[name];
      }
      return this.same;
    },

    async analyseChart() {
      let { sizeBy, volume } = this.state;

      // console.log('analyse', sizeBy, volume);

      const options: any = {};
      // Configure weighting
      if (volume === 'on') {
        if (sizeBy.match(/^(betweenness|closeness)$/)) {
          options.weights = true;
        }
        options.value = 'count';
      }
      // Configure direction options
      if (sizeBy.match(/^(betweenness|pageRank)$/)) {
        options.directed = this.state.direction !== 'any';
      } else {
        options.direction = this.state.direction;
      }

      const analyse = this.getAnalysisFunction(sizeBy);
      const values = await analyse(options);
      return this.animateValues(values);
    },

    calculateLinkWidths(showValue) {
      const links: any[] = [];
      this.chart.component.each({ type: 'link' }, (link) => {
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
    },

    doZoom(name) {
      this.chart.zoom(name, { animate: true, time: 350 });
    },


    onSelectionChange() {
      const ids = this.chart.component.selection();

      this.updateHighlight(ids);

      const miniChartItems: any[] = [];

      if (ids.length > 0) {
        const { nodes, links } = this.chart.component.graph().neighbours(ids);

        this.chart.component.each({ type: 'node' }, (node) => {
          if (ids.includes(node.id) || nodes.includes(node.id)) {
            // Clear hover styling and position
            node.x = 0;
            node.y = 0;
            delete node.ha0;
            miniChartItems.push(node);
          }
        });

        this.chart.component.each({ type: 'link' }, (link) => {
          if (ids.includes(link.id) || links.includes(link.id)) {
            link.c = colours.link;
            miniChartItems.push(link);
          }
        });
      }

      // console.log()
      this.loadMiniChart(miniChartItems);
    },


    registerClickHandler(id, fn) {
      console.log(id, fn);
      // document.getElementById(id)!.addEventListener('click', ()=>fn());
    },

    updateActiveState(nodes, activeValue) {
      nodes.forEach((node) => {
        if (node.value === activeValue) {
          node.classList.add('active');
        } else {
          node.classList.remove('active');
        }
      });
    },

    registerButtonGroup(className, handler) {
      const nodes = document.querySelectorAll(`.${className}`);
      nodes.forEach((node) => {
        node.addEventListener('click', () => {
          const value = node;
          // console.log(node);
          this.updateActiveState(nodes, value);

          handler(value);
        });
      });
    },



    onKlReady(charts) {

      //[this.chart, this.miniChart] = charts;

      // this.chart.component.load(data);
      console.log('loading', data, this.chart);
      this.chart.component.zoom('fit', { animate: true }).then(() => {
        this.runLayout(true, 'full');
      });





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
        const hand = !!this.chart.component.options().handMode; // be careful with undefined
        this.chart.component.options({ handMode: !hand });

        const icon = document.getElementById('iconMode');
        icon!.classList.toggle('fa-arrows-alt');
        icon!.classList.toggle('fa-edit');
      });
      this.registerClickHandler('layout', () => {
        this.runLayout(true, 'full');
      });

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
      // };

      // const miniChartConfig = {
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
</style>
