import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/Home.vue'),
          meta: { title: '首页' }
        },
        {
          path: 'companies',
          name: 'companies',
          component: () => import('@/views/Companies.vue'),
          meta: { title: '公司列表' }
        },
        {
          path: 'companies/:id',
          name: 'company-detail',
          component: () => import('@/views/CompanyDetail.vue'),
          meta: { title: '公司详情' }
        },
        {
          path: 'reviews/create',
          name: 'review-create',
          component: () => import('@/views/ReviewCreate.vue'),
          meta: { title: '发布评价', requiresAuth: true }
        },
        {
          path: 'reviews/:id',
          name: 'review-detail',
          component: () => import('@/views/ReviewDetail.vue'),
          meta: { title: '评价详情' }
        },
        {
          path: 'profile',
          name: 'profile',
          component: () => import('@/views/Profile.vue'),
          meta: { title: '个人中心', requiresAuth: true }
        },
        {
          path: 'my-reviews',
          name: 'my-reviews',
          component: () => import('@/views/MyReviews.vue'),
          meta: { title: '我的评价', requiresAuth: true }
        }
      ]
    },
    {
      path: '/auth',
      component: () => import('@/layouts/AuthLayout.vue'),
      children: [
        {
          path: 'login',
          name: 'login',
          component: () => import('@/views/auth/Login.vue'),
          meta: { title: '登录' }
        },
        {
          path: 'register',
          name: 'register',
          component: () => import('@/views/auth/Register.vue'),
          meta: { title: '注册' }
        }
      ]
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAuth: true, requiresModerator: true },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: () => import('@/views/admin/Dashboard.vue'),
          meta: { title: '审核后台' }
        },
        {
          path: 'reviews',
          name: 'admin-reviews',
          component: () => import('@/views/admin/Reviews.vue'),
          meta: { title: '评价审核' }
        },
        {
          path: 'comments',
          name: 'admin-comments',
          component: () => import('@/views/admin/Comments.vue'),
          meta: { title: '评论审核' }
        },
        {
          path: 'reports',
          name: 'admin-reports',
          component: () => import('@/views/admin/Reports.vue'),
          meta: { title: '举报处理' }
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - WelfareWatch` : 'WelfareWatch'
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }
  
  // 检查是否需要审核员权限
  if (to.meta.requiresModerator && !userStore.isModerator) {
    next({ name: 'home' })
    return
  }
  
  next()
})

export default router

