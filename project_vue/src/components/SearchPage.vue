<template>
  <div>
    <input v-model="search" placeholder="Search..." class="search-input">
    <ul v-if="search.length > 0">
      <li v-for="item in SearchFilterData" :key="item.id">
        Word: {{ item.word }}
        Meaning: {{ item.meaning }}
        Sound: {{ item.sound }}
      </li>
      <ul class="questions-list">
        <li
          v-for="element in RelatedData"
          :key="element.id"
          class="question-item"
          @click="showPanel(element)"
        >
          <span class="question-word">{{ element.word }}</span>
          <span class="question-meaning-sound">{{ element.meaning_sound }}</span>
        </li>
      </ul>
      <!-- Show a message if no results are found -->
      <li v-if="SearchFilterData.length === 0">No results found</li>
    </ul>
    <!-- Show a placeholder message if no search term is entered -->
    <p v-else>Type something to start searching...</p>
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
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      search: '',
      selected_Hanja:''
    };
  },
  methods:{
    showPanel(input) {
      this.selected_Hanja = input;
    },
    closePanel() {
      this.selected_Hanja = null;
    },
  },
  computed: {
    ...mapGetters(['allData']),
    SearchFilterData() {
      const searchTerm = this.search.toLowerCase();
      return this.allData.filter(item =>
        item.word.toLowerCase().includes(searchTerm)
      );
    },
    RelatedData() {
      const target= this.SearchFilterData[0]||null;
      if (target) {
        return this.allData.filter(item =>
          item.origin.toLowerCase().includes(target.origin)
        );
      }
      return {}
    }
  }
};
</script>

<style scoped>
.search-container {
  display: flex;
  justify-content: center;
  margin: 20px;
}

.search-input {
  width: 100%;
  max-width: 600px;
  padding: 10px 20px;
  border: 1px solid #ccc;
  border-radius: 25px;
  font-size: 16px;
  color: #333;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: #999;
}

.search-input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.search-input:focus::placeholder {
  color: #666;
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
/* Style for the list */
.questions-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 5 columns */
  gap: 10px; /* Space between grid items */
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
</style>


