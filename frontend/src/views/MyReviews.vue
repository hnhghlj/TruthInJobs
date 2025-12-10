<template>
  <div class="my-reviews-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">我的评价</h1>
        <el-button type="primary" @click="$router.push('/reviews/create')">
          <el-icon><Plus /></el-icon>
          发布新评价
        </el-button>
      </div>
      
      <div v-loading="loading" class="reviews-list">
        <el-card
          v-for="review in reviews"
          :key="review.id"
          class="review-card"
        >
          <template #header>
            <div class="card-header">
              <div>
                <h3 class="review-title">{{ review.title }}</h3>
                <span class="company-name">{{ review.company_name }}</span>
              </div>
              <el-tag :type="getStatusType(review.moderation_status)">
                {{ getStatusText(review.moderation_status) }}
              </el-tag>
            </div>
          </template>
          
          <div class="review-info">
            <div class="rating-row">
              <span class="label">综合评分：</span>
              <el-rate v-model="review.overall_rating" disabled />
            </div>
            <div class="info-row">
              <span class="label">职位：</span>
              <span>{{ review.job_title }}</span>
            </div>
            <div class="info-row">
              <span class="label">发布时间：</span>
              <span>{{ formatDate(review.created_at) }}</span>
            </div>
          </div>
          
          <div class="review-stats">
            <span>
              <el-icon><View /></el-icon>
              {{ review.view_count }} 浏览
            </span>
            <span>
              <el-icon><ChatDotRound /></el-icon>
              {{ review.comment_count }} 评论
            </span>
            <span>
              <el-icon><Star /></el-icon>
              {{ review.helpful_count }} 有用
            </span>
          </div>
          
          <div class="review-actions">
            <el-button
              size="small"
              @click="viewReview(review.id)"
            >
              查看详情
            </el-button>
            <el-button
              v-if="review.moderation_status === 'pending'"
              size="small"
              type="danger"
              @click="handleDelete(review)"
            >
              删除
            </el-button>
          </div>
        </el-card>
        
        <el-empty
          v-if="!loading && reviews.length === 0"
          description="暂无评价"
        >
          <el-button type="primary" @click="$router.push('/reviews/create')">
            发布第一条评价
          </el-button>
        </el-empty>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api'
import { Plus, View, ChatDotRound, Star } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const reviews = ref([])

const loadMyReviews = async () => {
  loading.value = true
  try {
    const response = await api.getMyReviews()
    reviews.value = response.data.map(r => ({
      ...r,
      overall_rating: Number(r.overall_rating)
    }))
  } catch (error) {
    console.error('Failed to load reviews:', error)
  } finally {
    loading.value = false
  }
}

const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return texts[status] || status
}

const viewReview = (id) => {
  router.push(`/reviews/${id}`)
}

const handleDelete = async (review) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条评价吗？此操作不可恢复。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
  } catch {
    return
  }
  
  try {
    await api.deleteReview(review.id)
    ElMessage.success('删除成功')
    loadMyReviews()
  } catch (error) {
    console.error('Failed to delete review:', error)
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadMyReviews()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.review-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.review-title {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
}

.company-name {
  font-size: 14px;
  color: #909399;
}

.review-info {
  margin-bottom: 16px;
}

.rating-row,
.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.label {
  font-weight: 500;
  color: #606266;
}

.review-stats {
  display: flex;
  gap: 24px;
  padding: 12px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
  margin-bottom: 16px;
  font-size: 14px;
  color: #909399;
}

.review-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.review-actions {
  display: flex;
  gap: 12px;
}
</style>
