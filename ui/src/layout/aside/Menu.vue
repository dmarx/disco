<template>
  <div>
    <div class="active-case" style="    background: rgb(36, 36, 36);
    text-align: center;
    padding: 42px 0 15px 0;">
      <div class="row">
        <!-- <div class="col-3">
          <div
            style="
              background-color: #b06601;
              width: 42px;
              height: 42px;
              display: block;
              margin: 8px;
              border-radius: 5px;
              line-height: 44px;
              text-align: center;
              font-weight: bold;
            "
          >
            DD
          </div>
        </div> -->
        <div
          class="col-12"
          style="
            line-height: 42px;
            margin-top: 15px;
            color: #fff;
            font-size: 10px;
          "
        >
          <div style="line-height: 16px">
            <b>Project Template</b>
            <br />Disco Diffusion
          </div>
        </div>
      </div>
    </div>

    <div
      id="kt_aside_menu_wrapper"
      ref="scrollElRef"
      class="hover-scroll-overlay-y my-5 my-lg-5"
      data-kt-scroll="true"
      data-kt-scroll-activate="{default: false, lg: true}"
      data-kt-scroll-dependencies="#kt_aside_logo, #kt_aside_footer"
      data-kt-scroll-height="auto"
      data-kt-scroll-offset="0"
      data-kt-scroll-wrappers="#kt_aside_menu"
    >
      <!--begin::Menu-->
      <div
        id="#kt_header_menu"
        class="
          menu
          menu-column
          menu-title-gray-800
          menu-state-title-primary
          menu-state-icon-primary
          menu-state-bullet-primary
          menu-arrow-gray-500
        "
        data-kt-menu="true"
      >
        <div id="aside-context"></div>

        <!-- <template v-for="(item, i) in MainMenuConfig" :key="i">
        <div v-if="item.heading" class="menu-item">
          <div class="menu-content pt-8 pb-2">
            <span
              class="menu-section text-muted text-uppercase fs-8 ls-1"
            >{{ translate(item.heading) }}</span>
          </div>
        </div>
        <template v-for="(menuItem, j) in item.pages" :key="j">
          <template v-if="menuItem.heading">
            <div class="menu-item">
              <router-link class="menu-link" active-class="active" :to="menuItem.route">
                <span v-if="menuItem.svgIcon || menuItem.fontIcon" class="menu-icon">
                  <i v-if="asideMenuIcons === 'font'" :class="menuItem.fontIcon" class="bi fs-3"></i>
                  <span v-else-if="asideMenuIcons === 'svg'" class="svg-icon svg-icon-2">
                    <inline-svg :src="menuItem.svgIcon" />
                  </span>
                </span>
                <span class="menu-title">
                  {{
                    translate(menuItem.heading)
                  }}
                </span>
              </router-link>
            </div>
          </template>
          <div
            v-if="menuItem.sectionTitle"
            :class="{ show: hasActiveChildren(menuItem.route) }"
            class="menu-item menu-accordion"
            data-kt-menu-sub="accordion"
            data-kt-menu-trigger="click"
          >
            <span class="menu-link">
              <span v-if="menuItem.svgIcon || menuItem.fontIcon" class="menu-icon">
                <i v-if="asideMenuIcons === 'font'" :class="menuItem.fontIcon" class="bi fs-3"></i>
                <span v-else-if="asideMenuIcons === 'svg'" class="svg-icon svg-icon-2">
                  <inline-svg :src="menuItem.svgIcon" />
                </span>
              </span>
              <span class="menu-title">
                {{
                  translate(menuItem.sectionTitle)
                }}
              </span>
              <span class="menu-arrow"></span>
            </span>
            <div
              :class="{ show: hasActiveChildren(menuItem.route) }"
              class="menu-sub menu-sub-accordion"
            >
              <template v-for="(item2, k) in menuItem.sub" :key="k">
                <div v-if="item2.heading" class="menu-item">
                  <router-link class="menu-link" active-class="active" :to="item2.route">
                    <span class="menu-bullet">
                      <span class="bullet bullet-dot"></span>
                    </span>
                    <span class="menu-title">
                      {{
                        translate(item2.heading)
                      }}
                    </span>
                  </router-link>
                </div>
                <div
                  v-if="item2.sectionTitle"
                  :class="{ show: hasActiveChildren(item2.route) }"
                  class="menu-item menu-accordion"
                  data-kt-menu-sub="accordion"
                  data-kt-menu-trigger="click"
                >
                  <span class="menu-link">
                    <span class="menu-bullet">
                      <span class="bullet bullet-dot"></span>
                    </span>
                    <span class="menu-title">
                      {{
                        translate(item2.sectionTitle)
                      }}
                    </span>
                    <span class="menu-arrow"></span>
                  </span>
                  <div
                    :class="{ show: hasActiveChildren(item2.route) }"
                    class="menu-sub menu-sub-accordion"
                  >
                    <template v-for="(item3, k) in item2.sub" :key="k">
                      <div v-if="item3.heading" class="menu-item">
                        <router-link class="menu-link" active-class="active" :to="item3.route">
                          <span class="menu-bullet">
                            <span class="bullet bullet-dot"></span>
                          </span>
                          <span class="menu-title">
                            {{
                              translate(item3.heading)
                            }}
                          </span>
                        </router-link>
                      </div>
                    </template>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </template>
      </template>-->
        <!-- <div class="menu-item">
          <div class="menu-content">
            <div class="separator mx-1 my-4"></div>
          </div>
        </div>
        <div class="menu-item" v-if="route.path != '/cases'">
          <a class="menu-link" href="/#/cases">
            <span class="menu-icon">
              <i
                v-if="asideMenuIcons === 'font'"
                class="bi bi-card-text fs-3"
              ></i>
              <span
                v-else-if="asideMenuIcons === 'svg'"
                class="svg-icon svg-icon-2"
              >
                <inline-svg src="media/icons/duotune/general/gen005.svg" />
              </span>
            </span>
            <span class="menu-title">Back to All Cases</span>
          </a>
        </div>
        <div class="menu-item">
          <a class="menu-link" href="/#/news">
            <span class="menu-icon">
              <i
                v-if="asideMenuIcons === 'font'"
                class="bi bi-card-text fs-3"
              ></i>
              <span
                v-else-if="asideMenuIcons === 'svg'"
                class="svg-icon svg-icon-2"
              >
                <inline-svg src="media/icons/duotune/general/gen005.svg" />
              </span>
            </span>
            <span class="menu-title">News &amp; Updates</span>
          </a>
        </div> -->
      </div>
      <!--end::Menu-->
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n/index";
import { version } from "@/core/helpers/documentation";
import { asideMenuIcons } from "@/core/helpers/config";
import MainMenuConfig from "@/core/config/MainMenuConfig";
import { useRouter, useRoute } from "vue-router";

export default defineComponent({
  name: "kt-menu",
  components: {},
  setup() {
    const router = useRouter();
    const route = useRoute();
    const { t, te } = useI18n();
    const scrollElRef = ref<null | HTMLElement>(null);

    watch(
      () => route.params.id,
      () => {
        console.log(route.path);
      }
      // async newId => {
      //   userData.value = await fetchUser(newId)
      // }
    );

    onMounted(() => {
      if (scrollElRef.value) {
        scrollElRef.value.scrollTop = 0;
      }

      console.log("Blue menu mounted");
      // this.$emit("AsideMounted");
    });

    const translate = (text) => {
      if (te(text)) {
        return t(text);
      } else {
        return text;
      }
    };

    const hasActiveChildren = (match) => {
      return route.path.indexOf(match) !== -1;
    };

    return {
      hasActiveChildren,
      MainMenuConfig,
      asideMenuIcons,
      version,
      translate,
      route,
      router,
    };
  },
});
</script>
