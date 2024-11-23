import { createRouter, createWebHistory } from 'vue-router'

import AppLayout from '@/layout/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('../views/HomeView.vue'),
        },
        {
          path: 'user/center',
          name: 'user-center',
          meta: { requiresAuth: true },
          component: () => import('../views/user/CenterView.vue'),
        },
        {
          path: 'user/settings',
          name: 'user-settings',
          meta: { requiresAuth: true },
          component: () => import('../views/user/SettingsView.vue'),
        },
        {
          path: 'user/profile/:userId(\\d+)',
          name: 'user-profile',
          component: () => import('../views/user/ProfileView.vue'),
          props: route => ({ userId: Number(route.params.userId) }),
        },
        {
          path: 'pub/arxiv/:arxivId/:slug?',
          name: 'pub-arxiv',
          component: () => import('../views/pub/ArxivView.vue'),
          props: true,
        },
        {
          path: 'pub/github/:owner/:repo',
          name: 'pub-github',
          component: () => import('../views/pub/GithubView.vue'),
          props: true,
        },
      ],
    },
    {
      path: '/auth/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
      props: route => ({ redirect: route.query.redirect }),
    },
    {
      path: '/auth/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
    },
    {
      path: '/subscription',
      name: 'subscription',
      component: () => import('../components/SubscriptionPanel.vue'),
    },
  ],
})

router.beforeEach((to, from) => {
  void from
  const authStore = useAuthStore()
  if (to.name === 'login' && authStore.isAuthenticated) {
    return { name: 'home' }
  }
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
})

export default router
