<template>
  <div class="dashboard">
    <header>
      <h1>族谱系统</h1>
      <button @click="handleLogout">退出登录</button>
    </header>
    <main>
      <p>欢迎回来！族谱管理功能将在 Phase 2 中实现。</p>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.dashboard { max-width: 900px; margin: 0 auto; padding: 24px; }
header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 16px; margin-bottom: 24px; }
h1 { font-size: 22px; }
button { padding: 8px 16px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer; }
button:hover { background: #dc2626; }
</style>
