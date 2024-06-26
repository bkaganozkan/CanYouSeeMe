import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import auth from './modules/auth'
import drones from './modules/drones';
import tasks from './modules/tasks';
import  images  from './modules/taskImages'; 


export interface RootState {
  tasks: ReturnType<typeof tasks.state | any>;
  drones: ReturnType<typeof drones.state | any>;
  images: ReturnType<typeof images.state | any>;
}



export default createStore<RootState>({
  modules: {
    auth,
    drones,
    tasks,
    images
  },
  plugins: [createPersistedState({
    key: 'DroneAppState',
    paths: ['auth'],
  })],
});