<template>
  <div>
    <v-btn @click="trigger" color="success">{{title}}</v-btn>
    <input class="visually-hidden" type="file" v-on:change="fileSelected" ref="fileInput">
  </div>
</template>

<script>
  export default {
    name: 'upload-button',
    props: {
      selectedCallback: Function,
      title: String
    },
    methods: {
      fileSelected(e) {
        if (this.selectedCallback) {
          if (e.target.files[0]) {
            this.selectedCallback(e.target.files[0]);
          } else {
            this.selectedCallback(null);
          }
        }
      },
      trigger() {
        this.$refs.fileInput.click();
      }
    }
  }
</script>

<style scoped>
.visually-hidden {
  position: absolute !important;
  height: 1px;
  width: 1px;
  overflow: hidden;
  clip: rect(1px, 1px, 1px, 1px);
}
</style>
