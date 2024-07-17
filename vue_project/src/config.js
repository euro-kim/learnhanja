// src/config.js

const API_BASE_URL = 'http://api.learnhanja.com/api/';

const config = {
   API: {
     BASE_URL: API_BASE_URL,
     // Define different API endpoints here
     HANJA: `${API_BASE_URL}hanja/`,
     QUESTION: `${API_BASE_URL}question/`,
     PERSON: `${API_BASE_URL}person/`,
     ORDERS: `${API_BASE_URL}orders/`,
     // Add more API paths as needed
   }
};

export default config;
