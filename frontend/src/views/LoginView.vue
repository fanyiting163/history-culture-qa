<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const message = ref('')

function submit() {
  if (!username.value || !password.value) {
    message.value = '请填写账号和密码。登录接口下一步才会签发 JWT。'
    return
  }
  message.value = '登录接口下一步才会签发 JWT。'
}

function back() {
  router.push('/chat')
}
</script>

<template>
  <main class="login">
    <el-card class="card">
      <h1>登录</h1>
      <p class="lead">账号体系还没接上。可以先回到问答页确认后端健康检查。</p>
      <el-form label-position="top" @submit.prevent="submit">
        <el-form-item label="账号">
          <el-input v-model="username" autocomplete="username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="password" type="password" show-password autocomplete="current-password" />
        </el-form-item>
        <el-button type="primary" native-type="submit">登录</el-button>
        <el-button @click="back">返回</el-button>
      </el-form>
      <p v-if="message" class="message">{{ message }}</p>
    </el-card>
  </main>
</template>

<style scoped>
.login {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: var(--el-bg-color-page);
}
.card {
  width: 380px;
}
h1 {
  margin: 0 0 8px;
  font-size: 22px;
}
.lead,
.message {
  color: var(--el-text-color-secondary);
}
.lead {
  margin: 0 0 16px;
}
.message {
  margin: 16px 0 0;
}
</style>
