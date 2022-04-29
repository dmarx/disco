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

              <div class="d-flex flex-column" style="width: 100%" v-if="state.project">
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
                      border: 1px solid #555;
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
                class="nav nav-stretch fs-5 fw-bold nav-line-tabs nav-line-tabs-2x border-transparent"
                role="tablist"
              >
                <li class="nav-item" role="presentation">
                  <a
                    class="nav-link text-active-primary active"
                    data-bs-toggle="tab"
                    role="tab"
                    href="#kt_scenes_tab_content"
                  >
                    Scenes
                  </a>
                </li>

                <li class="nav-item" role="presentation">
                  <a
                    class="nav-link text-active-primary ms-3"
                    data-bs-toggle="tab"
                    role="tab"
                    href="#kt_process_tab_content"
                  >
                    Process
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="card card-flush">
          <!-- <div class="card-header pt-8" style="">
            <div class="card-title">
              <h2>Generator Chain</h2>
            </div>
          </div> -->

          <div class="card-body" style="">
            <div id="kt_scenes_tab_contents" class="tab-content">
              <div
                id="kt_scenes_tab_content"
                class="py-0 tab-pane fade active show"
                role="tabpanel"
              >
                <div class="row">
                  <div class="col-6">
                    <h2 style="color: #fff">Generator Chain</h2>

                    <div class="flex" v-if="state.project != null">
                      <draggable
                        class="dragArea list-group w-full"
                        :list="state.project.generators"
                        @change="log"
                      >
                        <div
                          class="bg-gray-300 m-1 p-3 rounded-md text-center item-generator"
                          v-for="element in state.project.generators"
                          :key="element.title"
                        >
                          <h3>
                            <div style="float: right">
                              <button
                                class="btn btn-primary btn-sm"
                                @click="selectGenerator(element)"
                              >
                                Edit
                              </button>
                            </div>
                            {{ element.title }}
                          </h3>
                          <p>{{ element.description }}</p>
                        </div>
                      </draggable>
                    </div>
                  </div>
                  <div class="col-6">
                    <div v-if="state.selectedGenerator != null">
                      <h2 style="color: #fff; line-height: 36px">
                        <div style="float: right">
                          <button
                            class="btn btn-primary btn-sm"
                            @click="deleteGenerator(state.selectedGenerator)"
                          >
                            Delete
                          </button>
                        </div>
                        Settings
                      </h2>
                      <div class="item-generator">
                        <Vue3LiveForm
                          :schema="state.selectedGenerator.schema"
                          v-model="state.selectedGenerator.model"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div
                id="kt_process_tab_content"
                class="py-0 tab-pane fade show"
                role="tabpanel"
              >
                <div class="row">
                  <div class="col-6">
                    <h2 style="color: #fff">Status</h2>
                    <p style="color: #fff">Currently: {{ state.status }}</p>
                    <div style="color: #fff" v-html="state.output"></div>
                    <br />
                    <p>
                      <button class="btn btn-primary btn-sm" @click="startProject()">
                        Run</button
                      >&nbsp;&nbsp;&nbsp;<button
                        class="btn btn-primary btn-sm"
                        @click="updateStatus()"
                      >
                        Update
                      </button>
                    </p>
                  </div>
                  <div class="col-6" v-if="state.project">
                    <h2 style="color: #fff">Output</h2>

                    <div v-for="element in state.project.generators" :key="element.title">
                      <div
                        v-if="element.output_path?.length > 0"
                        class="card-generator"
                        style="margin: 15px 0 0 0; display: inline-block"
                      >
                        <img
                          v-bind:src="'http://localhost:5000/' + element.output_path"
                          alt=""
                        />
                      </div>
                      <div
                        v-if="element.output_path == null"
                        class="card-generator"
                        style="margin: 15px 0 0 0; color: #fff"
                      >
                        No preview available.
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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
                <div
                  class="card-generator"
                  v-for="element in state.generators"
                  :key="element.title"
                >
                  <h3>
                    <div style="float: right">
                      <button
                        class="btn btn-primary btn-sm"
                        @click="addGenerator(element)"
                      >
                        Add
                      </button>
                    </div>
                    {{ element.title }}
                  </h3>
                  <p>{{ element.description }}</p>
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
import Flow from "../../views/project/flow/Flow.vue";
import { inject } from "vue";
import { Vue3LiveForm } from "vue3-live-form";
import FilterTimeline from "../../components/filters/FilterTimeline.vue";
import AsideDefaultMenu from "@/components/widgets/menus/AsideDefaultMenu.vue";
import ApiService from "@/core/services/ApiService";
import { AxiosResponse, AxiosRequestConfig } from "axios";
import { useRoute } from "vue-router";
import { VueDraggableNext } from "vue-draggable-next";

export default defineComponent({
  name: "studio",

  components: {
    FilterTimeline,
    AsideDefaultMenu,
    Vue3LiveForm,
    draggable: VueDraggableNext,
    Flow,
  },

  setup() {
    const timer: any = null;

    const generator_options = [
      {
        type: 1,
        title: "Glid-3-ML",
        description: "Latent diffusion model",
        folder: "latent_diffusion",
      },
      {
        type: 2,
        title: "Disco Diffusion",
        description: "Disco diffusion network",
        folder: "disco_diffusion",
      },
    ];
    const state = reactive({
      count: 0,
      mounted: false,
      project: null,
      list: [],
      generators: generator_options,
      selectedGenerator: null,
      status: "Idle",
      output: "",
      autoUpdate: false,
    });

    return {
      state,

      timer,
      enabled: true,
      dragging: false,
    };
  },

  mounted() {
    // setCurrentPageTitle("Studio");
    this.state.mounted = true;
    const route = useRoute();

    if (this.state.autoUpdate) {
      this.timer = setInterval(this.updateStatus, 5000);
    }

    this.getProject(route.params.id);
  },
  beforeDestroy() {
    this.cancelAutoUpdate();
  },
  methods: {
    deleteGenerator(generator) {
      this.state.selectedGenerator = null;
      (this.state.project as any).generators = (this.state
        .project as any).generators.filter((x) => x.id != generator.id);
      console.log(this.state.selectedGenerator);
    },
    selectGenerator(generator) {
      this.state.selectedGenerator = generator;
      console.log(this.state.selectedGenerator);
    },

    addGenerator(generator) {
      var fs = require("fs");
      //http://172.29.230.209:8080/generators/latent_diffusion/schema.json
      const g: any = Object.assign({}, generator);
      g.id = (this.state.project as any).generators.length;

      fetch("/generators/" + g.folder + "/schema.json")
        .then((res) => res.json())
        .then((res) => {
          g.schema = res;
        });

      fetch("/generators/" + g.folder + "/defaults.json")
        .then((res) => res.json())
        .then((res) => {
          g.model = res;
        });

      // g.model = JSON.parse(
      //   import("/generators/" + g.folder + "/defaults.json").then(
      //     ({ prop: data }) => data

      //   );

      (this.state.project as any).generators.push(g);
    },

    log(event) {
      console.log(event);
      this.array_move(this.state.list, event.oldIndex, event.newIndex);
      console.log(this.state.list);
    },

    array_move(arr, old_index, new_index) {
      if (new_index >= arr.length) {
        var k = new_index - arr.length + 1;
        while (k--) {
          arr.push(undefined);
        }
      }
      arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
      return arr; // for testing
    },

    updateStatus() {
      ApiService.post("http://localhost:5000/api/task/update", {})
        .then(({ data }) => {
          console.log(data);
          this.state.output = data;
          this.state.status = data.length > 0 ? "Running" : "Idle"; // if ("_False" in data) else "Running";
        })
        .catch(({ response }) => {});
    },
    cancelAutoUpdate() {
      clearInterval(this.timer);
    },

    startProject() {
      ApiService.post(
        "http://localhost:5000/api/task/start/" +
          (this.state.project as any).id.toString(),
        {}
      )
        .then(({ data }) => {
          console.log(data);
          this.getProject((this.state.project as any).id);
        })
        .catch(({ response }) => {});
    },
    getProject(id) {
      ApiService.post("http://localhost:5000/api/project/" + id.toString(), {})
        .then(({ data }) => {
          this.state.project = data;
          //(this.state.project as any).chain = data.chain.nodes;
          console.log(data);
        })
        .catch(({ response }) => {});
    },
    saveProject() {
      console.log("save");
      // (this.state.project as any).chain = (this.instance as any).toObject();
      // console.log((this.instance as any).toObject());
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
  },
  // watch: {},
});
</script>
