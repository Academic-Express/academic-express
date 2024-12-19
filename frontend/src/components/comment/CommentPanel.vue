<script setup lang="ts">
import { ref, watchEffect } from 'vue'
import { useI18n } from 'vue-i18n'
import CommentParent from './CommentParent.vue'
import {
  FeedOrigin,
  type Comment,
  getComments,
  postComment,
  type CommentRequest,
  type CommentVoteRequest,
  voteComment,
  deleteComment,
  editComment,
} from '@/services/api'

const props = defineProps<{
  origin: FeedOrigin
  resource: string
}>()

const { t } = useI18n()
const showInput = ref(false)
const commentText = ref('')
const comments = ref<Comment[]>([])

const onComment = async () => {
  try {
    await postComment(props.origin, props.resource, {
      content: commentText.value,
    })
    await loadComments()
    commentText.value = ''
    showInput.value = false
  } catch (error) {
    console.error(error)
  }
}

const onReply = async (payload: CommentRequest) => {
  try {
    await postComment(props.origin, props.resource, payload)
    await loadComments()
  } catch (error) {
    console.error(error)
  }
}

const onEdit = async (
  commendId: number,
  payload: Omit<CommentRequest, 'parent'>,
) => {
  try {
    await editComment(props.origin, props.resource, commendId, payload)
    await loadComments()
  } catch (error) {
    console.error(error)
  }
}

const onVote = async (commentId: number, payload: CommentVoteRequest) => {
  try {
    await voteComment(props.origin, props.resource, commentId, payload)
    await loadComments()
  } catch (error) {
    console.error(error)
  }
}

const onDelete = async (commentId: number) => {
  try {
    await deleteComment(props.origin, props.resource, commentId)
    await loadComments()
  } catch (error) {
    console.error(error)
  }
}

const loadComments = async () => {
  try {
    const response = await getComments(props.origin, props.resource)
    comments.value = response.data
  } catch (error) {
    console.error(error)
  }
}

watchEffect(async () => {
  await loadComments()
})
</script>

<template>
  <div class="rounded-lg bg-surface-0 p-6 shadow-md dark:bg-surface-950">
    <div class="px-2">
      <!-- Add Comment Button -->
      <div class="mb-2">
        <Button
          :label="showInput ? t('cancel') : t('comment')"
          :icon="showInput ? 'pi pi-times' : 'pi pi-comment'"
          @click="showInput = !showInput"
          size="small"
        ></Button>
      </div>

      <div v-if="showInput" class="mb-4">
        <Textarea
          v-model="commentText"
          :placeholder="t('commentPlaceholder')"
          rows="4"
          auto-resize
          class="w-full rounded-xl"
        ></Textarea>
        <div class="text-right">
          <Button
            :label="t('submit')"
            icon="pi pi-check"
            @click="onComment"
            size="small"
          ></Button>
        </div>
      </div>
    </div>

    <!-- Scrollable Comments List -->
    <ScrollPanel style="width: 100%; height: 500px" class="px-2">
      <div v-for="comment in comments" :key="comment.id">
        <CommentParent
          :comment="comment"
          @reply="onReply"
          @vote="onVote"
          @delete="onDelete"
          @edit="onEdit"
        />
      </div>
    </ScrollPanel>
  </div>
</template>

<i18n locale="zh-CN">
{
  "comment": "评论",
  "cancel": "取消",
  "submit": "提交",
  "commentPlaceholder": "写下你的评论...",
}
</i18n>
