<template>
  <dialog ref="dlg">
  </dialog>
  <div style="background-color: #1E1E1E; height: 100%; display: flex;flex-direction: column">
    <h1 style="color: #FFF;margin: auto;text-align: center;">{{ header_msg }}</h1>
    <div class="editor" ref="script_editor"></div>
    <div style="display: flex;justify-content: space-evenly;">
      <button @click="create">{{ create_btn_msg }}</button>
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
const paths = document.location.pathname.split('/').filter((a) => a.length != 0);
let poll_id = null;
if(paths.length > 1)
  poll_id = paths[1];
import { ref, onMounted } from "vue"
import * as monaco from 'monaco-editor';
import { validate_yaml, display_poll } from "/src/poll_loader.js"
const header_msg = ref("Create a poll");
const create_btn_msg = ref("Create");
const dlg = ref(null);
const script_editor = ref(null);

function setupDialog(caption, header, caption_color="#FFF", header_color="#FFF") {
  dlg.value.innerHTML = '';
  const header_element = document.createElement("h1");
  header_element.setAttribute("style", "color: " + header_color + ";margin: auto;margin-top: 0;text-align: center");
  header_element.innerText = header;
  dlg.value.appendChild(header_element);
  const content_element = document.createElement("p");
  content_element.setAttribute("style", "color: " + caption_color);
  content_element.innerText = caption;
  dlg.value.appendChild(content_element);
  const hint_element = document.createElement("p");
  hint_element.setAttribute("style", "color: #FFF;margin: auto;margin-top: 0;text-align: center");
  hint_element.innerText = "Press ESC to close";
  dlg.value.appendChild(hint_element);
}

let example = 
`name: "The meaning of life"
image: "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.stock-free.org%2Fimages%2Fstock-free-test-photo-07092015-16.jpg&f=1&nofb=1&ipt=8fe8731f129a2098c9e0a559a7f987f32e7d832a6fbee15968c9a1b4aed2a9d5&ipo=images"
allow: CLIENT
res: '*'
# Time the poll is available, in Unix time.
begin: ${new Date/1E3|0}
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

let mounted = false;
let monaco_editor;

if(poll_id != null) {
  header_msg.value = "Edit poll";
  create_btn_msg.value = "Update";
  fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        f: "get",
        n: poll_id
    })
  }).then(res => res.json().then((body) => {
      if(mounted) {
        monaco_editor.setValue(body.yaml);
        return;
      }
      example = body.yaml;
  }));
}

function create() {
  const yml = monaco_editor.getValue()
  const res = validate_yaml(yml);
  if(!res.ok) {
    dlg.value.innerText = res.message;
    dlg.value.showModal();
    return;
  }
  setupDialog("Creating...", "Info");
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
      r: res.yaml.res,
      e: poll_id,
      y: yml
    })
  }).then(res => {
    if(res.ok) {
      setupDialog("Created", "Info");
      dlg.value.showModal();
      return;
    }
    res.text().then((text) => {
      setupDialog(text || res.statusText, "Error", "#F00");
      dlg.value.showModal();
    });
  }).catch(err => {
    setupDialog(err, "Error", "#F00");
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
  mounted = true;
  setInterval(() => localStorage.setItem("saved_poll", monaco_editor.getValue()), 3000);
})
</script>