import { Module, MutationTree, ActionTree, GetterTree } from "vuex";
import { RootState } from "@/store/index";
import {
  getDrones,
  droneUpdate,
  droneCreate,
  droneDelete,
  Drone,
} from "../../api/modules/drone";
import SSEClient from "@/api/sse";

export interface DroneState {
  drones: Drone[];
  loading: boolean;
  error: string | null;
  sseClient: SSEClient | null;
}

const state: DroneState = {
  drones: [],
  loading: false,
  error: null,
  sseClient: null,
};

const mutations: MutationTree<DroneState> = {
  setDrones(state, drones: Drone[]) {
    drones.forEach((drone) => {
      const existingDrone = state.drones.find((d) => d.id === drone.id);
      if (!existingDrone) {
        state.drones.push(drone);
      }
    });
  },
  setLoading(state, loading: boolean) {
    state.loading = loading;
  },
  setError(state, error: string | null) {
    state.error = error;
  },
  updateDrone(state, updatedDrone: Drone) {
    const index = state.drones.findIndex(
      (drone) => drone.id === updatedDrone.id
    );
    if (index !== -1) {
      state.drones.splice(index, 1, updatedDrone);
    }
  },
  addDrone(state, newDrone: Drone) {
    state.drones.push(newDrone);
  },
  deleteDrone(state, droneId: number) {
    state.drones = state.drones.filter((drone) => drone.id !== droneId);
  },
  setSSEClient(state, client: SSEClient) {
    state.sseClient = client;
  },
};

const actions: ActionTree<DroneState, any> = {
  async fetchDrones({ commit }) {
    commit("setLoading", true);
    try {
      const drones = await getDrones();
      commit("setDrones", drones);
      commit("setError", null);
    } catch (error: any) {
      commit("setError", error.message);
    } finally {
      commit("setLoading", false);
    }
  },
  async updateDrone({ commit }, { droneData }) {
    commit("setLoading", true);
    try {
      const updatedDrone = await droneUpdate(droneData);
      commit("setError", null);
    } catch (error: any) {
      commit("setError", error.message);
    } finally {
      commit("setLoading", false);
    }
  },
  async createDrone({ commit }, droneData) {
    commit("setLoading", true);
    try {
      const newDrone = await droneCreate(droneData);
      commit("setError", null);
    } catch (error: any) {
      commit("setError", error.message);
    } finally {
      commit("setLoading", false);
    }
  },
  async deleteDrone({ commit }, droneId) {
    commit("setLoading", true);
    try {
      await droneDelete(droneId);
      commit("deleteDrone", droneId);
      commit("setError", null);
    } catch (error: any) {
      commit("setError", error.message);
    } finally {
      commit("setLoading", false);
    }
  },
  async initSSE({ commit }) {
    if (state.sseClient) return;
    const sseClient = new SSEClient("/drones/stream");
    sseClient.addListener((data) => {
      switch (data.action) {
        case "insert":
          commit("addDrone", data.drone);
          break;
        case "update":
          commit("updateDrone", data.drone);
          break;
        case "delete":
          commit("deleteDrone", data.drone_id);
          break;
      }
    });

    commit("setSSEClient", sseClient);
  },
};

const getters: GetterTree<DroneState, RootState> = {
  allDrones: (state) => state.drones,
  isLoading: (state) => state.loading,
  error: (state) => state.error,
  getDronesByTaskId: (state, getters, rootState) => (taskId: number) => {
    if (taskId) {
      const droneIds: number[] = rootState.tasks.tasks.find(
        (task: any) => task.id === taskId
      ).drones_id;
      if (droneIds.length) {
        return state.drones.filter((drone: Drone) =>
          droneIds.includes(drone.id)
        );
      }
    }
  },
};

const drone: Module<DroneState, any> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};

export default drone;
