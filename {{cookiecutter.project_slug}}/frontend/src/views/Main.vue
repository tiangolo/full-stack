<template>
  <div>
    <v-navigation-drawer persistent :mini-variant="$store.state.dashboardMiniDrawer" v-model="showDrawer" fixed app>
      <v-layout column fill-height>
        <v-list>
          <v-list-tile to="/main">
            <v-list-tile-action>
              <v-icon>web</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Dashboard</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
          <v-spacer></v-spacer>
        <v-list>
          <v-list-tile @click="switchMiniDrawer">
            <v-list-tile-action>
              <v-icon v-html="$store.state.dashboardMiniDrawer ? 'chevron_right' : 'chevron_left'"></v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Collapse</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-layout>
    </v-navigation-drawer>
    <v-toolbar dark color="primary" app>
      <v-toolbar-side-icon @click.stop="switchShowDrawer"></v-toolbar-side-icon>
      <v-toolbar-title v-text="appName"></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-menu bottom left offset-y>
        <v-btn slot="activator" icon>
          <v-icon>more_vert</v-icon>
        </v-btn>

        <v-list>
          <v-list-tile @click="logout">
            <v-list-tile-content>
              <v-list-tile-title>Logout</v-list-tile-title>
            </v-list-tile-content>
            <v-list-tile-action>
              <v-icon>exit_to_app</v-icon>
            </v-list-tile-action>
          </v-list-tile>
        </v-list>
      </v-menu>
    </v-toolbar>
    <v-content>
    </v-content>
    <v-footer class="pa-3" fixed app>
      <v-spacer></v-spacer>
      <span>&copy; {{appName}}</span>
    </v-footer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

import { appName } from '@/env';
import store, {
  setDashboardMiniDrawer,
  setDashboardShowDrawer,
  actionLogOut,
} from '@/store';

@Component
export default class Main extends Vue {
  public appName = appName;

  public miniVariant = false;

  public beforeRouteEnter(to, from, next) {
    if (store.state.isLoggedIn) {
      next();
    } else {
      next('/');
    }
  }

  public beforeRouteUpdate(to, from, next) {
    if (store.state.isLoggedIn) {
      next();
    } else {
      next('/');
    }
  }

  get showDrawer() {
    return this.$store.state.dashboardShowDrawer;
  }

  set showDrawer(value) {
    this.$store.commit(setDashboardShowDrawer, value);
  }

  public switchShowDrawer() {
    this.$store.commit(
      setDashboardShowDrawer,
      !this.$store.state.dashboardShowDrawer,
    );
  }

  public switchMiniDrawer() {
    this.$store.commit(
      setDashboardMiniDrawer,
      !this.$store.state.dashboardMiniDrawer,
    );
  }

  public logout() {
    this.$store.dispatch(actionLogOut);
  }
}
</script>
