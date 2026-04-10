<template>
  <div class="auth-container">
    <h2>注册</h2>
    <form @submit.prevent="submit">
      <div class="field">
        <label>用户名</label>
        <input v-model="username" placeholder="用户名" required />
      </div>
      <div class="field">
        <label>邮箱</label>
        <input v-model="email" type="email" placeholder="your@email.com" required />
      </div>
      <div class="field">
        <label>密码</label>
        <input v-model="password" type="password" placeholder="••••••••" required />
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <button type="submit">注册</button>
    </form>
    <p>已有账号？<router-link to="/login">登录</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

async function submit() {
  error.value = ''
  try {
    await auth.register(username.value, email.value, password.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || '注册失败，请重试'
  }
}
</script>

<style scoped>
.auth-container { max-width: 360px; margin: 80px auto; padding: 24px; border: 1px solid #ddd; border-radius: 8px; }
h2 { margin-bottom: 20px; }
.field { margin-bottom: 14px; display: flex; flex-direction: column; gap: 4px; }
input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; }
button { width: 100%; padding: 10px; background: #4f46e5; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 15px; }
button:hover { background: #4338ca; }
.error { color: red; font-size: 13px; }
p { margin-top: 14px; font-size: 14px; }
</style>
