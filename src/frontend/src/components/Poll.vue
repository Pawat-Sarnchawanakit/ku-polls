<template>
    <div style="background-color: transparent;height: 100%;overflow: auto;">
        <dialog @close="dialog_closed" ref="dlg" style="background-color: #2B2B2B;border: none; border-radius: 10px;"><h1 :style="{ 'color': dlg_col }"> {{ dlg_text }}</h1><br/><p style="color: #FFF;margin: auto;text-align: center">Press ESC to close.</p></dialog>
        <div ref="poll"></div>
        <div v-if="loaded" style="display: flex;justify-content: center;margin-bottom: 10px"><button @click="submit">Submit</button></div>
    </div>
</template>

<style scoped>
dialog::backdrop {
    backdrop-filter: blur(2px);
}
button {
    border: none;
    border-radius: 10px;
    background: #3B3B3B;
    color: #FFF;
    font-weight: bold;
    font-size: 16pt;
    flex: 0 0 150px;
    height: 50px;
}
button:hover {
    background: #4B4B4B;
}
button:active {
    background: #5B5B5B;
}
</style>

<script setup>
import { ref, onMounted } from 'vue';
import { validate_yaml, display_poll, get_poll_answers, AllowType } from "/src/poll_loader.js"
var mounted = false;
const dlg_col = ref("#FFF")
const dlg_text = ref("Please answer all questions.");
const dlg = ref(false);
const loaded = ref(false);
const poll = ref(null);
let submitted = false;
const poll_id = document.location.pathname.split('/').filter((a) => a.length != 0)[1];
let poll_data;
function onYamlLoaded(body) {
    const result = validate_yaml(body);
    if(!result.ok) {
        submitted = true;
        dlg_col.value = "#F00";
        dlg_text.value = result.message;
        dlg.value.showModal();
        return;
    }
    poll_data = result.yaml;
    if(poll_data.allow != 0 && (poll_data.allow & AllowType.CLIENT) != 0 && localStorage.getItem("answered_" + poll_id) == 'y') {
        submitted = true;
        dlg_col.value = "#FFF";
        dlg_text.value = "You already answered this poll.";
        dlg.value.showModal();
        return;
    }
    display_poll(poll.value, poll_data);
    loaded.value = true;
}
onMounted(() => mounted = true);
fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        f: "get",
        n: poll_id
    })
}).then(res => res.text().then((body) => {
    if(mounted)
        onYamlLoaded(body)
    else onMounted(() => onYamlLoaded(body));
}));
// onMounted(() => {
// onYamlLoaded(`
// allow: CLIENT
// poll:
//     - info:
//         type: LABEL
//         text: "Example Survey"
//         label: "The purpose of this survey is to know what people think the meaning of life is.\nThis should give insight into why people commit suicide."
//     - name:
//         type: SHORT
//         text: "What is your name?"
//     - 1:
//         type: CHOICE
//         text: "What is the meaning of life?"
//         required: true
//         choices:
//             - a: "The engine of a film."
//             - b: "The fine game of nil."
//             - c: "42"
//             - d: "The meaning of life is a subjective concept that varies from person to person, often encompassing themes of purpose, fulfillment, and personal growth."
// `);
// });
function dialog_closed() {
    if(submitted)
        window.location = window.location.protocol + "//" + window.location.host;
}
function submit() {
    if(submitted)
        return;
    submitted = true;
    const answers = get_poll_answers(poll.value, poll_data);
    if(!answers.ok) {
        dlg_col.value = "#F00";
        dlg_text.value = answers.message;
        dlg.value.showModal();
        submitted = false;
        return;
    }
    dlg_col.value = "#FFF";
    dlg_text.value = "Please wait, submitting..."
    dlg.value.showModal();
    fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            f: "submit",
            n: poll_id,
            r: answers.answers
        })
    }).then(res => res.text().then((body) => {
        if(!res.ok && body == "")
            body = res.statusText;
        const is_ok = body == "ok";
        dlg_col.value = is_ok ? "#FFF" : "#F00";
        dlg_text.value = is_ok ? "Your response has been recorded." : body;
        dlg.value.showModal();
        if(!is_ok) {
            submitted = false;
            return;
        }
        if(poll_data.allow != 0 && (poll_data.allow & AllowType.CLIENT) != 0)
            localStorage.setItem("answered_" + poll_id, 'y');
    })).catch(() => {
        dlg_col.value = "#F00";
        dlg_text.value = "Failed to submit response.";
        dlg.value.showModal();
        submitted = false;
    });
}
</script>