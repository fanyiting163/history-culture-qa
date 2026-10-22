import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const loggedIn = computed(() => token.value !== null)

  function setToken(value: string | null) {
    token.value = value
  }

  return { token, loggedIn, setToken }
})
