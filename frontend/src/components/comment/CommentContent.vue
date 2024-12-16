<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { computed, ref, onMounted, nextTick } from 'vue'

defineProps<{
  content: string
}>()

const userStore = useUserStore()
const user = computed(() => userStore.user)

const isThumbUp = ref(false)
const isThumbDown = ref(false)
const showFullContent = ref(false)
const addResponse = ref(false)
const responseText = ref('')
const textRef = ref<HTMLElement | null>(null) // 用于获取文本的 DOM 元素
const isTextClipped = ref(false) // 标记文本是否超出显示区域

// 监测文本内容是否超出
const checkTextClipping = () => {
  if (textRef.value) {
    // 获取元素的 scrollHeight 和 clientHeight 来判断是否需要显示 Read more
    isTextClipped.value =
      textRef.value.scrollHeight > textRef.value.clientHeight
  }
}

onMounted(() => {
  nextTick(() => {
    checkTextClipping() // 在页面渲染完成后检查
  })
})
</script>

<template>
  <template v-if="user">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <img
          :src="user?.avatar"
          alt="avatar"
          class="inline h-8 w-8 rounded-md"
        />
        <span class="text-sm font-bold">{{ user?.nickname }}</span>
      </div>
      <div>
        <Button
          :icon="isThumbUp ? 'pi pi-thumbs-up-fill' : 'pi pi-thumbs-up'"
          variant="text"
          rounded
          @click="isThumbUp = !isThumbUp"
          size="small"
        ></Button>
        <Button
          :icon="isThumbDown ? 'pi pi-thumbs-down-fill' : 'pi pi-thumbs-down'"
          variant="text"
          rounded
          @click="isThumbDown = !isThumbDown"
          size="small"
        ></Button>
        <span
          class="ml-3 cursor-pointer text-sm text-green-500 dark:text-green-400"
          @click="addResponse = !addResponse"
          >{{ addResponse ? '取消' : '回复' }}
        </span>
      </div>
    </div>
    <div class="mt-2">
      <span
        ref="textRef"
        class="w-full text-sm"
        :class="{ 'line-clamp-4': !showFullContent }"
        style="line-height: 2"
      >
        {{ content }}
      </span>
    </div>
    <template v-if="!showFullContent && isTextClipped">
      <span
        class="cursor-pointer text-sm text-gray-500 underline dark:text-gray-400"
        @click="showFullContent = true"
        >更多</span
      >
    </template>
    <div class="mt-2" v-if="addResponse">
      <Textarea
        v-model="responseText"
        placeholder="Write your comment..."
        rows="4"
        auto-resize
        class="w-full rounded-xl text-xs"
      ></Textarea>
      <div class="text-right">
        <Button
          label="取消"
          icon="pi pi-times"
          @click="(addResponse = false), (responseText = '')"
          size="small"
          variant="text"
        ></Button>
        <Button
          label="提交"
          icon="pi pi-check"
          @click="(addResponse = false), (responseText = '')"
          size="small"
          variant="text"
        ></Button>
      </div>
    </div>
  </template>
</template>
