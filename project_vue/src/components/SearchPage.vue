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
          class="button-filter"
          :class="{ active: searchby_active.includes(filter.key) }"
          @click="toggleFilter(filter.key)"
        >
          {{ filter.label }}
        </button>
        <span class="span-filter-info">로 검색하기</span>
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
    <!-- Selection -->
    <div v-if="selected_item !== ''" class="div-container">
      <div class="table-container">
        <!-- 급수 -->
        <table  class="info-table">
          <tbody>
            <tr>
              <th>한국어문회급수</th>
              <td>{{ selected_item["읽기"] }} {{ selected_item["쓰기"] }}</td>
            </tr>
            <tr>
              <th>중국 통용규범한자표 급수</th>
              <td v-if="selected_item['通用規範'] !==0">{{ selected_item["级"] }}级</td>
              <td v-else>-</td>
            </tr>
            <tr >
              <th> 일본 상용한자</th>
              <td v-if="selected_item['常用'] !== 0">등재</td>
              <td v-else>미등재</td>
            </tr>
            <tr>
              <th>일본 漢字検定 급수</th>
              <td v-if="selected_item['漢字検定'] !== '[]'">{{ selected_item["漢字検定"] }}</td>
              <td v-else>-</td>
            </tr>
            <tr>
              <th>JIS 수준</th>
              <td v-if="selected_item['JIS水準'] !== '[]'">{{ selected_item["JIS水準"] }}</td>
              <td v-else>-</td>
            </tr>
          </tbody>
        </table>
        <!-- 기본 -->
        <div class="card-container" @click="toggleFlip">
          <div :class="['card', { flipped: isFlipped }]">
            <div class="card-front">
              <h1 class="h1-한자">{{ selected_item.kr }}</h1>
              <h2 class="h2-훈음">{{ 훈음(selected_item).join('\n') }}</h2>
            </div>
                  <!-- 모양 정보 -->
            <div class="card-back">
              <table class="card-table">
                <tr>
                  <th>제자원리</th>
                  <td>{{selected_item.制字}}</td>
                </tr>
                <tr>
                  <th>획수</th>
                  <td>{{selected_item.畫數}}</td>
                </tr>
                <tr>
                  <th>부수</th>
                  <td>{{selected_item.部首}}</td>
                </tr>
                <tr v-if="selected_item.聲部 !== ''">
                  <th>성부</th>
                  <td>{{selected_item.聲部}}</td>
                </tr>
              </table>
              <table class="card-table">
                <caption class="table-caption" v-if="selected_item.jp !== '' || selected_item.cn !== '' || selected_item.tw !== ''">
                  이체자
                </caption>
                <tr v-if="selected_item.jp !== ''">
                  <th>일본자</th>
                  <td>{{selected_item.jp}}</td>
                </tr>
                <tr v-if="selected_item.cn !== ''">
                  <th>중국자</th>
                  <td>{{selected_item.cn}}</td>
                </tr>
                <tr v-if="selected_item.tw !== ''">
                  <th>대만자</th>
                  <td>{{selected_item.tw}}</td>
                </tr>
              </table>
            </div>
          </div>
        </div>
        <!--소리-->
        <table  class="info-table">
          <tbody>
            <tr>
              <th>한국훈</th>
              <td>{{ (selected_item.훈).join('\n')}} </td>
            </tr>
            <tr>
              <th>한국음</th>
              <td>{{ (selected_item.음).join('\n')}} </td>
            </tr>
            <tr>
              <th>사성음</th>
              <td>{{ pinyin(selected_item).join('\n') }}</td>
            </tr>
            <tr>
              <th>일본훈</th>
              <td>{{ (selected_item["訓読み"]).join('\n') }}</td>
            </tr>
            <tr>
              <th>일본음</th>
              <td>{{ (selected_item['音読み']).join('\n') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    <div class="exposition">
      <div class="exposition-header">
        English Meaning
      </div>
      <div class="exposition-meaning">
        {{selected_item.meaning}}
      </div>
    </div>
    <div class="naver" @click="openPopup(`https://hanja.dict.naver.com/#/search?query=${selected_item.kr}&range=all`)">
      <div class="naver-header">
        Naver Search
      </div>
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

        <!-- <div v-if="selected_item['성어'] !== '' && activeTab === '성어'">
          <h3> 한국어문회 성어 </h3>
          <table class="custom-table">
            <tbody>
              <tr v-for="(row, rowIndex) in selected_item['성어'].split('\n')" :key="rowIndex">
                <td v-for="(item, colIndex) in parseProverb(row)" :key="colIndex">{{ item }}</td>
              </tr>
            </tbody>
          </table>
        </div>-->

        <div v-if="selected_item['HSK 급수'] !== '' && activeTab === 'HSK' ">
          <table class="custom-table">
            <thead>
              <tr>
                <th>HSK 급수</th>
                <th>단어</th>
                <th>사성음</th>
                <th>뜻</th>
                <th>Meaning</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="hskword in HSKData" :key="hskword.id"> <!-- Assuming each word has a unique id -->
                <td>{{ hskword.HSK}}</td>
                <td>{{ hskword.traditional }}({{ hskword.simplified }})</td>
                <td>{{ hskword.pinyin }}</td>
                <td>{{ hskword['meaning(kor)'] }}</td>
                <td>{{ hskword['meaning(eng)'] }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-if="selected_item['JLPT 급수'] !== '' && activeTab === 'JLPT'">
          <table class="custom-table">
            <thead>
              <tr>
                <th>JLPT 급수</th>
                <th>단어</th>
                <th>히라가나</th>
                <th>품사</th>
                <th>뜻</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="jlptword in JLPTData" :key="jlptword.JLPT"> <!-- Assuming each word has a unique id -->
                <td>{{ jlptword.JLPT}}</td>
                <td>{{ jlptword.word}}</td>
                <td>{{ jlptword.hiragana }}</td>
                <td>{{ jlptword.type.join(',') }}</td>
                <td>{{ jlptword.meaning }}</td>
              </tr>
            </tbody>
          </table>  
        </div> 
      </div>
      
    </div>

    <!-- Filter Dropdown -->
    <div v-if="searched_item !== '' && selected_item == ''"> 
      <div @click="handleClickOutside" class="dropdown-container">
        <div @click.stop="toggle_dropdown_readlev" 
          class="dropdown"
          :class="{ 'dropdown-open': filter_open_readlev }"
          >
          읽기급수
          <!-- <span v-if="filter_active_readlev.length"> ({{ filter_active_readlev.length }})</span> -->
        </div>
        <div v-if="filter_open_readlev" class="dropdown-content">
            <label v-for="option in filter_options_readlev" :key="option.value">
              <input 
                type="checkbox" 
                :value="option.value" 
                v-model="filter_active_readlev" 
              />
              {{ option.text }}
            </label>
        </div>
      </div> 

      <div @click="handleClickOutside" class="dropdown-container">
        <div 
          @click.stop="toggle_dropdown_writelev" 
          class="dropdown"
          :class="{ 'dropdown-open': filter_open_writelev }"
        >
          쓰기급수
          <!-- <span v-if="filter_active_writelev.length"> ({{ filter_active_writelev.length }})</span> -->
        </div>
        <div v-if="filter_open_writelev" class="dropdown-content">
          <label v-for="option in filter_options_writelev" :key="option.value">
            <input 
              type="checkbox" 
              :value="option.value" 
              v-model="filter_active_writelev" 
            />
            {{ option.text }}
          </label>
        </div>
      </div> 

      <div @click="handleClickOutside" class="dropdown-container">
        <div 
          @click.stop="toggle_dropdown_chinalev" 
          class="dropdown"
          :class="{ 'dropdown-open': filter_open_chinalev }"
        >
          China Level
          <!-- <span v-if="filter_active_chinalev.length"> ({{ filter_active_chinalev.length }})</span> -->
        </div>
        <div v-if="filter_open_chinalev" class="dropdown-content">
          <label v-for="option in filter_options_chinalev" :key="option.value">
            <input 
              type="checkbox" 
              :value="option.value" 
              v-model="filter_active_chinalev" 
            />
            {{ option.text }}
          </label>
        </div>
      </div> 
    </div>
      
      <!-- Search Result -->
      <div v-if="searched_item !== '' && selected_item == '' " class="div-container">
        <!-- Sortby Dropdown -->
        <div @click="handleClickOutside" class="dropdown-container">
          <div 
            @click.stop="toggle_dropdown_sortby" 
            class="dropdown"
            :class="{ 'dropdown-open': sortby_open }"
          >
            정렬기준
            <span v-if="sortby_active.length>0">: {{ sortby_active }}</span>
          </div>
          <div v-if="sortby_open" class="dropdown-content">
            <label v-for="option in sortby_options" :key="option.value">
              <input 
                type="radio" 
                :value="option.text" 
                v-model="sortby_active" 
              />
              {{ option.text }}
            </label>
          </div>
        </div> 
        <br>
        <br>
        <div> 
          <span v-if="selected_item !== ''"> {{selected_item.kr}}</span>
          <span v-if="selected_string !== ''"> {{selected_string}} does not exist </span>
        </div>
        <ul v-if=!selected_item class="ul-five">
          <li
          v-for="element in SortLogic"
          :key="element.id"
          @click="showPanel(element)"
          >
          <span class="span-level">{{ element["읽기"] }} {{element["쓰기"]}}</span>
          <span class="span-word" >{{ element.kr }}</span>
          <span class="span-meaning-sound">{{ 훈음(element).join('\n') }}</span>
          </li>
        </ul> 
      </div>
    <!-- Related Words -->
      <!-- <div v-if="searched_item !== '' && RelatedData !=null" class="div-container">
        <a1>관련 한자</a1>
        <ul class="ul-five">
          <li
            v-for="element in RelatedData"
            :key="element.한자"
            @click="showPanel(element)"
          >
            <span class="span-level">{{ element["읽기"] }} {{element["쓰기"]}}</span>
            <span class="span-word">{{ element.kr }}</span>
            <span class="span-meaning-sound">{{ 훈음(element).join('\n')}}</span>
          </li>
        </ul>
      </div> -->
      
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
import jsonHSK from '../data/hsk(merge).json';
import jsonJLPT from '../data/jlpt(kor).json';

export default {
  data() {
    return {
      //Load Data
      allData: jsonData,
      HSK : jsonHSK,
      JLPT: jsonJLPT,
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

      //sortby
      sortby_open: false,
      sortby_options: [
        {value: '어문회', text: '어문회'},
        {value: '畫數', text: '획수'},
      ], 
      sortby_active: '어문회', 
      
      //Filter
      filter_open_chinalev: false,
      filter_options_chinalev: [
        { value: 1, text: '1级' },
        { value: 2, text: '2级' },
        { value: 3, text: '3级' },
        { value: '', text: '기타' },
      ],
      filter_active_chinalev: [1,2,3,''], //'1级','2级','3级','기타']

      filter_open_readlev: false,
      filter_options_readlev: [
        { value: '읽기8급', text: '읽기8급' },
        { value: '읽기7급II', text: '읽기7급II' },
        { value: '읽기7급', text: '읽기7급' },
        { value: '읽기6급II', text: '읽기6급II' },
        { value: '읽기6급', text: '읽기6급' },
        { value: '읽기5급II', text: '읽기5급II' },
        { value: '읽기5급', text: '읽기5급' },
        { value: '읽기4급II', text: '읽기4급II' },
        { value: '읽기4급', text: '읽기4급' },
        { value: '읽기3급II', text: '읽기3급II' },
        { value: '읽기3급', text: '읽기3급' },
        { value: '읽기2급', text: '읽기2급' },
        { value: '읽기1급', text: '읽기1급' },
        { value: '읽기특급II', text: '읽기특급II' },
        { value: '읽기특급', text: '읽기특급' },
        { value: '', text: '기타' },
      ],
      filter_active_readlev: ['읽기8급','읽기7급II','읽기7급','읽기6급II','읽기6급','읽기5급II','읽기5급','읽기4급II','읽기4급','읽기3급II','읽기3급','읽기2급','읽기1급'],
      
      filter_open_writelev: false,
      filter_options_writelev: [
        { value: '쓰기8급', text: '쓰기8급' },
        { value: '쓰기7급II', text: '쓰기7급II' },
        { value: '쓰기7급', text: '쓰기7급' },
        { value: '쓰기6급II', text: '쓰기6급II' },
        { value: '쓰기6급', text: '쓰기6급' },
        { value: '쓰기5급II', text: '쓰기5급II' },
        { value: '쓰기5급', text: '쓰기5급' },
        { value: '쓰기4급II', text: '쓰기4급II' },
        { value: '쓰기4급', text: '쓰기4급' },
        { value: '쓰기3급II', text: '쓰기3급II' },
        { value: '쓰기3급', text: '쓰기3급' },
        { value: '쓰기2급', text: '쓰기2급' },
        { value: '쓰기1급', text: '쓰기1급' },
        { value: '쓰기특급II', text: '쓰기특급II' },
        { value: '쓰기특급', text: '쓰기특급' },
        { value: '', text: '기타' },
      ],
      filter_active_writelev: ['쓰기8급','쓰기7급II','쓰기7급','쓰기6급II','쓰기6급','쓰기5급II','쓰기5급','쓰기4급II','쓰기4급','쓰기3급II','쓰기3급','쓰기2급','쓰기1급'],
      

      //choose words
      selected_item: '',
      selected_string: '',
      clicked_item: '',
      //individual words
      activeTab: '성어', // Default active tab
      isFlipped: false,
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
    toggleFilter(key) {
      const index = this.searchby_active.indexOf(key);
      if (index === -1) {
        this.searchby_active.push(key); // Add the filter if not active
      } else {
        this.searchby_active.splice(index, 1); // Remove the filter if already active
      }
    },
    sortResults() {
      this.SortLogic; // Just to ensure it recalculates based on selected sort
    },
    openPopup(url) {
      window.open(url, '_blank', 'width=600,height=400');
    },
    toggleFlip() {
      this.isFlipped = !this.isFlipped;
    },
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
    performSearch() {
      // Trigger your search logic here
      if (this.user_input.trim() !== '') {
        // Perform the search with the input value
        console.log('Searching for:', this.user_input);
        this.searched_item=this.user_input
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
      console.log(input)
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
              return item.kr.toLowerCase().includes(searchTerm);
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
      const criterium =this.sortby_options.find(option => option.text === this.sortby_active).value

      return searchResults.sort((a, b) => {
        // Check if the properties exist and handle undefined cases
        const aValue = a[criterium] ? a[criterium].toString().toLowerCase() : '';
        const bValue = b[criterium] ? b[criterium].toString().toLowerCase() : '';

        if (aValue < bValue) {
          return -1; // a comes before b
        }
        if (aValue > bValue) {
          return 1; // a comes after b
        }
        return 0; // Equal case
      });
    },
    RelatedData() {
      const target = this.selected_item
      if (target !== '' && target.制字 == '형성' ) {
          return this.allData.filter(item =>
            item.聲部.toLowerCase().includes(target.聲部)
          );
        }
      else {
        return null;
      }
    },
    HSKData() {
      const target=this.selected_item    
      if (target) {
        return this.HSK.filter(item =>
            item.traditional.toLowerCase().includes(target.kr)
          );
        }
      else {
        return null;
      }
    },
    JLPTData() {
      const target=this.selected_item    
      if (target) {
        return this.JLPT.filter(item =>
            item.word.toLowerCase().includes(target.kr)
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
  border-bottom: 3px solid #007bff;
}

.tabs button.active {
  border-bottom: 3px solid #007bff;
}
/* dropdown */
/* dropdown */
.dropdown-container {
  position: relative;
  display: inline-block;
}

.dropdown {
  cursor: pointer;
  padding: 10px 30px 10px 10px;
  border: none;
  border-bottom: 2px solid transparent;
  font-weight: 500;
  transition: border-color 0.3s ease;
  position: relative;
  font-family: 'Noto Sans KR', sans-serif; /* Use pretty font */
}

.dropdown:hover {
  border-bottom: 2px solid #007BFF;
}

.dropdown-active {
  border-bottom: 2px solid #007bff;
}

.dropdown-content {
  display: block;
  position: absolute;
  background-color: rgba(255, 255, 255, 0.9);
  border: none;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1;
  padding: 10px;
  width: 120px;
}

.dropdown-content label {
  display: block;
  padding: 3px 0;
  font-weight: 400;
  cursor: pointer;
  transition: color 0.3s ease;
  text-align: left;
}

.dropdown-content label:hover {
  color: #007bff;
}

.dropdown-content input[type="checkbox"] {
  margin-right: 8px;
}

/* Custom arrow */
.dropdown::after {
  content: '';
  position: absolute;
  top: 50%;
  right: 10px;
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid #333; /* Simple arrow pointing down */
  transform: translateY(-50%);
  transition: transform 0.3s ease; /* Smooth rotation */
  pointer-events: none; /* Allow clicks through */
}

.dropdown-open::after {
  transform: translateY(-50%) rotate(180deg); /* Arrow pointing up */
}



/* Centering the dropdown */
.sort-dropdown {
  width: 200px; /* Maintain minimal width */
  margin: 0 auto; /* Center the dropdown */
  text-align: center; /* Center content */
  background-color: transparent;
  position: relative; /* Required for custom arrow */
}

/* Minimalistic select styling */
.sort-dropdown select {
  width: 100%;
  padding: 8px 0; /* Minimal padding */
  border: none; /* No border */
  border-bottom: 2px solid #ccc; /* Neutral underline */
  background-color: transparent; /* Transparent background */
  color: #333; /* Neutral text color */
  font-size: 16px;
  font-family: 'Noto Sans KR', sans-serif; /* Use pretty font */
  text-align: center; /* Center text */
  appearance: none; /* Remove default arrow */
  cursor: pointer;
  transition: border-color 0.3s ease;
}

/* Underline color when an item is selected */
.sort-dropdown select:not([value=""]) {
  border-bottom: 2px solid #007BFF; /* Blue underline when something is selected */
}

/* Subtle hover effect for dropdown */
.sort-dropdown select:hover {
  border-bottom: 2px solid #007BFF; /* Blue underline on hover */
}

/* Fancy dropdown items animation */
.sort-dropdown select option {
  padding: 8px; /* Minimal padding */
  background-color: transparent;
  color: #333;
  transition: transform 0.2s ease-in-out, opacity 0.2s ease-in-out; /* Animation for smooth dropdown effect */
  transform: translateY(20px); /* Initially below */
  opacity: 0; /* Initially invisible */
}

/* Animate dropdown items on open */
.sort-dropdown select:focus option {
  transform: translateY(0); /* Move to place */
  opacity: 1; /* Fade in */
}

/* Custom arrow */
.sort-dropdown::after {
  content: '';
  position: absolute;
  top: 50%;
  right: 10px;
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid #333; /* Simple arrow */
  transform: translateY(-50%);
  transition: transform 0.3s ease; /* Smooth rotation */
  pointer-events: none; /* Allow clicks through */
}

/* Rotate arrow when dropdown is open */
.sort-dropdown select:focus + .sort-dropdown::after {
  transform: translateY(-50%) rotate(180deg); /* Arrow pointing up */
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

/* Container for the table */
.info-table {
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
.info-table th {
  width: 15%;
  background: linear-gradient(45deg, #1E90FF, #00BFFF); /* Gradient blue */
  color: white;
  font-size: 13px;
  text-align: left;
  padding: 12px 15px;
  font-weight: bold;
}

/* Table body styling */
.info-table td {
  width: 15%;
  font-size: 13px;
  padding: 12px 15px;
  border-bottom: 1px solid #ddd; /* Light border for separation */
}

/* Alternate row background color */
.info-table tbody tr:nth-child(even) {
  background-color: #f2f8fc; /* Light blue background for even rows */
}

/* First column (header) styling */
.info-table th:first-child {
  border-top-left-radius: 10px; /* Rounded corners */
}

.info-table th:last-child {
  border-top-right-radius: 10px; /* Rounded corners */
}

.info-table td:first-child {
  border-left: none; /* Removes the border on the first column */
}

.info-table td:last-child {
  border-right: none; /* Removes the border on the last column */
}

/* Last row styling */
.info-table tbody tr:last-child td {
  border-bottom: none; /* Removes the bottom border for the last row */
}

/* Responsive design */
@media (max-width: 600px) {
  table, th, td {
    font-size: 16px;
  }
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
    box-sizing: border-box; /* Include padding and border in the element's total size */
  border-bottom: 3px solid transparent; /* Add a transparent border */
  background-color: transparent;
  color: #a0a0a0;
  font-size: 10px; 
  transition: color 0.2s ease-in-out, border-bottom 0.2s ease-in-out;

}

.button-filter:hover {
  color: #333;
  border-bottom: 3px solid #007bff;
   
}

.button-filter.active {
  color: #333; /* White text for active filter buttons */
  border-bottom: 3px solid #007bff;
}

.button-filter:hover:not(.disabled) {
  background-color: transparent; /* Example background color on hover */
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

/* wraps SearchBy and SearchBar */
.div-search-wrapper {
  display: flex;
  flex-direction: column; /* Stack children vertically */
  align-items: flex-start;
  width: 100%;
}

.div-search-by {
  display: flex; /* Use flexbox for alignment */
  justify-content: center;
  align-items: center;
  width: 100%;
}

.div-search-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.exposition {
  margin: 20px 0;
  padding: 20px;
  background-color: #e6f7ff; /* Light blue background */
  border-left: 5px solid #1E90FF; /* Accent border on the left */
  border-radius: 8px; /* Smooth rounded corners */
  font-family: 'Arial', sans-serif;
  font-size: 14px;
  color: #333; /* Dark text for readability */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Subtle shadow */
}

/* Make icon inline with text */
.exposition-header {
  display: flex;
  align-items: center;
  font-weight: bold;
  margin-bottom: 10px;
}

.exposition-header::before {
  content: "📘"; /* Icon to style it */
  font-size: 20px;
  margin-right: 10px;
}

.exposition-meaning {
  font-family: 'Times New Roman', Times, serif; /* Apply Times New Roman */
  font-size: 16px; /* Adjust size if needed */
  font-style: italic; /* Optional: makes the text italic */
}

@media (max-width: 600px) {
  .exposition {
    font-size: 16px;
    padding: 15px;
  }
}
.naver {
  margin: 20px 0;
  padding: 20px;
  background-color: #f0fff4; /* Light green background */
  border-left: 5px solid #00b300; /* Accent border on the left (darker green) */
  border-radius: 8px; /* Smooth rounded corners */
  font-family: 'Arial', sans-serif;
  font-size: 14px;
  color: #333; /* Dark text for readability */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Subtle shadow */
  cursor: pointer;
}


/* Make icon inline with text */
.naver-header {
  display: flex;
  align-items: center;
  font-weight: bold;
  margin-bottom: 10px;
}

.naver-header::before {
  content: "📗"; /* Icon to style it */
  font-size: 20px;
  margin-right: 10px;
}

@media (max-width: 600px) {
  .naver {
    font-size: 16px;
    padding: 15px;
  }
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
  perspective: 1000px;
  cursor: pointer; /* Change cursor to pointer to indicate it's clickable */
}

.card-container {
  perspective: 1000px;
  cursor: pointer;
  width: 20%; /* Keeping the card width as per your preference */
}

.card {
  width: 100%; /* Ensures the card takes up the full width of the container */
  height: 100%; /* Adjust the height as needed */
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.6s;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Your box-shadow style */
  border-radius: 10px; /* Your border-radius style */
}

/* Add hover effect */
.card:hover {
  transition: transform 0.3s;
  transform: rotateY(30deg); /* Slightly rotate to indicate a flip */
}

.card.flipped {
  transform: rotateY(180deg);
}

.card-front,
.card-back {
  width: 100%;
  height: 100%;
  position: absolute;
  backface-visibility: hidden;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  border-radius: 10px; /* Ensures the rounded corners are consistent */
  text-align: center;
  overflow: hidden; /* Ensure no overflow of text */
}

.card-back {
  background-color: #f1f1f1;
  color: #333;
  transform: rotateY(180deg);
}

</style>


