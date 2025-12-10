<template>
  <div class="main-layout">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-content">
          <div class="logo" @click="$router.push('/')">
            <el-icon :size="28"><OfficeBuilding /></el-icon>
            <span>WelfareWatch</span>
          </div>
          
          <el-menu
            mode="horizontal"
            :default-active="activeMenu"
            class="nav-menu"
            @select="handleMenuSelect"
          >
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/companies">公司列表</el-menu-item>
            <el-menu-item index="/reviews/create" v-if="userStore.isLoggedIn">
              <el-icon><Edit /></el-icon>
              发布评价
            </el-menu-item>
          </el-menu>
          
          <div class="header-actions">
            <template v-if="userStore.isLoggedIn">
              <el-button 
                v-if="userStore.isModerator" 
                type="warning" 
                @click="$router.push('/admin')"
                :icon="Setting"
              >
                审核后台
              </el-button>
              
              <el-dropdown @command="handleUserCommand">
                <span class="user-dropdown">
                  <el-avatar :size="32">{{ userStore.user?.username[0] }}</el-avatar>
                  <span class="username">{{ userStore.user?.username }}</span>
                  <el-icon><ArrowDown /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="profile">
                      <el-icon><User /></el-icon>
                      个人中心
                    </el-dropdown-item>
                    <el-dropdown-item command="my-reviews">
                      <el-icon><Document /></el-icon>
                      我的评价
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout">
                      <el-icon><SwitchButton /></el-icon>
                      退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
            
            <template v-else>
              <el-button @click="$router.push('/auth/login')">登录</el-button>
              <el-button type="primary" @click="$router.push('/auth/register')">注册</el-button>
            </template>
          </div>
        </div>
      </el-header>
      
      <!-- 主内容区 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
      
      <!-- 底部 -->
      <el-footer class="footer">
        <div class="footer-content">
          <p>&copy; 2024 WelfareWatch. All rights reserved.</p>
          <p>帮助职场人了解真实的公司福利待遇</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { 
  OfficeBuilding, Edit, Setting, User, Document, 
  SwitchButton, ArrowDown 
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const handleMenuSelect = (index) => {
  router.push(index)
}

const handleUserCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'my-reviews':
      router.push('/my-reviews')
      break
    case 'logout':
      userStore.logout()
      ElMessage.success('已退出登录')
      router.push('/')
      break
  }
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
}

.header {
  background: white;
  border-bottom: 1px solid #e8e8e8;
  padding: 0;
  height: 64px;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  cursor: pointer;
  margin-right: 48px;
}

.nav-menu {
  flex: 1;
  border: none;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.3s;
}

.user-dropdown:hover {
  background: #f5f5f5;
}

.username {
  font-size: 14px;
  color: #333;
}

.main-content {
  min-height: calc(100vh - 124px);
  background: #f5f7fa;
  padding: 24px;
}

.footer {
  background: white;
  border-top: 1px solid #e8e8e8;
  height: 120px;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  text-align: center;
  padding: 24px;
  color: #999;
}

.footer-content p {
  margin: 8px 0;
}
</style>

