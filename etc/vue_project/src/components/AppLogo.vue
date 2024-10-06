<template>
  <div class="logo-container">
    <a :href="redirectUrl">
      <img :src="logoSrc" alt="Logo" class="logo"/>
    </a>
  </div>
</template>

<script>
export default {
  name: 'AppLogo',
  props: {
    logoSrc: {
      type: String,
      required: true
    },
    redirectUrl: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.logo-container {
  position: relative;
  width: 0%;
  top: 0px; /* Adjust as needed */
  left: 0px; /* Adjust as needed */

}

.logo {
  height: 50px; /* Adjust as needed */
  width: auto;
}
</style>
