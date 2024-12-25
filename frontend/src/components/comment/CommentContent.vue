<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { useI18n } from 'vue-i18n'
import { computed, ref, onMounted, nextTick } from 'vue'
import { Marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js'
import DOMPurify from 'dompurify'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

import {
  VoteAction,
  type Comment,
  type CommentRequest,
  type CommentVoteRequest,
} from '@/services/api'
import { useClaimAuthorIds } from '@/services/claim'
import { usePromiseConfirm } from '@/services/confirm'

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

dayjs.extend(relativeTime).locale('zh-cn')

const userStore = useUserStore()
const { t } = useI18n()
const confirm = usePromiseConfirm()

const isThumbUp = computed(() => props.comment.user_vote > 0)
const isThumbDown = computed(() => props.comment.user_vote < 0)
const commentUser = computed(() => props.comment.author)
const isSelf = computed(() => userStore.user?.id === commentUser.value.id)
const isOwner = computed(() => props.ownerId === commentUser.value.id)
const createTime = computed(() => dayjs(props.comment.created_at).fromNow())
const updateTime = computed(() => dayjs(props.comment.updated_at).fromNow())

const showFullContent = ref(false)
const addReply = ref(false)
const editComment = ref(false)

const showReplyPreview = ref(false)
const replyPreviewText = ref<string>('')

const showEditPreview = ref(false)
const editPreviewText = ref<string>('')

const editText = ref(props.comment.content)
const replyText = ref<string>('')

const textRef = ref<HTMLElement | null>(null)
const isTextClipped = ref(false)

const checkTextClipping = () => {
  if (textRef.value) {
    isTextClipped.value =
      textRef.value.scrollHeight > textRef.value.clientHeight
  }
}

const onSubmitReply = async () => {
  if (replyText.value) {
    await props.onReply({
      content: replyText.value,
      parent: props.comment.parent ?? props.comment.id,
    })
    addReply.value = false
    replyText.value = ''
    showReplyPreview.value = false
    replyPreviewText.value = ''
  }
}

const onSubmitEdit = async () => {
  if (editText.value) {
    await props.onEdit(props.comment.id, { content: editText.value })
    editComment.value = false
    editText.value = ''
    showEditPreview.value = false
    editPreviewText.value = ''
  }
}

const onCancelEdit = async () => {
  editComment.value = false
  showEditPreview.value = false
  editPreviewText.value = ''
}

const onCancelReply = async () => {
  addReply.value = false
  showReplyPreview.value = false
  replyPreviewText.value = ''
}

const onPreviewEdit = async () => {
  if (editText.value) {
    showEditPreview.value = !showEditPreview.value
    if (showEditPreview.value) {
      editPreviewText.value = DOMPurify.sanitize(
        marked.parse(editText.value) as string,
      )
    }
  }
}

const onPreviewReply = async () => {
  if (replyText.value) {
    showReplyPreview.value = !showReplyPreview.value
    if (showReplyPreview.value) {
      replyPreviewText.value = DOMPurify.sanitize(
        marked.parse(replyText.value) as string,
      )
    }
  }
}

const onDeleteComment = async (event: MouseEvent) => {
  const ret = await confirm.require({
    group: 'popup',
    target: event.currentTarget as HTMLElement,
    message:
      props.comment.parent !== null
        ? t('confirm.deleteReply')
        : t('confirm.deleteComment'),
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: t('confirm.yes'),
    rejectLabel: t('confirm.no'),
    acceptProps: { severity: 'danger' },
    rejectProps: { severity: 'secondary', outlined: true },
  })
  if (!ret) {
    return
  }

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

const { authorIds } = useClaimAuthorIds()
</script>

<template>
  <template v-if="commentUser">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <img
          :src="commentUser.avatar"
          alt="avatar"
          class="inline h-8 w-8 rounded-md"
        />
        <span class="max-w-xs truncate text-sm font-bold">
          <RouterLink
            :to="{
              name: 'user-profile',
              params: { userId: commentUser.id },
            }"
            class="transition-colors hover:text-blue-500 hover:underline"
          >
            {{ commentUser.nickname }}
          </RouterLink>
        </span>
        <span class="text-sm">
          {{
            createTime === updateTime
              ? t('createdAt', { time: createTime })
              : t('updatedAt', { time: updateTime })
          }}
        </span>
      </div>
      <div class="mr-2 flex gap-2">
        <Tag
          v-if="authorIds.includes(commentUser.id)"
          value="作者"
          severity="success"
          class="shadow"
        ></Tag>
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
        <div
          v-html="renderedContent"
          ref="textRef"
          class="w-full break-words"
          :class="{ 'line-clamp-4': !showFullContent }"
          style="line-height: 2"
        ></div>
      </div>
      <template v-if="!showFullContent && isTextClipped">
        <span
          class="cursor-pointer text-gray-500 underline dark:text-gray-400"
          @click="showFullContent = true"
          >{{ t('more') }}</span
        >
      </template>
      <template v-if="showFullContent && isTextClipped">
        <span
          class="cursor-pointer text-gray-500 underline dark:text-gray-400"
          @click="showFullContent = false"
          >{{ t('less') }}</span
        >
      </template>
    </template>
    <div v-else class="mt-2">
      <Textarea
        v-if="!showEditPreview"
        v-model="editText"
        :placeholder="t('editPlaceholder')"
        rows="2"
        auto-resize
        class="max-h-[240px] w-full !overflow-auto rounded-xl"
      ></Textarea>
      <div
        v-if="showEditPreview"
        v-html="editPreviewText"
        class="max-h-[240px] overflow-auto break-words"
      ></div>
    </div>

    <div class="mt-2 flex items-center justify-between">
      <ButtonGroup
        class="flex items-center overflow-hidden rounded-full bg-gray-100 dark:bg-gray-800"
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
        ></Button>
        <Button variant="text" size="small" class="no-hover-bg !cursor-default">
          {{ props.comment.vote_count }}
        </Button>
        <Button
          :icon="isThumbDown ? 'pi pi-thumbs-down-fill' : 'pi pi-thumbs-down'"
          variant="text"
          @click="
            onVote(props.comment.id, {
              value: isThumbDown ? VoteAction.Cancel : VoteAction.Down,
            })
          "
          size="small"
        ></Button>
      </ButtonGroup>
      <div v-if="!editComment">
        <Button
          icon="pi pi-reply"
          variant="text"
          size="small"
          @click="addReply = !addReply"
        ></Button>
        <Button
          v-if="isSelf"
          icon="pi pi-pen-to-square"
          variant="text"
          size="small"
          @click="editComment = true"
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
      <ButtonGroup v-else>
        <Button
          icon="pi pi-eye"
          @click="onPreviewEdit"
          size="small"
          variant="text"
        >
        </Button>
        <Button
          icon="pi pi-times"
          @click="onCancelEdit"
          size="small"
          variant="text"
        ></Button>
        <Button
          icon="pi pi-check"
          @click="onSubmitEdit"
          size="small"
          variant="text"
        ></Button>
      </ButtonGroup>
    </div>

    <div class="mt-2" v-if="addReply && !editComment">
      <Textarea
        v-if="!showReplyPreview"
        v-model="replyText"
        :placeholder="t('commentPlaceholder')"
        rows="4"
        auto-resize
        class="max-h-[240px] w-full !overflow-auto rounded-xl"
      ></Textarea>
      <div
        v-if="showReplyPreview"
        v-html="replyPreviewText"
        class="max-h-[240px] overflow-auto break-words"
      ></div>
      <div class="text-right">
        <Button
          icon="pi pi-eye"
          @click="onPreviewReply"
          size="small"
          variant="text"
        ></Button>
        <Button
          icon="pi pi-times"
          @click="onCancelReply"
          size="small"
          variant="text"
        ></Button>
        <Button
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
  "less": "收起",
  "me": "我",
  "commentOwner": "楼主",
  "commentPlaceholder": "写下你的回复...",
  "editPlaceholder": "编辑评论",
  "createdAt": "发表于 {time}",
  "updatedAt": "修改于 {time}",
  "confirm": {
    "deleteComment": "删除这条评论？所有回复也会被删除。",
    "deleteReply": "删除这条回复？",
    "yes": "是",
    "no": "否",
  }
}
</i18n>
