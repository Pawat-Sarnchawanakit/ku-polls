<template>
    <div style="background-color: transparent;height: 100%;overflow: auto;">
        <dialog ref="dlg" style="background-color: #2B2B2B;border: none; border-radius: 10px;"><h1 :style="{ 'color': dlg_col }"> {{ dlg_text }}</h1><br/><p style="color: #FFF;margin: auto;text-align: center">Press ESC to close.</p></dialog>
        <div class="qb" v-for="(values, name) in responses">
            <h1>{{ name }}</h1>
            <ul> 
                <li v-for="obj in values">
                    <p style="color: #FFF">`{{ obj.value }}`: {{ obj.count }}</p>
                </li>
            </ul>
        </div>
    </div>
</template>

<style scoped>
.qb {
    background-color: #3B3B3B;
    padding: 10px;
    margin: 15px;
    margin-left: auto;
    margin-right:auto;
    border-radius: 5px;
    width: 600px
}
.qb h1, .qb li {
    color: #FFF
}
.qb h1 {
    margin: 0;
    margin-bottom: 5px;
}
dialog::backdrop {
    backdrop-filter: blur(2px);
}
</style>

<script setup>
import { ref } from 'vue';
const dlg_col = ref("#FFF")
const dlg_text = ref("Please answer all questions.");
const dlg = ref(false);
const responses = ref({});
const poll_id = document.location.pathname.split('/').filter((a) => a.length != 0)[1];
fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        f: "res",
        n: poll_id
    })
}).then(res => res.json().then((body) => {
    responses.value = body;
}));
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