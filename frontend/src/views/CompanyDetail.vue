<template>
  <div class="company-detail-page">
    <div class="container" v-loading="loading">
      <div v-if="company" class="company-detail">
        <!-- Company Header -->
        <div class="company-header card">
          <div class="company-logo">
            <img v-if="company.logo" :src="company.logo" :alt="company.name" />
            <el-icon v-else :size="60"><OfficeBuilding /></el-icon>
          </div>
          
          <div class="company-info">
            <h1 class="company-name">
              {{ company.name }}
              <el-tag v-if="company.is_verified" type="success">已认证</el-tag>
            </h1>
            
            <div class="company-rating">
              <el-rate v-model="company.average_rating" disabled show-score />
              <span class="review-count">基于 {{ company.review_count }} 条评价</span>
            </div>
            
            <div class="company-meta">
              <div class="meta-item">
                <el-icon><Briefcase /></el-icon>
                <span>{{ company.industry_name }}</span>
              </div>
              <div class="meta-item" v-if="company.size">
                <el-icon><User /></el-icon>
                <span>{{ company.size }}</span>
              </div>
              <div class="meta-item" v-if="company.location">
                <el-icon><Location /></el-icon>
                <span>{{ company.location }}</span>
              </div>
              <div class="meta-item" v-if="company.founded_year">
                <el-icon><Calendar /></el-icon>
                <span>成立于 {{ company.founded_year }} 年</span>
              </div>
            </div>
            
            <div class="company-actions">
              <el-button type="primary" @click="handleWriteReview">
                <el-icon><Edit /></el-icon>
                写评价
              </el-button>
              <el-button v-if="company.website" @click="openWebsite">
                <el-icon><Link /></el-icon>
                官网
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- Company Description -->
        <div v-if="company.description" class="company-description card">
          <h2 class="section-title">公司简介</h2>
          <p>{{ company.description }}</p>
        </div>
        
        <!-- Reviews -->
        <div class="company-reviews">
          <div class="section-header">
            <h2 class="section-title">员工评价 ({{ reviews.length }})</h2>
            <el-select v-model="reviewsOrdering" @change="loadReviews">
              <el-option label="最新发布" value="-created_at" />
              <el-option label="评分最高" value="-overall_rating" />
              <el-option label="最受欢迎" value="-helpful_count" />
            </el-select>
          </div>
          
          <div v-loading="reviewsLoading" class="reviews-list">
            <div
              v-for="review in reviews"
              :key="review.id"
              class="review-item card"
              @click="$router.push(`/reviews/${review.id}`)"
            >
              <div class="review-header">
                <div class="review-user">
                  <el-avatar :size="40">{{ review.user_info.username[0] }}</el-avatar>
                  <div>
                    <div class="user-name">{{ review.user_info.username }}</div>
                    <div class="review-meta">
                      <span v-if="review.job_title">{{ review.job_title }}</span>
                      <span>·</span>
                      <span>{{ review.employment_status === 'current' ? '在职' : '离职' }}</span>
                    </div>
                  </div>
                </div>
                <div class="review-rating">
                  <el-rate v-model="review.overall_rating" disabled />
                </div>
              </div>
              
              <h3 class="review-title">{{ review.title }}</h3>
              
              <div class="review-ratings">
                <div class="rating-item">
                  <span>福利待遇</span>
                  <el-rate v-model="review.welfare_rating" disabled show-score />
                </div>
                <div class="rating-item">
                  <span>工作环境</span>
                  <el-rate v-model="review.environment_rating" disabled show-score />
                </div>
                <div class="rating-item">
                  <span>发展机会</span>
                  <el-rate v-model="review.development_rating" disabled show-score />
                </div>
                <div class="rating-item">
                  <span>管理水平</span>
                  <el-rate v-model="review.management_rating" disabled show-score />
                </div>
              </div>
              
              <div class="review-footer">
                <span>{{ formatDate(review.created_at) }}</span>
                <span>
                  <el-icon><View /></el-icon>
                  {{ review.view_count }}
                </span>
                <span>
                  <el-icon><ChatDotRound /></el-icon>
                  {{ review.comment_count }}
                </span>
                <span>
                  <el-icon><Star /></el-icon>
                  {{ review.helpful_count }}
                </span>
              </div>
            </div>
            
            <el-empty v-if="!reviewsLoading && reviews.length === 0" description="暂无评价" />
          </div>
        </div>
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
  OfficeBuilding, Briefcase, User, Location, Calendar,
  Edit, Link, View, ChatDotRound, Star
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const reviewsLoading = ref(false)
const company = ref(null)
const reviews = ref([])
const reviewsOrdering = ref('-created_at')

const companyId = computed(() => route.params.id)

const loadCompany = async () => {
  loading.value = true
  try {
    const response = await api.getCompany(companyId.value)
    company.value = {
      ...response.data,
      average_rating: Number(response.data.average_rating)
    }
  } catch (error) {
    console.error('Failed to load company:', error)
    ElMessage.error('公司不存在')
    router.push('/companies')
  } finally {
    loading.value = false
  }
}

const loadReviews = async () => {
  reviewsLoading.value = true
  try {
    const response = await api.getReviews({
      company: companyId.value,
      ordering: reviewsOrdering.value
    })
    reviews.value = response.data.results.map(r => ({
      ...r,
      overall_rating: Number(r.overall_rating),
      welfare_rating: Number(r.welfare_rating),
      environment_rating: Number(r.environment_rating),
      development_rating: Number(r.development_rating),
      management_rating: Number(r.management_rating)
    }))
  } catch (error) {
    console.error('Failed to load reviews:', error)
  } finally {
    reviewsLoading.value = false
  }
}

const handleWriteReview = () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/auth/login')
    return
  }
  router.push(`/reviews/create?company=${companyId.value}`)
}

const openWebsite = () => {
  if (company.value.website) {
    window.open(company.value.website, '_blank')
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadCompany()
  loadReviews()
})
</script>

<style scoped>
.company-header {
  display: flex;
  gap: 32px;
  padding: 32px;
  margin-bottom: 24px;
}

.company-logo {
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 12px;
  flex-shrink: 0;
}

.company-logo img {
  max-width: 100%;
  max-height: 100%;
}

.company-info {
  flex: 1;
}

.company-name {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.company-rating {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.review-count {
  color: #666;
}

.company-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 24px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
}

.company-actions {
  display: flex;
  gap: 12px;
}

.company-description {
  padding: 24px;
  margin-bottom: 24px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
}

.company-reviews {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.review-item {
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s;
}

.review-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.review-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-name {
  font-weight: 500;
}

.review-meta {
  font-size: 14px;
  color: #999;
  display: flex;
  gap: 4px;
}

.review-title {
  font-size: 18px;
  margin-bottom: 16px;
}

.review-ratings {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.rating-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: #f9f9f9;
  border-radius: 4px;
}

.review-footer {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 14px;
  color: #999;
}

.review-footer span {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>

