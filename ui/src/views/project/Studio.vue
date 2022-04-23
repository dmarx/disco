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
          <div class="card-header pt-10">
            <div class="d-flex align-items-center">
              <div class="symbol symbol-circle me-5">
                <div
                  class="
                    symbol-label
                    bg-transparent
                    text-primary
                    border border-secondary border-dashed
                  "
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

              <div class="d-flex flex-column" style="margin-top: -21px">
                <h2 class="mb-1">Settings</h2>
                <div class="text-muted fw-bolder" style="line-height: 2px">
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
                class="
                  nav nav-stretch nav-line-tabs nav-line-tabs-2x
                  border-transparent
                  fs-5
                  fw-bold
                  flex-nowrap
                "
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
          <div class="card-header pt-8">
            <div class="card-title">
              <h2>Design Scene</h2>
            </div>
          </div>

          <div class="card-body">
            <form class="form" id="kt_file_manager_settings">
              <div class="fv-row row mb-15">
                <div class="col-md-3 d-flex align-items-center">
                  <label class="fs-6 fw-bold white" style="color: #fff"
                    >Prompt</label
                  >
                </div>

                <div class="col-md-9">
                  <input type="text" class="form-control" />
                </div>
              </div>

              <div class="fv-row row mb-15">
                <div class="col-md-3">
                  <label class="fs-6 fw-bold mt-2">Steps</label>
                  <div class="text-muted fs-7">
                    More info on steps can be found
                    <a href="#" target="_blank">here</a>.
                  </div>
                </div>

                <div class="col-md-3">
                  <input type="text" class="form-control" value="50" />
                </div>

                <div class="col-md-3">
                  <label class="fs-6 fw-bold mt-2 text-right">Resolution</label>
                  <!-- <div class="text-muted fs-7">
                More info on steps can be found 
                <a
                  href="#"
                  target="_blank"
                  >here</a
                >.
              </div> -->
                </div>

                <div class="col-md-3">
                  <input type="text" class="form-control" value="512x512" />
                </div>
              </div>

              <!-- <div class="fv-row row mb-15">
            <div class="col-md-3 d-flex align-items-center">
              <label class="fs-6 fw-bold">Automatic time zone</label>
            </div>

            <div class="col-md-9">
              <div
                class="
                  form-check form-switch form-check-custom form-check-solid
                  me-10
                "
              >
                <input
                  class="form-check-input h-30px w-50px"
                  name="autotimezone"
                  type="checkbox"
                  value=""
                  id="autotimezone"
                />
                <label class="form-check-label" for="autotimezone"
                  >GMT +10:00</label
                >
              </div>
            </div>
          </div> -->
              <!-- 
          <div class="fv-row row mb-15">
            <div class="col-md-3">
              <label class="fs-6 fw-bold mt-2">Folder Compression</label>
              <div class="text-muted fs-7">
                Default file compression type when downloading folders
              </div>
            </div>

            <div class="col-md-9">
              <select
                name="compression"
                aria-label="Select a Compressions type"
                data-control="select2"
                data-hide-search="true"
                data-placeholder="Select a Compressions type..."
                class="form-select mb-2 select2-hidden-accessible"
                data-select2-id="select2-data-16-nwub"
                tabindex="-1"
                aria-hidden="true"
              >
                <option data-select2-id="select2-data-18-qr9p"></option>
                <option value="1">*.zip</option>
                <option value="2">*.7z</option>
                <option value="3">*.rar</option>
                <option value="4">*.tar.gz</option></select
              ><span
                class="select2 select2-container select2-container--bootstrap5"
                dir="ltr"
                data-select2-id="select2-data-17-73hu"
                style="width: 100%"
                ><span class="selection"
                  ><span
                    class="
                      select2-selection select2-selection--single
                      form-select
                      mb-2
                    "
                    role="combobox"
                    aria-haspopup="true"
                    aria-expanded="false"
                    tabindex="0"
                    aria-disabled="false"
                    aria-labelledby="select2-compression-7c-container"
                    aria-controls="select2-compression-7c-container"
                    ><span
                      class="select2-selection__rendered"
                      id="select2-compression-7c-container"
                      role="textbox"
                      aria-readonly="true"
                      title="Select a Compressions type..."
                      ><span class="select2-selection__placeholder"
                        >Select a Compressions type...</span
                      ></span
                    ><span class="select2-selection__arrow" role="presentation"
                      ><b role="presentation"></b></span></span></span
                ><span class="dropdown-wrapper" aria-hidden="true"></span
              ></span>
            </div>
          </div> -->

              <div class="fv-row row mb-15">
                <div class="col-md-3">
                  <label class="fs-6 fw-bold">Selected Models</label>
                </div>

                <div class="col-md-9">
                  <label class="fs-6 fw-bold mb-3">ViT</label>

                  <div class="d-flex">
                    <div
                      class="
                        form-check
                        form-switch
                        form-check-custom
                        form-check-solid
                        me-10
                      "
                    >
                      <input
                        class="form-check-input h-30px w-50px"
                        name="org_read"
                        type="checkbox"
                        value=""
                        id="org_read"
                        checked="checked"
                      />
                      <label class="form-check-label" for="org_read"
                        >ViT-B/32</label
                      >
                    </div>

                    <div
                      class="
                        form-check
                        form-switch
                        form-check-custom
                        form-check-solid
                        me-10
                      "
                    >
                      <input
                        class="form-check-input h-30px w-50px"
                        name="org_write"
                        type="checkbox"
                        value=""
                        id="org_write"
                        checked="checked"
                      />
                      <label class="form-check-label" for="org_write"
                        >ViT-B/16</label
                      >
                    </div>
                  </div>

                  <div class="separator mt-6 mb-5"></div>

                  <label class="fs-6 fw-bold mb-3">ResNet</label>

                  <div class="d-flex">
                    <div
                      class="
                        form-check
                        form-switch
                        form-check-custom
                        form-check-solid
                        me-10
                      "
                    >
                      <input
                        class="form-check-input h-30px w-50px"
                        name="public_read"
                        type="checkbox"
                        value=""
                        id="public_read"
                        checked="checked"
                      />
                      <label class="form-check-label" for="public_read"
                        >RN50x16</label
                      >
                    </div>

                    <div
                      class="
                        form-check
                        form-switch
                        form-check-custom
                        form-check-solid
                        me-10
                      "
                    >
                      <input
                        class="form-check-input h-30px w-50px"
                        name="public_write"
                        type="checkbox"
                        value=""
                        id="public_write"
                      />
                      <label class="form-check-label" for="public_write"
                        >RN50x64</label
                      >
                    </div>
                  </div>
                </div>
              </div>

              <div class="row mt-12">
                <div class="col-md-9 offset-md-3">
                  <button type="button" class="btn btn-light me-3">
                    Reset
                  </button>

                  <button
                    type="button"
                    class="btn btn-primary"
                    id="kt_file_manager_settings_submit"
                  >
                    <span class="indicator-label">Start Run</span>
                    <span class="indicator-progress"
                      >Please wait...
                      <span
                        class="
                          spinner-border spinner-border-sm
                          align-middle
                          ms-2
                        "
                      ></span
                    ></span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>

        <div v-if="state.mounted">
          <Teleport to="#aside-context">
            <AsideDefaultMenu></AsideDefaultMenu>
          </Teleport>
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
            <span class="menu-section text-muted text-uppercase fs-8 ls-1"
              >Projects</span
            >
          </div>
          <span class="menu-link">
            <span class="menu-icon">
              <i class="bi bi-bag-check-fill fs-2x"></i>
            </span>
            <span class="menu-title">My Projects</span>
          </span>
          <span class="menu-link">
            <span class="menu-icon">
              <i class="bi bi-card-list fs-2x"></i>
            </span>
            <span class="menu-title">Shared Projects</span>
          </span>
          <span class="menu-link">
            <span class="menu-icon">
              <i class="bi bi-link-45deg fs-2x"></i>
            </span>
            <span class="menu-title">Closed Projects</span>
          </span>
        </div>
        <!-- 
      <div
        class="menu-item menu-accordion"
        data-kt-menu-sub="accordion"
        data-kt-menu-trigger="click"
      >
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">Investigation tools</span>
        </div>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-file-earmark-pdf-fill fs-2x"></i>
          </span>
          <span class="menu-title">Case reports &amp; evidence</span>
        </span>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-people-fill fs-2x"></i>
          </span>
          <span class="menu-title">People of interest</span>
        </span>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-briefcase-fill fs-2x"></i>
          </span>
          <span class="menu-title">Case log</span>
        </span>
      </div> -->
      </Teleport>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";

import { setCurrentPageTitle } from "@/core/helpers/breadcrumb";
// import Dropdown2 from "@/components/dropdown/Dropdown2.vue";
// var window : any;
// const KeyLines = window.KeyLines;
// KeyLines.promisify();
import { reactive } from "vue";
import FilterTimeline from "../../components/filters/FilterTimeline.vue";

interface Filter {
  status: string;
  author: boolean;
  customer: boolean;
  notifications: boolean;
}

export default defineComponent({
  name: "studio",
  components: {
    // Dropdown2,
    FilterTimeline,
  },
  setup() {
    const state = reactive({ count: 0, mounted: false });

    const currentStatus = reactive({
      busy: false,
      text: "Idle",
      mounted: false,
    });

    const currentProject = reactive({
      busy: false,
      text: "",
      steps: 50,
      resolution: "1280,768",
    });

    onMounted(() => {
      setCurrentPageTitle("Studio");
      state.mounted = true;
    });

    const data = ref<Filter>({
      status: "1",
      author: true,
      customer: true,
      notifications: true,
    });

    return {
      status,
      currentStatus,
      state,
    };
  },

  methods: {
    // iconSize() {
    //   return [this.iconWidth, this.iconHeight];
    // },
    // iconUrl() {
    //   return `https://placekitten.com/${this.iconWidth}/${this.iconHeight}`;
    // },
  },
});
</script>

