<template>
  <div v-if="state.mounted">
    <Teleport to="#aside-context">
      <div class="menu-item">
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">Browse events</span>
        </div>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-code-square fs-2x"></i>
          </span>
          <span class="menu-title">All events &amp; locations</span>
        </span>
      </div>

      <div
        class="menu-item menu-accordion"
        data-kt-menu-sub="accordion"
        data-kt-menu-trigger="click"
      >
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">Financial</span>
        </div>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-bag-check-fill fs-2x"></i>
          </span>
          <span class="menu-title">Account summary</span>
        </span>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-card-list fs-2x"></i>
          </span>
          <span class="menu-title">All transactions</span>
        </span>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-link-45deg fs-2x"></i>
          </span>
          <span class="menu-title">Linked transactions</span>
        </span>
      </div>

     
    </Teleport>
  </div>
  <div
    class="card card-flush pb-0 bgi-position-y-center bgi-no-repeat mb-10"
    style="background-size: auto calc(100% + 10rem); background-position-x: 100%; background-image: url('/metronic8/demo1/assets/media/illustrations/sketchy-1/4.png')"
  >
    <div class="card-header pt-10">
      <div class="d-flex align-items-center">
        <div class="symbol symbol-circle me-5">
          <div
            class="symbol-label bg-transparent text-primary border border-secondary border-dashed"
          >
            <span class="svg-icon svg-icon-2x svg-icon-primary">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
              >
                <path
                  d="M17.302 11.35L12.002 20.55H21.202C21.802 20.55 22.202 19.85 21.902 19.35L17.302 11.35Z"
                  fill="black"
                />
                <path
                  opacity="0.3"
                  d="M12.002 20.55H2.802C2.202 20.55 1.80202 19.85 2.10202 19.35L6.70203 11.45L12.002 20.55ZM11.302 3.45L6.70203 11.35H17.302L12.702 3.45C12.402 2.85 11.602 2.85 11.302 3.45Z"
                  fill="black"
                />
              </svg>
            </span>
          </div>
        </div>
        <div class="d-flex flex-column">
          <h2 class="mb-1">Workspaces</h2>
          <div class="text-muted fw-bolder">
            <a href="#">Create Workspace</a>
            <span class="mx-3">|</span>
            Selected Workspace:&nbsp;
            <b>
              <span style="color:#000">Subject Analysis</span>
            </b>
            <span class="mx-3">|</span>140 entities
            <span class="mx-3">|</span>10 subjects
          </div>
        </div>
      </div>
    </div>
    <div class="card-body pb-0">
      <ul
        class="nav nav-custom nav-tabs nav-line-tabs nav-stretch nav-line-tabs-2x border-0 fs-4 fw-bold mb-8"
        style="    position: absolute;
    right: 0;
    top: 156px;
    right:28%;
    z-index: 11;"
      >
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4 active"
            data-bs-toggle="tab"
            href="#kt_workspace_network_tab"
          >All Associations</a>
        </li>
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4"
            @click="switchTab(2)"
            data-bs-toggle="tab"
            href="#kt_workspace_social_tab"
          >Social Network</a>
        </li>
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4"
            @click="switchTab(3)"
            data-bs-toggle="tab"
            href="#kt_workspace_connection_tab"
          >Connection Graph</a>
        </li>
      </ul>
    </div>
  </div>
  <div class="tab-content" id="myTabContent" style="flex-grow: 1;
    width: 100%;">
    <div class="tab-pane fade show active" id="kt_workspace_network_tab" role="tabpanel" style="height:100%">
      <FilterMap ref="filterMap"></FilterMap>
    </div>
    <div class="tab-pane fade" id="kt_workspace_social_tab" role="tabpanel" style="height:100%">
      <SocialMapping ref="socialMapping"></SocialMapping>
    </div>
    <div class="tab-pane fade" id="kt_workspace_connection_tab" role="tabpanel" style="height:100%">
      <MafiaMap ref="mafiaMap"></MafiaMap>
    </div>  
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { setCurrentPageTitle } from "@/core/helpers/breadcrumb";
// import KlChart from "keylines/vue/Chart.vue";
import FilterMap from "@/components/charts/filtermap/FilterMapping.vue";
import Dropdown2 from "@/components/dropdown/Dropdown2.vue";
import SocialMapping from "@/components/charts/socialmap/SocialMapping.vue";
import MafiaMap from "@/components/charts/mafia/MafiaMap.vue";
import { reactive } from 'vue';

export default defineComponent({
  name: "workspace",
  components: {
    // KlChart,
    Dropdown2,
    FilterMap,
    SocialMapping,
    MafiaMap
  },
  setup() {

    const filterMap = ref();
    const socialMapping = ref();
    const mafiaMap = ref();
    const state = reactive({ count: 0, mounted: false })

    onMounted(() => {
      setCurrentPageTitle("Workspace");
      state.mounted = true;
    });

    const chartOptions = {
      backColour: "transparent",
      fontFamily: "Spartan, sans-serif",
      fontSize: 10,
      fontColor: "#FFFFFF",
    };

    var chartData = {
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
          u: "/media/keylines-6.8.0-75198/images/icons/man.png",
          t: "James HALL",
        },
        {
          type: "node",
          id: "p2",
          u: "/media/keylines-6.8.0-75198/images/icons/woman.png",
          t: "Michelle TURNER",
        },
        {
          type: "node",
          id: "p3",
          u: "/media/keylines-6.8.0-75198/images/icons/man.png",
          t: "Ryan TURNER",
        },
        {
          type: "node",
          id: "p4",
          u: "/media/keylines-6.8.0-75198/images/icons/woman.png",
          t: "Jennifer CARTER",
        },
        {
          type: "node",
          id: "p5",
          u: "/media/keylines-6.8.0-75198/images/icons/woman.png",
          t: "Isabella PEREZ",
        },
        {
          type: "node",
          id: "p6",
          u: "/media/keylines-6.8.0-75198/images/icons/woman.png",
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

    // chartData = json;

    return {
      socialMapping, mafiaMap, filterMap, chartOptions, chartData,
      state,
    };
  },
  methods: {
    switchTab(i) {
      console.log(i);
      switch (i) {
        case 1:
          break;
        case 2:
          console.log('social');
          this.socialMapping.fit();//runLayout(true,'full');
          break;
        case 3:
          console.log('mafiaMap');
          this.mafiaMap.fit();//runLayout(true,'full');
          break;
      }
    }
  }
});
</script>
