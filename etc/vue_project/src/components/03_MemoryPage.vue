<template>
  <div class="memory-page">
    <h1>외워봐요!</h1>

    <!-- Display a loading statement or spinner while data is being fetched -->
    <div v-if="loading" class="loading">
      <p>서버 연결 중입니다. 잠시만 기다려주세요...</p>
      <!-- Optionally add a spinner or any loading animation -->
      <div class="spinner"></div>
    </div>

    <!-- Display an error message if there is an error -->
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <!-- Display the list of questions only if data is loaded and there are questions -->
    <div v-if="!loading && sampled_Hanja.length" class="questions-container">
      <ul class="questions-list">
        <li
          v-for="element in sampled_Hanja"
          :key="element.id"
          class="question-item"
          @click="showPanel(element)"
        >
          <span class="question-word">{{ element.word }}</span>
          <span class="question-meaning-sound">{{ element.meaning_sound }}</span>
        </li>
      </ul>
    </div>

    <div v-if="!loading && sampled_Hanja.length" @submit.prevent="TakeTest" class="form-container">

        <button @click="TakeTest" sampling_type="submit">암기완료</button>


    </div>

    <form v-if="!loading && sampled_Hanja.length" @submit.prevent="TakeTest">
      <p style="font-size: smaller;">암기완료를 누르면 시험 페이지로 넘어갑니다.</p>
    </form>

    <!-- Popup Panel -->
    <div v-if="selected_Hanja" class="popup-panel">
      <p class="level-container">{{selected_Hanja.lev_read}} {{ selected_Hanja.lev_write}}</p>
      <button class="close-btn" @click="closePanel">&times;</button>
      <div class="component_meaning-container">
        <p>{{ selected_Hanja.component_meaning}}</p>
      </div>
      <div class="component_sound-container">
        <p>{{ selected_Hanja.component_sound}}</p>
      </div>
      <h1>{{ selected_Hanja.word }}</h1>
      <p>{{ selected_Hanja.meaning_sound}}</p>
      <!--<audio :src="selected_Hanja.sound" controls></audio> -->
    </div>

    <div v-if="elapsedTime" class="elapsed-time">
      <p>Time taken: {{ elapsedTime }} seconds</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import config from '../config.js'

export default {
  name: 'TestPage',
  data() {
    return {
      // Data from the previous page
      name: this.$route.query.name,
      survey_answers: {
        survey_answer0: this.$route.query.phone,
        survey_answer1: this.$route.query.know_hanja,
        survey_answer2: this.$route.query.know_component,
      },
      // New data from this page
      sampled_Hanja: [],
      sampling_type: null,
      sampled_Hanja_words:[],

      // Variables local to this page
      jsonData: [],
      count_retry:0,
      max_retry:2,
      selected_Hanja: null, // Track the selected question for the pop-up panel
      
      //loading screen
      errorMessage: null, // Error message
      loading: true, // Loading state
      
      // Add timing variables
      startTime: null,
      endTime: null,
      elapsedTime: null, // Add a property to hold the elapsed time
    };
  },
  created() {
    this.fetch_Hanja();
  },
  methods: {
    async fetch_Hanja() {
      try {
        // Make the API call
        const response = await axios.get(config.API.HANJA, {
          headers: {
            'Accept': 'application/json',
            'Content-type': 'application/json'
          },
          timeout: 10000  // Set a long timeout for slow requests
        });

        // Check if the response status is 200 OK
        if (response.status === 200) {
          this.jsonData = response.data;
          this.processData();
          this.count_retry=0
        } else {
          console.error('Unexpected status code:', response.status);  // Log unexpected status codes
          this.retryRequest();
        }
      } catch (error) {
        if (error.response) {
          console.error('Response error:', {
            status: error.response.status,
            data: error.response.data,
            headers: error.response.headers
          });
        } else if (error.request) {
          console.error('Request error:', {
            request: error.request
          });
        } else {
          console.error('Error:', {
            message: error.message
          });
        }
        this.retryRequest();
      }
    },
    retryRequest(){
      if (this.count_retry<this.max_retry){
        this.count_retry++;
        console.log(`retrying request ${this.count_retry}`);
        this.fetch_Hanja();
      }
      else{console.error(`Max request retry number reached`)}
    },
    processData() {
      this.sampled_Hanja = []; // Clear previously selected data
      this.sampling_type = Math.floor(Math.random() * 3); // Generate a random integer 0, 1, or 2

      if (this.sampling_type === 0) {
        this.selectRandomRows();
      } else if (this.sampling_type === 1) {
        this.selectByComponentMeaning();
      } else if (this.sampling_type === 2) {
        this.selectByOrigin();
      }
      this.sampled_Hanja_words = this.sampled_Hanja.map(element => element.word);
      this.loading=false;
      this.startTime = new Date(); // Capture the start time
    },
    selectRandomRows() {
      const shuffled = this.jsonData.sort(() => 0.5 - Math.random());
      this.sampled_Hanja = shuffled.slice(0, 5);
    },
    selectByComponentMeaning() {
      let rows = [];
      let meanings = [...new Set(this.jsonData.map(item => item.component_meaning))];

      while (rows.length < 5 && meanings.length > 0) {
        const randomMeaning = meanings.splice(Math.floor(Math.random() * meanings.length), 1)[0];
        const matchingRows = this.jsonData.filter(item => item.component_meaning === randomMeaning);
        rows = rows.concat(matchingRows.slice(0, 5 - rows.length));
      }

      this.sampled_Hanja = rows.slice(0, 5);
    },
    selectByOrigin() {
      let rows = [];
      let origins = [...new Set(this.jsonData.map(item => item.origin))];

      while (rows.length < 5 && origins.length > 0) {
        const randomOrigin = origins.splice(Math.floor(Math.random() * origins.length), 1)[0];
        const matchingRows = this.jsonData.filter(item => item.origin === randomOrigin);
        rows = rows.concat(matchingRows.slice(0, 5 - rows.length));
      }

      this.sampled_Hanja = rows.slice(0, 5);
    },

    TakeTest() {
      this.endTime = new Date(); // Capture the end time
      const elapsedTime = this.endTime - this.startTime; // Calculate the elapsed time in milliseconds
      this.elapsedTime = (elapsedTime / 1000).toFixed(2); // Convert to seconds

      // Log the elapsed time for debugging
      console.log(`Time taken: ${this.elapsedTime} seconds`);
      // Proceed with the form submission
      this.$router.push({
        path: '/test',
        query: {
          name: this.name,
          survey_answer0: this.survey_answers.survey_answer0,
          survey_answer1: this.survey_answers.survey_answer1,
          survey_answer2: this.survey_answers.survey_answer2,
          sampled_Hanja_words: JSON.stringify(this.sampled_Hanja_words),
          sampling_type: this.sampling_type,
          elapsedTime: this.elapsedTime, // Pass the elapsed time
        },
      });
    },
    showPanel(question) {
      this.selected_Hanja = question;
    },
    closePanel() {
      this.selected_Hanja = null;
    },
  },
}
</script>

<style scoped>
.loading {
  text-align: center;
  font-size: 1.2em;
  color: #666;
}
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left: 4px solid #0056b3;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
  margin: 20px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.memory-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f5f5;
}

/* Error message */
.error {
  color: red;
  margin-bottom: 20px;
}

/* Container for the list */
.questions-container {
  max-width: 1000px; /* Adjust as needed */
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Style for the list */
.questions-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 5 columns */
  gap: 10px; /* Space between grid items */
}

/* Style for each list item */
.question-item {
  background-color: #ffffff;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, transform 0.3s;
  text-align: center;
  cursor: pointer;
}

.question-item:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
}

/* Style for the question word */
.question-word {
  font-size: 30px;
  display: block;
  font-weight: bold;
  color: #333;
}

/* Style for the question meaning and sound */
.question-meaning-sound {
  display: block;
  color: #666;
}

/* Style for the popup panel */
.popup-panel {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  max-width: 400px;
  width: 100%;
  animation: fadeIn 0.3s ease-in-out;
}

/* Popup panel animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translate(-50%, -40%);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
}

/* Close button */
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  color: #0056b3;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
}

/* Overlay background */
.popup-panel::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0);
  z-index: -1;
}

audio {
  margin-top: 10px;
}

/* Add a responsive design */
@media (max-width: 1200px) {
  .questions-list {
    grid-template-columns: repeat(4, 1fr); /* 4 columns for medium screens */
  }
}

@media (max-width: 900px) {
  .questions-list {
    grid-template-columns: repeat(3, 1fr); /* 3 columns for smaller screens */
  }
}

@media (max-width: 600px) {
  .questions-list {
    grid-template-columns: repeat(2, 1fr); /* 2 columns for very small screens */
  }
}

@media (max-width: 400px) {
  .questions-list {
    grid-template-columns: 1fr; /* 1 column for extra small screens */
  }
}

/* Style for the form */
.form-container {
  justify-content: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 150px;
  margin: 20px auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Style for the submit button */
button {
  margin-top: 10px;
  font-size: 18px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 5px;
}

button:hover {
  background-color: #3464d4;
  color:#ffffff
}

.component_meaning-container {
  position: absolute;
  top: 30%;
  left: 10%;
  font-size: medium;
}

.component_sound-container {
  position: absolute;
  top: 30%;
  left: 80%;
  font-size: medium
}
.level-container{
  font-size: 12px; /* Adjust the font size as needed */
}

/* Form fields */
input[sampling_type="text"] {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease;
}

input[sampling_type="text"]:focus {
  border-color: #66afe9;
  outline: none;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 8px rgba(102, 175, 233, 0.6);
}

/* Style for elapsed time */
.elapsed-time {
  margin-top: 20px;
  font-size: 16px;
  color: #333;
}
p{
  font-size: small;
  color: #333
}
</style>