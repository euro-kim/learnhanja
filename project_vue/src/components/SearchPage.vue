<template>
  <div>
    <div :class="{'heading': true, 'folded-heading': search}">
      <a :href="link" rel="noopener noreferrer" class="logo-link">
        <img 
          alt="Vue logo" 
          src="../assets/logo.png" 
          :class="{'logo': true, 'folded': search}" 
        >
      </a>
    </div>

    <!-- Search Bar -->
    <div class="search-div-container">
      <input 
        v-model="search" 
        placeholder="Search..." 
        class="search-input"
        @keyup.enter="performSearch" 
      >
      <button class="search-button" @click="performSearch">Search</button>
    </div>

    <!-- tab -->
    <div class="tabs">
      <button
        v-for="filter in filters"
        :key="filter.key"
        class="button-filter"
        :class="{ active: activeFilter === filter.key }"
        @click="setActiveFilter(filter.key)"
      >
        {{ filter.label }}
      </button>
    </div>

    <!-- Selection -->
    <div v-if="selected_item!=null" class="div-container">
      <div>Selected Hanja</div>
       <ul class="ul-single">
           <li
             class="li-single"
             @click="showPanel(selected_item)"
           >
             <span class="span-word">{{ selected_item.word }}</span>
             <span class="span-meaning-sound">{{ selected_item.meaning_sound }}</span>
           </li>
           <button @click="clearSelection">Clear Selection</button>
       </ul>
    </div>

    <!-- Search Result -->
    <div v-if="search.length > 0" class="div-container">
        <div>Search Result</div>
        <div> 
          <span v-if="selected_item!=null"> {{selected_item.word}}</span>
          <span v-if="selected_string!=null"> {{selected_string}} does not exist </span>
        </div>
        <ul v-if=!selected_item class="ul-five">
          <li
            v-for="element in filteredData"
            :key="element.id"
            @click="showPanel(element)"
          >
            <span class="span-level">{{ element.lev_read }} {{element.lev_write}}</span>
            <span class="span-word">{{ element.word }}</span>
            <span class="span-meaning-sound">{{ element.meaning_sound }}</span>
          </li>
        </ul> 
      </div>

    <div v-if="search.length > 0 && RelatedData!=null" class="div-container">
      <!-- Related Words -->
      <a1>Related Words</a1>
      <div class="div-container">
        <ul class="ul-five">
          <li
            v-for="element in RelatedData"
            :key="element.id"
            @click="showPanel(element)"
          >
            <span class="span-word">{{ element.word }}</span>
            <span class="span-meaning-sound">{{ element.meaning_sound }}</span>
          </li>
        </ul>
      </div>
      <!-- Show a message if no results are found -->
      
    </div>
    
    <!-- Popup Panel -->
    <div v-if="clicked_item" class="popup-panel">
      <p class="level-div-container">{{clicked_item.lev_read}} {{ clicked_item.lev_write}}</p>
      <button class="close-btn" @click="closePanel">&times;</button>
      <div class="component_meaning-div-container">
        <p class="letter" @click="StringHandler(clicked_item.component_meaning)">{{ clicked_item.component_meaning}}</p>
      </div>
      <div class="component_sound-div-container" >
        <p class="p-label">성부<br></p>
        <p class="p-letter" @click="StringHandler(clicked_item.component_sound)">{{ clicked_item.component_sound}}</p>
      </div>
      <div class="word-div-container" @click="SelectClose(clicked_item)">
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
      selected_item:null,
      selected_string:null,
      clicked_item:null,
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
        this.clicked_item = null;
      }
    }
  },
  methods:{
    performSearch() {
      // Trigger your search logic here
      if (this.search.trim() !== '') {
        // Perform the search with the input value
        console.log('Searching for:', this.search);
        self.selected_item=null;
        self.selected_string=null;
        self.clicked_item=null;
        // You can replace the above line with your actual search logic
      } else {
        console.log('Search input is empty');
    }
    },
    SelectItem(input) {
      this.selected_item= input;
    },
    showPanel(input) {
      this.clicked_item = input;
    },
    closePanel() {
      this.clicked_item = null;
    },
    SelectClose(input){
      this.SelectItem(input);
      this.closePanel();
    },
    clearSelection() {
      this.selected_item = null;
      this.selected_string = null;
      this.search = ''; // Clear search input if needed
    },
    setActiveFilter(key) {
      // Check if the filter is already active
      if (this.activeFilter === key) {
        // Remove the active filter if it is already active
        this.activeFilter = null;
      } else {
        // Set the filter as active
        this.activeFilter = key;
      }
    },
    StringHandler(input){

      if (input != '' && input !=null) {
        this.selected_item  = this.allData.find(item => // finds the first element
              item.word.toLowerCase().includes(input)
            ) || null; //if the item does not exist, 
        this.clicked_item = this.selected_item || null;

      }
      else {
        this.clicked_item=null;
        this.selected_item=null;
        this.selected_string=input;
      }
    }
  },
  computed: {
    ...mapGetters(['allData']),
    filteredData() {
      const searchTerm = this.search.toLowerCase();

      switch (this.activeFilter) {
        case 'word':
          return this.allData.filter(item =>
            item.word.toLowerCase().includes(searchTerm)
          ) || null;
        case 'meaning':
          return this.allData.filter(item =>
            item.meaning.toLowerCase().includes(searchTerm)
          ) || null;
        case 'sound':
          return this.allData.filter(item =>
            item.sound.toLowerCase().includes(searchTerm)
          ) || null;
        case 'origin':
          return this.allData.filter(item =>
            item.origin.toLowerCase().includes(searchTerm)
          ) || null;
        default:
          return this.allData.filter(item =>
          item.word.toLowerCase().includes(searchTerm)||item.sound.toLowerCase().includes(searchTerm)||item.meaning.toLowerCase().includes(searchTerm)
        )  
      }
    },
    RelatedData() {
      const target = this.selected_item
      if (target!=null && target.component_sound!='') {
          return this.allData.filter(item =>
            item.component_sound.toLowerCase().includes(target.component_sound)
          );
        }
      else {
        return null;
      }
    }
  }
};
</script>

<style scoped>
.heading {
  display: flex; /* Flexbox to center the logo */
  align-items: center;
  justify-content: center;
  height: 200px; /* Initial height to accommodate the full-sized logo */
  transition: height 0.3s ease; /* Smooth transition for height */
  padding: 0; /* Remove any default padding */
  margin: 0; /* Remove any default margin */

}
/* Adjusted styles when the logo is folded */
.folded-heading {
  height: 10px; /* Reduced height when the logo is smaller */
}
/* Default styles for all <img> elements */
img {
  max-width: 100%; /* Ensures images scale properly within their div-containers */
  height: auto; /* Maintain aspect ratio */
  display: block; /* Removes any inline spacing */
  padding-bottom: 0;
  margin: 0; /* Remove any default margin */
}

/* Specific styles for the logo */
.logo {
  height: 9vw; /* Responsive height relative to the viewport width */
  width: auto; /* Maintain aspect ratio */
  max-height: 1000px; /* Maximum height of the image */
  /*margin-right: 10px; /* Space between the image and the text */
  transition: transform 0.3s ease, width 0.3s ease; /* Smooth transition when resizing */
}

/* Styles applied when the logo is folded (e.g., when search input is provided) */
.folded {
  transform: scale(0.3); /* Scale down the logo to 50% */
}

/* New styles for the <a> tag */
.logo-link {
  display: flex; /* Flexbox to ensure the link wraps around the content */
  align-items: center; /* Center vertically */
  justify-content: center; /* Center horizontally */
  height: 100%; /* Match height of the div-container */
  padding: 0; /* Remove default padding */
  margin: 0; /* Remove default margin */
  text-decoration: none; /* Remove underline from the link */
}


.search-div-container {
  display: flex;
  justify-content: center;
  align-items: center;
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


/* <div> */
.div-container {
  max-width: 1000px; /* Adjust as needed */
  margin: 13px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}


/* <li> */
li {
  background-color: #ffffff;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, transform 0.3s;
  text-align: center;
  cursor: pointer;
}

li:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
}
.li-single:hover{
  transform: translateY(0px);
}

/* <span> */
.span-level {
  font-size: 13px;
  display: block;
  font-weight:lighter;
  color: #333;
}

.span-word {
  font-size: 30px;
  display: block;
  font-weight: bold;
  color: #333;
}
.span-meaning-sound {
  display: block;
  color: #666;
}
/* <button> */
button {
  margin-top: 10px;
  font-size: 18px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 5px;
}

button:hover {
  background-color: #3464d4;
  color:#ffffff
}

.button-filter {
  padding: 7px 14px;
  background-color: transparent;
  color: #a0a0a0;
  font-size: 10px; 
}

.button-filter:hover {
  background-color:transparent;
}

.button-filter.active {
  color: #333; /* White text for active filter buttons */
}

.button-filter:hover:not(.disabled) {
  background-color: #f0f0f0; /* Example background color on hover */
}

button.search-button {
  border-radius: 25px;
  margin-left: 10px; /* Space between input and button */
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 8px;
}

button.search-button:hover {
  background-color: #0056b3;
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

button.search-button:focus {
  outline: none;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.5);
}


/* Style for the pop ups*/
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

.component_meaning-div-container {
  position: absolute;
  top: 30%;
  left: 10%;
  font-size: medium;
}


.component_sound-div-container {
  position: absolute;
  top: 30%;
  left: 80%;
  font-size: medium;
  width: auto; /* Adjust based on content */
  height: auto; /* Adjust based on content */
  box-sizing: border-box; /* Ensure padding and borders are included in the width and height */
}

.word-div-container {
  position:relative;
  top: 50%;
  left: 25%;
  width: 50%;
  height: 100%;
  font-size: medium
}
.p-label{
  font-size: 12px
}
.p-letter{
  cursor: pointer;
  margin: auto;
  transition: background-color 0.3s, transform 0.3s;
}
.p-letter:hover{
  background-color: #f0f0f0;
  transform: translateY(-2px);
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
.ul-single {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(1, 1fr); /* 5 columns */
  gap: 10px; /* Space between grid items */
}

.ul-five {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 5 columns */
  gap: 10px; /* Space between grid items */
}

/* Add a responsive design */
@media (max-width: 1200px) {
  .ul-five {
    grid-template-columns: repeat(4, 1fr); /* 4 columns for medium screens */
  }
}

@media (max-width: 900px) {
  .ul-five {
    grid-template-columns: repeat(3, 1fr); /* 3 columns for smaller screens */
  }
}

@media (max-width: 600px) {
  .ul-five {
    grid-template-columns: repeat(2, 1fr); /* 2 columns for very small screens */
  }
}

@media (max-width: 400px) {
  .ul-five {
    grid-template-columns: 1fr; /* 1 column for extra small screens */
  }
}

/* Style for the form */
.form-div-container {
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


