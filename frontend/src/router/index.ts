import { createRouter, createWebHistory } from 'vue-router'
import ChatView from '../views/ChatView.vue'
import KnowledgeView from '../views/KnowledgeView.vue'
import GraphView from '../views/GraphView.vue'
import AdminView from '../views/AdminView.vue'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/chat' },
    { path: '/chat', component: ChatView },
    { path: '/knowledge', component: KnowledgeView },
    { path: '/graph', component: GraphView },
    { path: '/admin', component: AdminView },
    { path: '/login', component: LoginView },
  ],
})

export default router
