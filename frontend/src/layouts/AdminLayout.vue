<template>
  <div class="admin-layout">
    <el-container>
      <el-aside width="240px" class="admin-aside">
        <div class="admin-logo" @click="$router.push('/')">
          <el-icon :size="24"><Setting /></el-icon>
          <span>审核后台</span>
        </div>
        
        <el-menu
          :default-active="activeMenu"
          class="admin-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="/admin">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据统计</span>
          </el-menu-item>
          <el-menu-item index="/admin/reviews">
            <el-icon><Document /></el-icon>
            <span>评价审核</span>
          </el-menu-item>
          <el-menu-item index="/admin/comments">
            <el-icon><ChatDotRound /></el-icon>
            <span>评论审核</span>
          </el-menu-item>
          <el-menu-item index="/admin/reports">
            <el-icon><Warning /></el-icon>
            <span>举报处理</span>
          </el-menu-item>
        </el-menu>
        
        <div class="back-to-main">
          <el-button @click="$router.push('/')" :icon="HomeFilled">
            返回主站
          </el-button>
        </div>
      </el-aside>
      
      <el-container>
        <el-header class="admin-header">
          <div class="header-right">
            <span class="admin-user">{{ userStore.user?.username }}</span>
          </div>
        </el-header>
        
        <el-main class="admin-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { 
  Setting, DataAnalysis, Document, ChatDotRound, 
  Warning, HomeFilled 
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const handleMenuSelect = (index) => {
  router.push(index)
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
}

.admin-aside {
  background: #001529;
  color: white;
  display: flex;
  flex-direction: column;
}

.admin-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px 20px;
  font-size: 18px;
  font-weight: bold;
  color: white;
  cursor: pointer;
}

.admin-menu {
  flex: 1;
  border: none;
  background: transparent;
}

.back-to-main {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-header {
  background: white;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.admin-user {
  font-weight: 500;
}

.admin-main {
  background: #f0f2f5;
  min-height: calc(100vh - 60px);
}
</style>

