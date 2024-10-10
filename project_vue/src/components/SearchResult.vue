<template>
    <div>

      <!-- Search Result -->
      <div v-if="searched_item !== '' && show_searchresult==true" class="div-container">

          <ul  class="ul-five">
            <li
            v-for="element in SortLogic"
            :key="element.id"
            @click="showPanel(element)"
            >
              <span v-if="checkbox_active.includes('급수')" class="span-level">{{ element["읽기"] }} {{element["쓰기"]}}</span>
              <span class="span-word" >{{ element.kr }}</span>
              <span v-if="checkbox_active.includes('훈음')" class="span-meaning-sound">{{ 훈음(element).join(', ') }}</span>
              <span v-if="checkbox_active.includes('중국음')" class="span-meaning-sound">{{ pinyin(element).join(', ') }}</span>
              <span v-if="checkbox_active.includes('일본음')" class="span-meaning-sound">{{ element.音読み.join(', ') }}</span>
              <span v-if="checkbox_active.includes('일본훈')" class="span-meaning-sound">{{ element.訓読み.join(', ') }}</span>
            </li>
          </ul> 
        </div>

        <!-- Popup Panel -->
        <div v-if="clicked_item" class="div-popup-panel">
          <p class="div-popup-level">{{clicked_item["읽기"]}} {{clicked_item["쓰기"]}}</p>
          <button class="button-close" @click="closePanel">&times;</button>
          <div class="div-panel-component-meaning">
            <p class="p-label">부수<br></p>
            <p class="p-letter" @click="StringHandler(clicked_item.部首)">{{ clicked_item.部首}}</p>
          </div>
          <div class="div-panel-component-sound" >
            <p class="p-label" v-if="clicked_item.聲部">성부<br></p>
            <p class="p-letter" @click="StringHandler(clicked_item.聲部)">{{ clicked_item.聲部}}</p>
          </div>
          <div class="div-panel-component-word">
            <h1 @click="SelectClose(clicked_item)" class="h1-word">{{ clicked_item.kr }}</h1>
          </div>
          <!--<audio :src="clicked_item.sound" controls></audio> -->
        </div>
    </div>
  </template>
  
  <script>
  import jsonData from '../data/hanja.json';
  
  export default {
    props:{
      searched_item:{
        type: String,
        required: true,
      },
      searchby_active:{
        type: Array,
        Required: true,
      },
      show_searchresult:{
        type: Boolean,
        Required: true,
      },
      show_searchinfo:{
        type: Boolean,
        Required: true,
      },
      sortby_active:{
        type: String,
        Required: true
      },
      filter_active_chinalev:{
        type: Array,
        Required: true
      },
      filter_active_readlev:{
        type: Array,
        Required: true
      },
      filter_active_writelev:{
        type: Array,
        Required: true
      },
      checkbox_active:{
        type: Array,
        Required: true
      },
      toggle_active:{
        type: Boolean,
        Required: true,
      },
    },
    data() {
      return {
        //Load Data
        allData: jsonData,
        sortby_options: [
          {value: '어문회', text: '어문회'},
          {value: '畫數', text: '획수'},
          {value: '음', text: '한국음'},
          {value: '사성음', text: '중국음'},
          {value: '音読み', text: '일본음'},
        ], 
        //choose words
        selected_item: {},
        selected_string: '',
        clicked_item: '',
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
      toggle_dropdown_readlev() {
        this.filter_open_readlev = !this.filter_open_readlev;
      },
      toggle_dropdown_writelev() {
        this.filter_open_writelev = !this.filter_open_writelev;
      },
      toggle_dropdown_chinalev() {
        this.filter_open_chinalev = !this.filter_open_chinalev;
      },
      toggle_dropdown_sortby() {
        this.sortby_open = !this.sortby_open;
      },
      handleClickOutside(event) {
        // Close dropdown if clicked outside of dropdown content
        const dropdownContent = this.$el.querySelector('.dropdown-content');
        const dropdown = this.$el.querySelector('.dropdown');
        if (this.filter_open_chinalev && !dropdown.contains(event.target) && !dropdownContent.contains(event.target)) {
          this.filter_open_chinalev = false;
        }
      }, 
      mounted() {
      // Add event listener to detect clicks outside
      document.addEventListener('click', this.handleClickOutside);
      },
      beforeDestroy() {
        // Remove event listener when component is destroyed
        document.removeEventListener('click', this.handleClickOutside);
      },
      sortResults() {
        this.SortLogic; // Just to ensure it recalculates based on selected sort
      },
      openPopup(url) {
        window.open(url, '_blank', 'width=600,height=400');
      },
      훈음(input) {
        const 훈 = input.훈;
        const 음 = input.음;
        const result = [];
        
        for (let i = 0; i < 훈.length; i++) {
          result.push(`${훈[i]} ${음[i]}`);
        }
        return result;
      },
      pinyin(input) {
        const 声 = input.声;
        const 韵 = input.韵;
        const tones = input.tones;
        const result = [];
        
        for (let i = 0; i < 声.length; i++) {
          result.push(`${声[i]}${韵[i]}${tones[i]}`);
        }
        return result;
      },
      SelectItem(input) {
        this.selected_item= input;
        this.$emit('emitted_searchresult',{selected_item: this.selected_item})
      },
      showPanel(input) {
        if (this.toggle_active){
          this.clicked_item = input;
        }
        else{
          this.SelectItem(input);
        }
      },
      closePanel() {
        this.clicked_item = '';
      },
      SelectClose(input){
        this.SelectItem(input);
        this.closePanel();
      },
      sortMethod(searchResults) {
        if (!searchResults || searchResults.length === 0) {
            return []; // Return an empty array if no results
          }
          
        const criterium = this.sortby_options.find(option => option.text === this.sortby_active).value;
          
          // Define the consonant order
        const consonantOrder = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's'];
          
        return searchResults.sort((a, b) => {
          // If sorting by pinyin, apply custom consonant and vowel logic
          if (criterium === '사성음') {
              const aConsonant = a.声[0] ? a.声[0].toString().toLowerCase() : '';
              const bConsonant = b.声[0] ? b.声[0].toString().toLowerCase() : '';
              
              const aVowel = a.韵[0] ? a.韵[0].toString().toLowerCase() : '';
              const bVowel = b.韵[0] ? b.韵[0].toString().toLowerCase() : '';
                
              const aTone = a.tones[0] ? parseInt(a.tones[0]) : 0;
              const bTone = b.tones[0] ? parseInt(b.tones[0]) : 0;
                
              // Compare consonants first
              if (`${aVowel}${aConsonant}` === `${bVowel}${bConsonant}`) {
                return aTone - bTone;
              }
                
              if (aConsonant === bConsonant) {
                return aVowel.localeCompare(bVowel);
              }
                return consonantOrder.indexOf(aConsonant) - consonantOrder.indexOf(bConsonant);
          }
            
          let aValue = '';
          let bValue = '';
          // For other criteria, use default sorting
          if (criterium === '음' || criterium === '音読み') {
              aValue = a[criterium][0] ? a[criterium][0].toString().toLowerCase() : '';
              bValue = b[criterium][0] ? b[criterium][0].toString().toLowerCase() : '';
          } 
          else {
              aValue = a[criterium] ? a[criterium].toString().toLowerCase() : '';
              bValue = b[criterium] ? b[criterium].toString().toLowerCase() : '';
          }
            
          return aValue.localeCompare(bValue);
        });
      },
    },
    computed: {
      SearchLogic() {
        const searchTerm = this.searched_item.toLowerCase();

        // If no filters are active, return null (or an empty array if preferred)
        if (this.searchby_active.length === 0) {
          console.log('no active filter');
          return null; // or return [];
        }
        console.log('Active Filter',this.searchby_active);
        // Apply the filters with OR logic (using `some`)
        return this.allData.filter(item => {
          return this.searchby_active.some(filter => {
            switch (filter) {
              case '한자':
                return [item.kr, item.jp, item.tw, item.cn].some(prop => 
                  prop.toLowerCase().includes(searchTerm)
                );
              case '훈':
                return item.훈.join(',').toLowerCase().includes(searchTerm);
              case '음':
                return item.음.join(',').toLowerCase().includes(searchTerm);
              case '부수':
                return item.部首.toLowerCase().includes(searchTerm);
              case '성부':
                return item.聲.toLowerCase().includes(searchTerm);
            }
          });
        });
      },
      FilterLogic() {
        const dataList = this.SearchLogic;

        // If no filters are selected for both filters, return all data
        if (this.filter_active_chinalev.length === 0 && this.filter_active_readlev.length === 0) {
          return dataList;
        }

        return dataList.filter(item => {
          // OR logic for Chinalev: if no filters for Chinalev, it's always true
          const matchesChinalev = this.filter_active_chinalev.length === 0 || 
          this.filter_active_chinalev.includes(item.级);

          // OR logic for Readlev: if no filters for Readlev, it's always true
          const matchesReadlev = this.filter_active_readlev.length === 0 || 
          this.filter_active_readlev.includes(item.읽기);

          // OR logic for Readlev: if no filters for Readlev, it's always true
          const matchesWritelev = this.filter_active_writelev.length === 0 || 
          this.filter_active_writelev.includes(item.쓰기);

          // AND logic: both Chinalev and Readlev conditions must be met
          return matchesChinalev && matchesReadlev && matchesWritelev;
        });
      },
      SortLogic() {
        const searchResults = this.FilterLogic; // Assuming FilterLogic is already defined

        // Filter the data
        if (!searchResults || searchResults.length === 0) {
          return []; // Return an empty array if no results
        }

        // Call the sortLogic method to sort the filtered results
        return this.sortMethod(searchResults);
      },  
    }  
  };
</script>
  <style>
    @import "../styles/checkbox.css";
    @import "../styles/searchbar.css";
    @import "../styles/searchresult.css";
    @import "../styles/toggle.css";
    @import "../styles/dropdown.css";
    @import "../styles/shape-table.css";
    @import "../styles/info-table.css";
    @import "../styles/related-table.css";
    @import "../styles/exposition.css";
    @import "../styles/popup.css";
    @import "../styles/flipcard.css";
  </style>
  
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




h2, h3 {
  margin: 0.5rem 0;
}

/* Dynamically scale the h2 text */
.h2-훈음 {
  margin: 0.5rem 0;
  font-size: clamp(0.8rem, 2.5vw, 1.5rem); /* Dynamic font size scaling */
  width: 100%; /* Ensures it takes the width of the container */
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.table-container {
  display: flex; /* Use Flexbox to align tables horizontally */
  gap: 20px; /* Add space between the tables */
}


/* Styles for the new table */
.custom-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  font-size: 0.9rem; /* Smaller font size */
  table-layout: auto; /* Allow columns to adjust based on content */
}

.custom-table td {
  border: 1px solid #ddd;
  padding: 6px 10px; /* Adjusted padding for better sizing */
}

.custom-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.custom-table tr:hover {
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
.span-filter-info {
  padding: 7px 14px;
  background-color: transparent;
  font-size: 10px; 
}
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
.blue-button {
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


.button-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  color: #0056b3;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  border-radius: 3px;
  transition: color 0.5s ease-in-out, border-bottom 0.5s ease-in-out;
}
.button-close:hover {
  background-color: #3464d4;
  color:#fff
}

/* <div> */
  .div-container {
  position: relative;
  max-width: 1000px; /* Adjust as needed */
  margin: 13px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Make icon inline with text */
.naver {
  background-color: #f0fff4; /* Light green background */
  border-left: 5px solid #00b300; /* Accent border on the left (darker green) */
  cursor: pointer;
}

.naver-header::before {
  content: "📗"; /* Icon to style it */
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
/* .h1-한자:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px) scale(1.05) rotate(-1deg);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
} */

.h5-context{
  font-size: small;
}



/* <audio> */
  audio {
  margin-top: 10px;
}

</style>
