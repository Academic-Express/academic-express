<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { useI18n } from 'vue-i18n'
import { computed, ref, onMounted, nextTick } from 'vue'
import { Marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js'
import DOMPurify from 'dompurify'
import {
  VoteAction,
  type Comment,
  type CommentRequest,
  type CommentVoteRequest,
} from '@/services/api'

import '@/assets/github-markdown.css'
import 'highlight.js/styles/github.css'

const props = defineProps<{
  comment: Comment
  ownerId?: number // 楼主 ID
  onReply: (payload: CommentRequest) => Promise<void>
  onVote: (commentId: number, payload: CommentVoteRequest) => Promise<void>
  onDelete: (commentId: number) => Promise<void>
  onEdit: (
    commentId: number,
    payload: Omit<CommentRequest, 'parent'>,
  ) => Promise<void>
}>()

const userStore = useUserStore()
const { t } = useI18n()

const isThumbUp = computed(() => props.comment.user_vote > 0)
const isThumbDown = computed(() => props.comment.user_vote < 0)
const commentUser = computed(() => props.comment.author)
const isSelf = computed(() => userStore.user?.id === commentUser.value.id)
const isOwner = computed(() => props.ownerId === commentUser.value.id)

const showFullContent = ref(false)
const addResponse = ref(false)
const editComment = ref(false)

const editText = ref('')
const responseText = ref('')

const textRef = ref<HTMLElement | null>(null)
const isTextClipped = ref(false)

const checkTextClipping = () => {
  if (textRef.value) {
    isTextClipped.value =
      textRef.value.scrollHeight > textRef.value.clientHeight
  }
}

const onSubmitReply = async () => {
  if (responseText.value) {
    await props.onReply({
      content: responseText.value,
      parent: props.comment.parent ?? props.comment.id,
    })
    addResponse.value = false
    responseText.value = ''
  }
}

const onSubmitEdit = async () => {
  if (editText.value) {
    await props.onEdit(props.comment.id, { content: editText.value })
    editComment.value = false
    editText.value = ''
  }
}

const onDeleteComment = async () => {
  await props.onDelete(props.comment.id)
}

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

const renderedContent = computed(() => {
  if (!props.comment.content) {
    return ''
  }
  return DOMPurify.sanitize(marked.parse(props.comment.content) as string)
})

onMounted(() => {
  nextTick(() => {
    checkTextClipping()
  })
})
</script>

<template>
  <template v-if="commentUser">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <img
          :src="commentUser?.avatar"
          alt="avatar"
          class="inline h-8 w-8 rounded-md"
        />
        <span class="text-sm font-bold">{{ commentUser?.nickname }}</span>
      </div>
      <div class="mr-2 flex gap-2">
        <Tag
          v-if="isOwner"
          :value="t('commentOwner')"
          severity="warn"
          class="shadow"
        ></Tag>
        <Tag v-if="isSelf" :value="t('me')" severity="info" class="shadow">
        </Tag>
      </div>
    </div>

    <template v-if="!editComment">
      <div class="mt-2">
        <span
          v-html="renderedContent"
          ref="textRef"
          class="w-full text-sm"
          :class="{ 'line-clamp-4': !showFullContent }"
          style="line-height: 2"
        >
        </span>
      </div>
      <template v-if="!showFullContent && isTextClipped">
        <span
          class="cursor-pointer text-sm text-gray-500 underline dark:text-gray-400"
          @click="showFullContent = true"
          >{{ t('more') }}</span
        >
      </template>
    </template>
    <template v-else>
      <Textarea
        v-model="editText"
        :placeholder="t('editPlaceholder')"
        rows="2"
        auto-resize
        class="mt-2 w-full rounded-xl"
      ></Textarea>
    </template>

    <div class="flex items-center justify-between">
      <ButtonGroup
        class="flex items-center rounded-full bg-gray-100 dark:bg-gray-800"
      >
        <Button
          :icon="isThumbUp ? 'pi pi-thumbs-up-fill' : 'pi pi-thumbs-up'"
          variant="text"
          @click="
            onVote(props.comment.id, {
              value: isThumbUp ? VoteAction.Cancel : VoteAction.Up,
            })
          "
          size="small"
          class="no-hover-bg"
        ></Button>
        <Button variant="text" size="small" class="no-hover-bg">{{
          props.comment.vote_count
        }}</Button>
        <Button
          :icon="isThumbDown ? 'pi pi-thumbs-down-fill' : 'pi pi-thumbs-down'"
          variant="text"
          @click="
            onVote(props.comment.id, {
              value: isThumbDown ? VoteAction.Cancel : VoteAction.Down,
            })
          "
          size="small"
          class="no-hover-bg"
        ></Button>
      </ButtonGroup>
      <div v-if="!editComment">
        <Button
          icon="pi pi-reply"
          variant="text"
          size="small"
          @click="addResponse = !addResponse"
        ></Button>
        <Button
          v-if="isSelf"
          icon="pi pi-pen-to-square"
          variant="text"
          size="small"
          @click="editComment = !editComment"
        ></Button>
        <Button
          v-if="isSelf"
          icon="pi pi-trash"
          variant="text"
          size="small"
          @click="onDeleteComment"
        >
        </Button>
      </div>
      <div v-else>
        <Button
          icon="pi pi-times"
          @click="(editComment = false), (editText = '')"
          size="small"
          variant="text"
        ></Button>
        <Button
          icon="pi pi-check"
          @click="onSubmitEdit"
          size="small"
          variant="text"
        ></Button>
      </div>
    </div>

    <div class="mt-2" v-if="addResponse">
      <Textarea
        v-model="responseText"
        :placeholder="t('commentPlaceholder')"
        rows="4"
        auto-resize
        class="w-full rounded-xl"
      ></Textarea>
      <div class="text-right">
        <Button
          :label="t('cancel')"
          icon="pi pi-times"
          @click="(addResponse = false), (responseText = '')"
          size="small"
          variant="text"
        ></Button>
        <Button
          :label="t('submit')"
          icon="pi pi-check"
          @click="onSubmitReply"
          size="small"
          variant="text"
        ></Button>
      </div>
    </div>
    <hr v-if="props.comment.parent" class="my-2" />
  </template>
</template>

<style scoped>
/* 禁用按钮 hover 背景变化 */
.no-hover-bg {
  background-color: transparent !important;
}

.no-hover-bg:hover {
  background-color: transparent !important;
  box-shadow: none !important;
}
</style>

<i18n locale="zh-CN">
{
  "comment": "评论",
  "reply": "回复",
  "cancel": "取消",
  "submit": "提交",
  "more": "更多",
  "me": "我",
  "commentOwner": "楼主",
  "commentPlaceholder": "写下你的评论...",
  "editPlaceholder": "编辑评论",
}
</i18n>
