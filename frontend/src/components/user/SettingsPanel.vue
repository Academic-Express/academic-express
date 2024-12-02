<script setup lang="ts">
import { useI18n, I18nT } from 'vue-i18n'
import { useToast } from 'primevue'
import { AxiosError } from 'axios'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import z from 'zod'
import { useField, useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'

import { useUserStore } from '@/stores/user'
import { patchProfile, type ErrorResponse } from '@/services/api'
import AvatarPopup from '@/components/user/AvatarPopup.vue'

const isAvatarPopupVisible = ref(false)

const router = useRouter()
const { t } = useI18n()
const userStore = useUserStore()
const toast = useToast()

const validationSchema = toTypedSchema(
  z.object({
    nickname: z.string().max(20, t('validation.nickname.max')),
    email: z.string().email(t('validation.email.invalid')),
    phone: z.string().refine(v => /^1[3-9]\d{9}$/.test(v), {
      message: t('validation.phone.invalid'),
    }),
    url: z.string().url(t('validation.url.invalid')).or(z.literal('')),
    intro: z.string().or(z.literal('')),
  }),
)

const { handleSubmit, errors, meta, isSubmitting } = useForm({
  validationSchema,
  initialValues: {
    nickname: userStore.user?.nickname ?? '',
    email: userStore.user?.email ?? '',
    phone: userStore.user?.phone ?? '',
    url: userStore.user?.url ?? '',
    intro: userStore.user?.intro ?? '',
  },
})

const onAvatarUpdated = (newAvatarUrl: string) => {
  // 更新 userStore 中的头像 URL
  if (userStore.user) {
    userStore.user.avatar = newAvatarUrl // 只更新 avatar 字段
  }
  console.log(newAvatarUrl)
}

const { value: nickname } = useField<string>('nickname')
const { value: email } = useField<string>('email')
const { value: phone } = useField<string>('phone')
const { value: url } = useField<string>('url')
const { value: intro } = useField<string>('intro')

const onEditProfile = handleSubmit(async values => {
  try {
    const response = await patchProfile(values)

    userStore.user = response.data

    toast.add({
      severity: 'success',
      summary: t('toast.success'),
      life: 5000,
    })

    router.push({
      name: 'user-profile',
      params: { userId: userStore.user?.id },
    })
  } catch (error) {
    let detail = t('toast.unknownError')
    if (error instanceof AxiosError && error.response?.data) {
      const data = error.response.data as ErrorResponse
      detail = data.detail ?? detail
    }
    console.error('Failed to edit profile:', error)
    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail: detail,
      life: 5000,
    })
  }
})
</script>

<template>
  <div class="flex flex-1 items-center justify-center overflow-hidden">
    <main
      class="flex max-w-[960px] flex-1 flex-col items-center justify-center"
    >
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
      <div class="flex w-full justify-center space-x-4">
        <div class="w-1/2 px-8 py-2">
          <div class="flex flex-col gap-4">
            <p class="text-xl font-bold">{{ t('editInfo') }}</p>
            <div class="flex flex-col gap-2">
              <label for="nickname">{{ t('nickname') }}</label>
              <InputText v-model="nickname" id="nickname" type="text" />
              <Message
                v-if="errors.nickname"
                severity="error"
                size="small"
                variant="simple"
                class="mx-2"
              >
                <span class="text-thin">{{ errors.nickname }}</span>
              </Message>
            </div>
            <div class="flex flex-col gap-2">
              <label for="url">{{ t('url') }}</label>
              <InputText v-model="url" id="url" type="text" />
              <Message
                v-if="errors.url"
                severity="error"
                size="small"
                variant="simple"
                class="mx-2"
              >
                <span class="text-thin">{{ errors.url }}</span>
              </Message>
            </div>
            <div class="flex flex-col gap-2">
              <label for="email">{{ t('email') }}</label>
              <InputText v-model="email" id="email" type="text" />
              <Message
                v-if="errors.email"
                severity="error"
                size="small"
                variant="simple"
                class="mx-2"
              >
                <span class="text-thin">{{ errors.email }}</span>
              </Message>
            </div>
            <div class="flex flex-col gap-2">
              <label for="phone"> {{ t('phone') }}</label>
              <InputText v-model="phone" id="phone" type="text" />
              <Message
                v-if="errors.phone"
                severity="error"
                size="small"
                variant="simple"
                class="mx-2"
              >
                <span class="text-thin">{{ errors.phone }}</span>
              </Message>
            </div>
            <div class="flex flex-wrap gap-4">
              <div class="flex w-full flex-col gap-2">
                <label for="intro">{{ t('intro') }}</label>
                <Textarea
                  v-model="intro"
                  id="intro"
                  rows="4"
                  fluid
                  auto-resize
                ></Textarea>
              </div>
              <div class="flex w-full justify-center">
                <Button
                  :label="t('profileEdit')"
                  :disabled="!meta.valid || isSubmitting"
                  @click="onEditProfile"
                ></Button>
              </div>
            </div>
          </div>
        </div>
        <div class="w-1/2 px-8 py-2">
          <div class="flex flex-col gap-4">
            <p class="text-xl font-bold">{{ t('editPassword') }}</p>
            <div class="flex flex-col gap-2">
              <div class="flex justify-between">
                <label for="oldPassword">
                  {{ t('password.oldPassword') }}</label
                >
                <I18nT
                  :keypath="t('password.forget')"
                  tag="div"
                  class="text-muted-color"
                >
                </I18nT>
              </div>
              <Password
                inputId="oldPassword"
                fluid
                :promptLabel="t('password.prompt')"
                :weakLabel="t('password.weak')"
                :mediumLabel="t('password.medium')"
                :strongLabel="t('password.strong')"
              />
            </div>
            <div class="flex flex-col gap-2">
              <label for="newPassword">{{ t('password.newPassword') }}</label>
              <Password
                inputId="newPassword"
                fluid
                :promptLabel="t('password.prompt')"
                :weakLabel="t('password.weak')"
                :mediumLabel="t('password.medium')"
                :strongLabel="t('password.strong')"
              />
            </div>
            <div class="flex flex-col gap-2">
              <label for="confirmPassword">{{
                t('password.conformPassword')
              }}</label>
              <Password
                inputId="confirmPassword"
                fluid
                :promptLabel="t('password.prompt')"
                :weakLabel="t('password.weak')"
                :mediumLabel="t('password.medium')"
                :strongLabel="t('password.strong')"
              />
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex w-full justify-center">
                <Button :label="t('password.conformButton')"></Button>
              </div>
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
  "nickname": "昵称",
  "url": "个人主页",
  "email": "邮箱",
  "phone": "电话",
  "intro": "个人简介",
  "profileEdit": "确认修改",
  "editInfo": "编辑个人信息",
  "editPassword": "修改密码",
  "userWelcome": "{username}, 您好",
  "toast": {
    "success": "修改个人资料成功",
    "error": "修改个人资料失败",
    "unknownError": "未知错误"
  },
  "validation": {
    "nickname": {
      "max": "昵称长度不能大于 20",
    },
    "email": {
      "invalid": "邮箱格式不正确",
    },
    "phone": {
      "invalid": "手机号格式不正确",
    },
    "url": {
      "invalid": "URL 格式不正确",
    },
  },
  "password": {
    "oldPassword": "旧密码",
    "newPassword": "新密码",
    "conformPassword": "确认密码",
    "conformButton": "修改密码",
    "prompt": "请输入密码",
    "weak": "弱",
    "medium": "中",
    "strong": "强",
    "forget": "忘记密码？"
  }
}
</i18n>
