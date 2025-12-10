import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isModerator = computed(() => {
    return user.value && ['moderator', 'admin'].includes(user.value.user_type)
  })
  
  // 设置认证信息
  function setAuth(authData) {
    token.value = authData.token
    user.value = authData.user
    localStorage.setItem('token', authData.token)
    api.setAuthToken(authData.token)
  }
  
  // 清除认证信息
  function clearAuth() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    api.setAuthToken(null)
  }
  
  // 检查认证状态
  async function checkAuth() {
    if (token.value) {
      try {
        api.setAuthToken(token.value)
        const response = await api.getCurrentUser()
        user.value = response.data
      } catch (error) {
        clearAuth()
      }
    }
  }
  
  // 登录
  async function login(credentials) {
    const response = await api.login(credentials)
    setAuth(response.data)
    return response.data
  }
  
  // 注册
  async function register(userData) {
    const response = await api.register(userData)
    return response.data
  }
  
  // 登出
  function logout() {
    clearAuth()
  }
  
  // 更新用户信息
  async function updateProfile(data) {
    const response = await api.updateProfile(data)
    user.value = response.data
    return response.data
  }
  
  return {
    user,
    token,
    isLoggedIn,
    isModerator,
    setAuth,
    clearAuth,
    checkAuth,
    login,
    register,
    logout,
    updateProfile
  }
})

