<template>
    <Login @swapauth="is_login = !is_login" v-if="is_login"/>
    <Register @swapauth="is_login = !is_login" v-if="!is_login"/>
</template>

<script setup>
    import { ref } from "vue";
    import Login from "./Login.vue";
    import Register from "./Register.vue";

    const is_login = ref(true);
</script>