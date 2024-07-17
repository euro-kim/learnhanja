<template>
  <div class="test-page">
    <!-- Display a loading statement if jsonData is empty -->
    <div v-if="jsonData.length === 0" class="loading">
      <p>서버 연결 중입니다. 잠시만 기다려주세요...</p>
          <!-- Optionally add a spinner or any loading animation -->
      <div class="spinner"></div>
    </div>

    <!-- Show the form only when data is loaded and there are questions -->
    <div v-else-if="currentQuestionIndex < jsonData.length">
      <form @submit.prevent="nextQuestion"> <!-- Prevent form submission -->
        <h3>Q{{ currentQuestionIndex + 1 }}: {{ value }}</h3>
        <div>
          <h1>{{ jsonData[currentQuestionIndex].question }}</h1>
        </div>
        <ul>
          <li v-for="(choice, index) in jsonData[currentQuestionIndex].choices" :key="index">
            <div class="question-container">
              <input type="radio" :id="'choice' + index" :value="index" v-model="user_selections[currentQuestionIndex]" />
              <label :for="'choice' + index">{{ choice }} </label>
            </div>
          </li>
        </ul>
        <div class="button-container">
          <button type="submit" :disabled="user_selections[currentQuestionIndex] === null">
            {{ currentQuestionIndex === jsonData.length - 1 ? '완료' : '다음' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Display the final results after all questions are answered -->
    <div v-else class="final-container">
      <h2>참여해주셔서 감사합니다!</h2>
      <p>정답표</p>
      <div class="result-container">
        <div v-for="(answer, index) in user_answers" :key="index" class="result-row">
          <div 
            class="question-column" 
            :style="{ color: answer + 1 === jsonData[index].answer + 1 ? 'green' : 'red' }">
            Q{{ index + 1 }}: {{ jsonData[index].question }}
          </div>
          <div class="answer-column">
            {{ answer + 1 }}번 선택
          </div>
          <div class="correct-answer-column">
            {{ jsonData[index].answer + 1 }}번
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import config from '../config.js';

export default {
  data() {
    const parsed_sampled_Hanja_words = this.$route.query.sampled_Hanja_words ? JSON.parse(this.$route.query.sampled_Hanja_words) : [];
    return {
      sampled_Hanja_words: parsed_sampled_Hanja_words,
      sampling_type: this.$route.query.sampling_type,
      name: this.$route.query.name,
      survey_answers: {
        survey_answer0: this.$route.query.survey_answer0,
        survey_answer1: this.$route.query.survey_answer1,
        survey_answer2: this.$route.query.survey_answer2,
      },
      elapsedTime: parseInt(this.$route.query.elapsedTime, 10) || 0,
      jsonData: [], // Response from WebFramework
      currentQuestionIndex: 0, // Marks the current question
      user_selections: [],  // Deals with user's current selections
      user_answers: [],  // User selected answers
      actual_answers: [], // Actual answers
      results: [] // 0 false 1 true
    };
  },
  mounted() {
    this.fetch_Question();  // Fetch data when the component is mounted
  },
  computed: {
    value() {
      return this.currentQuestionIndex + 1 > 5 ? '음을 골라주세요' : '뜻을 골라주세요';
    },
  },
  methods: {
    compareAnswers() {
      // Create an empty result array
      // Get the length of the shorter of the two arrays
      const length = Math.min(this.user_answers.length, this.actual_answers.length);

      // Loop through the arrays up to the length of the shorter one
      for (let i = 0; i < length; i++) {
        // Compare the values at the same index
        if (this.user_answers[i] === this.actual_answers[i]) {
          this.results.push(1); // Same values
        } else {
          this.results.push(0); // Different values
        }
      }
    },
    async fetch_Question() {
      try {
        const response = await axios.get(config.API.QUESTION, {
          params: this.buildParams(this.sampled_Hanja_words),
          timeout: 10000
        });

        if (response.status === 200) {
          this.jsonData = response.data;
          this.actual_answers = this.jsonData.map(element => element.answer);
          this.user_selections = Array(this.jsonData.length).fill(null); // Initialize user_selections array based on the number of jsonData
          console.log('Hanja data:', this.jsonData);
        } else {
          console.error('Unexpected status code:', response.status);
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
      }
    },

    buildParams(user_selections) {
      const params = {};
      params[`word0`] = user_selections[0];
      params[`word1`] = user_selections[1];
      params[`word2`] = user_selections[2];
      params[`word3`] = user_selections[3];
      params[`word4`] = user_selections[4];
      return params;
    },

    async nextQuestion() {
      if (this.currentQuestionIndex < this.jsonData.length) {
        // Save the index of the selected answer for the current question
        if (this.user_selections[this.currentQuestionIndex] !== null) {
          this.user_answers.push(this.user_selections[this.currentQuestionIndex]); // Save the selected index

          // Move to the next question
          this.currentQuestionIndex++;

          // Clear the selected answer for the new question
          if (this.currentQuestionIndex < this.jsonData.length) {
            this.user_selections[this.currentQuestionIndex] = null;
          } else {
            this.compareAnswers();
            await this.submitResults();  // Ensure submitResults is awaited
          }
        } else {
          alert("정답을 선택해주세요!");
        }
      }
    },

    async submitResults() {
      try {

        // Log the data being sent to the server for debugging
        const dataToSend = {
          name: this.name,
          survey_answer0: this.survey_answers.survey_answer0,
          survey_answer1: this.survey_answers.survey_answer1,
          survey_answer2: this.survey_answers.survey_answer2,
          sampling_type: this.sampling_type,
          sampled_Hanja: JSON.stringify(this.sampled_Hanja_words),
          elapsedTime: this.elapsedTime,
          result: JSON.stringify(this.results)
        };

        console.log('Data to send:', dataToSend);  // Log data to send

        // Make the POST request to the Django backend
        const response = await axios.post(config.API.PERSON, dataToSend, {
          timeout: 10000
        });

        // Log the server response
        console.log('Server response:', response.data);

        // Handle the response
        if (response.status === 201) {
          console.log('User created successfully');

        } else {
          console.error('Unexpected response status:', response.status);
        }
      } catch (error) {
        // Log the error details for debugging
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
      }
    }
  }
};
</script>

<style scoped>
h1 {
  font-size: 50px;
  margin: 10px;
}

button {
  font-size: 18px;
  padding: 10px 20px;
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
  margin-top: 10px;
  display: flex;
  justify-content: center;
  width: 100%; /* Ensure the button container spans the full width */
  margin-bottom: 10px;
}

.test-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

label {
  margin-top: 0px;
  font-size: 20px;
}
.error {
  color: red;
}

/* form */
form {
  justify-content: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 7px;
  background-color: #f9f9f9;
  border: 3px solid #ddd;
  border-radius: 8px;
  width: 300px;
  margin: 0 auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-questions {
  display: flex;
  flex-direction: column;
  margin-bottom: 2px;
}

ul {
  align-self: flex-start;
}

li {
  list-style-type: none;
  align-self: flex-start;
  margin-left: 0px;
}
div {
  display: flex;
}
.div-contianer {
  margin-top: 0px;
  align-items: flex-start;
  margin-bottom: 0px;
}
.outerquestion-contianer {
  margin-top: 0px;
  margin-left: 0px;
  align-items: flex-start;
  margin-bottom: 0px;
}
.question-container {
  align-self: flex-start;
  margin-top: 10px;
  margin-bottom: 10px;
}
.final-container {
  flex-direction: column;
  align-items: center;
}
.result-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.result-row {
  display: contents;
}

.question-column, .answer-column, .correct-answer-column {
  padding: 10px;
  border: 1px solid #ccc;
}

.question-column {
  font-weight: bold;
}
.loading {
  flex-direction: column;
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
  animation:spin 1s linear infinite;
  margin: 20px auto;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
p{
  font-size: small;
  color: #333
}
</style>
