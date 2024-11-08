<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useHead } from '@unhead/vue'
import { AxiosError } from 'axios'
import { useToast } from 'primevue'
import z from 'zod'
import { useField, useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'

import { register, type ErrorResponse } from '@/services/api'

const router = useRouter()
const { t } = useI18n()
const toast = useToast()

useHead({ title: t('_title') })

const validationSchema = toTypedSchema(
  z
    .object({
      username: z
        .string()
        .regex(/^[a-zA-Z0-9@.+-_]+$/, t('validation.username.character'))
        .min(4, t('validation.username.min'))
        .max(20, t('validation.username.max')),
      password: z
        .string()
        .min(6, t('validation.password.min'))
        .max(32, t('validation.password.max')),
      passwordRepeat: z.string(),
      email: z.string().email(t('validation.email.invalid')),
      phone: z.string().refine(v => /^1[3-9]\d{9}$/.test(v), {
        message: t('validation.phone.invalid'),
      }),
    })
    .refine(data => data.password === data.passwordRepeat, {
      message: t('validation.passwordRepeat.mismatch'),
      path: ['passwordRepeat'],
    }),
)

const { handleSubmit, errors, meta, isSubmitting } = useForm({
  validationSchema,
  initialValues: {
    username: '',
    password: '',
    passwordRepeat: '',
    email: '',
    phone: '',
  },
})

const { value: username } = useField<string>('username')
const { value: password } = useField<string>('password')
const { value: passwordRepeat } = useField<string>('passwordRepeat')
const { value: email } = useField<string>('email')
const { value: phone } = useField<string>('phone')

const onRegister = handleSubmit(async (values, ctx) => {
  try {
    await register({
      username: values.username,
      password: values.password,
      nickname: values.username,
      email: values.email,
      phone: values.phone,
    })

    toast.add({
      severity: 'success',
      summary: t('toast.success'),
      detail: t('toast.successDetail'),
      life: 5000,
    })

    router.push({ name: 'login' })
  } catch (error) {
    let detail = t('toast.unknownError')
    if (error instanceof AxiosError && error.response?.data) {
      const data = error.response.data as ErrorResponse
      detail = data.detail
      if (data.code === 'validation_error') {
        if (data.fields?.username?.some(e => e.code === 'unique')) {
          detail = t('toast.usernameExists')
        } else if (data.fields?.email?.some(e => e.code === 'unique')) {
          detail = t('toast.emailExists')
        } else if (data.fields?.phone?.some(e => e.code === 'unique')) {
          detail = t('toast.phoneExists')
        }

        if (data.fields) {
          for (const [field, errors] of Object.entries(data.fields)) {
            ctx.setFieldError(
              // @ts-expect-error field is not typed
              field,
              errors.map(e => e.detail),
            )
          }
        }
      }
    }

    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail,
      life: 5000,
    })
  }
})
</script>

<template>
  <div
    class="flex min-h-screen min-w-[100vw] items-center justify-center overflow-hidden bg-surface-50 dark:bg-surface-950"
  >
    <main class="flex flex-col items-center justify-center">
      <div
        style="
          border-radius: 56px;
          padding: 0.3rem;
          background: linear-gradient(
            180deg,
            var(--primary-color) 10%,
            transparent 30%
          );
        "
      >
        <div
          class="w-full bg-surface-0 px-8 py-16 dark:bg-surface-900 sm:px-20"
          style="border-radius: 53px"
        >
          <div class="mb-8 text-center">
            <div
              class="mb-4 text-3xl font-medium text-surface-900 dark:text-surface-0"
            >
              {{ t('title') }}
            </div>
            <span class="font-medium text-muted-color">{{
              t('subtitle')
            }}</span>
          </div>

          <div class="mb-2 md:w-[24rem]">
            <InputText
              id="username"
              type="text"
              v-model="username"
              :placeholder="t('usernamePlaceholder')"
              class="w-full"
              :invalid="!!errors.username"
            />
            <Message
              severity="error"
              size="small"
              variant="simple"
              class="mx-2 mt-1 min-h-2"
            >
              <span class="text-thin">{{ errors.username }}</span>
            </Message>
          </div>

          <div class="mb-2 md:w-[24rem]">
            <Password
              inputId="password"
              v-model="password"
              :placeholder="t('passwordPlaceholder')"
              :toggleMask="true"
              :feedback="false"
              fluid
              :invalid="!!errors.password"
            ></Password>
            <Message
              severity="error"
              size="small"
              variant="simple"
              class="mx-2 mt-1 min-h-2"
            >
              <span class="text-thin">{{ errors.password }}</span>
            </Message>
          </div>

          <div class="mb-2 md:w-[24rem]">
            <Password
              inputId="passwordRepeat"
              v-model="passwordRepeat"
              :placeholder="t('passwordRepeatPlaceholder')"
              :toggleMask="true"
              :feedback="false"
              fluid
              :invalid="!!errors.passwordRepeat"
            ></Password>
            <Message
              severity="error"
              size="small"
              variant="simple"
              class="mx-2 mt-1 min-h-2"
            >
              <span class="text-thin">{{ errors.passwordRepeat }}</span>
            </Message>
          </div>

          <div class="mb-2 md:w-[24rem]">
            <InputText
              id="email"
              v-model="email"
              type="email"
              :placeholder="t('emailPlaceholder')"
              class="w-full"
              :invalid="!!errors.email"
            />
            <Message
              severity="error"
              size="small"
              variant="simple"
              class="mx-2 mt-1 min-h-2"
            >
              <span class="text-thin">{{ errors.email }}</span>
            </Message>
          </div>

          <div class="mb-4 md:w-[24rem]">
            <InputText
              id="phone"
              v-model="phone"
              type="tel"
              :placeholder="t('phonePlaceholder')"
              class="w-full"
              :invalid="!!errors.phone"
            />
            <Message
              severity="error"
              size="small"
              variant="simple"
              class="mx-2 mt-1 min-h-2"
            >
              <span class="text-thin">{{ errors.phone }}</span>
            </Message>
          </div>

          <Button
            :label="t('register')"
            @click="onRegister"
            :disabled="!meta.valid || isSubmitting"
            :loading="isSubmitting"
            class="mb-4 w-full"
          ></Button>

          <I18nT
            keypath="loginPrompt"
            tag="div"
            class="text-center text-muted-color"
          >
            <RouterLink to="/auth/login" class="text-primary">{{
              t('login')
            }}</RouterLink>
          </I18nT>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped></style>

<i18n locale="zh-CN">
{
  "_title": "注册 - @:app.name",
  "title": "欢迎来到学术直通车",
  "subtitle": "加入我们，探索更多内容",
  "usernamePlaceholder": "用户名",
  "passwordPlaceholder": "密码",
  "passwordRepeatPlaceholder": "确认密码",
  "emailPlaceholder": "邮箱地址",
  "phonePlaceholder": "手机号",
  "register": "注册",
  "loginPrompt": "已有账号？{0}",
  "login": "登录",
  "validation": {
    "username": {
      "character": "用户名只能包含字母、数字和特殊字符 {'@.+-_'}",
      "min": "用户名长度不能小于 4",
      "max": "用户名长度不能大于 20",
    },
    "password": {
      "min": "密码长度不能小于 6",
      "max": "密码长度不能大于 32",
    },
    "passwordRepeat": {
      "mismatch": "两次输入的密码不一致",
    },
    "email": {
      "invalid": "邮箱格式不正确",
    },
    "phone": {
      "invalid": "手机号格式不正确",
    },
  },
  "toast": {
    "success": "注册成功",
    "successDetail": "欢迎加入学术直通车！",
    "error": "注册失败",
    "unknownError": "未知错误",
    "usernameExists": "用户名已存在",
    "emailExists": "邮箱地址已存在",
    "phoneExists": "手机号已存在",
  },
}
</i18n>
