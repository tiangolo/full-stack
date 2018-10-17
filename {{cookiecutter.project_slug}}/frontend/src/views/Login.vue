<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>{{appName}}</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <v-form @keyup.enter="submit">
                <v-text-field @keyup.enter="submit" v-model="email" prepend-icon="person" name="login" label="Login" type="text"></v-text-field>
                <v-text-field @keyup.enter="submit" v-model="password" prepend-icon="lock" name="password" label="Password" id="password" type="password"></v-text-field>
              </v-form>
              <div v-if="$store.state.logInError">
                <v-alert :value="$store.state.logInError" transition="fade-transition" type="error">
                  Incorrect email or password
                </v-alert>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click.prevent="submit">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { checkIsLoggedIn, saveToken } from '@/utils';
import { api } from '@/api';
import store, {
  setToken,
  setLoggedIn,
  actionLogIn,
  actionCheckLoggedIn,
  actionLogOut,
} from '@/store';
import { appName } from '@/env';

@Component
export default class Login extends Vue {
  public email: string = '';
  public password: string = '';
  appName = appName;


  public beforeRouteEnter(to, from, next) {
    if (store.state.isLoggedIn === false) {
      next();
    } else {
      next('/');
    }
  }

  public beforeRouteUpdate(to, from, next) {
    if (store.state.isLoggedIn === false) {
      next();
    } else {
      next('/');
    }
  }

  public checkLogin() {
    this.$store.dispatch(actionCheckLoggedIn);
  }

  public submit() {
    this.$store.dispatch(actionLogIn, {
      username: this.email,
      password: this.password,
    });
  }
}
</script>

<style>
</style>
