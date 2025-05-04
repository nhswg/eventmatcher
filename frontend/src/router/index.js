import { createRouter, createWebHistory } from 'vue-router'
import StartView from '../views/StartView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Start',
      component: StartView
    },
    {
      path: '/people/',
      name: 'PeopleView',
      component: () => import('../views/PeopleView.vue')
    },
    {
      path: '/exhibitors/',
      name: 'ExhibitoView',
      component: () => import('../views/ExhibitorView.vue')
    },
  ]
})

export default router
