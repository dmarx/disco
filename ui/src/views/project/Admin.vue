<template>
  <div v-if="state.mounted">
    <Teleport to="#aside-context">
      <div class="menu-item">
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">Browse Settings</span>
        </div>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-code-square fs-2x"></i>
          </span>
          <span class="menu-title">Options</span>
        </span>
      </div>

    </Teleport>
  </div>
  <!-- <div class="d-flex flex-column flex-lg-row">
    <div class="flex-lg-row-fluid me-lg-15 order-2 order-lg-1 mb-10 mb-lg-0">
      <Details></Details>
      <Events></Events>
      <Invoices></Invoices>
    </div>
    <div class="flex-column flex-lg-row-auto w-lg-250px w-xl-300px mb-10 order-1 order-lg-2">
      <Summary></Summary>
    </div>
  </div> -->
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import Details from "@/components/subscriptions/view/Details.vue";
import Events from "@/components/subscriptions/view/Events.vue";
import Invoices from "@/components/subscriptions/view/Invoices.vue";
import Summary from "@/components/subscriptions/view/Summary.vue";
import { setCurrentPageBreadcrumbs } from "@/core/helpers/breadcrumb";
import { reactive } from 'vue';

export default defineComponent({
  name: "admin",
  components: {
    Details,
    Events,
    Invoices,
    Summary,
  },
  setup() {
    const state = reactive({ count: 0, mounted: false })
    onMounted(() => {
      setCurrentPageBreadcrumbs("Account Details", ["Apps", "Admin"]);
      state.mounted = true;
    });

    return {
      state,

    }
  },
});
</script>
