<template>
    <div style="background-color: transparent;height: 100%;overflow: auto;">
        <div style="display: flex;flex-direction: row;">
            <a href="/"><input class="left-btn" :style='{ "background-image": `url("${home_img}")` }' type="button"/></a>
            <input v-if="can_view_res || is_creator" title="View responses" @click="view_response" class="left-btn" :style='{ "background-image": `url("${bars_img}")` }' type="button"/>
            <input v-if="is_creator" title="Edit poll" @click="edit_poll" class="left-btn" :style='{ "background-image": `url("${edit_img}")` }' type="button"/>
            <input v-if="allow_delete" title="Delete responses" @click="delete_answers" class="left-btn" :style='{ "background-image": `url("${delete_img}")` }' type="button"/>
            <input v-if="!authenticated" title="Login" @click="login" class="left-btn" :style='{ "background-image": `url("${login_img}")` }' type="button"/>
            <input v-if="authenticated" title="Logout" @click="log_out" class="left-btn" :style='{ "background-image": `url("${logout_img}")` }' type="button"/>
        </div>
        <dialog ref="dlg" style="background-color: #2B2B2B;border: none; border-radius: 10px;"><h1 :style="{ 'color': dlg_col }"> {{ dlg_text }}</h1><br/><p style="color: #FFF;margin: auto;text-align: center">Press ESC to close.</p></dialog>
        <div ref="poll"></div>
        <div v-if="loaded" style="display: flex;justify-content: center;margin-bottom: 10px"><button @click="submit">{{ submit_text }}</button></div>
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
import { login, log_out } from '/src/common.js';
import { ref, onMounted } from 'vue';
import { validate_yaml, display_poll, get_poll_answers, refill_poll_answers, AllowType } from "/src/poll_loader.js"
import home_img from './../assets/home.svg?url';
import edit_img from './../assets/edit.svg?url';
import bars_img from './../assets/bars.svg?url';
import delete_img from './../assets/delete.svg?url';
import login_img from './../assets/login.svg?url';
import logout_img from './../assets/logout.svg?url';
const submit_text = ref('Submit');
const can_view_res = ref(false);
const is_creator = ref(false);
const allow_delete = ref(false);
const dlg_col = ref("#FFF")
const dlg_text = ref("Please answer all questions.");
const dlg = ref(false);
const loaded = ref(false);
const poll = ref(null);
const data = JSON.parse(document.getElementById("server-data").innerText);
const authenticated = ref(data.auth);
let cantsubmit = false;
const poll_id = document.location.pathname.split('/').filter((a) => a.length != 0)[1];
let poll_data;

if(data.is_creator)
    is_creator.value = true;
if(data.can_res)
    can_view_res.value = true;

onMounted(() => onYamlLoaded(data));

function view_response() {
    document.location.href = window.location.protocol + "//" + window.location.host + "/res/" + data.id;
}

function edit_poll() {
    document.location.href = window.location.protocol + "//" + window.location.host + "/create/" + data.id;
}

function onYamlLoaded(body) {
    if(body.yaml != null) {
        const result = validate_yaml(body.yaml);
        if(!result.ok) {
            cantsubmit = true;
            dlg_col.value = "#F00";
            dlg_text.value = result.message;
            dlg.value.showModal();
            return;
        }
        if(result.res == 0)
            can_view_res.value = true;
        poll_data = result.yaml;
        cantsubmit = true;
        if(poll_data.allow == 0) {
            cantsubmit = false;
        } else if((poll_data.allow & AllowType.CLIENT) != 0 && !body.auth) {
            if(localStorage.getItem("answered_" + poll_id) == 'y') {
                dlg_col.value = "#FFF";
                dlg_text.value = "You already answered this poll.";
                dlg.value.showModal();
                cantsubmit = true;
            } else cantsubmit = false;
        } else cantsubmit = false;
        display_poll(poll.value, poll_data);
        if(!cantsubmit && body.prev_ans.length > 0) {
            allow_delete.value = true;
            refill_poll_answers(poll.value, result.yaml, body.prev_ans);
            dlg_col.value = "#FFF";
            dlg_text.value = "You already answered this poll.";
            dlg.value.showModal();
            submit_text.value = "Change answers";
        }
    } else {
        const msg = document.createElement("h1");
        msg.innerText = "You don't have permission to view this poll.";
        msg.style.color = "#FFF";
        msg.style.margin = "auto";
        msg.style.textAlign = "center";
        poll.value.appendChild(msg);
    }
    
    
    if(body.closed) {
        cantsubmit = true;
        dlg_col.value = "#F00";
        dlg_text.value = "This poll is already closed.";
        dlg.value.showModal();
    } else if(!body.can_vote) {
        cantsubmit = true;
        dlg_col.value = "#F00";
        dlg_text.value = "You do not have permission to vote in this poll.";
        dlg.value.showModal();
    }
    if(!cantsubmit)
        loaded.value = true;
}

// fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({
//         f: "get",
//         n: poll_id
//     })
// }).then(res => res.json().then((body) => {
//     if(body.is_creator)
//         is_creator.value = true;
//     if(body.can_res)
//         can_view_res.value = true;
//     if(mounted)
//         return onYamlLoaded(body)
//     return onMounted(() => onYamlLoaded(body.yaml));
// }));
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

function delete_answers() {
    fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            f: "submit",
            n: poll_id,
            r: []
        })
    }).then(res => res.text().then((body) => {
        if(!res.ok && body == "")
            body = res.statusText;
        const is_ok = body == "ok";
        dlg_col.value = is_ok ? "#FFF" : "#F00";
        dlg_text.value = is_ok ? "Your response has been deleted." : body;
        dlg.value.showModal();
        if(!is_ok) {
            cantsubmit = false;
            return;
        }
        if(cantsubmit)
            loaded.value = false;
        setTimeout(() => window.location.reload(true), 500);
    })).catch(() => {
        dlg_col.value = "#F00";
        dlg_text.value = "Failed to delete response.";
        dlg.value.showModal();
        cantsubmit = false;
    });
}

function submit() {
    if(cantsubmit)
        return;
    cantsubmit = true;
    const answers = get_poll_answers(poll.value, poll_data);
    if(!answers.ok) {
        dlg_col.value = "#F00";
        dlg_text.value = answers.message;
        dlg.value.showModal();
        cantsubmit = false;
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
            cantsubmit = false;
            return;
        }
        if(cantsubmit)
            loaded.value = false;
        if(poll_data.allow != 0 && (poll_data.allow & AllowType.CLIENT) != 0)
            localStorage.setItem("answered_" + poll_id, 'y');
        setTimeout(() => window.location.reload(true), 500);
    })).catch(() => {
        dlg_col.value = "#F00";
        dlg_text.value = "Failed to submit response.";
        dlg.value.showModal();
        cantsubmit = false;
    });
}
</script>