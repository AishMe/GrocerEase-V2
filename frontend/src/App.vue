<template>
  <div>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { computed, reactive } from 'vue'
import { useHead } from '@vueuse/head'
</script>

<script>
export default {
  name: 'App',
  setup() {
    const siteData = reactive({
      title: `GrocerEase`,
      description: `Shop with Ease, Groceries at your Fingertips.`
    })
    useHead({
      // Can be static or computed
      title: computed(() => siteData.title),
      meta: [
        {
          name: `description`,
          content: computed(() => siteData.description)
        },
      ],
    })
  },
  async mounted() {
    await this.$store.commit('initialiseStore')
  },
}
</script>
