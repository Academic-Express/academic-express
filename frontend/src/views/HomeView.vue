<script lang="ts">
import { ref } from 'vue'

export default {
  setup() {
    const leftTab = ref('0') // 左侧区域激活的 tab
    const sidebarTab1 = ref('0') // 第一个小块 tab
    const sidebarTab2 = ref('0') // 第二个小块 tab
    return { leftTab, sidebarTab1, sidebarTab2 }
  },
}
</script>

<template>
  <div class="flex h-screen justify-center">
    <!-- 左侧内容区域 -->
    <section class="w-3/4 max-w-4xl overflow-y-auto">
      <Tabs v-model:value="leftTab">
        <!-- 左侧 Tabs -->
        <TabList class="mb-4 overflow-hidden rounded-lg shadow">
          <Tab value="0">推荐</Tab>
          <Tab value="1">热点</Tab>
          <Tab value="2">视频</Tab>
        </TabList>
        <TabPanels class="overflow-hidden rounded-lg shadow">
          <TabPanel v-if="leftTab === '0'" value="0">
            这是推荐内容的示例。
          </TabPanel>
          <TabPanel v-if="leftTab === '1'" value="1">
            这是热点内容的示例。
          </TabPanel>
          <TabPanel v-if="leftTab === '2'" value="2">
            这是视频内容的示例。
          </TabPanel>
        </TabPanels>
      </Tabs>
    </section>

    <!-- 右侧边栏 -->
    <aside class="ml-10 w-1/4 space-y-6 overflow-y-auto">
      <!-- 第一块 -->
      <div class="rounded-lg bg-white p-4 shadow dark:bg-gray-700">
        <Tabs v-model:value="sidebarTab1">
          <TabList class="mb-4 flex gap-4">
            <Tab value="0">创作中心</Tab>
            <Tab value="1">推荐关注</Tab>
          </TabList>
          <TabPanels>
            <TabPanel v-if="sidebarTab1 === '0'" value="0">
              <div>创作中心的功能和内容。</div>
            </TabPanel>
            <TabPanel v-if="sidebarTab1 === '1'" value="1">
              <div>推荐关注的用户列表和内容。</div>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </div>

      <!-- 第二块 -->
      <div class="rounded-lg bg-white p-4 shadow dark:bg-gray-700">
        <Tabs v-model:value="sidebarTab2">
          <TabList class="mb-4 flex gap-4">
            <Tab value="0">活跃用户</Tab>
            <Tab value="1">活动通知</Tab>
          </TabList>
          <TabPanels>
            <TabPanel v-if="sidebarTab2 === '0'" value="0">
              <div>展示活跃用户的信息。</div>
            </TabPanel>
            <TabPanel v-if="sidebarTab2 === '1'" value="1">
              <div>展示活动通知的内容。</div>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </div>

      <!-- 第三块 -->
      <!-- <div class="rounded-lg bg-white p-4 shadow dark:bg-gray-700">
        <div class="text-gray-700 dark:text-gray-200">
          <h3 class="mb-2 text-lg font-bold">其他内容</h3>
          <p>这里可以显示其他信息块，比如广告位或者公告。</p>
        </div>
      </div> -->
    </aside>
  </div>
</template>
