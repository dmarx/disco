<template>
  <div v-if="state.mounted">
    <Teleport to="#aside-context">
      <AsideDefaultMenu></AsideDefaultMenu>
    </Teleport>
  </div>
  <!-- <div style="position: relative">
    <div id="map"  style="height: 500px"></div>
    <div
      style="position: absolute; top: 0; left: 0; display: flex; flex-direction: column; z-index: 20;"
    >
      <button @click="findRoute()">Find Route</button>
      <button @click="clearRoute()">Clear Route</button>
    </div>
  </div>-->

  <div class="row gy-5 gx-xl-8">
    <div class="col-xxl-4">
      <Subjects widget-classes="card-xxl-stretch mb-5 mb-xxl-8"></Subjects>
    </div>
    <div class="col-xxl-8">
      <div
        class="card"
        style="height: calc(100% - 17px);background:url(/media/patterns/graph-bg.jpg) repeat;     background-size: 48px;"
      >
        <div class="card-header border-0" style="z-index: 4;">
          <h3 class="card-title fw-bolder text-dark">Associations</h3>

          <div class="card-toolbar">
            <ul class="nav nav-tabs nav-line-tabs nav-stretch fs-6 border-0">
              <li class="nav-item">
                <a class="nav-link active" data-bs-toggle="tab" href="#kt_tab_pane_7">Network</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-bs-toggle="tab" href="#kt_tab_pane_8">Map</a>
              </li>
            </ul>
          </div>
        </div>
        <div class="card-body pt-2" style="padding: 0;    margin-top: -75px;">
          <div class="tab-content" id="myTabContent" style="height: 100%">
            <div
              class="tab-pane fade show active"
              id="kt_tab_pane_7"
              role="tabpanel"
              style="height: 100%"
            >
              <div
                :id="'chart-container'"
                class="d-flex flex-grow-1 flex-column chart-container"
                style="height: 100%"
              >
                <AssocationsSimple></AssocationsSimple>
                <!-- <KlChart
                  class="flex-grow-1"
                  :containerClass="'chart-container'"
                  :data="chartData"
                  :options="chartOptions"
                  :id="'kl-chart'"
                  :animateOnLoad="true"
                ></KlChart>-->
              </div>
            </div>
            <div class="tab-pane fade" id="kt_tab_pane_8" role="tabpanel" style="height: 100%">
              <div style="position: relative">
                <div id="map" style="width:100%;height: 480px"></div>
              </div>

              <!-- <div style="height: 480px; width: 100%">
                <l-map
                  v-model="zoom"
                  v-model:zoom="zoom"
                  :center="[47.41322, -1.219482]"
                  @move="log('move')"
                >
                  <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"></l-tile-layer>
                  <l-control-layers />
                  <l-marker :lat-lng="[0, 0]" draggable @moveend="log('moveend')">
                    <l-tooltip>lol</l-tooltip>
                  </l-marker>

                  <l-marker :lat-lng="[47.41322, -1.219482]">
                    <l-icon :icon-url="iconUrl()" :icon-size="iconSize()" />
                  </l-marker>

                  <l-marker :lat-lng="[50, 50]" draggable @moveend="log('moveend')">
                    <l-popup>lol</l-popup>
                  </l-marker>

                  <l-polyline
                    :lat-lngs="[
                      [47.334852, -1.509485],
                      [47.342596, -1.328731],
                      [47.241487, -1.190568],
                      [47.234787, -1.358337],
                    ]"
                    color="green"
                  ></l-polyline>
                  <l-polygon
                    :lat-lngs="[
                      [46.334852, -1.509485],
                      [46.342596, -1.328731],
                      [46.241487, -1.190568],
                      [46.234787, -1.358337],
                    ]"
                    color="#41b782"
                    :fill="true"
                    :fillOpacity="0.5"
                    fillColor="#41b782"
                  />
                  <l-rectangle
                    :lat-lngs="[
                      [46.334852, -1.509485],
                      [46.342596, -1.328731],
                      [46.241487, -1.190568],
                      [46.234787, -1.358337],
                    ]"
                    :fill="true"
                    color="#35495d"
                  />
                  <l-rectangle
                    :bounds="[
                      [46.334852, -1.190568],
                      [46.241487, -1.090357],
                    ]"
                  >
                    <l-popup>lol</l-popup>
                  </l-rectangle>
                </l-map>
              </div>-->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="row gy-5 gx-xl-8">
    <div class="col-xxl-12">
      <CardEvents></CardEvents>
    </div>
  </div>
  <br />
  <div class="row gy-5 gx-xl-8">
    <div class="col-xxl-6">
      <div class="card">
        <div class="card-header border-0">
          <h3 class="card-title fw-bolder text-dark">Top 10 Entities Matrix</h3>
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
          <table id="kt_datatable_example_1" class="table table-row-bordered gy-5 table-small">
            <thead>
              <tr class="fw-bold fs-6 text-muted">
                <th>Ref</th>
                <th>Call ID</th>
                <th>Start time</th>
                <th>Duration</th>
                <th>Type</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
            </tbody>
            <tfoot></tfoot>
          </table>
        </div>
      </div>
    </div>
    <div class="col-xxl-6">
      <div class="card">
        <div class="card-header border-0">
          <h3 class="card-title fw-bolder text-dark">Hourly Events Per Day Matrix</h3>
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
          <table id="kt_datatable_example_1" class="table table-row-bordered gy-5 table-small">
            <thead>
              <tr class="fw-bold fs-6 text-muted">
                <th>Ref</th>
                <th>Call ID</th>
                <th>Start time</th>
                <th>Duration</th>
                <th>Type</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
              </tr>
            </tbody>
            <tfoot></tfoot>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

declare var Wrld: any;
declare var WrldNavigation: any;
declare var WrldRouteView: any;

import { defineComponent, onMounted, ref } from "vue";

import {
  LMap,
  LIcon,
  LTileLayer,
  LMarker,
  LControlLayers,
  LTooltip,
  LPopup,
  LPolyline,
  LPolygon,
  LRectangle,
} from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
// import TableWidget9 from "@/components/widgets/tables/Widget9.vue";
// import TableWidget5 from "@/components/widgets/tables/Widget5.vue";
// import ListWidget1 from "@/components/widgets/lists/Widget1.vue";
// import ListWidget2 from "@/components/widgets/lists/Widget2.vue";
// import ListWidget3 from "@/components/widgets/lists/Widget3.vue";
// import ListWidget5 from "@/components/widgets/lists/Widget5.vue";
// import ListWidget6 from "@/components/widgets/lists/Widget6.vue";
// import MixedWidget2 from "@/components/widgets/mixed/Widget2.vue";
// import MixedWidget5 from "@/components/widgets/mixed/Widget5.vue";
// import MixedWidget7 from "@/components/widgets/mixed/Widget7.vue";
// import MixedWidget10 from "@/components/widgets/mixed/Widget10.vue";
import { setCurrentPageTitle } from "@/core/helpers/breadcrumb";
import Subjects from "@/components/widgets/tables/Subjects.vue";
import Dropdown2 from "@/components/dropdown/Dropdown2.vue";
// var window : any;
// const KeyLines = window.KeyLines;
// KeyLines.promisify();
import KlChart from "keylines/vue/Chart.vue";
import AssocationsSimple from "@/components/charts/assocations-simple/AssocationsSimple.vue";
import { reactive } from 'vue';
import CardEvents from "@/components/cards/CardEvents.vue";
import AsideDefaultMenu from "@/components/widgets/menus/AsideDefaultMenu.vue";

export default defineComponent({
  name: "dashboard",
  components: {
    Subjects,
    KlChart,
    LMap,
    LIcon,
    LTileLayer,
    LMarker,
    LControlLayers,
    LTooltip,
    LPopup,
    LPolyline,
    LPolygon,
    LRectangle,
    Dropdown2,
    AssocationsSimple,
    CardEvents,
    AsideDefaultMenu
  },
  setup() {
    var navigation;
    var routeView;
    const state = reactive({ count: 0, mounted: false })

    onMounted(() => {
      setCurrentPageTitle("Summary");
      state.mounted = true;

      // KeyLines.create({ container: 'kl' }, function (err, chart) {
      //   chart.load({
      //     type: 'LinkChart',
      //     items: [{ id: 'id1', type: 'node', x: 150, y: 150, t: 'Hello World!' }]
      //   });
      // });

      // $("#kt_datatable_example_1").DataTable();
      var api_key = "e2596674243d85b8ccc9b41ae77c1aee";
      var map = Wrld.map("map", api_key, {
        center: [37.7858, -122.401],
        zoom: 16
      });
      navigation = new WrldNavigation(null, map, api_key);
      routeView = new WrldRouteView(map);

    });







    const zoom = ref(2);
    const iconWidth = ref(25);
    const iconHeight = ref(40);

    const chartOptions = {
      backColour: "transparent",
      fontFamily: "Spartan, sans-serif",
      fontSize: 10,
      fontColor: "#FFFFFF",
      packing: "adaptive",
      tightness: 10,
      minZoom: 0.6,
    };

    const chartData = {
      // type: "LinkChart",
      // items: [{
      //   // Definition of a node
      //   id: "tamara_black",
      //   type: "node",
      //   t: "Tamara Black", // The node’s text
      //   c: "#B2356D",
      //   d: { email: "tamara.black@enron.com" } // custom node data
      // }, {
      //   // Definition of a link
      //   id: "l1",
      //   id1: "tamara_black",
      //   id2: "maria_valdes"
      // }
      // ]
      type: "LinkChart",
      // items: [
      //   { id: 'id1', type: 'node', c: '#f59d15', t: 'Jon Smith', fs: 10, fbc: 'rgba(0,0,0,0)' },
      //   { id: 'id2', type: 'node', c: '#f59d15', t: 'Jack Smith', fs: 10, fbc: 'rgba(0,0,0,0)' },
      //   { id: 'id3', type: 'node', c: '#f59d15', t: 'Jack Smith2', fs: 10, fbc: 'rgba(0,0,0,0)' },
      //   { id: 'id4', type: 'node', c: '#f59d15', t: 'Jack Smith3', fs: 10, fbc: 'rgba(0,0,0,0)' },

      //   { type: 'link', id: 'a-b1', id1: 'id1', id2: 'id2' },
      //   { type: 'link', id: 'a-b2', id1: 'id2', id2: 'id3' },
      //   { type: 'link', id: 'a-b3', id1: 'id3', id2: 'id4' },
      //   { type: 'link', id: 'a-b4', id1: 'id3', id2: 'id2' },
      //   { type: 'link', id: 'a-b5', id1: 'id3', id2: 'id4' }
      // ]

      items: [
        {
          type: "node",
          id: "ac1",
          u: "/media/keylines-6.8.0-75198/images/icons/bank.png",
          t: "45081063",
        },
        {
          type: "node",
          id: "ac2",
          u: "/media/keylines-6.8.0-75198/images/icons/bank.png",
          t: "91422615",
        },
        {
          type: "node",
          id: "ac3",
          u: "/media/keylines-6.8.0-75198/images/icons/bank.png",
          t: "59798694",
        },
        {
          type: "node",
          id: "ac4",
          u: "/media/keylines-6.8.0-75198/images/icons/bank.png",
          t: "71012007",
        },
        {
          type: "node",
          id: "ac5",
          u: "/media/keylines-6.8.0-75198/images/icons/bank.png",
          t: "29692722",
        },
        {
          type: "node",
          id: "ad1",
          u: "/media/keylines-6.8.0-75198/images/icons/address.png",
          t: "2480 Richards Ave",
        },
        {
          type: "node",
          id: "ad2",
          u: "/media/keylines-6.8.0-75198/images/icons/address.png",
          t: "3731 Farland St",
        },
        {
          type: "node",
          id: "ad3",
          u: "/media/keylines-6.8.0-75198/images/icons/address.png",
          t: "3343 Beechwood Ave",
        },
        {
          type: "node",
          id: "p1",
          u: "/media/svg/avatars/001-boy.svg",
          t: "James HALL",
        },
        {
          type: "node",
          id: "p2",
          u: "/media/svg/avatars/018-girl-9.svg",
          t: "Michelle TURNER",
        },
        {
          type: "node",
          id: "p3",
          u: "/media/svg/avatars/001-boy.svg",
          t: "Ryan TURNER",
        },
        {
          type: "node",
          id: "p4",
          u: "/media/svg/avatars/018-girl-9.svg",
          t: "Jennifer CARTER",
        },
        {
          type: "node",
          id: "p5",
          u: "/media/svg/avatars/018-girl-9.svg",
          t: "Isabella PEREZ",
        },
        {
          type: "node",
          id: "p6",
          u: "/media/svg/avatars/018-girl-9.svg",
          t: "Brittany CAMPBELL",
        },
        {
          type: "link",
          id: "l1",
          id1: "ac1",
          id2: "ac3",
          a1: true,
          c: "#999999",
          w: 15,
        },
        {
          type: "link",
          id: "l2",
          id1: "ac1",
          id2: "ac3",
          a2: true,
          c: "#999999",
          w: 3,
        },
        {
          type: "link",
          id: "l3",
          id1: "ac2",
          id2: "ac1",
          a1: true,
          c: "#999999",
          w: 8,
        },
        {
          type: "link",
          id: "l4",
          id1: "ac2",
          id2: "ac4",
          a2: true,
          c: "#999999",
          w: 12,
        },
        {
          type: "link",
          id: "l5",
          id1: "ac2",
          id2: "ac5",
          a2: true,
          c: "#999999",
          w: 10,
        },
        {
          type: "link",
          id: "l6",
          id1: "ac3",
          id2: "ac2",
          a2: true,
          c: "#999999",
          w: 7,
        },
        { type: "link", id: "l7", id1: "p1", id2: "ac1", c: "#666666", w: 5 },
        { type: "link", id: "l8", id1: "p1", id2: "ad2", c: "#666666", w: 5 },
        { type: "link", id: "l9", id1: "p2", id2: "ad1", c: "#666666", w: 5 },
        { type: "link", id: "l10", id1: "p2", id2: "ac3", c: "#666666", w: 5 },
        { type: "link", id: "l11", id1: "p3", id2: "ac3", c: "#666666", w: 5 },
        { type: "link", id: "l12", id1: "p3", id2: "ad1", c: "#666666", w: 5 },
        { type: "link", id: "l13", id1: "p4", id2: "ad2", c: "#666666", w: 5 },
        { type: "link", id: "l14", id1: "p4", id2: "ac4", c: "#666666", w: 5 },
        { type: "link", id: "l15", id1: "p5", id2: "ad3", c: "#666666", w: 5 },
        { type: "link", id: "l16", id1: "p5", id2: "ac2", c: "#666666", w: 5 },
        { type: "link", id: "l17", id1: "p6", id2: "ad3", c: "#666666", w: 5 },
        { type: "link", id: "l18", id1: "p6", id2: "ac5", c: "#666666", w: 5 },
      ],
    };

    return {
      zoom,
      iconWidth,
      iconHeight,
      chartOptions,
      chartData,
      state,
      // navigation,
      // routeView
    };
  },

  methods: {
    iconSize() {
      return [this.iconWidth, this.iconHeight];
    },
    iconUrl() {
      return `https://placekitten.com/${this.iconWidth}/${this.iconHeight}`;
    },
    itemTitle(item) {
      let result = item.i;
      if (item.static) {
        result += " - Static";
      }
      return result;
    },

    log(a) {
      console.log(a);
    },
    changeIcon() {
      this.iconWidth += 2;
      if (this.iconWidth > this.iconHeight) {
        this.iconWidth = Math.floor(this.iconHeight / 2);
      }
    },


    // clearRoute() {
    //   this.routeView.clearDirections();
    // },

    // findRoute() {
    //   var startLocation = WrldNavigation.buildLocation("Westport House", 56.4600344, -2.9783117);
    //   var endLocation = WrldNavigation.buildLocation("Abertay", 56.463008, -2.974135);
    //   this.navigation.findRoute(startLocation, endLocation, this.findRouteCallback);
    // },

    // findRouteCallback(result) {
    //   if (result.route) {
    //     this.navigation.buildDirectionsForRoute(result.route, this.buildDirectionsCallback);
    //   }
    // },

    // buildDirectionsCallback(result) {
    //   if (result.directions) {
    //     this.routeView.setDirections(result.directions);
    //   }
    // }

  },
});
</script>
