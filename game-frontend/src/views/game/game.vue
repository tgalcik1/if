<template>
    <div class="game-container">
      <Navbar/>
      <Sidebar/>
      <DialogueWindow ref="dialogueWindow"/>
      <InputBar :showCharacterDialogueWindow="dialogueWindowState" @player-message="handlePlayerMessage"/>
      
    </div>
</template>
  
<script>
import Navbar from './components/navbar.vue';
import Sidebar from './components/sidebar.vue';
import DialogueWindow from './components/dialogue-window.vue';
import InputBar from './components/input-bar.vue';

export default {
  name: 'GameView',
  components:
  {
    Navbar,
    Sidebar,
    DialogueWindow,
    InputBar
  },
  data(){
    return {
      dialogueWindowState: false
    }
  },
  methods:{
    handlePlayerMessage(type, message){
      this.$refs.dialogueWindow.addMessage(type, message);
    },
    updateDialogueWindowState() {
      if (this.$refs.dialogueWindow) {
        this.dialogueWindowState = this.$refs.dialogueWindow.showCharacterDialogueWindow;
      }
    }
  },
  mounted() {
    window.api.send('toMain', { command: 'start-game' });
    this.updateDialogueWindowState();
  },
  beforeUnmount() {
    window.api.send('toMain', { command: 'end-game' });
  }
};
</script>

<style scoped>
</style>
  