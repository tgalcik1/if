<template>
    <div class="title" @mousemove="handleMouseMove">
        <div class="parallax-container">
            <div
            v-for="(layer, index) in layers"
            :key="index"
            :class="`parallax-layer layer-${index + 1}`"
            :style="getLayerStyle(index)"
            ></div>
        </div>
        <div class="content">
            <h1 style="font-family: cthulu; font-size: 72px; background-color: black; font-weight: 100; color: white; padding: 16px">Heir of the Profane</h1>
            <h3 style="font-size: 18px; color: white; font-weight: 100">An LLM-Based Text Adventure Game</h3>
            <button @click="this.$router.push('/game')">Start Game</button>
        </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      layers: [1, 2, 3, 4],
      mouseX: 0,
      mouseY: 0,
      lerpMouseX: 0,
      lerpMouseY: 0,
      idleX: 0,
      idleY: 0,
      idleAngle: 0,
      idleTimer: null,
      isIdle: true,
      animationFrame: null,
    };
  },
  methods: {
    handleMouseMove(event) {
      clearTimeout(this.idleTimer);

      const { clientX, clientY } = event;
      const { innerWidth, innerHeight } = window;

      this.mouseX = (clientX / innerWidth - 0.5) * 2;
      this.mouseY = (clientY / innerHeight - 0.5) * 2;

      this.isIdle = false;
      this.idleTimer = setTimeout(() => {
        this.isIdle = true;
      }, 2000);
    },
    animateLerp() {
      const lerpFactor = 0.01;

      if (this.isIdle) {
        this.idleAngle += 0.001;
        this.idleX = Math.cos(this.idleAngle) * 0.5;
        this.idleY = Math.sin(this.idleAngle) * 0.5;

        this.lerpMouseX += (this.idleX - this.lerpMouseX) * lerpFactor;
        this.lerpMouseY += (this.idleY - this.lerpMouseY) * lerpFactor;
      } else {
        this.lerpMouseX += (this.mouseX - this.lerpMouseX) * lerpFactor;
        this.lerpMouseY += (this.mouseY - this.lerpMouseY) * lerpFactor;
      }

      this.animationFrame = requestAnimationFrame(this.animateLerp);
    },
    getLayerStyle(index) {
      const intensity = (index + 1) * 15;
      const offsetX = this.lerpMouseX * intensity;
      const offsetY = this.lerpMouseY * intensity;

      return {
        transform: `translate(${offsetX}px, ${offsetY}px) scale(1.2)`,
        backgroundImage: `url(/backgrounds/title/${index + 1}.png)`,
        backgroundSize: '120%',
        backgroundPosition: 'center',
        imageRendering: 'pixelated',
      };
    },
  },
  mounted() {
    this.animateLerp();
  },
  beforeUnmount() {
    clearTimeout(this.idleTimer);
    cancelAnimationFrame(this.animationFrame);
  },
};
</script>

<style scoped>
.title {
  margin: -8px;
  height: 100vh;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background-color: lightgray;
}

.parallax-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.parallax-layer {
  position: absolute;
  width: 100%;
  height: 100%;
  will-change: transform;
}

.content {
  position: relative;
  z-index: 10;
}

button {
  height: 40px;
  margin-top: 16px;
}
</style>
