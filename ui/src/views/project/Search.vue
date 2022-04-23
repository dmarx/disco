<template>
  <div v-if="componentState.mounted">
    <Teleport to="#aside-context">
      <SearchFilters @search="filterUpdate" reset="reset"></SearchFilters>
      <!--end::Action-->
    </Teleport>
  </div>
  <!-- <button @click="increment">{{ state.count }}</button>
  <button @click="toggle()">asdasd</button>-->
  <!--begin::Dashboard-->
  <!-- <teleport to=".aside-extras"><div></div></teleport>  -->
  <div class="row gy-5 g-xl-8">
    <div class="col-xxl-12">
      <div class="card mb-5 mb-xl-8">
        <div class="card-header card-header-stretch overflow-auto">
          <!--begin::Tabs-->
          <ul
            class="nav nav-stretch nav-line-tabs fw-bold border-transparent flex-nowrap"
            role="tablist"
            id="kt_layout_builder_tabs"
          >
            <li class="nav-item">
              <a
                class="nav-link"
                data-bs-toggle="tab"
                href="#kt_builder_main"
                role="tab"
                aria-selected="false"
              >Current Search</a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                data-bs-toggle="tab"
                href="#kt_builder_header"
                role="tab"
                aria-selected="false"
              >Search #2</a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                data-bs-toggle="tab"
                href="#kt_builder_toolbar"
                role="tab"
                aria-selected="false"
              >Add New Search +</a>
            </li>
          </ul>
          <!--end::Tabs-->
        </div>

        <div class="card-body">
          <!-- <div class="position-relative">
            <span
              class="svg-icon svg-icon-3 svg-icon-gray-500 position-absolute top-50 translate-middle ms-6"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
              >
                <rect
                  opacity="0.5"
                  x="17.0365"
                  y="15.1223"
                  width="8.15546"
                  height="2"
                  rx="1"
                  transform="rotate(45 17.0365 15.1223)"
                  fill="black"
                />
                <path
                  d="M11 19C6.55556 19 3 15.4444 3 11C3 6.55556 6.55556 3 11 3C15.4444 3 19 6.55556 19 11C19 15.4444 15.4444 19 11 19ZM11 5C7.53333 5 5 7.53333 5 11C5 14.4667 7.53333 17 11 17C14.4667 17 17 14.4667 17 11C17 7.53333 14.4667 5 11 5Z"
                  fill="black"
                />
              </svg>
            </span>
            <input
              type="text"
              class="form-control form-control-solid ps-10"
              name="search"
              placeholder="Search"
              v-model="data.keyword"
            />
          </div>
          <br />-->
          <div>
            <!--begin::Form-->
            <form
              class="w-100 position-relative mb-3"
              autocomplete="off"
              v-on:submit.prevent="noop"
            >
              <span
                class="svg-icon svg-icon-2 svg-icon-lg-1 svg-icon-gray-500 position-absolute top-50 translate-middle-y ms-0"
              >
                <inline-svg src="media/icons/duotune/general/gen021.svg" />
              </span>
              <input
                ref="inputRef"
                v-model="search"
                v-on:keyup.enter="searchSD($event)"
                type="text"
                class="form-control form-control-flush ps-10"
                name="search"
                placeholder="Search..."
              />
              <span
                v-if="componentState.loading"
                class="position-absolute top-50 end-0 translate-middle-y lh-0 me-1"
              >
                <span class="spinner-border h-15px w-15px align-middle text-gray-400"></span>
              </span>
              <span
                v-show="search.length && !componentState.loading"
                @click="reset()"
                class="btn btn-flush btn-active-color-primary position-absolute top-50 end-0 translate-middle-y lh-0"
              >
                <span class="svg-icon svg-icon-2 svg-icon-lg-1 me-0">
                  <inline-svg src="media/icons/duotune/arrows/arr061.svg" />
                </span>
              </span>
              <div class="position-absolute top-50 end-0 translate-middle-y">
                <!-- <div
                  v-if="!search && !loading"
                  @click="state = 'preferences'"
                  class="btn btn-icon w-20px btn-sm btn-active-color-primary me-1"
                  data-bs-toggle="tooltip"
                  title="Show search preferences"
                >
                  <span class="svg-icon svg-icon-1">
                    <inline-svg src="media/icons/duotune/coding/cod001.svg" />
                  </span>
                </div>-->
                <!-- <div
                  v-if="!search && !loading"
                  @click="state = 'advanced-options'"
                  class="btn btn-icon w-20px btn-sm btn-active-color-primary"
                  data-bs-toggle="tooltip"
                  title="Show more search options"
                >
                  <span class="svg-icon svg-icon-2">
                    <inline-svg src="media/icons/duotune/arrows/arr072.svg" />
                  </span>
                </div>-->
              </div>
            </form>

            <!--begin::Separator-->
            <div class="separator border-gray-200 mb-6"></div>

            <div style="width:100%">
              <el-select
                style="width:100%"
                v-model="connectorsValue"
                multiple
                filterable
                allow-create
                default-first-option
                :reserve-keyword="false"
                placeholder="Choose connectors"
              >
                <el-option
                  v-for="item in connectorsOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </div>
            <br />
            <!--end::Separator-->
            <SearchResults :componentState="componentState" ref="searchResults"></SearchResults>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- <div class="row gy-5 g-xl-8">
    <div class="col-xxl-12">
      <SearchResult></SearchResult>
      <br />
      <SearchResult></SearchResult>
      <br />
      <SearchResult></SearchResult>
      <br />
    </div>
  </div>-->
</template>


<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { setCurrentPageTitle } from "@/core/helpers/breadcrumb";
import { reactive } from 'vue';
import SearchResult from '../../components/widgets/search/SearchResult.vue';
import SearchFilters from "@/components/widgets/search/SearchFilters.vue";
import SearchResults from "@/components/widgets/search/results/SearchResults.vue";
import Main from "@/components/widgets/search/results/Main.vue";
import Empty from "@/components/widgets/search/results/Empty.vue";
import MenuComponent from "@/components/menu/MenuComponent.vue";
import { NOOP } from "@vue/shared";

interface Filter {
  status: string;
  author: boolean;
  customer: boolean;
  notifications: boolean;
  keyword: string;
}

export default defineComponent({
  name: "search",
  // props: {
  //   telTarget
  //   altText: String,
  // },
  components: {
    SearchResult,
    SearchFilters,
    SearchResults,
    Main,
    Empty,
    MenuComponent,
  },

  setup() {
    const componentState = reactive({ count: 0, mounted: false, resultData: null, loading: false, keyword: "" })
    const searchResults = ref<typeof SearchResults>();//(null);
    // const results = ref<Results>();

    onMounted(() => {
      setCurrentPageTitle("Search");
      componentState.mounted = true;
      console.log('Search mounted ');
      // componentState.resultData="123"
    });

    const noop = (e) => {
      // return false;
    };

    const search = ref<string>("");
    const inputRef = ref<HTMLInputElement | null>(null);

    const telTarget = "#body";

    const connectorsValue = ref<string[]>(["Shadow Dragon", "Discover"])
    const connectorsOptions = [
      {
        value: 'Shadow Dragon',
        label: 'Shadow Dragon',
      },
      {
        value: 'Discover',
        label: 'Discover',
      },
      {
        value: 'Fusion',
        label: 'Fusion',
      },
    ];

    return {
      connectorsValue,
      connectorsOptions,
      telTarget,
      search,
      inputRef,
      componentState,
    };
  },
  methods: {
    searchSD(e) {
      if (e.target.value.length > 1) {
        this.reset();
        this.componentState.keyword = e.target.value;
        this.componentState.loading = true;
        console.log('componentState', this.componentState);
        setTimeout(() => {
          var myHeaders = new Headers();
          myHeaders.append("Authorization", "Token j2vtTtDVaChVhVex9GUsAyh3m8kUMFqWgHbMTnhEDTG");
          fetch("https://api.socialnet.shadowdragon.io/facebook/search?limit=25&name=" + this.componentState.keyword, {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
          })
            .then(response => response.text())
            .then(result => {
              console.log("searched");
              this.componentState.resultData = JSON.parse(result);
              this.componentState.loading = false;
              //componentState.title="test";
              // (searchResults as any).title = JSON.stringify(result);
              // console.log(searchResults);
              // console.log("loaded",result);
            })
            .catch(error => console.log('error', error));
        }, 0);
      } else {
        // this.searchSD();
      }

    },

    reset() {
      this.search = "";
      this.componentState.loading = false;
      this.componentState.resultData = null;
    },

    filterUpdate(data) {
      this.reset();
      console.log('update', data);

      this.componentState.loading = true;
      console.log('componentState', this.componentState);
      setTimeout(() => {

        var myHeaders = new Headers();
        myHeaders.append("X-Api-Key", "ae2e6247a05bef057d761d24c2a1708245f8b71dde136dbbb0503c3b4c43529b");
        myHeaders.append("Content-Type", "application/x-www-form-urlencoded");
        //myHeaders.append("Origin", "https://javascript.info");
        //#myHeaders.append("Host", "anywhere.com");

        myHeaders.append("Access-Control-Allow-Origin", "*")
        // myHeaders.append("Access-Control-Allow-Methods", "DELETE, POST, GET, OPTIONS")
        // myHeaders.append("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")


        var urlencoded = new URLSearchParams();
        urlencoded.append("name", data.name);
        urlencoded.append("location", data.location);
        urlencoded.append("email", data.email);
        urlencoded.append("phone", data.phone);
        urlencoded.append("company", data.company);

        var urldata = "name=Sean%20Thorne&location=SF%20Bay%20Area&profile=www.twitter.com%2Fseanthorne5&phone=%2B15555091234";
        var urldata = "name=" + data.name.replace(" ", "%20") + 
                      (data.location.length > 0 ? "&location=" + data.location.replace(" ", "%20") : "") + 
                      (data.phone.length > 0 ? "&phone=" + data.phone.replace(" ", "%20") : "") + 
                      (data.email.length > 0 ? "&email=" + data.email.replace(" ", "%20") : "") + 
                      (data.company.length > 0 ? "&company=" + data.company.replace(" ", "%20") : "");

        //curl --location --request GET 'https://api.peopledatalabs.com/v5/person/enrich?api_key=ae2e6247a05bef057d761d24c2a1708245f8b71dde136dbbb0503c3b4c43529b&pretty=True&profile=linkedin.com/in/twmmason'
        // fetch("https://api.peopledatalabs.com/v5/person/enrich?api_key=ae2e6247a05bef057d761d24c2a1708245f8b71dde136dbbb0503c3b4c43529b&pretty=True&profile=linkedin.com/in/twmmason", {
        // fetch("https://api.peopledatalabs.com/v5/person/enrich?api_key=ae2e6247a05bef057d761d24c2a1708245f8b71dde136dbbb0503c3b4c43529b&pretty=True&"+urldata, {
        fetch("https://api.peopledatalabs.com/v5/person/identify?api_key=ae2e6247a05bef057d761d24c2a1708245f8b71dde136dbbb0503c3b4c43529b&pretty=True&" + urldata, {
          // fetch("https://api.peopledatalabs.com/v5/person/enrich" + urldata, {
          method: 'GET',
          // headers: myHeaders,
          //  mode: 'no-cors',
          // body: urlencoded,
          redirect: 'follow'
        })
          .then(response => response.text())
          .then(result => {
            var results = JSON.parse(result).matches.map(x => x.data);

            this.componentState.resultData = results;
            console.log('componentStateAFterSearch', this.componentState);
            (this.componentState.resultData as any).forEach(x => {
              x.pdl = true;
            });
            this.componentState.loading = false;
          })
          .catch(error => console.log('error', error));

      }, 0);

    }
  }
});
</script>

<style lang="scss">
.accordion-body .form-control.form-control-solid {
  padding: 8px;
  background-color: #20478f;
  border-color: #556687;
  color: #5e6278;
}
.accordion-button:not(.collapsed) {
  color: #fff;
  background-color: transparent;
  box-shadow: inset 0 -1px 0 #eff2f5;
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
.accordion-body .form-control.form-control-solid {
    padding: 8px;
    background-color: #20478f;
    border-color: #556687;
    color: #ffffff;
}
.accordion-body {padding:15px 1.5rem}
</style>