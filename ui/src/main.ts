import { createApp } from "vue";
import App from "./App.vue";

import store from './store'
// import axios from 'axios'
// import VueAxios from 'vue-axios'

/*
TIP: To get started with clean router change path to @/router/clean.ts.
 */
import router from "./router";
import ElementPlus from "element-plus";
import i18n from "@/core/plugins/i18n";

//imports for app initialization
import ApiService from "@/core/services/ApiService";
import { initApexCharts } from "@/core/plugins/apexcharts";
import { initInlineSvg } from "@/core/plugins/inline-svg";
import { initVeeValidate } from "@/core/plugins/vee-validate";

import * as THREE from 'three';
import { TroisJSVuePlugin } from 'troisjs';

import "@/core/plugins/prismjs";
import "bootstrap";

import "@braks/vue-flow/dist/style.css";
import "@braks/vue-flow/dist/theme-default.css";

// import Vue from 'vue'
const app = createApp(App).use(store);
// app.use(VueAxios, axios)
app.use(router);
app.use(ElementPlus);
app.use(TroisJSVuePlugin);

// app.provide('axios', app.config.globalProperties.axios)

ApiService.init(app);
initApexCharts(app);
initInlineSvg(app);
initVeeValidate();

app.use(i18n);
// app.use(FlowyPlugin);

app.mount("#app");
