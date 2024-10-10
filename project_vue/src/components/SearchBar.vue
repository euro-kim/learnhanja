<template>
    <div>
      <div :class="{'heading': true, 'folded-heading': user_input}">
        <a :href="link" rel="noopener noreferrer" class="logo-link">
          <img 
            alt="LearnHanja" 
            img src="/logo.png"
            :class="{'logo': true, 'folded': user_input}" 
          >
        </a>
      </div>
  
      <div class="div-search-wrapper">
        <div class="div-search-by">
          <button
            v-for="filter in searchby_options"
            :key="filter.key"
            class="button-searchby"
            :class="{ active: searchby_active.includes(filter.key) }"
            @click="toggleFilter(filter.key)"
          >
            {{ filter.label }}
          </button>
          <span class="span-searchby">로 검색하기</span>
        </div>
        <!-- Search Bar -->
        <div class="div-search-bar">
          <input 
            v-model="user_input" 
            placeholder="Search..." 
            class="input-search"
            @keyup.enter="performSearch" 
          >
          <button class="button-search" @click="performSearch">Search</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        //link
        link: 'http://learnhanja.com',
        //Search 
        user_input: '', //user input
        searched_item: '',
  
        //searchby
        searchby_options: [
          { key: '한자', label: '한자' },
          { key: '훈', label: '훈' },
          { key: '음', label: '음' },
          { key: '부수', label: '부수' },
          { key: '성부', label: '성부' },
        ],
        searchby_active: ['한자','훈','음'], // array to store active filters
  
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
      performSearch() {
        if (this.user_input.trim() !== '') {
          console.log('Searching for:', this.user_input);
          this.searched_item=this.user_input
          this.selected_item = '';
          this.selected_string = '';
          this.clicked_item = '';
          this.$emit('emitted_searchbar',{searched_item: this.searched_item, searchby_active: this.searchby_active})
        } else {
          console.log('Search input is empty');
        }
      },
    },
 };
  
  </script>
  <style>
  @import "../styles/searchbar.css";
  </style>

  <style lang="css" scoped>
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


  </style>
  
 
  
  
  