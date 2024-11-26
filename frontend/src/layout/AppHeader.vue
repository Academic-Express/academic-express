<script setup lang="ts">
import { reactive, useTemplateRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { useThemeStore } from '@/stores/theme'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const authStore = useAuthStore()
const userStore = useUserStore()
const themeStore = useThemeStore()

const userMenu = useTemplateRef('userMenu')

const userMenuItems = reactive([
  {
    separator: true,
  },
  {
    label: t('userProfile'),
    icon: 'pi pi-address-book',
    command: goToUserProfile,
  },
  {
    label: t('userCenter'),
    icon: 'pi pi-user',
    command: () => router.push({ name: 'user-center' }),
  },
  {
    label: t('userSettings'),
    icon: 'pi pi-cog',
    command: () => router.push({ name: 'user-settings' }),
  },
  {
    label: t('logout'),
    icon: 'pi pi-sign-out',
    command: logout,
  },
])

function goToUserProfile() {
  router.push({
    name: 'user-profile',
    params: { userId: userStore.user!.id },
  })
}

function logout() {
  authStore.logout()
  userStore.resetUser()

  if (route.meta.requiresAuth) {
    router.replace({ name: 'home' })
  }
}
</script>

<template>
  <header
    class="sticky top-0 z-20 border-b border-slate-300 bg-surface-0/60 backdrop-blur dark:border-slate-600 dark:bg-transparent"
  >
    <div class="container mx-auto px-8">
      <div class="flex h-16 items-center">
        <RouterLink to="/">
          <h1 class="text-xl font-semibold">{{ t('app.name') }}</h1>
        </RouterLink>
        <div class="ml-auto flex items-center space-x-2">
          <Button
            @click="() => themeStore.toggleDarkMode()"
            :icon="`pi pi-${themeStore.darkMode ? 'moon' : 'sun'}`"
            variant="text"
            severity="contrast"
            rounded
          ></Button>

          <Button
            icon="pi pi-bell"
            variant="text"
            severity="contrast"
            rounded
          ></Button>

          <template v-if="userStore.user">
            <Button
              @click="event => userMenu?.toggle(event)"
              variant="text"
              severity="contrast"
              rounded
            >
              <Avatar :image="userStore.user.avatar" shape="circle" />
              <span class="pi pi-chevron-down !text-xs"></span>
            </Button>

            <Menu ref="userMenu" :model="userMenuItems" popup>
              <template #start>
                <div
                  class="relative flex w-full cursor-pointer items-center overflow-hidden rounded-none p-2 pl-4 transition-colors duration-200 hover:bg-surface-100 dark:hover:bg-surface-800"
                  @click="goToUserProfile"
                >
                  <Avatar
                    :image="userStore.user.avatar"
                    class="mr-3"
                    shape="circle"
                  />
                  <span class="inline-flex flex-col items-start">
                    <span>{{ userStore.user.username }}</span>
                    <span class="text-xs text-muted-color">{{
                      userStore.user.nickname
                    }}</span>
                  </span>
                </div>
              </template>
            </Menu>
          </template>

          <template v-else>
            <Button
              v-if="!userStore.user"
              as="router-link"
              :to="{ name: 'login', query: { redirect: route.fullPath } }"
              :label="t('login')"
              variant="text"
              severity="primary"
            ></Button>
            <Button
              v-if="!userStore.user"
              as="router-link"
              to="/auth/register"
              :label="t('register')"
              variant="text"
              severity="contrast"
            ></Button>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<i18n locale="zh-CN">
{
  "login": "登录",
  "register": "注册",
  "userProfile": "个人主页",
  "userCenter": "用户中心",
  "logout": "退出登录",
  "userSettings": "编辑资料",
}
</i18n>
