<script setup lang="ts" name="AvatarPanel">
import { defineProps, defineEmits, ref, watch } from 'vue'
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
const defaultAvatar = 'https://via.placeholder.com/150' // 默认头像

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
  console.log('Avatar File:', avatar.value)

  if (!avatar.value) {
    toast.add({
      severity: 'warn',
      summary: t('cancel'),
      detail: t('请选择文件后再保存'),
      life: 3000,
    })
    return
  }

  try {
    const response = await uploadAvatar(avatar.value)
    toast.add({
      severity: 'success',
      summary: t('save'),
      detail: t('头像上传成功'),
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
      summary: t('保存失败'),
      detail: t('头像上传失败，请稍后再试'),
      life: 3000,
    })
  }
}
</script>

<template>
  <div class="flex justify-center">
    <Dialog
      v-model:visible="localVisible"
      modal
      :header="t('editProfile')"
      :style="{ width: '25rem' }"
      @hide="emit('update:visible', false)"
    >
      <span class="mb-8 block text-surface-500 dark:text-surface-400">
        {{ t('updateYourInformation') }}
      </span>

      <!-- 头像上传部分 -->
      <div class="mb-6 flex flex-col items-center">
        <img
          :src="avatarUrl || defaultAvatar"
          alt="Avatar"
          class="mb-4 h-24 w-24 rounded-full object-cover"
        />
        <InputText type="file" @change="onFileChange" accept="image/*" />
      </div>

      <!-- 按钮部分 -->
      <div class="flex justify-end gap-2">
        <Button
          type="button"
          :label="t('cancel')"
          severity="secondary"
          @click="handleCancel"
        ></Button>
        <Button type="button" :label="t('save')" @click="handleSave"></Button>
      </div>
    </Dialog>
  </div>
</template>

<style scoped>
.card {
  /* 示例样式 */
  padding: 1rem;
  background-color: var(--color-card-background, #fff);
  border-radius: 0.5rem;
  box-shadow: var(--shadow, 0 2px 8px rgba(0, 0, 0, 0.1));
}
</style>

<i18n locale="zh-CN">
{
  "editProfile": "修改头像",
  "updateYourInformation": "编辑你的头像。",
  "cancel": "取消",
  "save": "保存"
}
</i18n>
