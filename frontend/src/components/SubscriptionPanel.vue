<script setup lang="ts">
import { ref } from 'vue'
import { Button, InputText } from 'primevue' // 示例组件库引入

// 控制面板显示状态
const isOpen = ref(false)

// 论文订阅部分
const newInstitution = ref('')
const institutions = ref<string[]>([])
const newPaperTopic = ref('')
const paperTopics = ref<string[]>([])

// 代码仓库订阅部分
const newRepoInstitution = ref('')
const repoInstitutions = ref<string[]>([])
const newRepoTopic = ref('')
const repoTopics = ref<string[]>([])

// 推送设置
const email = ref('')

// 打开和关闭面板
function openPanel() {
  isOpen.value = true
}

function closePanel() {
  isOpen.value = false
}

// 添加到论文订阅列表的函数
function addInstitution() {
  if (newInstitution.value) {
    institutions.value.push(newInstitution.value)
    newInstitution.value = ''
  }
}

function addPaperTopic() {
  if (newPaperTopic.value) {
    paperTopics.value.push(newPaperTopic.value)
    newPaperTopic.value = ''
  }
}

// 添加到代码仓库订阅列表的函数
function addRepoInstitution() {
  if (newRepoInstitution.value) {
    repoInstitutions.value.push(newRepoInstitution.value)
    newRepoInstitution.value = ''
  }
}

function addRepoTopic() {
  if (newRepoTopic.value) {
    repoTopics.value.push(newRepoTopic.value)
    newRepoTopic.value = ''
  }
}

// 保存邮箱设置
function saveEmail() {
  if (email.value) {
    alert(`推送设置已保存，将会推送至邮箱：${email.value}`)
  } else {
    alert('请输入有效的邮箱地址')
  }
}
</script>

<template>
  <div>
    <!-- 背景遮罩层 -->
    <div
      v-if="isOpen"
      class="fixed inset-0 bg-black bg-opacity-50"
      @click="closePanel"
    ></div>

    <!-- 双列滑出面板 -->
    <div
      class="fixed right-0 top-0 h-full w-[700px] bg-white p-6 shadow-lg transition-transform duration-300"
      :class="{ 'translate-x-0': isOpen, 'translate-x-full': !isOpen }"
    >
      <!-- 关闭按钮 -->
      <Button
        severity="secondary"
        icon="pi pi-times"
        class="mb-4"
        @click="closePanel"
      />

      <!-- 双列布局 -->
      <div class="grid grid-cols-2 gap-6">
        <!-- 左侧：论文订阅 -->
        <div>
          <h2 class="mb-4 text-xl font-bold">论文订阅</h2>

          <!-- 1. 追踪机构（论文） -->
          <div class="mb-6">
            <h3 class="text-lg font-semibold">追踪这些机构：</h3>
            <InputText
              v-model="newInstitution"
              placeholder="输入机构名称"
              class="mt-2 w-full"
            />
            <Button
              severity="primary"
              label="添加机构"
              class="mt-2 w-full"
              @click="addInstitution"
            />
            <ul class="mt-4">
              <li
                v-for="institution in institutions"
                :key="institution"
                class="text-gray-700"
              >
                - {{ institution }}
              </li>
            </ul>
          </div>

          <!-- 2. 追踪 Topic（论文） -->
          <div class="mb-6">
            <h3 class="text-lg font-semibold">追踪这些 Topic：</h3>
            <InputText
              v-model="newPaperTopic"
              placeholder="输入 Topic 名称"
              class="mt-2 w-full"
            />
            <Button
              severity="primary"
              label="添加 Topic"
              class="mt-2 w-full"
              @click="addPaperTopic"
            />
            <ul class="mt-4">
              <li
                v-for="topic in paperTopics"
                :key="topic"
                class="text-gray-700"
              >
                - {{ topic }}
              </li>
            </ul>
          </div>
        </div>

        <!-- 右侧：代码仓库订阅 -->
        <div>
          <h2 class="mb-4 text-xl font-bold">代码仓库订阅</h2>

          <!-- 1. 追踪机构（代码仓库） -->
          <div class="mb-6">
            <h3 class="text-lg font-semibold">追踪这些机构：</h3>
            <InputText
              v-model="newRepoInstitution"
              placeholder="输入机构名称"
              class="mt-2 w-full"
            />
            <Button
              severity="primary"
              label="添加机构"
              class="mt-2 w-full"
              @click="addRepoInstitution"
            />
            <ul class="mt-4">
              <li
                v-for="institution in repoInstitutions"
                :key="institution"
                class="text-gray-700"
              >
                - {{ institution }}
              </li>
            </ul>
          </div>

          <!-- 2. 追踪 Topic（代码仓库） -->
          <div class="mb-6">
            <h3 class="text-lg font-semibold">追踪这些 Topic：</h3>
            <InputText
              v-model="newRepoTopic"
              placeholder="输入 Topic 名称"
              class="mt-2 w-full"
            />
            <Button
              severity="primary"
              label="添加 Topic"
              class="mt-2 w-full"
              @click="addRepoTopic"
            />
            <ul class="mt-4">
              <li
                v-for="topic in repoTopics"
                :key="topic"
                class="text-gray-700"
              >
                - {{ topic }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 推送至我的邮箱 -->
      <div class="mt-6 border-t pt-4">
        <h2 class="mb-4 text-lg font-semibold">
          推送选定论文和代码仓库至我的邮箱：
        </h2>
        <InputText
          v-model="email"
          placeholder="请输入邮箱地址"
          class="w-full"
        />
        <Button
          severity="success"
          label="保存并推送"
          class="mt-2 w-full"
          @click="saveEmail"
        />
      </div>
    </div>

    <!-- 打开面板按钮，只有在面板关闭时显示 -->
    <Button
      v-if="!isOpen"
      severity="primary"
      icon="pi pi-plus"
      label="打开订阅面板"
      class="fixed bottom-4 right-4"
      @click="openPanel"
    />
  </div>
</template>

<style scoped>
.translate-x-full {
  transform: translateX(100%);
}

.translate-x-0 {
  transform: translateX(0);
}
</style>
