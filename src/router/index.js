import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterFormView from '../views/RegisterFormView.vue'
import LoginFormView from '../views/LoginFormView.vue'
import LogoutView from '../views/LogoutView.vue'
import ExploreView from '../views/ExploreView.vue'
import NewPostView from '../views/NewPostView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/register',
      name: 'RegisterFormView',
      component: RegisterFormView
    },
    {
      path: '/posts/new',
      name: 'NewPostView',
      component: NewPostView
    },
    {
      path: '/explore',
      name: 'ExploreView',
      component: ExploreView
    },
    {
      path: '/users/user_id',
      name: 'ProfileView',
      component: ProfileView
    },
    {
      path: '/login',
      name: 'LoginFormView',
      component: LoginFormView
    },
    {
      path: '/logout',
      name: 'LogoutView',
      component: LogoutView
    }
  ]
})

export default router
