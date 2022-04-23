<template>
  <!--begin::Charts Widget 1-->
  <div class="card" :class="widgetClasses">
    <!--begin::Header-->
    <div class="card-header border-0 pt-5">
      <!--begin::Title-->
      <h3 class="card-title align-items-start flex-column">
        <span class="card-label fw-bolder fs-3 mb-1">Recent Statistics</span>

        <span class="text-muted fw-bold fs-7">More than 400 new members</span>
      </h3>
      <!--end::Title-->

      <!--begin::Toolbar-->
      <div class="card-toolbar">
        <!--begin::Menu-->
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
        <Dropdown1></Dropdown1>
        <!--end::Menu-->
      </div>
      <!--end::Toolbar-->
    </div>
    <!--end::Header-->

    <!--begin::Body-->
    <div class="card-body">
      <!--begin::Chart-->
      <div id="kl" style="width: 818px; height: 586px;"></div>
      <!-- <apexchart type="bar" :options="options" :series="series"></apexchart> -->
      <!--end::Chart-->
    </div>
    <!--end::Body-->
  </div>
  <!--end::Charts Widget 1-->
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { getCSSVariableValue } from "@/assets/ts/_utils";
import Dropdown1 from "@/components/dropdown/Dropdown1.vue";
var KeyLines : any;



export default defineComponent({
  name: "kl-chart",
  props: {
    widgetClasses: String,
  },
  components: {
    Dropdown1,
  },
  setup() {
    // KeyLines.create({ container: 'kl' }, function (err, chart) {
    //   chart.load({
    //     type: 'LinkChart',
    //     items: [{ id: 'id1', type: 'node', x: 150, y: 150, t: 'Hello World!' }]
    //   });
    // });
  },
});
</script>
