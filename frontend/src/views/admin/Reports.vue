<template>
  <div class="admin-reports">
    <h1 class="page-title">举报处理</h1>
    
    <el-tabs v-model="activeTab" @tab-change="loadReports">
      <el-tab-pane label="待处理" name="pending" />
      <el-tab-pane label="处理中" name="processing" />
      <el-tab-pane label="已处理" name="resolved" />
      <el-tab-pane label="已驳回" name="dismissed" />
    </el-tabs>
    
    <div v-loading="loading" class="reports-list">
      <el-card
        v-for="report in reports"
        :key="report.id"
        class="report-card"
      >
        <template #header>
          <div class="card-header">
            <div>
              <el-tag :type="getReportTypeTag(report.report_type)">
                {{ getReportTypeText(report.report_type) }}
              </el-tag>
              <span class="report-content-type">
                {{ report.content_type_name }}
              </span>
            </div>
            <el-tag :type="getStatusTag(report.status)">
              {{ getStatusText(report.status) }}
            </el-tag>
          </div>
        </template>
        
        <div class="report-info">
          <div class="info-row">
            <span class="label">举报人：</span>
            <span>{{ report.reporter_name }}</span>
          </div>
          <div class="info-row">
            <span class="label">举报时间：</span>
            <span>{{ formatDate(report.created_at) }}</span>
          </div>
          <div class="info-row">
            <span class="label">举报对象：</span>
            <span>{{ report.content_type_name }} #{{ report.object_id }}</span>
          </div>
          <div class="info-row full-width">
            <span class="label">举报说明：</span>
            <p class="report-description">{{ report.description }}</p>
          </div>
          
          <template v-if="report.status !== 'pending'">
            <el-divider />
            <div class="info-row">
              <span class="label">处理人：</span>
              <span>{{ report.handler_name || '未知' }}</span>
            </div>
            <div class="info-row">
              <span class="label">处理时间：</span>
              <span>{{ formatDate(report.handled_at) }}</span>
            </div>
            <div class="info-row full-width" v-if="report.handler_note">
              <span class="label">处理备注：</span>
              <p class="report-description">{{ report.handler_note }}</p>
            </div>
          </template>
        </div>
        
        <div v-if="report.status === 'pending'" class="report-actions">
          <el-input
            v-model="report.handlerNote"
            placeholder="处理备注（可选）"
            style="flex: 1; margin-right: 12px;"
          />
          <el-button
            type="success"
            :loading="report.handling"
            @click="handleReport(report, 'resolve')"
          >
            <el-icon><Select /></el-icon>
            处理完成
          </el-button>
          <el-button
            type="warning"
            :loading="report.handling"
            @click="handleReport(report, 'dismiss')"
          >
            <el-icon><Close /></el-icon>
            驳回举报
          </el-button>
        </div>
      </el-card>
      
      <el-empty
        v-if="!loading && reports.length === 0"
        description="暂无举报"
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
const reports = ref([])
const activeTab = ref('pending')

const loadReports = async () => {
  loading.value = true
  try {
    const response = await api.getReports({ status: activeTab.value })
    reports.value = response.data.map(r => ({
      ...r,
      handlerNote: '',
      handling: false
    }))
  } catch (error) {
    console.error('Failed to load reports:', error)
  } finally {
    loading.value = false
  }
}

const handleReport = async (report, action) => {
  const actionText = action === 'resolve' ? '处理完成' : '驳回'
  
  try {
    await ElMessageBox.confirm(
      `确认${actionText}这条举报吗？`,
      '确认操作',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: action === 'resolve' ? 'success' : 'warning'
      }
    )
  } catch {
    return
  }
  
  report.handling = true
  try {
    await api.handleReport(report.id, {
      action: action,
      handler_note: report.handlerNote
    })
    
    ElMessage.success(`举报已${actionText}`)
    
    // 从列表中移除
    const index = reports.value.findIndex(r => r.id === report.id)
    if (index > -1) {
      reports.value.splice(index, 1)
    }
  } catch (error) {
    console.error('Failed to handle report:', error)
  } finally {
    report.handling = false
  }
}

const getReportTypeTag = (type) => {
  const tags = {
    spam: 'info',
    inappropriate: 'warning',
    false_info: 'danger',
    offensive: 'danger',
    other: 'info'
  }
  return tags[type] || 'info'
}

const getReportTypeText = (type) => {
  const texts = {
    spam: '垃圾信息',
    inappropriate: '不当内容',
    false_info: '虚假信息',
    offensive: '攻击性言论',
    other: '其他'
  }
  return texts[type] || type
}

const getStatusTag = (status) => {
  const tags = {
    pending: 'warning',
    processing: 'info',
    resolved: 'success',
    dismissed: 'info'
  }
  return tags[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待处理',
    processing: '处理中',
    resolved: '已处理',
    dismissed: '已驳回'
  }
  return texts[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadReports()
})
</script>

<style scoped>
.page-title {
  font-size: 24px;
  margin-bottom: 24px;
}

.reports-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 24px;
}

.report-card {
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header > div {
  display: flex;
  align-items: center;
  gap: 12px;
}

.report-content-type {
  font-size: 14px;
  color: #909399;
}

.report-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-row {
  display: flex;
  gap: 8px;
}

.info-row.full-width {
  grid-column: 1 / -1;
  flex-direction: column;
}

.info-row .label {
  font-weight: 500;
  color: #606266;
  min-width: 80px;
}

.report-description {
  padding: 12px;
  background: #f9f9f9;
  border-radius: 4px;
  line-height: 1.6;
  margin: 4px 0 0 0;
  white-space: pre-wrap;
}

.report-actions {
  display: flex;
  align-items: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #eee;
}
</style>
