<template>
  <div class="profile-page">
    <div class="container">
      <h1 class="page-title">个人中心</h1>
      
      <el-row :gutter="24">
        <el-col :span="8">
          <el-card class="profile-card">
            <div class="profile-avatar">
              <el-avatar :size="100">{{ userStore.user?.username[0] }}</el-avatar>
              <h2 class="username">{{ userStore.user?.username }}</h2>
              <el-tag v-if="userStore.isModerator" type="warning">审核员</el-tag>
            </div>
            
            <el-divider />
            
            <div class="profile-stats">
              <div class="stat-item">
                <div class="stat-value">{{ userStore.user?.review_count || 0 }}</div>
                <div class="stat-label">评价数</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ userStore.user?.comment_count || 0 }}</div>
                <div class="stat-label">评论数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="16">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>基本信息</span>
                <el-button text @click="isEditing = !isEditing">
                  {{ isEditing ? '取消编辑' : '编辑' }}
                </el-button>
              </div>
            </template>
            
            <el-form
              ref="formRef"
              :model="form"
              :rules="rules"
              label-width="120px"
              :disabled="!isEditing"
            >
              <el-form-item label="用户名">
                <el-input v-model="form.username" disabled />
              </el-form-item>
              
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="form.email" />
              </el-form-item>
              
              <el-form-item label="手机号" prop="phone">
                <el-input v-model="form.phone" />
              </el-form-item>
              
              <el-form-item label="匿名昵称" prop="anonymous_name">
                <el-input v-model="form.anonymous_name" />
                <div class="form-tip">匿名发布时显示的昵称</div>
              </el-form-item>
              
              <el-form-item label="个人简介">
                <el-input
                  v-model="form.bio"
                  type="textarea"
                  :rows="4"
                  placeholder="介绍一下自己..."
                />
              </el-form-item>
              
              <el-form-item v-if="isEditing">
                <el-button
                  type="primary"
                  :loading="saving"
                  @click="handleSave"
                >
                  保存
                </el-button>
                <el-button @click="isEditing = false">取消</el-button>
              </el-form-item>
            </el-form>
          </el-card>
          
          <el-card class="password-card">
            <template #header>
              <span>修改密码</span>
            </template>
            
            <el-form
              ref="passwordFormRef"
              :model="passwordForm"
              :rules="passwordRules"
              label-width="120px"
            >
              <el-form-item label="原密码" prop="old_password">
                <el-input
                  v-model="passwordForm.old_password"
                  type="password"
                  show-password
                />
              </el-form-item>
              
              <el-form-item label="新密码" prop="new_password">
                <el-input
                  v-model="passwordForm.new_password"
                  type="password"
                  show-password
                />
              </el-form-item>
              
              <el-form-item label="确认密码" prop="new_password_confirm">
                <el-input
                  v-model="passwordForm.new_password_confirm"
                  type="password"
                  show-password
                />
              </el-form-item>
              
              <el-form-item>
                <el-button
                  type="primary"
                  :loading="changingPassword"
                  @click="handleChangePassword"
                >
                  修改密码
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import api from '@/api'

const userStore = useUserStore()

const formRef = ref()
const passwordFormRef = ref()
const isEditing = ref(false)
const saving = ref(false)
const changingPassword = ref(false)

const form = ref({
  username: '',
  email: '',
  phone: '',
  anonymous_name: '',
  bio: ''
})

const passwordForm = ref({
  old_password: '',
  new_password: '',
  new_password_confirm: ''
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱', trigger: 'blur' }
  ]
}

const validatePasswordConfirm = (rule, value, callback) => {
  if (value !== passwordForm.value.new_password) {
    callback(new Error('两次密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ],
  new_password_confirm: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validatePasswordConfirm, trigger: 'blur' }
  ]
}

const loadProfile = () => {
  if (userStore.user) {
    form.value = {
      username: userStore.user.username,
      email: userStore.user.email,
      phone: userStore.user.phone || '',
      anonymous_name: userStore.user.anonymous_name || '',
      bio: userStore.user.bio || ''
    }
  }
}

const handleSave = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    saving.value = true
    try {
      await userStore.updateProfile(form.value)
      ElMessage.success('保存成功')
      isEditing.value = false
    } catch (error) {
      console.error('Failed to update profile:', error)
    } finally {
      saving.value = false
    }
  })
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    changingPassword.value = true
    try {
      await api.changePassword(passwordForm.value)
      ElMessage.success('密码修改成功')
      
      // 清空表单
      passwordForm.value = {
        old_password: '',
        new_password: '',
        new_password_confirm: ''
      }
      passwordFormRef.value.resetFields()
    } catch (error) {
      console.error('Failed to change password:', error)
    } finally {
      changingPassword.value = false
    }
  })
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-card {
  margin-bottom: 24px;
}

.profile-avatar {
  text-align: center;
  padding: 24px 0;
}

.username {
  margin: 16px 0 8px;
  font-size: 24px;
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  padding: 16px 0;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.info-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-tip {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.password-card {
  margin-bottom: 24px;
}
</style>
