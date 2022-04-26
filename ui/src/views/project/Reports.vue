<template>
  <div v-if="state.mounted">
    <Teleport to="#aside-context">
      <div class="menu-item">
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">Browse events</span>
        </div>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-code-square fs-2x"></i>
          </span>
          <span class="menu-title">All events &amp; locations</span>
        </span>
      </div>

      <div
        class="menu-item menu-accordion"
        data-kt-menu-sub="accordion"
        data-kt-menu-trigger="click"
      >
        <div class="menu-content pt-8 pb-2">
          <span class="menu-section text-muted text-uppercase fs-8 ls-1">Financial</span>
        </div>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-bag-check-fill fs-2x"></i>
          </span>
          <span class="menu-title">Account summary</span>
        </span>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-card-list fs-2x"></i>
          </span>
          <span class="menu-title">All transactions</span>
        </span>
        <span class="menu-link">
          <span class="menu-icon">
            <i class="bi bi-link-45deg fs-2x"></i>
          </span>
          <span class="menu-title">Linked transactions</span>
        </span>
      </div>

    
    </Teleport>
  </div>
  <div class="row g-5 g-xl-8">
    <!--begin::Col-->
    <div class="col-xl-6">
      
      <div class="card mb-5 mb-xl-8">
        <!--begin::Body-->
        <div class="card-body pb-0">
          <!--begin::Header-->
          <div class="d-flex align-items-center mb-5">
            <!--begin::User-->
            <div class="d-flex align-items-center flex-grow-1">
              <!--begin::Avatar-->
              <div class="symbol symbol-45px me-5">
                <img src="/media/avatars/300-23.jpg" alt />
              </div>
              <!--end::Avatar-->
              <!--begin::Info-->
              <div class="d-flex flex-column">
                <a
                  href="#"
                  class="text-gray-900 text-hover-primary fs-6 fw-bolder"
                  >Nick Logan</a
                >
                <span class="text-gray-400 fw-bold"
                  >PHP, SQLite, Artisan CLI</span
                >
              </div>
              <!--end::Info-->
            </div>
            <!--end::User-->
            <!--begin::Menu-->
            <div class="my-0">
              <button
                type="button"
                class="btn btn-sm btn-icon btn-color-primary btn-active-light-primary"
                data-kt-menu-trigger="click"
                data-kt-menu-placement="bottom-end"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen024.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24px"
                    height="24px"
                    viewBox="0 0 24 24"
                  >
                    <g
                      stroke="none"
                      stroke-width="1"
                      fill="none"
                      fill-rule="evenodd"
                    >
                      <rect
                        x="5"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                      />
                      <rect
                        x="14"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="5"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="14"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                    </g>
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </button>
              <!--begin::Menu 2-->
              <div
                class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-800 menu-state-bg-light-primary fw-bold w-200px"
                data-kt-menu="true"
              >
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <div class="menu-content fs-6 text-dark fw-bolder px-3 py-4">
                    Quick Actions
                  </div>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu separator-->
                <div class="separator mb-3 opacity-75"></div>
                <!--end::Menu separator-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Ticket</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Customer</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div
                  class="menu-item px-3"
                  data-kt-menu-trigger="hover"
                  data-kt-menu-placement="right-start"
                >
                  <!--begin::Menu item-->
                  <a href="#" class="menu-link px-3">
                    <span class="menu-title">New Group</span>
                    <span class="menu-arrow"></span>
                  </a>
                  <!--end::Menu item-->
                  <!--begin::Menu sub-->
                  <div class="menu-sub menu-sub-dropdown w-175px py-4">
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Admin Group</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Staff Group</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Member Group</a>
                    </div>
                    <!--end::Menu item-->
                  </div>
                  <!--end::Menu sub-->
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Contact</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu separator-->
                <div class="separator mt-3 opacity-75"></div>
                <!--end::Menu separator-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <div class="menu-content px-3 py-3">
                    <a class="btn btn-primary btn-sm px-4" href="#"
                      >Generate Reports</a
                    >
                  </div>
                </div>
                <!--end::Menu item-->
              </div>
              <!--end::Menu 2-->
            </div>
            <!--end::Menu-->
          </div>
          <!--end::Header-->
          <!--begin::Post-->
          <div class="mb-5">
            <!--begin::Text-->
            <p class="text-gray-800 fw-normal mb-5">
              Outlines keep you honest. They stop you from indulging in poorly
              thought-out metaphors about driving and keep you focused on the
              overall structure of your post
            </p>
            <!--end::Text-->
            <!--begin::Toolbar-->
            <div class="d-flex align-items-center mb-5">
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-success px-4 py-2 me-4"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com012.svg-->
                <span class="svg-icon svg-icon-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M20 3H4C2.89543 3 2 3.89543 2 5V16C2 17.1046 2.89543 18 4 18H4.5C5.05228 18 5.5 18.4477 5.5 19V21.5052C5.5 22.1441 6.21212 22.5253 6.74376 22.1708L11.4885 19.0077C12.4741 18.3506 13.6321 18 14.8167 18H20C21.1046 18 22 17.1046 22 16V5C22 3.89543 21.1046 3 20 3Z"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="12"
                      width="7"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="7"
                      width="12"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                120
              </a>
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-danger px-4 py-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen030.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M18.3721 4.65439C17.6415 4.23815 16.8052 4 15.9142 4C14.3444 4 12.9339 4.73924 12.003 5.89633C11.0657 4.73913 9.66 4 8.08626 4C7.19611 4 6.35789 4.23746 5.62804 4.65439C4.06148 5.54462 3 7.26056 3 9.24232C3 9.81001 3.08941 10.3491 3.25153 10.8593C4.12155 14.9013 9.69287 20 12.0034 20C14.2502 20 19.875 14.9013 20.7488 10.8593C20.9109 10.3491 21 9.81001 21 9.24232C21.0007 7.26056 19.9383 5.54462 18.3721 4.65439Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                15
              </a>
            </div>
            <!--end::Toolbar-->
          </div>
          <!--end::Post-->
          <!--begin::Separator-->
          <div class="separator mb-4"></div>
          <!--end::Separator-->
          <!--begin::Reply input-->
          <form class="position-relative mb-6">
            <textarea
              class="form-control border-0 p-0 pe-10 resize-none min-h-25px"
              data-kt-autosize="true"
              rows="1"
              placeholder="Reply.."
              style="overflow: hidden; overflow-wrap: break-word; height: 25px"
            ></textarea>
            <div class="position-absolute top-0 end-0 me-n5">
              <span
                class="btn btn-icon btn-sm btn-active-color-primary pe-0 me-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com008.svg-->
                <span class="svg-icon svg-icon-3 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M4.425 20.525C2.525 18.625 2.525 15.525 4.425 13.525L14.825 3.125C16.325 1.625 18.825 1.625 20.425 3.125C20.825 3.525 20.825 4.12502 20.425 4.52502C20.025 4.92502 19.425 4.92502 19.025 4.52502C18.225 3.72502 17.025 3.72502 16.225 4.52502L5.82499 14.925C4.62499 16.125 4.62499 17.925 5.82499 19.125C7.02499 20.325 8.82501 20.325 10.025 19.125L18.425 10.725C18.825 10.325 19.425 10.325 19.825 10.725C20.225 11.125 20.225 11.725 19.825 12.125L11.425 20.525C9.525 22.425 6.425 22.425 4.425 20.525Z"
                      fill="black"
                    />
                    <path
                      d="M9.32499 15.625C8.12499 14.425 8.12499 12.625 9.32499 11.425L14.225 6.52498C14.625 6.12498 15.225 6.12498 15.625 6.52498C16.025 6.92498 16.025 7.525 15.625 7.925L10.725 12.8249C10.325 13.2249 10.325 13.8249 10.725 14.2249C11.125 14.6249 11.725 14.6249 12.125 14.2249L19.125 7.22493C19.525 6.82493 19.725 6.425 19.725 5.925C19.725 5.325 19.525 4.825 19.125 4.425C18.725 4.025 18.725 3.42498 19.125 3.02498C19.525 2.62498 20.125 2.62498 20.525 3.02498C21.325 3.82498 21.725 4.825 21.725 5.925C21.725 6.925 21.325 7.82498 20.525 8.52498L13.525 15.525C12.325 16.725 10.525 16.725 9.32499 15.625Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
              <span class="btn btn-icon btn-sm btn-active-color-primary ps-0">
                <!--begin::Svg Icon | path: icons/duotune/general/gen018.svg-->
                <span class="svg-icon svg-icon-2 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M18.0624 15.3453L13.1624 20.7453C12.5624 21.4453 11.5624 21.4453 10.9624 20.7453L6.06242 15.3453C4.56242 13.6453 3.76242 11.4453 4.06242 8.94534C4.56242 5.34534 7.46242 2.44534 11.0624 2.04534C15.8624 1.54534 19.9624 5.24534 19.9624 9.94534C20.0624 12.0453 19.2624 13.9453 18.0624 15.3453Z"
                      fill="black"
                    />
                    <path
                      d="M12.0624 13.0453C13.7193 13.0453 15.0624 11.7022 15.0624 10.0453C15.0624 8.38849 13.7193 7.04535 12.0624 7.04535C10.4056 7.04535 9.06241 8.38849 9.06241 10.0453C9.06241 11.7022 10.4056 13.0453 12.0624 13.0453Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
            </div>
          </form>
          <!--edit::Reply input-->
        </div>
        <!--end::Body-->
      </div>
      <!--end::Feeds Widget 2-->
      <!--begin::Feeds Widget 3-->
      <div class="card mb-5 mb-xl-8">
        <!--begin::Body-->
        <div class="card-body pb-0">
          <!--begin::Header-->
          <div class="d-flex align-items-center mb-3">
            <!--begin::User-->
            <div class="d-flex align-items-center flex-grow-1">
              <!--begin::Avatar-->
              <div class="symbol symbol-45px me-5">
                <img src="/media/avatars/300-21.jpg" alt />
              </div>
              <!--end::Avatar-->
              <!--begin::Info-->
              <div class="d-flex flex-column">
                <a
                  href="#"
                  class="text-gray-900 text-hover-primary fs-6 fw-bolder"
                  >Carles Nilson</a
                >
                <span class="text-gray-400 fw-bold">Yestarday at 5:06 PM</span>
              </div>
              <!--end::Info-->
            </div>
            <!--end::User-->
            <!--begin::Menu-->
            <div class="my-0">
              <button
                type="button"
                class="btn btn-sm btn-icon btn-color-primary btn-active-light-primary"
                data-kt-menu-trigger="click"
                data-kt-menu-placement="bottom-end"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen024.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24px"
                    height="24px"
                    viewBox="0 0 24 24"
                  >
                    <g
                      stroke="none"
                      stroke-width="1"
                      fill="none"
                      fill-rule="evenodd"
                    >
                      <rect
                        x="5"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                      />
                      <rect
                        x="14"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="5"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="14"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                    </g>
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </button>
              <!--begin::Menu 2-->
              <div
                class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-800 menu-state-bg-light-primary fw-bold w-200px"
                data-kt-menu="true"
              >
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <div class="menu-content fs-6 text-dark fw-bolder px-3 py-4">
                    Quick Actions
                  </div>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu separator-->
                <div class="separator mb-3 opacity-75"></div>
                <!--end::Menu separator-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Ticket</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Customer</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div
                  class="menu-item px-3"
                  data-kt-menu-trigger="hover"
                  data-kt-menu-placement="right-start"
                >
                  <!--begin::Menu item-->
                  <a href="#" class="menu-link px-3">
                    <span class="menu-title">New Group</span>
                    <span class="menu-arrow"></span>
                  </a>
                  <!--end::Menu item-->
                  <!--begin::Menu sub-->
                  <div class="menu-sub menu-sub-dropdown w-175px py-4">
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Admin Group</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Staff Group</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Member Group</a>
                    </div>
                    <!--end::Menu item-->
                  </div>
                  <!--end::Menu sub-->
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Contact</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu separator-->
                <div class="separator mt-3 opacity-75"></div>
                <!--end::Menu separator-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <div class="menu-content px-3 py-3">
                    <a class="btn btn-primary btn-sm px-4" href="#"
                      >Generate Reports</a
                    >
                  </div>
                </div>
                <!--end::Menu item-->
              </div>
              <!--end::Menu 2-->
            </div>
            <!--end::Menu-->
          </div>
          <!--end::Header-->
          <!--begin::Post-->
          <div class="mb-7">
            <!--begin::Text-->
            <div class="text-gray-800 mb-5">
              Outlines keep you honest. They stop you from indulging in poorly
              thought-out metaphors about driving and keep you focused on the
              overall structure of your post
            </div>
            <!--end::Text-->
            <!--begin::Toolbar-->
            <div class="d-flex align-items-center mb-5">
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-success px-4 py-2 me-4"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com012.svg-->
                <span class="svg-icon svg-icon-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M20 3H4C2.89543 3 2 3.89543 2 5V16C2 17.1046 2.89543 18 4 18H4.5C5.05228 18 5.5 18.4477 5.5 19V21.5052C5.5 22.1441 6.21212 22.5253 6.74376 22.1708L11.4885 19.0077C12.4741 18.3506 13.6321 18 14.8167 18H20C21.1046 18 22 17.1046 22 16V5C22 3.89543 21.1046 3 20 3Z"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="12"
                      width="7"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="7"
                      width="12"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                12
              </a>
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-danger px-4 py-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen030.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M18.3721 4.65439C17.6415 4.23815 16.8052 4 15.9142 4C14.3444 4 12.9339 4.73924 12.003 5.89633C11.0657 4.73913 9.66 4 8.08626 4C7.19611 4 6.35789 4.23746 5.62804 4.65439C4.06148 5.54462 3 7.26056 3 9.24232C3 9.81001 3.08941 10.3491 3.25153 10.8593C4.12155 14.9013 9.69287 20 12.0034 20C14.2502 20 19.875 14.9013 20.7488 10.8593C20.9109 10.3491 21 9.81001 21 9.24232C21.0007 7.26056 19.9383 5.54462 18.3721 4.65439Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                150
              </a>
            </div>
            <!--end::Toolbar-->
          </div>
          <!--end::Post-->
          <!--begin::Replies-->
          <div class="mb-7 ps-10">
            <!--begin::Reply-->
            <div class="d-flex mb-5">
              <!--begin::Avatar-->
              <div class="symbol symbol-45px me-5">
                <img src="/media/avatars/300-14.jpg" alt />
              </div>
              <!--end::Avatar-->
              <!--begin::Info-->
              <div class="d-flex flex-column flex-row-fluid">
                <!--begin::Info-->
                <div class="d-flex align-items-center flex-wrap mb-1">
                  <a
                    href="#"
                    class="text-gray-800 text-hover-primary fw-bolder me-2"
                    >Alice Danchik</a
                  >
                  <span class="text-gray-400 fw-bold fs-7">1 day</span>
                  <a
                    href="#"
                    class="ms-auto text-gray-400 text-hover-primary fw-bold fs-7"
                    >Reply</a
                  >
                </div>
                <!--end::Info-->
                <!--begin::Post-->
                <span class="text-gray-800 fs-7 fw-normal pt-1"
                  >Long before you sit dow to put digital pen to paper you need
                  to make sure you have to sit down and write.</span
                >
                <!--end::Post-->
              </div>
              <!--end::Info-->
            </div>
            <!--end::Reply-->
            <!--begin::Reply-->
            <div class="d-flex">
              <!--begin::Avatar-->
              <div class="symbol symbol-45px me-5">
                <img src="/media/avatars/300-9.jpg" alt />
              </div>
              <!--end::Avatar-->
              <!--begin::Info-->
              <div class="d-flex flex-column flex-row-fluid">
                <!--begin::Info-->
                <div class="d-flex align-items-center flex-wrap mb-1">
                  <a
                    href="#"
                    class="text-gray-800 text-hover-primary fw-bolder me-2"
                    >Harris Bold</a
                  >
                  <span class="text-gray-400 fw-bold fs-7">2 days</span>
                  <a
                    href="#"
                    class="ms-auto text-gray-400 text-hover-primary fw-bold fs-7"
                    >Reply</a
                  >
                </div>
                <!--end::Info-->
                <!--begin::Post-->
                <span class="text-gray-800 fs-7 fw-normal pt-1"
                  >Outlines keep you honest. They stop you from indulging in
                  poorly</span
                >
                <!--end::Post-->
              </div>
              <!--end::Info-->
            </div>
            <!--end::Reply-->
          </div>
          <!--end::Replies-->
          <!--begin::Separator-->
          <div class="separator mb-4"></div>
          <!--end::Separator-->
          <!--begin::Reply input-->
          <form class="position-relative mb-6">
            <textarea
              class="form-control border-0 p-0 pe-10 resize-none min-h-25px"
              data-kt-autosize="true"
              rows="1"
              placeholder="Reply.."
              style="overflow: hidden; overflow-wrap: break-word; height: 25px"
            ></textarea>
            <div class="position-absolute top-0 end-0 me-n5">
              <span
                class="btn btn-icon btn-sm btn-active-color-primary pe-0 me-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com008.svg-->
                <span class="svg-icon svg-icon-3 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M4.425 20.525C2.525 18.625 2.525 15.525 4.425 13.525L14.825 3.125C16.325 1.625 18.825 1.625 20.425 3.125C20.825 3.525 20.825 4.12502 20.425 4.52502C20.025 4.92502 19.425 4.92502 19.025 4.52502C18.225 3.72502 17.025 3.72502 16.225 4.52502L5.82499 14.925C4.62499 16.125 4.62499 17.925 5.82499 19.125C7.02499 20.325 8.82501 20.325 10.025 19.125L18.425 10.725C18.825 10.325 19.425 10.325 19.825 10.725C20.225 11.125 20.225 11.725 19.825 12.125L11.425 20.525C9.525 22.425 6.425 22.425 4.425 20.525Z"
                      fill="black"
                    />
                    <path
                      d="M9.32499 15.625C8.12499 14.425 8.12499 12.625 9.32499 11.425L14.225 6.52498C14.625 6.12498 15.225 6.12498 15.625 6.52498C16.025 6.92498 16.025 7.525 15.625 7.925L10.725 12.8249C10.325 13.2249 10.325 13.8249 10.725 14.2249C11.125 14.6249 11.725 14.6249 12.125 14.2249L19.125 7.22493C19.525 6.82493 19.725 6.425 19.725 5.925C19.725 5.325 19.525 4.825 19.125 4.425C18.725 4.025 18.725 3.42498 19.125 3.02498C19.525 2.62498 20.125 2.62498 20.525 3.02498C21.325 3.82498 21.725 4.825 21.725 5.925C21.725 6.925 21.325 7.82498 20.525 8.52498L13.525 15.525C12.325 16.725 10.525 16.725 9.32499 15.625Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
              <span class="btn btn-icon btn-sm btn-active-color-primary ps-0">
                <!--begin::Svg Icon | path: icons/duotune/general/gen018.svg-->
                <span class="svg-icon svg-icon-2 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M18.0624 15.3453L13.1624 20.7453C12.5624 21.4453 11.5624 21.4453 10.9624 20.7453L6.06242 15.3453C4.56242 13.6453 3.76242 11.4453 4.06242 8.94534C4.56242 5.34534 7.46242 2.44534 11.0624 2.04534C15.8624 1.54534 19.9624 5.24534 19.9624 9.94534C20.0624 12.0453 19.2624 13.9453 18.0624 15.3453Z"
                      fill="black"
                    />
                    <path
                      d="M12.0624 13.0453C13.7193 13.0453 15.0624 11.7022 15.0624 10.0453C15.0624 8.38849 13.7193 7.04535 12.0624 7.04535C10.4056 7.04535 9.06241 8.38849 9.06241 10.0453C9.06241 11.7022 10.4056 13.0453 12.0624 13.0453Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
            </div>
          </form>
          <!--edit::Reply input-->
        </div>
        <!--end::Body-->
      </div>
      <!--end::Feeds Widget 3-->
      <!--begin::Feeds Widget 4-->
      <div class="card mb-5 mb-xl-8">
        <!--begin::Body-->
        <div class="card-body pb-0">
          <!--begin::Header-->
          <div class="d-flex align-items-center mb-5">
            <!--begin::User-->
            <div class="d-flex align-items-center flex-grow-1">
              <!--begin::Avatar-->
              <div class="symbol symbol-45px me-5">
                <img src="/media/avatars/300-7.jpg" alt />
              </div>
              <!--end::Avatar-->
              <!--begin::Info-->
              <div class="d-flex flex-column">
                <a
                  href="#"
                  class="text-gray-900 text-hover-primary fs-6 fw-bolder"
                  >Carles Nilson</a
                >
                <span class="text-gray-400 fw-bold">Last week at 10:00 PM</span>
              </div>
              <!--end::Info-->
            </div>
            <!--end::User-->
            <!--begin::Menu-->
            <div class="my-0">
              <button
                type="button"
                class="btn btn-sm btn-icon btn-color-primary btn-active-light-primary"
                data-kt-menu-trigger="click"
                data-kt-menu-placement="bottom-end"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen024.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24px"
                    height="24px"
                    viewBox="0 0 24 24"
                  >
                    <g
                      stroke="none"
                      stroke-width="1"
                      fill="none"
                      fill-rule="evenodd"
                    >
                      <rect
                        x="5"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                      />
                      <rect
                        x="14"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="5"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="14"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                    </g>
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </button>
              <!--begin::Menu 3-->
              <div
                class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-800 menu-state-bg-light-primary fw-bold w-200px py-3"
                data-kt-menu="true"
              >
                <!--begin::Heading-->
                <div class="menu-item px-3">
                  <div
                    class="menu-content text-muted pb-2 px-3 fs-7 text-uppercase"
                  >
                    Payments
                  </div>
                </div>
                <!--end::Heading-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">Create Invoice</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link flex-stack px-3">
                    Create Payment
                    <i
                      class="fas fa-exclamation-circle ms-2 fs-7"
                      data-bs-toggle="tooltip"
                      title
                      data-bs-original-title="Specify a target name for future usage and reference"
                      aria-label="Specify a target name for future usage and reference"
                    ></i>
                  </a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">Generate Bill</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div
                  class="menu-item px-3"
                  data-kt-menu-trigger="hover"
                  data-kt-menu-placement="right-end"
                >
                  <a href="#" class="menu-link px-3">
                    <span class="menu-title">Subscription</span>
                    <span class="menu-arrow"></span>
                  </a>
                  <!--begin::Menu sub-->
                  <div class="menu-sub menu-sub-dropdown w-175px py-4">
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Plans</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Billing</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Statements</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu separator-->
                    <div class="separator my-2"></div>
                    <!--end::Menu separator-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <div class="menu-content px-3">
                        <!--begin::Switch-->
                        <label
                          class="form-check form-switch form-check-custom form-check-solid"
                        >
                          <!--begin::Input-->
                          <input
                            class="form-check-input w-30px h-20px"
                            type="checkbox"
                            value="1"
                            checked="checked"
                            name="notifications"
                          />
                          <!--end::Input-->
                          <!--end::Label-->
                          <span class="form-check-label text-muted fs-6"
                            >Recuring</span
                          >
                          <!--end::Label-->
                        </label>
                        <!--end::Switch-->
                      </div>
                    </div>
                    <!--end::Menu item-->
                  </div>
                  <!--end::Menu sub-->
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3 my-1">
                  <a href="#" class="menu-link px-3">Settings</a>
                </div>
                <!--end::Menu item-->
              </div>
              <!--end::Menu 3-->
            </div>
            <!--end::Menu-->
          </div>
          <!--end::Header-->
          <!--begin::Post-->
          <div class="mb-7">
            <!--begin::Text-->
            <div class="text-gray-800 mb-5">
              Outlines keep you honest. They stop you from indulging in poorly
              thought-out metaphors about driving and keep you focused on the
              overall structure of your post
            </div>
            <!--end::Text-->
            <!--begin::Toolbar-->
            <div class="d-flex align-items-center mb-5">
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-success px-4 py-2 me-4"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com012.svg-->
                <span class="svg-icon svg-icon-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M20 3H4C2.89543 3 2 3.89543 2 5V16C2 17.1046 2.89543 18 4 18H4.5C5.05228 18 5.5 18.4477 5.5 19V21.5052C5.5 22.1441 6.21212 22.5253 6.74376 22.1708L11.4885 19.0077C12.4741 18.3506 13.6321 18 14.8167 18H20C21.1046 18 22 17.1046 22 16V5C22 3.89543 21.1046 3 20 3Z"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="12"
                      width="7"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="7"
                      width="12"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                22
              </a>
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-danger px-4 py-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen030.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M18.3721 4.65439C17.6415 4.23815 16.8052 4 15.9142 4C14.3444 4 12.9339 4.73924 12.003 5.89633C11.0657 4.73913 9.66 4 8.08626 4C7.19611 4 6.35789 4.23746 5.62804 4.65439C4.06148 5.54462 3 7.26056 3 9.24232C3 9.81001 3.08941 10.3491 3.25153 10.8593C4.12155 14.9013 9.69287 20 12.0034 20C14.2502 20 19.875 14.9013 20.7488 10.8593C20.9109 10.3491 21 9.81001 21 9.24232C21.0007 7.26056 19.9383 5.54462 18.3721 4.65439Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                59
              </a>
            </div>
            <!--end::Toolbar-->
          </div>
          <!--end::Post-->
          <!--begin::Separator-->
          <div class="separator mb-4"></div>
          <!--end::Separator-->
          <!--begin::Reply input-->
          <form class="position-relative mb-6">
            <textarea
              class="form-control border-0 p-0 pe-10 resize-none min-h-25px"
              data-kt-autosize="true"
              rows="1"
              placeholder="Reply.."
              style="overflow: hidden; overflow-wrap: break-word; height: 25px"
            ></textarea>
            <div class="position-absolute top-0 end-0 me-n5">
              <span
                class="btn btn-icon btn-sm btn-active-color-primary pe-0 me-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com008.svg-->
                <span class="svg-icon svg-icon-3 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M4.425 20.525C2.525 18.625 2.525 15.525 4.425 13.525L14.825 3.125C16.325 1.625 18.825 1.625 20.425 3.125C20.825 3.525 20.825 4.12502 20.425 4.52502C20.025 4.92502 19.425 4.92502 19.025 4.52502C18.225 3.72502 17.025 3.72502 16.225 4.52502L5.82499 14.925C4.62499 16.125 4.62499 17.925 5.82499 19.125C7.02499 20.325 8.82501 20.325 10.025 19.125L18.425 10.725C18.825 10.325 19.425 10.325 19.825 10.725C20.225 11.125 20.225 11.725 19.825 12.125L11.425 20.525C9.525 22.425 6.425 22.425 4.425 20.525Z"
                      fill="black"
                    />
                    <path
                      d="M9.32499 15.625C8.12499 14.425 8.12499 12.625 9.32499 11.425L14.225 6.52498C14.625 6.12498 15.225 6.12498 15.625 6.52498C16.025 6.92498 16.025 7.525 15.625 7.925L10.725 12.8249C10.325 13.2249 10.325 13.8249 10.725 14.2249C11.125 14.6249 11.725 14.6249 12.125 14.2249L19.125 7.22493C19.525 6.82493 19.725 6.425 19.725 5.925C19.725 5.325 19.525 4.825 19.125 4.425C18.725 4.025 18.725 3.42498 19.125 3.02498C19.525 2.62498 20.125 2.62498 20.525 3.02498C21.325 3.82498 21.725 4.825 21.725 5.925C21.725 6.925 21.325 7.82498 20.525 8.52498L13.525 15.525C12.325 16.725 10.525 16.725 9.32499 15.625Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
              <span class="btn btn-icon btn-sm btn-active-color-primary ps-0">
                <!--begin::Svg Icon | path: icons/duotune/general/gen018.svg-->
                <span class="svg-icon svg-icon-2 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M18.0624 15.3453L13.1624 20.7453C12.5624 21.4453 11.5624 21.4453 10.9624 20.7453L6.06242 15.3453C4.56242 13.6453 3.76242 11.4453 4.06242 8.94534C4.56242 5.34534 7.46242 2.44534 11.0624 2.04534C15.8624 1.54534 19.9624 5.24534 19.9624 9.94534C20.0624 12.0453 19.2624 13.9453 18.0624 15.3453Z"
                      fill="black"
                    />
                    <path
                      d="M12.0624 13.0453C13.7193 13.0453 15.0624 11.7022 15.0624 10.0453C15.0624 8.38849 13.7193 7.04535 12.0624 7.04535C10.4056 7.04535 9.06241 8.38849 9.06241 10.0453C9.06241 11.7022 10.4056 13.0453 12.0624 13.0453Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
            </div>
          </form>
          <!--edit::Reply input-->
        </div>
        <!--end::Body-->
      </div>
      <!--end::Feeds Widget 4-->
      <!--begin::Feeds widget 5-->
      <div class="card d-none" id="kt_widget_5">
        <!--begin::Body-->
        <div class="card-body pb-0">
          <!--begin::Header-->
          <div class="d-flex align-items-center mb-5">
            <!--begin::User-->
            <div class="d-flex align-items-center flex-grow-1">
              <!--begin::Avatar-->
              <div class="symbol symbol-45px me-5">
                <img src="/media/avatars/300-7.jpg" alt />
              </div>
              <!--end::Avatar-->
              <!--begin::Info-->
              <div class="d-flex flex-column">
                <a
                  href="#"
                  class="text-gray-800 text-hover-primary fs-6 fw-bolder"
                  >Carles Nilson</a
                >
                <span class="text-gray-400 fw-bold">Last week at 10:00 PM</span>
              </div>
              <!--end::Info-->
            </div>
            <!--end::User-->
            <!--begin::Menu-->
            <div class="my-0">
              <button
                type="button"
                class="btn btn-sm btn-icon btn-color-primary btn-active-light-primary"
                data-kt-menu-trigger="click"
                data-kt-menu-placement="bottom-end"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen024.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24px"
                    height="24px"
                    viewBox="0 0 24 24"
                  >
                    <g
                      stroke="none"
                      stroke-width="1"
                      fill="none"
                      fill-rule="evenodd"
                    >
                      <rect
                        x="5"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                      />
                      <rect
                        x="14"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="5"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="14"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                    </g>
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </button>
              <!--begin::Menu 2-->
              <div
                class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-800 menu-state-bg-light-primary fw-bold w-200px"
                data-kt-menu="true"
              >
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <div class="menu-content fs-6 text-dark fw-bolder px-3 py-4">
                    Quick Actions
                  </div>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu separator-->
                <div class="separator mb-3 opacity-75"></div>
                <!--end::Menu separator-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Ticket</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Customer</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div
                  class="menu-item px-3"
                  data-kt-menu-trigger="hover"
                  data-kt-menu-placement="right-start"
                >
                  <!--begin::Menu item-->
                  <a href="#" class="menu-link px-3">
                    <span class="menu-title">New Group</span>
                    <span class="menu-arrow"></span>
                  </a>
                  <!--end::Menu item-->
                  <!--begin::Menu sub-->
                  <div class="menu-sub menu-sub-dropdown w-175px py-4">
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Admin Group</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Staff Group</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Member Group</a>
                    </div>
                    <!--end::Menu item-->
                  </div>
                  <!--end::Menu sub-->
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Contact</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu separator-->
                <div class="separator mt-3 opacity-75"></div>
                <!--end::Menu separator-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <div class="menu-content px-3 py-3">
                    <a class="btn btn-primary btn-sm px-4" href="#"
                      >Generate Reports</a
                    >
                  </div>
                </div>
                <!--end::Menu item-->
              </div>
              <!--end::Menu 2-->
            </div>
            <!--end::Menu-->
          </div>
          <!--end::Header-->
          <!--begin::Post-->
          <div class="mb-7">
            <!--begin::Image-->
            <div
              class="bgi-no-repeat bgi-size-cover rounded min-h-250px mb-5"
              style="background-image: url('/media/stock/900x600/19.jpg')"
            ></div>
            <!--end::Image-->
            <!--begin::Text-->
            <div class="text-gray-800 mb-5">
              Outlines keep you honest. They stop you from indulging in poorly
              thought-out metaphors about driving and keep you focused on the
              overall structure of your post
            </div>
            <!--end::Text-->
            <!--begin::Toolbar-->
            <div class="d-flex align-items-center mb-5">
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-success px-4 py-2 me-4"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com012.svg-->
                <span class="svg-icon svg-icon-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M20 3H4C2.89543 3 2 3.89543 2 5V16C2 17.1046 2.89543 18 4 18H4.5C5.05228 18 5.5 18.4477 5.5 19V21.5052C5.5 22.1441 6.21212 22.5253 6.74376 22.1708L11.4885 19.0077C12.4741 18.3506 13.6321 18 14.8167 18H20C21.1046 18 22 17.1046 22 16V5C22 3.89543 21.1046 3 20 3Z"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="12"
                      width="7"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="7"
                      width="12"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                20
              </a>
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-danger px-4 py-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen030.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M18.3721 4.65439C17.6415 4.23815 16.8052 4 15.9142 4C14.3444 4 12.9339 4.73924 12.003 5.89633C11.0657 4.73913 9.66 4 8.08626 4C7.19611 4 6.35789 4.23746 5.62804 4.65439C4.06148 5.54462 3 7.26056 3 9.24232C3 9.81001 3.08941 10.3491 3.25153 10.8593C4.12155 14.9013 9.69287 20 12.0034 20C14.2502 20 19.875 14.9013 20.7488 10.8593C20.9109 10.3491 21 9.81001 21 9.24232C21.0007 7.26056 19.9383 5.54462 18.3721 4.65439Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                50
              </a>
            </div>
            <!--end::Toolbar-->
          </div>
          <!--end::Post-->
          <!--begin::Separator-->
          <div class="separator mb-4"></div>
          <!--end::Separator-->
          <!--begin::Reply input-->
          <form class="position-relative mb-6">
            <textarea
              class="form-control border-0 p-0 pe-10 resize-none min-h-25px"
              data-kt-autosize="true"
              rows="1"
              placeholder="Reply.."
              style="overflow: hidden; overflow-wrap: break-word"
            ></textarea>
            <div class="position-absolute top-0 end-0 me-n5">
              <span
                class="btn btn-icon btn-sm btn-active-color-primary pe-0 me-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com008.svg-->
                <span class="svg-icon svg-icon-3 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M4.425 20.525C2.525 18.625 2.525 15.525 4.425 13.525L14.825 3.125C16.325 1.625 18.825 1.625 20.425 3.125C20.825 3.525 20.825 4.12502 20.425 4.52502C20.025 4.92502 19.425 4.92502 19.025 4.52502C18.225 3.72502 17.025 3.72502 16.225 4.52502L5.82499 14.925C4.62499 16.125 4.62499 17.925 5.82499 19.125C7.02499 20.325 8.82501 20.325 10.025 19.125L18.425 10.725C18.825 10.325 19.425 10.325 19.825 10.725C20.225 11.125 20.225 11.725 19.825 12.125L11.425 20.525C9.525 22.425 6.425 22.425 4.425 20.525Z"
                      fill="black"
                    />
                    <path
                      d="M9.32499 15.625C8.12499 14.425 8.12499 12.625 9.32499 11.425L14.225 6.52498C14.625 6.12498 15.225 6.12498 15.625 6.52498C16.025 6.92498 16.025 7.525 15.625 7.925L10.725 12.8249C10.325 13.2249 10.325 13.8249 10.725 14.2249C11.125 14.6249 11.725 14.6249 12.125 14.2249L19.125 7.22493C19.525 6.82493 19.725 6.425 19.725 5.925C19.725 5.325 19.525 4.825 19.125 4.425C18.725 4.025 18.725 3.42498 19.125 3.02498C19.525 2.62498 20.125 2.62498 20.525 3.02498C21.325 3.82498 21.725 4.825 21.725 5.925C21.725 6.925 21.325 7.82498 20.525 8.52498L13.525 15.525C12.325 16.725 10.525 16.725 9.32499 15.625Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
              <span class="btn btn-icon btn-sm btn-active-color-primary ps-0">
                <!--begin::Svg Icon | path: icons/duotune/general/gen018.svg-->
                <span class="svg-icon svg-icon-2 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M18.0624 15.3453L13.1624 20.7453C12.5624 21.4453 11.5624 21.4453 10.9624 20.7453L6.06242 15.3453C4.56242 13.6453 3.76242 11.4453 4.06242 8.94534C4.56242 5.34534 7.46242 2.44534 11.0624 2.04534C15.8624 1.54534 19.9624 5.24534 19.9624 9.94534C20.0624 12.0453 19.2624 13.9453 18.0624 15.3453Z"
                      fill="black"
                    />
                    <path
                      d="M12.0624 13.0453C13.7193 13.0453 15.0624 11.7022 15.0624 10.0453C15.0624 8.38849 13.7193 7.04535 12.0624 7.04535C10.4056 7.04535 9.06241 8.38849 9.06241 10.0453C9.06241 11.7022 10.4056 13.0453 12.0624 13.0453Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
            </div>
          </form>
          <!--edit::Reply input-->
        </div>
        <!--end::Body-->
      </div>
      <!--end::Feeds widget 5-->
      <!--begin::Feeds widget 4, 5 load more-->

      <!--end::Feeds widget 4, 5 load more-->
    </div>
    <!--end::Col-->
    <!--begin::Col-->
    <div class="col-xl-6">
      <!--begin::Feeds Widget 5-->
      <div class="card mb-5 mb-xl-8">
        <!--begin::Body-->
        <div class="card-body pb-0">
          <!--begin::Header-->
          <div class="d-flex align-items-center mb-5">
            <!--begin::User-->
            <div class="d-flex align-items-center flex-grow-1">
              <!--begin::Avatar-->
              <div class="symbol symbol-45px me-5">
                <img src="/media/avatars/300-25.jpg" alt />
              </div>
              <!--end::Avatar-->
              <!--begin::Info-->
              <div class="d-flex flex-column">
                <a
                  href="#"
                  class="text-gray-900 text-hover-primary fs-6 fw-bolder"
                  >Sam Logan</a
                >
                <span class="text-gray-400 fw-bold">Mango, Java, Python</span>
              </div>
              <!--end::Info-->
            </div>
            <!--end::User-->
            <!--begin::Menu-->
            <div class="my-0">
              <button
                type="button"
                class="btn btn-sm btn-icon btn-color-primary btn-active-light-primary"
                data-kt-menu-trigger="click"
                data-kt-menu-placement="bottom-end"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen024.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24px"
                    height="24px"
                    viewBox="0 0 24 24"
                  >
                    <g
                      stroke="none"
                      stroke-width="1"
                      fill="none"
                      fill-rule="evenodd"
                    >
                      <rect
                        x="5"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                      />
                      <rect
                        x="14"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="5"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="14"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                    </g>
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </button>
              <!--begin::Menu 2-->
              <div
                class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-800 menu-state-bg-light-primary fw-bold w-200px"
                data-kt-menu="true"
              >
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <div class="menu-content fs-6 text-dark fw-bolder px-3 py-4">
                    Quick Actions
                  </div>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu separator-->
                <div class="separator mb-3 opacity-75"></div>
                <!--end::Menu separator-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Ticket</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Customer</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div
                  class="menu-item px-3"
                  data-kt-menu-trigger="hover"
                  data-kt-menu-placement="right-start"
                >
                  <!--begin::Menu item-->
                  <a href="#" class="menu-link px-3">
                    <span class="menu-title">New Group</span>
                    <span class="menu-arrow"></span>
                  </a>
                  <!--end::Menu item-->
                  <!--begin::Menu sub-->
                  <div class="menu-sub menu-sub-dropdown w-175px py-4">
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Admin Group</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Staff Group</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Member Group</a>
                    </div>
                    <!--end::Menu item-->
                  </div>
                  <!--end::Menu sub-->
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">New Contact</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu separator-->
                <div class="separator mt-3 opacity-75"></div>
                <!--end::Menu separator-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <div class="menu-content px-3 py-3">
                    <a class="btn btn-primary btn-sm px-4" href="#"
                      >Generate Reports</a
                    >
                  </div>
                </div>
                <!--end::Menu item-->
              </div>
              <!--end::Menu 2-->
            </div>
            <!--end::Menu-->
          </div>
          <!--end::Header-->
          <!--begin::Post-->
          <div class="mb-5">
            <!--begin::Image-->
            <div
              class="bgi-no-repeat bgi-size-cover rounded min-h-250px mb-5"
              style="background-image: url('/media/stock/900x600/20.jpg')"
            ></div>
            <!--end::Image-->
            <!--begin::Text-->
            <div class="text-gray-800 mb-5">
              Outlines keep you honest. They stop you from indulging in poorly
              thought-out metaphors about driving and keep you focused on the
              overall structure of your post
            </div>
            <!--end::Text-->
            <!--begin::Toolbar-->
            <div class="d-flex align-items-center mb-5">
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-success px-4 py-2 me-4"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com012.svg-->
                <span class="svg-icon svg-icon-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M20 3H4C2.89543 3 2 3.89543 2 5V16C2 17.1046 2.89543 18 4 18H4.5C5.05228 18 5.5 18.4477 5.5 19V21.5052C5.5 22.1441 6.21212 22.5253 6.74376 22.1708L11.4885 19.0077C12.4741 18.3506 13.6321 18 14.8167 18H20C21.1046 18 22 17.1046 22 16V5C22 3.89543 21.1046 3 20 3Z"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="12"
                      width="7"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="7"
                      width="12"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                89
              </a>
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-danger px-4 py-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen030.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M18.3721 4.65439C17.6415 4.23815 16.8052 4 15.9142 4C14.3444 4 12.9339 4.73924 12.003 5.89633C11.0657 4.73913 9.66 4 8.08626 4C7.19611 4 6.35789 4.23746 5.62804 4.65439C4.06148 5.54462 3 7.26056 3 9.24232C3 9.81001 3.08941 10.3491 3.25153 10.8593C4.12155 14.9013 9.69287 20 12.0034 20C14.2502 20 19.875 14.9013 20.7488 10.8593C20.9109 10.3491 21 9.81001 21 9.24232C21.0007 7.26056 19.9383 5.54462 18.3721 4.65439Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                29
              </a>
            </div>
            <!--end::Toolbar-->
          </div>
          <!--end::Post-->
          <!--begin::Separator-->
          <div class="separator mb-4"></div>
          <!--end::Separator-->
          <!--begin::Reply input-->
          <form class="position-relative mb-6">
            <textarea
              class="form-control border-0 p-0 pe-10 resize-none min-h-25px"
              data-kt-autosize="true"
              rows="1"
              placeholder="Reply.."
              style="overflow: hidden; overflow-wrap: break-word; height: 25px"
            ></textarea>
            <div class="position-absolute top-0 end-0 me-n5">
              <span
                class="btn btn-icon btn-sm btn-active-color-primary pe-0 me-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com008.svg-->
                <span class="svg-icon svg-icon-3 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M4.425 20.525C2.525 18.625 2.525 15.525 4.425 13.525L14.825 3.125C16.325 1.625 18.825 1.625 20.425 3.125C20.825 3.525 20.825 4.12502 20.425 4.52502C20.025 4.92502 19.425 4.92502 19.025 4.52502C18.225 3.72502 17.025 3.72502 16.225 4.52502L5.82499 14.925C4.62499 16.125 4.62499 17.925 5.82499 19.125C7.02499 20.325 8.82501 20.325 10.025 19.125L18.425 10.725C18.825 10.325 19.425 10.325 19.825 10.725C20.225 11.125 20.225 11.725 19.825 12.125L11.425 20.525C9.525 22.425 6.425 22.425 4.425 20.525Z"
                      fill="black"
                    />
                    <path
                      d="M9.32499 15.625C8.12499 14.425 8.12499 12.625 9.32499 11.425L14.225 6.52498C14.625 6.12498 15.225 6.12498 15.625 6.52498C16.025 6.92498 16.025 7.525 15.625 7.925L10.725 12.8249C10.325 13.2249 10.325 13.8249 10.725 14.2249C11.125 14.6249 11.725 14.6249 12.125 14.2249L19.125 7.22493C19.525 6.82493 19.725 6.425 19.725 5.925C19.725 5.325 19.525 4.825 19.125 4.425C18.725 4.025 18.725 3.42498 19.125 3.02498C19.525 2.62498 20.125 2.62498 20.525 3.02498C21.325 3.82498 21.725 4.825 21.725 5.925C21.725 6.925 21.325 7.82498 20.525 8.52498L13.525 15.525C12.325 16.725 10.525 16.725 9.32499 15.625Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
              <span class="btn btn-icon btn-sm btn-active-color-primary ps-0">
                <!--begin::Svg Icon | path: icons/duotune/general/gen018.svg-->
                <span class="svg-icon svg-icon-2 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M18.0624 15.3453L13.1624 20.7453C12.5624 21.4453 11.5624 21.4453 10.9624 20.7453L6.06242 15.3453C4.56242 13.6453 3.76242 11.4453 4.06242 8.94534C4.56242 5.34534 7.46242 2.44534 11.0624 2.04534C15.8624 1.54534 19.9624 5.24534 19.9624 9.94534C20.0624 12.0453 19.2624 13.9453 18.0624 15.3453Z"
                      fill="black"
                    />
                    <path
                      d="M12.0624 13.0453C13.7193 13.0453 15.0624 11.7022 15.0624 10.0453C15.0624 8.38849 13.7193 7.04535 12.0624 7.04535C10.4056 7.04535 9.06241 8.38849 9.06241 10.0453C9.06241 11.7022 10.4056 13.0453 12.0624 13.0453Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
            </div>
          </form>
          <!--edit::Reply input-->
        </div>
        <!--end::Body-->
      </div>
      <!--end::Feeds Widget 5-->
      <!--begin::Forms Widget 6-->
      <div class="card mb-5 mb-xl-8">
        <!--begin::Body-->
        <div class="card-body pb-0">
          <!--begin::Header-->
          <div class="d-flex align-items-center mb-5">
            <!--begin::User-->
            <div class="d-flex align-items-center flex-grow-1">
              <!--begin::Avatar-->
              <div class="symbol symbol-45px me-5">
                <img src="/media/avatars/300-13.jpg" alt />
              </div>
              <!--end::Avatar-->
              <!--begin::Info-->
              <div class="d-flex flex-column">
                <a
                  href="#"
                  class="text-gray-900 text-hover-primary fs-6 fw-bolder"
                  >Mat Dillon</a
                >
                <span class="text-gray-400 fw-bold">Last month</span>
              </div>
              <!--end::Info-->
            </div>
            <!--end::User-->
            <!--begin::Menu-->
            <div class="my-0">
              <button
                type="button"
                class="btn btn-sm btn-icon btn-color-primary btn-active-light-primary"
                data-kt-menu-trigger="click"
                data-kt-menu-placement="bottom-end"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen024.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24px"
                    height="24px"
                    viewBox="0 0 24 24"
                  >
                    <g
                      stroke="none"
                      stroke-width="1"
                      fill="none"
                      fill-rule="evenodd"
                    >
                      <rect
                        x="5"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                      />
                      <rect
                        x="14"
                        y="5"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="5"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                      <rect
                        x="14"
                        y="14"
                        width="5"
                        height="5"
                        rx="1"
                        fill="#000000"
                        opacity="0.3"
                      />
                    </g>
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </button>
              <!--begin::Menu 3-->
              <div
                class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-800 menu-state-bg-light-primary fw-bold w-200px py-3"
                data-kt-menu="true"
              >
                <!--begin::Heading-->
                <div class="menu-item px-3">
                  <div
                    class="menu-content text-muted pb-2 px-3 fs-7 text-uppercase"
                  >
                    Payments
                  </div>
                </div>
                <!--end::Heading-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">Create Invoice</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link flex-stack px-3">
                    Create Payment
                    <i
                      class="fas fa-exclamation-circle ms-2 fs-7"
                      data-bs-toggle="tooltip"
                      title
                      data-bs-original-title="Specify a target name for future usage and reference"
                      aria-label="Specify a target name for future usage and reference"
                    ></i>
                  </a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3">
                  <a href="#" class="menu-link px-3">Generate Bill</a>
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div
                  class="menu-item px-3"
                  data-kt-menu-trigger="hover"
                  data-kt-menu-placement="right-end"
                >
                  <a href="#" class="menu-link px-3">
                    <span class="menu-title">Subscription</span>
                    <span class="menu-arrow"></span>
                  </a>
                  <!--begin::Menu sub-->
                  <div class="menu-sub menu-sub-dropdown w-175px py-4">
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Plans</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Billing</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <a href="#" class="menu-link px-3">Statements</a>
                    </div>
                    <!--end::Menu item-->
                    <!--begin::Menu separator-->
                    <div class="separator my-2"></div>
                    <!--end::Menu separator-->
                    <!--begin::Menu item-->
                    <div class="menu-item px-3">
                      <div class="menu-content px-3">
                        <!--begin::Switch-->
                        <label
                          class="form-check form-switch form-check-custom form-check-solid"
                        >
                          <!--begin::Input-->
                          <input
                            class="form-check-input w-30px h-20px"
                            type="checkbox"
                            value="1"
                            checked="checked"
                            name="notifications"
                          />
                          <!--end::Input-->
                          <!--end::Label-->
                          <span class="form-check-label text-muted fs-6"
                            >Recuring</span
                          >
                          <!--end::Label-->
                        </label>
                        <!--end::Switch-->
                      </div>
                    </div>
                    <!--end::Menu item-->
                  </div>
                  <!--end::Menu sub-->
                </div>
                <!--end::Menu item-->
                <!--begin::Menu item-->
                <div class="menu-item px-3 my-1">
                  <a href="#" class="menu-link px-3">Settings</a>
                </div>
                <!--end::Menu item-->
              </div>
              <!--end::Menu 3-->
            </div>
            <!--end::Menu-->
          </div>
          <!--end::Header-->
          <!--begin::Post-->
          <div class="mb-6">
            <!--begin::Text-->
            <div class="text-gray-800 fs-6 fw-normal mb-5">
              Outlines keep you honest. They stop you from indulging in poorly
              thought-out metaphors
            </div>
            <!--end::Text-->
            <!--begin::Video-->
            <div class="mb-5">
              <iframe
                class="embed-responsive-item rounded h-300px w-100"
                src="https://www.youtube.com/embed/qIHXpnASPAA"
                allowfullscreen="allowfullscreen"
              ></iframe>
            </div>
            <!--end::Video-->
            <!--begin::Toolbar-->
            <div class="d-flex align-items-center mb-5">
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-success px-4 py-2 me-4"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com012.svg-->
                <span class="svg-icon svg-icon-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M20 3H4C2.89543 3 2 3.89543 2 5V16C2 17.1046 2.89543 18 4 18H4.5C5.05228 18 5.5 18.4477 5.5 19V21.5052C5.5 22.1441 6.21212 22.5253 6.74376 22.1708L11.4885 19.0077C12.4741 18.3506 13.6321 18 14.8167 18H20C21.1046 18 22 17.1046 22 16V5C22 3.89543 21.1046 3 20 3Z"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="12"
                      width="7"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                    <rect
                      x="6"
                      y="7"
                      width="12"
                      height="2"
                      rx="1"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                189
              </a>
              <a
                href="#"
                class="btn btn-sm btn-light btn-color-muted btn-active-light-danger px-4 py-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/general/gen030.svg-->
                <span class="svg-icon svg-icon-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M18.3721 4.65439C17.6415 4.23815 16.8052 4 15.9142 4C14.3444 4 12.9339 4.73924 12.003 5.89633C11.0657 4.73913 9.66 4 8.08626 4C7.19611 4 6.35789 4.23746 5.62804 4.65439C4.06148 5.54462 3 7.26056 3 9.24232C3 9.81001 3.08941 10.3491 3.25153 10.8593C4.12155 14.9013 9.69287 20 12.0034 20C14.2502 20 19.875 14.9013 20.7488 10.8593C20.9109 10.3491 21 9.81001 21 9.24232C21.0007 7.26056 19.9383 5.54462 18.3721 4.65439Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
                229
              </a>
            </div>
            <!--end::Toolbar-->
          </div>
          <!--end::Bottom-->
          <!--begin::Separator-->
          <div class="separator mb-4"></div>
          <!--end::Separator-->
          <!--begin::Reply input-->
          <form class="position-relative mb-6">
            <textarea
              class="form-control border-0 p-0 pe-10 resize-none min-h-25px"
              data-kt-autosize="true"
              rows="1"
              placeholder="Reply.."
              style="overflow: hidden; overflow-wrap: break-word; height: 25px"
            ></textarea>
            <div class="position-absolute top-0 end-0 me-n5">
              <span
                class="btn btn-icon btn-sm btn-active-color-primary pe-0 me-2"
              >
                <!--begin::Svg Icon | path: icons/duotune/communication/com008.svg-->
                <span class="svg-icon svg-icon-3 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M4.425 20.525C2.525 18.625 2.525 15.525 4.425 13.525L14.825 3.125C16.325 1.625 18.825 1.625 20.425 3.125C20.825 3.525 20.825 4.12502 20.425 4.52502C20.025 4.92502 19.425 4.92502 19.025 4.52502C18.225 3.72502 17.025 3.72502 16.225 4.52502L5.82499 14.925C4.62499 16.125 4.62499 17.925 5.82499 19.125C7.02499 20.325 8.82501 20.325 10.025 19.125L18.425 10.725C18.825 10.325 19.425 10.325 19.825 10.725C20.225 11.125 20.225 11.725 19.825 12.125L11.425 20.525C9.525 22.425 6.425 22.425 4.425 20.525Z"
                      fill="black"
                    />
                    <path
                      d="M9.32499 15.625C8.12499 14.425 8.12499 12.625 9.32499 11.425L14.225 6.52498C14.625 6.12498 15.225 6.12498 15.625 6.52498C16.025 6.92498 16.025 7.525 15.625 7.925L10.725 12.8249C10.325 13.2249 10.325 13.8249 10.725 14.2249C11.125 14.6249 11.725 14.6249 12.125 14.2249L19.125 7.22493C19.525 6.82493 19.725 6.425 19.725 5.925C19.725 5.325 19.525 4.825 19.125 4.425C18.725 4.025 18.725 3.42498 19.125 3.02498C19.525 2.62498 20.125 2.62498 20.525 3.02498C21.325 3.82498 21.725 4.825 21.725 5.925C21.725 6.925 21.325 7.82498 20.525 8.52498L13.525 15.525C12.325 16.725 10.525 16.725 9.32499 15.625Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
              <span class="btn btn-icon btn-sm btn-active-color-primary ps-0">
                <!--begin::Svg Icon | path: icons/duotune/general/gen018.svg-->
                <span class="svg-icon svg-icon-2 mb-3">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      opacity="0.3"
                      d="M18.0624 15.3453L13.1624 20.7453C12.5624 21.4453 11.5624 21.4453 10.9624 20.7453L6.06242 15.3453C4.56242 13.6453 3.76242 11.4453 4.06242 8.94534C4.56242 5.34534 7.46242 2.44534 11.0624 2.04534C15.8624 1.54534 19.9624 5.24534 19.9624 9.94534C20.0624 12.0453 19.2624 13.9453 18.0624 15.3453Z"
                      fill="black"
                    />
                    <path
                      d="M12.0624 13.0453C13.7193 13.0453 15.0624 11.7022 15.0624 10.0453C15.0624 8.38849 13.7193 7.04535 12.0624 7.04535C10.4056 7.04535 9.06241 8.38849 9.06241 10.0453C9.06241 11.7022 10.4056 13.0453 12.0624 13.0453Z"
                      fill="black"
                    />
                  </svg>
                </span>
                <!--end::Svg Icon-->
              </span>
            </div>
          </form>
          <!--edit::Reply input-->
        </div>
        <!--end::Body-->
      </div>
      <!--end::Forms Widget 6-->
    </div>
    <!--end::Col-->
  </div>
  <div style="height: 600px !important">
    <div class="card" style="height: 100% !important">
      <div class="card-header border-0">
        <h3 class="card-title fw-bolder text-dark">Data Map</h3>
        <div class="card-toolbar">
          <button
            type="button"
            class="btn btn-sm btn-icon btn-color-primary btn-active-light-primary"
            data-kt-menu-trigger="click"
            data-kt-menu-placement="bottom-end"
            data-kt-menu-flip="top-end"
          >
            <span class="svg-icon svg-icon-2">
              <inline-svg src="media/icons/duotune/general/gen024.svg" />
            </span>
          </button>
          <Dropdown2></Dropdown2>
        </div>
      </div>
      <div class="card-body pt-2">
        <span
          id="tooltip"
          :class="tooltip.tooltipClass"
          :style="{ left: tooltip.left, top: tooltip.top }"
        >
          <div :class="tooltip.arrowClass"></div>
          <tr>
            <td class="table-cell">
              <b>Appointed on:</b>
            </td>
            <td>{{ tooltip.start }}</td>
          </tr>
          <tr>
            <td class="table-cell">
              <b>Resigned on:</b>
            </td>
            <td>{{ tooltip.end }}</td>
          </tr>
        </span>
        <div
          :id="'chart-container'"
          class="chart-container"
          style="height: 85%"
        >
          <KlChart
            :containerClass="'chart-container'"
            :data="data"
            :options="chartOptions"
            :id="'kl-chart'"
            style="height: 100%"
            @kl-ready="onChartReady"
            @kl-selection-change="highlightSelections"
            @kl-hover="toggleTooltip"
            @kl-drag-move="toggleTooltip"
          ></KlChart>
        </div>
        <div
          :id="'timebar-container'"
          class="timebar-container"
          style="height: 15%"
        >
          <KlTimebar
            class="flex-grow-1"
            :containerClass="'timebar-container'"
            :data="data"
            :options="timebarOptions"
            :id="'kl-timebar'"
            @kl-change="onTimebarChange"
            @kl-ready="onTimebarReady"
          ></KlTimebar>
        </div>

        <!-- <kl-chart
      id="kl"
      containerClass="klchart klchart-timebar"
      :animateOnLoad="true"
      :data="data"
      :options="chartOptions"
      @kl-ready="onChartReady"
      @kl-selection-change="highlightSelections"
      @kl-hover="toggleTooltip"
      @kl-drag-move="toggleTooltip"
    />
    <kl-timebar
      id="timebar"
      containerClass="kltimebar"
      :animateOnLoad="true"
      :data="data"
      :options="timebarOptions"
      @kl-change="onTimebarChange"
      @kl-ready="onTimebarReady"
        />-->
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import KlChart from "keylines/vue/Chart.vue";
import KlTimebar from "keylines/vue/Timebar.vue";
import data from "./../../assets/data/vuechartfilter-data.js";

import { setCurrentPageTitle } from "@/core/helpers/breadcrumb";
import { reactive } from 'vue';

const KeyLines = (window as any).KeyLines;
// KeyLines.promisify();

export default defineComponent({
  name: "reports",
  components: {
    KlChart,
    KlTimebar,
  },
  setup() {
    const state = reactive({ count: 0, mounted: false })
    onMounted(() => {
      setCurrentPageTitle("Reports");
      state.mounted = true;

      // WebFont.load({
      //   custom: {
      //     // be sure to include the CSS file in the page with the @font-face definition
      //     families: ['Font Awesome 5 Free Solid'],
      //   }
      // }),
      //   // set font icons for each node type
      //   this.data.items.forEach((item) => {
      //     if (item && item.type === 'node') {
      //       item.fi = {
      //         c: this.greyColours[0],
      //         t: KeyLines.getFontIcon(item.d.type === 'person' ? 'fa-user' : 'fa-building'),
      //       };
      //     }
      //   })
    });

    var chart;
    var timebar;

    const chartOptions = {
      // logo: { u: 'images/Logo.png' },
      backColour: "transparent",
      handMode: true,
      fontFamily: "Spartan, sans-serif",
      fontSize: 10,
      fontColor: "#FFFFFF",
      iconFontFamily: "Font Awesome 5 Free Solid",
      selectionColour: "#35495E",
      hover: 0,
      selectedNode: {
        fbc: "rgba(0,0,0,0)",
      },
      selectedLink: {
        fbc: "rgba(0,0,0,0)",
      },
    };
    const timebarOptions = {
      backColour: "transparent",
      fontFamily: "Spartan, sans-serif",
      fontSize: 10,
      fontColor: "#FFFFFF",
      histogram: {
        colour: "#42B883",
        highlightColour: "#35495E",
        markColour: "rgb(192, 192, 192)",
        markHiColour: "rgb(105, 105, 105)",
      },
      playSpeed: 30,
    };
    const greyColours = ["rgb(105, 105, 105)", "rgb(192, 192, 192)"];
    // only style the first 3 selections
    const selectionColours = [
      ["#9600d5", "#d0a3cb"],
      ["#0044ff", "#6b93ff"],
      ["#ff0000", "#ff9e9e"],
    ];
    const marks = [
      {
        dt1: new Date("01 Jan 2018 01:00:00"),
        dt2: new Date("01 Jan 2050 01:00:00"),
      },
    ];

    const tooltip = {
      start: "",
      end: "",
      left: "",
      top: "",
      tooltipClass: "hidden",
      arrowClass: "arrow",
    };

    return {
      chart,
      timebar,
      data,
      chartOptions,
      timebarOptions,
      greyColours,
      selectionColours,
      marks,
      tooltip,
      state,
    };
  },

  methods: {
    onChartReady(chart) {
      this.chart = chart;
    },
    onTimebarReady(timebar) {
      this.timebar = timebar;
      this.timebar.mark(this.marks);
    },
    onTimebarChange() {
      if (this.chart && this.timebar) {
        // filter the chart to show only items in the new range
        this.chart
          .filter(this.timebar.inRange, { animate: false, type: "link" })
          .then(() => {
            this.chart.layout("organic", {
              time: 500,
              mode: "adaptive",
              easing: "linear",
            });
          });
      }
    },
    buildItemStyling(item, width, colour, border = false) {
      if (item.type === "node") {
        return {
          id: item.id,
          fi: {
            c: colour,
            t:
              item.d.type === "person"
                ? KeyLines.getFontIcon("fa-user")
                : KeyLines.getFontIcon("fa-building"),
          },
          b: border ? colour : null,
        };
      }
      // else it's a link
      return { id: item.id, w: width || 4, c: colour };
    },
    highlightSelections() {
      if (!this.chart || !this.timebar) return;
      const timebarSelection: any[] = [];
      const chartProperties = {};

      // set default colouring
      this.chart.each({ type: "all" }, (item) => {
        chartProperties[item.id] = this.buildItemStyling(
          item,
          3,
          item.type === "node" ? this.greyColours[0] : this.greyColours[1]
        );
      });
      let selectedIds = this.chart.selection();
      if (selectedIds) {
        if (selectedIds.length > this.selectionColours.length) {
          selectedIds = selectedIds.slice(0, this.selectionColours.length);
          this.chart.selection(selectedIds);
        }

        selectedIds.forEach((id, index) => {
          let neighbouringNodes: any[] = [];
          var links: any[] = [];
          const item = this.chart?.getItem(id);
          const colour =
            index < this.selectionColours.length
              ? this.selectionColours[index][0]
              : this.greyColours[1];
          const linkColour = this.selectionColours[index][1];

          if (item && item.type === "node") {
            // all: true - applies styles to hidden nodes + links not in current time range
            const neighbours = this.chart
              ?.graph()
              .neighbours(id, { all: true });
            if (neighbours && neighbours.links) {
              links = neighbours.links;
              neighbouringNodes = neighbours.nodes;
            }

            // colour node
            chartProperties[id] = this.buildItemStyling(item, 3, colour, true);
            links.forEach((link) => {
              const linkItem = this.chart?.getItem(link);
              chartProperties[link] = this.buildItemStyling(
                linkItem,
                5,
                linkColour
              );
            });
          } else if (item && item.type === "link") {
            links.push(id);
            neighbouringNodes.push(item.id1, item.id2);

            // colour link
            chartProperties[id] = this.buildItemStyling(item, 5, colour);
          }
          // colour neighbour nodes
          neighbouringNodes.forEach((neighbourId) => {
            if (
              chartProperties[neighbourId].fi.c === this.greyColours[0] &&
              index < this.selectionColours.length
            ) {
              chartProperties[neighbourId] = this.buildItemStyling(
                this.chart?.getItem(neighbourId),
                3,
                this.selectionColours[index][1]
              );
            }
          });
          // and select in the timebar
          timebarSelection.push({
            id: links,
            index,
            c: colour,
          });
        });

        this.timebar.selection(timebarSelection);
        this.chart.setProperties(
          Object.keys(chartProperties).map((key) => chartProperties[key])
        );
      }
    },
    getDateFromTimestamp(timestamp) {
      return timestamp ? new Date(timestamp).toDateString().slice(4) : "n/a";
    },
    toggleTooltip({ id, x, y }) {
      if (this.chart) {
        const item = id ? this.chart.getItem(id) : null;
        const viewWidth = this.chart.viewOptions().width;
        if (item && item.type === "link") {
          const timebarItem = data.items.filter((tbItem) => {
            if (tbItem.id === item.id) {
              return tbItem;
            }
          });
          this.tooltip.start = this.getDateFromTimestamp(
            timebarItem[0].dt[0].dt1
          );
          this.tooltip.end = this.getDateFromTimestamp(
            timebarItem[0].dt[0].dt2
          );

          // style tooltip to left of cursor if it's x position + width exceeds
          // the remaining chart space.
          if (viewWidth && viewWidth > x + 250) {
            this.tooltip.top = `${y - 24}px`;
            this.tooltip.left = `${x + 22}px`;
            this.tooltip.tooltipClass = "";
          } else {
            this.tooltip.top = `${y - 24}px`;
            this.tooltip.left = `${x - 218}px`;
            this.tooltip.tooltipClass = "right";
          }
        } else {
          this.tooltip.tooltipClass = "hidden";
        }
      }
    },
  },
});
</script>
<style type="text/css">
#tooltip {
  position: absolute;
  visibility: visible;
  padding: 5px;
  display: block;
  color: black;
  float: left;
  border: 1px solid #ccc;
  background-color: #fff;
  z-index: 1000;
  width: 208px;
}
.arrow {
  position: absolute;
  top: 20px;
  left: -9px;
  border-width: 0px 0px 1px 1px;
  border-style: solid;
  border-color: #ccc;
  background-color: #fff;
  transform: rotateZ(45deg);
  height: 15px;
  width: 15px;
}

.right .arrow {
  top: 20px;
  left: 199px;
  transform: rotateZ(225deg);
}
.table-cell {
  text-align: right;
  padding: 5px;
}
.hidden {
  visibility: hidden !important;
}
</style>
