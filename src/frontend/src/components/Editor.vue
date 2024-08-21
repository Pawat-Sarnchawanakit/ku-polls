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
import { validate_yaml, display_poll } from "/src/poll_loader.js"
const dlg = ref(null);
const script_editor = ref(null);

const example = `
name: "The meaning of life"
image: "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.stock-free.org%2Fimages%2Fstock-free-test-photo-07092015-16.jpg&f=1&nofb=1&ipt=8fe8731f129a2098c9e0a559a7f987f32e7d832a6fbee15968c9a1b4aed2a9d5&ipo=images"
allow: CLIENT
poll:
    - info:
        type: LABEL
        text: "Example Survey"
        label: "The purpose of this survey is to know what people think the meaning of life is.\\nThis should give insight into why people commit suicide."
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
  const res = validate_yaml(yml);
  if(!res.ok) {
    dlg.value.innerText = res.message;
    dlg.value.showModal();
    return;
  }
  dlg.value.innerText = "Creating..."
  dlg.value.showModal();
  fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      f: "create",
      n: res.yaml.name,
      i: res.yaml.image,
      a: res.yaml.allow,
      y: yml
    })
  }).then(_ => {
    dlg.value.innerText = "Created"
    dlg.value.showModal();
  });
}

function preview() {
  const res = validate_yaml(monaco_editor.getValue());
  if(!res.ok) {
    const text = document.createElement("p");
    text.setAttribute("style", "color: #F00")
    text.innerText = res.message;
    dlg.value.showModal();
    return;
  }
  dlg.value.innerHTML = '';
  display_poll(dlg.value, res.yaml, false);
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
  const saved_poll = localStorage.getItem("saved_poll");
  if(saved_poll != null)
    monaco_editor.setValue(saved_poll);
  setInterval(() => localStorage.setItem("saved_poll", monaco_editor.getValue()), 3000);
})
</script>