<script setup lang="ts">
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'
import { reactive, ref } from 'vue'

const { t } = useI18n()
const selectedItem = ref<string | null>('user')

const menuItems = reactive([
  {
    label: t('accountInfo.title'),
    items: [
      {
        label: t('accountInfo.scholar'),
        icon: 'pi pi-graduation-cap',
        command: () => {
          selectedItem.value = 'scholar'
        },
      },
      {
        label: t('accountInfo.user'),
        icon: 'pi pi-user',
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
        label: t('pubInfo.concerned'),
        icon: 'pi pi-bookmark',
        command: () => {
          selectedItem.value = 'concerned'
        },
      },
      {
        label: t('pubInfo.collected'),
        icon: 'pi pi-star',
        command: () => {
          selectedItem.value = 'collected'
        },
      },
      {
        label: t('pubInfo.history'),
        icon: 'pi pi-history',
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
    <div class="flex gap-8">
      <Menu :model="menuItems" class="ml-8 w-32 rounded-xl shadow"> </Menu>
      <Panel class="mr-8 flex-1 rounded-xl shadow">
        <template v-if="selectedItem === 'scholar'">
          <h2>{{ t('accountInfo.scholar') }}</h2>
        </template>
        <template v-else-if="selectedItem === 'user'">
          <h2>{{ t('accountInfo.user') }}</h2>
        </template>
        <template v-else-if="selectedItem === 'concerned'">
          <h2>{{ t('pubInfo.concerned') }}</h2>
        </template>
        <template v-else-if="selectedItem === 'collected'">
          <h2>{{ t('pubInfo.collected') }}</h2>
        </template>
        <template v-else-if="selectedItem === 'history'">
          <h2>{{ t('pubInfo.history') }}</h2>
        </template>
      </Panel>
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
    "concerned": "我的关注",
    "collected": "我的收藏",
    "history": "历史记录",
  },
}
</i18n>
