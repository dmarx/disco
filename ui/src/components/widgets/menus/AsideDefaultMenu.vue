<template>
  <div
    class="menu-item menu-accordion"
    data-kt-menu-sub="accordion"
    data-kt-menu-trigger="click"
  >
    <div class="menu-content pt-8 pb-2">
      <span class="menu-section text-muted text-uppercase fs-8 ls-1"
        >Projects</span
      >
    </div>
    <span class="menu-link">
      <span class="menu-icon">
        <i class="bi bi-bag-check-fill fs-2x"></i>
      </span>
      <span class="menu-title">My Projects</span>
    </span>
    <span class="menu-link">
      <span class="menu-icon">
        <i class="bi bi-card-list fs-2x"></i>
      </span>
      <span class="menu-title">Shared Projects</span>
    </span>
    <span class="menu-link">
      <span class="menu-icon">
        <i class="bi bi-link-45deg fs-2x"></i>
      </span>
      <span class="menu-title">Closed Projects</span>
    </span>
  </div>

  <!--       
  <div class="menu-item">
    <div class="menu-content pt-8 pb-2">
      <span class="menu-section text-muted text-uppercase fs-8 ls-1">Browse case</span>
    </div>
    <router-link to="/case/dashboard">
      <span class="menu-link">
        <span class="menu-icon">
          <i class="bi bi-code-square fs-2x"></i>
        </span>
        <span class="menu-title">All events &amp; locations</span>
      </span>
    </router-link>
  </div>

  <div class="menu-item menu-accordion" data-kt-menu-sub="accordion" data-kt-menu-trigger="click">
    <div class="menu-content pt-8 pb-2">
      <span class="menu-section text-muted text-uppercase fs-8 ls-1">Recent activity</span>
    </div>
    <router-link to="#">
      <span class="menu-link">
        <span class="menu-icon">
          <i class="bi bi-bag-check-fill fs-2x"></i>
        </span>
        <span class="menu-title">My Alerts &amp; Hints</span>
      </span>
    </router-link>
    <router-link to="#">
      <span class="menu-link">
        <span class="menu-icon">
          <i class="bi bi-card-list fs-2x"></i>
        </span>
        <span class="menu-title">All Tasks</span>
      </span>
    </router-link>
    <router-link to="#">
      <span class="menu-link">
        <span class="menu-icon">
          <i class="bi bi-link-45deg fs-2x"></i>
        </span>
        <span class="menu-title">My Tasks</span>
      </span>
    </router-link>
  </div>

  <div class="menu-item menu-accordion" data-kt-menu-sub="accordion" data-kt-menu-trigger="click">
    <div class="menu-content pt-8 pb-2">
      <span class="menu-section text-muted text-uppercase fs-8 ls-1">Case Links</span>
    </div>
    <router-link to="/case/contents">
      <span class="menu-link">
        <span class="menu-icon">
          <i class="bi bi-file-earmark-pdf-fill fs-2x"></i>
        </span>
        <span class="menu-title">Case files and uploads</span>
      </span>
    </router-link>
    <router-link to="/case/attribution">
      <span class="menu-link">
        <span class="menu-icon">
          <i class="bi bi-people-fill fs-2x"></i>
        </span>
        <span class="menu-title">People of interest</span>
      </span>
    </router-link>
    <router-link to="/case/contents">
      <span class="menu-link">
        <span class="menu-icon">
          <i class="bi bi-briefcase-fill fs-2x"></i>
        </span>
        <span class="menu-title">Case reports</span>
      </span>
    </router-link>
  </div> -->
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "aside_default_menu",
  components: {},
  props: {
    widgetClasses: String,
  },
  setup() {
    const items = [
      // {
      //   icon: "media/icons/duotune/abstract/abs027.svg",
      //   color: "success",
      //   title: "Project Briefing",
      //   description: "Project Manager",
      // },
      // {
      //   icon: "media/icons/duotune/art/art005.svg",
      //   color: "warning",
      //   title: "Concept Design",
      //   description: "Art Director",
      // },
      // {
      //   icon: "media/icons/duotune/communication/com012.svg",
      //   color: "primary",
      //   title: "Functional Logics",
      //   description: "Lead Developer",
      // },
      // {
      //   icon: "media/icons/duotune/coding/cod008.svg",
      //   color: "danger",
      //   title: "Development",
      //   description: "DevOps",
      // },
      // {
      //   icon: "media/icons/duotune/general/gen049.svg",
      //   color: "info",
      //   title: "Testing",
      //   description: "QA Managers",
      // },
    ];

    return {
      items,
    };
  },
});
</script>
