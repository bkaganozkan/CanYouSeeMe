import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Dashboard from '@/views/DashboardView.vue'
import Admin from '@/views/AdminView.vue'
import Login from '@/views/Auth/LoginView.vue'
import Register from '@/views/Auth/RegisterView.vue'
import store from '@/store/index';
import MainView from '@/views/MainView.vue'
import TaskDetailsPage from '@/views/TaskDetailsPage.vue';
import Page404Error from '@/views/Error/Page404Error.vue';

import { showUnauthorizedDialog } from '@/utils/unauthorizedHelper';

const routes: Array<RouteRecordRaw> = [
  { path: '/login', name: 'Login', component: Login, meta: { requiresAuth: false } },
  { path: '/register', name: 'Register', component: Register, meta: { requiresAuth: false } },
  {
    path: '/',
    component: MainView,
    meta: { requiresAuth: true, roles: ['user', 'admin'] },
    children: [
      { path: 'admin', name: 'Admin', component: Admin, meta: { requiresAuth: true, roles: ['admin'] } },
      { path: 'dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true, roles: ['user', 'admin'] } },
      {
        path: 'tasks/:id', name: 'TaskDetailsPage', component: TaskDetailsPage,
        props: route => ({ id: Number(route.params.id) }),
        meta: { requiresAuth: true, roles: ['user', 'admin'] }
      }
    ],
  },
  { path: '/:pathMatch(.*)*', name: 'Page404Error', component: Page404Error }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('authToken');
  const userRole = store.getters['auth/userRole'];

  if ((to.path === '/login' || to.path === '/register') && token) {
    return next('/');
  }

  if(to.name !== 'TaskDetailsPage') {
    store.dispatch('images/stopSSE')
  }

  if (token && userRole) {
    store.dispatch('drones/initSSE')
    store.dispatch('tasks/initSSE')
  }
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next('/login');
    } else if (to.meta.roles && Array.isArray(to.meta.roles) && !to.meta.roles.includes(userRole)) {
      store.commit('auth/setUnauthorized', true);
      showUnauthorizedDialog('Unauthorized', 'Trying to Access Unauthorized Page')
      next(from.fullPath);
    } else {
      store.commit('auth/setUnauthorized', false);
      next();
    }
  } else {
    return next();
  }
});

export default router;