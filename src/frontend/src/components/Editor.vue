<template>
  <dialog ref="dlg" style="color: #F00">
  </dialog>
  <div style="background-color: #1E1E1E; height: 100%; display: flex;flex-direction: column">
    <h1 style="color: #FFF;margin: auto;text-align: center;">Create a poll</h1>
    <div class="editor" ref="script_editor"></div>
    <div style="display: flex;justify-content: space-evenly;">
      <button @click="create">Create</button>
      <button @click="preview">Preview</button>
    </div>
  </div>
</template>

<style scoped>
dialog {
  border: none;
  border-radius: 10px;
  background-color: #2B2B2B;
}
button {
  margin: 5px;
  color: #FFF;
  font-size: 16pt;
  height: 50px;
  width: 150px;
  border: none;
  border-radius: 10px;
  background-color: #2B2B2B;
}
button:hover {
  background-color: #3B3B3B;
}
.editor {
  flex: 1 1 auto;
}
</style>

<script setup>
import { ref, onMounted } from "vue"
import * as monaco from 'monaco-editor';
import { load_yaml } from "/src/poll_loader.js"
const dlg = ref(null);
const script_editor = ref(null);

const example = `
poll:
    - name:
        type: SHORT
        text: "What is your name?"
    - 1:
        type: CHOICE
        text: "What is the meaning of life?"
        choices:
            - a: "The engine of a film."
            - b: "The fine game of nil."
            - c: "42"
            - d: "The meaning of life is a subjective concept that varies from person to person, often encompassing themes of purpose, fulfillment, and personal growth."
`;

let monaco_editor;

function create() {
  const yml = monaco_editor.getValue()
  const res = load_yaml(yml);
  if(!res.ok) {
    dlg.value.innerText = res;
    dlg.value.showModal();
    return;
  }
  dlg.value.innerText = "Created"
  dlg.value.showModal();
  fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      f: "create",
      y: yml
    })
  }).then(res => {});
}

function preview() {
  const res = load_yaml(monaco_editor.getValue());
  if(res.ok) {
    dlg.value.innerHTML = res.content;
  } else {
    dlg.value.innerText = res;
  }
  dlg.value.showModal();
}

onMounted(() => {
  monaco_editor = monaco.editor.create(script_editor.value, {
        value: example,
        language: 'yaml',
        automaticLayout: true,
        theme: 'vs-dark',
        tabSize: 4,
    });
})
</script>