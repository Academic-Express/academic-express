<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'

const { t } = useI18n()

const newInstitution = ref<string>('')
const recommendedInstitutions = ref<Array<{ name: string; followed: boolean }>>(
  [
    { name: 'Microsoft', followed: false },
    { name: 'Google', followed: false },
    { name: 'Tsinghua University', followed: false },
  ],
)
const followedInstitutions = ref<Array<{ name: string }>>([])
const hoveredIndex = ref<number>(-1)

function addInstitution() {
  if (newInstitution.value) {
    const existingFollowed = followedInstitutions.value.some(
      institution => institution.name === newInstitution.value,
    )

    if (!existingFollowed) {
      followedInstitutions.value.push({ name: newInstitution.value })
    }

    const recommended = recommendedInstitutions.value.find(
      item => item.name === newInstitution.value,
    )
    if (recommended) {
      recommended.followed = true
    }

    newInstitution.value = ''
  }
}

function toggleFollow(index: number) {
  const institution = recommendedInstitutions.value[index]
  institution.followed = !institution.followed

  if (institution.followed) {
    if (
      !followedInstitutions.value.some(item => item.name === institution.name)
    ) {
      followedInstitutions.value.push({ name: institution.name })
    }
  } else {
    followedInstitutions.value = followedInstitutions.value.filter(
      item => item.name !== institution.name,
    )
  }
}

function removeInstitution(index: number) {
  const removedInstitution = followedInstitutions.value[index]
  followedInstitutions.value.splice(index, 1)

  const recommended = recommendedInstitutions.value.find(
    item => item.name === removedInstitution.name,
  )
  if (recommended) recommended.followed = false
}
</script>

<template>
  <div class="space-y-6 p-4">
    <!-- Sub-component 1 -->
    <div class="flex space-x-2">
      <InputText
        v-model="newInstitution"
        :placeholder="t('inputBox.placeholder')"
        class="min-w-0 flex-1"
        size="small"
      />
      <Button
        :label="t('inputBox.addButton')"
        icon="pi pi-plus"
        size="small"
        @click="addInstitution"
      ></Button>
    </div>

    <!-- Sub-component 2 -->
    <div class="space-y-2">
      <h3 class="font-bold">{{ t('recommendedInstitutions') }}</h3>
      <div class="flex flex-wrap gap-2">
        <Chip
          v-for="(institution, index) in recommendedInstitutions"
          :key="index"
          :label="institution.name"
          class="cursor-pointer text-sm hover:text-blue-500"
          :icon="institution.followed ? 'pi pi-check' : 'pi pi-plus'"
          @click="toggleFollow(index)"
        />
      </div>
    </div>

    <!-- Sub-component 3-->
    <div class="space-y-2">
      <h3 class="font-bold">{{ t('followedInstitutions') }}</h3>
      <div class="flex flex-wrap gap-2">
        <Chip
          v-for="(institution, index) in followedInstitutions"
          :key="index"
          :label="institution.name"
          class="cursor-pointer text-sm hover:text-red-500"
          :icon="hoveredIndex === index ? 'pi pi-times' : 'pi pi-check'"
          @mouseenter="hoveredIndex = index"
          @mouseleave="hoveredIndex = -1"
          @click="removeInstitution(index)"
        />
      </div>
    </div>
  </div>
</template>

<i18n locale="zh-CN">
{
  "inputBox": {
    "placeholder": "请输入机构名称",
    "addButton": "添加"
  },
  "recommendedInstitutions": "推荐的机构",
  "followedInstitutions": "已关注的机构",
}
</i18n>
