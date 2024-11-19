<template>
    <div class="input-bar">
        <input v-model="message" @keyup.enter="sendMessage" style="width:100%">
        <button @click="sendMessage">Send</button>
    </div>
</template>

<script>

export default{
    name: 'InputBar',
    data(){
        return {
            message: ''
        }
    },
    methods: {
        sendMessage(){
            window.api.send('toMain', { command: 'send-message', message: this.message });

            this.message = "";
        }
    }
}

</script>

<style scoped>
.input-bar{
    margin-left: -8px;
    background-color: rgba(0, 0, 0, 0);
    position: absolute;
    bottom: 0;
    width: calc(100% - 300px - 16px);
    height: 40px;
    display: flex;
    justify-content: space-between;
    padding: 8px;
    filter: drop-shadow(0px 0px 4px rgba(0, 0, 0, 0.5));
}

</style>