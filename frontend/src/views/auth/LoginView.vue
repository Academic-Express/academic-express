<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { I18nT, useI18n } from 'vue-i18n'
import { useHead } from '@unhead/vue'
import { AxiosError } from 'axios'
import { useToast } from 'primevue'

import { login, type ErrorResponse } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

const props = defineProps<{
  redirect?: string
}>()

const router = useRouter()
const { t } = useI18n()
const toast = useToast()
const authStore = useAuthStore()
const userStore = useUserStore()

useHead({ title: t('_title') })

const username = ref('')
const password = ref('')
const rememberMe = ref(true)
const loading = ref(false)

const valid = computed(() => {
  return username.value.length > 0 && password.value.length > 0
})

async function onLogin() {
  if (!valid.value || loading.value) return

  loading.value = true

  try {
    const response = await login({
      username: username.value,
      password: password.value,
    })
    authStore.login(response.data, rememberMe.value)

    await userStore.fetchUser()

    toast.add({
      severity: 'success',
      summary: t('toast.success'),
      detail: t('toast.successDetail', { username: userStore.user!.username }),
      life: 5000,
    })
    router.replace(props.redirect ?? { name: 'home' })
  } catch (error) {
    let detail = t('toast.unknownError')
    if (error instanceof AxiosError && error.response?.data) {
      const data = error.response.data as ErrorResponse
      detail = data.detail ?? detail
      if (data.code === 'no_active_account') {
        detail = t('toast.invalidCredentials')
      }
    }

    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail,
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}
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
          class="w-full bg-surface-0 px-8 py-20 dark:bg-surface-900 sm:px-20"
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

          <div>
            <label
              for="username"
              class="mb-2 block text-lg font-medium text-surface-900 dark:text-surface-0"
              >{{ t('username') }}</label
            >
            <InputText
              id="username"
              type="text"
              :placeholder="t('usernamePlaceholder')"
              class="mb-8 w-full md:w-[24rem]"
              v-model="username"
            />

            <label
              for="password"
              class="mb-2 block text-lg font-medium text-surface-900 dark:text-surface-0"
              >{{ t('password') }}</label
            >
            <Password
              inputId="password"
              v-model="password"
              :placeholder="t('passwordPlaceholder')"
              :toggleMask="true"
              :feedback="false"
              class="mb-4"
              fluid
            ></Password>

            <div class="mb-8 mt-2 flex items-center justify-between gap-8">
              <div class="flex items-center">
                <Checkbox
                  v-model="rememberMe"
                  inputId="rememberme"
                  binary
                  class="mr-2"
                ></Checkbox>
                <label for="rememberme">{{ t('rememberMe') }}</label>
              </div>
              <span
                class="ml-2 cursor-pointer text-right font-medium text-primary no-underline"
                >{{ t('forgotPassword') }}</span
              >
            </div>

            <Button
              :label="t('login')"
              class="mb-4 w-full"
              @click="onLogin"
              :disabled="!valid || loading"
              :loading="loading"
            ></Button>

            <I18nT
              keypath="registerPrompt"
              tag="div"
              class="text-center text-muted-color"
            >
              <RouterLink to="/auth/register" class="text-primary">{{
                t('register')
              }}</RouterLink>
            </I18nT>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped></style>

<i18n locale="zh-CN">
{
  "_title": "登录 - @:app.name",
  "title": "欢迎来到学术直通车",
  "subtitle": "登录探索更多内容",
  "username": "用户名",
  "usernamePlaceholder": "用户名/手机号/邮箱地址",
  "password": "密码",
  "passwordPlaceholder": "密码",
  "rememberMe": "保持登录状态",
  "forgotPassword": "忘记密码？",
  "login": "登录",
  "registerPrompt": "没有账号？{0}",
  "register": "注册",
  "toast": {
    "success": "登录成功",
    "successDetail": "欢迎回来，{username}！",
    "error": "登录失败",
    "unknownError": "未知错误",
    "invalidCredentials": "用户名或密码错误",
  },
}
</i18n>
