<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'

import { useUserStore } from '@/stores/user'
import AvatarPopup from '@/components/user/AvatarPopup.vue'
import ProfileEditPanel from './center/ProfileEditPanel.vue'
import PasswordChangePanel from './center/PasswordChangePanel.vue'

const isAvatarPopupVisible = ref(false)

const { t } = useI18n()
const userStore = useUserStore()

const onAvatarUpdated = (newAvatarUrl: string) => {
  // 更新 userStore 中的头像 URL
  if (userStore.user) {
    userStore.user.avatar = newAvatarUrl // 只更新 avatar 字段
  }
  console.log(newAvatarUrl)
}
</script>

<template>
  <div class="flex flex-1 items-center justify-center overflow-hidden">
    <main
      class="flex max-w-[960px] flex-1 flex-col items-center justify-center"
    >
      <!-- 头像 -->
      <div class="mb-4 w-full p-10 sm:px-20" style="border-radius: 20px">
        <div class="flex items-center justify-center space-x-6">
          <img
            :src="userStore.user?.avatar"
            alt="Avatar"
            class="inline h-24 w-24 rounded-full text-center leading-[6rem] shadow"
          />

          <div
            class="min-w-32 text-left text-3xl font-medium text-surface-900 dark:text-surface-0 sm:min-w-48"
          >
            {{ t('userWelcome', { username: userStore.user?.username }) }}
          </div>
          <Button
            :label="t('editImage')"
            icon="pi pi-pencil"
            @click="isAvatarPopupVisible = true"
          ></Button>
          <AvatarPopup
            v-model:visible="isAvatarPopupVisible"
            @update-avatar="onAvatarUpdated"
          />
        </div>
      </div>

      <!-- 编辑个人信息 -->
      <div class="flex w-full justify-center space-x-4">
        <div class="w-1/2 px-8 py-2">
          <ProfileEditPanel
            v-if="userStore.user"
            :current-user="userStore.user"
            @profile-updated="user => (userStore.user = user)"
          />
        </div>

        <!-- 修改密码 -->
        <div class="w-1/2 px-8 py-2">
          <PasswordChangePanel />
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped></style>

<i18n locale="zh-CN">
{
  "editImage": "修改头像",
  "userWelcome": "{username}, 您好",
}
</i18n>
