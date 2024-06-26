import { Module, MutationTree, ActionTree, GetterTree } from 'vuex';
import { register as apiRegister, login as apiLogin, logout as apiLogout, UserData } from '@/api/modules/auth';




interface AuthState {
  userRole: string | null;
  authToken: string | null;
  unauthorized : boolean;
}

const state: AuthState = {
  userRole: null,
  authToken: null,
  unauthorized : false,
};

const getters: GetterTree<AuthState, any> = {
  isAuthenticated: (state) => !!state.authToken,
  userRole: (state) => state.userRole,
  unauthorized: (state) => state.unauthorized,

};


const mutations: MutationTree<AuthState> = {
  setUserRole(state, role) {
    state.userRole = role;
  },
  setAuthToken(state, token) {
    state.authToken = token;
  },
  logout(state) {
    state.userRole = null;
    state.authToken = null;
    state.unauthorized  = false;
  },
  setUnauthorized(state, status) {
    state.unauthorized  = status;
  }
};

const actions:  ActionTree<AuthState, any> = {
  async register({ dispatch }, { username, password }: { username: string; password: string }) {
    await apiRegister(username, password);
    await dispatch('login', { username, password });
  },
  async login({ commit, dispatch }, { username, password }: { username: string; password: string }) {
    const data: UserData = await apiLogin(username, password);
    commit('setUserRole', data.user_role);
    commit('setAuthToken', data.access_token);
    localStorage.setItem('authToken', data.access_token);
    dispatch('drones/initSSE', null, { root: true });
    dispatch('tasks/initSSE', null, { root: true });
  },
  async logout({ commit }) {
    await apiLogout();
    commit('logout');
    localStorage.removeItem('authToken');
  },
};


const auth: Module<AuthState, any> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};

export default auth;
