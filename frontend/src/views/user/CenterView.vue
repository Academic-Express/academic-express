<script setup lang="ts">
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { reactive, ref } from 'vue'

import SubscriptionPanel from '@/components/user/SubscriptionPanel.vue'
import SettingsPanel from '@/components/user/SettingsPanel.vue'

const { t } = useI18n()
const selectedItem = ref<string>('user')

const menuItems = reactive([
  {
    label: t('accountInfo.title'),
    items: [
      {
        label: t('accountInfo.scholar'),
        icon: 'pi pi-graduation-cap',
        key: 'scholar',
        command: () => {
          selectedItem.value = 'scholar'
        },
      },
      {
        label: t('accountInfo.user'),
        icon: 'pi pi-user',
        key: 'user',
        command: () => {
          selectedItem.value = 'user'
        },
      },
    ],
  },
  {
    separator: true,
  },
  {
    label: t('pubInfo.title'),
    items: [
      {
        label: t('pubInfo.subscriptions'),
        icon: 'pi pi-bookmark',
        key: 'subscriptions',
        command: () => {
          selectedItem.value = 'subscriptions'
        },
      },
      {
        label: t('pubInfo.collections'),
        icon: 'pi pi-star',
        key: 'collections',
        command: () => {
          selectedItem.value = 'collections'
        },
      },
      {
        label: t('pubInfo.history'),
        icon: 'pi pi-history',
        key: 'history',
        command: () => {
          selectedItem.value = 'history'
        },
      },
    ],
  },
])

useHead({ title: t('_title') })
</script>

<template>
  <main>
    <div class="flex items-start gap-8">
      <Menu :model="menuItems" class="ml-8 w-32 rounded-xl shadow">
        <template #item="{ item, props }">
          <a
            v-ripple
            class="flex items-center"
            v-bind="props.action"
            :class="{
              'bg-surface-200 dark:bg-surface-700': selectedItem === item.key,
            }"
          >
            <span class="p-menu-item-icon" :class="item.icon"></span>
            <span class="p-menu-item-label">{{ item.label }}</span>
          </a>
        </template>
      </Menu>
      <div
        class="mr-8 flex-1 rounded-xl bg-surface-0 p-6 shadow dark:bg-surface-900"
      >
        <template v-if="selectedItem === 'scholar'">
          <h2>{{ t('accountInfo.scholar') }}</h2>
        </template>
        <template v-else-if="selectedItem === 'user'">
          <SettingsPanel />
        </template>
        <template v-else-if="selectedItem === 'subscriptions'">
          <SubscriptionPanel />
        </template>
        <template v-else-if="selectedItem === 'collections'">
          <h2>{{ t('pubInfo.collections') }}</h2>
        </template>
        <template v-else-if="selectedItem === 'history'">
          <h2>{{ t('pubInfo.history') }}</h2>
        </template>
      </div>
    </div>
  </main>
</template>

<i18n locale="zh-CN">
{
  "_title": "用户中心 - @:app.name",
  "accountInfo": {
    "title": "账户信息",
    "scholar": "学术主页",
    "user": "个人账户",
  },
  "pubInfo": {
    "title": "学术中心",
    "subscriptions": "我的关注",
    "collections": "我的收藏",
    "history": "历史记录",
  },
}
</i18n>
