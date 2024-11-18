<script setup lang="ts">

// Hard-coded article data
const article = {
  title: "Learning General-Purpose Biomedical Volume Representations using\n  Randomized Synthesis",
  summary:
    "Current volumetric biomedical foundation models struggle to generalize as\npublic 3D datasets are small and do not cover the broad diversity of medical\nprocedures, conditions, anatomical regions, and imaging protocols. We address\nthis by creating a representation learning method that instead anticipates\nstrong domain shifts at training time itself. We first propose a data engine\nthat synthesizes highly variable training samples that enable generalization to\nnew biomedical contexts. To then train a single 3D network for any voxel-level\ntask, we develop a contrastive learning method that pretrains the network to be\nstable against nuisance imaging variation simulated by the data engine, a key\ninductive bias for generalization. This network's features can be used as\nrobust representations of input images for downstream tasks and its weights\nprovide a strong, dataset-agnostic initialization for finetuning on new\ndatasets. As a result, we set new standards across both multimodality\nregistration and few-shot segmentation, a first for any 3D biomedical vision\nmodel, all without (pre-)training on any existing dataset of real images.",
  authors: [
    "Neel Dey",
    "Benjamin Billot",
    "Hallee E. Wong",
    "Clinton J. Wang",
    "Mengwei Ren",
    "P. Ellen Grant",
    "Adrian V. Dalca",
    "Polina Golland",
    "Heyang Jiang",
    "Ruotong Sun"
  ],
  published: "2024-11-04T18:40:46Z",
  updated: "2024-11-04T18:40:46Z",
  primary_category: "cs.CV",
  categories: ["cs.CV", "cs.LG"],
  link: "http://arxiv.org/abs/2411.02372v1",
  pdf: "https://arxiv.org/pdf/2411.02372v1",
}
</script>

<template>
  <div class="container mx-auto p-4">
    <div class="p-6 rounded-lg shadow-md">
      <!-- Title -->
      <h1 class="text-2xl font-bold mb-4">{{ article.title }}</h1>

      <!-- Authors -->
      <div class="mb-4">
        <h2 class="text-lg font-bold">Authors:</h2>
        <p>{{ article.authors.join(", ") }}</p>
      </div>

      <!-- Summary -->
      <div class="mb-4">
        <h2 class="text-lg font-bold">Summary:</h2>
        <p>{{ article.summary }}</p>
      </div>

      <!-- Categories -->
      <div class="mb-4">
        <div class="flex flex-wrap gap-2">
          <button
            v-for="category in article.categories"
            :key="category"
            class="px-4 py-2 bg-red-200 text-gray-700 rounded hover:bg-red-300"
          >
            {{ category }}
          </button>
        </div>
      </div>

      <!-- Publication Dates -->
      <div class="mb-4">
        <p><strong>Published:</strong> {{ new Date(article.published).toLocaleString() }}</p>
        <p><strong>Updated:</strong> {{ new Date(article.updated).toLocaleString() }}</p>
      </div>

      <!-- Links -->
      <div class="flex gap-4">
        <a
          :href="article.link"
          target="_blank"
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          View Original
        </a>
        <a
          :href="article.pdf"
          target="_blank"
          class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Download PDF
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 960px;
}
</style>