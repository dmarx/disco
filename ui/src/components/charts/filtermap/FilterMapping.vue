<template>
  <div class="row gy-5 gx-xl-8" style="height: 100%">
    <div class="col-xxl-9">
      <div
        class="card"
        style="height: 100% ;background:url(/media/patterns/graph-bg.jpg) repeat;     background-size: 48px;"
      >
        <!-- <div class="card-header border-0">
          <h3 class="card-title fw-bolder text-dark">Workspace Associations</h3>

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
        <div class="card-body pt-2" style="height: 100%">
          <div class="chart-wrapper h-100" style="min-height:85%">
            <KlChart
              :containerClass="'chart-container-big'"
              :id="'kl-chart'"
              ref="chart"
              :data="chartData"
              :options="chartOptions"
              @kl-ready="onKlReady"
              @kl-selection-change="onSelectionChange"
              @kl-map="mapModeChange"
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
    <div class="col-xxl-3">
      <div class="card" style="height: 100%">
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
        <div class="card-body pt-2" style="height: 100%">
          <div class="h-100">
            <ul class="nav nav-pills nav-pills-custom mb-3" style="flex-wrap:nowrap">
              <li class="nav-item mb-6 me-6 me-lg-6" style="width:50% !important">
                <a
                  style="width:100% !important"
                  ref="mapOff"
                  class="nav-link btn btn-outline btn-flex btn-active-color-primary flex-column overflow-hidden w-80px h-85px pt-5 pb-2"
                  data-bs-toggle="pill"
                  href="#kt_stats_widget_6_tab_1"
                >
                  <div class="nav-icon mb-3">
                    <i class="bi bi-list-task" style="font-size:22px;"></i>
                  </div>
                  <span class="nav-text text-gray-800 fw-bolder fs-6 lh-1">Network</span>
                  <span class="bullet-custom position-absolute bottom-0 w-100 h-4px bg-primary"></span>
                </a>
              </li>
              <li class="nav-item mb-6 me-6 me-lg-6" style="width:50% !important">
                <a
                  style="width:100% !important"
                  ref="mapOn"
                  class="nav-link btn btn-outline btn-flex btn-active-color-primary flex-column overflow-hidden w-80px h-85px pt-5 pb-2"
                  data-bs-toggle="pill"
                  href="#kt_stats_widget_6_tab_2"
                >
                  <div class="nav-icon mb-3">
                    <i class="bi bi-list-check" style="font-size:22px;"></i>
                  </div>
                  <span class="nav-text text-gray-800 fw-bolder fs-6 lh-1">Map</span>
                  <span class="bullet-custom position-absolute bottom-0 w-100 h-4px bg-primary"></span>
                </a>
              </li>
            </ul>
            <!-- 
            <div class="cicontent">
              <div>
                <div class="btn-group">
                  <input
                    class="mapMode span2 btn"
                    type="button"
                    value="Map Mode"
                    id="mapOn"
                    ref="mapOn"
                  />
                  <input
                    class="mapMode btn span2 btn-kl active"
                    type="button"
                    value="Network Mode"
                    id="mapOff"
                    ref="mapOff"
                  />
                </div>
            </div>-->
            <br />
            <div class="form-check form-check-custom form-check-solid">
              <input
                class="form-check-input"
                type="checkbox"
                value
                id="fgSelect"
                ref="fgSelectCheckbox"
                checked
              />
              <label class="form-check-label" for="flexCheckDefault">Show edges in foreground</label>
            </div>
            <br />

            <label>
              Minimum edge strength:
              <span id="sliderDisplayValue">0</span>
            </label>
            <fieldset>
              <label id="slider-container">
                <input
                  ref="flightVolumeSlider"
                  id="flightVolumeSlider"
                  type="range"
                  min="0"
                  max="18000"
                  value="0"
                  step="100"
                  style="display: block"
                />
              </label>
            </fieldset>
            <br />
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="AA" checked />
              <label class="form-check-label" for="AA">American</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="AS" checked />
              <label class="form-check-label" for="AS">Alaska</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="B6" checked />
              <label class="form-check-label" for="B6">JetBlue</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="DL" checked />
              <label class="form-check-label" for="DL">Delta</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="EV" checked />
              <label class="form-check-label" for="EV">ExpressJet</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="F9" checked />
              <label class="form-check-label" for="F9">Frontier</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="FL" checked />
              <label class="form-check-label" for="FL">AirTran</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="HA" checked />
              <label class="form-check-label" for="HA">Hawaiian</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="MQ" checked />
              <label class="form-check-label" for="MQ">Envoy</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="OO" checked />
              <label class="form-check-label" for="OO">SkyWest</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="UA" checked />
              <label class="form-check-label" for="UA">United</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="US" checked />
              <label class="form-check-label" for="US">US Airways</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="VX" checked />
              <label class="form-check-label" for="VX">Virgin</label>
            </div>
            <div class="form-check form-check-custom form-check-solid form-check-sm">
              <input class="form-check-input airlineCheckbox" type="checkbox" id="WN" checked />
              <label class="form-check-label" for="WN">Southwest</label>
            </div>
            <br />
            <div class="row" style="margin-top: 15px">
              <div class="span">
                <input
                  class="btn btn-spaced btn-sm btn-primary"
                  type="button"
                  value="All"
                  ref="selectAllButton"
                  style="width:32%;margin-right:4px;"
                />
                <input
                  class="btn btn-spaced btn-sm btn-primary"
                  type="button"
                  value="Clear"
                  ref="selectNoneButton"
                  style="width:32%;margin-right:4px;"
                />
                <input
                  class="btn btn-spaced btn-sm btn-primary"
                  type="button"
                  value="Invert"
                  ref="selectInvertButton"
                  style="width:32%"
                />
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
import json from "./filtermap-data.js";
import L from "leaflet";
import Dropdown2 from "@/components/dropdown/Dropdown2.vue";


export default defineComponent({
  name: "chart-filter-mapping",
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
    const fgSelectCheckbox = ref();
    const flightVolumeSlider = ref();
    //const checkboxNodeList = ref();
    const selectAllButton = ref();
    const selectNoneButton = ref();
    const selectInvertButton = ref();
    const mapOn = ref();
    const mapOff = ref();


    let filterInProgress = false;
    let refilter = false;
    let minFlightVolume = 0;

    const southwest = (L as any).latLng(-30, -210);
    const northeast = (L as any).latLng(80, -30);
    const chartOptions = {
      backColour: "transparent",
      fontFamily: "Spartan, sans-serif",
      fontSize: 10,
      fontColor: "#FFFFFF",
      animate: true,
      handMode: true,
      time: 800,
      transition: "layout",
      navigation: { shown: false },
      leaflet: {
        maxZoom: 10,
        minZoom: 3,
        // Limit map panning and zoom to be roughly around USA
        maxBounds: L.latLngBounds(southwest, northeast),
        maxBoundsViscosity: 1,
      },
    };
    // this.chart.map().options(mapOptions);

    const chartData = json;

    return {
      chart,
      chartOptions,
      chartData,
      filterInProgress,
      refilter,
      minFlightVolume,
      fgSelectCheckbox,
      flightVolumeSlider,
      // checkboxNodeList,
      selectAllButton,
      selectNoneButton,
      selectInvertButton,
      mapOn,
      mapOff,
      json,
    };
  },
  mounted() {
    // chart = ref(null);
    // console.log(this.chart);
    this.addEventListeners();
    // chart = ref.chart
    // this.fgSelectCheckbox.focus();
  },
  methods: {
    // returns an object with airline IDs as keys and bool values indicating if its checkbox is checked
    getCheckboxStatuses() {
      const checkedList = {};
      let checkboxes = document.getElementsByClassName("airlineCheckbox");
      const elementList = Array.from(checkboxes);
      elementList.forEach((el) => {
        checkedList[(el as any).id] = (el as any).checked;
      });
      return checkedList;
    },

    filterChart() {
      // Don't start a new filter if one is currently running but
      // ensure it refilters with the updated settings once the current filter has finished
      this.refilter = this.filterInProgress;
      if (this.refilter) {
        return;
      }
      this.filterInProgress = true;
      const checked = this.getCheckboxStatuses();

      this.chart.component
        .filter(
          (item) => item.d.n >= this.minFlightVolume && checked[item.d.carrier],
          { type: "link" }
        )
        .then(() => {
          this.filterInProgress = false;
          if (this.refilter) {
            this.filterChart();
          } else if (!this.chart.target.map().isShown()) {
            this.chart.layout();
          }
        });
    },

    onSelectionChange() {
      let chart = this.chart as any;
      const selectedItems = chart.component.selection();
      if (selectedItems.length > 0 && (this.fgSelectCheckbox as any).checked) {
        const neighbours = chart.component.graph().neighbours(selectedItems);
        const idsToForeground = selectedItems.concat(neighbours.links);
        // foreground only links which will automatically foreground nodes at end of those links
        chart.component.foreground((item) => idsToForeground.includes(item.id), {
          type: "link",
        });
      } else {
        // foreground everything
        chart.component.foreground(() => true);
      }
      // focus back on the slider to stop Edge requiring 2 taps
      this.flightVolumeSlider.focus();
    },

    updateAirlineCheckboxes(updateFn) {
      let checkboxes = document.getElementsByClassName("airlineCheckbox");
      const elementList = Array.from(checkboxes);
      elementList.forEach(updateFn);
    },

    addEventListeners() {
      // updates slider text when moved
      let checkboxes = document.getElementsByClassName("airlineCheckbox");
      // console.log(this.flightVolumeSlider);
      this.flightVolumeSlider.addEventListener("input", () => {
        const sliderValue = this.flightVolumeSlider.value;
        document.getElementById(
          "sliderDisplayValue"
        )!.innerHTML = ` ${sliderValue}`;
      });
      // does all filtering once slider has changed and been released
      this.flightVolumeSlider!.addEventListener("change", () => {
        this.minFlightVolume = this.flightVolumeSlider.value;
        this.filterChart();
        this.onSelectionChange();
      });
      this.flightVolumeSlider.addEventListener("mouseup", () => {
        if (this.minFlightVolume !== this.flightVolumeSlider.value) {
          this.minFlightVolume = this.flightVolumeSlider.value;
          this.filterChart();
          this.onSelectionChange();
        }
      });

      this.selectAllButton.addEventListener("click", () => {
        this.updateAirlineCheckboxes((checkbox) => {
          checkbox.checked = true;
        });
        this.filterChart();
      });

      this.selectNoneButton.addEventListener("click", () => {
        this.updateAirlineCheckboxes((checkbox) => {
          checkbox.checked = false;
        });
        this.filterChart();
      });

      this.selectInvertButton.addEventListener("click", () => {
        this.updateAirlineCheckboxes((checkbox) => {
          checkbox.checked = !checkbox.checked;
        });
        this.filterChart();
      });


      Array.from(checkboxes).forEach((checkbox) => {
        (checkbox as any).addEventListener("change", this.filterChart);
      });

      this.fgSelectCheckbox.addEventListener("change", this.onSelectionChange);

    },

    // Enable/Disable filters, used on transition start.
    disableUiControls(disabledVal) {
      this.updateAirlineCheckboxes((checkbox) => {
        checkbox.disabled = disabledVal;
      });
      this.flightVolumeSlider.disabled = disabledVal;
      this.selectAllButton.disabled = disabledVal;
      this.selectNoneButton.disabled = disabledVal;
      this.selectInvertButton.disabled = disabledVal;
      this.fgSelectCheckbox.disabled = disabledVal;
    },

    mapModeChange({ type }) {
      // Disable UI on map transition start and enable it on end
      if (type === "showstart" || type === "hidestart") {
        this.mapOn.classList.toggle("active");
        this.mapOff.classList.toggle("active");
        this.disableUiControls(true);
      } else if (type === "showend" || type === "hideend") {
        this.disableUiControls(false);
      }
    },

    doZoom(name) {
      this.chart.component.zoom(name, { animate: true, time: 350 });
    },

    registerClickHandler(id, fn) {
      document.getElementById(id)!.addEventListener('click', fn);
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

    onKlReady() {
      // data is defined in filtermap-data.js
      // console.log("chart");
      // console.log(this.chart);
      // console.log(this.chart.component);

      // this.chart.load(this.json);
      // this.chart.layout();
      const southwest = (L as any).latLng(-30, -210);
      const northeast = (L as any).latLng(80, -30);
      const mapOptions = {
        animate: true,
        time: 800,
        transition: "layout",
        leaflet: {
          maxZoom: 10,
          minZoom: 3,
          // Limit map panning and zoom to be roughly around USA
          maxBounds: L.latLngBounds(southwest, northeast),
          maxBoundsViscosity: 1,
        },
      };
      // this.chart.component.map().options(mapOptions);
      this.mapOn.addEventListener("click", this.chart.component.map().show);
      this.mapOff.addEventListener("click", this.chart.component.map().hide)



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



      // this.chart.target.on("selection-change", this.onSelectionChange);
      // this.chart.target.on("map", this.mapModeChange);
      // loadKeyLines() {
      //   KeyLines.promisify();
      //   const options = {
      //     logo: 'images/Logo.png',
      //     hover: 100,
      //     handMode: true,
      //   };
      //   this.chart = await KeyLines.create({
      //     container: 'klchart',
      //     options,
      //   });
      //   this.klReady();
      // }
      // window.addEventListener('DOMContentLoaded', this.loadKeyLines);
    },
  },
});
</script>

<style scoped>
.chart-container {
  height: 100%;
}
span.circle {
  padding: 3px;
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  border-radius: 5px;
  color: white;
  width: 29px;
  text-align: center;
  display: inline-block;
}
label.checkbox {
}
.circleAA {
  background: #4481ba;
}
.circleAS {
  background: #1f405f;
}
.circleB6 {
  background: #9e4817;
}
.circleDL {
  background: #ff9651;
}
.circleEV {
  background: #98bb60;
}
.circleF9 {
  background: #4d622c;
}
.circleFL {
  background: #31acc4;
}
.circleHA {
  background: #115967;
}
.circleMQ {
  background: #413151;
}
.circleOO {
  background: #8263a0;
}
.circleUA {
  background: #808080;
}
.circleUS {
  background: #404040;
}
.circleVX {
  background: #672525;
}
.circleWN {
  background: #c85150;
}

#slider-container {
  width: 100%;
  margin: 0px;
}

#flightVolumeSlider {
  width: calc(100% - 20px);
  margin: 10px;
}
.checkbox span {
  margin-left: 5px;
}
</style>
