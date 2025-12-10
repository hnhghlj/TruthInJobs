<template>
  <div class="companies-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">公司列表</h1>
      </div>
      
      <div class="filters-bar card">
        <el-form :inline="true" :model="filters">
          <el-form-item label="行业">
            <el-select v-model="filters.industry" placeholder="全部行业" clearable @change="handleFilter">
              <el-option
                v-for="industry in industries"
                :key="industry.id"
                :label="industry.name"
                :value="industry.id"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="公司规模">
            <el-select v-model="filters.size" placeholder="全部规模" clearable @change="handleFilter">
              <el-option label="1-50人" value="1-50" />
              <el-option label="51-200人" value="51-200" />
              <el-option label="201-500人" value="201-500" />
              <el-option label="501-1000人" value="501-1000" />
              <el-option label="1001-5000人" value="1001-5000" />
              <el-option label="5000人以上" value="5001+" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="搜索">
            <el-input
              v-model="filters.search"
              placeholder="公司名称/地址"
              clearable
              @keyup.enter="handleFilter"
            >
              <template #append>
                <el-button :icon="Search" @click="handleFilter" />
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item label="排序">
            <el-select v-model="filters.ordering" @change="handleFilter">
              <el-option label="评价数量" value="-review_count" />
              <el-option label="平均评分" value="-average_rating" />
              <el-option label="最新添加" value="-created_at" />
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      
      <div v-loading="loading" class="companies-list">
        <div
          v-for="company in companies"
          :key="company.id"
          class="company-item card"
          @click="$router.push(`/companies/${company.id}`)"
        >
          <div class="company-logo">
            <img v-if="company.logo" :src="company.logo" :alt="company.name" />
            <el-icon v-else :size="48"><OfficeBuilding /></el-icon>
          </div>
          
          <div class="company-info">
            <div class="company-header">
              <h3 class="company-name">
                {{ company.name }}
                <el-tag v-if="company.is_verified" type="success" size="small">已认证</el-tag>
              </h3>
              <div class="company-rating">
                <el-rate v-model="company.average_rating" disabled show-score />
              </div>
            </div>
            
            <div class="company-meta">
              <el-tag size="small">{{ company.industry_name }}</el-tag>
              <span v-if="company.size">{{ company.size }}</span>
              <span v-if="company.location">
                <el-icon><Location /></el-icon>
                {{ company.location }}
              </span>
            </div>
            
            <div class="company-stats">
              <span>
                <el-icon><Document /></el-icon>
                {{ company.review_count }} 条评价
              </span>
            </div>
          </div>
        </div>
        
        <el-empty v-if="!loading && companies.length === 0" description="暂无公司数据" />
      </div>
      
      <el-pagination
        v-if="total > pageSize"
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next, total"
        @current-change="handlePageChange"
        class="pagination"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import { Search, OfficeBuilding, Location, Document } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const companies = ref([])
const industries = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)

const filters = ref({
  industry: '',
  size: '',
  search: route.query.search || '',
  ordering: '-review_count'
})

const loadIndustries = async () => {
  try {
    const response = await api.getIndustries()
    industries.value = response.data
  } catch (error) {
    console.error('Failed to load industries:', error)
  }
}

const loadCompanies = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      ...filters.value
    }
    
    // 清理空值
    Object.keys(params).forEach(key => {
      if (!params[key]) delete params[key]
    })
    
    const response = await api.getCompanies(params)
    companies.value = response.data.results.map(c => ({
      ...c,
      average_rating: Number(c.average_rating)
    }))
    total.value = response.data.count
  } catch (error) {
    console.error('Failed to load companies:', error)
  } finally {
    loading.value = false
  }
}

const handleFilter = () => {
  currentPage.value = 1
  loadCompanies()
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadCompanies()
}

onMounted(() => {
  loadIndustries()
  loadCompanies()
})

watch(() => route.query.search, (newSearch) => {
  if (newSearch !== undefined) {
    filters.value.search = newSearch
    handleFilter()
  }
})
</script>

<style scoped>
.filters-bar {
  margin-bottom: 24px;
}

.companies-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 400px;
}

.company-item {
  display: flex;
  gap: 24px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s;
}

.company-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.company-logo {
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 8px;
  flex-shrink: 0;
}

.company-logo img {
  max-width: 100%;
  max-height: 100%;
}

.company-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.company-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.company-name {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.company-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 14px;
  color: #666;
}

.company-stats {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 14px;
  color: #999;
}

.company-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination {
  margin-top: 32px;
  display: flex;
  justify-content: center;
}
</style>

