<template>
    <div class="holder">
        <h1 class="title">KU Polls</h1>
        <div class="header">
            <a href="/create/"><button class="header-btn">Create a poll</button></a>
        </div>
        <div class="grid">
            <a v-for="itm in list" :href="'/poll/' + itm.id">
                <div :style="{ 'background-image': 'url(' + itm.image + ')' }" class="grid-itm">
                    <h3>{{ itm.name }} {{ itm.open ? "(Open)" : "(Closed)" }}</h3>
                </div>
            </a>
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
    list.value = JSON.parse(document.getElementById("server-data").innerText)
</script>