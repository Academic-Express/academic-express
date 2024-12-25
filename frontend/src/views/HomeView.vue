<script setup lang="ts">
import { ref } from 'vue'
import { useI18n, I18nT } from 'vue-i18n'
import { useHead } from '@unhead/vue'

import { useUserStore } from '@/stores/user'

import FollowFeed from '@/components/feed/FollowFeed.vue'
import SubscriptionFeed from '@/components/feed/SubscriptionFeed.vue'
import HotFeed from '@/components/feed/HotFeed.vue'
import SearchFeed from '@/components/feed/SearchFeed.vue'
import UserStats from '@/components/home/UserStats.vue'
import TopicPanel from '@/components/subscription/TopicPanel.vue'
import ScholarPanel from '@/components/subscription/ScholarPanel.vue'
// import InstitutionPanel from '@/components/subscription/InstitutionPanel.vue'

const { t } = useI18n()
const userStore = useUserStore()

useHead({ title: t('_title') })

const mainTab = ref('subscription')
const searchText = ref('')
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
          <Tab value="search">{{ t('main.search') }}</Tab>
          <div class="mx-4 flex-1 content-center" v-if="mainTab === 'search'">
            <IconField>
              <InputIcon>
                <i class="pi pi-search"></i>
              </InputIcon>
              <InputText
                v-model="searchText"
                :placeholder="t('subscriptionPanel.searchBar.input')"
                fluid
              />
              <InputIcon>
                <i
                  class="pi pi-times cursor-pointer transition-colors hover:text-primary"
                  v-if="searchText"
                  @click="searchText = ''"
                ></i>
              </InputIcon>
            </IconField>
          </div>
        </TabList>
        <TabPanels class="relative overflow-hidden rounded-lg shadow">
          <TabPanel value="follow">
            <KeepAlive>
              <FollowFeed v-if="mainTab === 'follow'" />
            </KeepAlive>
          </TabPanel>
          <TabPanel value="subscription">
            <KeepAlive>
              <SubscriptionFeed v-if="mainTab === 'subscription'" />
            </KeepAlive>
          </TabPanel>
          <TabPanel value="hot">
            <KeepAlive>
              <HotFeed v-if="mainTab === 'hot'" />
            </KeepAlive>
          </TabPanel>
          <TabPanel value="search">
            <KeepAlive>
              <SearchFeed
                v-if="mainTab === 'search'"
                :searchText="searchText"
              />
            </KeepAlive>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </section>

    <!-- 右侧边栏 -->
    <aside class="ml-10 w-1/4 min-w-[240px] space-y-6">
      <!-- 用户卡片 -->
      <Card>
        <template #header>
          <div class="flex items-center border-b p-4">
            <!-- 用户头像和信息 -->
            <template v-if="userStore.user">
              <Avatar
                :image="userStore.user.avatar"
                shape="circle"
                size="large"
              ></Avatar>

              <div class="ml-4">
                <div>
                  <RouterLink
                    to="/user/center"
                    class="text-lg font-bold transition-colors hover:text-blue-500"
                  >
                    {{ userStore.user.username }}
                  </RouterLink>
                </div>
                <div class="text-sm text-muted-color">
                  <a
                    v-if="userStore.user.scholar_url"
                    :href="userStore.user.scholar_url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="transition-colors hover:text-primary"
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
          <UserStats />
        </template>
      </Card>

      <!-- 订阅推荐 -->
      <Panel
        :header="t('subscriptionPanel.topics.header')"
        class="overflow-hidden rounded-xl shadow"
        toggleable
      >
        <TopicPanel />
      </Panel>

      <Panel
        :header="t('subscriptionPanel.scholars.header')"
        class="overflow-hidden rounded-xl shadow"
        toggleable
      >
        <ScholarPanel />
      </Panel>

      <!-- <Panel
        :header="t('subscriptionPanel.institutions.header')"
        class="overflow-hidden rounded-xl shadow"
        toggleable
      >
        <InstitutionPanel />
      </Panel> -->
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
    "search": "搜索",
  },
  "userPanel": {
    "myScholarPage": "我的学术主页",
    "noScholarPage": "暂无学术主页，{0}",
    "noScholarPageLink": "去关联",
    "login": "立即登录",
    "loginTips": "加入@:app.name{''}，探索更多内容",
  },
  "subscriptionPanel": {
    "searchBar": {
      "input": "搜索作者或话题...",
    },
    "topics": {
      "header": "订阅话题",
    },
    "scholars": {
      "header": "关注学者",
    },
    "institutions": {
      "header": "关注机构",
    },
  }
}
</i18n>
