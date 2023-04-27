import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AddUserFormView from '../views/AddUserFormView.vue'
import LoginFormView from '../views/LoginFormView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/user/create',
      name: 'AddUserFormView',
      component: AddUserFormView
    },
    {
      path: '/login',
      name: 'LoginFormView',
      component: LoginFormView
    }
  ]
})

export default router
