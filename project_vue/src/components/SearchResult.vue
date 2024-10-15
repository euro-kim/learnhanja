<template>
    <div>

      <!-- Search Result -->
      <div v-if="searched_item !== '' && show_searchresult==true" class="div-container">

          <ul class="searchresult-ul">
            <li
            v-for="element in paginatedItems"
            :key="element.id"
            @click="showPanel(element)"
            class="searchresult-li"
            >
              <!-- 급수 -->
              <span 
                v-if="checkbox_active.includes('급수')" 
                style="font-size: 13px; display: block;font-weight:lighter;color: #333;"
              >
                {{ element["읽기"] }} {{element["쓰기"]}}
              </span>
              <!-- 한자 -->
              <span 
                style="font-size: 30px;display: block;font-weight: bold;color: #333;"
              >
                {{ element.kr }}
              </span>
              <!-- 훈음 -->
              <span 
                v-if="checkbox_active.includes('훈음')" 
                style="display: block;color: #666;"
              >
                {{ 훈음(element).join(', ') }}
              </span>
              <!-- 사성음 -->
              <span 
                v-if="checkbox_active.includes('중국음')" 
                style="display: block;color: #666;"
              >
                {{ pinyin(element).join(', ') }}
              </span>
              <!-- 일본음 -->
              <span 
                v-if="checkbox_active.includes('일본음')" 
                style="display: block;color: #666;"
              >
                {{ element.音読み.join(', ') }}
              </span>
              <!-- 일본훈 -->
              <span 
                v-if="checkbox_active.includes('일본훈')"
                style="display: block;color: #666;"
              >
                {{ element.訓読み.join(', ') }}
              </span>
            </li>
          </ul> 
      </div>

      <!-- Popup Panel -->
      <div v-if="clicked_item" class="popup-container">
        <p class="div-popup-level">{{clicked_item["읽기"]}} {{clicked_item["쓰기"]}}</p>
        <button class="popup-close" @click="closePanel">&times;</button>
        <div style="position: absolute;font-size: medium;top: 30%;left: 10%;">
          <p style="font-size: 12px">부수<br></p>
          <p class="popup-letter" @click="StringHandler(clicked_item.部首)">{{ clicked_item.部首}}</p>
        </div>
        <div style="position: absolute;font-size: medium;top: 30%;left: 80%;" >
          <p style="font-size: 12px" v-if="clicked_item.聲部">성부<br></p>
          <p class="popup-letter" @click="StringHandler(clicked_item.聲部)">{{ clicked_item.聲部}}</p>
        </div>
        <div style="position:relative;font-size: medium;top: 50%;left: 25%; width: 50%;height: 100%;">
          <h1 @click="SelectClose(clicked_item)" class="popup-word">{{ clicked_item.kr }}</h1>
        </div>
      </div>


      <div 
        class="pagination"
      >
        <button 
          v-for="page in page_options"
          :key="page"
          :class="{ active: page === currentPage }"
          @click="page !== '...' && page !=='..'? (currentPage = page, handlePageClick(page)) : null&&handlePageClick"
          @mouseover="page !== '...' && page !=='..'"
        >
          {{ page }}
        </button>
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
        //paegs
        currentPage: 1,    // Track the current page
        itemsPerPage: 25, // Number of items per page
        page_options:[],
      };
    },
  
  
    watch: {
      search(newVal) {
        if (newVal.length === 0) {
          this.clicked_item = '';
        }
      },
      searched_item(newVal, oldVal) {
        // Trigger handlePageClick() when searched_item (prop) is updated
        if (newVal !== oldVal) {
          this.handlePageClick();
        }
      }
    },
  
  
    methods:{
      mounted() {
        document.addEventListener('click', this.handleClickOutside);
      },  
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
      handlePageClick(){
        console.log('pages',this.page_options)
        const page=this.currentPage
        const pages = [];

        const totalPages = this.totalPages;
        if (totalPages <= 5) {
          // If there are 5 or fewer pages, show them all
          for (let i = 1; i <= totalPages; i++) {
            pages.push(i);
          }
        } 
        else {
          // More than 5 pages
          if (page <= 3) {
            pages.push(1, 2, 3, 4, '..', totalPages-1,totalPages);
          } else if (page >= totalPages - 2) {
            pages.push(1, 2, '...', totalPages - 3, totalPages - 2, totalPages - 1, totalPages);
          } else {
            pages.push(1, '..', page - 1, page, page + 1, '...', totalPages);
          }
        }
        this.page_options=pages

      }
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
        const searchResults = this.FilterLogic; 
        if (!searchResults || searchResults.length === 0) {
          return []; // Return an empty array if no results
        }
        // Call the sortLogic method to sort the filtered results
        return this.sortMethod(searchResults);
      },
      totalPages() {
        return Math.ceil(this.SortLogic.length / this.itemsPerPage);
      },
      // Return items for the current page
      paginatedItems() {
        const dataList=this.SortLogic
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.sortMethod(dataList).slice(start, end);
      },

    }  
  };
</script>
  <style>
    @import "../styles/searchresult.css";
    @import "../styles/shape-table.css";
    @import "../styles/popup.css";
    @import "../styles/pagination.css";
    </style>
  
<style scoped>
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

</style>
