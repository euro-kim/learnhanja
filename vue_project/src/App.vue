<template>
  <div id="app">
    <AppLogo v-if="showLogo" :logoSrc="logoSrc" :redirectUrl="redirectUrl"/>
    <router-view/>
  </div>
</template>

<script>
import AppLogo from './components/AppLogo.vue';
export default {
  name: 'App',
  components: {
    AppLogo
  },
  data() {
    return {
      logoSrc: require('./assets/horozontal.png'), // Replace with your logo path
      redirectUrl: 'https://example.com' // Replace with your redirect URL
    }
  },
  computed: {
    showLogo() {
      // List the route names where the logo should be shown
      const routesWithLogo = []; 
      return routesWithLogo.includes(this.$route.name);
    }
  }
}
</script>

<style>

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
