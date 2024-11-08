import axios from 'axios'

import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { refreshLogin, URLS } from './api'

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
})

client.interceptors.request.use(
  config => {
    const authStore = useAuthStore()
    const token = authStore.accessToken
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  },
)

client.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    const { config, response } = error

    if (
      response?.status === 401 &&
      response.data.code === 'token_not_valid' &&
      config?.url !== URLS.refreshLogin &&
      config._retry !== true &&
      (await tryRefreshToken())
    ) {
      config._retry = true
      return client(config)
    }

    return Promise.reject(error)
  },
)

let refreshPromise: Promise<boolean> | null = null

async function tryRefreshToken() {
  if (refreshPromise) {
    return refreshPromise
  }

  const authStore = useAuthStore()
  const userStore = useUserStore()
  const refreshToken = authStore.refreshToken
  if (!refreshToken) {
    return false
  }

  refreshPromise = (async () => {
    try {
      const response = await refreshLogin({ refresh: refreshToken })
      authStore.login(response.data)
      return true
    } catch (error) {
      console.error('Failed to refresh token', error)
      authStore.logout()
      userStore.resetUser()
      return false
    } finally {
      refreshPromise = null
    }
  })()
  return refreshPromise
}

export default client
