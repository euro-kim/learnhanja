<template>
  <div id="app">
    <router-view/>
  </div>
</template>


<style>
html, body {
    overscroll-behavior: none; /* Prevents the bounce effect */
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

</style>
