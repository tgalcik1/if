<template>
    <div class="input-bar">
        <input v-model="message" @keyup.enter="sendMessage" style="width:100%">
        <button @click="sendMessage">Send</button>
    </div>
</template>

<script>

export default{
    name: 'InputBar',
    props: {
        showCharacterDialogueWindow: {
            type: Boolean,
            default: false,
        },
    },
    data(){
        return {
            message: ''
        }
    },
    methods: {
        sendMessage(){
            if (this.message)
            {
                // first send to the dialogue window component so it shows up
                this.$emit('player-message', 'player-message', this.message);

                // then send to the game engine
                window.api.send('toMain', { command: 'send-message', message: this.message });
                this.message = "";
            }
        }
    }
}

</script>

<style scoped>
.input-bar{
    margin-left: 0px;
    background-color: rgba(0, 0, 0, 0);
    position: absolute;
    bottom: 8px;
    width: calc(100% - 300px - 34px);
    height: 40px;
    display: flex;
    justify-content: space-between;
    padding: 8px;
    filter: drop-shadow(4px 4px 1px rgba(0, 0, 0, 0.5));
    z-index: 10;
}

input{
    border-top: 2px solid black;
    border-left: 2px solid black;
    border-bottom: 2px solid black;
}

button{
    margin-left: -2px;
    border-top: 2px solid black;
    border-right: 2px solid black;
    border-bottom: 2px solid black;
}

</style>