<template>
    <div class="dialogue-container" @mousemove="handleMouseMove">
      <!-- Background Layers -->
      <div class="background-layers">
        <div class="layer" :style="layerStyle(0.01)" style="background-image: url('/backgrounds/sky/1.png')"></div>
        <div class="layer" :style="layerStyle(0.02)" style="background-image: url('/backgrounds/sky/2.png')"></div>
        <div class="layer" :style="layerStyle(0.03)" style="background-image: url('/backgrounds/sky/3.png')"></div>
        <div class="layer" :style="layerStyle(0.04)" style="background-image: url('/backgrounds/sky/4.png')"></div>
      </div>
  
      <div>
        <button 
          class="speed-up-typing-button"
          :class="{'pushed': isButtonHeldDown}"
          v-if="isAnimating"
          @mousedown="speedUpTyping" 
          @mouseup="resetTypingSpeed" 
          @mouseleave="resetTypingSpeed">
          ▶▶|
        </button>
        <div class="dialogue-window" ref="dialogueWindow">
          <div class="messages" v-for="(message, index) in visibleMessages" :key="index">
            <div class="hr-with-text" v-if="message.type == 'header-message'">
              <span>{{ message.visibleText }}</span>
            </div>
            <div class="system-message" v-if="message.type == 'system-message'">
              <p>{{ message.visibleText }}</p>
            </div>
            <div class="player-message" v-if="message.type == 'player-message'">
              <p>{{ message.visibleText }}</p>
            </div>
            <div class="story-message" v-if="message.type == 'story-message'">
              <p>{{ message.visibleText }}</p>
            </div>
          </div>
        </div>
        <div v-if="showCharacterDialogueWindow">
          <CharacterDialogueWindow :messages="characterMessages" :character="currentCharacterDialogue"/>
        </div>
      </div>
    </div>
  </template>
  

  <script>
  import CharacterDialogueWindow from './character-dialogue-window.vue';
  
  export default {
    name: 'DialogueWindow',
    components: {
      CharacterDialogueWindow,
    },
    data() {
        return {
            messages: [],
            characterMessages: [],
            showCharacterDialogueWindow: false,
            currentCharacterDialogue: '',
            typingSpeed: 35,
            messageDelay: 500,
            isAnimating: false,
            scrollSmooth: true,
            isButtonHeldDown: false,
            mouseX: 0,
            mouseY: 0,
            currentMouseX: 0,
            currentMouseY: 0,
            lerpSpeed: 0.01,
        };
    },
    computed: {
      visibleMessages() {
        return this.messages.filter((message) => message.visible);
      },
    },
    methods: {
      addMessage(type, text) {
        if (!this.showCharacterDialogueWindow) {
          const message = { type, text, visibleText: '', visible: false };
          this.messages.push(message);
  
          if (!this.isAnimating) {
            this.animateMessages();
          }
  
        } else {
          this.characterMessages.push({ type, text });
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
          const container = this.$refs.dialogueWindow;
          if (container) {
            container.scrollTo({
              top: container.scrollHeight,
              behavior: this.scrollSmooth ? 'auto' : 'auto',
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
      handleMouseMove(e) {
        this.mouseX = e.clientX;
        this.mouseY = e.clientY;
      },
      lerp(start, end, t) {
        return start + (end - start) * t;
      },
      updateLayerPositions() {
        this.currentMouseX = this.lerp(this.currentMouseX, this.mouseX, this.lerpSpeed);
        this.currentMouseY = this.lerp(this.currentMouseY, this.mouseY, this.lerpSpeed);
      },
      layerStyle(ratio) {
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        const translateX = (this.currentMouseX - centerX) * ratio;
        const translateY = (this.currentMouseY - centerY) * ratio;
        return {
            transform: `translate(${translateX}px, ${translateY}px)`,
        };
      },
    },
    mounted() {
        this.scrollToBottom();
        const updateLoop = () => {
            this.updateLayerPositions();
            requestAnimationFrame(updateLoop);
        };
        updateLoop();
      if (window.api && window.api.receive) {
        window.api.receive('fromMain', (data) => {
          if (['header-message', 'system-message', 'player-message', 'story-message'].includes(data.type)) {
            this.addMessage(data.type, data.message);
          }
          if (data.type === 'dialogue-window' && data.status === 'initiate-dialogue') {
            this.showCharacterDialogueWindow = true;
            this.currentCharacterDialogue = data.character;
          }
          if (data.type === 'dialogue-window' && data.status === 'end-dialogue') {
            this.showCharacterDialogueWindow = false;
            this.characterMessages = [];
          }
          if (data.type === 'dialogue-message' && this.showCharacterDialogueWindow) {
            this.characterMessages.push({ type: 'dialogue-message', text: data.message });
          }
        });
      }
    },
  };
</script>
  

<style scoped>
.dialogue-container {
    position: relative;
    width: 100%;
    height: calc(100vh - 50px);
    overflow: hidden;
}
  
.background-layers {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
    image-rendering: pixelated;
    transform: scale(1.1);
}
  
.layer {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center;
}
  
.dialogue-window {
    display: flex;
    flex-direction: column;
    position: absolute;
    left: 0;
    width: calc(100% - 300px);
    height: calc(100vh - 40px);
    overflow-y: scroll;
    background-color: rgba(255,255,255,0.0);
    position: relative;
    z-index: 10;
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
  
.story-message {
    align-self: flex-start;
    display: inline-block;
    margin-top: 8px;
    margin-left: 16px;
    margin-right: 8px;
    background-color: rgb(241, 221, 183);
    padding-left: 12px;
    padding-right: 12px;
    border: 2px solid black;
    overflow-wrap: break-word;
    word-break: break-word;
    line-height: 1.5;
    box-shadow: 4px 4px 1px rgba(0, 0, 0, 0.5);
}
  
.system-message {
    align-self: flex-start;
    display: inline-block;
    margin-top: 8px;
    margin-left: 16px;
    margin-right: 50%;
    background-color: white;
    padding-left: 12px;
    padding-right: 12px;
    border: 2px solid black;
    overflow-wrap: break-word;
    word-break: break-word;
    line-height: 1.5;
    box-shadow: 4px 4px 1px rgba(0, 0, 0, 0.5);
}
  
.player-message {
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
    line-height: 1.5;
    box-shadow: 4px 4px 1px rgba(0, 0, 0, 0.5);
}
  
.messages {
    width: 100%;
}

.messages:last-child {
    margin-bottom: 64px;
}

.hr-with-text {
    display: flex;
    align-items: center;
    margin-left: 16px;
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

.speed-up-typing-button {
    position: absolute;
    cursor: pointer;
    height: 40px;
    width: 58px;
    z-index: 18;
    border: 2px solid black;
    bottom: 6px;
    left: calc(100vw - 300px - 92px);
}

.speed-up-typing-button.pushed {
    transform: translateY(1px);
    box-shadow: inset 2px 2px 2px rgba(0,0,0,0.3);
    background-color: #bbb;
}
</style>
