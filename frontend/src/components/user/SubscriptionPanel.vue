<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

import TopicSubscription from './subscriptions/TopicSubscription.vue'

const { t } = useI18n()
const mainTab = ref('topic')
</script>

<template>
  <Tabs v-model:value="mainTab">
    <TabList class="mb-4 overflow-hidden">
      <Tab value="topic">{{ t('subscriptionPanel.topic') }}</Tab>
      <Tab value="scholar">{{ t('subscriptionPanel.scholar') }}</Tab>
      <Tab value="institution">{{ t('subscriptionPanel.institution') }}</Tab>
    </TabList>
    <TabPanels>
      <TabPanel value="topic">
        <KeepAlive>
          <TopicSubscription v-if="mainTab === 'topic'" />
        </KeepAlive>
      </TabPanel>
    </TabPanels>
  </Tabs>
</template>

<i18n locale="zh-CN">
{
  "subscriptionPanel": {
    "topic": "领域",
    "scholar": "学者",
    "institution": "机构"
  }
}
</i18n>
