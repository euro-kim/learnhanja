<template>
  <div class="main-page">
    <h1 class="heading">
      <a :href="link" rel="noopener noreferrer">
        <img :src="logo" alt="Logo" class="logo" />
      </a>
    </h1>

    <form @submit.prevent="startTest" class="form-container">
      <button type="submit">시작하기</button>
    </form>
  </div>
</template>

<script>
import logo from '@/assets/file.png'; // Import the logo image file
export default {
  name: 'MainPage',
  data() {
    return {
      logo, // Set logo image as a data property
      link: 'http://learnhanja.com' // The URL to navigate to when the image is clicked
    };
  },
  methods: {
    startTest() {
      this.$router.push('/survey');
    }
  }
};
</script>

<style scoped>
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

.main-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

button {
  font-size: 2vw;
  padding: 1vw 2vw;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #3464d4;
}

.button-container {
  border-color: #66afe9;
  display: flex;
  justify-content: center;
  width: 100%; /* Maintain aspect ratio */
}

.form-container {
  justify-content: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin: 0 auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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



.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

input[type='text'] {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease;
}

input[type='text']:focus {
  border-color: #66afe9;
  outline: none;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 8px rgba(102, 175, 233, 0.6);
}
</style>
