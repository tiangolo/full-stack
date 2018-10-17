<template>

</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import { checkIsLoggedIn, removeToken } from '@/utils';
import store, { setLoggedIn, actionCheckLoggedIn } from '@/store';

@Component
export default class Start extends Vue {

  public beforeRouteEnter(to, from, next) {
    if (store.state.isLoggedIn) {
      next('/main');
    } else if (store.state.isLoggedIn === false) {
      next('/login');
    }
  }

  public beforeRouteUpdate(to, from, next) {
    if (store.state.isLoggedIn) {
      next('/main');
    } else if (store.state.isLoggedIn === false) {
      next('/login');
    }
  }

  public checkLogin() {
    this.$store.dispatch(actionCheckLoggedIn);
  }

  public initApp() {
    if (checkIsLoggedIn(this.$store)) {
      this.$router.push('/main');
    } else {
      this.$router.push('/login');
    }
  }
}
</script>
