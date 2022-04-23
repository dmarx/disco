<template>
  <div class="card" :class="widgetClasses">
    <!--begin::Header-->
    <div class="card-header border-0 pt-5">
      <h3 class="card-title align-items-start flex-column">
        <span class="card-label fw-bolder fs-3 mb-1">Published Files</span>
        <span class="text-muted mt-1 fw-bold fs-7"
          >Showing all uploaded files</span
        >
      </h3>
      <div class="card-toolbar">
        <ul class="nav">
          <li class="nav-item">
            <a
              class="nav-link btn btn-sm btn-color-muted btn-active btn-active-light-primary fw-bolder px-4 me-1 active"
              data-bs-toggle="tab"
              href="#kt_table_widget_5_tab_1"
              >Successful (10)</a
            >
          </li>
          <li class="nav-item">
            <a
              class="nav-link btn btn-sm btn-color-muted btn-active btn-active-light-primary fw-bolder px-4 me-1"
              data-bs-toggle="tab"
              href="#kt_table_widget_5_tab_1"
              >Processing (0)</a
            >
          </li>
          <li class="nav-item">
            <a
              class="nav-link btn btn-sm btn-color-muted btn-active btn-active-light-primary fw-bolder px-4"
              data-bs-toggle="tab"
              href="#kt_table_widget_5_tab_1"
              >Failed (0)</a
            >
          </li>
        </ul>
      </div>
    </div>
    <!--end::Header-->
    <!--begin::Body-->
    <div class="card-body py-3">
      <div class="tab-content">
        <!--begin::Tap pane-->
        <div class="tab-pane fade active show" id="kt_table_widget_5_tab_1">
          <!--begin::Table container-->
          <div class="table-responsive">
            <!--begin::Table-->
            <table
              class="table table-row-dashed table-row-gray-200 align-middle gs-0 gy-4"
            >
              <!--begin::Table head-->
              <thead>
                <tr class="border-0">
                  <th class="p-0 w-50px">Type</th>
                  <th class="p-0 min-w-150px">Name</th>
                  <th class="p-0 min-w-140px">Source</th>
                  <th class="p-0 min-w-110px">Dates / Times</th>
                  <th class="p-0 min-w-50px">Record Count</th>
                  <th class="p-0 min-w-50px">Status</th>
                  <th class="p-0 min-w-50px"></th>
                </tr>
              </thead>
              <!--end::Table head-->
              <!--begin::Table body-->
              <tbody>
                <tr>
                  <td>
                    <div class="symbol symbol-45px me-2">
                      <span class="symbol-label">
                        <i class="align-self-center bi bi-telephone-forward-fill"></i>
                    
                      </span>
                    </div>
                  </td>
                  <td>
                    <a
                      href="#"
                      class="text-dark fw-bolder text-hover-primary mb-1 fs-6"
                      >Unknown-T-mobile-334-220-917.xls</a
                    >
                    <span class="text-muted fw-bold d-block"
                      >Call Data Record (CDR)</span
                    >
                  </td>
                  <td class=" text-muted fw-bold">T-Mobile United States</td>
                  <td class=" text-muted fw-bold">30-12-2021 - 31-12-2021</td>
                  <td class=" text-muted fw-bold">420</td>
                  <td class="">
                    <span class="badge badge-light-success">Approved</span>
                  </td>
                  <td class="text-end">
                    <a
                      href="#"
                      class="btn btn-sm btn-icon btn-bg-light btn-active-color-primary"
                    >
                      <!--begin::Svg Icon | path: -->
                      <router-link to="/case/contents/preview">
                      <span class="svg-icon svg-icon-2" >
                        <inline-svg
                          src="media/icons/duotune/arrows/arr064.svg"
                        />
                      </span></router-link>
                      <!--end::Svg Icon-->
                    </a>
                  </td>
                </tr>
           
            <tr>
                  <td>
                    <div class="symbol symbol-45px me-2">
                      <span class="symbol-label">
                        <i class="align-self-center bi bi-telephone-forward-fill"></i>
                    
                      </span>
                    </div>
                  </td>
                  <td>
                    <a
                      href="#"
                      class="text-dark fw-bolder text-hover-primary mb-1 fs-6"
                      >Unknown-T-mobile-334-220-917.xls</a
                    >
                    <span class="text-muted fw-bold d-block"
                      >Call Data Record (CDR)</span
                    >
                  </td>
                  <td class=" text-muted fw-bold">T-Mobile United States</td>
                  <td class=" text-muted fw-bold">30-12-2021 - 31-12-2021</td>
                  <td class=" text-muted fw-bold">420</td>
                  <td class="">
                    <span class="badge badge-light-success">Approved</span>
                  </td>
                  <td class="text-end">
                    <a
                      href="#"
                      class="btn btn-sm btn-icon btn-bg-light btn-active-color-primary"
                    >
                      <!--begin::Svg Icon | path: -->
                      <span class="svg-icon svg-icon-2">
                        <inline-svg
                          src="media/icons/duotune/arrows/arr064.svg"
                        />
                      </span>
                      <!--end::Svg Icon-->
                    </a>
                  </td>
                </tr>

                 <tr>
                  <td>
                    <div class="symbol symbol-45px me-2">
                      <span class="symbol-label">
                        <i class="align-self-center bi bi-telephone-forward-fill"></i>
                    
                      </span>
                    </div>
                  </td>
                  <td>
                    <a
                      href="#"
                      class="text-dark fw-bolder text-hover-primary mb-1 fs-6"
                      >Unknown-T-mobile-334-220-917.xls</a
                    >
                    <span class="text-muted fw-bold d-block"
                      >Call Data Record (CDR)</span
                    >
                  </td>
                  <td class=" text-muted fw-bold">T-Mobile United States</td>
                  <td class=" text-muted fw-bold">30-12-2021 - 31-12-2021</td>
                  <td class=" text-muted fw-bold">420</td>
                  <td class="">
                    <span class="badge badge-light-success">Approved</span>
                  </td>
                  <td class="text-end">
                    <a
                      href="#"
                      class="btn btn-sm btn-icon btn-bg-light btn-active-color-primary"
                    >
                      <!--begin::Svg Icon | path: -->
                      <span class="svg-icon svg-icon-2">
                        <inline-svg
                          src="media/icons/duotune/arrows/arr064.svg"
                        />
                      </span>
                      <!--end::Svg Icon-->
                    </a>
                  </td>
                </tr>

                 <tr>
                  <td>
                    <div class="symbol symbol-45px me-2">
                      <span class="symbol-label">
                        <i class="align-self-center bi bi-telephone-forward-fill"></i>
                    
                      </span>
                    </div>
                  </td>
                  <td>
                    <a
                      href="#"
                      class="text-dark fw-bolder text-hover-primary mb-1 fs-6"
                      >Unknown-T-mobile-334-220-917.xls</a
                    >
                    <span class="text-muted fw-bold d-block"
                      >Call Data Record (CDR)</span
                    >
                  </td>
                  <td class=" text-muted fw-bold">T-Mobile United States</td>
                  <td class=" text-muted fw-bold">30-12-2021 - 31-12-2021</td>
                  <td class=" text-muted fw-bold">420</td>
                  <td class="">
                    <span class="badge badge-light-success">Approved</span>
                  </td>
                  <td class="text-end">
                    <a
                      href="#"
                      class="btn btn-sm btn-icon btn-bg-light btn-active-color-primary"
                    >
                      <!--begin::Svg Icon | path: -->
                      <span class="svg-icon svg-icon-2">
                        <inline-svg
                          src="media/icons/duotune/arrows/arr064.svg"
                        />
                      </span>
                      <!--end::Svg Icon-->
                    </a>
                  </td>
                </tr>

                 <tr>
                  <td>
                    <div class="symbol symbol-45px me-2">
                      <span class="symbol-label">
                        <i class="align-self-center bi bi-telephone-forward-fill"></i>
                    
                      </span>
                    </div>
                  </td>
                  <td>
                    <a
                      href="#"
                      class="text-dark fw-bolder text-hover-primary mb-1 fs-6"
                      >Unknown-T-mobile-334-220-917.xls</a
                    >
                    <span class="text-muted fw-bold d-block"
                      >Call Data Record (CDR)</span
                    >
                  </td>
                  <td class=" text-muted fw-bold">T-Mobile United States</td>
                  <td class=" text-muted fw-bold">30-12-2021 - 31-12-2021</td>
                  <td class=" text-muted fw-bold">420</td>
                  <td class="">
                    <span class="badge badge-light-success">Approved</span>
                  </td>
                  <td class="text-end">
                    <a
                      href="#"
                      class="btn btn-sm btn-icon btn-bg-light btn-active-color-primary"
                    >
                      <!--begin::Svg Icon | path: -->
                      <span class="svg-icon svg-icon-2">
                        <inline-svg
                          src="media/icons/duotune/arrows/arr064.svg"
                        />
                      </span>
                      <!--end::Svg Icon-->
                    </a>
                  </td>
                </tr>

                 <tr>
                  <td>
                    <div class="symbol symbol-45px me-2">
                      <span class="symbol-label">
                        <i class="align-self-center bi bi-telephone-forward-fill"></i>
                    
                      </span>
                    </div>
                  </td>
                  <td>
                    <a
                      href="#"
                      class="text-dark fw-bolder text-hover-primary mb-1 fs-6"
                      >Unknown-T-mobile-334-220-917.xls</a
                    >
                    <span class="text-muted fw-bold d-block"
                      >Call Data Record (CDR)</span
                    >
                  </td>
                  <td class=" text-muted fw-bold">T-Mobile United States</td>
                  <td class=" text-muted fw-bold">30-12-2021 - 31-12-2021</td>
                  <td class=" text-muted fw-bold">420</td>
                  <td class="">
                    <span class="badge badge-light-success">Approved</span>
                  </td>
                  <td class="text-end">
                    <a
                      href="#"
                      class="btn btn-sm btn-icon btn-bg-light btn-active-color-primary"
                    >
                      <!--begin::Svg Icon | path: -->
                      <span class="svg-icon svg-icon-2">
                        <inline-svg
                          src="media/icons/duotune/arrows/arr064.svg"
                        />
                      </span>
                      <!--end::Svg Icon-->
                    </a>
                  </td>
                </tr>

                 <tr>
                  <td>
                    <div class="symbol symbol-45px me-2">
                      <span class="symbol-label">
                        <i class="align-self-center bi bi-telephone-forward-fill"></i>
                    
                      </span>
                    </div>
                  </td>
                  <td>
                    <a
                      href="#"
                      class="text-dark fw-bolder text-hover-primary mb-1 fs-6"
                      >Unknown-T-mobile-334-220-917.xls</a
                    >
                    <span class="text-muted fw-bold d-block"
                      >Call Data Record (CDR)</span
                    >
                  </td>
                  <td class=" text-muted fw-bold">T-Mobile United States</td>
                  <td class=" text-muted fw-bold">30-12-2021 - 31-12-2021</td>
                  <td class=" text-muted fw-bold">420</td>
                  <td class="">
                    <span class="badge badge-light-success">Approved</span>
                  </td>
                  <td class="text-end">
                    <a
                      href="#"
                      class="btn btn-sm btn-icon btn-bg-light btn-active-color-primary"
                    >
                      <!--begin::Svg Icon | path: -->
                      <span class="svg-icon svg-icon-2">
                        <inline-svg
                          src="media/icons/duotune/arrows/arr064.svg"
                        />
                      </span>
                      <!--end::Svg Icon-->
                    </a>
                  </td>
                </tr>

                 <tr>
                  <td>
                    <div class="symbol symbol-45px me-2">
                      <span class="symbol-label">
                        <i class="align-self-center bi bi-telephone-forward-fill"></i>
                    
                      </span>
                    </div>
                  </td>
                  <td>
                    <a
                      href="#"
                      class="text-dark fw-bolder text-hover-primary mb-1 fs-6"
                      >Unknown-T-mobile-334-220-917.xls</a
                    >
                    <span class="text-muted fw-bold d-block"
                      >Call Data Record (CDR)</span
                    >
                  </td>
                  <td class=" text-muted fw-bold">T-Mobile United States</td>
                  <td class=" text-muted fw-bold">30-12-2021 - 31-12-2021</td>
                  <td class=" text-muted fw-bold">420</td>
                  <td class="">
                    <span class="badge badge-light-success">Approved</span>
                  </td>
                  <td class="text-end">
                    <a
                      href="#"
                      class="btn btn-sm btn-icon btn-bg-light btn-active-color-primary"
                    >
                      <!--begin::Svg Icon | path: -->
                      <span class="svg-icon svg-icon-2">
                        <inline-svg
                          src="media/icons/duotune/arrows/arr064.svg"
                        />
                      </span>
                      <!--end::Svg Icon-->
                    </a>
                  </td>
                </tr>

                 <tr>
                  <td>
                    <div class="symbol symbol-45px me-2">
                      <span class="symbol-label">
                        <i class="align-self-center bi bi-telephone-forward-fill"></i>
                    
                      </span>
                    </div>
                  </td>
                  <td>
                    <a
                      href="#"
                      class="text-dark fw-bolder text-hover-primary mb-1 fs-6"
                      >Unknown-T-mobile-334-220-917.xls</a
                    >
                    <span class="text-muted fw-bold d-block"
                      >Call Data Record (CDR)</span
                    >
                  </td>
                  <td class=" text-muted fw-bold">T-Mobile United States</td>
                  <td class=" text-muted fw-bold">30-12-2021 - 31-12-2021</td>
                  <td class=" text-muted fw-bold">420</td>
                  <td class="">
                    <span class="badge badge-light-success">Approved</span>
                  </td>
                  <td class="text-end">
                    <a
                      href="#"
                      class="btn btn-sm btn-icon btn-bg-light btn-active-color-primary"
                    >
                      <!--begin::Svg Icon | path: -->
                      <span class="svg-icon svg-icon-2">
                        <inline-svg
                          src="media/icons/duotune/arrows/arr064.svg"
                        />
                      </span>
                      <!--end::Svg Icon-->
                    </a>
                  </td>
                </tr>
              </tbody>
              <!--end::Table body-->
            </table>
          </div>
          <!--end::Table-->
        </div>
      </div>
    </div>
    <!--end::Body-->
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "kt-widget-5",
  components: {},
  props: {
    widgetClasses: String,
  },
});
</script>
