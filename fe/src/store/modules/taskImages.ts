import { Module, ActionTree, MutationTree, GetterTree } from 'vuex';
import { RootState } from '@/store/index';
import SSEClient from '@/api/sse';

interface TaskImage {
    id: number;
    task_id: number,
    drone_id: number;
    image_path: string;
}

interface Drone {
    id: number;
    model: string;
    name: string;
    status: string;
    images: TaskImage[];
}

interface Task {
    id: number;
    task_name: string;
    description: string;
    status: string;
    drones: Drone[];
}

interface TaskImagesState {
    task: Task | null;
    loading: boolean;
    error: string | null;
    sseClient: SSEClient | null;
}

const state: TaskImagesState = {
    task: null,
    loading: false,
    error: null,
    sseClient: null,
};

const getters: GetterTree<TaskImagesState, RootState> = {
    getRootTask: (state, getters, rootState) => (taskId: number) => {
        return rootState.tasks.tasks.find((task: Task) => task.id === taskId);
    },
    isLoading: (state) => state.loading,
    getError: (state) => state.error,

    getLastImagesByTaskId: (state, getters, rootState) => (taskId: number) => {
        const rootTask = rootState.tasks.tasks.find((task: Task) => task.id === taskId);
        if (!state.task || !rootTask) return [];

        return state.task.drones.map((drone: Drone) => {
            const lastImage = drone.images && drone.images.length > 0 ? drone.images[drone.images.length - 1] : null;
            let fallbackImage = null;

            if (!lastImage) {
                const rootDrone = rootTask.drones.find((rootDrone: Drone) => rootDrone.id === drone.id);
                if (rootDrone && rootDrone.images && rootDrone.images.length > 0) {
                    fallbackImage = rootDrone.images[rootDrone.images.length - 1];
                }
            }

            return {
                drone_id: drone.id,
                drone_name: drone.name,
                last_image: lastImage || fallbackImage
            };
        });
    },

};

const actions: ActionTree<TaskImagesState, RootState> = {
    async fetchTaskImages({ commit, dispatch, rootState }, taskId: number) {
        commit('setLoading', true);
        try {
            const task = rootState.tasks.tasks.find((task: Task) => task.id === taskId) || null;
            if (task) {
                commit('setTask', task);
                dispatch('initSSE', taskId);
            } else {
                commit('setError', 'Task not found');
            }
        } catch (error: any) {
            commit('setError', error.message);
        } finally {
            commit('setLoading', false);
        }
    },

    async initSSE({ commit }, taskId: number) {
        if (state.sseClient) return;
        const sseClient = new SSEClient(`/tasks/${taskId}/images`, true);
        sseClient.addListener((data) => {
            const { id, task_id, drone_id, image_path } = data;
            commit('updateDroneImage', { id, task_id, drone_id, image_path });
        });
        commit('setSSEClient', sseClient);
    },

    async stopSSE({ commit }) {
        if (state.sseClient) {
            state.sseClient.close();
            commit('setSSEClient', null);
        }
    },
    updateTaskFromSSE({ commit }, task: Task) {
        commit('setTask', task);
    },
};

const mutations: MutationTree<TaskImagesState> = {
    setTask(state, task: Task) {
        state.task = task;
    },
    setLoading(state, loading: boolean) {
        state.loading = loading;
    },
    setError(state, error: string | null) {
        state.error = error;
    },
    setSSEClient(state, sseClient: SSEClient | null) {
        state.sseClient = sseClient;
    },
    updateDroneImage(state, { id, task_id, drone_id, image_path }) {
        const drone = state.task?.drones.find(d => d.id === drone_id);
        if (drone) {
            if (!drone.images) {
                drone.images = [];
            }
            drone.images.push({ id, task_id, drone_id, image_path });
        }
    }
};

const taskImages: Module<TaskImagesState, RootState> = {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};

export default taskImages;
