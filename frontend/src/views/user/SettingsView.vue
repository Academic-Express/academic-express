<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

<template>
  <div
    class="flex min-h-screen w-full items-center justify-center overflow-hidden bg-surface-50 dark:bg-surface-950"
  >
    <main class="mt-[-50px] flex flex-col items-center justify-center">
      <div
        class="mb-4 w-full bg-surface-0 px-20 py-8 dark:bg-surface-900 sm:px-32"
        style="border-radius: 20px; transform: translateY(-50px)"
      >
        <div
          class="mt-8 flex items-center justify-center space-x-4 text-center"
        >
          <img
            src="https://avatars.githubusercontent.com/t/11448713?s=116&v=4"
            alt="Avatar"
            class="inline h-24 w-24 rounded-full"
          />
          <div
            class="min-w-40 text-left text-3xl font-medium text-surface-900 dark:text-surface-0"
          >
            xxx, 您好
          </div>
          <Button class="text-surface-900 dark:text-surface-0">
            {{ t('editImage') }}
          </Button>
        </div>
      </div>
      <div class="flex w-full justify-center space-x-4">
        <div
          class="w-1/2 bg-surface-0 px-8 py-8 dark:bg-surface-900"
          style="border-radius: 20px; transform: translateY(-50px)"
        >
          <div class="card flex flex-col gap-4">
            <div class="flex flex-col gap-2">
              <label for="name1">{{ t('username') }}</label>
              <InputText id="name1" type="text" />
            </div>
            <div class="flex flex-col gap-2">
              <label for="email1">{{ t('email') }}</label>
              <InputText id="email1" type="text" />
            </div>
            <div class="flex flex-col gap-2">
              <label for="age1"> {{ t('phone') }}</label>
              <InputText id="age1" type="text" />
            </div>
            <div class="flex w-full justify-center">
              <Button label="submitEdit" :fluid="false">{{
                t('submitEdit')
              }}</Button>
            </div>
          </div>
        </div>
        <div
          class="w-1/2 bg-surface-0 px-8 py-8 dark:bg-surface-900"
          style="border-radius: 20px; transform: translateY(-50px)"
        >
          <div class="flex flex-wrap gap-2">
            <label for="address">{{ t('description') }}</label>
            <Textarea id="address" rows="4" fluid auto-resize />
            <div class="flex w-full justify-center">
              <Button label="submitEdit" :fluid="false">{{
                t('submitEdit')
              }}</Button>
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
  }
</i18n>
