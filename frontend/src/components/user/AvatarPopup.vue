<script setup lang="ts" name="AvatarPanel">
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { uploadAvatar } from '@/services/api' // 引入上传函数
import { useToast } from 'primevue/usetoast' // 引入 Toast 消息组件

// 接收来自父组件的 `visible` 状态
const props = defineProps({
  visible: {
    type: Boolean,
    required: true,
  },
})

// 定义 `update:visible` 和 `update-avatar` 事件
const emit = defineEmits(['update:visible', 'update-avatar'])

const localVisible = ref(false) // 内部控制对话框显示状态的变量
const avatar = ref<File | null>(null)
const avatarUrl = ref<string | null>(null)
const defaultAvatar = 'https://placehold.co/256x256' // 默认头像
const loading = ref(false) // 上传状态

const toast = useToast() // 用于显示上传提示

// 国际化
const { t } = useI18n()

// 监听父组件的 `visible` 属性变化
watch(
  () => props.visible,
  newVal => {
    localVisible.value = newVal
  },
  { immediate: true },
)

// 文件选择处理
const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    avatar.value = target.files[0]
    const reader = new FileReader()
    reader.onload = e => {
      avatarUrl.value = e.target?.result as string
    }
    reader.readAsDataURL(target.files[0])
  }
}

// 取消操作
const handleCancel = () => {
  avatar.value = null
  avatarUrl.value = null
  emit('update:visible', false)
}

// 保存操作（上传逻辑）
const handleSave = async () => {
  if (!avatar.value) {
    return
  }

  try {
    loading.value = true

    const response = await uploadAvatar(avatar.value)
    toast.add({
      severity: 'success',
      summary: t('toast.success'),
      detail: t('toast.successDetail'),
      life: 3000,
    })

    emit('update-avatar', response.data.avatar) // 通知父组件更新头像
    avatar.value = null
    avatarUrl.value = null
    emit('update:visible', false) // 关闭对话框
  } catch (error) {
    console.error('上传失败：', error)
    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail: t('toast.unknownError'),
      life: 3000,
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex justify-center">
    <Dialog
      v-model:visible="localVisible"
      modal
      :header="t('title')"
      :style="{ width: '25rem' }"
      @hide="emit('update:visible', false)"
    >
      <span class="mb-8 block text-surface-500 dark:text-surface-400">
        {{ t('description') }}
      </span>

      <!-- 头像上传部分 -->
      <div class="mb-6 flex flex-col items-center px-8">
        <img
          :src="avatarUrl || defaultAvatar"
          alt="Avatar"
          class="mb-6 h-36 w-36 rounded-full object-cover"
        />
        <InputText type="file" @change="onFileChange" accept="image/*" fluid />
      </div>

      <!-- 按钮部分 -->
      <div class="flex justify-end gap-2">
        <Button
          type="button"
          :label="t('cancel')"
          severity="secondary"
          @click="handleCancel"
        ></Button>
        <Button
          type="button"
          :label="t('save')"
          @click="handleSave"
          :disabled="!avatar || loading"
          :loading="loading"
        ></Button>
      </div>
    </Dialog>
  </div>
</template>

<i18n locale="zh-CN">
{
  "title": "修改头像",
  "description": "编辑你的头像。",
  "cancel": "取消",
  "save": "保存",
  "toast": {
    "success": "上传成功",
    "successDetail": "头像已更新",
    "error": "上传失败",
    "unknownError": "未知错误",
  },
}
</i18n>
