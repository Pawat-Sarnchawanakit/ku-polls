<script setup>
import { ref } from 'vue';
import Home from './components/Home.vue';
import Poll from './components/Poll.vue';
import Editor from './components/Editor.vue';
const page_type = ref("");
switch(document.location.pathname.split('/').filter((a) => a.length != 0)[0]) {
  case 'create':
    page_type.value = 'create';
    break;
  case 'poll':
    page_type.value = 'poll';
    break;
  default:
    page_type.value = '';
    break;
}
const path = ref(page_type);
</script>

<template>
  <Editor v-if="path == 'create'"/>
  <Poll v-if="path == 'poll'"/>
  <Home v-if="path == ''" @change_page="(new_page) => page_type=new_page"/>
</template>

<style scoped>
</style>
