import { ref } from 'vue'
import { defineStore } from 'pinia'

import { getCurrentUser, type UserDetail } from '@/services/api'

export const useUserStore = defineStore('user', () => {
  const user = ref<UserDetail | null>(null)

  async function fetchUser() {
    const response = await getCurrentUser()
    user.value = response.data
  }

  function resetUser() {
    user.value = null
  }

  return {
    user,
    fetchUser,
    resetUser,
  }
})
