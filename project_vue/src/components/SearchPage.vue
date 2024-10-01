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
              <td>{{ (selected_item.훈).join(', ')}} </td>
            </tr>
            <tr>
              <th>한국음</th>
              <td>{{ (selected_item.음).join(', ')}} </td>
            </tr>
            <tr>
              <th>사성음</th>
              <td>{{ pinyin(selected_item).join(', ') }}</td>
            </tr>
            <tr>
              <th>일본훈</th>
              <td>{{ (selected_item["訓読み"]).join(', ') }}</td>
            </tr>
            <tr>
              <th>일본음</th>
              <td>{{ (selected_item['音読み']).join(', ') }}</td>
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
    <div class="exposition naver" @click="openPopup(`https://hanja.dict.naver.com/#/search?query=${selected_item.kr}&range=all`)">
      <div class="exposition-header naver-header">
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
                <th>번체자</th>
                <th>간체자</th>
                <th>사성음</th>
                <th>뜻</th>
                <th>Meaning</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="hskword in HSKData" :key="hskword.id"> <!-- Assuming each word has a unique id -->
                <td>{{ hskword.HSK}}</td>
                <td>{{ hskword.traditional }}</td>
                <td>{{ hskword.simplified }}</td>
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
          통용규범한자표
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
      <!-- Toggle Button -->
      <div class="toggle-container">
        <label class="switch">
          <input type="checkbox" v-model="toggle_active">
          <span class="slider"></span>
        </label>
        <p>미리보기</p>
      </div>
      <!-- Checkbox -->
        <div class="checkbox-group">
          <label v-for="option in checkbox_options" :key="option.value" class="checkbox-label">
            <input
              type="checkbox"
              :value="option.value"
              v-model="checkbox_active"
            />
            {{ option.value }}
          </label>
        </div>

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
            <span v-if="checkbox_active.includes('급수')" class="span-level">{{ element["읽기"] }} {{element["쓰기"]}}</span>
            <span class="span-word" >{{ element.kr }}</span>
            <span v-if="checkbox_active.includes('훈음')" class="span-meaning-sound">{{ 훈음(element).join(', ') }}</span>
            <span v-if="checkbox_active.includes('중국음')" class="span-meaning-sound">{{ pinyin(element).join(', ') }}</span>
            <span v-if="checkbox_active.includes('일본음')" class="span-meaning-sound">{{ element.音読み.join(', ') }}</span>
            <span v-if="checkbox_active.includes('일본훈')" class="span-meaning-sound">{{ element.訓読み.join(', ') }}</span>
          </li>
        </ul> 
      </div>
    <!-- Related Words -->
      <div v-if="selected_item !== '' " class="div-container">
        <a1>소리가 비슷한 한자</a1>
        <ul class="ul-five">
          <li
            v-for="element in RelatedData"
            :key="element.kr"
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
import jsonData from '../assets/json/hanja.json';
import jsonHSK from '../assets/json/hsk(merge).json';
import jsonJLPT from '../assets/json/jlpt(kor).json';

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
        {value: '음', text: '한국음'},
        {value: '사성음', text: '중국음'},
        {value: '音読み', text: '일본음'},
      ], 
      sortby_active: '중국음', 
      
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
      filter_active_readlev: ['읽기8급','읽기7급II','읽기7급','읽기6급II','읽기6급','읽기5급II','읽기5급','읽기4급II','읽기4급','읽기3급II','읽기3급','읽기2급','읽기1급','읽기특급II','읽기특급','' ],
      
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
      filter_active_writelev: ['쓰기8급','쓰기7급II','쓰기7급','쓰기6급II','쓰기6급','쓰기5급II','쓰기5급','쓰기4급II','쓰기4급','쓰기3급II','쓰기3급','쓰기2급','쓰기1급','쓰기특급II','쓰기특급',''],
      
      //Display
      checkbox_active: ['훈음','중국음'], // List to store all selected values
      checkbox_options: [
        {value: '급수'},
        {value: '훈음'},
        {value: '중국음'},
        {value: '일본음'},
        {value: '일본훈'},
      
      ],

      toggle_active: false, // State of the toggle (binary: true/false)

      //choose words
      selected_item: '',
      selected_string: '',
      clicked_item: '',
      //individual words
      activeTab: 'HSK', // Default active tab
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
        } else {
          aValue = a[criterium] ? a[criterium].toString().toLowerCase() : '';
          bValue = b[criterium] ? b[criterium].toString().toLowerCase() : '';
        }

        return aValue.localeCompare(bValue);
      });
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
      const searchResults = this.FilterLogic; // Assuming FilterLogic is already defined

      // Filter the data
      if (!searchResults || searchResults.length === 0) {
        return []; // Return an empty array if no results
      }

      // Call the sortLogic method to sort the filtered results
      return this.sortMethod(searchResults);
    },  
    RelatedData() {
      const target = this.selected_item;

      // Return an empty array if target is invalid or doesn't meet the conditions
      if (!target) {
        return []; 
      }

      // Filter the data based on the target, only applying each filter if the target value is not an empty string
      const filteredData = this.allData.filter(item => {
        const matches聲部 = target.聲部 !== '' ? item.聲.toLowerCase().includes(target.聲部.toLowerCase()) : false;
        const matches聲 = target.聲 !== '' ? item.聲.toLowerCase().includes(target.聲.toLowerCase()) : false;
        const matchesKr = target.kr !== '' ? item.聲.toLowerCase().includes(target.kr.toLowerCase()) : false;

        // Include the item if it matches any one of the applicable filters (OR logic)
        return matches聲部 || matches聲 || matchesKr;
      });


      // Call the sortMethod to sort the filtered results
      return this.sortMethod(filteredData);
    },

    HSKData() {
      const target=this.selected_item    
      if (target) {
        if (target.tw !== '' && target.jp === ''){
          return this.HSK.filter(item =>
              item.traditional.toLowerCase().includes(target.tw)
            );
        }
        if (target.tw === '' && target.jp !== ''){
          return this.HSK.filter(item =>
              item.traditional.toLowerCase().includes(target.jp)
            );
        }
        if (target.tw !== '' && target.jp !== ''){
          return this.HSK.filter(item =>
              item.traditional.toLowerCase().includes(target.tw)
            );
        }
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
      console.log(target)
      if (target) {
        if (target.tw !== '' && target.jp === ''){
          return this.JLPT.filter(item =>
              item.word.toLowerCase().includes(target.tw)
            );
          }
        if (target.tw === '' && target.jp !== ''){
          return this.JLPT.filter(item =>
              item.word.toLowerCase().includes(target.jp)
            );
        }
        if (target.tw !== '' && target.jp !== ''){
          return this.JLPT.filter(item =>
              item.word.toLowerCase().includes(target.jp)
            );
        }
        return this.JLPT.filter(item =>
          item.word.toLowerCase().includes(target.kr)
        );
      }
      else {
        return null;
      }
    },
  }  
};

</script>
<style>
@import "../assets/css/checkbox.css";
@import "../assets/css/searchbar.css";
@import "../assets/css/searchresult.css";
@import "../assets/css/toggle.css";
@import "../assets/css/dropdown.css";
@import "../assets/css/info-table.css";
@import "../assets/css/related-table.css";
@import "../assets/css/exposition.css";
@import "../assets/css/popup.css";
@import "../assets/css/flipcard.css";
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


