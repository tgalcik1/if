<template>
  <div id="app">
    <router-view></router-view>
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

body, input, button, textarea {
  font-family: "dogicapixel";
  font-weight: 500;
  font-style: normal;
  font-size: 12px;
  font-stretch: condensed;
}


</style>
