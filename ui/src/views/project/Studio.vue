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
                    <button class="btn btn-primary" @click="startProject()">Run</button
                    >&nbsp;&nbsp;&nbsp;
                    <button class="btn btn-primary" @click="saveProject()">Save</button
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
                  <span class="mx-3"
                    ><span v-if="state.busy"
                      >Running {{ state.progressPercentage }}&nbsp;
                      <div style="display: inline-block">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          xmlns:xlink="http://www.w3.org/1999/xlink"
                          style="
                            margin: auto;
                            background: transparen;
                            width: 36px;
                            display: inline-block;
                            margin-top: -3px;
                          "
                          width="200px"
                          height="200px"
                          viewBox="0 0 100 100"
                          preserveAspectRatio="xMidYMid"
                        >
                          <circle
                            cx="50"
                            cy="50"
                            r="0"
                            fill="none"
                            stroke="#03d8ae"
                            stroke-width="12"
                          >
                            <animate
                              attributeName="r"
                              repeatCount="indefinite"
                              dur="2.4390243902439024s"
                              values="0;40"
                              keyTimes="0;1"
                              keySplines="0 0.2 0.8 1"
                              calcMode="spline"
                              begin="0s"
                            ></animate>
                            <animate
                              attributeName="opacity"
                              repeatCount="indefinite"
                              dur="2.4390243902439024s"
                              values="1;0"
                              keyTimes="0;1"
                              keySplines="0.2 0 0.8 1"
                              calcMode="spline"
                              begin="0s"
                            ></animate>
                          </circle>
                          <circle
                            cx="50"
                            cy="50"
                            r="0"
                            fill="none"
                            stroke="#03d8ae"
                            stroke-width="12"
                          >
                            <animate
                              attributeName="r"
                              repeatCount="indefinite"
                              dur="2.4390243902439024s"
                              values="0;40"
                              keyTimes="0;1"
                              keySplines="0 0.2 0.8 1"
                              calcMode="spline"
                              begin="-1.2195121951219512s"
                            ></animate>
                            <animate
                              attributeName="opacity"
                              repeatCount="indefinite"
                              dur="2.4390243902439024s"
                              values="1;0"
                              keyTimes="0;1"
                              keySplines="0.2 0 0.8 1"
                              calcMode="spline"
                              begin="-1.2195121951219512s"
                            ></animate>
                          </circle>
                        </svg></div></span
                    ><span v-if="!state.busy">Idle</span></span
                  >
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
                    href="#kt_animation_tab_content"
                    @click="delayLoadAnimation()"
                  >
                    Animation
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
                    <br />
                    <div class="flex" v-if="state.project != null">
                      <div
                        v-if="state.project.generators.length == 0"
                        style="color: #fff"
                      >
                        Add some generators into this project chain to get started.
                        <br />
                        <br />
                      </div>

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
                    </div>

                    <br />
                    <br />
                    <br />

                    <div v-if="state.project && state.project.generators.length > 0">
                      <h2 style="color: #fff">Preview</h2>

                      <div
                        v-for="element in state.project.generators"
                        :key="element.title"
                      >
                        <div
                          v-if="element.type == 2 && state.busy"
                          class="card-generator"
                          style="margin: 15px 0 0 0; display: inline-block; width: 100%"
                        >
                          <img
                            style="width: 100%"
                            v-bind:src="apiUrl + '/output/progress.png'"
                            alt=""
                          />
                        </div>
                        <div
                          v-if="element.output_path?.length > 0"
                          class="card-generator"
                          style="margin: 15px 0 0 0; display: inline-block; width: 100%"
                        >
                          <img
                            style="width: 100%"
                            v-bind:src="apiUrl + '/' + element.output_path"
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
                        <div
                          v-if="
                            state.selectedGenerator.type != 21 && state.loading == false
                          "
                        >
                          <Vue3LiveForm
                            :schema="state.selectedGenerator.schema"
                            v-model="state.selectedGenerator.settings"
                          />
                        </div>
                        <div
                          v-if="state.selectedGenerator.type == 2"
                          style="padding: 15px"
                        >
                          <h3>Scene Tools</h3>
                          <p>
                            Create scene items from a list of text lines (e.g.
                            poem/lyrics).
                          </p>
                          <div class="form-group">
                            <textarea
                              type="text"
                              class="form-control"
                              name="Lines"
                              placeholder="Lines..."
                              v-model="state.sceneLines"
                              style="color: white; border: 1px solid #555"
                            />
                          </div>
                          <br />
                          <div class="form-group">
                            <div class="form-label">
                              Frames per Scene
                              <input
                                type="text"
                                class="form-control"
                                name="FramePerScene"
                                placeholder="10"
                                v-model="state.sceneLinesFramesPerScene"
                                style="color: white; border: 1px solid #555"
                              />
                            </div>
                          </div>
                          <br />

                          <button
                            class="btn btn-primary btn-sm"
                            @click="createScenesFromLines()"
                          >
                            Create Scenes
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div
                id="kt_animation_tab_content"
                class="py-0 tab-pane fade show"
                role="tabpanel"
              >
                <div>
                  <!-- <SearchResults :componentState="componentState" ref="searchResults"></SearchResults> -->
                  <KeyFrameEditor
                    :project="state.project"
                    :generator="generator_disco"
                    v-if="state.project"
                    ref="keyframeEditor"
                  />
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
                    <p style="color: #fff">
                      Currently:
                      <span v-if="state.busy">Running {{ state.progressPercentage }}</span
                      ><span v-if="!state.busy">Idle</span>
                    </p>
                    <br />
                    <h3 style="color: #fff">Output</h3>
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
                    <br />
                    <br />
                    <br />
                    <div v-if="state.project">
                      <h2 style="color: #fff">CLI</h2>
                      <p style="color: #fff">
                        To run from shell:
                        <br /><span>python cli.py --project {{ state.project.id }}</span>
                      </p>
                    </div>
                    <div v-if="state.project">
                      <h2 style="color: #fff">Delete Project</h2>
                      <p style="color: #fff">
                        If you're sure you want to delete the project you can do so below.
                        <br />
                        <button id="btn btn-primary" @click="deleteProject()">
                          Delete Project
                        </button>
                      </p>
                    </div>
                  </div>
                  <div class="col-6" v-if="state.project">
                    <h2 style="color: #fff">Output</h2>

                    <div v-for="element in state.project.generators" :key="element.title">
                      <div
                        v-if="element.type == 2 && state.busy"
                        class="card-generator"
                        style="margin: 15px 0 0 0; display: inline-block"
                      >
                        <img v-bind:src="apiUrl + '/output/progress.png'" alt="" />
                      </div>
                      <div
                        v-if="element.output_path?.length > 0"
                        class="card-generator"
                        style="margin: 15px 0 0 0; display: inline-block"
                      >
                        <img v-bind:src="apiUrl + '/' + element.output_path" alt="" />
                      </div>
                      <div
                        v-if="element.output_path == null"
                        class="card-generator"
                        style="margin: 15px 0 0 0; color: #fff"
                      >
                        No preview available.
                      </div>
                    </div>

                    <br />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="state.mounted">
    <Teleport to="#aside-context">
      <div
        class="menu-item menu-accordion"
        data-kt-menu-sub="accordion"
        data-kt-menu-trigger="click"
      >
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">Projects</span>
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
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">Generators</span>
        </div>
        <div
          class="card-generator"
          v-for="element in state.generators"
          :key="element.title"
        >
          <h3>
            <div style="float: right">
              <button class="btn btn-primary btn-sm" @click="addGenerator(element)">
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
</template>

<script lang="ts">
import * as THREE from "three";
import { TWEEN } from "three/examples/jsm/libs/tween.module.min";

import { defineComponent, onMounted, ref, reactive } from "vue";
import Flow from "../../views/project/flow/Flow.vue";
import { inject } from "vue";
import { Vue3LiveForm } from "vue3-live-form";
import FilterTimeline from "../../components/filters/FilterTimeline.vue";
import AsideDefaultMenu from "@/components/widgets/menus/AsideDefaultMenu.vue";
import KeyFrameEditor from "@/views/project/animation/KeyFrameEditor.vue";
import ApiService from "@/core/services/ApiService";
import { AxiosResponse, AxiosRequestConfig } from "axios";
import { useRoute } from "vue-router";

export default defineComponent({
  name: "studio",

  components: {
    KeyFrameEditor,
    AsideDefaultMenu,
    Vue3LiveForm,
    Flow,
  },

  setup() {
    // const renderer:any = ref(null);
    // const box:any = ref(null);
    const keyframeEditor: any = ref(null);

    // const box: any = null;
    const timer: any = null;
    let apiUrl = "http://localhost:5000";

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
      {
        type: 3,
        title: "DALLE2 Pytorch",
        description: "Open DALLE2 + Extras",
        folder: "dalle2_pytorch",
      },
      {
        type: 4,
        title: "Upscale",
        description: "BigJpg Upscaler API",
        folder: "go_big",
      },
    ];
    const generator_disco = null;
    const state = reactive({
      count: 0,
      mounted: false,
      project: null,
      list: [],
      generators: generator_options,
      selectedGenerator: null,
      busy: false,
      loading: false,
      output: "",
      progress: 0,
      progressPercentage: "",
      autoUpdate: true,
      preloadFrame: 0,
      selectedFrame: 0,
      autoPlay: false,
      sceneLines: "",
      sceneLinesFramesPerScene: 10,
      // renderer,
      // box
    });
    return {
      state,
      timer,
      enabled: true,
      dragging: false,
      apiUrl,

      keyframeEditor,
      generator_disco,
      // frameTimelineSlider,
    };
  },

  mounted() {
    // setCurrentPageTitle("Studio");

    console.log(location.host);
    if (location.host.indexOf("localhost") > -1) {
      this.apiUrl = "http://localhost:5000";
    } else {
      this.apiUrl = "";
    }

    this.state.mounted = true;
    const route = useRoute();

    if (this.state.autoUpdate) {
      this.timer = setInterval(this.updateStatus, 1000);
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
      g.enabled = true;

      fetch(this.apiUrl + "/data/generators/" + g.folder + "/schema.json")
        .then((res) => res.json())
        .then((res) => {
          g.schema = res;
          console.log(res);
        });

      fetch(this.apiUrl + "/data/generators/" + g.folder + "/defaults.json")
        .then((res) => res.json())
        .then((res) => {
          g.settings = res;
          console.log(res);
        });

      // g.model = JSON.parse(
      //   import("/generators/" + g.folder + "/defaults.json").then(
      //     ({ prop: data }) => data

      //   );

      (this.state.project as any).generators.push(g);

      this.keyframeEditor.updateView();
      // this.updateView();
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
      ApiService.post(this.apiUrl + "/api/task/update", {})
        .then(({ data }) => {
          console.log(data);
          this.state.output = data["output"];
          this.state.progress = data["progress"];
          this.state.busy = data["busy"];
          this.state.progressPercentage = Math.round(this.state.progress * 100) + "%";
          // this.state.status = data.length > 0 ? "Running" : "Idle"; // if ("_False" in data) else "Running";
        })
        .catch(({ response }) => {});
    },
    cancelAutoUpdate() {
      clearInterval(this.timer);
    },

    delayLoadAnimation() {
      setTimeout(() => {
        this.keyframeEditor.updateView();
      }, 1000);
    },

    startProject() {
      ApiService.post(
        this.apiUrl + "/api/project/save/" + (this.state.project as any).id.toString(),
        this.state.project as any
      )
        .then(({ data }) => {
          ApiService.post(
            this.apiUrl + "/api/task/start/" + (this.state.project as any).id.toString(),
            {}
          )
            .then(({ data }) => {
              console.log(data);
              this.getProject((this.state.project as any).id);
            })
            .catch(({ response }) => {});
        })
        .catch(({ response }) => {});
    },
    getProject(id) {
      ApiService.post(this.apiUrl + "/api/project/" + id.toString(), {})
        .then(({ data }) => {
          this.state.project = data;
          //(this.state.project as any).chain = data.chain.nodes;
          console.log(data);

          this.generator_disco = (this.state.project as any).generators.find(
            (x) => x.type == 2
          );

          this.keyframeEditor.updateView();
          //this.updateView();
          // const renderer = this.$refs.renderer;
          // const box = (this.$refs.box as any).mesh;
          // // const renderer: any = ref());
          // // const box: any = ref(null);
          // console.log(renderer, box);
          // (renderer as any).onBeforeRender(() => {
          //   box.rotation.x += 0.01;
          // });
        })
        .catch(({ response }) => {});
    },
    saveProject() {
      console.log(this.apiUrl);
      ApiService.post(
        this.apiUrl + "/api/project/save/" + (this.state.project as any).id.toString(),
        this.state.project as any
      )
        .then(({ data }) => {
          console.log("saved");
        })
        .catch(({ response }) => {});
    },
    refreshProject() {
      console.log(this.apiUrl);
      ApiService.post(
        this.apiUrl + "/api/project/save/" + (this.state.project as any).id.toString(),
        this.state.project as any
      )
        .then(({ data }) => {
          this.getProject((this.state.project as any).id);
        })
        .catch(({ response }) => {});
    },
    deleteProject(id) {
      console.log("delete");
      ApiService.delete(this.apiUrl + "/api/project/" + id.toString())
        .then(({ data }) => {
          //this.state.projects = data;
          // this.getProjects();
        })
        .catch(({ response }) => {});
    },

    createScenesFromLines() {
      this.state.loading = true;
      let lines = this.state.sceneLines.split("\n");
      let text_prompts: any[] = [];
      for (let i = 0; i < lines.length; i++) {
        text_prompts.push({
          start: i * this.state.sceneLinesFramesPerScene,
          prompt: lines[i],
        });
      }
      this.state.loading = false;

      let g: any = this.state.selectedGenerator;
      g.settings.text_prompts = text_prompts;
      g.settings.max_frames = lines.length * this.state.sceneLinesFramesPerScene;
      ApiService.post(
        this.apiUrl + "/api/project/save/" + (this.state.project as any).id.toString(),
        this.state.project as any
      )
        .then(({ data }) => {
          location.reload();
        })
        .catch(({ response }) => {});
    },
  },
  // watch: {},
});
</script>
