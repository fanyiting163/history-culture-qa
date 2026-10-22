<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from './hooks/useAuth'

const route = useRoute()
const router = useRouter()
const { loggedIn } = useAuth()
const isLogin = computed(() => route.path === '/login')

const menus = [
  { path: '/chat', label: '智能问答' },
  { path: '/knowledge', label: '知识库' },
  { path: '/graph', label: '图谱' },
  { path: '/admin', label: '管理' },
]
</script>

<template>
  <router-view v-if="isLogin" />
  <el-container v-else class="shell">
    <el-aside width="200px" class="aside">
      <div class="brand">历史文化问答</div>
      <el-menu :default-active="route.path" router>
        <el-menu-item v-for="item in menus" :key="item.path" :index="item.path">
          {{ item.label }}
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span>{{ loggedIn ? '已登录' : '未登录' }}</span>
        <el-button text @click="router.push('/login')">登录</el-button>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.shell {
  min-height: 100vh;
  background: #ffffff;
}
.aside {
  border-right: 1px solid var(--el-border-color);
}
.brand {
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  font-weight: 600;
}
.header {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  border-bottom: 1px solid var(--el-border-color);
}
</style>
