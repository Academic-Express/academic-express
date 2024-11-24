<script setup lang="ts">
import { ref } from 'vue'
import { useI18n, I18nT } from 'vue-i18n'

import { useUserStore } from '@/stores/user'

const { t } = useI18n()
const userStore = useUserStore()

const mainTab = ref('subscription')
</script>

<template>
  <div class="flex justify-center">
    <!-- 左侧内容区域 -->
    <section class="w-3/4 max-w-4xl">
      <Tabs v-model:value="mainTab">
        <!-- 左侧 Tabs -->
        <TabList class="mb-4 overflow-hidden rounded-lg shadow">
          <Tab value="follow">{{ t('main.follow') }}</Tab>
          <Tab value="subscription">{{ t('main.subscription') }}</Tab>
          <Tab value="hot">{{ t('main.hot') }}</Tab>
        </TabList>
        <TabPanels class="overflow-hidden rounded-lg shadow">
          <TabPanel value="follow">
            <p>关注动态组件</p>
          </TabPanel>
          <TabPanel value="subscription">
            <p>订阅推荐组件</p>
          </TabPanel>
          <TabPanel value="hot">
            <p>热点追踪组件</p>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </section>

    <!-- 右侧边栏 -->
    <aside class="ml-10 w-1/4 min-w-[240px] space-y-6">
      <!-- 用户卡片 -->
      <Card>
        <template #header>
          <div class="flex items-center p-4">
            <!-- 用户头像和信息 -->
            <template v-if="userStore.user">
              <Avatar
                :image="userStore.user.avatar"
                shape="circle"
                size="large"
              ></Avatar>

              <div class="ml-4">
                <div class="text-lg font-bold">
                  <RouterLink to="/user/center">
                    {{ userStore.user.username }}
                  </RouterLink>
                </div>
                <div class="text-sm text-muted-color">
                  <a
                    v-if="userStore.user.scholar_url"
                    :href="userStore.user.scholar_url"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {{ t('userPanel.myScholarPage') }}
                  </a>
                  <I18nT v-else keypath="userPanel.noScholarPage">
                    <RouterLink to="/user/center" class="text-primary">
                      {{ t('userPanel.noScholarPageLink') }}
                    </RouterLink>
                  </I18nT>
                </div>
              </div>
            </template>

            <!-- 未登录用户 -->
            <template v-else>
              <Avatar icon="pi pi-user" shape="circle" size="large"></Avatar>
              <div class="ml-4">
                <div class="text-lg font-bold">
                  <RouterLink
                    to="/auth/login"
                    class="transition-colors hover:text-primary"
                  >
                    {{ t('userPanel.login') }}
                  </RouterLink>
                </div>
                <div class="text-sm text-muted-color">
                  {{ t('userPanel.loginTips') }}
                </div>
              </div>
            </template>
          </div>
        </template>
        <template #content>
          <div>用户信息的内容。</div>
        </template>
      </Card>

      <!-- 订阅推荐 -->
      <Panel
        :header="t('subscriptionPanel.topics.header')"
        class="overflow-hidden rounded-xl shadow"
        toggleable
      >
        <div>订阅话题的内容。</div>
      </Panel>

      <Panel
        :header="t('subscriptionPanel.scholars.header')"
        class="overflow-hidden rounded-xl shadow"
        toggleable
      >
        <div>关注学者的内容。</div>
      </Panel>

      <Panel
        :header="t('subscriptionPanel.organizations.header')"
        class="overflow-hidden rounded-xl shadow"
        toggleable
      >
        <div>关注机构的内容。</div>
      </Panel>
    </aside>
  </div>
</template>

<i18n locale="zh-CN">
{
  "_title": "@:app.name",
  "main": {
    "follow": "关注动态",
    "subscription": "订阅推荐",
    "hot": "热点追踪",
  },
  "userPanel": {
    "myScholarPage": "我的学术主页",
    "noScholarPage": "暂无学术主页，{0}",
    "noScholarPageLink": "去关联",
    "login": "立即登录",
    "loginTips": "加入@:app.name{''}，探索更多内容",
  },
  "subscriptionPanel": {
    "topics": {
      "header": "订阅话题",
    },
    "scholars": {
      "header": "关注学者",
    },
    "organizations": {
      "header": "关注机构",
    },
  }
}
</i18n>
