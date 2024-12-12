<template>
  <div id="app">
    <transition
      name="fade"
      mode="out-in"
      appear
    >
      <router-view />
    </transition>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
@font-face {
  font-family: "dogicapixel";
  src: url('~@/static/dogicapixel.ttf');
}

@font-face {
  font-family: "cthulu";
  src: url('~@/static/cthulu.ttf');
}

body, input, button, textarea {
  font-family: "dogicapixel";
  font-weight: 500;
  font-style: normal;
  font-size: 12px;
  font-stretch: condensed;
}

body{
  background-color: black;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 3s, background-color 3s;
  background-color: black;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  background-color: black;
}
</style>
