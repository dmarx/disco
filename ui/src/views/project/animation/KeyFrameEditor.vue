<template>
  <div>
    <div v-if="!generator" style="color: #fff">
      <h3>Animation Tools</h3>
      Only visible when a Disco generator is in the chain.
    </div>
    <div v-show="generator != null">
      <div class="bg-gray-300 m-1 p-3 rounded-md text-center item-generator">
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
              v-if="generator && generator.settings"
              style="display: inline-block; display: inline-block; margin-right: 60px"
              >Mode:&nbsp;
              <select
                v-model="generator.settings['animation_mode']"
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
            &nbsp;&nbsp;
            <button class="btn btn-primary btn-sm" @click="resetFrames()">Reset</button>
            &nbsp;&nbsp;
            <button
              class="btn btn-primary btn-sm"
              @click="loadPreviewFrame(state.selectedFrame)"
            >
              Preview
            </button>
            &nbsp;&nbsp;
            <button class="btn btn-primary btn-sm" @click="exportToKeyframes()">
              Export
            </button>
          </div>
          Animation Tools&nbsp;&nbsp;&nbsp;
          <button
            class="btn btn-primary btn-sm"
            @click="scrub_start()"
            style="margin-right: 8px"
          >
            <i class="fas fa-backward"></i>
          </button>
          <button
            class="btn btn-primary btn-sm"
            @click="scrub_play()"
            v-if="state.autoPlay == false"
            style="margin-right: 8px"
          >
            <i class="fas fa-play"></i>
          </button>
          <button
            class="btn btn-primary btn-sm"
            @click="scrub_pause()"
            v-if="state.autoPlay == true"
            style="margin-right: 8px"
          >
            <i class="fas fa-pause"></i>
          </button>
          <button
            class="btn btn-primary btn-sm"
            @click="scrub_end()"
            style="margin-right: 8px"
          >
            <i class="fas fa-fast-forward"></i>
          </button>
        </h3>

        <div style="width: 100%" v-if="generator && generator.settings">
          <label style="color: #fff; width: 100%; text-align: center; color: #999">
            Frame Timeline:
            <span id="sliderDisplayValue">0</span>
          </label>
          <fieldset style="width: 100%">
            <label id="slider-container" style="width: 100%">
              <input
                style="width: 100%; display: block"
                ref="frameTimelineSlider"
                id="frameTimelineSlider"
                class="slider"
                type="range"
                min="0"
                :max="generator.settings.max_frames"
                value="0"
                step="1"
              />
            </label>
          </fieldset>
          <div>
            <br />
            <b>Keyframe Details</b><br />
            <div class="row">
              <div class="col-4">
                Translation (X):
                <input type="text" class="form-control" :value="state.curFrame.x" /><br />
              </div>
              <div class="col-4">
                Translation (Y):
                <input type="text" class="form-control" :value="state.curFrame.y" /><br />
              </div>
              <div class="col-4">
                Translation (Z):
                <input type="text" class="form-control" :value="state.curFrame.z" /><br />
              </div>
            </div>
          </div>
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
</template>

<script lang="ts">
import * as THREE from "three";
import { TWEEN } from "three/examples/jsm/libs/tween.module.min";

import ApiService from "@/core/services/ApiService";

import { defineComponent, onMounted, ref, reactive } from "vue";
import Flow from "../../views/project/flow/Flow.vue";
import { inject } from "vue";
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
    ApiService,
  },
  props: {
    project: null,
    generator: null,
  },
  setup() {
    let apiUrl = "http://localhost:5000";

    const state = reactive({
      count: 0,
      mounted: false,
      list: [],
      busy: false,
      output: "",
      progress: 0,
      progressPercentage: "",
      preloadFrame: 0,
      selectedFrame: 0,
      autoPlay: false,
      curFrame: {},
      keyframes: [],
      // renderer,
      // box
    });

    // const frameTimelineSlider = ref();

    const renderer: any = null;
    const camera: any = null;

    const previewPlanes: any[] = [];
    const splineHelperObjects: any[] = [];
    let splinePointsLength = 100;
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

    const splines = {};
    const tween: any = null;

    const params = {
      uniform: true,
      tension: 0.75,
      centripetal: false,
      chordal: false,
      addPoint: null,
      removePoint: null,
      exportSpline: null,
    };

    return {
      state,

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
      geometry,
      renderer,
      camera,
      previewMaterial,
      previewImage,
      tween,
      previewPlanes,
    };
  },

  mounted() {
    // setCurrentPageTitle("Studio");

    if (location.host.indexOf("localhost") > -1) {
      this.apiUrl = "http://localhost:5000";
    } else {
      this.apiUrl = "";
    }

    this.renderer.onBeforeRender(() => {
      TWEEN.update();
    });
  },
  beforeDestroy() {},
  methods: {
    updateTimeframe() {
      let frameTimelineSlider = this.$refs.frameTimelineSlider as any;
      frameTimelineSlider.value = this.state.selectedFrame;
      // this.camera.position.copy(this.positions[this.state.selectedFrame]);
      // this.camera.position.z += 50.0;
      // console.log(this.state.selectedFrame);
      this.state.selectedFrame = +this.state.selectedFrame;

      var from = this.camera.position.clone();
      var to = new Vector3().copy(this.positions[this.state.selectedFrame]).clone();
      to.z += 100.0;
      //debugger;
      var lookAt: any = null;
      if (this.positions && this.state.selectedFrame < this.positions.length - 3) {
        let p2 = this.positions[this.state.selectedFrame + 1];
        if (p2) lookAt = new Vector3().copy(p2); //.clone();
      }
      if (lookAt) {
        lookAt.z += 100.0;
        // var cam = new Vector3()
        //   .copy(this.positions[this.state.selectedFrame])
        //   .clone()
        //   .subScalar(100);
        to.y += 25.0;
        // cam.y += 25.0;
        // console.log(from, to, cam);
        this.tween = new TWEEN.Tween(from)
          .to(to, 1500)
          .easing(TWEEN.Easing.Linear.None)
          .onUpdate((p) => {
            //console.log(p);
            this.camera.position.set(p.x, p.y, p.z);
            if (lookAt) this.camera.lookAt(to);
            // controls.update();
            // controls.target = new THREE.Vector3(
            //   -2.3990653437361487,
            //   -3.4148881873690886,
            //   54.09252756000919
            // );
          });
        this.tween.start();
      }
      if (this.state.autoPlay) {
        setTimeout(() => {
          if (this.state.selectedFrame < this.generator.settings.max_frames - 1) {
            this.state.selectedFrame += 1;
            this.updateTimeframe();
          }
        }, 1500);
      }
    },

    updateView() {
      if (this.generator) {
        let frameTimelineSlider = this.$refs.frameTimelineSlider as any;
        frameTimelineSlider.addEventListener("input", () => {
          const sliderValue = frameTimelineSlider.value;
          document.getElementById(
            "sliderDisplayValue"
          )!.innerHTML = ` ${sliderValue} / ${this.generator.settings.max_frames}`;
        });
        // does all filtering once slider has changed and been released
        frameTimelineSlider!.addEventListener("change", () => {
          this.state.selectedFrame = frameTimelineSlider.value;
          this.state.curFrame = this.state.keyframes[this.state.selectedFrame];
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

      this.splinePointsLength = this.generator.settings.max_frames;
      this.state.curFrame = { x: 0, y: 0, z: 0 };

      // cons
      this.state.keyframes = [];
      for (let i = 0; i < this.generator.settings.max_frames; i++) {
        (this.state.keyframes as any).push({ x: 0, y: 0, z: -1.0 });
      }

      this.buildScene();
      /*******
       * Curves
       *********/

      console.log(this.splinePointsLength, this.positions);
      for (let i = 0; i < this.splinePointsLength; i++) {
        this.addSplineObject(this.positions[i]);
      }

      this.positions.length = 0;

      for (let i = 0; i < this.splinePointsLength; i++) {
        this.positions.push((this.splineHelperObjects[i] as any).position);
      }
      console.log(this.splinePointsLength, this.positions);

      this.geometry = new BufferGeometry();
      this.geometry.setAttribute(
        "position",
        new BufferAttribute(new Float32Array(this.generator.settings.max_frames * 3), 3)
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

      //this.resetFrames();

      let new_positions: Vector3[] = [];
      for (let i = 0; i < this.splinePointsLength; i++) {
        let kf = this.state.keyframes[i] as any;
        let pos = new Vector3();
        if (i > 0) {
          let prev = new_positions[i - 1] as any;
          pos.x += prev.x + kf.x;
          pos.y += prev.y + kf.y;
          pos.z += prev.z + kf.z * 100.0;
        }
        new_positions.push(pos);
      }
      this.load(new_positions);

      this.onWindowResize();
    },

    buildScene() {
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

      const helper = new GridHelper(10000, 100);
      helper.position.y = -199;
      helper.position.z = -(this.generator.settings.max_frames * 100) / 2.0;
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
    },

    exportToKeyframes() {
      let sx = "";
      let sy = "";
      let sz = "";
      for (let i = 0; i < this.generator.settings.max_frames; i++) {
        let kf: any = this.state.keyframes[i];
        sx += i.toString() + ": (" + kf.x.toString() + "),";
        sy += i.toString() + ": (" + kf.y.toString() + "),";
        sz += i.toString() + ": (" + kf.z.toString() + "),";
      }

      this.generator.settings.translation_x = sx;
      this.generator.settings.translation_y = sy;
      this.generator.settings.translation_z = sz;

      console.log(this.generator.settings);
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
      // console.log("updateSplineOutline");
      let axis = new THREE.Vector3();
      let up = new THREE.Vector3(0, 0, -1);
      for (const k in this.splines) {
        const spline = this.splines[k];
        const splineMesh = spline.mesh;
        const position = splineMesh.geometry.attributes.position;
        for (let i = 0; i < this.generator.settings.max_frames; i++) {
          const t = i / (this.generator.settings.max_frames - 1);
          spline.getPoint(t, this.point);
          position.setXYZ(i, this.point.x, this.point.y, this.point.z);

          console.log("updating kf");
          if (i > 0) {
            let prev: any = this.positions[i - 1];
            let kf: any = this.state.keyframes[i];
            kf.x = (this.point.x - prev.x) / 100.0;
            kf.y = (this.point.y - prev.y) / 100.0;
            kf.z = (this.point.z - prev.z) / 100.0;
            console.log(kf);
          }

          let pp = this.previewPlanes.find((x) => x.userData.id == i);
          if (pp) {
            // console.log(pp,i,this.point)
            pp.position.set(this.point.x, this.point.y, this.point.z);

            // get the tangent to the curve
            let tangent = spline.getTangent(t).normalize();

            // calculate the axis to rotate around
            axis.crossVectors(new THREE.Vector3(0, 0, -1), tangent).normalize();

            // calcluate the angle between the up vector and the tangent
            let radians = Math.acos(up.dot(tangent));

            // set the quaternion
            pp.rotation.y = Math.PI / 2;
            pp.quaternion.setFromAxisAngle(axis, radians);
          }
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
        // console.log("rendering");
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
      // console.log("resize");
      // //let camera = (this.$refs.camera as Camera).camera;
      // console.log("camera", this.camera);
      if (this.camera != null) {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
      }
      if (this.renderer) {
        try {
          this.renderer.setSize(window.innerWidth, window.innerHeight);
        } catch (e) {}
        this.render();
      }
    },

    existsFile(url) {
      var http = new XMLHttpRequest();
      http.open("HEAD", url, false);
      http.send();
      return http.status != 404;
    },

    loadPreviewFrame(frame) {
      let fr = parseInt(Math.round(frame).toString());
      let path =
        "/data/projects/" +
        (this.project as any).id.toString() +
        "/" +
        "output/2/preview/" +
        fr.toString() +
        "/preview.png";

      if (this.existsFile(this.apiUrl + path)) {
        // console.log("exists", this.apiUrl + path);
        this.addPreviewToScene(path, frame);
      } else {
        ApiService.post(
          this.apiUrl +
            "/api/task/preview/" +
            (this.project as any).id.toString() +
            "/" +
            fr.toString(),
          {}
        )
          .then((data) => {
            //console.log("preview", data.data);
            //this.getProject((this.project as any).id);
            // console.log("fetched", this.apiUrl + path, data.data);
            if (data.data != "Busy") this.addPreviewToScene(path, frame);
          })
          .catch(({ response }) => {});
      }
    },

    addPreviewToScene(path, frame) {
      THREE.ImageUtils.crossOrigin = "";

      console.log(this.apiUrl + path);

      const texture = new THREE.TextureLoader().load(this.apiUrl + path, () => {
        mat.map.needsUpdate = true; //ADDED
      });

      const mat = new THREE.MeshBasicMaterial({
        transparent: true,
        map: texture,
        opacity: 0.5,
        side: THREE.DoubleSide,
      });

      // console.log("selframe", this.state.selectedFrame);
      let previewPlane = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), mat);
      previewPlane.userData.id = frame;
      previewPlane.position.z = -frame * 100.0;
      previewPlane.overdraw = true;
      this.previewPlanes.push(previewPlane);
      this.renderer.scene.add(previewPlane);

      // if (this.state.preloadFrame < 100) {
      //   this.state.preloadFrame += 5;
      //   // this.state.selectedFrame = this.state.preloadFrame;
      //   this.loadPreviewFrame(this.state.preloadFrame);
      // }
    },

    resetFrames() {
      let av: any[] = [];
      for (let i = 0; i < this.splinePointsLength; i++) {
        av.push(new Vector3(0, 0, -100.0 * i));
      }
      this.load(av);
    },

    scrub_start() {
      this.state.autoPlay = false;
      this.state.selectedFrame = 0;
      this.updateTimeframe();
    },
    scrub_play() {
      this.state.autoPlay = true;
      this.updateTimeframe();
    },
    scrub_pause() {
      this.state.autoPlay = false;
      // this.updateTimeframe();
    },
    scrub_end() {
      this.state.autoPlay = false;
      this.state.selectedFrame = this.generator.settings.max_frames - 1;
      this.updateTimeframe();
    },
  },

  // watch: {},
});
</script>
