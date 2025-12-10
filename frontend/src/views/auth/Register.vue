<template>
  <div class="register-page">
    <h2 class="auth-title">注册</h2>
    
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      @submit.prevent="handleSubmit"
    >
      <el-form-item prop="username">
        <el-input
          v-model="form.username"
          placeholder="用户名"
          size="large"
          :prefix-icon="User"
        />
      </el-form-item>
      
      <el-form-item prop="email">
        <el-input
          v-model="form.email"
          placeholder="邮箱"
          size="large"
          :prefix-icon="Message"
        />
      </el-form-item>
      
      <el-form-item prop="password">
        <el-input
          v-model="form.password"
          type="password"
          placeholder="密码（至少6位）"
          size="large"
          :prefix-icon="Lock"
        />
      </el-form-item>
      
      <el-form-item prop="password_confirm">
        <el-input
          v-model="form.password_confirm"
          type="password"
          placeholder="确认密码"
          size="large"
          :prefix-icon="Lock"
          @keyup.enter="handleSubmit"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button
          type="primary"
          size="large"
          style="width: 100%"
          :loading="loading"
          @click="handleSubmit"
        >
          注册
        </el-button>
      </el-form-item>
    </el-form>
    
    <div class="auth-footer">
      <span>已有账号？</span>
      <el-button text type="primary" @click="$router.push('/auth/login')">
        立即登录
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { User, Message, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)

const form = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: ''
})

const validatePasswordConfirm = (rule, value, callback) => {
  if (value !== form.value.password) {
    callback(new Error('两次密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为 3-20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少需要 6 个字符', trigger: 'blur' }
  ],
  password_confirm: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePasswordConfirm, trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      await userStore.register(form.value)
      ElMessage.success('注册成功，请登录')
      router.push('/auth/login')
    } catch (error) {
      console.error('Register failed:', error)
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.auth-title {
  text-align: center;
  margin-bottom: 32px;
  font-size: 24px;
  color: #333;
}

.auth-footer {
  text-align: center;
  margin-top: 24px;
  color: #666;
}
</style>

