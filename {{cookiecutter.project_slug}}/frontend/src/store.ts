import Vue from 'vue';
import Vuex from 'vuex';

import router from '@/router';
import { api } from '@/api';
import { saveToken } from '@/utils';

Vue.use(Vuex);

export interface State {
  token: string | null;
  isLoggedIn: boolean | null;
  logInError: boolean;
  userName: string;
  dashboardMiniDrawer: boolean;
  dashboardShowDrawer: boolean;
}

const defaultState: State = {
  isLoggedIn: null,
  token: null,
  logInError: false,
  userName: '',
  dashboardMiniDrawer: false,
  dashboardShowDrawer: true,
};

// Mutations
export const setToken = 'setToken';
export const setLoggedIn = 'setLoggedIn';
export const setUsername = 'setUsername';
export const setLogInError = 'setLogInError';
export const setDashboardMiniDrawer = 'setDashboardMiniDrawer';
export const setDashboardShowDrawer = 'setDashboardShowDrawer';

// Actions
export const actionCheckLoggedIn = 'actionCheckLoggedIn';
export const actionCheckStateToken = 'actionCheckStateToken';
export const actionCheckLocalStorageToken = 'actionCheckLocalStorageToken';
export const actionLogIn = 'actionLogIn';
export const actionLogOut = 'actionLogOut';
export const actionRouteLogOut = 'actionRouteLogOut';
export const actionRouteLoggedIn = 'actionRouteLoggedIn';


export default new Vuex.Store({
  state: defaultState,
  mutations: {
    [setToken]: (state, payload: string) => {
      state.token = payload;
    },
    [setLoggedIn]: (state, payload: boolean) => {
      state.isLoggedIn = payload;
    },
    [setLogInError]: (state, payload: boolean) => {
      state.logInError = payload;
    },
    [setUsername]: (state, payload: string) => {
      state.userName = payload;
    },
    [setDashboardMiniDrawer]: (state, payload: boolean) => {
      state.dashboardMiniDrawer = payload;
    },
    [setDashboardShowDrawer]: (state, payload: boolean) => {
      state.dashboardShowDrawer = payload;
    },
  },
  actions: {
    [actionLogIn]: (context, payload) => {
      api.logInGetToken(payload.username, payload.password).then((response) => {
        const token = response.data.access_token;
        if (token) {
          saveToken(token);
          context.commit(setToken, token);
          context.commit(setLoggedIn, true);
          context.commit(setLogInError, false);
          context.dispatch(actionRouteLoggedIn);
        } else {
          context.dispatch(actionLogOut);
        }
      }).catch((err) => {
        context.commit(setLogInError, true);
        context.dispatch(actionLogOut);
      });
    },
    [actionCheckLoggedIn]: async (context) => {
      if (context.state.isLoggedIn) {
        context.dispatch(actionRouteLoggedIn);
      } else {
        context.dispatch(actionCheckStateToken);
      }
    },
    [actionCheckStateToken]: async (context) => {
      if (context.state.token) {
        api.getMe(context.state.token).then((response) => {
          context.commit(setLoggedIn, true);
          context.dispatch(actionRouteLoggedIn);
          if (response.data.name) {
            context.commit(setUsername, response.data.name);
          }
        }).catch((err) => {
          context.dispatch(actionLogOut);
        });
      } else {
        context.dispatch(actionCheckLocalStorageToken);
      }
    },
    [actionCheckLocalStorageToken]: async (context) => {
      const token = localStorage.getItem('token');
      if (token) {
        api.getMe(token).then((response) => {
          context.commit(setToken, token);
          context.commit(setLoggedIn, true);
          context.dispatch(actionRouteLoggedIn);
          if (response.data.name) {
            context.commit(setUsername, response.data.name);
          }
        }).catch((err) => {
          context.dispatch(actionLogOut);
        });
      } else {
        context.dispatch(actionLogOut);
      }
    },
    [actionLogOut]: (context) => {
      localStorage.removeItem('token');
      context.commit(setToken, '');
      context.commit(setLoggedIn, false);
      context.dispatch(actionRouteLogOut);
    },
    [actionRouteLogOut]: (context) => {
      if (router.currentRoute.path !== '/login') {
        router.push('/login');
      }
    },
    [actionRouteLoggedIn]: (context) => {
      if (router.currentRoute.path === '/login' || router.currentRoute.path === '/') {
        router.push('/main');
      }
    },
  },
});
