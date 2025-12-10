<template>
  <div class="admin-reviews">
    <h1 class="page-title">评价审核</h1>
    
    <div v-loading="loading" class="reviews-list">
      <el-card
        v-for="review in reviews"
        :key="review.id"
        class="review-card"
      >
        <template #header>
          <div class="card-header">
            <div>
              <h3>{{ review.title }}</h3>
              <span class="company-name">{{ review.company_name }}</span>
            </div>
            <el-tag type="warning">待审核</el-tag>
          </div>
        </template>
        
        <div class="review-info">
          <div class="info-row">
            <span class="label">用户：</span>
            <span>{{ review.user_info.username }}</span>
          </div>
          <div class="info-row">
            <span class="label">职位：</span>
            <span>{{ review.job_title }}</span>
          </div>
          <div class="info-row">
            <span class="label">状态：</span>
            <span>{{ review.employment_status === 'current' ? '在职' : '离职' }}</span>
          </div>
          <div class="info-row">
            <span class="label">综合评分：</span>
            <el-rate v-model="review.overall_rating" disabled />
          </div>
          <div class="info-row">
            <span class="label">提交时间：</span>
            <span>{{ formatDate(review.created_at) }}</span>
          </div>
        </div>
        
        <el-divider />
        
        <div class="review-content">
          <div v-html="review.content"></div>
        </div>
        
        <el-divider />
        
        <div class="review-actions">
          <el-input
            v-model="review.moderationReason"
            placeholder="审核备注（可选）"
            style="flex: 1; margin-right: 12px;"
          />
          <el-button
            type="success"
            :loading="review.moderating"
            @click="handleModerate(review, 'approve')"
          >
            <el-icon><Select /></el-icon>
            通过
          </el-button>
          <el-button
            type="danger"
            :loading="review.moderating"
            @click="handleModerate(review, 'reject')"
          >
            <el-icon><Close /></el-icon>
            拒绝
          </el-button>
        </div>
      </el-card>
      
      <el-empty
        v-if="!loading && reviews.length === 0"
        description="暂无待审核的评价"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api'
import { Select, Close } from '@element-plus/icons-vue'

const loading = ref(false)
const reviews = ref([])

const loadPendingReviews = async () => {
  loading.value = true
  try {
    const response = await api.getPendingReviews()
    reviews.value = response.data.map(r => ({
      ...r,
      overall_rating: Number(r.overall_rating),
      moderationReason: '',
      moderating: false
    }))
  } catch (error) {
    console.error('Failed to load pending reviews:', error)
  } finally {
    loading.value = false
  }
}

const handleModerate = async (review, action) => {
  const actionText = action === 'approve' ? '通过' : '拒绝'
  
  try {
    await ElMessageBox.confirm(
      `确认${actionText}这条评价吗？`,
      '确认操作',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: action === 'approve' ? 'success' : 'warning'
      }
    )
  } catch {
    return
  }
  
  review.moderating = true
  try {
    await api.moderateReview({
      review_id: review.id,
      action: action,
      reason: review.moderationReason
    })
    
    ElMessage.success(`评价已${actionText}`)
    
    // 从列表中移除
    const index = reviews.value.findIndex(r => r.id === review.id)
    if (index > -1) {
      reviews.value.splice(index, 1)
    }
  } catch (error) {
    console.error('Failed to moderate review:', error)
  } finally {
    review.moderating = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadPendingReviews()
})
</script>

<style scoped>
.page-title {
  font-size: 24px;
  margin-bottom: 24px;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.review-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.card-header h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
}

.company-name {
  font-size: 14px;
  color: #909399;
}

.review-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-row .label {
  font-weight: 500;
  color: #606266;
}

.review-content {
  max-height: 300px;
  overflow-y: auto;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 4px;
  line-height: 1.6;
}

.review-actions {
  display: flex;
  align-items: center;
}
</style>

