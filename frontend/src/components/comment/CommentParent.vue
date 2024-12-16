<script setup lang="ts">
import { ref } from 'vue'
import CommentContent from './CommentContent.vue'

const props = defineProps<{
  parentContent: string
  childrenContents: string[]
}>()

const { parentContent, childrenContents } = props

const showResponses = ref(false)
</script>

<template>
  <!-- parent -->
  <div class="mb-3 rounded-xl border-2 p-2">
    <CommentContent :content="parentContent" />
    <template v-if="childrenContents.length > 0">
      <span
        class="cursor-pointer text-sm text-green-500 underline dark:text-green-400"
        @click="showResponses = !showResponses"
        >{{ showResponses ? '隐藏回复' : '展开回复' }}
      </span>
      <transition name="fade">
        <template v-if="showResponses">
          <div class="flex">
            <div
              class="my-2 mr-2 w-1 rounded border-l-2 border-dashed border-green-400"
            ></div>
            <div class="flex-1">
              <template v-for="item in childrenContents" :key="item">
                <div class="mb-2 min-w-[250px]">
                  <CommentContent :content="item" />
                </div>
              </template>
            </div>
          </div>
        </template>
      </transition>
    </template>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.2s,
    max-height 0.2s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  max-height: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  max-height: 500px; /* You can adjust this value to fit your content */
}
</style>
