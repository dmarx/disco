<template>
    <div class="card card-flush">
        <!--begin::Card header-->
        <div class="card-header mt-6">
          <!--begin::Card title-->
          <div class="card-title flex-column">
            <h3 class="fw-bolder mb-1">My Tasks</h3>
            <div class="fs-6 text-gray-400">Total 7 tasks pending</div>
          </div>
          <!--end::Card title-->
          <!--begin::Card toolbar-->
          <div class="card-toolbar">
            <a href="#" class="btn btn-bg-light btn-active-color-primary btn-sm">View All</a>
          </div>
          <!--end::Card toolbar-->
        </div>
        <!--end::Card header-->
        <!--begin::Card body-->
        <div class="card-body d-flex flex-column mb-9 p-9 pt-3">
          <!--begin::Item-->
          <div class="d-flex align-items-center position-relative mb-7">
            <!--begin::Label-->
            <div class="position-absolute top-0 start-0 rounded h-100 bg-secondary w-4px"></div>
            <!--end::Label-->
            <!--begin::Checkbox-->
            <div class="form-check form-check-custom form-check-solid ms-6 me-4">
              <input class="form-check-input" type="checkbox" value />
            </div>
            <!--end::Checkbox-->
            <!--begin::Details-->
            <div class="fw-bold">
              <a
                href="#"
                class="fs-6 fw-bolder text-gray-900 text-hover-primary"
              >Request DVLA data for Subject A</a>
              <!--begin::Info-->
              <div class="text-gray-400">
                Due in 1 day
                <a href="#">Richard Helson</a>
              </div>
              <!--end::Info-->
            </div>
            <!--end::Details-->
            <!--begin::Menu-->
            <button
              type="button"
              class="btn btn-clean btn-sm btn-icon btn-icon-primary btn-active-light-primary ms-auto"
              data-kt-menu-trigger="click"
              data-kt-menu-placement="bottom-end"
            >
              <!--begin::Svg Icon | path: icons/duotune/general/gen024.svg-->
              <span class="svg-icon svg-icon-3">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24px"
                  height="24px"
                  viewBox="0 0 24 24"
                >
                  <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <rect x="5" y="5" width="5" height="5" rx="1" fill="#000000" />
                    <rect x="14" y="5" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                    <rect x="5" y="14" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                    <rect x="14" y="14" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                  </g>
                </svg>
              </span>
              <!--end::Svg Icon-->
            </button>
            <!--begin::Menu 1-->
            <div
              class="menu menu-sub menu-sub-dropdown w-250px w-md-300px"
              data-kt-menu="true"
              id="kt_menu_62051c572e5a6"
            >
              <!--begin::Header-->
              <div class="px-7 py-5">
                <div class="fs-5 text-dark fw-bolder">Filter Options</div>
              </div>
              <!--end::Header-->
              <!--begin::Menu separator-->
              <div class="separator border-gray-200"></div>
              <!--end::Menu separator-->
              <!--begin::Form-->
              <div class="px-7 py-5">
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Status:</label>
                  <!--end::Label-->
                  <!--begin::Input-->
                  <div>
                    <select
                      class="form-select form-select-solid select2-hidden-accessible"
                      data-kt-select2="true"
                      data-placeholder="Select option"
                      data-dropdown-parent="#kt_menu_62051c572e5a6"
                      data-allow-clear="true"
                      data-select2-id="select2-data-28-8zoy"
                      tabindex="-1"
                      aria-hidden="true"
                    >
                      <option data-select2-id="select2-data-30-80uh"></option>
                      <option value="1">Approved</option>
                      <option value="2">Pending</option>
                      <option value="2">In Process</option>
                      <option value="2">Rejected</option>
                    </select>
                    <span
                      class="select2 select2-container select2-container--bootstrap5"
                      dir="ltr"
                      data-select2-id="select2-data-29-ppa8"
                      style="width: 100%;"
                    >
                      <span class="selection">
                        <span
                          class="select2-selection select2-selection--single form-select form-select-solid"
                          role="combobox"
                          aria-haspopup="true"
                          aria-expanded="false"
                          tabindex="0"
                          aria-disabled="false"
                          aria-labelledby="select2-7asb-container"
                          aria-controls="select2-7asb-container"
                        >
                          <span
                            class="select2-selection__rendered"
                            id="select2-7asb-container"
                            role="textbox"
                            aria-readonly="true"
                            title="Select option"
                          >
                            <span class="select2-selection__placeholder">Select option</span>
                          </span>
                          <span class="select2-selection__arrow" role="presentation">
                            <b role="presentation"></b>
                          </span>
                        </span>
                      </span>
                      <span class="dropdown-wrapper" aria-hidden="true"></span>
                    </span>
                  </div>
                  <!--end::Input-->
                </div>
                <!--end::Input group-->
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Member Type:</label>
                  <!--end::Label-->
                  <!--begin::Options-->
                  <div class="d-flex">
                    <!--begin::Options-->
                    <label class="form-check form-check-sm form-check-custom form-check-solid me-5">
                      <input class="form-check-input" type="checkbox" value="1" />
                      <span class="form-check-label">Author</span>
                    </label>
                    <!--end::Options-->
                    <!--begin::Options-->
                    <label class="form-check form-check-sm form-check-custom form-check-solid">
                      <input class="form-check-input" type="checkbox" value="2" checked="checked" />
                      <span class="form-check-label">Customer</span>
                    </label>
                    <!--end::Options-->
                  </div>
                  <!--end::Options-->
                </div>
                <!--end::Input group-->
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Notifications:</label>
                  <!--end::Label-->
                  <!--begin::Switch-->
                  <div
                    class="form-check form-switch form-switch-sm form-check-custom form-check-solid"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      value
                      name="notifications"
                      checked="checked"
                    />
                    <label class="form-check-label">Enabled</label>
                  </div>
                  <!--end::Switch-->
                </div>
                <!--end::Input group-->
                <!--begin::Actions-->
                <div class="d-flex justify-content-end">
                  <button
                    type="reset"
                    class="btn btn-sm btn-light btn-active-light-primary me-2"
                    data-kt-menu-dismiss="true"
                  >Reset</button>
                  <button
                    type="submit"
                    class="btn btn-sm btn-primary"
                    data-kt-menu-dismiss="true"
                  >Apply</button>
                </div>
                <!--end::Actions-->
              </div>
              <!--end::Form-->
            </div>
            <!--end::Menu 1-->
            <!--end::Menu-->
          </div>
          <!--end::Item-->
          <!--begin::Item-->
          <div class="d-flex align-items-center position-relative mb-7">
            <!--begin::Label-->
            <div class="position-absolute top-0 start-0 rounded h-100 bg-secondary w-4px"></div>
            <!--end::Label-->
            <!--begin::Checkbox-->
            <div class="form-check form-check-custom form-check-solid ms-6 me-4">
              <input class="form-check-input" type="checkbox" value />
            </div>
            <!--end::Checkbox-->
            <!--begin::Details-->
            <div class="fw-bold">
              <a
                href="#"
                class="fs-6 fw-bolder text-gray-900 text-hover-primary"
              >Research OSINT data for Subject B</a>
              <!--begin::Info-->
              <div class="text-gray-400">
                Due in 3 days
                <a href="#">Richard Helson</a>
              </div>
              <!--end::Info-->
            </div>
            <!--end::Details-->
            <!--begin::Menu-->
            <button
              type="button"
              class="btn btn-clean btn-sm btn-icon btn-icon-primary btn-active-light-primary ms-auto"
              data-kt-menu-trigger="click"
              data-kt-menu-placement="bottom-end"
            >
              <!--begin::Svg Icon | path: icons/duotune/general/gen024.svg-->
              <span class="svg-icon svg-icon-3">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24px"
                  height="24px"
                  viewBox="0 0 24 24"
                >
                  <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <rect x="5" y="5" width="5" height="5" rx="1" fill="#000000" />
                    <rect x="14" y="5" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                    <rect x="5" y="14" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                    <rect x="14" y="14" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                  </g>
                </svg>
              </span>
              <!--end::Svg Icon-->
            </button>
            <!--begin::Menu 1-->
            <div
              class="menu menu-sub menu-sub-dropdown w-250px w-md-300px"
              data-kt-menu="true"
              id="kt_menu_62051c572e60b"
            >
              <!--begin::Header-->
              <div class="px-7 py-5">
                <div class="fs-5 text-dark fw-bolder">Filter Options</div>
              </div>
              <!--end::Header-->
              <!--begin::Menu separator-->
              <div class="separator border-gray-200"></div>
              <!--end::Menu separator-->
              <!--begin::Form-->
              <div class="px-7 py-5">
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Status:</label>
                  <!--end::Label-->
                  <!--begin::Input-->
                  <div>
                    <select
                      class="form-select form-select-solid select2-hidden-accessible"
                      data-kt-select2="true"
                      data-placeholder="Select option"
                      data-dropdown-parent="#kt_menu_62051c572e60b"
                      data-allow-clear="true"
                      data-select2-id="select2-data-31-xdcv"
                      tabindex="-1"
                      aria-hidden="true"
                    >
                      <option data-select2-id="select2-data-33-yatj"></option>
                      <option value="1">Approved</option>
                      <option value="2">Pending</option>
                      <option value="2">In Process</option>
                      <option value="2">Rejected</option>
                    </select>
                    <span
                      class="select2 select2-container select2-container--bootstrap5"
                      dir="ltr"
                      data-select2-id="select2-data-32-bgzv"
                      style="width: 100%;"
                    >
                      <span class="selection">
                        <span
                          class="select2-selection select2-selection--single form-select form-select-solid"
                          role="combobox"
                          aria-haspopup="true"
                          aria-expanded="false"
                          tabindex="0"
                          aria-disabled="false"
                          aria-labelledby="select2-ds5a-container"
                          aria-controls="select2-ds5a-container"
                        >
                          <span
                            class="select2-selection__rendered"
                            id="select2-ds5a-container"
                            role="textbox"
                            aria-readonly="true"
                            title="Select option"
                          >
                            <span class="select2-selection__placeholder">Select option</span>
                          </span>
                          <span class="select2-selection__arrow" role="presentation">
                            <b role="presentation"></b>
                          </span>
                        </span>
                      </span>
                      <span class="dropdown-wrapper" aria-hidden="true"></span>
                    </span>
                  </div>
                  <!--end::Input-->
                </div>
                <!--end::Input group-->
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Member Type:</label>
                  <!--end::Label-->
                  <!--begin::Options-->
                  <div class="d-flex">
                    <!--begin::Options-->
                    <label class="form-check form-check-sm form-check-custom form-check-solid me-5">
                      <input class="form-check-input" type="checkbox" value="1" />
                      <span class="form-check-label">Author</span>
                    </label>
                    <!--end::Options-->
                    <!--begin::Options-->
                    <label class="form-check form-check-sm form-check-custom form-check-solid">
                      <input class="form-check-input" type="checkbox" value="2" checked="checked" />
                      <span class="form-check-label">Customer</span>
                    </label>
                    <!--end::Options-->
                  </div>
                  <!--end::Options-->
                </div>
                <!--end::Input group-->
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Notifications:</label>
                  <!--end::Label-->
                  <!--begin::Switch-->
                  <div
                    class="form-check form-switch form-switch-sm form-check-custom form-check-solid"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      value
                      name="notifications"
                      checked="checked"
                    />
                    <label class="form-check-label">Enabled</label>
                  </div>
                  <!--end::Switch-->
                </div>
                <!--end::Input group-->
                <!--begin::Actions-->
                <div class="d-flex justify-content-end">
                  <button
                    type="reset"
                    class="btn btn-sm btn-light btn-active-light-primary me-2"
                    data-kt-menu-dismiss="true"
                  >Reset</button>
                  <button
                    type="submit"
                    class="btn btn-sm btn-primary"
                    data-kt-menu-dismiss="true"
                  >Apply</button>
                </div>
                <!--end::Actions-->
              </div>
              <!--end::Form-->
            </div>
            <!--end::Menu 1-->
            <!--end::Menu-->
          </div>
          <!--end::Item-->
          <!--begin::Item-->
          <div class="d-flex align-items-center position-relative mb-7">
            <!--begin::Label-->
            <div class="position-absolute top-0 start-0 rounded h-100 bg-secondary w-4px"></div>
            <!--end::Label-->
            <!--begin::Checkbox-->
            <div class="form-check form-check-custom form-check-solid ms-6 me-4">
              <input class="form-check-input" type="checkbox" value />
            </div>
            <!--end::Checkbox-->
            <!--begin::Details-->
            <div class="fw-bold">
              <a
                href="#"
                class="fs-6 fw-bolder text-gray-900 text-hover-primary"
              >Produce evidence reports for submission</a>
              <!--begin::Info-->
              <div class="text-gray-400">
                Due in 1 week
                <a href="#">Richard Helson</a>
              </div>
              <!--end::Info-->
            </div>
            <!--end::Details-->
            <!--begin::Menu-->
            <button
              type="button"
              class="btn btn-clean btn-sm btn-icon btn-icon-primary btn-active-light-primary ms-auto"
              data-kt-menu-trigger="click"
              data-kt-menu-placement="bottom-end"
            >
              <!--begin::Svg Icon | path: icons/duotune/general/gen024.svg-->
              <span class="svg-icon svg-icon-3">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24px"
                  height="24px"
                  viewBox="0 0 24 24"
                >
                  <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <rect x="5" y="5" width="5" height="5" rx="1" fill="#000000" />
                    <rect x="14" y="5" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                    <rect x="5" y="14" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                    <rect x="14" y="14" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                  </g>
                </svg>
              </span>
              <!--end::Svg Icon-->
            </button>
            <!--begin::Menu 1-->
            <div
              class="menu menu-sub menu-sub-dropdown w-250px w-md-300px"
              data-kt-menu="true"
              id="kt_menu_62051c572e682"
            >
              <!--begin::Header-->
              <div class="px-7 py-5">
                <div class="fs-5 text-dark fw-bolder">Filter Options</div>
              </div>
              <!--end::Header-->
              <!--begin::Menu separator-->
              <div class="separator border-gray-200"></div>
              <!--end::Menu separator-->
              <!--begin::Form-->
              <div class="px-7 py-5">
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Status:</label>
                  <!--end::Label-->
                  <!--begin::Input-->
                  <div>
                    <select
                      class="form-select form-select-solid select2-hidden-accessible"
                      data-kt-select2="true"
                      data-placeholder="Select option"
                      data-dropdown-parent="#kt_menu_62051c572e682"
                      data-allow-clear="true"
                      data-select2-id="select2-data-34-fvye"
                      tabindex="-1"
                      aria-hidden="true"
                    >
                      <option data-select2-id="select2-data-36-hleg"></option>
                      <option value="1">Approved</option>
                      <option value="2">Pending</option>
                      <option value="2">In Process</option>
                      <option value="2">Rejected</option>
                    </select>
                    <span
                      class="select2 select2-container select2-container--bootstrap5"
                      dir="ltr"
                      data-select2-id="select2-data-35-kuju"
                      style="width: 100%;"
                    >
                      <span class="selection">
                        <span
                          class="select2-selection select2-selection--single form-select form-select-solid"
                          role="combobox"
                          aria-haspopup="true"
                          aria-expanded="false"
                          tabindex="0"
                          aria-disabled="false"
                          aria-labelledby="select2-n7bk-container"
                          aria-controls="select2-n7bk-container"
                        >
                          <span
                            class="select2-selection__rendered"
                            id="select2-n7bk-container"
                            role="textbox"
                            aria-readonly="true"
                            title="Select option"
                          >
                            <span class="select2-selection__placeholder">Select option</span>
                          </span>
                          <span class="select2-selection__arrow" role="presentation">
                            <b role="presentation"></b>
                          </span>
                        </span>
                      </span>
                      <span class="dropdown-wrapper" aria-hidden="true"></span>
                    </span>
                  </div>
                  <!--end::Input-->
                </div>
                <!--end::Input group-->
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Member Type:</label>
                  <!--end::Label-->
                  <!--begin::Options-->
                  <div class="d-flex">
                    <!--begin::Options-->
                    <label class="form-check form-check-sm form-check-custom form-check-solid me-5">
                      <input class="form-check-input" type="checkbox" value="1" />
                      <span class="form-check-label">Author</span>
                    </label>
                    <!--end::Options-->
                    <!--begin::Options-->
                    <label class="form-check form-check-sm form-check-custom form-check-solid">
                      <input class="form-check-input" type="checkbox" value="2" checked="checked" />
                      <span class="form-check-label">Customer</span>
                    </label>
                    <!--end::Options-->
                  </div>
                  <!--end::Options-->
                </div>
                <!--end::Input group-->
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Notifications:</label>
                  <!--end::Label-->
                  <!--begin::Switch-->
                  <div
                    class="form-check form-switch form-switch-sm form-check-custom form-check-solid"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      value
                      name="notifications"
                      checked="checked"
                    />
                    <label class="form-check-label">Enabled</label>
                  </div>
                  <!--end::Switch-->
                </div>
                <!--end::Input group-->
                <!--begin::Actions-->
                <div class="d-flex justify-content-end">
                  <button
                    type="reset"
                    class="btn btn-sm btn-light btn-active-light-primary me-2"
                    data-kt-menu-dismiss="true"
                  >Reset</button>
                  <button
                    type="submit"
                    class="btn btn-sm btn-primary"
                    data-kt-menu-dismiss="true"
                  >Apply</button>
                </div>
                <!--end::Actions-->
              </div>
              <!--end::Form-->
            </div>
            <!--end::Menu 1-->
            <!--end::Menu-->
          </div>
          <!--end::Item-->
          <!--begin::Item-->
          <div class="d-flex align-items-center position-relative mb-7">
            <!--begin::Label-->
            <div class="position-absolute top-0 start-0 rounded h-100 bg-secondary w-4px"></div>
            <!--end::Label-->
            <!--begin::Checkbox-->
            <div class="form-check form-check-custom form-check-solid ms-6 me-4">
              <input class="form-check-input" type="checkbox" value />
            </div>
            <!--end::Checkbox-->
            <!--begin::Details-->
            <div class="fw-bold">
              <a
                href="#"
                class="fs-6 fw-bolder text-gray-900 text-hover-primary"
              >Approve pending data for ingestion</a>
              <!--begin::Info-->
              <div class="text-gray-400">
                Due in 1 week
                <a href="#">Richard Helson</a>
              </div>
              <!--end::Info-->
            </div>
            <!--end::Details-->
            <!--begin::Menu-->
            <button
              type="button"
              class="btn btn-clean btn-sm btn-icon btn-icon-primary btn-active-light-primary ms-auto"
              data-kt-menu-trigger="click"
              data-kt-menu-placement="bottom-end"
            >
              <!--begin::Svg Icon | path: icons/duotune/general/gen024.svg-->
              <span class="svg-icon svg-icon-3">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24px"
                  height="24px"
                  viewBox="0 0 24 24"
                >
                  <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <rect x="5" y="5" width="5" height="5" rx="1" fill="#000000" />
                    <rect x="14" y="5" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                    <rect x="5" y="14" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                    <rect x="14" y="14" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                  </g>
                </svg>
              </span>
              <!--end::Svg Icon-->
            </button>
            <!--begin::Menu 1-->
            <div
              class="menu menu-sub menu-sub-dropdown w-250px w-md-300px"
              data-kt-menu="true"
              id="kt_menu_62051c572e704"
            >
              <!--begin::Header-->
              <div class="px-7 py-5">
                <div class="fs-5 text-dark fw-bolder">Filter Options</div>
              </div>
              <!--end::Header-->
              <!--begin::Menu separator-->
              <div class="separator border-gray-200"></div>
              <!--end::Menu separator-->
              <!--begin::Form-->
              <div class="px-7 py-5">
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Status:</label>
                  <!--end::Label-->
                  <!--begin::Input-->
                  <div>
                    <select
                      class="form-select form-select-solid select2-hidden-accessible"
                      data-kt-select2="true"
                      data-placeholder="Select option"
                      data-dropdown-parent="#kt_menu_62051c572e704"
                      data-allow-clear="true"
                      data-select2-id="select2-data-37-jmac"
                      tabindex="-1"
                      aria-hidden="true"
                    >
                      <option data-select2-id="select2-data-39-tk9z"></option>
                      <option value="1">Approved</option>
                      <option value="2">Pending</option>
                      <option value="2">In Process</option>
                      <option value="2">Rejected</option>
                    </select>
                    <span
                      class="select2 select2-container select2-container--bootstrap5"
                      dir="ltr"
                      data-select2-id="select2-data-38-jrun"
                      style="width: 100%;"
                    >
                      <span class="selection">
                        <span
                          class="select2-selection select2-selection--single form-select form-select-solid"
                          role="combobox"
                          aria-haspopup="true"
                          aria-expanded="false"
                          tabindex="0"
                          aria-disabled="false"
                          aria-labelledby="select2-2ze4-container"
                          aria-controls="select2-2ze4-container"
                        >
                          <span
                            class="select2-selection__rendered"
                            id="select2-2ze4-container"
                            role="textbox"
                            aria-readonly="true"
                            title="Select option"
                          >
                            <span class="select2-selection__placeholder">Select option</span>
                          </span>
                          <span class="select2-selection__arrow" role="presentation">
                            <b role="presentation"></b>
                          </span>
                        </span>
                      </span>
                      <span class="dropdown-wrapper" aria-hidden="true"></span>
                    </span>
                  </div>
                  <!--end::Input-->
                </div>
                <!--end::Input group-->
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Member Type:</label>
                  <!--end::Label-->
                  <!--begin::Options-->
                  <div class="d-flex">
                    <!--begin::Options-->
                    <label class="form-check form-check-sm form-check-custom form-check-solid me-5">
                      <input class="form-check-input" type="checkbox" value="1" />
                      <span class="form-check-label">Author</span>
                    </label>
                    <!--end::Options-->
                    <!--begin::Options-->
                    <label class="form-check form-check-sm form-check-custom form-check-solid">
                      <input class="form-check-input" type="checkbox" value="2" checked="checked" />
                      <span class="form-check-label">Customer</span>
                    </label>
                    <!--end::Options-->
                  </div>
                  <!--end::Options-->
                </div>
                <!--end::Input group-->
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Notifications:</label>
                  <!--end::Label-->
                  <!--begin::Switch-->
                  <div
                    class="form-check form-switch form-switch-sm form-check-custom form-check-solid"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      value
                      name="notifications"
                      checked="checked"
                    />
                    <label class="form-check-label">Enabled</label>
                  </div>
                  <!--end::Switch-->
                </div>
                <!--end::Input group-->
                <!--begin::Actions-->
                <div class="d-flex justify-content-end">
                  <button
                    type="reset"
                    class="btn btn-sm btn-light btn-active-light-primary me-2"
                    data-kt-menu-dismiss="true"
                  >Reset</button>
                  <button
                    type="submit"
                    class="btn btn-sm btn-primary"
                    data-kt-menu-dismiss="true"
                  >Apply</button>
                </div>
                <!--end::Actions-->
              </div>
              <!--end::Form-->
            </div>
            <!--end::Menu 1-->
            <!--end::Menu-->
          </div>
          <!--end::Item-->
          <!--begin::Item-->
          <div class="d-flex align-items-center position-relative">
            <!--begin::Label-->
            <div class="position-absolute top-0 start-0 rounded h-100 bg-secondary w-4px"></div>
            <!--end::Label-->
            <!--begin::Checkbox-->
            <div class="form-check form-check-custom form-check-solid ms-6 me-4">
              <input class="form-check-input" type="checkbox" value />
            </div>
            <!--end::Checkbox-->
            <!--begin::Details-->
            <div class="fw-bold">
              <a
                href="#"
                class="fs-6 fw-bolder text-gray-900 text-hover-primary"
              >Review new detected geographic areas</a>
              <!--begin::Info-->
              <div class="text-gray-400">
                Due in 2 weeks
                <a href="#">Richard Helson</a>
              </div>
              <!--end::Info-->
            </div>
            <!--end::Details-->
            <!--begin::Menu-->
            <button
              type="button"
              class="btn btn-clean btn-sm btn-icon btn-icon-primary btn-active-light-primary ms-auto"
              data-kt-menu-trigger="click"
              data-kt-menu-placement="bottom-end"
            >
              <!--begin::Svg Icon | path: icons/duotune/general/gen024.svg-->
              <span class="svg-icon svg-icon-3">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24px"
                  height="24px"
                  viewBox="0 0 24 24"
                >
                  <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <rect x="5" y="5" width="5" height="5" rx="1" fill="#000000" />
                    <rect x="14" y="5" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                    <rect x="5" y="14" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                    <rect x="14" y="14" width="5" height="5" rx="1" fill="#000000" opacity="0.3" />
                  </g>
                </svg>
              </span>
              <!--end::Svg Icon-->
            </button>
            <!--begin::Menu 1-->
            <div
              class="menu menu-sub menu-sub-dropdown w-250px w-md-300px"
              data-kt-menu="true"
              id="kt_menu_62051c572e776"
            >
              <!--begin::Header-->
              <div class="px-7 py-5">
                <div class="fs-5 text-dark fw-bolder">Filter Options</div>
              </div>
              <!--end::Header-->
              <!--begin::Menu separator-->
              <div class="separator border-gray-200"></div>
              <!--end::Menu separator-->
              <!--begin::Form-->
              <div class="px-7 py-5">
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Status:</label>
                  <!--end::Label-->
                  <!--begin::Input-->
                  <div>
                    <select
                      class="form-select form-select-solid select2-hidden-accessible"
                      data-kt-select2="true"
                      data-placeholder="Select option"
                      data-dropdown-parent="#kt_menu_62051c572e776"
                      data-allow-clear="true"
                      data-select2-id="select2-data-40-28eg"
                      tabindex="-1"
                      aria-hidden="true"
                    >
                      <option data-select2-id="select2-data-42-pudo"></option>
                      <option value="1">Approved</option>
                      <option value="2">Pending</option>
                      <option value="2">In Process</option>
                      <option value="2">Rejected</option>
                    </select>
                    <span
                      class="select2 select2-container select2-container--bootstrap5"
                      dir="ltr"
                      data-select2-id="select2-data-41-ikuk"
                      style="width: 100%;"
                    >
                      <span class="selection">
                        <span
                          class="select2-selection select2-selection--single form-select form-select-solid"
                          role="combobox"
                          aria-haspopup="true"
                          aria-expanded="false"
                          tabindex="0"
                          aria-disabled="false"
                          aria-labelledby="select2-iohx-container"
                          aria-controls="select2-iohx-container"
                        >
                          <span
                            class="select2-selection__rendered"
                            id="select2-iohx-container"
                            role="textbox"
                            aria-readonly="true"
                            title="Select option"
                          >
                            <span class="select2-selection__placeholder">Select option</span>
                          </span>
                          <span class="select2-selection__arrow" role="presentation">
                            <b role="presentation"></b>
                          </span>
                        </span>
                      </span>
                      <span class="dropdown-wrapper" aria-hidden="true"></span>
                    </span>
                  </div>
                  <!--end::Input-->
                </div>
                <!--end::Input group-->
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Member Type:</label>
                  <!--end::Label-->
                  <!--begin::Options-->
                  <div class="d-flex">
                    <!--begin::Options-->
                    <label class="form-check form-check-sm form-check-custom form-check-solid me-5">
                      <input class="form-check-input" type="checkbox" value="1" />
                      <span class="form-check-label">Author</span>
                    </label>
                    <!--end::Options-->
                    <!--begin::Options-->
                    <label class="form-check form-check-sm form-check-custom form-check-solid">
                      <input class="form-check-input" type="checkbox" value="2" checked="checked" />
                      <span class="form-check-label">Customer</span>
                    </label>
                    <!--end::Options-->
                  </div>
                  <!--end::Options-->
                </div>
                <!--end::Input group-->
                <!--begin::Input group-->
                <div class="mb-10">
                  <!--begin::Label-->
                  <label class="form-label fw-bold">Notifications:</label>
                  <!--end::Label-->
                  <!--begin::Switch-->
                  <div
                    class="form-check form-switch form-switch-sm form-check-custom form-check-solid"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      value
                      name="notifications"
                      checked="checked"
                    />
                    <label class="form-check-label">Enabled</label>
                  </div>
                  <!--end::Switch-->
                </div>
                <!--end::Input group-->
                <!--begin::Actions-->
                <div class="d-flex justify-content-end">
                  <button
                    type="reset"
                    class="btn btn-sm btn-light btn-active-light-primary me-2"
                    data-kt-menu-dismiss="true"
                  >Reset</button>
                  <button
                    type="submit"
                    class="btn btn-sm btn-primary"
                    data-kt-menu-dismiss="true"
                  >Apply</button>
                </div>
                <!--end::Actions-->
              </div>
              <!--end::Form-->
            </div>
            <!--end::Menu 1-->
            <!--end::Menu-->
          </div>
          <!--end::Item-->
        </div>
        <!--end::Card body-->
      </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "tasks_widget",
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
