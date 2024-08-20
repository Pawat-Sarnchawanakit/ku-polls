<template>
    <div class="holder">
        <h1 class="title">KU Polls</h1>
        <div class="header">
            <button class="header-btn" @click="redirect('Create poll', 'create', 'create')">Create a poll</button>
        </div>
        <div class="grid">
            <div v-for="itm in list" :style="{ 'background-image': 'url(' + itm.image + ')' }" @click="redirect('Poll: ' + itm.name, 'poll/' + itm.id, 'poll')" class="grid-itm">
                <h3>{{ itm.name }}</h3>
            </div>
        </div>
    </div>
</template>


<style scoped>
.grid-itm > h3 {
    user-select: none;
    background-color: rgba(0,0,0,0.5);
    color: #FFF;
    margin: auto;
    margin-top: 5px;
    text-align: center;
    font-weight: bold;
}
.grid-itm {
    cursor: pointer;
    margin: 10px;
    border-radius: 10px;
    width: 150px;
    height: 150px;
    background-color: #1E1E1E;
    background-size: cover;
}
.holder {
    height: 100%;
    display: flex;
    flex-direction: column;
}
.grid {
    border-radius: 20px;
    margin: auto;
    width: 90%;
    margin-bottom: 20px;
    background-color: #2E2E2E;
    display: grid;
    flex: 1 1 auto;
    overflow: auto;
    grid-template: repeat(6, 1fr) / repeat(7, 1fr);
}
.logo {
    margin: auto;
    display: block;
    width: 200px;
}
.title {
    font-size: 64pt;
}
h1, h2, p {
    margin: auto;
    text-align: center;
    color: #FFF;
}
.header-btn {
    color: #FFF;
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    background-color: #2E2E2E;
    border: none;
    border-radius: 10px;
    margin: 10px;
    padding: 10px;
}
.header-btn:hover {
    background-color: #3E3E3E;
}
.header-btn:active {
    background-color: #4E4E4E;
}
.header {
    display: flex;
    justify-content: space-evenly;
}
</style>

<script setup>
    import { ref } from 'vue';
    const list = ref([]);
    const emit = defineEmits(['change_page']);
    function redirect(title, link, name) {
        window.history.replaceState({}, title, link);
        emit('change_page', name);
    }
    fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            f: "list"
        })
    }).then(res => res.json().then(new_list => {
        list.value = new_list;
    }));
</script>