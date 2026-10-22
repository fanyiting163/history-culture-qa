import axios from 'axios'

export const http = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export interface HealthResponse {
  status: string
  service: string
  phase: string
}
