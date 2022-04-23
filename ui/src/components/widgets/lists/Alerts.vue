<template>
  <!--begin::List Widget 6-->
  <div class="card" :class="widgetClasses">
    <!--begin::Header-->
    <div class="card-header border-0">
      <h3 class="card-title fw-bolder text-dark">Alerts &amp; Hints</h3>

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
        <Dropdown3></Dropdown3>
        <!--end::Menu-->
      </div>
    </div>
    <!--end::Header-->

    <!--begin::Body-->
    <div class="card-body pt-0">
      <ul class="nav nav-pills nav-pills-custom mb-3">
        
        <li class="nav-item mb-6 me-6 me-lg-6">
          <a
            class="nav-link btn btn-outline btn-flex btn-active-color-primary flex-column overflow-hidden w-80px h-85px pt-5 pb-2"
            data-bs-toggle="pill"
            href="#kt_stats_widget_6_tab_1"
          >
            <div class="nav-icon mb-3">
              <i class="bi bi-list-task" style="font-size:22px;"></i>
            </div>
            <span class="nav-text text-gray-800 fw-bolder fs-6 lh-1">Alerts</span>
            <span class="bullet-custom position-absolute bottom-0 w-100 h-4px bg-primary"></span>
          </a>
        </li>
        <li class="nav-item mb-6 me-6 me-lg-6">
          <a
            class="nav-link btn btn-outline btn-flex btn-active-color-primary flex-column overflow-hidden w-80px h-85px pt-5 pb-2"
            data-bs-toggle="pill"
            href="#kt_stats_widget_6_tab_2"
          >
            <div class="nav-icon mb-3">
              <i class="bi bi-list-check" style="font-size:22px;"></i>
            </div>
            <span class="nav-text text-gray-800 fw-bolder fs-6 lh-1">Hints</span>
            <span class="bullet-custom position-absolute bottom-0 w-100 h-4px bg-primary"></span>
          </a>
        </li>
        <!-- <li class="nav-item mb-3 me-3 me-lg-6">
              <a
                class="nav-link btn btn-outline btn-flex btn-active-color-primary flex-column overflow-hidden w-80px h-85px pt-5 pb-2 active"
                data-bs-toggle="pill"
                href="#kt_stats_widget_6_tab_3"
              >
                <div class="nav-icon mb-3">
                  <i class="fonticon-drone fs-1 p-0"></i>
                </div>
                <span class="nav-text text-gray-800 fw-bolder fs-6 lh-1">Drone</span>
                <span class="bullet-custom position-absolute bottom-0 w-100 h-4px bg-primary"></span>
              </a>
        </li>-->
      </ul>
      <template v-for="(item, index) in list" :key="index">
        <!--begin::Item-->
        <div
          :class="[
            'mb-7' && list.length - 1 !== index,
            `bg-light-${item.color}`,
          ]"
          class="d-flex align-items-center rounded p-5 mb-7"
        >
          <!--begin::Icon-->
          <span :class="`svg-icon-${item.color}`" class="svg-icon me-5">
            <span class="svg-icon svg-icon-1">
              <inline-svg src="media/icons/duotune/abstract/abs027.svg" />
            </span>
          </span>
          <!--end::Icon-->

          <!--begin::Title-->
          <div class="flex-grow-1 me-2">
            <a href="#" class="fw-bolder text-gray-800 text-hover-primary fs-6">{{ item.title }}</a>

            <span class="text-muted fw-bold d-block">{{ item.text }}</span>
          </div>
          <!--end::Title-->

          <!--begin::Lable-->
          <span :class="`text-${item.color}`" class="fw-bolder py-1">
            {{
              item.number
            }}
          </span>
          <!--end::Lable-->
        </div>
        <!--end::Item-->
      </template>
    </div>
    <!--end::Body-->
  </div>
  <!--end::List Widget 6-->
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import Dropdown3 from "@/components/dropdown/Dropdown3.vue";

export default defineComponent({
  name: "kt-widget-6",
  components: {
    Dropdown3,
  },
  props: {
    widgetClasses: String,
  },
  setup() {
    const list = ref([
      {
        color: "warning",
        icon: "icons/duotune/abstract/abs027.svg",
        title: "New OSINT data matches",
        text: "Data attribution suggestion",
        number: "30 mins ago",
      },
      {
        color: "success",
        icon: "icons/duotune/art/art005.svg",
        title: "New entities resolved",
        text: "Entity resolution service",
        number: "+50%",
      },
      {
        color: "danger",
        icon: "icons/duotune/communication/com012.svg",
        title: "Detection of data against Fusion source",
        text: "Watchlist monitoring",
        number: "-27%",
      },
      {
        color: "info",
        icon: "icons/duotune/communication/com012.svg",
        title: "Suggested report to review",
        text: "Pattern finder service",
        number: "+8%",
      },
    ]);

    return {
      list,
    };
  },
});
</script>
