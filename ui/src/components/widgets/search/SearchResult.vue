<template>
   <div class="card mb-5 mb-xl-8">
        <!--begin::Card body-->
        <div class="card-body pt-15">
          <!--begin::Summary-->
          <div class="row">
            <div class="col-12">
              <div class="row">
                <div class="col-4">
                  <div class="row">
                    <div class="col-4">
                      <div class="symbol symbol-circle mb-7" style="width:64px">
                        <img src="media/avatars/300-1.jpg" alt="image" />
                      </div>
                    </div>
                    <div class="col-8">
                      <a href="#" class="fs-3 text-gray-800 text-hover-primary fw-bolder mb-1">
                        Max Smith
                        <br />
                        <span style="color:#999;font-size:14px;">Person</span>
                      </a>
                    </div>
                  </div>
                </div>
                <div class="col-4">
                  <!--begin::Stats-->
                  <div
                    class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3"
                    style="display:inline-block"
                  >
                    <div class="fs-4 fw-bolder text-gray-700">
                      <span class="w-75px">6,900</span>
                      <span class="svg-icon svg-icon-3 svg-icon-success">
                        <inline-svg src="media/icons/duotune/arrows/arr066.svg" />
                      </span>
                    </div>
                    <div class="fw-bold text-muted">Earnings</div>
                  </div>
                  <!--end::Stats-->

                  <!--begin::Stats-->
                  <div
                    class="border border-gray-300 border-dashed rounded py-3 px-3 mx-4 mb-3"
                    style="display:inline-block"
                  >
                    <div class="fs-4 fw-bolder text-gray-700">
                      <span class="w-50px">130</span>
                      <span class="svg-icon svg-icon-3 svg-icon-danger">
                        <inline-svg src="media/icons/duotune/arrows/arr065.svg" />
                      </span>
                    </div>
                    <div class="fw-bold text-muted">Tasks</div>
                  </div>
                  <!--end::Stats-->

                  <!--begin::Stats-->
                  <div
                    class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3"
                    style="display:inline-block"
                  >
                    <div class="fs-4 fw-bolder text-gray-700">
                      <span class="w-50px">500</span>
                      <span class="svg-icon svg-icon-3 svg-icon-success">
                        <inline-svg src="media/icons/duotune/arrows/arr066.svg" />
                      </span>
                    </div>
                    <div class="fw-bold text-muted">Hours</div>
                  </div>
                </div>
                <div class="col-4" style="text-align:right">
                  <span
                    data-bs-toggle="tooltip"
                    data-bs-trigger="hover"
                    title="Edit customer details"
                  >
                    <a
                      href="#"
                      class="btn btn-sm btn-light-primary"
                      data-bs-toggle="modal"
                      data-bs-target="#kt_modal_update_customer"
                    >Edit</a>
                  </span>
                  <div
                    class="fw-bolder rotate collapsible"
                    data-bs-toggle="collapse"
                    href="#kt_customer_view_details"
                    role="button"
                    aria-expanded="false"
                    aria-controls="kt_customer_view_details"
                    style="margin-left: 16px;"
                  >
                    Details
                    <span class="ms-2 rotate-180">
                      <span class="svg-icon svg-icon-3">
                        <inline-svg src="media/icons/duotune/arrows/arr072.svg" />
                      </span>
                    </span>
                  </div>
                </div>
              </div>

              <!--end::Name-->

              <!--begin::Info-->

              <!--end::Info-->
              <div class="separator separator-dashed my-3"></div>

              <!--begin::Details content-->
              <div id="kt_customer_view_details" class="collapse show">
                <div class="py-5 fs-6">
                  <!--begin::Badge-->
                  <div class="badge badge-light-info d-inline">Attributes</div>
                  <!--begin::Badge-->
                  <!--begin::Details item-->
                  <div class="fw-bolder mt-5">Account ID</div>
                  <div class="text-gray-600">ID-45453423</div>
                  <!--begin::Details item-->
                  <!--begin::Details item-->
                  <div class="fw-bolder mt-5">Billing Email</div>
                  <div class="text-gray-600">
                    <a href="#" class="text-gray-600 text-hover-primary">info@keenthemes.com</a>
                  </div>
                  <!--begin::Details item-->
                  <!--begin::Details item-->
                  <div class="fw-bolder mt-5">Billing Address</div>
                  <div class="text-gray-600">
                    101 Collin Street,
                    <br />Melbourne 3000 VIC
                    <br />Australia
                  </div>
                  <!--begin::Details item-->
                  <!--begin::Details item-->
                  <div class="fw-bolder mt-5">Language</div>
                  <div class="text-gray-600">English</div>
                  <!--begin::Details item-->
                  <!--begin::Details item-->
                  <div class="fw-bolder mt-5">Upcoming Invoice</div>
                  <div class="text-gray-600">54238-8693</div>
                  <!--begin::Details item-->
                  <!--begin::Details item-->
                  <div class="fw-bolder mt-5">Tax ID</div>
                  <div class="text-gray-600">TX-8674</div>
                  <!--begin::Details item-->
                </div>
              </div>
            </div>
          </div>
          <!--end::Summary-->

          <!--begin::Details toggle-->

          <!--end::Details content-->
        </div>
        <!--end::Card body-->
      </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "search_result",
  components: {
  },
  props: {
    widgetClasses: String,
  },
  setup() {
    const items = [
      // {
      //   icon: "media/icons/duotune/abstract/abs027.svg",
      //   color: "success",
      //   title: "Project Briefing",
      //   description: "Project Manager",
      // },
      // {
      //   icon: "media/icons/duotune/art/art005.svg",
      //   color: "warning",
      //   title: "Concept Design",
      //   description: "Art Director",
      // },
      // {
      //   icon: "media/icons/duotune/communication/com012.svg",
      //   color: "primary",
      //   title: "Functional Logics",
      //   description: "Lead Developer",
      // },
      // {
      //   icon: "media/icons/duotune/coding/cod008.svg",
      //   color: "danger",
      //   title: "Development",
      //   description: "DevOps",
      // },
      // {
      //   icon: "media/icons/duotune/general/gen049.svg",
      //   color: "info",
      //   title: "Testing",
      //   description: "QA Managers",
      // },
    ];

    return {
      items,
    };
  },
});
</script>
