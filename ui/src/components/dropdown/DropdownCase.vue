<template>
  <!--begin::Menu 2-->
  <div
    class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-bold w-200px"
    data-kt-menu="true"
  >
    <!--begin::Menu item-->
    <div class="menu-item px-3">
      <div class="menu-content fs-6 text-dark fw-bolder px-3 py-4">
        Quick Actions
      </div>
    </div>
    <!--end::Menu item-->

    <!--begin::Menu separator-->
    <div class="separator mb-3 opacity-75"></div>
    <!--end::Menu separator-->

    <!--begin::Menu item-->
    <!-- <div class="menu-item px-3">
      <a href="/#/case/work-log" class="menu-link px-3"> Open Case </a>
    </div> -->
    <!--end::Menu item-->

    <!--begin::Menu item-->
    <div class="menu-item px-3">
      <a href="/#/case/data" class="menu-link px-3"> Upload Data </a>
    </div>
     <div class="menu-item px-3">
      <a href="/#/case/search" class="menu-link px-3"> Search </a>
    </div>
     <div class="menu-item px-3">
      <a href="/#/case/capture" class="menu-link px-3"> Capture </a>
    </div>
    <!--end::Menu item-->

    <!-- <div
      class="menu-item px-3"
      data-kt-menu-trigger="hover"
      data-kt-menu-placement="right-start"
      data-kt-menu-flip="left-start, top"
    >
      <a href="#" class="menu-link px-3">
        <span class="menu-title">New Group</span>
        <span class="menu-arrow"></span>
      </a>
      <div class="menu-sub menu-sub-dropdown w-175px py-4">
        <div class="menu-item px-3">
          <a href="#" class="menu-link px-3"> Admin Group </a>
        </div>
        <div class="menu-item px-3">
          <a href="#" class="menu-link px-3"> Staff Group </a>
        </div>
        <div class="menu-item px-3">
          <a href="#" class="menu-link px-3"> Member Group </a>
        </div>
      </div>
    </div>
    <div class="menu-item px-3">
      <a href="#" class="menu-link px-3"> New Contact </a>
    </div> -->
    <div class="separator mt-3 opacity-75"></div>
    <div class="menu-item px-3">
      <div class="menu-content px-3 py-3">
        <a class="btn btn-primary btn-sm px-4" href="/#/case/work-log"> Open Case </a>
      </div>
    </div>
  </div>
  <!--end::Menu 2-->
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "dropdown-2",
  components: {},
});
</script>
