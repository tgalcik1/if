<template>
    <div class="character-dialogue-window" ref="characterDialogueWindow">
        <div class="header">
            <p style="color: gray">Conversation with <span style="color: white">{{ character }}</span></p>
            <button class="end-conversation-button" @click="endConversation">End Conversation</button>
        </div>

        <div class="messages-container">
            <div class="messages" v-for="(message, index) in messages" :key="index">
                <div class="player-message" v-if="message.type === 'player-message'">
                    <p>{{ message.visibleText }}</p>
                </div>
                <div class="dialogue-message" v-else>
                    <p>{{ message.visibleText }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CharacterDialogueWindow',
    props: {
        messages: {
            type: Array,
            default: () => [],
        },
        character: {
            type: String,
            default: '',
        }
    },
    data() {
        return {
            typingSpeed: 35,
            messageDelay: 500,
            isAnimating: false,
            isButtonHeldDown: false,
            scrollSmooth: true,
        };
    },
    methods:{
        endConversation(){
            if (window.api){
                window.api.send('toMain', { command: 'send-message', message: "[END]" });
            }
        },
        animateMessages() {
            const nextMessage = this.messages.find((msg) => !msg.visible);
        
            if (!nextMessage) {
                this.isAnimating = false;
                return;
            }
        
            this.isAnimating = true;
            nextMessage.visible = true;
            nextMessage.visibleText = '';
            let charIndex = 0;
            const revealCharacter = () => {
                nextMessage.visibleText += nextMessage.text[charIndex];
                charIndex++;
                this.scrollToBottom();
        
                if (charIndex < nextMessage.text.length) {
                    setTimeout(revealCharacter, this.typingSpeed);
                } else {
                    this.resetTypingSpeed();
                    setTimeout(() => {
                        this.animateMessages();
                    }, this.messageDelay);
                }
            };
        
            revealCharacter();
        },
        scrollToBottom() {
            this.$nextTick(() => {
                const container = this.$refs.characterDialogueWindow;
                if (container) {
                    container.scrollTo({
                        top: container.scrollHeight,
                        behavior: this.scrollSmooth ? 'smooth' : 'auto',
                    });
                }
            });
        },
        speedUpTyping() {
            this.typingSpeed = 3;
            this.scrollSmooth = false;
            this.isButtonHeldDown = true;
        },
        resetTypingSpeed() {
            this.typingSpeed = 35;
            this.scrollSmooth = true;
            this.isButtonHeldDown = false;
        },
    },
    watch: {
        messages: {
            handler() {
                if (!this.isAnimating) {
                    this.animateMessages();
                }
            },
            deep: true,
        },
    },
    mounted() {
        this.scrollToBottom();
    }
};
</script>


<style scoped>
.character-dialogue-window {
    position: fixed;
    top: 40px;
    left: 0;
    width: calc(100% - 300px);
    height: calc(100vh - 40px);
    z-index: 15;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(15px);
    display: flex;
    flex-direction: column;
}

.header {
    position: sticky;
    top: 0;
    z-index: 1;
    display: flex;
    justify-content: space-between;
    padding: 8px;
    padding-left: 16px;
    background-color: rgba(0, 0, 0, 0.0);
    backdrop-filter: blur(15px);
    border-bottom: 2px solid black;
}

.messages-container {
    flex: 1;
    overflow-y: auto;
}

.messages {
    width: 100%;
}

.messages:last-child {
    margin-bottom: 64px;
}

.messages-container::-webkit-scrollbar {
    width: 10px;
}

.messages-container::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0);
}

.messages-container::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.25);
    border-radius: 5px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
    background-color: rgba(255, 255, 255, 0.5);
}


.dialogue-message{
    align-self: flex-start;
    display: inline-block;
    margin-top: 8px;
    margin-left: 16px;
    margin-right: 50%;
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

.player-message{
    float: right;
    align-self: flex-end;
    margin-top: 8px;
    margin-right: 16px;
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

.end-conversation-button {
    height: 40px;
    margin-right: 8px;
}

</style>