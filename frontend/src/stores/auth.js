import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'))
  const isAuthenticated = computed(() => !!token.value)

  async function register(username, email, password) {
    const { data } = await api.post('/api/v1/auth/register', { username, email, password })
    token.value = data.access_token
    localStorage.setItem('token', data.access_token)
  }

  async function login(email, password) {
    const { data } = await api.post('/api/v1/auth/login', { email, password })
    token.value = data.access_token
    localStorage.setItem('token', data.access_token)
  }

  function logout() {
    token.value = null
    localStorage.removeItem('token')
  }

  return { token, isAuthenticated, register, login, logout }
})
