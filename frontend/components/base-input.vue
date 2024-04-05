<script setup lang="ts">
defineProps<{
  label: string
}>()

const model = defineModel()
</script>

<template>
  <div class="flex flex-col gap-2">
    <label class="text-xl text-white">{{ label }}</label>
    <input v-model="model" class="rounded-full shadow-lg border-violet-700 border-2">
  </div>
</template>
