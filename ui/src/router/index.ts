import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import store from "@/store";
import { Mutations, Actions } from "@/store/enums/StoreEnums";
import JwtService from "@/core/services/JwtService";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/projects",
    component: () => import("@/layout/Layout.vue"),
    children: [
      {
        path: "/projects",
        name: "projects",
        component: () => import("@/views/Projects.vue"),
      },
      {
        path: "/builder",
        name: "builder",
        component: () => import("@/views/Builder.vue"),
      },
      {
        path: "/project/:id/admin",
        name: "project-admin",
        component: () => import("@/views/project/Admin.vue"),
      },
      {
        path: "/project/:id/studio",
        name: "project-studio",
        component: () => import("@/views/project/Studio.vue"),
      },
      // {
      //   path: "/project/admin",
      //   name: "project-admin",
      //   component: () => import("@/views/project/Admin.vue"),
      // },
      // {
      //   path: "/project/contents/preview",
      //   name: "project-contents-preview",
      //   component: () => import("@/views/project/contents/Preview.vue"),
      // },
      // {
      //   path: "/project/dashboard",
      //   name: "project-dashboard",
      //   component: () => import("@/views/project/Dashboard.vue"),
      // },
      // {
      //   path: "/project/data",
      //   name: "project-data",
      //   component: () => import("@/views/project/Data.vue"),
      // },
      // {
      //   path: "/project/reports",
      //   name: "project-reports",
      //   component: () => import("@/views/project/Reports.vue"),
      // },
      // {
      //   path: "/project/search",
      //   name: "project-search",
      //   component: () => import("@/views/project/Search.vue"),
      // },
      // {
      //   path: "/project/workspace",
      //   name: "project-workspace",
      //   component: () => import("@/views/project/Workspace.vue"),
      // },

    ],
  },
  {
    path: "/",
    component: () => import("@/components/page-layouts/Auth.vue"),
    children: [
      {
        path: "/sign-in",
        name: "sign-in",
        component: () =>
          import("@/views/crafted/authentication/basic-flow/SignIn.vue"),
      },
      {
        path: "/sign-up",
        name: "sign-up",
        component: () =>
          import("@/views/crafted/authentication/basic-flow/SignUp.vue"),
      },
      {
        path: "/password-reset",
        name: "password-reset",
        component: () =>
          import("@/views/crafted/authentication/basic-flow/PasswordReset.vue"),
      },
    ],
  },
  {
    // the 404 route, when none of the above matches
    path: "/404",
    name: "404",
    component: () => import("@/views/crafted/authentication/Error404.vue"),
  },
  {
    path: "/500",
    name: "500",
    component: () => import("@/views/crafted/authentication/Error500.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/404",
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach(() => {
  // reset config to initial state
  store.commit(Mutations.RESET_LAYOUT_CONFIG);

  store.dispatch(Actions.VERIFY_AUTH, { api_token: JwtService.getToken() });

  // Scroll page to top on every route change
  setTimeout(() => {
    window.scrollTo(0, 0);
  }, 100);
});

export default router;
