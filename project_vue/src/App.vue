<template>
  <div id="app">
    <SearchPage />
    <router-view/>
  </div>
</template>

<script>

import SearchPage from './components/SearchPage.vue'
export default {
  name: 'App',
  components: {
    SearchPage
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

.heading {
  display: flex;
  align-items: center; /* Vertically center the image and text */
  justify-content: center; /* Center the text and image horizontally */
  font-size: 2em; /* Adjust the text size */
  color: #333; /* Text color */
}

.logo {
  height: 9vw; /* Responsive height relative to the viewport width */
  width: auto; /* Maintain aspect ratio */
  max-height: 1000px; /* Maximum height of the image */
  /*margin-right: 10px; /* Space between the image and the text */
}

/* Media Queries for Responsive Design */
@media (max-width: 768px) {
  .logo {
  height: 18vw; /* Responsive height relative to the viewport width */
  width: auto; /* Maintain aspect ratio */
  }

  button {
    font-size: 5vw;
    padding: 3vw 4vw;
  }

  .form-container {
    width: 30vw;
    height: 15vw;
    padding: 1vw;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  button {
    font-size: 2vw;
    padding: 0.5vw 2vw;
  }

  .form-container {
    width: 15vw;
    height: auto;
    padding: 1vw;
  }
}

@media (min-width: 1025px) {
  button {
    font-size: 1.7vw;
    padding: 0.4vw 2vw;
  }

  .form-container {
    width: 13vw;
    height: auto;
    padding: 1vw;
  }
}
</style>
