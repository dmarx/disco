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
                    ><span v-if="state.busy">Running {{ state.progressPercentage }}</span
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
                      <div
                        v-if="state.project.generators.length == 0"
                        style="color: #fff"
                      >
                        <br />
                        Add some generators into this project chain to get started.
                        <br />
                        <br />
                      </div>
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
                        <Vue3LiveForm
                          :schema="state.selectedGenerator.schema"
                          v-model="state.selectedGenerator.settings"
                        />
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
                  <div v-if="!generator_disco" style="color: #fff">
                    <h3>Animation Tools</h3>
                    Only visible when a Disco generator is in the chain.
                  </div>
                  <div v-show="generator_disco != null">
                    <div
                      class="bg-gray-300 m-1 p-3 rounded-md text-center item-generator"
                    >
                      <h3
                        style="
                          padding: 10px;
                          padding-bottom: 25px;
                          line-height: 30px;
                          margin-bottom: 16px;
                        "
                      >
                        <div style="float: right; white-space: nowrap">
                          <span
                            v-if="generator_disco && generator_disco.settings"
                            style="
                              display: inline-block;
                              display: inline-block;
                              margin-right: 60px;
                            "
                            >Mode:&nbsp;
                            <select
                              v-model="generator_disco.settings['animation_mode']"
                              class="form-control"
                              style="
                                background: #222;
                                border: 1px solid #555;
                                display: inline-block;
                                color: #fff;
                              "
                            >
                              <option disabled value="">Select animation mode...</option>
                              <option>None</option>
                              <option>2D</option>
                              <option>3D</option>
                              <option>Video</option>
                            </select>
                          </span>

                          &nbsp;&nbsp;&nbsp;
                          <button class="btn btn-primary btn-sm" @click="previewFrame()">
                            Preview
                          </button>
                        </div>
                        Animation Tools
                      </h3>

                      <div style="width: 100%">
                        <label
                          style="
                            color: #fff;
                            width: 100%;
                            text-align: center;
                            color: #999;
                          "
                        >
                          Frame Timeline:
                          <span id="sliderDisplayValue">0</span>
                        </label>
                        <fieldset style="width: 100%">
                          <label id="slider-container" style="width: 100%">
                            <input
                              style="width: 100%; display: block"
                              ref="frameTimelineSlider"
                              id="frameTimelineSlider"
                              type="range"
                              min="0"
                              max="100"
                              value="0"
                              step="1"
                            />
                          </label>
                        </fieldset>
                      </div>
                    </div>

                    <div style="position: relative" class="threejs" id="threejs">
                      <div style="width: 100%; height: 600px; position: relative">
                        <Renderer ref="renderer" style="width: 100%; height: 600px">
                          <Camera ref="camera" :fov="70" :near="1" :far="10000" />
                          <Scene ref="scene"> </Scene>
                        </Renderer>
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
import * as THREE from "three";

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

import { GUI } from "three/examples/jsm/libs/lil-gui.module.min.js";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { TransformControls } from "three/examples/jsm/controls/TransformControls";
import {
  AmbientLight,
  Scene,
  SpotLight,
  Mesh,
  BufferAttribute,
  BufferGeometry,
  Line,
  CatmullRomCurve3,
  LineBasicMaterial,
  MeshLambertMaterial,
  Vector3,
  Camera,
  Renderer,
  GridHelper,
  ShadowMaterial,
  PlaneGeometry,
} from "three";
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
    // const renderer:any = ref(null);
    // const box:any = ref(null);

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
        title: "Upscale",
        description: "BigJpg Upscaler API",
        folder: "go_big",
      },
    ];
    const state = reactive({
      count: 0,
      mounted: false,
      project: null,
      list: [],
      generators: generator_options,
      selectedGenerator: null,
      busy: false,
      output: "",
      progress: 0,
      progressPercentage: "",
      autoUpdate: true,
      selectedFrame: 0,
      // renderer,
      // box
    });

    // const frameTimelineSlider = ref();

    const generator_disco = null;

    const renderer: any = null;
    const camera: any = null;

    const splineHelperObjects: any[] = [];
    let splinePointsLength = 4;
    const positions: any[] = [];
    const point = new THREE.Vector3();

    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    const onUpPosition = new THREE.Vector2();
    const onDownPosition = new THREE.Vector2();

    const geometry = new THREE.BoxGeometry(5, 5, 5);
    let transformControl;

    const previewMaterial: any = null;
    const previewImage: any = null;

    const ARC_SEGMENTS = 200;

    const splines = {};

    const params = {
      uniform: true,
      tension: 0.5,
      centripetal: true,
      chordal: true,
      addPoint: null,
      removePoint: null,
      exportSpline: null,
    };

    return {
      state,
      generator_disco,

      timer,
      enabled: true,
      dragging: false,
      apiUrl,

      // frameTimelineSlider,

      transformControl,
      splineHelperObjects,
      raycaster,
      pointer,
      onUpPosition,
      onDownPosition,
      splines,
      params,
      positions,
      splinePointsLength,
      point,
      ARC_SEGMENTS,
      geometry,
      renderer,
      camera,
      previewMaterial,  
      previewImage
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
      this.timer = setInterval(this.updateStatus, 5000);
    }

    this.getProject(route.params.id);
  },
  beforeDestroy() {
    this.cancelAutoUpdate();
  },
  methods: {
    updateTimeframe() {
      let frameTimelineSlider = this.$refs.frameTimelineSlider as any;

      this.state.selectedFrame = frameTimelineSlider.value;
    },

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
          console.log(res);
        });

      fetch("/generators/" + g.folder + "/defaults.json")
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

      this.updateView();
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

          this.updateView();
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
    deleteProject(id) {
      console.log("delete");
      ApiService.delete(this.apiUrl + "/api/project/" + id.toString())
        .then(({ data }) => {
          //this.state.projects = data;
          // this.getProjects();
        })
        .catch(({ response }) => {});
    },

    updateView() {
      this.generator_disco = (this.state.project as any).generators.find(
        (x) => x.type == 2
      );
      if (this.generator_disco) {
        let frameTimelineSlider = this.$refs.frameTimelineSlider as any;
        frameTimelineSlider.addEventListener("input", () => {
          const sliderValue = frameTimelineSlider.value;
          document.getElementById("sliderDisplayValue")!.innerHTML = ` ${sliderValue}`;
        });
        // does all filtering once slider has changed and been released
        frameTimelineSlider!.addEventListener("change", () => {
          this.state.selectedFrame = frameTimelineSlider.value;
          this.updateTimeframe();
        });
        frameTimelineSlider.addEventListener("mouseup", () => {
          if (this.state.selectedFrame !== frameTimelineSlider.value) {
            this.state.selectedFrame = frameTimelineSlider.value;
            this.updateTimeframe();
          }
        });

        (this.params as any).addPoint = () => {
          this.addPoint();
        };
        (this.params as any).removePoint = () => {
          this.removePoint();
        };
        (this.params as any).exportSpline = () => {
          this.exportSpline();
        };

        console.log("window", window.innerWidth, window.innerHeight);
        this.initScene();
      }
    },
    initScene() {
      // camera = new PerspectiveCamera(
      //   70,
      //   window.innerWidth / window.innerHeight,
      //   1,
      //   10000
      // );
      // camera.position.set(0, 250, 1000);
      // scene.add(camera);

      let scene: Scene = (this.$refs.scene as Scene).scene;

      scene.add(new AmbientLight(0xf0f0f0));
      const light = new SpotLight(0xffffff, 1.5);
      light.position.set(0, 250, 100);
      light.angle = Math.PI * 0.2;
      light.castShadow = true;
      light.shadow.camera.near = 200;
      light.shadow.camera.far = 2000;
      light.shadow.bias = -0.000222;
      light.shadow.mapSize.width = 1024;
      light.shadow.mapSize.height = 1024;
      scene.add(light);

      const planeGeometry = new PlaneGeometry(2000, 2000);
      planeGeometry.rotateX(-Math.PI / 2);
      const planeMaterial = new ShadowMaterial({ color: 0x000000, opacity: 0.2 });

      // const plane = new Mesh(planeGeometry, planeMaterial);
      // plane.position.y = -200;
      // plane.receiveShadow = true;
      // scene.add(plane);

      const helper = new GridHelper(2000, 100);
      helper.position.y = -199;
      helper.material.opacity = 0.25;
      helper.material.transparent = true;
      scene.add(helper);

      this.camera = (this.$refs.camera as Camera).camera;
      this.renderer = (this.$refs.renderer as Renderer).renderer;
      this.camera.position.set(0, 25, 100);

      // renderer = new WebGLRenderer({ antialias: true });
      this.renderer.setPixelRatio(window.devicePixelRatio);
      //renderer.setSize(window.innerWidth, window.innerHeight);
      this.renderer.shadowMap.enabled = true;
      // container.appendChild(renderer.domElement);

      const gui = new GUI({
        container: document.getElementById("threejs"),
      });

      gui.add(this.params, "uniform").onChange(() => {
        this.render();
      });
      gui
        .add(this.params, "tension", 0, 1)
        .step(0.01)
        .onChange((value) => {
          (this.splines as any).uniform.tension = value;
          this.updateSplineOutline();
          this.render();
        });
      gui.add(this.params, "centripetal").onChange(() => {
        this.render();
      });
      gui.add(this.params, "chordal").onChange(() => {
        this.render();
      });
      console.log(1231);
      gui.add(this.params, "addPoint");
      gui.add(this.params, "removePoint");
      gui.add(this.params, "exportSpline");
      gui.open();

      console.log(123);

      // Controls
      // console.log("asdasd",(this.$refs.renderer as Renderer).renderer.domElement);
      const controls = new OrbitControls(this.camera, this.renderer.domElement);
      controls.damping = 0.2;
      controls.addEventListener("change", () => {
        this.render();
      });

      this.transformControl = new TransformControls(
        this.camera,
        this.renderer.domElement
      );
      this.transformControl.addEventListener("change", () => {
        this.render();
      });
      this.transformControl.addEventListener("dragging-changed", (event) => {
        controls.enabled = !event.value;
      });
      scene.add(this.transformControl);

      this.transformControl.addEventListener("objectChange", () => {
        this.updateSplineOutline();
      });

      document.addEventListener("pointerdown", (e) => {
        this.onPointerDown(e);
      });
      document.addEventListener("pointerup", () => {
        this.onPointerUp();
      });
      document.addEventListener("pointermove", (e) => {
        this.onPointerMove(e);
      });
      window.addEventListener("resize", () => {
        this.onWindowResize();
      });

      /*******
       * Curves
       *********/

      for (let i = 0; i < this.splinePointsLength; i++) {
        this.addSplineObject(this.positions[i]);
      }

      this.positions.length = 0;

      for (let i = 0; i < this.splinePointsLength; i++) {
        this.positions.push((this.splineHelperObjects[i] as any).position);
      }

      this.geometry = new BufferGeometry();
      this.geometry.setAttribute(
        "position",
        new BufferAttribute(new Float32Array(this.ARC_SEGMENTS * 3), 3)
      );

      let curve = new CatmullRomCurve3(this.positions);
      curve.curveType = "catmullrom";
      curve.mesh = new Line(
        this.geometry.clone(),
        new LineBasicMaterial({
          color: 0xff0000,
          opacity: 0.35,
        })
      );
      curve.mesh.castShadow = true;
      (this.splines as any).uniform = curve;

      curve = new CatmullRomCurve3(this.positions);
      curve.curveType = "centripetal";
      curve.mesh = new Line(
        this.geometry.clone(),
        new LineBasicMaterial({
          color: 0x00ff00,
          opacity: 0.35,
        })
      );
      curve.mesh.castShadow = true;
      (this.splines as any).centripetal = curve;

      curve = new CatmullRomCurve3(this.positions);
      curve.curveType = "chordal";
      curve.mesh = new Line(
        this.geometry.clone(),
        new LineBasicMaterial({
          color: 0x0000ff,
          opacity: 0.35,
        })
      );
      curve.mesh.castShadow = true;
      (this.splines as any).chordal = curve;

      for (const k in this.splines) {
        const spline = this.splines[k];
        (this.$refs.scene as Scene).scene.add(spline.mesh);
      }

      this.load([
        new Vector3(28.76843686945404, 45.51481137238443, 5.10018915737797),
        new Vector3(-5.56300074753207, 17.49711742836848, -1.495472686253045),
        new Vector3(-9.40118730204415, 17.4306956436485, -0.958271935582161),
        new Vector3(-38.785318791128, 49.1365363371675, 4.869296953772746),
      ]);

      this.onWindowResize();
    },

    addSplineObject(position) {
      const material = new MeshLambertMaterial({ color: Math.random() * 0xffffff });
      const object = new Mesh(this.geometry, material);
      if (position) {
        object.position.copy(position);
      } else {
        object.position.x = Math.random() * 1000 - 500;
        object.position.y = Math.random() * 600;
        object.position.z = Math.random() * 800 - 400;
        object.position.z = Math.random() * 800 - 400;
      }
      object.castShadow = true;
      object.receiveShadow = true;
      (this.$refs.scene as Scene).scene.add(object);
      (this.splineHelperObjects as any).push(object);
      return object;
    },

    addPoint() {
      this.splinePointsLength++;
      this.positions.push(this.addSplineObject(null).position);
      this.updateSplineOutline();
      this.render();
    },

    removePoint() {
      if (this.splinePointsLength <= 4) {
        return;
      }
      const point = this.splineHelperObjects.pop();
      this.splinePointsLength--;
      this.positions.pop();
      if (this.transformControl.object === this.point) this.transformControl.detach();
      (this.$refs.scene as Scene).scene.remove(this.point);
      this.updateSplineOutline();
      this.render();
    },

    updateSplineOutline() {
      for (const k in this.splines) {
        const spline = this.splines[k];
        const splineMesh = spline.mesh;
        const position = splineMesh.geometry.attributes.position;
        for (let i = 0; i < this.ARC_SEGMENTS; i++) {
          const t = i / (this.ARC_SEGMENTS - 1);
          spline.getPoint(t, this.point);
          position.setXYZ(i, this.point.x, this.point.y, this.point.z);
        }
        position.needsUpdate = true;
      }
    },

    exportSpline() {
      const strplace: any[] = [];
      for (let i = 0; i < this.splinePointsLength; i++) {
        const p = this.splineHelperObjects[i].position;
        strplace.push(`new Vector3(${p.x}, ${p.y}, ${p.z})`);
      }
      console.log(strplace.join(",\n"));
      const code = "[" + strplace.join(",\n\t") + "]";
      prompt("copy and paste code", code);
    },

    delayLoadAnimation() {
      setTimeout(() => {
        this.onWindowResize();
        this.render();
      }, 1000);
    },

    load(new_positions) {
      while (new_positions.length > this.positions.length) {
        this.addPoint();
      }
      while (new_positions.length < this.positions.length) {
        this.removePoint();
      }
      for (let i = 0; i < this.positions.length; i++) {
        this.positions[i].copy(new_positions[i]);
      }
      this.updateSplineOutline();
    },

    render() {
      if (this.renderer) {
        console.log("rendering");
        (this.splines as any).uniform.mesh.visible = this.params.uniform;
        (this.splines as any).centripetal.mesh.visible = this.params.centripetal;
        (this.splines as any).chordal.mesh.visible = this.params.chordal;
        let scene: Scene = this.renderer.scene;
        let camera: Scene = this.camera;
        this.renderer.render(scene, camera);
      }
    },

    onPointerDown(event) {
      this.onDownPosition.x = (event as any).clientX;
      this.onDownPosition.y = (event as any).clientY;
    },

    onPointerUp() {
      this.onUpPosition.x = (event as any).clientX;
      this.onUpPosition.y = (event as any).clientY;

      if (this.onDownPosition.distanceTo(this.onUpPosition) === 0)
        (this.transformControl as any).detach();
    },

    onPointerMove(event) {
      if (this.$refs.renderer != null) {
        let renderer = (this.$refs.renderer as Renderer).renderer;
        //let canvas = renderer.canvas;
        // this.pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
        // this.pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;

        //console.log(renderer, renderer.domElement);

        var rect = renderer.domElement.getBoundingClientRect();
        this.pointer.x = ((event.clientX - rect.left) / (rect.right - rect.left)) * 2 - 1;
        this.pointer.y = -((event.clientY - rect.top) / (rect.bottom - rect.top)) * 2 + 1;

        // this.pointer.x =
        //   ((event.clientX - renderer.domElement.offsetLeft) /
        //     renderer.domElement.clientWidth) *
        //     2 -
        //   1;
        // this.pointer.y =
        //   -(
        //     (event.clientY - renderer.domElement.offsetTop) /
        //     renderer.domElement.clientHeight
        //   ) *
        //     2 +
        //   1;

        //console.log((this.renderer as any).three.pointer.intersectObjects.length, (this.renderer as any).three.positionN .intersectObjects.length);

        this.raycaster.setFromCamera(this.pointer, this.camera);
        const intersects = this.raycaster.intersectObjects(
          this.splineHelperObjects,
          false
        );
        // console.log("intersects", intersects);
        if (intersects.length > 0) {
          const object = intersects[0].object;
          console.log("intersected");
          if (object !== (this.transformControl as any).object) {
            (this.transformControl as any).attach(object);
          }
        }
      }
    },

    onWindowResize() {
      console.log("resize");
      //let camera = (this.$refs.camera as Camera).camera;
      console.log("camera", this.camera);
      if (this.camera != null) {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
      }
      if (this.renderer) {
        this.renderer.setSize(window.innerWidth, window.innerHeight);
      }
      this.render();
    },

    previewFrame() {
      ApiService.post(
        this.apiUrl + "/api/task/preview/" + (this.state.project as any).id.toString() + "/" + this.state.selectedFrame.toString(),
        {}
      )
        .then(({ data }) => {
          console.log(data);
          // this.getProject((this.state.project as any).id);

          THREE.ImageUtils.crossOrigin = '';
          let  mapOverlay = THREE.ImageUtils.loadTexture(this.apiUrl  + "/output/" + data);

          this.previewMaterial = new THREE.MeshBasicMaterial({ //CHANGED to MeshBasicMaterial
              map:mapOverlay
          });
          this.previewMaterial.map.needsUpdate = true; //ADDED

          // plane
          this.previewImage = new THREE.Mesh(new THREE.PlaneGeometry(200, 200),this.previewMaterial);
          this.previewImage.overdraw = true;
          this.renderer.scene.add(this.previewImage);



          console.log();
        })
        .catch(({ response }) => {});
    },
  },
  // watch: {},
});
</script>
