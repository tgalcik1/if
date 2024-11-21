<template>
    <div class="game-container">
      <Navbar/>
      <Sidebar/>
      <DialogueWindow ref="dialogueWindow"/>
      <InputBar @player-message="handlePlayerMessage"/>
      
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
  methods:{
    handlePlayerMessage(type, message){
      this.$refs.dialogueWindow.addMessage(type, message);
    }
  },
  mounted() {
    window.api.send('toMain', { command: 'start-game' });
  },
  beforeUnmount() {
    window.api.send('toMain', { command: 'end-game' });
  }
};
</script>

<style scoped>
</style>
  