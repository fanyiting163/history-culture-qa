<template>
  <section class="page">
    <h1>知识库</h1>
    <p class="lead">上传、切分和入库走 `/api/documents`。接口已留在后端，这一步还不能写入向量库。</p>
    <el-upload drag disabled action="#">
      <div class="upload-text">文档上传将在向量问答阶段打开</div>
    </el-upload>
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
.upload-text {
  color: var(--el-text-color-secondary);
}
</style>
