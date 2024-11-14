<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue'
import { AxiosError } from 'axios'

import { useUserStore } from '@/stores/user'
import { getUserById, type User } from '@/services/api'
import { compactButtonDt } from '@/dt'

const props = defineProps<{
  userId: number
}>()

const { t } = useI18n()
const userStore = useUserStore()
const toast = useToast()

const fetchedUser = ref<User | null>(null)
const isSelf = computed(() => userStore.user?.id === props.userId)
const displayUser = computed(() =>
  isSelf.value ? userStore.user : fetchedUser.value,
)

watchEffect(async () => {
  if (isSelf.value) return

  try {
    const response = await getUserById(props.userId)
    fetchedUser.value = response.data
  } catch (error) {
    console.error(error)

    let detail = t('toast.unknownError')
    if (error instanceof AxiosError) {
      detail = error.response?.data.detail ?? detail
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
            class="flex min-w-32 flex-col items-start justify-center gap-2 text-left sm:min-w-48"
          >
            <template v-if="displayUser">
              <span class="text-3xl font-medium">{{
                displayUser?.username
              }}</span>
              <span class="text-lg text-muted-color">{{
                displayUser?.nickname
              }}</span>
            </template>
            <template v-else>
              <Skeleton width="10rem" height="2.25rem" border-radius="0.5rem" />
              <Skeleton width="8rem" height="1.75rem" border-radius="0.5rem" />
            </template>
          </div>

          <div class="flex flex-col items-center justify-center gap-4">
            <template v-if="isSelf">
              <Button
                :label="t('editProfile')"
                icon="pi pi-pencil"
                :dt="compactButtonDt"
                as="router-link"
                to="/user/settings"
              ></Button>
              <Button
                :label="t('userCenter')"
                icon="pi pi-user"
                :dt="compactButtonDt"
                as="router-link"
                to="/user/center"
                severity="secondary"
              ></Button>
            </template>

            <template v-else>
              <Button
                :label="t('follow')"
                icon="pi pi-user-plus"
                :dt="compactButtonDt"
              ></Button>
              <Button
                :label="t('directMessage')"
                icon="pi pi-envelope"
                severity="secondary"
                :dt="compactButtonDt"
              ></Button>
            </template>
          </div>
        </div>
      </div>

      <div class="flex w-full justify-center space-x-4">
        <div
          class="w-1/2 bg-surface-0 px-8 py-8 dark:bg-surface-900"
          style="border-radius: 20px"
        >
          <div class="flex flex-col gap-4">
            <template v-if="displayUser">
              <div class="flex flex-col gap-2">
                <span class="font-bold">{{ t('username') }}</span>
                <span>{{ displayUser.username }}</span>
              </div>

              <div v-if="displayUser.nickname" class="flex flex-col gap-2">
                <span class="font-bold">{{ t('nickname') }}</span>
                <span>{{ displayUser.nickname }}</span>
              </div>

              <div v-if="displayUser.url" class="flex flex-col gap-2">
                <span class="font-bold">{{ t('personalWebsite') }}</span>
                <span>
                  <a
                    :href="displayUser.url"
                    target="_blank"
                    class="text-blue-500 hover:underline"
                    >{{ displayUser.url }}</a
                  >
                </span>
              </div>

              <div v-if="displayUser.scholar_url" class="flex flex-col gap-2">
                <span class="font-bold">{{ t('googleScholar') }}</span>
                <span>
                  <a
                    :href="displayUser.scholar_url"
                    target="_blank"
                    class="text-blue-500 hover:underline"
                    >{{ displayUser.scholar_url }}</a
                  >
                </span>
              </div>

              <div class="flex flex-col gap-2">
                <span class="font-bold">{{ t('viewCount') }}</span>
                <span>{{ displayUser.view_count }}</span>
              </div>
            </template>

            <template v-else>
              <Skeleton width="6rem"></Skeleton>
              <Skeleton></Skeleton>
              <Skeleton width="6rem"></Skeleton>
              <Skeleton></Skeleton>
              <Skeleton width="6rem"></Skeleton>
            </template>
          </div>
        </div>

        <div
          class="w-1/2 bg-surface-0 px-8 py-8 dark:bg-surface-900"
          style="border-radius: 20px"
        >
          <div class="flex flex-wrap gap-4">
            <div class="flex w-full flex-col gap-2">
              <span class="font-bold">{{ t('description') }}</span>
              <div v-if="displayUser">
                <p v-if="displayUser.intro">{{ displayUser.intro }}</p>
                <p v-else class="text-muted-color">{{ t('noIntro') }}</p>
              </div>
              <div class="space-y-2" v-else>
                <Skeleton></Skeleton>
                <Skeleton width="75%"></Skeleton>
                <Skeleton width="40%"></Skeleton>
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
    "follow": "关注",
    "directMessage": "私信",
    "editProfile": "编辑资料",
    "userCenter": "用户中心",
    "username": "用户名",
    "nickname": "昵称",
    "viewCount": "浏览次数",
    "description": "个人简介",
    "submitEdit": "确认修改",
    "googleScholar": "Google 学术",
    "personalWebsite": "个人主页",
    "noIntro": "这位用户很懒，什么也没有留下",
    "toast": {
      "error": "出错啦！",
      "unknownError": "未知错误",
    }
  }
</i18n>
