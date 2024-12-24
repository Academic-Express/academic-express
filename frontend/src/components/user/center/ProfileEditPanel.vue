<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import z from 'zod'
import { useField, useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'

import { patchProfile, type UserDetail } from '@/services/api'
import { useCustomToast } from '@/services/toast'

const props = defineProps<{
  currentUser: UserDetail
  onProfileUpdated?: (user: UserDetail) => void
}>()

const { t } = useI18n()
const toast = useCustomToast()

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
    nickname: props.currentUser.nickname,
    email: props.currentUser.email,
    phone: props.currentUser.phone,
    url: props.currentUser.url,
    intro: props.currentUser.intro,
  },
})

const { value: nickname } = useField<string>('nickname')
const { value: email } = useField<string>('email')
const { value: phone } = useField<string>('phone')
const { value: url } = useField<string>('url')
const { value: intro } = useField<string>('intro')

const onEditProfile = handleSubmit(async values => {
  try {
    const response = await patchProfile(values)

    props.onProfileUpdated?.(response.data)

    toast.add({
      severity: 'success',
      summary: t('toast.success'),
      detail: t('toast.successDetail'),
      life: 5000,
    })
  } catch (error) {
    toast.reportError(error)
  }
})
</script>

<template>
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
          :disabled="!meta.dirty || !meta.valid || isSubmitting"
          @click="onEditProfile"
        ></Button>
      </div>
    </div>
  </div>
</template>

<i18n locale="zh-CN">
{
  "nickname": "昵称",
  "url": "个人主页",
  "email": "邮箱",
  "phone": "电话",
  "intro": "个人简介",
  "profileEdit": "确认修改",
  "editInfo": "编辑个人信息",
  "toast": {
    "success": "修改成功",
    "successDetail": "您的个人资料已更新",
    "error": "修改失败",
    "unknownError": "未知错误"
  },
  "validation": {
    "nickname": {
      "max": "昵称长度不能大于 20"
    },
    "email": {
      "invalid": "邮箱格式不正确"
    },
    "phone": {
      "invalid": "手机号格式不正确"
    },
    "url": {
      "invalid": "URL 格式不正确"
    }
  }
}
</i18n>
