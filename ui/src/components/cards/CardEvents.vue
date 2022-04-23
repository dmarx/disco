<template>
   <div class="card">
        <div class="card-header border-0">
          <h3 class="card-title fw-bolder text-dark">All Events &amp; Transactions</h3>
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
          <div class="table_wrapper">
            <table id="kt_datatable_example_1" class="table table-row-bordered gy-5">
              <thead>
                <tr class="fw-bold fs-6 text-muted">
                  <th>Ref</th>
                  <th>Call ID</th>
                  <th>Start time</th>
                  <th>Duration</th>
                  <th>Type</th>
                  <th>First Location</th>
                  <th>Last Location</th>
                  <th>Entity</th>
                  <th>Subject Attribution</th>
                  <th>Receiver</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>45</td>
                  <td>ID 4587</td>
                  <td>14-09-14 13:48</td>
                  <td>17 mins</td>
                  <td>Voice call</td>
                  <td>Birmingham</td>
                  <td>Manchester</td>
                  <td>078417900765</td>
                  <td>Subject 2</td>
                  <td>0845 300 235</td>
                </tr>
                <tr>
                  <td>45</td>
                  <td>ID 4587</td>
                  <td>14-09-14 13:48</td>
                  <td>17 mins</td>
                  <td>Voice call</td>
                  <td>Birmingham</td>
                  <td>Manchester</td>
                  <td>078417900765</td>
                  <td>Subject 2</td>
                  <td>0845 300 235</td>
                </tr>
                <tr>
                  <td>45</td>
                  <td>ID 4587</td>
                  <td>14-09-14 13:48</td>
                  <td>17 mins</td>
                  <td>Voice call</td>
                  <td>Birmingham</td>
                  <td>Manchester</td>
                  <td>078417900765</td>
                  <td>Subject 2</td>
                  <td>0845 300 235</td>
                </tr>
                <tr>
                  <td>45</td>
                  <td>ID 4587</td>
                  <td>14-09-14 13:48</td>
                  <td>17 mins</td>
                  <td>Voice call</td>
                  <td>Birmingham</td>
                  <td>Manchester</td>
                  <td>078417900765</td>
                  <td>Subject 2</td>
                  <td>0845 300 235</td>
                </tr>
                <tr>
                  <td>45</td>
                  <td>ID 4587</td>
                  <td>14-09-14 13:48</td>
                  <td>17 mins</td>
                  <td>Voice call</td>
                  <td>Birmingham</td>
                  <td>Manchester</td>
                  <td>078417900765</td>
                  <td>Subject 2</td>
                  <td>0845 300 235</td>
                </tr>
                <tr>
                  <td>45</td>
                  <td>ID 4587</td>
                  <td>14-09-14 13:48</td>
                  <td>17 mins</td>
                  <td>Voice call</td>
                  <td>Birmingham</td>
                  <td>Manchester</td>
                  <td>078417900765</td>
                  <td>Subject 2</td>
                  <td>0845 300 235</td>
                </tr>
              </tbody>
              <!-- <tfoot>
                <tr>
                  <th>Ref</th>
                  <th>Call ID</th>
                  <th>Start time</th>
                  <th>Duration</th>
                  <th>Type</th>
                  <th>First Location</th>
                  <th>Last Location</th>
                  <th>Entity</th>
                  <th>Subject Attribution</th>
                  <th>Receiver</th>
                </tr>
              </tfoot> -->
            </table>
          </div>
        </div>
      </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Dropdown2 from "../dropdown/Dropdown2.vue";

export default defineComponent({
  name: "card-events",
  props: {
    title: String,
    description: String,
    buttonText: String,
    image: String,
    modalId: String,
  },
  components: { Dropdown2 },
});
</script>
