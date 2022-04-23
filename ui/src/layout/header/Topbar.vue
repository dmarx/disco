<template>
<div>
</div>
  <!-- <div class="d-flex align-items-stretch flex-shrink-0">
    <div class="d-flex align-items-stretch ms-1 ms-lg-3">
      <KTSearch></KTSearch>
    </div>
    <div class="d-flex align-items-center ms-1 ms-lg-3">
      <div
        class="btn btn-icon btn-active-light-primary w-30px h-30px w-md-40px h-md-40px"
        id="kt_activities_toggle"
      >
        <span class="svg-icon svg-icon-1">
          <inline-svg src="media/icons/duotune/general/gen032.svg" />
        </span>
      </div>
    </div>
    <div class="d-flex align-items-center ms-1 ms-lg-3">
      <div
        class="btn btn-icon btn-active-light-primary w-30px h-30px w-md-40px h-md-40px"
        data-kt-menu-trigger="click"
        data-kt-menu-attach="parent"
        data-kt-menu-placement="bottom-end"
        data-kt-menu-flip="bottom"
      >
        <span class="svg-icon svg-icon-1">
          <inline-svg src="media/icons/duotune/general/gen025.svg" />
        </span>
      </div>
      <KTQuickLinksMenu></KTQuickLinksMenu>
    </div>
    <div class="d-flex align-items-center ms-1 ms-lg-3">
      <div
        class="btn btn-icon btn-active-light-primary position-relative w-30px h-30px w-md-40px h-md-40px"
        id="kt_drawer_chat_toggle"
      >
        <span class="svg-icon svg-icon-1">
          <inline-svg src="media/icons/duotune/communication/com012.svg" />
        </span>

        <span
          class="bullet bullet-dot bg-success h-6px w-6px position-absolute translate-middle top-0 start-50 animation-blink"
        >
        </span>
      </div>
    </div>

    <div class="d-flex align-items-center ms-1 ms-lg-3">
      <div
        class="btn btn-icon btn-active-light-primary position-relative w-30px h-30px w-md-40px h-md-40px"
        data-kt-menu-trigger="click"
        data-kt-menu-attach="parent"
        data-kt-menu-placement="bottom-end"
        data-kt-menu-flip="bottom"
      >
        <span class="svg-icon svg-icon-1">
          <inline-svg src="media/icons/duotune/general/gen022.svg" />
        </span>
      </div>
      <KTNotificationsMenu></KTNotificationsMenu>
    </div>
    <div
      class="d-flex align-items-center ms-1 ms-lg-3"
      id="kt_header_user_menu_toggle"
    >
      <div
        class="cursor-pointer symbol symbol-30px symbol-md-40px"
        data-kt-menu-trigger="click"
        data-kt-menu-attach="parent"
        data-kt-menu-placement="bottom-end"
        data-kt-menu-flip="bottom"
      >
        <img src="media/avatars/300-1.jpg" alt="metronic" />
      </div>
      <KTUserMenu></KTUserMenu>
    </div>
    <div
      class="d-flex align-items-center d-lg-none ms-2 me-n3"
      title="Show header menu"
    >
      <div
        class="btn btn-icon btn-active-light-primary btn-custom w-30px h-30px w-md-40px h-md-40px"
        id="kt_header_menu_mobile_toggle"
      >
        <span class="svg-icon svg-icon-1">
          <inline-svg src="media/icons/duotune/text/txt001.svg" />
        </span>
      </div>
    </div>
  </div> -->
</template>

<script lang="ts">
import { defineComponent } from "vue";
// import KTSearch from "@/layout/header/partials/Search.vue";
// import KTNotificationsMenu from "@/layout/header/partials/NotificationsMenu.vue";
// import KTQuickLinksMenu from "@/layout/header/partials/QuickLinksMenu.vue";
// import KTUserMenu from "@/layout/header/partials/UserMenu.vue";

export default defineComponent({
  name: "topbar",
  components: {
    // KTSearch,
    // KTNotificationsMenu,
    // KTQuickLinksMenu,
    // KTUserMenu,
  },
});
</script>
