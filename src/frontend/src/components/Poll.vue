<template>
    <div style="background-color: transparent;height: 100%;overflow: auto;">
        <dialog ref="dlg" style="background-color: #2B2B2B;border: none; border-radius: 10px;"><h1 style="color: #FFF"> {{ dlg_text }}</h1><br/><p style="color: #FFF;margin: auto;text-align: center">Press ESC to close.</p></dialog>
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
    import { load_yaml } from "/src/poll_loader.js"
    var mounted = false;
    const dlg_text = ref("Please answer all questions.");
    const dlg = ref(false);
    const loaded = ref(false);
    const poll = ref(null);
    var poll_answers = [];
    function onYamlLoaded(body) {
        const data = load_yaml(body);
        if(!data.ok) {
            dlg_text = data;
            dlg.showModal();
            return;
        }
        poll.value.innerHTML = data.content;
        poll_answers = data.answers;
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
            n: document.location.pathname.split('/').filter((a) => a.length != 0)[1]
        })
    }).then(res => res.text().then((body) => {
        if(mounted)
            onYamlLoaded(body)
        else onMounted(() => onYamlLoaded(body));
    })).catch(() => {
        dlg_text.value = "Failed to load poll.";
        dlg.value.showModal();
    });
// onMounted(() => {
// onYamlLoaded(`
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
//         choices:
//             - a: "The engine of a film."
//             - b: "The fine game of nil."
//             - c: "42"
//             - d: "The meaning of life is a subjective concept that varies from person to person, often encompassing themes of purpose, fulfillment, and personal growth."
// `);
// });
    function submit() {
        let answers = {}
        for(let i = 0;i < poll_answers.length;++i) {
            const answer = poll_answers[i];
            switch(answer.type) {
                case "SHORT":
                    answers[answer.name] = document.getElementById("pi_" + answer.name).value;
                    break;
                case "CHOICE":
                    const div = document.getElementById("pi_" + answer.name);
                    const choice = div.querySelector("input:checked");
                    if(choice == null) {
                        dlg_text.value = "Please answer all questions."
                        dlg.value.showModal();
                        return;
                    }
                    answers[answer.name] = choice ? choice.getAttribute("choice") : null;
                    break;
            }
        }
        dlg_text.value = "Please wait, submitting..."
        dlg.value.showModal();
        fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                f: "submit",
                n: document.location.pathname.split('/').filter((a) => a.length != 0)[1],
                r: answers
            })
        }).then(res => res.text().then((body) => {
            dlg_text.value = (body == "ok") ? "Your response has been recorded." : body;
            dlg.value.showModal();
        })).catch(() => {
            dlg_text.value = "Failed to submit response.";
            dlg.value.showModal();
        });
    }
</script>