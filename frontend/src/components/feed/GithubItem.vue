<script setup lang="ts">
import type { GithubRepo } from '@/services/api'
import { useThemeStore } from '@/stores/theme'

import githubMark from '@/assets/github-mark.svg'
import githubMarkWhite from '@/assets/github-mark-white.svg'

defineProps<{
  githubRepo: GithubRepo
}>()

const themeStore = useThemeStore()
</script>

<template>
  <div>
    <div class="flex gap-4">
      <!-- Avator -->
      <img
        v-if="githubRepo"
        :src="githubRepo.owner.avatar_url"
        alt="Owner Avatar"
        class="h-7 w-7 rounded-full"
      />
      <!-- Title -->
      <div class="mb-3 line-clamp-1 text-xl font-bold" v-if="githubRepo">
        <RouterLink
          :to="{
            name: 'pub-github',
            params: { owner: githubRepo.owner.login, repo: githubRepo.name },
          }"
          class="transition-colors hover:text-blue-500 hover:underline"
        >
          {{ githubRepo.full_name }}
        </RouterLink>
      </div>
    </div>

    <!-- Description -->
    <div class="mb-3 flex items-center">
      <p v-if="githubRepo" class="line-clamp-3">{{ githubRepo.description }}</p>
    </div>

    <!-- Topics -->
    <div class="mb-4 flex flex-wrap gap-x-4 gap-y-2" v-if="githubRepo">
      <Button
        v-for="topic in githubRepo.topics"
        :key="topic"
        class="p-button-sm text-xs"
        severity="secondary"
      >
        {{ topic }}
      </Button>
    </div>

    <div class="flex gap-6 text-gray-600 dark:text-gray-400">
      <!-- Language -->
      <template v-if="githubRepo && githubRepo.language">
        <span>
          <i class="pi pi-tag"></i>
          {{ githubRepo.language }}
        </span>
      </template>

      <!-- Stars -->
      <template v-if="githubRepo">
        <span>
          <i class="pi pi-star"></i>
          {{ githubRepo.stargazers_count }}
        </span>
      </template>

      <!-- Watches -->
      <template v-if="githubRepo">
        <span>
          <i class="pi pi-eye"></i>
          {{ githubRepo.subscribers_count }}
        </span>
      </template>

      <!-- Forks -->
      <template v-if="githubRepo">
        <span>
          <i class="pi pi-share-alt -rotate-90"></i>
          {{ githubRepo.forks_count }}
        </span>
      </template>

      <div class="ml-auto mr-2 flex items-center">
        <a :href="githubRepo.html_url" target="_blank">
          <img
            :src="themeStore.darkMode ? githubMarkWhite : githubMark"
            alt="Github Logo"
            class="h-5"
          />
        </a>
      </div>
    </div>
  </div>
</template>
