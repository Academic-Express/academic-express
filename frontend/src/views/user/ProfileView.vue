<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useUserStore } from '@/stores/user'
const { t } = useI18n()
const userStore = useUserStore()
const nickname = userStore.user?.nickname
const email = userStore.user?.email
const phone = userStore.user?.phone
const url = userStore.user?.url
// console.log(userStore.user)
</script>

<template>
  <div class="flex flex-1 items-center justify-center overflow-hidden">
    <main
      class="flex max-w-[960px] flex-1 flex-col items-center justify-center"
    >
      <div
        class="mb-4 w-full bg-surface-0 p-10 dark:bg-surface-900 sm:px-20"
        style="border-radius: 20px"
      >
        <div class="my-6 flex items-center justify-center space-x-6">
          <img
            src="https://avatars.githubusercontent.com/t/11448713?s=116&v=4"
            alt="Avatar"
            class="inline h-24 w-24 rounded-full"
          />
          <div
            class="min-w-32 text-left text-3xl font-medium text-surface-900 dark:text-surface-0 sm:min-w-48"
          >
            {{ nickname }}, 您好
          </div>
          <!-- <Button :label="t('editImage')"></Button> -->
        </div>
      </div>
      <div class="flex w-full justify-center space-x-4">
        <div
          class="w-1/2 bg-surface-0 px-8 py-8 dark:bg-surface-900"
          style="border-radius: 20px"
        >
          <div class="flex flex-col gap-4">
            <!-- 显示静态用户名 -->
            <!-- <div class="flex flex-col gap-2">
              <label for="name1">{{ t('username') }}</label>
              <span id="name1" class="text-surface-900 dark:text-surface-0">{{ nickname }}</span>
            </div> -->
            <!-- 显示静态邮箱 -->
            <div class="flex flex-col gap-2">
              <label for="email1">{{ t('email') }}</label>
              <span id="email1" class="text-surface-900 dark:text-surface-0">{{email}}</span>
            </div>
            <!-- 显示静态电话 -->
            <div class="flex flex-col gap-2">
              <label for="age1"> {{ t('phone') }}</label>
              <span id="age1" class="text-surface-900 dark:text-surface-0">{{phone}}</span>
            </div>
            <div class="flex flex-col gap-2">
              <label for="personalWebsite">{{ t('personalWebsite') }}</label>
              <span id="personalWebsite" class="text-surface-900 dark:text-surface-0">
                <a :href="url" target="_blank" class="text-blue-500 hover:underline">{{ url || 'https://your-website.com' }}</a>
              </span>
            </div>
            
            <div class="flex w-full justify-center">
              <!-- 按钮可以去掉 -->
            </div>
          </div>
        </div>
        <div
          class="w-1/2 bg-surface-0 px-8 py-8 dark:bg-surface-900"
          style="border-radius: 20px"
        >
          <div class="flex flex-wrap gap-4">
            <!-- 显示 Google Scholar 链接 -->
            <!-- <div class="flex flex-col gap-2">
              <label for="googleScholar">{{ t('googleScholar') }}</label>
              <span id="googleScholar" class="text-surface-900 dark:text-surface-0">
                <a href="https://scholar.google.com/citations?user=XXXXXXXXX" target="_blank" class="text-blue-500 hover:underline">Google Scholar</a>
              </span>
            </div> -->
            <!-- 显示描述文本 -->
            <div class="flex w-full flex-col gap-2">
              <label for="address">{{ t('description') }}</label>
              <div id="address" class="text-surface-900 dark:text-surface-0">
                这是一段可以展示多行的描述文本。根据需要，可以调整内容的显示形式。
              </div>
            </div>
            <div class="flex w-full justify-center">
              <!-- 按钮可以去掉 -->
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>


<style scoped></style>

<i18n locale="zh-CN">
  {
    "editImage": "修改头像",
    "username": "用户名",
    "email": "邮箱",
    "phone": "电话",
    "description": "个人简介",
    "submitEdit": "确认修改",
    "googleScholar": "谷歌学术",
    "personalWebsite": "个人主页"
  }
</i18n>