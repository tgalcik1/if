<template>
    <div class="dialogue-window" ref="dialogueWindow">
        <div class="messages" v-for="(message, index) in messages" :key="index">
            <div class="hr-with-text" v-if="message.type == 'header-message'">
                <span>{{message.text}}</span>
            </div>
            <div class="system-message" v-if="message.type == 'system-message'">
                <p>{{message.text}}</p>
            </div>
            <div class="player-message" v-if="message.type == 'player-message'">
                <p>{{message.text}}</p>
            </div>
            <div class="story-message" v-if="message.type == 'story-message'">
                <p>{{message.text}}</p>
            </div>
        </div>
    </div>
</template>

<script>


export default{
    name: 'DialogueWindow',
    data(){
        return {
            messages: [],
        }
    },
    methods: {
        addMessage(type, message){
            this.messages.push({type: type, text: message});
            this.scrollToBottom();
        },
        scrollToBottom(){
            this.$nextTick(() => {
                const container = this.$refs.dialogueWindow;
                if (container){
                    container.scrollTo({top: container.scrollHeight, behavior: "smooth"});
                }
            });
        },
    },
    mounted() {
        this.scrollToBottom();
        
        // get only message outputs from python game engine
        if (window.api && window.api.receive) {
            window.api.receive('fromMain', (data) => {
                this.addMessage(data.type, data.message);
                console.log(data);
            });
        }
    }
}

</script>

<style scoped>
.dialogue-window{
    display: flex;
    flex-direction: column;
    background: lightgray;
    position: absolute;
    left: 0;
    width: calc(100% - 300px);
    height: calc(100vh - 40px);
    overflow-y:scroll;
    
    /* via https://gist.github.com/dfrankland/f6fed3e3ccc42e3de482b324126f9542 */
    background-image:
      linear-gradient(45deg, #bbb 25%, transparent 25%), 
      linear-gradient(135deg, #bbb 25%, transparent 25%),
      linear-gradient(45deg, transparent 75%, #bbb 75%),
      linear-gradient(135deg, transparent 75%, #bbb 75%);
    background-size:25px 25px;
    background-position:0 0, 12.5px 0, 12.5px -12.5px, 0px 12.5px;
    animation: scroll-checkerboard 2s linear infinite;
}

@keyframes scroll-checkerboard {
    0% {
        background-position: 0 0, 12.5px 0, 12.5px -12.5px, 0px 12.5px;
    }
    100% {
        background-position: 25px 25px, 37.5px 25px, 37.5px 12.5px, 25px 37.5px;
    }
}

.dialogue-window::-webkit-scrollbar {
    width: 10px;
    margin-bottom: 100px;
}

.dialogue-window::-webkit-scrollbar-track {
    background: rgba(0,0,0,0);
    margin-bottom: 50px;
}

.dialogue-window::-webkit-scrollbar-thumb {
    background-color: rgba(0,0,0,0.25);
    border-radius: 5px;
    border: 2px solid #ccc;
}

.dialogue-window::-webkit-scrollbar-thumb:hover {
    background-color: rgba(0,0,0,0.5);
}

.story-message{
    align-self: flex-start;
    display: inline-block;
    margin-top: 8px;
    margin-left: 8px;
    margin-right: 8px;
    background-color: rgb(241, 221, 183);
    padding-left: 12px;
    padding-right: 12px;
    border: 2px solid black;
    overflow-wrap: break-word;
    word-break: break-word;
    word-wrap: break-word;
    line-height: 1.5;
    box-shadow: 4px 4px 1px rgba(0, 0, 0, 0.5);
}

.system-message{
    align-self: flex-start;
    display: inline-block;
    margin-top: 8px;
    margin-left: 8px;
    margin-right: 50%;
    background-color: white;
    padding-left: 12px;
    padding-right: 12px;
    border: 2px solid black;
    overflow-wrap: break-word;
    word-break: break-word;
    word-wrap: break-word;
    line-height: 1.5;
    box-shadow: 4px 4px 1px rgba(0, 0, 0, 0.5);
}

.player-message{
    float: right;
    align-self: flex-end;
    margin-top: 8px;
    margin-right: 8px;
    margin-left: 50%;
    background-color: lightblue;
    padding-left: 12px;
    padding-right: 12px;
    border: 2px solid black;
    overflow-wrap: break-word;
    word-break: break-word;
    word-wrap: break-word;
    line-height: 1.5;
    box-shadow: 4px 4px 1px rgba(0, 0, 0, 0.5);
}

.messages{
    width: 100%;
}

.messages:last-child{
    margin-bottom: 60px;
}

.hr-with-text {
    display: flex;
    align-items: center;
    margin-left: 8px;
    margin-right: 8px;
    margin-top: 32px;
    margin-bottom: 24px;
}

.hr-with-text::before,
.hr-with-text::after {
    content: '';
    flex: 1;
    border-top: 2px solid black;
}

.hr-with-text span {
    margin: 0 12px;
    color: black;
}

</style>