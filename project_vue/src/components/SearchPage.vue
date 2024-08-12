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
    <div class="div-searchbar">
      <input 
        v-model="search" 
        placeholder="Search..." 
        class="input-search"
        @keyup.enter="performSearch" 
      >
      <button class="button-search" @click="performSearch">Search</button>
    </div>

    <!-- tab -->
    <div>
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
    <div v-if="selected_item !== ''" class="div-container">
      <div class="table-container">
        <!-- 급수 -->
        <table  class="table-급수">
          <tbody>
            <tr>
              <th>한국어문회급수</th>
              <td>{{ selected_item["한국어문회 읽기급수"] }} {{ selected_item["한국어문회 쓰기급수"] }}</td>
            </tr>
            <tr>
              <th>중국 통용규범한자표 급수</th>
              <td v-if="selected_item['통용규범한자표 등재'] === '등재'">{{ selected_item["통용규범한자표 급수"] }}급</td>
              <td v-else>-</td>
            </tr>
            <tr >
              <th> 일본 상용한자</th>
              <td v-if="selected_item['상용한자 등재'] === '상용한자'">등재</td>
              <td v-else-if="selected_item['상용한자 등재'] === '표외한자'">표외한자 등재</td>
              <td v-else>미등재</td>
            </tr>
            <tr>
              <th>HSK 급수</th>
              <td v-if="selected_item['HSK 급수'] !== ''">{{ selected_item["HSK 급수"] }}급</td>
              <td v-else>-</td>
            </tr>
            <tr>
              <th>JLPT 급수</th>
              <td v-if="selected_item['JLPT 급수'] !== ''">{{ selected_item["JLPT 급수"] }}</td>
              <td v-else>-</td>
            </tr>
          </tbody>
        </table>
        <!-- 기본 -->
         <div class="div-기본">
          <h1 class="h1-한자">{{ selected_item.한자 }}</h1>
          <h2 class="h2-훈음">{{ selected_item.훈음 }}</h2>
         </div>
          <!--소리-->
        <table  class="table-소리">
          <tbody>
            <tr>
              <th>한국음</th>
              <td>{{ selected_item.음}} </td>
            </tr>
            <tr>
              <th>사성음</th>
              <td>{{ selected_item["중국 사성음"] }}</td>
            </tr>
            <tr v-if="selected_item.訓 !== ''">
              <th>일본훈</th>
              <td>{{ selected_item.訓 }}</td>
            </tr>
            <tr v-if="selected_item['音(カタカナ)'] !== ''">
              <th>일본음</th>
              <td>{{ selected_item['音(カタカナ)'] }}</td>
            </tr>
          </tbody>
        </table>
    </div>
      <!-- 모양 정보 -->
      <div>
        {{selected_item.육서}} <br>
          총 {{selected_item.총획}}획 <br>
          부수: {{selected_item.부수}} <br>
          <span v-if="selected_item.성부===''">{{selected_item.성부}} <br> </span>
        설명 {{selected_item.설명}}
      </div>

      <!-- 예시 -->
      <div>
          <!-- Tabs -->
        <div class="tabs">
          <button :class="{ active: activeTab === '성어' }" @click="activeTab = '성어'">한자성어</button>
          <button :class="{ active: activeTab === 'HSK' }" @click="activeTab = 'HSK'">HSK</button>
          <button :class="{ active: activeTab === 'JLPT' }" @click="activeTab = 'JLPT'">JLPT</button>
        </div>
        <!-- <span v-if="selected_item['예'] !== ''">
          <br>
          <h3> 한국어 예시 </h3> 
          <ul>
            <li v-for="(item, index) in selected_item['예'].split('\n')" :key="index">{{ item }}</li>
          </ul>
        </span> -->

        <div v-if="selected_item['성어'] !== '' && activeTab === '성어'">
          <h3> 한국어문회 성어 </h3>
          <tr v-for="(row, rowIndex) in selected_item['성어'].split('\n')" :key="rowIndex">
            <td v-for="(item, colIndex) in parseProverb(row)" :key="colIndex">{{ item }}</td>
          </tr>
        </div>

        <div v-if="selected_item['HSK 급수'] !== '' && activeTab === 'HSK' ">
          <h3>HSK 단어 </h3> 
          <tr v-for="(row, rowIndex) in selected_item['HSK 단어'].split('\n')" :key="rowIndex">
            <td v-for="(item, colIndex) in parseHSK(row)" :key="colIndex">{{ item }}</td>
          </tr>
        </div>
        <div v-if="selected_item['JLPT 급수'] !== '' && activeTab === 'JLPT'">
          <h3>JLPT 단어</h3>
          <tr v-for="(row, rowIndex) in selected_item['JLPT 단어'].split('\n')" :key="rowIndex">
          <td v-for="(item, colIndex) in parseJLPT(row)" :key="colIndex">{{ item }}</td>
          </tr>
        </div>
      </div>
      
    </div>

    <!-- Search Result -->
    <div v-if="searched_item !== '' && selected_item == '' " class="div-container">
        <div>검색결과</div>
        <div> 
          <span v-if="selected_item !== ''"> {{selected_item.한자}}</span>
          <span v-if="selected_string !== ''"> {{selected_string}} does not exist </span>
        </div>
        <ul v-if=!selected_item class="ul-five">
          <li
            v-for="element in filteredData"
            :key="element.id"
            @click="showPanel(element)"
          >
            <span class="span-level">{{ element["한국어문회 읽기급수"] }} {{element["한국어문회 쓰기급수"]}}</span>
            <span class="span-word" >{{ element.한자 }}</span>
            <span class="span-meaning-sound">{{ element.훈음 }}</span>
          </li>
        </ul> 
      </div>

    <div v-if="searched_item !== '' && RelatedData !=null" class="div-container">
      <!-- Related Words -->
      <a1>관련 한자</a1>
      <ul class="ul-five">
        <li
          v-for="element in RelatedData"
          :key="element.한자"
          @click="showPanel(element)"
        >
          <span class="span-level">{{ element["한국어문회 읽기급수"] }} {{element["한국어문회 쓰기급수"]}}</span>
          <span class="span-word">{{ element.한자 }}</span>
          <span class="span-meaning-sound">{{ element.훈음}}</span>
        </li>
      </ul>
      <!-- Show a message if no results are found -->
      
    </div>
    
    <!-- Popup Panel -->
    <div v-if="clicked_item" class="div-popup-panel">
      <p class="div-popup-level">{{clicked_item["한국어문회 읽기급수"]}} {{clicked_item["한국어문회 쓰기급수"]}}</p>
      <button class="button-close" @click="closePanel">&times;</button>
      <div class="div-panel-component-meaning">
        <p class="p-label">부수<br></p>
        <p class="p-letter" @click="StringHandler(clicked_item.부수)">{{ clicked_item.부수}}</p>
      </div>
      <div class="div-panel-component-sound" >
        <p class="p-label" v-if="clicked_item.성부">성부<br></p>
        <p class="p-letter" @click="StringHandler(clicked_item.성부)">{{ clicked_item.성부}}</p>
      </div>
      <div class="div-panel-component-word">
        <h1 @click="SelectClose(clicked_item)" class="h1-word">{{ clicked_item.한자 }}</h1>
      </div>
      <div class="div-panel-component-explanation">
        <h5 class="h5-context">{{clicked_item.육서}} <br>{{ clicked_item.설명}}</h5>
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
      searched_item: '',
      selected_item: '',
      selected_string: '',
      clicked_item: '',
      activeFilter: '', // Default filter
      activeTab: '성어', // Default active tab
      filters: [
        { key: '한자', label: '한자' },
        { key: '훈음', label: '훈음' },
        { key: '음', label: '음' },
        { key: '성부', label: '성부' }
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
    parseProverb(input) {
      // Define the regex pattern for A(B): (C) D
      // No unnecessary escape characters for parentheses in this case
      const regex = /^([^(]+)\(([^)]+)\): \(([^)]+)\) (.+)$/;

      // Apply the regex to extract matches
      const match = input.match(regex);

      // Initialize an empty array to hold the results
      let items = [];

      // Check if the input matches the pattern
      if (match) {
        // Extract items from the match array
        items = [match[1].trim(), match[2].trim(), match[3].trim(), match[4].trim()];
      } else {
        // Handle the case where the input does not match the expected format
        console.error("Input does not match the expected format.");
      }

      return items;
    },

    parseHSK(input) {
      // Define the regex pattern
      const regex = /^([^(]+)\(([^)]+)\)\[([^\]]+)\]: \(([^)]+)\) (.+)$/;
      
      // Apply the regex to extract matches
      const match = input.match(regex);
      
      // Use 'let' instead of 'const' to allow reassignment
      let items = [];
      
      if (match) {
        // Extract items from the match array
        items = [match[1], match[2], match[3], match[4], match[5]];
      }
      
      return items;
    },

    
    parseJLPT(input) {
      // Define the regex pattern
      const regex = /^([^[]+)\[([^\]]+)\]: \(([^)]+)\) \(([^)]+)\) (.+)$/;
      
      // Apply the regex to extract matches
      const match = input.match(regex);
      
      // Use 'let' instead of 'const' to allow reassignment
      let items = [];
      
      if (match) {
        // Extract items from the match array
        items = [match[1], match[2], match[3], match[4], match[5]];
      }
      
      return items;
    },

    performSearch() {
      // Trigger your search logic here
      if (this.search.trim() !== '') {
        // Perform the search with the input value
        console.log('Searching for:', this.search);
        this.searched_item=this.search
        this.selected_item = '';
        this.selected_string = '';
        this.clicked_item = '';
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
      this.clicked_item = '';
    },
    SelectClose(input){
      this.SelectItem(input);
      this.closePanel();
    },
    setActiveFilter(key) {
      // Check if the filter is already active
      if (this.activeFilter === key) {
        // Remove the active filter if it is already active
        this.activeFilter = '';
      } else {
        // Set the filter as active
        this.activeFilter = key;
      }
    },
    StringHandler(input){

      if (input !== '' && input !==null) {
        this.selected_item  = this.allData.find(item => // finds the first element
              item.한자.toLowerCase().includes(input)
            ) || ''; //if the item does not exist, 
        this.searched_item = this.selected_item
        this.clicked_item = this.selected_item || '';

      }
      else {
        this.clicked_item = '';
        this.selected_item = '';
        this.selected_string=input;
      }
    }
  },
  computed: {
    ...mapGetters(['allData']),
    filteredData() {
      const searchTerm = this.searched_item.toLowerCase();

      switch (this.activeFilter) {
        case '한자':
          return this.allData.filter(item =>
            item.한자.toLowerCase().includes(searchTerm)
          ) || null;
        case '훈음':
          return this.allData.filter(item =>
            item.훈음.toLowerCase().includes(searchTerm)
          ) || null;
        case '음':
          return this.allData.filter(item =>
            item.음.toLowerCase().includes(searchTerm)
          ) || null;
        case '성부':
          return this.allData.filter(item =>
            item.성부.toLowerCase().includes(searchTerm)
          ) || null;
        default:
          return this.allData.filter(item =>
          item.한자.toLowerCase().includes(searchTerm)||item.음.toLowerCase().includes(searchTerm)||item.훈음.toLowerCase().includes(searchTerm)
        )  
      }
    },
    RelatedData() {
      const target = this.selected_item
      if (target !== '' && target.성부 !== '' ) {
          return this.allData.filter(item =>
            item.성부.toLowerCase().includes(target.성부)
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

@media (max-width: 768px) {
  .logo {
  height: 18vw; /* Responsive height relative to the viewport width */
  width: auto; /* Maintain aspect ratio */
  }
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


.input-search {
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

.input-search::placeholder {
  color: #999;
}

.input-search:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.input-search:focus::placeholder {
  color: #666;
}

.div-기본{
  width: 20%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.table-container {
  display: flex; /* Use Flexbox to align tables horizontally */
  gap: 20px; /* Add space between the tables */
}

/* Container for the table */
table {
  width: 30%;
  flex:1;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 13px;
  font-family: 'Arial', sans-serif;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden; /* Rounds the corners */
}

/* Table header styling */
th {
  width: 15%;
  background: linear-gradient(45deg, #1E90FF, #00BFFF); /* Gradient blue */
  color: white;
  font-size: 13px;
  text-align: left;
  padding: 12px 15px;
  font-weight: bold;
}

/* Table body styling */
td {
  width: 15%;
  font-size: 13px;
  padding: 12px 15px;
  border-bottom: 1px solid #ddd; /* Light border for separation */
}

/* Alternate row background color */
tbody tr:nth-child(even) {
  background-color: #f2f8fc; /* Light blue background for even rows */
}

/* First column (header) styling */
th:first-child {
  border-top-left-radius: 10px; /* Rounded corners */
}

th:last-child {
  border-top-right-radius: 10px; /* Rounded corners */
}

td:first-child {
  border-left: none; /* Removes the border on the first column */
}

td:last-child {
  border-right: none; /* Removes the border on the last column */
}

/* Last row styling */
tbody tr:last-child td {
  border-bottom: none; /* Removes the bottom border for the last row */
}

/* Responsive design */
@media (max-width: 600px) {
  table, th, td {
    font-size: 16px;
  }
}

/* Responsive design */
.tabs {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1rem;
  border-bottom: 2px solid #ccc;
}

.tabs button {
  background: none;
  border: none;
  padding: 1rem;
  cursor: pointer;
  font-size: 1.2rem;
  color: #333;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.tabs button:hover {
  color: #007bff;
}

.tabs button.active {
  color: #007bff;
  border-bottom: 3px solid #007bff;
}

h2, h3 {
  margin: 0.5rem 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

table td {
  border: 1px solid #ddd;
  padding: 8px;
}

table tr:nth-child(even) {
  background-color: #f9f9f9;
}

table tr:hover {
  background-color: #f1f1f1;
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

.button-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  color: #0056b3;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
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

.button-search {
  border-radius: 25px;
  margin-left: 10px; /* Space between input and button */
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 8px;
}

.button-search:hover {
  background-color: #0056b3;
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

.button-search:focus {
  outline: none;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.5);
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

.div-popup-panel {
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

.div-popup-panel::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0);
  z-index: -1;
}

@media (max-width: 768px) {
  .div-popup-panel {
    max-width: 400px; /* Adjust max-width to be 90% of the viewport width */
    width: 80%;    /* Allow width to auto adjust within the max-width */
    height: auto;   /* Allow height to auto adjust based on content */
  }
}

.div-panel-component-meaning {
  position: absolute;
  font-size: medium;
  top: 30%;
  left: 10%;
}

.div-panel-component-sound {
  position: absolute;
  font-size: medium;
  top: 30%;
  left: 80%;
  width: auto; /* Adjust based on content */
  height: auto; /* Adjust based on content */
  box-sizing: border-box; /* Ensure padding and borders are included in the width and height */
}

.div-panel-component-word{
  position:relative;
  top: 50%;
  left: 25%;
  width: 50%;
  height: 100%;
  font-size: medium
}

.div-panel-component-explanation{
  text-align: left
}

.div-searchbar {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px;
}

/* <p> */
.p-label{
  font-size: 12px
}
.p-letter{
  cursor: pointer;
  margin: auto;
  border-radius: 3px; /* Adjust the value to control the roundness */
  font-size: 25px;
  transition: background-color 0.3s, transform 0.3s;
}
.p-letter:hover{
  background-color: #f0f0f0;
  transform: translateY(-2px) scale(1.05) rotate(-1deg);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
}

/* <h1> */
.h1-word {
  background-color: #ffffff;
  padding: 10px;
  border-radius: 8px; /* Adjust the value to control the roundness */
  transition: background-color 0.3s, transform 0.3s;
  text-align: center;
  cursor: pointer;
  font-size: 50px;
  display: inline-block; /* Makes the width match the text size */
}

.h1-word:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px) scale(1.05) rotate(-1deg);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
}

.h1-한자{
  font-size: 70px;
  transition: background-color 0.3s, transform 0.3s;
  display: inline-block; /* Makes the width match the text size */
}

.h1-한자:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px) scale(1.05) rotate(-1deg);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
}

.h5-context{
  font-size: small;
}

/* <ul> */
.ul-single {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(5, 1fr); 
  gap: 10px; /* Space between grid items */
}

.ul-single li {
  grid-column: 3 / 4; /* Place item in the 3rd column */
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

/* <audio> */
  audio {
  margin-top: 10px;
}

.card-container {
  perspective: 1000px; /* Gives the card depth from the viewer's perspective */
}

.card {
  width: 300px;
  height: 200px;
  position: relative;
  transform-style: preserve-3d; /* Ensures child elements are rendered in 3D space */
  transition: transform 0.6s; /* Duration of the flip animation */
}

.card:hover {
  transform: rotateY(180deg); /* Flip the card on hover */
}

.card-front,
.card-back {
  width: 100%;
  height: 100%;
  position: absolute;
  backface-visibility: hidden; /* Hides the back side of the card when flipped */
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card-front {
  background-color: #007bff; /* Blue background for the front */
  color: white;
}

.card-back {
  background-color: #f1f1f1; /* Light gray background for the back */
  color: #333;
  transform: rotateY(180deg); /* Positions the back side initially */
}

</style>


