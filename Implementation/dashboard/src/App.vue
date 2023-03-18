<script setup>
import ChartViews from "./views/ChartViews.vue";
</script>

<template>
  <ChartViews />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
<style>
.tooltip {
  position: absolute;
  display: flex;
  flex-direction: column;
  border: 1px solid #999;
  padding: 5px;
  background: white;
  border-radius: 5px;
}
.tooltip p {
  margin: 0;
}

.maker {
  display: inline-block;
  width: 12px;
  height: 12px;
  margin-right: 5px;
  border-radius: 50%;
}
</style>