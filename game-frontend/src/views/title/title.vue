<template>
    <div class="title">
        <h1 style="background-color: black; color: white; padding: 16px">Heir of the Profane</h1>
        <h3>An LLM-Based Text Adventure Game</h3>
        <button @click="this.$router.push('/game')">Start Game</button>
        <button>Exit Game</button>
    </div>
</template>

<style scoped>
.title {
    margin: -8px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background-color: lightgray;

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

button{
    height: 40px;
    margin-top: 16px;
}
</style>