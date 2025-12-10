import axios from 'axios'
import { ElMessage } from 'element-plus'

const instance = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器
instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
instance.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      const { status, data } = error.response
      
      if (status === 401) {
        ElMessage.error('请先登录')
        localStorage.removeItem('token')
        window.location.href = '/auth/login'
      } else if (status === 403) {
        ElMessage.error('没有权限访问')
      } else if (status === 404) {
        ElMessage.error('请求的资源不存在')
      } else if (status >= 500) {
        ElMessage.error('服务器错误，请稍后重试')
      } else {
        const message = data.detail || data.message || '请求失败'
        ElMessage.error(message)
      }
    } else {
      ElMessage.error('网络错误，请检查您的网络连接')
    }
    return Promise.reject(error)
  }
)

// API 方法
const api = {
  // 设置 token
  setAuthToken(token) {
    if (token) {
      instance.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      delete instance.defaults.headers.common['Authorization']
    }
  },
  
  // 用户相关
  login: (data) => instance.post('/accounts/login/', data),
  register: (data) => instance.post('/accounts/register/', data),
  getCurrentUser: () => instance.get('/accounts/me/'),
  updateProfile: (data) => instance.put('/accounts/profile/', data),
  changePassword: (data) => instance.post('/accounts/change-password/', data),
  
  // 公司相关
  getCompanies: (params) => instance.get('/companies/', { params }),
  getCompany: (id) => instance.get(`/companies/${id}/`),
  createCompany: (data) => instance.post('/companies/', data),
  updateCompany: (id, data) => instance.put(`/companies/${id}/`, data),
  
  // 行业相关
  getIndustries: () => instance.get('/companies/industries/'),
  
  // 评价相关
  getReviews: (params) => instance.get('/reviews/reviews/', { params }),
  getReview: (id) => instance.get(`/reviews/reviews/${id}/`),
  createReview: (data) => instance.post('/reviews/reviews/', data),
  updateReview: (id, data) => instance.put(`/reviews/reviews/${id}/`, data),
  deleteReview: (id) => instance.delete(`/reviews/reviews/${id}/`),
  markReviewHelpful: (id) => instance.post(`/reviews/reviews/${id}/mark_helpful/`),
  getMyReviews: () => instance.get('/reviews/reviews/my_reviews/'),
  uploadReviewImage: (id, data) => instance.post(`/reviews/reviews/${id}/upload_image/`, data),
  
  // 评论相关
  getComments: (params) => instance.get('/reviews/comments/', { params }),
  createComment: (data) => instance.post('/reviews/comments/', data),
  getReplies: (id) => instance.get(`/reviews/comments/${id}/replies/`),
  markCommentHelpful: (id) => instance.post(`/reviews/comments/${id}/mark_helpful/`),
  uploadCommentImage: (id, data) => instance.post(`/reviews/comments/${id}/upload_image/`, data),
  
  // 审核相关
  getPendingReviews: () => instance.get('/moderation/pending_reviews/'),
  getPendingComments: () => instance.get('/moderation/pending_comments/'),
  moderateReview: (data) => instance.post('/moderation/moderate_review/', data),
  moderateComment: (data) => instance.post('/moderation/moderate_comment/', data),
  getModerationStatistics: () => instance.get('/moderation/statistics/'),
  
  // 举报相关
  getReports: (params) => instance.get('/moderation/reports/', { params }),
  createReport: (data) => instance.post('/moderation/reports/', data),
  handleReport: (id, data) => instance.post(`/moderation/reports/${id}/handle/`, data)
}

export default api

