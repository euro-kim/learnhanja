<template>
  <div>
    <input v-model="search" placeholder="Search..." class="search-input">
    <div class="tabs">
      <button
        v-for="filter in filters"
        :key="filter.key"
        :class="{ active: activeFilter === filter.key }"
        @click="setActiveFilter(filter.key)"
      >
        {{ filter.label }}
      </button>
    </div>

    <div v-if="search.length > 0" class="container">
       <!-- Search Result -->
        <div>Search Result</div>
        <ul v-if=!selected_item class="five-ul">
          <li
            v-for="element in SearchWordData"
            :key="element.id"
            class="general-li"
            @click="showPanel(element)"
          >
            <span class="question-word">{{ element.word }}</span>
            <span class="question-meaning-sound">{{ element.meaning_sound }}</span>
          </li>
        </ul>
        <!-- Selection -->
        <ul v-if="selected_item" class="single-ul">
            <li
              selected_item
              class="general-li"
              @click="SelectItem(selected_item)"
            >
              <span class="question-word">{{ selected_item.word }}</span>
              <span class="question-meaning-sound">{{ selected_item.meaning_sound }}</span>
            </li>
            <button @click="clearSelection">Clear Selection</button>
          </ul>
      </div>

    <ul v-if="search.length > 0 && selected_item !=''">
      <!-- Related Words -->
      <a1>Related Words</a1>
      <div class="container">
        <ul class="five-ul">
          <li
            v-for="element in RelatedData"
            :key="element.id"
            class="general-li"
            @click="showPanel(element)"
          >
            <span class="question-word">{{ element.word }}</span>
            <span class="question-meaning-sound">{{ element.meaning_sound }}</span>
          </li>
        </ul>
      </div>
      <!-- Show a message if no results are found -->
      <li v-if="SearchWordData.length === 0">No results found</li>
    </ul>
    
    <!-- Popup Panel -->
    <div v-if="clicked_item" class="popup-panel">
      <p class="level-container">{{clicked_item.lev_read}} {{ clicked_item.lev_write}}</p>
      <button class="close-btn" @click="closePanel">&times;</button>
      <div class="component_meaning-container" @click="SelectClose">
        <p>{{ clicked_item.component_meaning}}</p>
      </div>
      <div class="component_sound-container" @click="SelectClose">
        <p>{{ clicked_item.component_sound}}</p>
      </div>
      <div class="word-container" @click="SelectClose">
        <h1>{{ clicked_item.word }}</h1>
      </div>
      <!--<audio :src="clicked_item.sound" controls></audio> -->
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      search: '',
      selected_item:'',
      clicked_item:'',
      activeFilter: '', // Default filter
      filters: [
        { key: 'word', label: 'Word' },
        { key: 'meaning', label: 'Meaning' },
        { key: 'sound', label: 'Sound' },
        { key: 'origin', label: 'Origin' }
      ]
    };
  },
  watch: {
    search(newVal) {
      if (newVal.length === 0) {
        this.clicked_item = '';
      }
    }
  },
  methods:{
    SelectItem(input) {
      this.selected_item= input;
    },
    showPanel(input) {
      this.clicked_item = input;
    },
    closePanel() {
      this.clicked_item = null;
    },
    SelectClose(){
      this.SelectItem(this.clicked_item);
      this.closePanel();
    },
    clearSelection() {
      this.selected_item = null;
      this.search = ''; // Clear search input if needed
    },
    setActiveFilter(filterKey) {
      this.activeFilter = filterKey;
    }
  },
  computed: {
    ...mapGetters(['allData']),
    SearchWordData() {
      const searchTerm = this.search.toLowerCase();

      return this.allData.filter(item =>
        item.word.toLowerCase().includes(searchTerm)||item.sound.toLowerCase().includes(searchTerm)||item.meaning.toLowerCase().includes(searchTerm)
      )

    },
    SearchMeaningData() {
      const searchTerm = this.search.toLowerCase();
      return this.allData.filter(item =>
        item.meaning.toLowerCase().includes(searchTerm)
      )||null;
    },
    SearchSoundData() {
      const searchTerm = this.search.toLowerCase();
      return this.allData.filter(item =>
        item.sound.toLowerCase().includes(searchTerm)
      )||null;
    },
    SearchOriginData() {
      const searchTerm = this.search.toLowerCase();
      return this.allData.filter(item =>
        item.origin.toLowerCase().includes(searchTerm)
      )||null;
    },
    RelatedData() {
      const target= this.selected_item||null;
      if (target) {
        return this.allData.filter(item =>
          item.component_sound.toLowerCase().includes(target.component_sound)
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

/* Container for the list */
.container {
  max-width: 1000px; /* Adjust as needed */
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Style for each list item */
.general-li {
  background-color: #ffffff;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, transform 0.3s;
  text-align: center;
  cursor: pointer;
}

.general-li:hover {
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



/* Styke for the pop ups*/
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

.word-container {
  position:relative;
  top: 50%;
  left: 25%;
  width: 50%;
  height: 100%;
  font-size: medium
}
h1 {
  background-color: #ffffff;
  padding: 10px;
  border-radius: 5px;
  transition: background-color 0.3s, transform 0.3s;
  text-align: center;
  cursor: pointer;
}

h1:hover{
  background-color: #f0f0f0;
  transform: translateY(-2px);
}

/* Style for the list */
.single-ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(1, 1fr); /* 5 columns */
  gap: 10px; /* Space between grid items */
}

.five-ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 5 columns */
  gap: 10px; /* Space between grid items */
}

/* Add a responsive design */
@media (max-width: 1200px) {
  .five-ul {
    grid-template-columns: repeat(4, 1fr); /* 4 columns for medium screens */
  }
}

@media (max-width: 900px) {
  .five-ul {
    grid-template-columns: repeat(3, 1fr); /* 3 columns for smaller screens */
  }
}

@media (max-width: 600px) {
  .five-ul {
    grid-template-columns: repeat(2, 1fr); /* 2 columns for very small screens */
  }
}

@media (max-width: 400px) {
  .five-ul {
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


