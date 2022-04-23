<template>
  <div class="menu-item">
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">SEARCH FILTERS</span>
        </div>
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
            >Location</button>
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
          <h2 class="accordion-header" id="kt_accordion_1_header_2">
            <button
              class="accordion-button fw-bold collapsed"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#kt_accordion_1_body_2"
              aria-expanded="false"
              aria-controls="kt_accordion_1_body_2"
            >Gender</button>
          </h2>
          <div
            id="kt_accordion_1_body_2"
            class="accordion-collapse collapse"
            aria-labelledby="kt_accordion_1_header_2"
          >
            <div class="accordion-body">
              <div>
                <el-select
                  class="form-select-solid"
                  placeholder="Select option"
                  v-model="data.status"
                >
                  <el-option label="Approved" value="1">Approved</el-option>
                  <el-option label="Pending" value="2">Pending</el-option>
                  <el-option label="In Process" value="3">In Process</el-option>
                  <el-option label="Rejected" value="4">Rejected</el-option>
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
            >Approx. Age</button>
          </h2>
          <div
            id="kt_accordion_1_body_3"
            class="accordion-collapse collapse"
            aria-labelledby="kt_accordion_1_header_3"
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
                      <rect opacity="0.3" x="2" y="2" width="20" height="20" rx="10" fill="black" />
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
                  value="50"
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
                      <rect opacity="0.3" x="2" y="2" width="20" height="20" rx="10" fill="black" />
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
          <h2 class="accordion-header" id="kt_accordion_1_header_4">
            <button
              class="accordion-button fw-bold collapsed"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#kt_accordion_1_body_4"
              aria-expanded="false"
              aria-controls="kt_accordion_1_body_4"
            >Vehicle Reg No.</button>
          </h2>
          <div
            id="kt_accordion_1_body_4"
            class="accordion-collapse collapse"
            aria-labelledby="kt_accordion_1_header_4"
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
          <h2 class="accordion-header" id="kt_accordion_1_header_5">
            <button
              class="accordion-button fw-bold collapsed"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#kt_accordion_1_body_5"
              aria-expanded="false"
              aria-controls="kt_accordion_1_body_5"
            >Vehicle Make</button>
          </h2>
          <div
            id="kt_accordion_1_body_5"
            class="accordion-collapse collapse"
            aria-labelledby="kt_accordion_1_header_5"
          >
            <div class="accordion-body">
              <div class="form-check form-check-custom form-check-solid mb-5">
                <input class="form-check-input" type="checkbox" id="kt_search_category_1" />
                <label
                  class="form-check-label flex-grow-1 fw-bold text-gray-700 fs-6"
                  for="kt_search_category_1"
                >Fraud</label>
                <span class="text-gray-400 fw-bolder">28</span>
              </div>
              <!--end::Checkbox-->
              <!--begin::Checkbox-->
              <div class="form-check form-check-custom form-check-solid mb-5">
                <input
                  class="form-check-input"
                  type="checkbox"
                  id="kt_search_category_2"
                  checked="checked"
                />
                <label
                  class="form-check-label flex-grow-1 fw-bold text-gray-700 fs-6"
                  for="kt_search_category_2"
                >Theft</label>
                <span class="text-gray-400 fw-bolder">307</span>
              </div>
              <!--end::Checkbox-->
              <!--begin::Checkbox-->
              <div class="form-check form-check-custom form-check-solid">
                <input class="form-check-input" type="checkbox" id="kt_search_category_3" />
                <label
                  class="form-check-label flex-grow-1 fw-bold text-gray-700 fs-6"
                  for="kt_search_category_3"
                >Assault</label>
                <span class="text-gray-400 fw-bolder">54</span>
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
            >Vehicle Model.</button>
          </h2>
          <div
            id="kt_accordion_1_body_6"
            class="accordion-collapse collapse"
            aria-labelledby="kt_accordion_1_header_6"
          >
            <div class="accordion-body">
              <div class="nav-group nav-group-fluid">
                <label>
                  <input type="radio" class="btn-check" name="type" value="has" checked="checked" />
                  <span
                    class="btn btn-sm btn-color-muted btn-active btn-active-primary fw-bolder px-4"
                  >1-5</span>
                </label>
                <label>
                  <input type="radio" class="btn-check" name="type" value="users" />
                  <span
                    class="btn btn-sm btn-color-muted btn-active btn-active-primary fw-bolder px-4"
                  >5-10</span>
                </label>
                <label>
                  <input type="radio" class="btn-check" name="type" value="orders" />
                  <span
                    class="btn btn-sm btn-color-muted btn-active btn-active-primary fw-bolder px-4"
                  >10++</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <br />
      <!--end::Input group-->
      <!--begin::Action-->
      <div class="d-flex align-items-center justify-content-end" style="margin-right:15px;">
        <a href="#" class="btn btn-active-light-primary btn-color-gray-400 me-3">Discard</a>
        <a href="#" class="btn btn-primary">Search</a>
      </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

interface Filter {
  status: string;
  author: boolean;
  customer: boolean;
  notifications: boolean;
  keyword: string;
}

export default defineComponent({
  name: "search_filters",
  components: {
  },
  props: {
    widgetClasses: String,
  },
  setup() {
      const data = ref<Filter>({
      status: "1",
      author: true,
      customer: true,
      notifications: true,
      keyword: ""
    });

    return {
    data
    };
  },
});
</script>
