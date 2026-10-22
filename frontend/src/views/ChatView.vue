<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { http, type HealthResponse } from '../api/http'

const health = ref<HealthResponse | null>(null)
const error = ref('')

onMounted(async () => {
  try {
    const { data } = await http.get<HealthResponse>('/health')
    health.value = data
  } catch {
    error.value = '后端未启动。在 backend 目录运行 uvicorn 后再刷新。'
  }
})
</script>

<template>
  <section class="page">
    <h1>智能问答</h1>
    <p class="lead">这一阶段先确认前后端能连上。上传文档和向量回答在下一步接通。</p>
    <el-alert v-if="health" type="success" :closable="false" show-icon>
      {{ health.service }}已连通，当前阶段：{{ health.phase }}
    </el-alert>
    <el-alert v-else-if="error" type="warning" :closable="false" show-icon>
      {{ error }}
    </el-alert>
    <el-input
      class="ask"
      disabled
      placeholder="提问会在知识库入库后开放"
    />
  </section>
</template>

<style scoped>
.page {
  max-width: 720px;
}
.lead {
  margin: 0 0 16px;
  color: var(--el-text-color-secondary);
}
.ask {
  margin-top: 16px;
}
</style>
