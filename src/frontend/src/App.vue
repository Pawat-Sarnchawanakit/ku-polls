<script setup>
import { ref } from 'vue';
import Poll from './components/Poll.vue';
import Editor from './components/Editor.vue';
let tipe = "index";
switch(document.location.pathname.split('/').filter((a) => a.length != 0)[0]) {
  case 'create':
    tipe = 'create';
    break;
  case 'poll':
    tipe = 'poll';
    break;
}
const path = ref(tipe);
</script>

<template>
  <Editor v-if="path == 'create'"/>
  <Poll v-if="path == 'poll'"/>
</template>

<style scoped>
</style>
