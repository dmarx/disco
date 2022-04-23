//
//     Vue components KeyLines v6.8.0-75198
//
//     Copyright © 2011-2022 Cambridge Intelligence Limited.
//     All rights reserved.
//

<template>
  <div ref="container" :class="containerClass" :style="styleObject"></div>
</template>

<script>
const KeyLines = window.KeyLines;
KeyLines.promisify();
export default {
  name: "KlComponent",
  props: {
    id: {
      type: String,
      required: true
    },
    container: Object,
    containerClass: String,
    styleObject: Object,
    options: Object,
    data: Object,
    animateOnLoad: {
      type: Boolean,
      default: false
    },
    selection: {
      type: Array,
      default: () => []
    }
  },
  mounted() {
    KeyLines.create({
      id: this.id,
      options: this.options,
      container: this.$refs ? this.$refs.container : null,
      type: this.type
    }).then(component => {
      this.klcreate(component);
    }).catch(console.err);
  },
  beforeUnmount() {
    this.component.destroy();
  },
  methods: {
    onEvent(props) {
      const name = 'kl-' + props.name;
      this.$emit('kl-all', props);
      this.$emit(name, props.event);
    },
    klcreate(component) {
      this.component = component;
      this.component.on('all', this.onEvent);
      this.component.load(this.data)
        .then(() => this.onLoad({ animate: !!this.animateOnLoad }))
        .then(() => {
          component.selection(this.selection);
          this.$emit('kl-ready', component);
        });
    }
  }
};
</script>
