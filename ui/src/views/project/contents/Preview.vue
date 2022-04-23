<template>
  <div v-if="state.mounted">
    <Teleport to="#aside-context">
      <el-form @submit.prevent="submit()" :model="formData" :rules="rules" ref="formRef">
        <div class="menu-item">
          <div class="menu-content pt-8 pb-2">
            <span class="menu-section text-muted text-uppercase fs-8 ls-1">EVENT FILTERS</span>
          </div>
          <!-- <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-code-square fs-2x"></i>
          </span>
          <span class="menu-title">All events &amp; locations</span>
          </span>-->
        </div>

        <div class="accordion" id="kt_accordion_1">
          <div class="accordion-item">
            <h2 class="accordion-header" id="kt_accordion_1_header_1">
              <button
                class="accordion-button fw-bold"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#kt_accordion_1_body_1"
                aria-expanded="true"
                aria-controls="kt_accordion_1_body_1"
              >Keyword</button>
            </h2>
            <div
              id="kt_accordion_1_body_1"
              class="accordion-collapse collapse show"
              aria-labelledby="kt_accordion_1_header_1"
            >
              <div class="accordion-body">
                <input
                  type="text"
                  class="form-control form-control form-control-solid"
                  name="city"
                  style="background-image: url(&quot;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABHklEQVQ4EaVTO26DQBD1ohQWaS2lg9JybZ+AK7hNwx2oIoVf4UPQ0Lj1FdKktevIpel8AKNUkDcWMxpgSaIEaTVv3sx7uztiTdu2s/98DywOw3Dued4Who/M2aIx5lZV1aEsy0+qiwHELyi+Ytl0PQ69SxAxkWIA4RMRTdNsKE59juMcuZd6xIAFeZ6fGCdJ8kY4y7KAuTRNGd7jyEBXsdOPE3a0QGPsniOnnYMO67LgSQN9T41F2QGrQRRFCwyzoIF2qyBuKKbcOgPXdVeY9rMWgNsjf9ccYesJhk3f5dYT1HX9gR0LLQR30TnjkUEcx2uIuS4RnI+aj6sJR0AM8AaumPaM/rRehyWhXqbFAA9kh3/8/NvHxAYGAsZ/il8IalkCLBfNVAAAAABJRU5ErkJggg==&quot;); background-repeat: no-repeat; background-attachment: scroll; background-size: 16px 18px; background-position: 98% 50%; cursor: auto;"
                />
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header" id="kt_accordion_1_header_1d">
              <button
                class="accordion-button fw-bold collapsed"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#kt_accordion_1_body_1d"
                aria-expanded="true"
                aria-controls="kt_accordion_1_body_1d"
              >Date Range</button>
            </h2>
            <div
              id="kt_accordion_1_body_1d"
              class="accordion-collapse collapse"
              aria-labelledby="kt_accordion_1_header_1d"
            >
              <div class="accordion-body">
                <el-form-item prop="name">
                  <el-date-picker type="daterange" v-model="formData.dateRange"></el-date-picker>
                </el-form-item>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header" id="kt_accordion_1_header_2">
              <button
                class="accordion-button fw-bold collapsed"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#kt_accordion_1_body_2"
                aria-expanded="false"
                aria-controls="kt_accordion_1_body_2"
              >Type</button>
            </h2>
            <div
              id="kt_accordion_1_body_2"
              class="accordion-collapse collapse"
              aria-labelledby="kt_accordion_1_header_2"
            >
              <div class="accordion-body">
                <div>
                  <el-select class="form-select-solid" placeholder="Select option">
                    <el-option label="Approved" value="1">All Events</el-option>
                    <el-option label="Pending" value="2">Call</el-option>
                    <el-option label="In Process" value="3">Text</el-option>
                    <el-option label="Rejected" value="4">Chat Message</el-option>
                  </el-select>
                </div>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header" id="kt_accordion_1_header_3">
              <button
                class="accordion-button fw-bold collapsed"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#kt_accordion_1_body_3"
                aria-expanded="false"
                aria-controls="kt_accordion_1_body_3"
              >Subject</button>
            </h2>
            <div
              id="kt_accordion_1_body_3"
              class="accordion-collapse collapse"
              aria-labelledby="kt_accordion_1_header_3"
            >
              <div class="accordion-body">
                <div>
                  <el-select class="form-select-solid" placeholder="Select option">
                    <el-option label="Approved" value="1">Subject 1</el-option>
                    <el-option label="Pending" value="2">Subject 2</el-option>
                    <el-option label="In Process" value="3">Subject 3</el-option>
                    <el-option label="Rejected" value="4">Subject 4</el-option>
                  </el-select>
                </div>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header" id="kt_accordion_1_header_4">
              <button
                class="accordion-button fw-bold collapsed"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#kt_accordion_1_body_4"
                aria-expanded="false"
                aria-controls="kt_accordion_1_body_4"
              >Approx. Age</button>
            </h2>
            <div
              id="kt_accordion_1_body_4"
              class="accordion-collapse collapse"
              aria-labelledby="kt_accordion_1_header_4"
            >
              <div class="accordion-body">
                <div
                  class="position-relative"
                  data-kt-dialer="true"
                  data-kt-dialer-min="1"
                  data-kt-dialer-max="100"
                  data-kt-dialer-step="1000"
                  data-kt-dialer-prefix
                  data-kt-dialer-decimals="2"
                >
                  <!--begin::Decrease control-->
                  <button
                    type="button"
                    class="btn btn-icon btn-active-color-gray-700 position-absolute translate-middle-y top-50 start-0"
                    data-kt-dialer-control="decrease"
                  >
                    <!--begin::Svg Icon | path: icons/duotune/general/gen042.svg-->
                    <span class="svg-icon svg-icon-1">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                      >
                        <rect
                          opacity="0.3"
                          x="2"
                          y="2"
                          width="20"
                          height="20"
                          rx="10"
                          fill="black"
                        />
                        <rect x="6.01041" y="10.9247" width="12" height="2" rx="1" fill="black" />
                      </svg>
                    </span>
                    <!--end::Svg Icon-->
                  </button>
                  <!--end::Decrease control-->
                  <!--begin::Input control-->
                  <input
                    type="text"
                    class="form-control form-control-solid border-0 ps-12"
                    data-kt-dialer-control="input"
                    placeholder="Amount"
                    name="manageBudget"
                    readonly="readonly"
                    value="$50"
                  />
                  <!--end::Input control-->
                  <!--begin::Increase control-->
                  <button
                    type="button"
                    class="btn btn-icon btn-active-color-gray-700 position-absolute translate-middle-y top-50 end-0"
                    data-kt-dialer-control="increase"
                  >
                    <!--begin::Svg Icon | path: icons/duotune/general/gen041.svg-->
                    <span class="svg-icon svg-icon-1">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                      >
                        <rect
                          opacity="0.3"
                          x="2"
                          y="2"
                          width="20"
                          height="20"
                          rx="10"
                          fill="black"
                        />
                        <rect
                          x="10.8891"
                          y="17.8033"
                          width="12"
                          height="2"
                          rx="1"
                          transform="rotate(-90 10.8891 17.8033)"
                          fill="black"
                        />
                        <rect x="6.01041" y="10.9247" width="12" height="2" rx="1" fill="black" />
                      </svg>
                    </span>
                    <!--end::Svg Icon-->
                  </button>
                  <!--end::Increase control-->
                </div>
              </div>
            </div>
          </div>

          <div class="accordion-item">
            <h2 class="accordion-header" id="kt_accordion_1_header_6">
              <button
                class="accordion-button fw-bold collapsed"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#kt_accordion_1_body_6"
                aria-expanded="false"
                aria-controls="kt_accordion_1_body_6"
              >Location</button>
            </h2>
            <div
              id="kt_accordion_1_body_6"
              class="accordion-collapse collapse"
              aria-labelledby="kt_accordion_1_header_6"
            >
              <div class="accordion-body">
                <input
                  type="text"
                  class="form-control form-control form-control-solid"
                  name="city"
                  style="background-image: url(&quot;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABHklEQVQ4EaVTO26DQBD1ohQWaS2lg9JybZ+AK7hNwx2oIoVf4UPQ0Lj1FdKktevIpel8AKNUkDcWMxpgSaIEaTVv3sx7uztiTdu2s/98DywOw3Dued4Who/M2aIx5lZV1aEsy0+qiwHELyi+Ytl0PQ69SxAxkWIA4RMRTdNsKE59juMcuZd6xIAFeZ6fGCdJ8kY4y7KAuTRNGd7jyEBXsdOPE3a0QGPsniOnnYMO67LgSQN9T41F2QGrQRRFCwyzoIF2qyBuKKbcOgPXdVeY9rMWgNsjf9ccYesJhk3f5dYT1HX9gR0LLQR30TnjkUEcx2uIuS4RnI+aj6sJR0AM8AaumPaM/rRehyWhXqbFAA9kh3/8/NvHxAYGAsZ/il8IalkCLBfNVAAAAABJRU5ErkJggg==&quot;); background-repeat: no-repeat; background-attachment: scroll; background-size: 16px 18px; background-position: 98% 50%; cursor: auto;"
                />
              </div>
            </div>
          </div>
        </div>
      </el-form>
      <br />
      <!--end::Input group-->
      <!--begin::Action-->
      <div class="d-flex align-items-center justify-content-end" style="margin-right:15px;">
        <a href="#" class="btn btn-active-light-primary btn-color-gray-400 me-3">Discard</a>
        <button @click="submit();" class="btn btn-primary">Search</button>
      </div>

      <div class="menu-item">
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">Actions</span>
        </div>
        <a class="menu-link" href="/#/case/contents">
          <span class="menu-icon">
            <i class="bi bi-card-text fs-3"></i>
          </span>
          <span class="menu-title">Back to Case Contents</span>
        </a>
      </div>
    </Teleport>
  </div>
  <div class="row g-5 gx-xxl-8">
    <div class="col-xxl-12">
      <CardEvents></CardEvents>
    </div>
  </div>
  <!--end::Dashboard-->
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, toRefs } from "vue";
import Contents from "@/components/widgets/tables/Contents.vue";
import { setCurrentPageTitle } from "@/core/helpers/breadcrumb";
import { reactive } from 'vue';
import { setCurrentPageBreadcrumbs } from "@/core/helpers/breadcrumb";
import Dropdown2 from "@/components/dropdown/Dropdown2.vue";
import CardEvents from "@/components/cards/CardEvents.vue";
import Swal from "sweetalert2/dist/sweetalert2.js";

export default defineComponent({
  name: "preview",
  components: {
    Contents,
    Dropdown2,
    CardEvents
  },
  setup() {
    const formRef = ref<null | HTMLFormElement>(null);
    const loading = ref<boolean>(false);
    const state = reactive({ count: 0, mounted: false })
    onMounted(() => {
      setCurrentPageBreadcrumbs("Preview", ["Contents"]);
      // setCurrentPageTitle("Preview");
      state.mounted = true;
    });


    const formData = ref({
      dateRange: [],
      exportFormat: "",
      paymentType: "",
    });

    const rules = ref({
      dateRange: [
        {
          required: true,
          message: "Date range is required",
          trigger: "change",
        },
      ],
    });

    const submit = () => {
      if (!formRef.value) {
        return;
      }

      formRef.value.validate((valid) => {
        if (valid) {
          loading.value = true;

          setTimeout(() => {
            loading.value = false;

            Swal.fire({
              text: "Form has been successfully submitted!",
              icon: "success",
              buttonsStyling: false,
              confirmButtonText: "Ok, got it!",
              customClass: {
                confirmButton: "btn btn-primary",
              },
            }).then(() => {
              //window.location.reload();
            });
          }, 250);
        } else {
          Swal.fire({
            text: "Sorry, looks like there are some errors detected, please try again.",
            icon: "error",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
              confirmButton: "btn btn-primary",
            },
          });
          return false;
        }
      });
    };



    return {
      ...toRefs(state),
      state,
      formData,
      rules,
      submit,
      formRef,
      loading,
    }
  },
});
</script>
<style lang="scss">
.accordion-body .form-control.form-control-solid {
  padding: 8px;
  background-color: #20478f;
  border-color: #556687;
  color: #5e6278;
}
.accordion-button {
  padding: 8px 22px;
}
.accordion-item {
  background-color: transparent;
  border: none;
}
.accordion-button {
  background-color: transparent;
  color: #fff;
}

.el-date-editor--daterange.el-input__inner {
  width: 100%;
  font-size:11px;
}
.el-date-editor--daterange {
  width: 100% !important;
}

.accordion-button:not(.collapsed) {
    color: #FFF;
    background-color: transparent;
    box-shadow: inset 0 -1px 0 #eff2f5;
}
</style>