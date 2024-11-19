<template>
    <div class="game-container">
      <Navbar/>
      <Sidebar/>
      <DialogueWindow/>
      <InputBar/>
      
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
  }
};
</script>

<style scoped>
</style>
  