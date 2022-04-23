<template>
  <div v-if="state.mounted">
    <Teleport to="#aside-context">
      <!-- <div class="menu-item">
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">CASES</span>
        </div>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-code-square fs-2x"></i>
          </span>
          <span class="menu-title">All events &amp; locations</span>
        </span>
      </div> -->

      <div
        class="menu-item menu-accordion"
        data-kt-menu-sub="accordion"
        data-kt-menu-trigger="click"
      >
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">Projects</span>
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
      <div
        class="menu-item menu-accordion"
        data-kt-menu-sub="accordion"
        data-kt-menu-trigger="click"
      >
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">Investigation tools</span>
        </div>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-file-earmark-pdf-fill fs-2x"></i>
          </span>
          <span class="menu-title">Case reports &amp; evidence</span>
        </span>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-people-fill fs-2x"></i>
          </span>
          <span class="menu-title">People of interest</span>
        </span>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-briefcase-fill fs-2x"></i>
          </span>
          <span class="menu-title">Case log</span>
        </span>
      </div> -->
    </Teleport>
  </div>

</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { setCurrentPageTitle } from "@/core/helpers/breadcrumb";
import { reactive } from 'vue';

export default defineComponent({
  name: "cases",
  components: {
  },
  setup() {
    const state = reactive({ count: 0, mounted: false })
    onMounted(() => {
      setCurrentPageTitle("Projects");
      state.mounted = true;
    });
    return {
      state,
    }
  },
});
</script>
