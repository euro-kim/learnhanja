<template>
  <div v-if="show_searchresult==true">
    <!-- Filter Dropdown -->
    <div class="optionbar-wrapper">
      <!-- Checkbox -->
      <div class="optionbar-container">
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

        <!-- Toggle Button -->
        <div class="toggle-container">
          <p>미리보기: </p>
          <label class="switch">
            <input type="checkbox" v-model="toggle_active">
            <span class="slider"></span>
          </label>
        </div>
      </div>
      <div class="optionbar-container">
      <!-- options -->
      <div class="dropdown-group">
        <div class="dropdown-container">
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
        <div class="dropdown-container">
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
        <div class="dropdown-container">
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
    </div>
    </div>
  </div>
</template>
  
  <script>
  export default {
    emits: ['emitted_searchbar'],
    props:{
      show_searchresult:{
        type: Boolean,
        Required: true,
      },
    },
    data() {
      return {
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
  
      };
    },
    watch: {
        sortby_active: 'emitFilters',
        filter_active_chinalev: 'emitFilters',
        filter_active_readlev: 'emitFilters',
        filter_active_writelev: 'emitFilters',
        checkbox_active: 'emitFilters',
        toggle_active: 'emitFilters'
    },
    methods:{
      emitFilters() {
        this.$emit('emitted_searchbar', {
        sortby_active: this.sortby_active,
        filter_active_chinalev: this.filter_active_chinalev,
        filter_active_readlev: this.filter_active_readlev,
        filter_active_writelev: this.filter_active_writelev,
        checkbox_active: this.checkbox_active,
        toggle_active: this.toggle_active
        });
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
    },
    mounted() {
      this.emitFilters();
    }
  };
</script>
<style>
  @import "../styles/checkbox.css";
  @import "../styles/toggle.css";
  @import "../styles/dropdown.css";
  @import "../styles/optionbar.css";
</style>
  
<style lang="css" scoped>
/* <div> */
  body {
  font-family: Arial, sans-serif; /* Set a clean, modern font */
  margin: 0;
  padding: 20px; /* Add padding around the body */
  background-color: #f7f9fc; /* Light background for contrast */
}

</style>
