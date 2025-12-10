<template>
  <div class="review-create-page">
    <div class="container">
      <el-card class="create-card">
        <template #header>
          <h2 class="card-title">发布评价</h2>
        </template>
        
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="120px"
          label-position="left"
        >
          <el-form-item label="选择公司" prop="company">
            <el-select
              v-model="form.company"
              placeholder="请选择公司"
              filterable
              style="width: 100%"
            >
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.name"
                :value="company.id"
              />
            </el-select>
            <div class="form-tip">如果没有找到公司，请先添加公司</div>
          </el-form-item>
          
          <el-form-item label="评价标题" prop="title">
            <el-input
              v-model="form.title"
              placeholder="请输入评价标题"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>
          
          <el-form-item label="职位信息" prop="job_title">
            <el-input
              v-model="form.job_title"
              placeholder="例如：高级前端工程师"
            />
          </el-form-item>
          
          <el-form-item label="就职状态" prop="employment_status">
            <el-radio-group v-model="form.employment_status">
              <el-radio label="current">在职</el-radio>
              <el-radio label="former">离职</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item label="工作年限">
            <el-input-number
              v-model="form.work_years"
              :min="0"
              :max="50"
              placeholder="年"
            />
          </el-form-item>
          
          <el-divider />
          
          <el-form-item label="综合评分" prop="overall_rating">
            <el-rate v-model="form.overall_rating" show-text />
          </el-form-item>
          
          <el-form-item label="福利待遇" prop="welfare_rating">
            <el-rate v-model="form.welfare_rating" show-text />
          </el-form-item>
          
          <el-form-item label="工作环境" prop="environment_rating">
            <el-rate v-model="form.environment_rating" show-text />
          </el-form-item>
          
          <el-form-item label="发展机会" prop="development_rating">
            <el-rate v-model="form.development_rating" show-text />
          </el-form-item>
          
          <el-form-item label="管理水平" prop="management_rating">
            <el-rate v-model="form.management_rating" show-text />
          </el-form-item>
          
          <el-divider />
          
          <el-form-item label="详细评价" prop="content">
            <el-input
              v-model="form.content"
              type="textarea"
              :rows="10"
              placeholder="请详细描述您的工作体验..."
            />
            <div class="form-tip">
              您可以从以下方面展开：工作内容、团队氛围、薪资福利、晋升机会、公司文化等
            </div>
          </el-form-item>
          
          <el-form-item label="匿名发布">
            <el-switch v-model="form.is_anonymous" />
            <div class="form-tip">
              开启后，其他用户将看不到您的真实用户名
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" :loading="submitting" @click="handleSubmit">
              提交评价
            </el-button>
            <el-button @click="$router.back()">取消</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/api'

const route = useRoute()
const router = useRouter()

const formRef = ref()
const submitting = ref(false)
const companies = ref([])

const form = ref({
  company: route.query.company ? Number(route.query.company) : null,
  title: '',
  content: '',
  overall_rating: 5,
  welfare_rating: 5,
  environment_rating: 5,
  development_rating: 5,
  management_rating: 5,
  job_title: '',
  employment_status: 'current',
  work_years: null,
  is_anonymous: true
})

const rules = {
  company: [{ required: true, message: '请选择公司', trigger: 'change' }],
  title: [{ required: true, message: '请输入评价标题', trigger: 'blur' }],
  content: [
    { required: true, message: '请输入详细评价', trigger: 'blur' },
    { min: 50, message: '评价内容至少50个字符', trigger: 'blur' }
  ],
  job_title: [{ required: true, message: '请输入职位', trigger: 'blur' }]
}

const loadCompanies = async () => {
  try {
    const response = await api.getCompanies({ page_size: 1000 })
    companies.value = response.data.results
  } catch (error) {
    console.error('Failed to load companies:', error)
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitting.value = true
    try {
      // 将纯文本转换为简单HTML
      const contentHtml = `<p>${form.value.content.replace(/\n/g, '</p><p>')}</p>`
      
      await api.createReview({
        ...form.value,
        content: contentHtml
      })
      
      ElMessage.success('评价提交成功，等待审核')
      router.push('/my-reviews')
    } catch (error) {
      console.error('Failed to create review:', error)
    } finally {
      submitting.value = false
    }
  })
}

onMounted(() => {
  loadCompanies()
})
</script>

<style scoped>
.create-card {
  max-width: 900px;
  margin: 0 auto;
}

.card-title {
  font-size: 24px;
  margin: 0;
}

.form-tip {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
  line-height: 1.5;
}

.el-divider {
  margin: 24px 0;
}
</style>
