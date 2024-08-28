<template>
    <div style="background-color: transparent;height: 100%;overflow: auto;">
        <div style="display: flex;flex-direction: row;">
            <a href="/"><input class="left-btn" :style='{ "background-image": `url("${home_img}")` }' type="button"/></a>
            <input @click="view_poll" v-if="data.can_view" class="left-btn" :style='{ "background-image": `url("${poll_img}")` }' type="button"/>
            <input @click="edit_poll" v-if="data.can_edit" class="left-btn" :style='{ "background-image": `url("${edit_img}")` }' type="button"/>
        </div>
        <dialog ref="dlg" style="background-color: #2B2B2B;border: none; border-radius: 10px;"><h1 :style="{ 'color': dlg_col }"> {{ dlg_text }}</h1><br/><p style="color: #FFF;margin: auto;text-align: center">Press ESC to close.</p></dialog>
        <div class="qb" v-for="(values, name) in responses">
            <h1>{{ name }}</h1>
            <table>
                <tr>
                    <th style="color: #FFF">Answer</th>
                    <th style="color: #FFF">Count</th>
                </tr>
                <tr v-for="obj in values">
                    <td style="color: #FFF">{{ obj.value }}</td>
                    <td style="color: #FFF">{{ obj.count }}</td>
                </tr>
            </table>
        </div>
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
th {
    text-align: left;
    text-decoration: underline;
}
table {
    margin: auto;
    width: 90%
}
.qb {
    background-color: #3B3B3B;
    padding: 10px;
    margin: 15px;
    margin-left: auto;
    margin-right:auto;
    border-radius: 5px;
    width: 600px
}
.qb h1, .qb li, .nores {
    color: #FFF
}
.qb h1, .nores {
    margin: 0;
    margin-bottom: 5px;
}
dialog::backdrop {
    backdrop-filter: blur(2px);
}
</style>

<script setup>
import { onMounted, ref } from 'vue';
import { validate_yaml } from "/src/poll_loader.js"
import home_img from './../assets/home.svg?url';
import edit_img from './../assets/edit.svg?url';
import poll_img from './../assets/poll.svg?url';
const dlg_col = ref("#FFF")
const dlg_text = ref("Sample text");
const dlg = ref(null);
const responses = ref({});
const data = JSON.parse(document.getElementById("server-data").innerText)
const poll_id = data.id;
var mounted = false;
onMounted(() => mounted = true);
const yaml = validate_yaml(data.yaml).yaml;
for(const blk of yaml.poll) {
    const question_var = Object.keys(blk)[0];
    const question = blk[question_var];
    switch(question.type) {
        case "CHOICE": {
            if(data.responses[question_var] == null)
                data.responses[question_var] = {}
            for(const choice of question.choices) {
                const choice_var = Object.keys(choice)[0];
                if(data.responses[question_var][choice_var] == null)
                    data.responses[question_var][choice_var] = {
                        "value": choice_var,
                        "count": 0
                    };
            }
            break;
        }
        case "SHORT": {
            if(data.responses[question_var] == null)
                data.responses[question_var] = {};
            break;
        }
    }
}
responses.value = data.responses;

function view_poll() {
    document.location.href = window.location.protocol + "//" + window.location.host + "/poll/" + poll_id;
}

function edit_poll() {
    document.location.href = window.location.protocol + "//" + window.location.host + "/create/" + poll_id;
}
// responses.value = {
//     "1": [
//         {"value": "a", "count": 1},
//     ],
//     name: [
//         {"value": "", "count": 2},
//         {"value": "dwadw", "count": 1},
//     ]
// }
</script>