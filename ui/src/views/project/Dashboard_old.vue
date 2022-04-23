<template>
  <!--begin::Dashboard-->
  <div class="row gy-5 g-xl-8">
    <div class="col-xxl-8">
      <div class="card">
        <div class="card-header border-0">
          <h3 class="card-title fw-bolder text-dark">Data Map</h3>
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
          <div style="height: 600px; width: 100%;">
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
                <l-icon :icon-url="iconUrl" :icon-size="iconSize" />
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
            <!-- <button @click="changeIcon">New kitten icon</button> -->
          </div>
        </div>
      </div>
    </div>
    <div class="col-xxl-4">
      <div class="row gy-5 gx-xl-8">
        <div class="col-xxl-12">
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
          <br />
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
      <!-- <TableWidget5 widget-classes="card-xxl-stretch mb-5 mb-xxl-8"></TableWidget5> -->
    </div>
  </div>
  <br />
  <br />
  <div class="row gy-5 gx-xl-8">
    <div class="col-xxl-12">
      <div class="card">
        <div class="card-header border-0">
          <h3 class="card-title fw-bolder text-dark">All Events &amp; Transactions</h3>
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
          <table id="kt_datatable_example_1" class="table table-row-bordered gy-5">
            <thead>
              <tr class="fw-bold fs-6 text-muted">
                <th>Ref</th>
                <th>Call ID</th>
                <th>Start time</th>
                <th>Duration</th>
                <th>Type</th>
                <th>First Location</th>
                <th>Last Location</th>
                <th>Entity</th>
                <th>Subject Attribution</th>
                <th>Receiver</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
                <td>Birmingham</td>
                <td>Manchester</td>
                <td>078417900765</td>
                <td>Subject 2</td>
                <td>0845 300 235</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
                <td>Birmingham</td>
                <td>Manchester</td>
                <td>078417900765</td>
                <td>Subject 2</td>
                <td>0845 300 235</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
                <td>Birmingham</td>
                <td>Manchester</td>
                <td>078417900765</td>
                <td>Subject 2</td>
                <td>0845 300 235</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
                <td>Birmingham</td>
                <td>Manchester</td>
                <td>078417900765</td>
                <td>Subject 2</td>
                <td>0845 300 235</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
                <td>Birmingham</td>
                <td>Manchester</td>
                <td>078417900765</td>
                <td>Subject 2</td>
                <td>0845 300 235</td>
              </tr>
              <tr>
                <td>45</td>
                <td>ID 4587</td>
                <td>14-09-14 13:48</td>
                <td>17 mins</td>
                <td>Voice call</td>
                <td>Birmingham</td>
                <td>Manchester</td>
                <td>078417900765</td>
                <td>Subject 2</td>
                <td>0845 300 235</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <th>Ref</th>
                <th>Call ID</th>
                <th>Start time</th>
                <th>Duration</th>
                <th>Type</th>
                <th>First Location</th>
                <th>Last Location</th>
                <th>Entity</th>
                <th>Subject Attribution</th>
                <th>Receiver</th>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    </div>
  </div>
  <!--end::Dashboard-->
</template>

<script lang="ts">
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
import { defineComponent, onMounted, ref } from "vue";
import TableWidget5 from "@/components/widgets/tables/Widget5.vue";
import { setCurrentPageTitle } from "@/core/helpers/breadcrumb";
import Dropdown2 from "@/components/dropdown/Dropdown2.vue";

export default defineComponent({
  name: "dashboard",
  components: {
    // TableWidget5,
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
    Dropdown2
  },
  setup() {
    onMounted(() => {
      setCurrentPageTitle("Dashboard");
    });

    const zoom = ref(2);
    const iconWidth = ref(25);
    const iconHeight = ref(40);

    return {
      zoom,
      iconWidth,
      iconHeight
    }
  },

  iconUrl() {
    return `https://placekitten.com/${this.iconWidth}/${this.iconHeight}`;
  },
  iconSize() {
    return [this.iconWidth, this.iconHeight];
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
});
</script>
