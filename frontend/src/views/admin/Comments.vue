<template>
  <div class="admin-comments">
    <h1 class="page-title">评论审核</h1>
    
    <div v-loading="loading" class="comments-list">
      <el-card
        v-for="comment in comments"
        :key="comment.id"
        class="comment-card"
      >
        <template #header>
          <div class="card-header">
            <div>
              <span class="user-name">{{ comment.user_info.username }}</span>
              <span class="divider">·</span>
              <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
            </div>
            <el-tag type="warning">待审核</el-tag>
          </div>
        </template>
        
        <div class="comment-info">
          <div class="info-row">
            <span class="label">评论内容：</span>
          </div>
          <div class="comment-content">
            {{ comment.content }}
          </div>
          
          <div class="info-row" style="margin-top: 16px;">
            <span class="label">所属评价ID：</span>
            <el-button
              text
              type="primary"
              size="small"
              @click="viewReview(comment.review)"
            >
              #{{ comment.review }}
            </el-button>
          </div>
        </div>
        
        <el-divider />
        
        <div class="comment-actions">
          <el-input
            v-model="comment.moderationReason"
            placeholder="审核备注（可选）"
            style="flex: 1; margin-right: 12px;"
          />
          <el-button
            type="success"
            :loading="comment.moderating"
            @click="handleModerate(comment, 'approve')"
          >
            <el-icon><Select /></el-icon>
            通过
          </el-button>
          <el-button
            type="danger"
            :loading="comment.moderating"
            @click="handleModerate(comment, 'reject')"
          >
            <el-icon><Close /></el-icon>
            拒绝
          </el-button>
        </div>
      </el-card>
      
      <el-empty
        v-if="!loading && comments.length === 0"
        description="暂无待审核的评论"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api'
import { Select, Close } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const comments = ref([])

const loadPendingComments = async () => {
  loading.value = true
  try {
    const response = await api.getPendingComments()
    comments.value = response.data.map(c => ({
      ...c,
      moderationReason: '',
      moderating: false
    }))
  } catch (error) {
    console.error('Failed to load pending comments:', error)
  } finally {
    loading.value = false
  }
}

const handleModerate = async (comment, action) => {
  const actionText = action === 'approve' ? '通过' : '拒绝'
  
  try {
    await ElMessageBox.confirm(
      `确认${actionText}这条评论吗？`,
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
  
  comment.moderating = true
  try {
    await api.moderateComment({
      comment_id: comment.id,
      action: action,
      reason: comment.moderationReason
    })
    
    ElMessage.success(`评论已${actionText}`)
    
    // 从列表中移除
    const index = comments.value.findIndex(c => c.id === comment.id)
    if (index > -1) {
      comments.value.splice(index, 1)
    }
  } catch (error) {
    console.error('Failed to moderate comment:', error)
  } finally {
    comment.moderating = false
  }
}

const viewReview = (reviewId) => {
  window.open(`/reviews/${reviewId}`, '_blank')
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadPendingComments()
})
</script>

<style scoped>
.page-title {
  font-size: 24px;
  margin-bottom: 24px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.comment-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-name {
  font-weight: 500;
  font-size: 16px;
}

.divider {
  margin: 0 8px;
  color: #dcdfe6;
}

.comment-time {
  font-size: 14px;
  color: #909399;
}

.comment-info {
  margin-bottom: 16px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.info-row .label {
  font-weight: 500;
  color: #606266;
}

.comment-content {
  padding: 16px;
  background: #f9f9f9;
  border-radius: 4px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.comment-actions {
  display: flex;
  align-items: center;
}
</style>

