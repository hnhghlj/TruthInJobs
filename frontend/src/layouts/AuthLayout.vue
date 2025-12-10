<template>
  <div class="auth-layout">
    <div class="auth-container">
      <div class="auth-header">
        <div class="logo" @click="$router.push('/')">
          <el-icon :size="36"><OfficeBuilding /></el-icon>
          <span>WelfareWatch</span>
        </div>
        <p class="tagline">发现真实的公司福利</p>
      </div>
      
      <div class="auth-content">
        <router-view />
      </div>
      
      <div class="auth-footer">
        <p>&copy; 2024 WelfareWatch</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { OfficeBuilding } from '@element-plus/icons-vue'
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-container {
  width: 100%;
  max-width: 420px;
  padding: 20px;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  font-size: 32px;
  font-weight: bold;
  color: white;
  cursor: pointer;
  margin-bottom: 12px;
}

.tagline {
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
}

.auth-content {
  background: white;
  border-radius: 12px;
  padding: 40px 32px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.auth-footer {
  text-align: center;
  margin-top: 24px;
  color: rgba(255, 255, 255, 0.8);
}
</style>

