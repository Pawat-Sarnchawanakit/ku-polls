<template>
    <div style="background-color: transparent;height: 100%;overflow: auto;">
        <div style="display: flex;flex-direction: row;">
            <a href="/"><input class="left-btn" :style='{ "background-image": `url("${home_img}")` }' type="button"/></a>
            <input v-if="can_view_res || is_creator" @click="view_response" class="left-btn" :style='{ "background-image": `url("${bars_img}")` }' type="button"/>
            <input v-if="is_creator" @click="edit_poll" class="left-btn" :style='{ "background-image": `url("${edit_img}")` }' type="button"/>
        </div>
        <dialog ref="dlg" style="background-color: #2B2B2B;border: none; border-radius: 10px;"><h1 :style="{ 'color': dlg_col }"> {{ dlg_text }}</h1><br/><p style="color: #FFF;margin: auto;text-align: center">Press ESC to close.</p></dialog>
        <div ref="poll"></div>
        <div v-if="loaded" style="display: flex;justify-content: center;margin-bottom: 10px"><button @click="submit">Submit</button></div>
    </div>
</template>

<style scoped>
.left-btn {
    user-select: none;
    margin: 5px;
    background-color: #3B3B3B;
    background-size: cover;
    width: 50px;
    height: 50px;
    border: none;
    border-radius: 10px;
    display: block;
}
.left-btn:hover {
    background-color: #4B4B4B;
}
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
import home_img from './../assets/home.svg?url';
import edit_img from './../assets/edit.svg?url';
import bars_img from './../assets/bars.svg?url';
var mounted = false;
const can_view_res = ref(true);
const is_creator = ref(true);
const dlg_col = ref("#FFF")
const dlg_text = ref("Please answer all questions.");
const dlg = ref(false);
const loaded = ref(false);
const poll = ref(null);
let submitted = false;
const poll_id = document.location.pathname.split('/').filter((a) => a.length != 0)[1];
let poll_data;

function view_response() {
    document.location.href = window.location.protocol + "//" + window.location.host + "/res/" + poll_id;
}

function edit_poll() {
    document.location.href = window.location.protocol + "//" + window.location.host + "/create/" + poll_id;
}

async function onYamlLoaded(body) {
    const result = validate_yaml(body);
    if(!result.ok) {
        submitted = true;
        dlg_col.value = "#F00";
        dlg_text.value = result.message;
        dlg.value.showModal();
        return;
    }
    if(result.res == 0)
        can_view_res.value = true;
    poll_data = result.yaml;
    submitted = true;
    if(poll_data.allow == 0) {
        submitted = false;
    } else {
        if((poll_data.allow & AllowType.CLIENT) != 0) {
            if(localStorage.getItem("answered_" + poll_id) == 'y') {
                dlg_col.value = "#FFF";
                dlg_text.value = "You already answered this poll.";
                dlg.value.showModal();
                submitted = true;
            } else submitted = false;
        }
        // console.log(submitted, poll_data.allow, AllowType.AUTH, (poll_data.allow & AllowType.AUTH) != 0);
        if(submitted && (poll_data.allow & AllowType.AUTH) != 0) {
            submitted = true;
            const res = await fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    f: "aa",
                    n: poll_id,
                })
            });
            const body = await res.text()
            if(body != 'y')
                submitted = false;
            else {
                dlg_col.value = "#FFF";
                dlg_text.value = "You already answered this poll.";
                dlg.value.showModal();
            }
        }
    }
    display_poll(poll.value, poll_data);
    if(!submitted)
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
}).then(res => res.json().then((body) => {
    if(body.is_creator)
        is_creator.value = true;
    if(body.login)
        window.location.href = window.location.protocol + "//" + window.location.host + "/login";
    if(mounted)
        return onYamlLoaded(body.yaml)
    return onMounted(() => onYamlLoaded(body.yaml));
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