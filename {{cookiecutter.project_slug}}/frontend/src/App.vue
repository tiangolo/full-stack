<template>
  <div id="app">
    <v-app>
      <v-content v-if="$store.state.isLoggedIn===null">
        <v-container fill-height>
          <v-layout align-center justify-center>
            <v-flex>
              <div class="text-xs-center">
                <div class="headline my-5">Loading...</div>
                <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
              </div>
            </v-flex>
          </v-layout>
        </v-container>
      </v-content>
      <router-view v-else/>
    </v-app>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { actionCheckLoggedIn } from '@/store';

@Component
export default class App extends Vue {

  created() {
    this.$store.dispatch(actionCheckLoggedIn);
  }
}
</script>
