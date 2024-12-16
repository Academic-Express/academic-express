<script setup lang="ts">
import { ref } from 'vue'
import CommentParent from './CommentParent.vue'

const showInput = ref(false)
const commentText = ref('')

// template
const items = [
  {
    parentContent:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit sed',
    childrenContents: [
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit sed',
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit sed',
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit sed',
    ],
  },
  {
    parentContent: 'This is another parent comment',
    childrenContents: [],
  },
]
</script>

<template>
  <div class="rounded-lg bg-surface-0 p-6 shadow-md dark:bg-surface-950">
    <div class="px-2">
      <!-- Add Comment Button -->
      <div class="mb-2">
        <Button
          :label="showInput ? '取消' : '评论'"
          :icon="showInput ? 'pi pi-times' : 'pi pi-comment'"
          @click="showInput = !showInput"
          size="small"
        ></Button>
      </div>

      <div v-if="showInput" class="mb-4">
        <Textarea
          v-model="commentText"
          placeholder="Write your comment..."
          rows="4"
          auto-resize
          class="w-full rounded-xl"
        ></Textarea>
        <div class="text-right">
          <Button
            label="提交"
            icon="pi pi-check"
            @click="(showInput = false), (commentText = '')"
            size="small"
          ></Button>
        </div>
      </div>
    </div>

    <!-- Scrollable Comments List -->
    <ScrollPanel style="width: 100%; height: 500px" class="px-2">
      <div v-for="(item, index) in items" :key="index">
        <CommentParent
          :parent-content="item.parentContent"
          :children-contents="item.childrenContents"
        />
      </div>
    </ScrollPanel>
  </div>
</template>
