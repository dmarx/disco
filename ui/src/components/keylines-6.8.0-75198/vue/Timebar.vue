//
//     Vue components KeyLines v6.8.0-75198
//
//     Copyright © 2011-2022 Cambridge Intelligence Limited.
//     All rights reserved.
//

<script>
import KlComponent from './Keylines.vue';
export default {
  name: 'KlTimebar',
  extends: KlComponent,
  data: () => ({
    type: 'timebar'
  }),
  methods: {
    onLoad() {
      return this.component.zoom('fit');
    }
  }
};
</script>
