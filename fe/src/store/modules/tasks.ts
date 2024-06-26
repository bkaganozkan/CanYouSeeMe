import { Module, MutationTree, ActionTree, GetterTree } from "vuex";
import { RootState } from "@/store/index";
import {
  Task,
  getTasks,
  getTaskById,
  taskUpdate,
  taskCreate,
  taskDelete,
  taskExecute,
  Task as TaskData,
  Drone,
  Image,
} from "@/api/modules/tasks";
import SSEClient from "@/api/sse";

export interface TasksState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  sseClient: EventSource | null;
}

const state: TasksState = {
  tasks: [],
  loading: false,
  error: null,
  sseClient: null,
};

const getters: GetterTree<TasksState, any> = {
  getTaskById: (state) => (id: number) => {
    return state.tasks.find((task: TaskData) => task.id === id);
  },
  tasks: (state) => state.tasks,
  loading: (state) => state.loading,
  error: (state) => state.error,
};

const mutations: MutationTree<TasksState> = {
  setTasks(state, tasks: Task[]) {
    state.tasks = tasks;
  },
  setLoading(state, loading: boolean) {
    state.loading = loading;
  },
  setError(state, error: string) {
    state.error = error;
  },
  setTask(state, task: Task) {
    const index = state.tasks.findIndex((t) => t.id === task.id);
    if (index !== -1) {
      state.tasks.splice(index, 1, task);
    } else {
      state.tasks.push(task);
    }
  },
  updateTask(state, updatedTask: Task) {
    const index = state.tasks.findIndex((task) => task.id === updatedTask.id);
    if (index !== -1) {
      state.tasks.splice(index, 1, updatedTask);
    }
  },
  addTask(state, newTask: Task) {
    state.tasks.push(newTask);
  },
  removeTask(state, taskId: number) {
    state.tasks = state.tasks.filter((task) => task.id !== taskId);
  },
  setSSEClient(state, sseClient: EventSource | null) {
    state.sseClient = sseClient;
  },
};

const actions: ActionTree<TasksState, RootState> = {
  async fetchTasks({ commit }) {
    commit("setLoading", true);
    try {
      const tasks = await getTasks();
      commit("setTasks", tasks);
    } catch (error: any) {
      commit("setError", error.message);
    } finally {
      commit("setLoading", false);
    }
  },
  async fetchTaskById({ commit }, taskId: number) {
    commit("setLoading", true);
    try {
      const task = await getTaskById(taskId);
      commit("setTask", task);
      commit("drones/setDrones", task.drones, { root: true });
    } catch (error: any) {
      commit("setError", error.message);
    } finally {
      commit("setLoading", false);
    }
  },
  async updateTask({ commit }, taskData: Partial<Task>) {
    try {
      const updatedTask = await taskUpdate(taskData);
    } catch (error: any) {
      commit("setError", error.message);
    }
  },
  async createTask({ commit }, taskData: Partial<Task>) {
    try {
      await taskCreate(taskData);
    } catch (error: any) {
      commit("setError", error.message);
    }
  },
  async deleteTask({ commit }, taskId: number) {
    try {
      await taskDelete(taskId);
    } catch (error: any) {
      commit("setError", error.message);
    }
  },
  async executeTask({ commit }, taskId: number) {
    try {
      await taskExecute(taskId);
    } catch (error: any) {
      commit("setError", error.message);
    }
  },
  async initSSE({ commit, dispatch }) {
    if (state.sseClient) return;
    const sseClient = new SSEClient("/tasks/stream");
    sseClient.addListener((data) => {
      switch (data.action) {
        case "insert":
          commit("addTask", data.task);
          break;
        case "update":
          commit("updateTask", data.task);
          dispatch("images/updateTaskFromSSE", data.task, { root: true });
          break;
        case "delete":
          commit("removeTask", data.task_id);
          break;
      }
    });
    commit("setSSEClient", sseClient);
  },
};

const tasks: Module<TasksState, any> = {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};

export default tasks;
