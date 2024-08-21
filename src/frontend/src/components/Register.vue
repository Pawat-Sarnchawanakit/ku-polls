<template>
    <dialog ref="dlg">
        <div>
            <p style="color: #FFF">{{ msg }}</p>
        </div>
    </dialog>
    <div class="bg">
        <div class="box">
            <h1>Register</h1>
            <div style="display: flex;flex-direction: column;">
                <input ref="username" placeholder="Username" type="text"/>
                <input ref="password" placeholder="********" type="password"/>
            </div>
            <p class="noacc" >Already have an account? <a @click="$emit('swapauth')">Login Here</a></p>
            <button @click="register">Register</button>
        </div>
    </div>
</template>

<style scoped>
a {
    color: #50F;
    cursor: pointer;
}
button {
    cursor: pointer;
    color: #FFF;
    border: none;
    display: block;
    border-radius: 10px;
    background-color: #3E3E3E;
    padding: 10px;
    padding-left: 20px;
    padding-right: 20px;
    font-size: 16pt;
    margin: auto;
    margin-bottom: 10px;
    margin-top: 10px;
}
button:hover {
    background-color: #4E4E4E;
}
button:active {
    background-color: #5E5E5E;
}
.noacc {
    color: #FFF;
    margin: auto;
    text-align: center;
}
.bg {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.box {
    padding: 20px;
    border-radius: 10px;  
    margin: auto;
    margin: top;
    width: min(80%, 300px);
    background-color: #2E2E2E;
}
h1 {
    margin: auto;
    margin-bottom: 15px;
    text-align: center;
    color: #FFF;
    font-size: 32pt;
}
input {
    padding: 10px;
    margin: 5px;
    margin-left: auto;
    margin-right: auto;
    width: 80%;
    color: #FFF;
    font-size: 12pt;
    border-radius: 10px;
    border: none;
    background-color: #1E1E1E;
}
</style>

<script setup>
    import { ref } from "vue";
    const emit = defineEmits(["swapauth"])
    const dlg = ref(null);
    const msg = ref("");
    const username = ref(null);
    const password = ref(null);
    function register() {
        msg.value = "Logging in...";
        dlg.value.showModal();
        fetch(window.location.protocol + "//" + window.location.host + "/gyatt", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                f: "regis",
                u: username.value.value,
                p: password.value.value
            })
        }).then(res => res.text().then(new_msg => {
            if(new_msg == "ok") {
                window.location = window.location.protocol + "//" + window.location.host
                return;
            }
            msg.value = new_msg;
            dlg.value.showModal();
        })).catch(() => {
            msg.value = "Failed to register.";
            dlg.value.showModal();
        });
    }
</script>