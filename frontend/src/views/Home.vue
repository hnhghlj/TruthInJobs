<template>
  <div class="home-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="container">
        <h1 class="hero-title">发现真实的公司福利</h1>
        <p class="hero-subtitle">帮助职场人了解公司真实待遇，做出更明智的职业选择</p>
        
        <div class="search-box">
          <el-input
            v-model="searchQuery"
            placeholder="搜索公司名称..."
            size="large"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
            <template #append>
              <el-button :icon="Search" @click="handleSearch">搜索</el-button>
            </template>
          </el-input>
        </div>
      </div>
    </div>
    
    <!-- Stats Section -->
    <div class="stats-section">
      <div class="container">
        <el-row :gutter="24">
          <el-col :span="8">
            <div class="stat-card">
              <el-icon class="stat-icon" color="#409eff"><OfficeBuilding /></el-icon>
              <div class="stat-number">{{ stats.companies }}+</div>
              <div class="stat-label">入驻公司</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-card">
              <el-icon class="stat-icon" color="#67c23a"><Document /></el-icon>
              <div class="stat-number">{{ stats.reviews }}+</div>
              <div class="stat-label">真实评价</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-card">
              <el-icon class="stat-icon" color="#e6a23c"><User /></el-icon>
              <div class="stat-number">{{ stats.users }}+</div>
              <div class="stat-label">注册用户</div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
    
    <!-- Hot Companies -->
    <div class="section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">热门公司</h2>
          <el-button text @click="$router.push('/companies')">查看更多 <el-icon><ArrowRight /></el-icon></el-button>
        </div>
        
        <div v-loading="loading.companies" class="companies-grid">
          <div 
            v-for="company in hotCompanies" 
            :key="company.id"
            class="company-card"
            @click="$router.push(`/companies/${company.id}`)"
          >
            <div class="company-logo">
              <img v-if="company.logo" :src="company.logo" :alt="company.name" />
              <el-icon v-else :size="40"><OfficeBuilding /></el-icon>
            </div>
            <h3 class="company-name">{{ company.name }}</h3>
            <div class="company-rating">
              <el-rate v-model="company.average_rating" disabled show-score />
            </div>
            <div class="company-meta">
              <el-tag size="small">{{ company.industry_name }}</el-tag>
              <span class="review-count">{{ company.review_count }} 条评价</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Latest Reviews -->
    <div class="section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">最新评价</h2>
        </div>
        
        <div v-loading="loading.reviews" class="reviews-list">
          <div 
            v-for="review in latestReviews" 
            :key="review.id"
            class="review-card"
            @click="$router.push(`/reviews/${review.id}`)"
          >
            <div class="review-header">
              <div class="review-company">
                <h4>{{ review.company_name }}</h4>
                <span class="review-job">{{ review.job_title }}</span>
              </div>
              <el-rate v-model="review.overall_rating" disabled />
            </div>
            <h3 class="review-title">{{ review.title }}</h3>
            <div class="review-footer">
              <span class="review-author">{{ review.user_info.username }}</span>
              <span class="review-date">{{ formatDate(review.created_at) }}</span>
              <span class="review-views">
                <el-icon><View /></el-icon>
                {{ review.view_count }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { 
  Search, OfficeBuilding, Document, User, ArrowRight, View 
} from '@element-plus/icons-vue'

const router = useRouter()
const searchQuery = ref('')

const stats = ref({
  companies: 0,
  reviews: 0,
  users: 0
})

const hotCompanies = ref([])
const latestReviews = ref([])

const loading = ref({
  companies: false,
  reviews: false
})

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      name: 'companies',
      query: { search: searchQuery.value }
    })
  }
}

const loadHotCompanies = async () => {
  loading.value.companies = true
  try {
    const response = await api.getCompanies({
      ordering: '-review_count',
      page_size: 8
    })
    hotCompanies.value = response.data.results.map(c => ({
      ...c,
      average_rating: Number(c.average_rating)
    }))
    stats.value.companies = response.data.count
  } catch (error) {
    console.error('Failed to load companies:', error)
  } finally {
    loading.value.companies = false
  }
}

const loadLatestReviews = async () => {
  loading.value.reviews = true
  try {
    const response = await api.getReviews({
      ordering: '-created_at',
      page_size: 5
    })
    latestReviews.value = response.data.results.map(r => ({
      ...r,
      overall_rating: Number(r.overall_rating)
    }))
    stats.value.reviews = response.data.count
  } catch (error) {
    console.error('Failed to load reviews:', error)
  } finally {
    loading.value.reviews = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days} 天前`
  if (days < 30) return `${Math.floor(days / 7)} 周前`
  return date.toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadHotCompanies()
  loadLatestReviews()
  stats.value.users = 1000 // Mock data
})
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 80px 0;
  color: white;
  text-align: center;
}

.hero-title {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 20px;
  margin-bottom: 40px;
  opacity: 0.9;
}

.search-box {
  max-width: 600px;
  margin: 0 auto;
}

.stats-section {
  padding: 48px 0;
  background: white;
}

.stat-card {
  text-align: center;
  padding: 24px;
}

.stat-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 16px;
  color: #666;
}

.section {
  padding: 48px 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.section-title {
  font-size: 28px;
  font-weight: 600;
}

.companies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

.company-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #e8e8e8;
}

.company-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}

.company-logo {
  width: 80px;
  height: 80px;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 8px;
}

.company-logo img {
  max-width: 100%;
  max-height: 100%;
}

.company-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
}

.company-rating {
  margin-bottom: 12px;
}

.company-meta {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #999;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.review-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #e8e8e8;
}

.review-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.review-company h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.review-job {
  font-size: 14px;
  color: #666;
}

.review-title {
  font-size: 18px;
  margin-bottom: 16px;
  color: #333;
}

.review-footer {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 14px;
  color: #999;
}

.review-views {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>

