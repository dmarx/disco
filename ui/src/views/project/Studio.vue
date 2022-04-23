<template>
  <div class="row">
    <div class="col-12">
      <div>
        <div
          class="card card-flush pb-0 bgi-position-y-center bgi-no-repeat mb-10"
          style="
            margin-top: 14px;
            background-size: auto calc(100% + 10rem);
            background-position-x: 100%;
            background-image: url('/metronic8/demo1/assets/media/illustrations/sketchy-1/4.png');
          "
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
                        fill="currentColor"
                      ></path>
                      <path
                        opacity="0.3"
                        d="M12.002 20.55H2.802C2.202 20.55 1.80202 19.85 2.10202 19.35L6.70203 11.45L12.002 20.55ZM11.302 3.45L6.70203 11.35H17.302L12.702 3.45C12.402 2.85 11.602 2.85 11.302 3.45Z"
                        fill="currentColor"
                      ></path>
                    </svg>
                  </span>
                </div>
              </div>

              <div class="d-flex flex-column" style="margin-top: -21px">
                <h2 class="mb-1">Settings</h2>
                <div class="text-muted fw-bolder" style="line-height: 2px">
                  <a href="#">Disco Studio</a>
                  <!-- <span class="mx-3">|</span> -->
                  <!-- <a href="#">Studio</a> -->
                  <span class="mx-3">|</span>Status
                  <span class="mx-3">Idle</span>
                </div>
              </div>
            </div>
          </div>

          <div class="card-body pb-0">
            <div class="d-flex overflow-auto h-55px">
              <ul
                class="nav nav-stretch nav-line-tabs nav-line-tabs-2x border-transparent fs-5 fw-bold flex-nowrap"
              >
                <li class="nav-item">
                  <a
                    class="nav-link text-active-primary me-6 active"
                    href="/metronic8/demo1/../demo1/apps/file-manager/folders.html"
                    >Scenes</a
                  >
                </li>

                <li class="nav-item">
                  <a
                    class="nav-link text-active-primary me-6"
                    href="/metronic8/demo1/../demo1/apps/file-manager/settings.html"
                    >Tools</a
                  >
                </li>

                <li class="nav-item">
                  <a
                    class="nav-link text-active-primary me-6"
                    href="/metronic8/demo1/../demo1/apps/file-manager/settings.html"
                    >Preview</a
                  >
                </li>
                <li class="nav-item">
                  <a
                    class="nav-link text-active-primary me-6"
                    href="/metronic8/demo1/../demo1/apps/file-manager/settings.html"
                    >Post Process</a
                  >
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="card card-flush">
          <div class="card-header pt-8" style="position: absolute; width: 400px">
            <div class="card-title">
              <h2>Design Scene</h2>
            </div>
          </div>

          <div class="card-body" style="">
            <div class="row">
              <div class="col-6" style="max-height: 500px">
                <VueFlow
                  v-model="elements"
                  class="vue-flow-basic-example"
                  :default-zoom="1.0"
                  :min-zoom="1.0"
                  :max-zoom="1.0"
                  :zoom-on-scroll="false"
                  @connect="onConnect"
                  @pane-ready="onPaneReady"
                  @node-drag-stop="onNodeDragStop"
                >
                  <Background />
                  <!-- <MiniMap /> -->
                  <!-- <Controls /> -->
                  <!-- <div style="position: absolute; right: 10px; top: 10px; z-index: 4">
                <button style="margin-right: 5px" @click="resetTransform">
                  reset transform
                </button>
                <button style="margin-right: 5px" @click="updatePos">change pos</button>
                <button style="margin-right: 5px" @click="toggleclass">
                  toggle class
                </button>
                <button @click="logToObject">toObject</button>
              </div> -->
                </VueFlow>
              </div>
              <div class="col-6">
                <Vue3LiveForm :schema="schema" v-model="model" />
              </div>
            </div>
          </div>

          <div v-if="state.mounted">
            <Teleport to="#aside-context">
              <AsideDefaultMenu></AsideDefaultMenu>
            </Teleport>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, reactive } from "vue";
import {
  VueFlow,
  Background,
  MiniMap,
  Controls,
  Elements,
  FlowEvents,
  FlowInstance,
  isNode,
  addEdge,
} from "@braks/vue-flow";

// import { setCurrentPageTitle } from "@core/helpers/breadcrumb";
import { Vue3LiveForm } from "vue3-live-form";

// import Dropdown2 from "@/components/dropdown/Dropdown2.vue";
// var window : any;
// const KeyLines = window.KeyLines;
// KeyLines.promisify();
import FilterTimeline from "../../components/filters/FilterTimeline.vue";
import test_data from "../../assets/data/generators/test/defaults.json";
import test_schema from "../../assets/data/generators/test/schema.json";
import AsideDefaultMenu from "@/components/widgets/menus/AsideDefaultMenu.vue";

export default defineComponent({
  name: "studio",
  components: {
    FilterTimeline,
    AsideDefaultMenu,
    Vue3LiveForm,
    VueFlow,
    Background,
    MiniMap,
    Controls,
  },
  setup() {
    const state = reactive({
      count: 0,
      mounted: false,
    });
    const schema = test_schema; // = reactive (news_schema);
    const model = test_data; // = reactive ({});

    // const elements = ref([
    //   {
    //     id: "1",
    //     label: "node 1",
    //     position: { x: 100, y: 100 },
    //   },
    //   {
    //     id: "2",
    //     label: "node 2",
    //     position: { x: 100, y: 200 },
    //   },
    //   {
    //     id: "e1-2",
    //     target: "2",
    //     source: "1",
    //   },
    // ]);

    console.log(schema);

    // const currentStatus = reactive({
    //   busy: false,
    //   text: "Idle",
    //   mounted: false,
    // });

    // const currentProject = reactive({
    //   busy: false,
    //   text: "",
    //   steps: 50,
    //   resolution: "1280,768",
    // });

    onMounted(() => {
      // setCurrentPageTitle("Studio");
      state.mounted = true;

      axios
        .get('http://localhost:5000/fetch_projects')
        .then(response => {
          this.info = response;
        }


    });

    
    // const loadProjects = () => {
    //   fetch("http://localhost:5000/status").then((response) => {
    //     response.json().then(function (data) {
    //       console.log("status response", data);
    //       // if (data.busy) {
    //       //   isBusy = true;
    //       //   //showLoading();
    //       //   setTimeout((x) => {
    //       //     updateStatus();
    //       //   }, 5000);
    //       // } else {
    //       //   //showReady();
    //       // }

    //       //updateCurrentMash();

    //       // $("#logs").html(
    //       //   data.logs.reverse().map((x) => {
    //       //     return "<div>" + x + "</div>";
    //       //   })
    //       // );
    //       // $("#logs").scrollTop($("#logs")[0].scrollHeight);
    //       // // console.log('updated logs');

    //       // $(".queue-info").hide();
    //       // if (parseInt(data.queued) > 0) {
    //       //   $(".queue-info").show();
    //       //   $(".queue-info-body").html(data.queued);
    //       // }
    //     });
    //   });
    // };


    return {
      // status,
      // currentStatus,
      state,
      schema,
      model,

      loadProjects,
      
      instance: null as FlowInstance | null,
      elements: [
        { id: "1", type: "input", label: "Grid-3-ML", position: { x: 250, y: 5 } },
        { id: "2", label: "Superres", position: { x: 100, y: 100 } },
        { id: "3", label: "Disco Diffusion", position: { x: 400, y: 100 } },
        { id: "4", label: "Superres", position: { x: 400, y: 200 } },
        { id: "e1-2", source: "1", target: "2", animated: true },
        { id: "e1-3", source: "1", target: "3" },
        { id: "e1-3", source: "3", target: "4" },
        { id: "e1-4", source: "4", target: "5" },
      ] as Elements,
    };
  },

  methods: {
    // iconSize() {
    //   return [this.iconWidth, this.iconHeight];
    // },
    // iconUrl() {
    //   return `https://placekitten.com/${this.iconWidth}/${this.iconHeight}`;
    // },
    // submit(e) {
    //   // this.model contains the valid data according your JSON Schema.
    //   // You can submit your model to the server here
    // },

    logToObject() {
      console.log(this.instance?.toObject());
    },
    resetTransform() {
      this.instance?.setTransform({ x: 0, y: 0, zoom: 1 });
    },
    toggleclass() {
      this.elements.forEach((el) => (el.class = el.class === "light" ? "dark" : "light"));
    },
    updatePos() {
      this.elements.forEach((el) => {
        if (isNode(el)) {
          el.position = {
            x: Math.random() * 400,
            y: Math.random() * 400,
          };
        }
      });
    },
    onNodeDragStop(e: FlowEvents["nodeDragStop"]) {
      console.log("drag stop", e);
    },
    onPaneReady(instance: FlowEvents["paneReady"]) {
      instance.fitView();
      this.instance = instance;
    },
    onConnect(params: FlowEvents["connect"]) {
      addEdge(params, this.elements);
    },
  },
  watch: {},
});
</script>
