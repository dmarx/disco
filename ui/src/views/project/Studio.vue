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
          <div class="card-header pt-10" style="width: 100%">
            <div class="d-flex align-items-center" style="width: 100%">
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

              <div
                class="d-flex flex-column"
                style="margin-top: -21px; width: 100%"
                v-if="state.project"
              >
                <h2 class="mb-1">Settings</h2>
                <div class="text-muted fw-bolder" style="line-height: 2px">
                  <div style="float: right">
                    <button class="btn btn-primary" @click="saveProject()">
                      Save Project</button
                    ><!-- <router-link to="item.id"> Launch </router-link> -->
                  </div>
                  <input
                    type="text"
                    class="form-control"
                    name="title"
                    placeholder="Title..."
                    v-model="state.project.title"
                    style="
                      display: inline-block;
                      width: 200px;
                      color: white;
                      margin-right: 15px;
                      background: transparent;
                    "
                  />
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
              <div
                class="col-6"
                style="max-height: 500px; min-height: 500px"
                @drop="onDrop"
              >
                <VueFlow
                  v-if="state.project"
                  v-model="state.project.chain"
                  class="vue-flow-basic-example"
                  :default-zoom="1.0"
                  :min-zoom="1.0"
                  :max-zoom="1.0"
                  :zoom-on-scroll="false"
                  @connect="onConnect"
                  @pane-ready="onPaneReady"
                  @node-drag-stop="onNodeDragStop"
                  @dragover="onDragOver"
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
              <div class="col-6"></div>
            </div>
          </div>
          <div v-if="state.mounted">
            <Teleport to="#aside-context">
              <!-- <AsideDefaultMenu></AsideDefaultMenu> -->
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
                <router-link to="/projects">
                  <span class="menu-link">
                    <span class="menu-icon">
                      <i class="bi bi-bag-check-fill fs-2x"></i>
                    </span>
                    <span class="menu-title">My Projects</span>
                  </span>
                </router-link>
                <router-link to="/projects">
                  <span class="menu-link">
                    <span class="menu-icon">
                      <i class="bi bi-card-list fs-2x"></i>
                    </span>
                    <span class="menu-title">Shared Projects</span>
                  </span>
                </router-link>
                <router-link to="/projects">
                  <span class="menu-link">
                    <span class="menu-icon">
                      <i class="bi bi-link-45deg fs-2x"></i>
                    </span>
                    <span class="menu-title">Closed Projects</span>
                  </span>
                </router-link>
              </div>

              <div
                class="menu-item menu-accordion"
                data-kt-menu-sub="accordion"
                data-kt-menu-trigger="click"
              >
                <div class="menu-content pt-8 pb-2">
                  <span class="menu-section text-muted text-uppercase fs-8 ls-1"
                    >Generators</span
                  >
                </div>
                <!-- <router-link to="/projects">
                  <span class="menu-link">
                    <span class="menu-icon">
                      <i class="bi bi-bag-check-fill fs-2x"></i>
                    </span>
                    <span class="menu-title">My Projects</span>
                  </span>
                </router-link> -->
                <div
                  class="vue-flow__node-input"
                  :draggable="true"
                  @dragstart="(event: DragEvent) => onDragStart(event, 'input')"
                >
                  Input Node
                </div>
                <div
                  class="vue-flow__node-default"
                  :draggable="true"
                  @dragstart="(event: DragEvent) => onDragStart(event, 'default')"
                >
                  Default Node
                </div>
                <div
                  class="vue-flow__node-output"
                  :draggable="true"
                  @dragstart="(event: DragEvent) => onDragStart(event, 'output')"
                >
                  Output Node
                </div>
              </div>
            </Teleport>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, reactive } from "vue";
// import {
//   VueFlow,
//   Background,
//   MiniMap,
//   Controls,
//   Elements,
//   FlowEvents,
//   FlowInstance,
//   isNode,
//   addEdge,
// } from "@braks/vue-flow";
import { inject } from "vue";
// import { setCurrentPageTitle } from "@core/helpers/breadcrumb";
import { Vue3LiveForm } from "vue3-live-form";
import FilterTimeline from "../../components/filters/FilterTimeline.vue";
import test_data from "../../assets/data/generators/test/defaults.json";
import test_schema from "../../assets/data/generators/test/schema.json";
import AsideDefaultMenu from "@/components/widgets/menus/AsideDefaultMenu.vue";
import ApiService from "@/core/services/ApiService";
import { AxiosResponse, AxiosRequestConfig } from "axios";
import { useRoute } from "vue-router";
import {
  VueFlow,
  MiniMap,
  Controls,
  Background,
  isNode,
  useVueFlow,
  Elements,
  Node,
  addEdge,
  FlowInstance,
  FlowElements,
  FlowEvents,
} from "@braks/vue-flow";

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
    //const a$roxios: any = inject("axios"); // inject axios

    const state = reactive({
      count: 0,
      mounted: false,
      project: null,
    });
    const schema = test_schema; // = reactive (news_schema);
    const model = test_data; // = reactive ({});

    //console.log(schema);

    const {
      onPaneReady,
      onNodeDragStop,
      onNodeDragStart,
      instance,
      addEdges,
      addNodes,
    } = useVueFlow({
      defaultZoom: 1.5,
      minZoom: 0.2,
      maxZoom: 4,
    });

    let id = 0;
    const getId = () => `dndnode_${id++}`;

    return {
      // status,
      // currentStatus,
      state,
      schema,
      model,

      instance: null as FlowInstance | null,
      onNodeDragStop,
      onNodeDragStart,
      getId,
      addNodes,
      addEdges,
    };
  },

  mounted() {
    // setCurrentPageTitle("Studio");
    this.state.mounted = true;
    const route = useRoute();

    this.getProject(route.params.id);
  },

  methods: {
    getProject(id) {
      ApiService.post("http://localhost:5000/api/project/" + id.toString(), {})
        .then(({ data }) => {
          this.state.project = data;

          // (this.state.project as any).chain = [
          //   { id: "1", type: "input", label: "Grid-3-ML", position: { x: 250, y: 5 } },
          //   { id: "2", label: "Superres", position: { x: 100, y: 100 } },
          //   { id: "3", label: "Disco Diffusion", position: { x: 400, y: 100 } },
          //   { id: "4", label: "Superres", position: { x: 400, y: 200 } },
          //   { id: "e1-2", source: "1", target: "2", animated: true },
          //   { id: "e1-3", source: "1", target: "3" },
          //   { id: "e1-3", source: "3", target: "4" },
          //   // { id: "e1-4", source: "4", target: "5" },
          // ] as Elements;
          console.log(data);
          //console.log(this.state.project);
          // if (this.state.project !=null){
          //let p = (this.state.project as any);
          //p.title = "New Project";

          // }

          // this.getProjects();
        })
        .catch(({ response }) => {});
    },
    saveProject() {
      console.log("save");
      (this.state.project as any).chain = (this.instance as any).toObject();
      ApiService.post(
        "http://localhost:5000/api/project/save/" +
          (this.state.project as any).id.toString(),
        this.state.project as any
      )
        .then(({ data }) => {
          console.log("saved");
        })
        .catch(({ response }) => {});
    },
    deleteProject(id) {
      console.log("delete");
      ApiService.delete("http://localhost:5000/api/project/" + id.toString())
        .then(({ data }) => {
          //this.state.projects = data;
          // this.getProjects();
        })
        .catch(({ response }) => {});
    },

    onDragStart(event: DragEvent, nodeType: string) {
      if (event.dataTransfer) {
        event.dataTransfer.setData("application/vueflow", nodeType);
        event.dataTransfer.effectAllowed = "move";
      }
    },
    onDragOver(event: DragEvent) {
      event.preventDefault();
      if (event.dataTransfer) {
        event.dataTransfer.dropEffect = "move";
      }
    },
    onPaneReady(instance: FlowEvents["paneReady"]) {
      //instance.fitView();
      this.instance = instance;
    },
    onConnect(params: FlowEvents["connect"]) {
      console.log('on connect', params)
      this.addEdges([params]);//, (this.state.project as any).chain);
    },
    onDrop(event: DragEvent) {
      console.log("dropped", event);
      if (this.instance as any) {
        console.log("dropped2", event);
        const type = event.dataTransfer?.getData("application/vueflow");
        const position = (this.instance as any).project({
          x: event.clientX - 240,
          y: event.clientY - 280,
        });
        const newNode = {
          id: this.getId(),
          type,
          position,
          label: `${type} node`,
        } as Node;
        this.addNodes([newNode]);
      }
    },
  },
  // watch: {},
});
</script>
