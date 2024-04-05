<template>
    <div class="flex flex-col gap-2">
    <label class="text-xl text-white">{{ label }}</label>
    <input class="rounded-full shadow-lg border-violet-700 border-2" v-model="model" />
    </div>
</template>

<script setup lang="ts">
defineProps<{
    label: string
}>()

const model = defineModel()
</script>