<script setup lang="ts">
import { ref, watchEffect } from 'vue'
import { useI18n } from 'vue-i18n'
import { Marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js'
import DOMPurify from 'dompurify'

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

const marked = new Marked(
  markedHighlight({
    emptyLangClass: 'hljs',
    langPrefix: 'hljs language-',
    highlight(code, lang) {
      const language = hljs.getLanguage(lang) ? lang : 'plaintext'
      return hljs.highlight(code, { language }).value
    },
  }),
)

const { t } = useI18n()
const showInput = ref(false)
const commentText = ref<string>('')
const showPreview = ref(false)
const previewText = ref<string>('')

const comments = ref<Comment[]>([])

const onPreview = async () => {
  if (!showInput.value || !commentText.value) {
    // 如果没有按下"评论"，或者没有输入回复
    return
  }
  showPreview.value = !showPreview.value
  if (showPreview.value) {
    previewText.value = DOMPurify.sanitize(
      marked.parse(commentText.value) as string,
    )
  }
}

const onCancel = async () => {
  showInput.value = false
  previewText.value = ''
  showPreview.value = false
}

const onSubmit = async () => {
  try {
    await postComment(props.origin, props.resource, {
      content: commentText.value,
    })
    await loadComments()
    commentText.value = ''
    showInput.value = false
    previewText.value = ''
    showPreview.value = false
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
  <div
    class="flex max-h-[800px] flex-col gap-4 rounded-lg bg-surface-0 p-6 shadow-md dark:bg-surface-900"
  >
    <!-- Add Comment Button -->
    <div>
      <Button
        :label="showInput ? t('cancel') : t('comment')"
        :icon="showInput ? 'pi pi-times' : 'pi pi-comment'"
        @click="showInput = !showInput"
        size="small"
      ></Button>
    </div>

    <div v-if="showInput">
      <Textarea
        v-if="!showPreview"
        v-model="commentText"
        :placeholder="t('commentPlaceholder')"
        rows="4"
        auto-resize
        class="max-h-[240px] w-full !overflow-auto rounded-xl"
      ></Textarea>
      <div
        v-if="showPreview"
        v-html="previewText"
        class="max-h-[240px] overflow-y-auto break-words"
      ></div>
      <ButtonGroup class="flex justify-end text-right">
        <Button
          icon="pi pi-eye"
          @click="onPreview"
          size="small"
          variant="text"
        ></Button>
        <Button
          icon="pi pi-times"
          @click="onCancel"
          size="small"
          variant="text"
        ></Button>
        <Button
          icon="pi pi-check"
          @click="onSubmit"
          size="small"
          variant="text"
        ></Button>
      </ButtonGroup>
    </div>

    <!-- Scrollable Comments List -->
    <div
      v-if="comments.length === 0 && !showInput"
      class="rounded-xl border-2 py-8 text-center text-muted-color"
    >
      {{ t('noComments') }}
    </div>

    <div v-if="comments.length > 0" class="w-full flex-1 overflow-y-auto">
      <CommentParent
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        @reply="onReply"
        @vote="onVote"
        @delete="onDelete"
        @edit="onEdit"
      />
    </div>
  </div>
</template>

<i18n locale="zh-CN">
{
  "comment": "评论",
  "cancel": "取消",
  "submit": "提交",
  "commentPlaceholder": "写下你的评论...",
  "noComments": "暂无评论",
}
</i18n>
