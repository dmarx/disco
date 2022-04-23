<template>
  <div class="menu-item">
    <div class="menu-content pt-8 pb-2">
      <span class="menu-section text-muted text-uppercase fs-8 ls-1">SEARCH FILTERS</span>
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
        >Name / Keyword</button>
      </h2>
      <div
        id="kt_accordion_1_body_1"
        class="accordion-collapse collapse show"
        aria-labelledby="kt_accordion_1_header_1"
      >
        <div class="accordion-body">
          <input
            type="text" v-model="data.name"
            class="form-control form-control form-control-solid"
            name="name"
            style="background-image: url(&quot;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABHklEQVQ4EaVTO26DQBD1ohQWaS2lg9JybZ+AK7hNwx2oIoVf4UPQ0Lj1FdKktevIpel8AKNUkDcWMxpgSaIEaTVv3sx7uztiTdu2s/98DywOw3Dued4Who/M2aIx5lZV1aEsy0+qiwHELyi+Ytl0PQ69SxAxkWIA4RMRTdNsKE59juMcuZd6xIAFeZ6fGCdJ8kY4y7KAuTRNGd7jyEBXsdOPE3a0QGPsniOnnYMO67LgSQN9T41F2QGrQRRFCwyzoIF2qyBuKKbcOgPXdVeY9rMWgNsjf9ccYesJhk3f5dYT1HX9gR0LLQR30TnjkUEcx2uIuS4RnI+aj6sJR0AM8AaumPaM/rRehyWhXqbFAA9kh3/8/NvHxAYGAsZ/il8IalkCLBfNVAAAAABJRU5ErkJggg==&quot;); background-repeat: no-repeat; background-attachment: scroll; background-size: 16px 18px; background-position: 98% 50%; cursor: auto;"
          />
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header" id="kt_accordion_1_header_2">
        <button
          class="accordion-button fw-bold"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#kt_accordion_1_body_2"
          aria-expanded="true"
          aria-controls="kt_accordion_1_body_2"
        >Location</button>
      </h2>
      <div
        id="kt_accordion_1_body_2"
        class="accordion-collapse collapse show"
        aria-labelledby="kt_accordion_1_header_2"
      >
        <div class="accordion-body">
          <input
            type="text"  v-model="data.location"
            class="form-control form-control form-control-solid"
            name="city"
            style="background-image: url(&quot;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABHklEQVQ4EaVTO26DQBD1ohQWaS2lg9JybZ+AK7hNwx2oIoVf4UPQ0Lj1FdKktevIpel8AKNUkDcWMxpgSaIEaTVv3sx7uztiTdu2s/98DywOw3Dued4Who/M2aIx5lZV1aEsy0+qiwHELyi+Ytl0PQ69SxAxkWIA4RMRTdNsKE59juMcuZd6xIAFeZ6fGCdJ8kY4y7KAuTRNGd7jyEBXsdOPE3a0QGPsniOnnYMO67LgSQN9T41F2QGrQRRFCwyzoIF2qyBuKKbcOgPXdVeY9rMWgNsjf9ccYesJhk3f5dYT1HX9gR0LLQR30TnjkUEcx2uIuS4RnI+aj6sJR0AM8AaumPaM/rRehyWhXqbFAA9kh3/8/NvHxAYGAsZ/il8IalkCLBfNVAAAAABJRU5ErkJggg==&quot;); background-repeat: no-repeat; background-attachment: scroll; background-size: 16px 18px; background-position: 98% 50%; cursor: auto;"
          />
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header" id="kt_accordion_1_header_3">
        <button
          class="accordion-button fw-bold"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#kt_accordion_1_body_3"
          aria-expanded="true"
          aria-controls="kt_accordion_1_body_3"
        >Email</button>
      </h2>
      <div
        id="kt_accordion_1_body_3"
        class="accordion-collapse collapse show"
        aria-labelledby="kt_accordion_1_header_3"
      >
        <div class="accordion-body">
          <input
            type="text"  v-model="data.email"
            class="form-control form-control form-control-solid"
            name="city"
            style="background-image: url(&quot;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABHklEQVQ4EaVTO26DQBD1ohQWaS2lg9JybZ+AK7hNwx2oIoVf4UPQ0Lj1FdKktevIpel8AKNUkDcWMxpgSaIEaTVv3sx7uztiTdu2s/98DywOw3Dued4Who/M2aIx5lZV1aEsy0+qiwHELyi+Ytl0PQ69SxAxkWIA4RMRTdNsKE59juMcuZd6xIAFeZ6fGCdJ8kY4y7KAuTRNGd7jyEBXsdOPE3a0QGPsniOnnYMO67LgSQN9T41F2QGrQRRFCwyzoIF2qyBuKKbcOgPXdVeY9rMWgNsjf9ccYesJhk3f5dYT1HX9gR0LLQR30TnjkUEcx2uIuS4RnI+aj6sJR0AM8AaumPaM/rRehyWhXqbFAA9kh3/8/NvHxAYGAsZ/il8IalkCLBfNVAAAAABJRU5ErkJggg==&quot;); background-repeat: no-repeat; background-attachment: scroll; background-size: 16px 18px; background-position: 98% 50%; cursor: auto;"
          />
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header" id="kt_accordion_1_header_4">
        <button
          class="accordion-button fw-bold"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#kt_accordion_1_body_4"
          aria-expanded="true"
          aria-controls="kt_accordion_1_body_4"
        >Phone</button>
      </h2>
      <div
        id="kt_accordion_1_body_4"
        class="accordion-collapse collapse show"
        aria-labelledby="kt_accordion_1_header_4"
      >
        <div class="accordion-body">
          <input
            type="text"  v-model="data.phone"
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
          class="accordion-button fw-bold"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#kt_accordion_1_body_5"
          aria-expanded="true"
          aria-controls="kt_accordion_1_body_5"
        >Company</button>
      </h2>
      <div
        id="kt_accordion_1_body_5"
        class="accordion-collapse collapse show"
        aria-labelledby="kt_accordion_1_header_5"
      >
        <div class="accordion-body">
          <input
            type="text"  v-model="data.company"
            class="form-control form-control form-control-solid"
            name="city"
            style="background-image: url(&quot;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABHklEQVQ4EaVTO26DQBD1ohQWaS2lg9JybZ+AK7hNwx2oIoVf4UPQ0Lj1FdKktevIpel8AKNUkDcWMxpgSaIEaTVv3sx7uztiTdu2s/98DywOw3Dued4Who/M2aIx5lZV1aEsy0+qiwHELyi+Ytl0PQ69SxAxkWIA4RMRTdNsKE59juMcuZd6xIAFeZ6fGCdJ8kY4y7KAuTRNGd7jyEBXsdOPE3a0QGPsniOnnYMO67LgSQN9T41F2QGrQRRFCwyzoIF2qyBuKKbcOgPXdVeY9rMWgNsjf9ccYesJhk3f5dYT1HX9gR0LLQR30TnjkUEcx2uIuS4RnI+aj6sJR0AM8AaumPaM/rRehyWhXqbFAA9kh3/8/NvHxAYGAsZ/il8IalkCLBfNVAAAAABJRU5ErkJggg==&quot;); background-repeat: no-repeat; background-attachment: scroll; background-size: 16px 18px; background-position: 98% 50%; cursor: auto;"
          />
        </div>
      </div>
    </div>
  </div>

  <br />
  <!--end::Input group-->
  <!--begin::Action-->
  <div class="d-flex align-items-center justify-content-end" style="margin-right:15px;">
    <a
      
      @click="discard"
      class="btn btn-active-light-primary btn-color-gray-400 me-3"
    >Discard</a>
    <a  @click="search" class="btn btn-primary">Search</a>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

interface Filter {
  status: string;
  name: string;
  location: string;
  email: string;
  phone: string;
  company: string;
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
      name: "tom mason",
      location: "london",
      email: "",
      phone: "",
      company: ""
    });

    return {
      data
    };
  },
  methods:{
    discard(){
      console.log('reset');
      this.$emit('reset',{});
    },
    search(){
      console.log('Search ' ,this.data);
      this.$emit('search',this.data);

    }
  }
});
</script>
