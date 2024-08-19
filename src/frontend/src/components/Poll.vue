<template>
    <div ref="poll"></div>
</template>

<script setup>
    import { ref } from 'vue';
    import { load_yaml } from "/src/poll_loader.js"
    const poll = ref(null);
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
        const data = load_yaml(body);
        if(!data.ok)
            console.log(data)
        poll.value.innerHTML = data.content;
    }));
</script>