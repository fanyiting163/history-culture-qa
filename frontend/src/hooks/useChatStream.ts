import { ref } from 'vue'

export function useChatStream() {
  const streaming = ref(false)

  async function ask(question: string): Promise<void> {
    if (!question.trim()) return
    streaming.value = false
    throw new Error('流式问答将在文档入库接通后实现')
  }

  return { streaming, ask }
}
