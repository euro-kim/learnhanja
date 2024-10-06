<template>
  <div class="manage-page">
    <h1 class="heading">manage</h1>

    <form class="form-container">
      <div class="button-container">
        <button @click.prevent="delete_Person()">Delete Most Recent Person</button>
      </div>
    </form>

    <form class="form-container">
      <div class="input-container">
        <input v-model="person_name" type="text" placeholder="Enter Person Name">
      </div>
      <div class="button-container">
        <button @click.prevent="delete_Person_ByName()">Delete Person By Name</button>
      </div>
    </form>

    <form class="form-container">
      <div class="input-container">
        <input v-model="person_id" type="number" placeholder="Enter Person ID">
      </div>
      <div class="button-container">
        <button @click.prevent="delete_Person_ByID()">Delete Person By ID</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import config from '../config'; // Ensure the config file is correctly imported

export default {
  name: 'ManagePage',
  data() {
    return {
      person_id: null,
      person_name: null,
      jsonData: [],
      count_retry: 0,
      max_retry: 2,
    };
  },
  methods: {
    async get_Person() {
      try {
        const response = await axios.get(config.API.HANJA, {
          headers: {
            'Accept': 'application/json',
            'Content-type': 'application/json'
          },
          timeout: 10000  // Set a long timeout for slow requests
        });

        if (response.status === 200) {
          this.jsonData = response.data;
          this.processData();
        } else {
          console.error('Unexpected status code:', response.status);  // Log unexpected status codes
          this.retryRequest();
        }
      } catch (error) {
        this.handleError(error);
        this.retryRequest();
      }
    },

    async delete_Person(identifier = null) {
      try {
        const requestData = identifier ? (typeof identifier === 'number' ? { id: identifier } : { name: identifier }) : {};

        const response = await axios.delete(config.API.PERSON, {
          headers: {
            'Accept': 'application/json',
            'Content-type': 'application/json'
          },
          data: requestData,
          timeout: 10000  // Set a long timeout for slow requests
        });

        if (response.status === 200) {
          alert(`Person deleted successfully`);
        } else {
          console.error('Unexpected status code:', response.status);  // Log unexpected status codes
          alert("Unexpected error: Person not deleted");
        }
      } catch (error) {
        this.handleError(error);
        alert('Error: Person not deleted');
      }
    },

    delete_Person_ByID() {
      this.delete_Person(this.person_id);
    },

    delete_Person_ByName() {
      this.delete_Person(this.person_name);
    },

    retryRequest() {
      if (this.count_retry < this.max_retry) {
        this.count_retry++;
        console.log(`Retrying request ${this.count_retry}`);
        this.get_Person();
      } else {
        console.error('Max request retry number reached');
      }
    },

    processData() {
      this.jsonData.map(element => element.word);
    },

    handleError(error) {
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

  created() {
    this.get_Person();
  }
}
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
  margin-right: 10px; /* Space between the image and the text */
}


  .main-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }
  button {
    margin-top: 0px;
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
    border-color: #66afe9;
    display: flex;
    justify-content: center;
    width: 100%; /* Ensure the button container spans the full width */
  }
  
  form {
    display: flex;
    flex-direction: column;
    align-items: center; /* Center the form contents */
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 300px;
  }
  
  .form-container {
  justify-content: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 300px;
  margin: 0 auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
  
  .form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
  }

  input {
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: border-color 0.3s ease;
  }
  input:focus {
    border-color: #66afe9;
    outline: none;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 8px rgba(102, 175, 233, 0.6);
  }
  </style>