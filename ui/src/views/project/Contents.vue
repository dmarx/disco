<template>
  <div v-if="state.mounted">
    <Teleport to="#aside-context">
      <AsideDefaultMenu></AsideDefaultMenu>
    </Teleport>
  </div>
  <div class="notice d-flex bg-light-primary rounded border-primary border border-dashed p-6">
    <!--begin::Icon-->
    <!--begin::Svg Icon | path: icons/duotune/finance/fin001.svg-->
    <span class="svg-icon svg-icon-2tx svg-icon-primary me-4">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
      >
        <path
          d="M20 19.725V18.725C20 18.125 19.6 17.725 19 17.725H5C4.4 17.725 4 18.125 4 18.725V19.725H3C2.4 19.725 2 20.125 2 20.725V21.725H22V20.725C22 20.125 21.6 19.725 21 19.725H20Z"
          fill="black"
        />
        <path
          opacity="0.3"
          d="M22 6.725V7.725C22 8.325 21.6 8.725 21 8.725H18C18.6 8.725 19 9.125 19 9.725C19 10.325 18.6 10.725 18 10.725V15.725C18.6 15.725 19 16.125 19 16.725V17.725H15V16.725C15 16.125 15.4 15.725 16 15.725V10.725C15.4 10.725 15 10.325 15 9.725C15 9.125 15.4 8.725 16 8.725H13C13.6 8.725 14 9.125 14 9.725C14 10.325 13.6 10.725 13 10.725V15.725C13.6 15.725 14 16.125 14 16.725V17.725H10V16.725C10 16.125 10.4 15.725 11 15.725V10.725C10.4 10.725 10 10.325 10 9.725C10 9.125 10.4 8.725 11 8.725H8C8.6 8.725 9 9.125 9 9.725C9 10.325 8.6 10.725 8 10.725V15.725C8.6 15.725 9 16.125 9 16.725V17.725H5V16.725C5 16.125 5.4 15.725 6 15.725V10.725C5.4 10.725 5 10.325 5 9.725C5 9.125 5.4 8.725 6 8.725H3C2.4 8.725 2 8.325 2 7.725V6.725L11 2.225C11.6 1.925 12.4 1.925 13.1 2.225L22 6.725ZM12 3.725C11.2 3.725 10.5 4.425 10.5 5.225C10.5 6.025 11.2 6.725 12 6.725C12.8 6.725 13.5 6.025 13.5 5.225C13.5 4.425 12.8 3.725 12 3.725Z"
          fill="black"
        />
      </svg>
    </span>
    <!--end::Svg Icon-->
    <!--end::Icon-->
    <!--begin::Wrapper-->
    <div class="d-flex flex-stack flex-grow-1 flex-wrap flex-md-nowrap">
      <!--begin::Content-->
      <div class="mb-3 mb-md-0 fw-bold">
        <h4 class="text-gray-900 fw-bolder">Upload Data</h4>
        <div
          class="fs-6 text-gray-700 pe-7"
        >Upload more data to enrich your case and discover new items of interest.</div>
      </div>
      <!--end::Content-->
      <!--begin::Action-->
      <a href="#" class="btn btn-primary px-6 align-self-center text-nowrap">Upload</a>
      <!--end::Action-->
    </div>
    <!--end::Wrapper-->
  </div>
  <br />
  <div class="row g-5 gx-xxl-8">
    <div class="col-xxl-12">
      <Contents widget-classes="card-xxl-stretch mb-5 mb-xxl-8"></Contents>
    </div>
  </div>
  <!--end::Dashboard-->
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import Contents from "@/components/widgets/tables/Contents.vue";
import { setCurrentPageTitle } from "@/core/helpers/breadcrumb";
import { reactive } from 'vue';
import AsideDefaultMenu from "@/components/widgets/menus/AsideDefaultMenu.vue";
import { useRoute } from 'vue-router';

export default defineComponent({
  name: "contents",
  components: {
    Contents,
    AsideDefaultMenu
  },
  setup() {
    const state = reactive({ count: 0, mounted: false })
    onMounted(() => {
      setCurrentPageTitle("Contents");
      state.mounted = true;
    });
    return {
      state,

    }
  },
});
</script>
