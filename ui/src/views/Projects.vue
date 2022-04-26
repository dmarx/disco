<template>
  <div class="row">

    <template  v-for="(item, k) in state.projects" :key="k">
      <div class="col-3" style="margin-bottom:15px">
        <div class="card" style="text-align: center">
          <div class="card-body">
            <br />
            <br />
            <br />
            <h3 v-if="item?.ength==0">Unnamd Project</h3>
            <!-- <buttom  v-iftitleitem.length>0">{{ item.tietle }}</h3> -->
            <br />
            <br />
            <button class="btn btn-primary" @click="showProject(item.id)">View</button><!-- <router-link to="item.id"> Launch </router-link> -->
          </div>
          <br />
        <span style="color:#FFF !important">{{item.id}}</span>
          <br />
          <br />
        </div>
      </div>
    </template>
    
    <div class="col-3">
      <div class="card" style="text-align: center">
        <div class="card-body">
          <br />
          <br />
          <br />
            <h3 >Start Project</h3>
          <br />
          <br />

          <button class="btn btn-primary" @click="addProject()">
            <i class="bi bi-plus fs-3"></i>
          </button>
          <br />
          <br />
          <span>nbsp;</span>
          <br />
          <br />
        </div>
      </div>
    </div>
  </div>

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

    </Teleport>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { setCurrentPageTitle } from "@/core/helpers/breadcrumb";
import { reactive } from "vue";
import ApiService from "@/core/services/ApiService";

export default defineComponent({
  name: "cases",
  components: {},
  setup() {
    const state = reactive({
      count: 0,
      mounted: false,
      projects: null,
    });
    return {
      state,
    };
  },
  mounted() {
    setCurrentPageTitle("Projects");
    this.state.mounted = true;
    this.getProjects();
  },
  methods: {
    showProject(id){
      this.$router.push("/project/"+id+"/studio");
    },
    getProjects() {
      console.log("get")
      ApiService.post("http://localhost:5000/api/projects", {})
        .then(({ data }) => {
          this.state.projects = data;
          console.log("get projects" ,data);
        })
        .catch(({ response }) => {});
    },
    addProject() {
      console.log("add")
      ApiService.post("http://localhost:5000/api/project/add", {})
        .then(({ data }) => {
          //this.state.projects = data;
          this.getProjects();
        })
        .catch(({ response }) => {});
    },
    saveProject(id) {
      console.log("save")
      ApiService.post("http://localhost:5000/api/project/" + id.toString(), {})
        .then(({ data }) => {
          //this.state.projects = data;
          // this.getProjects();
        })
        .catch(({ response }) => {});
    },
    deleteProject(id) {
      console.log("delete")
      ApiService.delete("http://localhost:5000/api/project/" + id.toString())
        .then(({ data }) => {
          //this.state.projects = data;
          // this.getProjects();
        })
        .catch(({ response }) => {});
    },
  },
});
</script>
