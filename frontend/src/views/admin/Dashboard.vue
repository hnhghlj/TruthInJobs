<template>
  <div class="admin-dashboard">
    <h1 class="page-title">审核统计</h1>
    
    <div v-loading="loading" class="dashboard-content">
      <el-row :gutter="24" class="stats-row">
        <el-col :span="8">
          <el-card class="stat-card pending">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon :size="48"><Clock /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">待审核评价</div>
                <div class="stat-value">{{ stats.pending_reviews }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card class="stat-card pending">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon :size="48"><ChatDotRound /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">待审核评论</div>
                <div class="stat-value">{{ stats.pending_comments }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card class="stat-card warning">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon :size="48"><Warning /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">待处理举报</div>
                <div class="stat-value">{{ stats.pending_reports }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <el-row :gutter="24" class="stats-row">
        <el-col :span="12">
          <el-card class="stat-card success">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon :size="48"><Select /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">今日已审核评价</div>
                <div class="stat-value">{{ stats.approved_reviews_today }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card class="stat-card success">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon :size="48"><Select /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-label">今日已审核评论</div>
                <div class="stat-value">{{ stats.approved_comments_today }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <el-row :gutter="24">
        <el-col :span="24">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>快捷操作</span>
              </div>
            </template>
            
            <div class="quick-actions">
              <el-button
                type="warning"
                size="large"
                @click="$router.push('/admin/reviews')"
              >
                <el-icon><Document /></el-icon>
                审核评价
              </el-button>
              
              <el-button
                type="warning"
                size="large"
                @click="$router.push('/admin/comments')"
              >
                <el-icon><ChatDotRound /></el-icon>
                审核评论
              </el-button>
              
              <el-button
                type="danger"
                size="large"
                @click="$router.push('/admin/reports')"
              >
                <el-icon><Warning /></el-icon>
                处理举报
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import {
  Clock, ChatDotRound, Warning, Select, Document
} from '@element-plus/icons-vue'

const loading = ref(false)
const stats = ref({
  pending_reviews: 0,
  pending_comments: 0,
  pending_reports: 0,
  approved_reviews_today: 0,
  approved_comments_today: 0
})

const loadStatistics = async () => {
  loading.value = true
  try {
    const response = await api.getModerationStatistics()
    stats.value = response.data
  } catch (error) {
    console.error('Failed to load statistics:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStatistics()
  // 自动刷新统计数据
  setInterval(loadStatistics, 30000) // 每30秒刷新一次
})
</script>

<style scoped>
.page-title {
  font-size: 24px;
  margin-bottom: 24px;
}

.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.stat-card.pending {
  border-left: 4px solid #e6a23c;
}

.stat-card.warning {
  border-left: 4px solid #f56c6c;
}

.stat-card.success {
  border-left: 4px solid #67c23a;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 24px;
}

.stat-icon {
  color: #909399;
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quick-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
</style>

