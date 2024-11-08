import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import type { TokenPair } from '@/services/api'

function parseTokenPair(value: string | null): TokenPair | null {
  if (value) {
    try {
      const { access, refresh } = JSON.parse(value)
      if (typeof access === 'string' && typeof refresh === 'string') {
        return { access, refresh }
      }
    } catch {}
  }

  return null
}

export const useAuthStore = defineStore('auth', () => {
  const STORAGE_KEY = 'tokenPair'

  const tokenPair = ref<TokenPair | null>(null)
  const persistent = ref(true)

  for (const storage of [localStorage, sessionStorage]) {
    const value = parseTokenPair(storage.getItem(STORAGE_KEY))
    if (value) {
      tokenPair.value = value
      persistent.value = storage === localStorage
      break
    }
  }

  const accessToken = computed(() => tokenPair.value?.access ?? null)
  const refreshToken = computed(() => tokenPair.value?.refresh ?? null)
  const isAuthenticated = computed(() => !!tokenPair.value)

  function login(data: TokenPair, remember?: boolean) {
    tokenPair.value = data

    if (typeof remember === 'boolean') {
      persistent.value = remember
    }

    if (persistent.value) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
    } else {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(data))
    }
  }

  function logout() {
    tokenPair.value = null
    localStorage.removeItem(STORAGE_KEY)
    sessionStorage.removeItem(STORAGE_KEY)
  }

  return {
    tokenPair,
    accessToken,
    refreshToken,
    isAuthenticated,
    login,
    logout,
  }
})
