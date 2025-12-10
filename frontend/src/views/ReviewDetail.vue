<template>
  <div class="review-detail-page">
    <div class="container" v-loading="loading">
      <div v-if="review" class="review-detail">
        <!-- 返回按钮 -->
        <el-button @click="$router.back()" class="back-btn">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        
        <!-- 评价头部 -->
        <el-card class="review-header">
          <div class="company-info" @click="goToCompany">
            <h3 class="company-name">{{ review.company_name }}</h3>
            <el-icon><ArrowRight /></el-icon>
          </div>
          
          <h1 class="review-title">{{ review.title }}</h1>
          
          <div class="review-meta">
            <div class="author-info">
              <el-avatar :size="40">{{ review.user_info.username[0] }}</el-avatar>
              <div>
                <div class="author-name">{{ review.user_info.username }}</div>
                <div class="job-info">
                  {{ review.job_title }}
                  <span>·</span>
                  {{ review.employment_status === 'current' ? '在职' : '离职' }}
                  <span v-if="review.work_years">· {{ review.work_years }} 年</span>
                </div>
              </div>
            </div>
            <div class="review-date">{{ formatDate(review.created_at) }}</div>
          </div>
          
          <el-divider />
          
          <div class="ratings-grid">
            <div class="rating-item">
              <span class="rating-label">综合评分</span>
              <el-rate v-model="review.overall_rating" disabled show-score />
            </div>
            <div class="rating-item">
              <span class="rating-label">福利待遇</span>
              <el-rate v-model="review.welfare_rating" disabled show-score />
            </div>
            <div class="rating-item">
              <span class="rating-label">工作环境</span>
              <el-rate v-model="review.environment_rating" disabled show-score />
            </div>
            <div class="rating-item">
              <span class="rating-label">发展机会</span>
              <el-rate v-model="review.development_rating" disabled show-score />
            </div>
            <div class="rating-item">
              <span class="rating-label">管理水平</span>
              <el-rate v-model="review.management_rating" disabled show-score />
            </div>
          </div>
        </el-card>
        
        <!-- 评价内容 -->
        <el-card class="review-content">
          <div v-html="review.content"></div>
        </el-card>
        
        <!-- 操作栏 -->
        <el-card class="review-actions">
          <div class="action-buttons">
            <el-button @click="handleHelpful" :disabled="hasMarkedHelpful">
              <el-icon><Star /></el-icon>
              有用 ({{ review.helpful_count }})
            </el-button>
            <el-button @click="handleShare">
              <el-icon><Share /></el-icon>
              分享
            </el-button>
          </div>
          <div class="view-count">
            <el-icon><View /></el-icon>
            {{ review.view_count }} 次浏览
          </div>
        </el-card>
        
        <!-- 评论区 -->
        <el-card class="comments-section">
          <h3 class="section-title">评论 ({{ review.comment_count }})</h3>
          
          <!-- 发表评论 -->
          <div v-if="userStore.isLoggedIn" class="comment-form">
            <el-input
              v-model="commentContent"
              type="textarea"
              :rows="3"
              placeholder="写下你的评论..."
            />
            <div class="comment-actions">
              <el-checkbox v-model="commentAnonymous">匿名评论</el-checkbox>
              <el-button
                type="primary"
                :loading="commentSubmitting"
                @click="handleCommentSubmit"
              >
                发表评论
              </el-button>
            </div>
          </div>
          <div v-else class="login-tip">
            <el-button text type="primary" @click="$router.push('/auth/login')">
              登录后发表评论
            </el-button>
          </div>
          
          <!-- 评论列表 -->
          <div class="comments-list">
            <div
              v-for="comment in review.comments"
              :key="comment.id"
              class="comment-item"
            >
              <el-avatar :size="36">{{ comment.user_info.username[0] }}</el-avatar>
              <div class="comment-content">
                <div class="comment-header">
                  <span class="comment-author">{{ comment.user_info.username }}</span>
                  <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                </div>
                <div class="comment-text">{{ comment.content }}</div>
                <div class="comment-footer">
                  <el-button text size="small" @click="handleCommentHelpful(comment)">
                    <el-icon><Star /></el-icon>
                    有用 ({{ comment.helpful_count }})
                  </el-button>
                </div>
              </div>
            </div>
            
            <el-empty
              v-if="review.comments && review.comments.length === 0"
              description="暂无评论"
            />
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import api from '@/api'
import {
  ArrowLeft, ArrowRight, Star, Share, View
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const review = ref(null)
const hasMarkedHelpful = ref(false)
const commentContent = ref('')
const commentAnonymous = ref(true)
const commentSubmitting = ref(false)

const reviewId = computed(() => route.params.id)

const loadReview = async () => {
  loading.value = true
  try {
    const response = await api.getReview(reviewId.value)
    review.value = {
      ...response.data,
      overall_rating: Number(response.data.overall_rating),
      welfare_rating: Number(response.data.welfare_rating),
      environment_rating: Number(response.data.environment_rating),
      development_rating: Number(response.data.development_rating),
      management_rating: Number(response.data.management_rating)
    }
  } catch (error) {
    console.error('Failed to load review:', error)
    ElMessage.error('评价不存在')
    router.push('/')
  } finally {
    loading.value = false
  }
}

const handleHelpful = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  try {
    const response = await api.markReviewHelpful(reviewId.value)
    review.value.helpful_count = response.data.helpful_count
    hasMarkedHelpful.value = true
    ElMessage.success('感谢您的反馈')
  } catch (error) {
    console.error('Failed to mark helpful:', error)
  }
}

const handleShare = () => {
  const url = window.location.href
  navigator.clipboard.writeText(url)
  ElMessage.success('链接已复制到剪贴板')
}

const handleCommentSubmit = async () => {
  if (!commentContent.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  
  commentSubmitting.value = true
  try {
    await api.createComment({
      review: reviewId.value,
      content: commentContent.value,
      is_anonymous: commentAnonymous.value
    })
    
    ElMessage.success('评论提交成功，等待审核')
    commentContent.value = ''
    
    // 重新加载评价
    setTimeout(() => {
      loadReview()
    }, 1000)
  } catch (error) {
    console.error('Failed to create comment:', error)
  } finally {
    commentSubmitting.value = false
  }
}

const handleCommentHelpful = async (comment) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  try {
    const response = await api.markCommentHelpful(comment.id)
    comment.helpful_count = response.data.helpful_count
    ElMessage.success('感谢您的反馈')
  } catch (error) {
    console.error('Failed to mark comment helpful:', error)
  }
}

const goToCompany = () => {
  router.push(`/companies/${review.value.company}`)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadReview()
})
</script>

<style scoped>
.back-btn {
  margin-bottom: 16px;
}

.review-header {
  margin-bottom: 24px;
}

.company-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #409eff;
  cursor: pointer;
  margin-bottom: 16px;
  width: fit-content;
}

.company-info:hover {
  color: #66b1ff;
}

.company-name {
  font-size: 16px;
  margin: 0;
}

.review-title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 24px;
}

.review-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-name {
  font-weight: 500;
  font-size: 16px;
}

.job-info {
  font-size: 14px;
  color: #999;
  display: flex;
  gap: 4px;
}

.review-date {
  color: #999;
}

.ratings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.rating-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rating-label {
  font-weight: 500;
  color: #606266;
}

.review-content {
  margin-bottom: 24px;
  line-height: 1.8;
}

.review-content :deep(h3) {
  margin: 24px 0 16px;
  font-size: 18px;
}

.review-content :deep(p) {
  margin: 12px 0;
}

.review-content :deep(ul) {
  margin: 12px 0;
  padding-left: 24px;
}

.review-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.view-count {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #999;
}

.comments-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 20px;
  margin-bottom: 24px;
}

.comment-form {
  margin-bottom: 32px;
}

.comment-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.login-tip {
  text-align: center;
  padding: 24px;
  background: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 24px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.comment-item {
  display: flex;
  gap: 12px;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 500;
}

.comment-date {
  font-size: 14px;
  color: #999;
}

.comment-text {
  line-height: 1.6;
  margin-bottom: 8px;
}

.comment-footer {
  display: flex;
  gap: 16px;
}
</style>
