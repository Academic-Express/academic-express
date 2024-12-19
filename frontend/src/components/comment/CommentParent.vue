<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import CommentContent from './CommentContent.vue'
import {
  type Comment,
  type CommentRequest,
  type CommentVoteRequest,
} from '@/services/api'

defineProps<{
  comment: Comment
  onReply: (payload: CommentRequest) => Promise<void>
  onVote: (commentId: number, payload: CommentVoteRequest) => Promise<void>
  onDelete: (commentId: number) => Promise<void>
  onEdit: (
    commentId: number,
    payload: Omit<CommentRequest, 'parent'>,
  ) => Promise<void>
}>()

const showResponses = ref(false)
const { t } = useI18n()
</script>

<template>
  <div class="mb-3 rounded-xl border-2 p-2">
    <CommentContent
      :comment="comment"
      @reply="onReply"
      @vote="onVote"
      @delete="onDelete"
      @edit="onEdit"
    />
    <template v-if="comment.replies.length > 0">
      <div class="my-2">
        <span
          class="cursor-pointer text-sm text-green-500 underline dark:text-green-400"
          @click="showResponses = !showResponses"
          >{{ showResponses ? t('hideResponses') : t('showResponses') }}
        </span>
      </div>
      <transition name="fade">
        <template v-if="showResponses">
          <div class="flex">
            <div
              class="my-2 mr-2 w-1 rounded border-l-2 border-dashed border-green-400"
            ></div>
            <div class="flex-1">
              <template
                v-for="child_comment in comment.replies"
                :key="child_comment.id"
              >
                <div class="mb-2 min-w-[250px]">
                  <CommentContent
                    :comment="child_comment"
                    :ownerId="comment.author.id"
                    @reply="onReply"
                    @vote="onVote"
                    @delete="onDelete"
                    @edit="onEdit"
                  />
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
  max-height: 500px;
}
</style>

<i18n locale="zh-CN">
{
  "hideResponses": "隐藏回复",
  "showResponses": "展开回复"
}
</i18n>
