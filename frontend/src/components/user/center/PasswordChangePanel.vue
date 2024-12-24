<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import z from 'zod'
import { useField, useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'

import { changePassword } from '@/services/api'
import { useCustomToast } from '@/services/toast'

const { t } = useI18n()
const toast = useCustomToast()

const passwordSchema = toTypedSchema(
  z
    .object({
      oldPassword: z.string().min(1, t('validation.oldPassword.min')),
      newPassword: z.string().min(6, t('validation.newPassword.min')),
      confirmPassword: z.string().min(1, t('validation.confirmPassword.min')),
    })
    .refine(data => data.newPassword === data.confirmPassword, {
      message: t('validation.confirmPassword.mismatch'),
      path: ['confirmPassword'],
    }),
)

const { handleSubmit, errors, meta, isSubmitting, resetForm } = useForm({
  validationSchema: passwordSchema,
  initialValues: {
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
  },
})

const { value: oldPassword } = useField<string>('oldPassword')
const { value: newPassword } = useField<string>('newPassword')
const { value: confirmPassword } = useField<string>('confirmPassword')

const onChangePassword = handleSubmit(async values => {
  try {
    await changePassword({
      old_password: values.oldPassword,
      new_password: values.newPassword,
    })

    resetForm()

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
    <p class="text-xl font-bold">{{ t('editPassword') }}</p>
    <div class="flex flex-col gap-2">
      <div class="flex justify-between">
        <label for="oldPassword"> {{ t('password.oldPassword') }}</label>
        <span
          class="cursor-pointer transition-colors text-muted-color hover:text-primary"
        >
          {{ t('password.forget') }}
        </span>
      </div>
      <Password
        inputId="oldPassword"
        v-model="oldPassword"
        fluid
        :feedback="false"
      />
      <Message
        v-if="errors.oldPassword"
        severity="error"
        size="small"
        variant="simple"
        class="mx-2"
      >
        <span class="text-thin">{{ errors.oldPassword }}</span>
      </Message>
    </div>

    <div class="flex flex-col gap-2">
      <label for="newPassword">{{ t('password.newPassword') }}</label>
      <Password
        inputId="newPassword"
        v-model="newPassword"
        fluid
        :promptLabel="t('password.prompt')"
        :weakLabel="t('password.weak')"
        :mediumLabel="t('password.medium')"
        :strongLabel="t('password.strong')"
      />
      <Message
        v-if="errors.newPassword"
        severity="error"
        size="small"
        variant="simple"
        class="mx-2"
      >
        <span class="text-thin">{{ errors.newPassword }}</span>
      </Message>
    </div>

    <div class="flex flex-col gap-2">
      <label for="confirmPassword">{{ t('password.conformPassword') }}</label>
      <Password
        inputId="confirmPassword"
        v-model="confirmPassword"
        fluid
        :feedback="false"
      />
      <Message
        v-if="errors.confirmPassword"
        severity="error"
        size="small"
        variant="simple"
        class="mx-2"
      >
        <span class="text-thin">{{ errors.confirmPassword }}</span>
      </Message>
    </div>

    <div class="flex flex-col gap-2">
      <div class="flex w-full justify-center">
        <Button
          :label="t('password.conformButton')"
          :disabled="!meta.valid || isSubmitting"
          :loading="isSubmitting"
          @click="onChangePassword"
        ></Button>
      </div>
    </div>
  </div>
</template>

<i18n locale="zh-CN">
{
  "editPassword": "修改密码",
  "toast": {
    "success": "修改成功",
    "successDetail": "您的密码已更新",
    "error": "修改失败",
    "unknownError": "未知错误"
  },
  "validation": {
    "oldPassword": {
      "min": "原密码不能为空",
    },
    "newPassword": {
      "min": "新密码长度不能小于 6",
    },
    "confirmPassword": {
      "min": "请再次输入新密码",
      "mismatch": "两次输入的密码不一致",
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
