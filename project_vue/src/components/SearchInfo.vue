<template>
    <div>
      <!-- Selection -->
      <div v-if="show_searchinfo==true" class="div-container">
        <div style="display: flex;gap: 20px;">
          <!-- 급수 -->
          <table  class="info-table">
            <tbody>
              <tr>
                <th>한국 한국어문회 읽기급수</th>
                <td v-if="selected_item['읽기']">{{ selected_item["읽기"] }}</td>
                <td v-else>-</td>
              </tr>
              <tr>
                <th>한국 한국어문회 쓰기급수</th>
                <td v-if="selected_item['쓰기']">{{ selected_item["쓰기"] }}</td>
                <td v-else>-</td>
              </tr>
              <tr>
                <th>중국 통용규범한자표 급수</th>
                <td v-if="selected_item['通用'] !==0">{{ selected_item["级"] }}级</td>
                <td v-else>-</td>
              </tr>
              <tr>
                <th>일본 検定 급수</th>
                <td v-if="selected_item['検定']">{{ selected_item["検定"] }}</td>
                <td v-else>-</td>
              </tr>
              <tr>
                <th>일본 JIS 수준</th>
                <td v-if="selected_item['JIS']">{{ selected_item["JIS"] }}</td>
                <td v-else>-</td>
              </tr>
            </tbody>
          </table>
          <!-- 기본 -->
          <div class="card-container" @click="toggleFlip">
            <div :class="['card', { flipped: isFlipped }]">
              <div class="card-front">
                <h1 
                  style="font-size: 70px;transition: background-color 0.3s, transform 0.3s; display: inline-block;"
                >
                  {{ selected_item.kr }}
                </h1>
                <h2 
                  style="margin: 0.5rem 0;font-size: clamp(0.8rem, 2.5vw, 1.5rem);width: 100%;text-align: center; white-space: nowrap;overflow: hidden;text-overflow: ellipsis;"
                >
                  {{ 훈음(selected_item).join('\n') }}
                </h2>
              </div>
                    <!-- 모양 정보 -->
              <div class="card-back">
                <h4>등재번호</h4>
                <table class="card-table">
                  <tr>
                    <th>한국 한국어문회</th>
                    <td v-if="selected_item.어문회==0">미등재</td>
                    <td v-else>{{selected_item.어문회}}</td>
                  </tr>
                  <tr>
                    <th>대만 표준국자자체표</th>
                    <td v-if="selected_item.標準==0">미등재</td>
                    <td v-else>{{selected_item.標準}}</td>
                  </tr>
                  <tr>
                    <th>중국 통용규범한자표</th>
                    <td v-if="selected_item.通用==0">미등재</td>
                    <td v-else>{{selected_item.通用}}</td>
                  </tr>
                  <tr>
                    <th>일본 상용한자표</th>
                    <td v-if="selected_item.常用==0">미등재</td>
                    <td v-else-if="selected_item.常用==-1">표외한자</td>
                    <td v-else>{{selected_item.常用}}</td>
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
                <td v-if="selected_item.훈">{{ (selected_item.훈).join(', ')}} </td>
                <td v-else>-</td>
              </tr>
              <tr>
                <th>한국음</th>
                <td v-if="selected_item.음">{{ (selected_item.음).join(', ')}} </td>
                <td v-else>-</td>
              </tr>
              <tr>
                <th>사성음</th>
                <td v-if="pinyin(selected_item)">{{ pinyin(selected_item).join(', ') }}</td>
                <td v-else>-</td>
              </tr>
              <tr>
                <th>일본훈</th>
                <td v-if="selected_item['訓読み'].join(', ') ">{{ (selected_item["訓読み"]).join(', ') }}</td>
                <td v-else>-</td>
              </tr>
              <tr>
                <th>일본음</th>
                <td v-if="(selected_item['音読み']).join(', ')">{{ (selected_item['音読み']).join(', ') }}</td>
                <td v-else>-</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="shape-container">
          <table class="shape-table property">
            <thead>
              <tr>
                <th v-for="(shape_property_header, index) in shape_property_headers" :key="index">
                  {{ shape_property_header }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td v-for="(shape_property_datum, index) in shape_property_data" :key="index">
                  {{ shape_property_datum }}
                </td>
              </tr>
            </tbody>
          </table>
          <table class="shape-table variant">
            <thead>
              <tr>
                <th v-for="(shape_variant_header, index) in shape_variant_headers" :key="index">
                  {{ shape_variant_header }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td v-for="(shape_variant_datum, index) in shape_variant_data" :key="index">
                  {{ shape_variant_datum }}
                </td>
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
            <table class="usage-table">
              <tbody>
                <tr v-for="(row, rowIndex) in selected_item['성어'].split('\n')" :key="rowIndex">
                  <td v-for="(item, colIndex) in parseProverb(row)" :key="colIndex">{{ item }}</td>
                </tr>
              </tbody>
            </table>
          </div>-->
  
          <div v-if="selected_item['HSK 급수'] !== '' && activeTab === 'HSK' ">
            <table class="usage-table">
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
                  <td>{{ hskword.HSK }}</td>
                  <td>
                    <span 
                      v-for="(char, index) in hskword.traditional.split('')" 
                      :key="index" 
                      @mouseover="updateHover($event, char); showPopup = true"
                      @mouseleave="showPopup = false" 
                      @click="handleCharacterClick(char)"
                    >
                      <a href="javascript:void(0)">{{ char }}</a>
                    </span>
                    <div 
                      v-if="showPopup" 
                      class="popup"
                      :style="{ top: popupY + 'px', left: popupX + 'px', position: 'fixed' }"

                    >
                      {{this.hover_item.kr}}
                      {{ 훈음(this.hover_item).join('\n') }}
                    </div>
                  </td>
                  <td>{{ hskword.simplified }}</td>
                  <td>{{ hskword.pinyin }}</td>
                  <td>{{ hskword['meaning(kor)'] }}</td>
                  <td>{{ hskword['meaning(eng)'] }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div v-if="selected_item['JLPT 급수'] !== '' && activeTab === 'JLPT'">
            <table class="usage-table">
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
    </div>
  </template>
  
  <script>
  import jsonData from '../data/hanja.json';
  import jsonHSK from '../data/hsk(merge).json';
  import jsonJLPT from '../data/jlpt(kor).json';
  
  export default {
    props:{
      selected_item:{
        type: Object,
        required: true,
      },
      show_searchinfo:{
        type: Boolean,
        Required: true,
      },
    },
    data() {
      return {
        //Load Data
        allData: jsonData,
        HSK : jsonHSK,
        JLPT: jsonJLPT,
  
        //choose words
        selected_string: '',
        clicked_item: '',
        //individual words
        activeTab: 'HSK', // Default active tab
        isFlipped: false,
        // Hanja Shapes
        shape_property_headers:['획수','제자원리','부수','성부'],
        shape_variant_headers:['한국자','대만자','중국자','일본자'],

        //
        showPopup: false,
        popupX: 0,
        popupY: 0,
        hover_item:'',
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
      openPopup(url) {
        window.open(url, '_blank', 'width=600,height=400');
      },
      toggleFlip() {
        this.isFlipped = !this.isFlipped;
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
      handleCharacterClick(input) {
        // Assuming allData is an array of objects
        var element = this.allData.find(item => item.kr === input);
        
        if (element) {
          console.log("Found element with 'kr' attribute:", element);
        } else {
          element = this.allData.find(item => item.tw === input);
          if (element) {
            console.log("Found element with 'tw' attribute:", element);
          } 
        }
        this.$emit('emitted_searchinfo',{updated_selected_item: element})
      },
      updateHover(event, char) {
        const offsetX = event.clientX * 0.1; // Adjust left by 10% of mouse position
        const offsetY = event.clientY * 0.09; // Adjust above by 10% of mouse position

        this.popupX = event.clientX - offsetX; // Move left
        this.popupY = event.clientY - offsetY; // Move above and add a little extra spacing (10px)

        // this.popupY = event.target.getBoundingClientRect().top + window.scrollY-(offsety)*zoomLevel/2;
        var element = this.allData.find(item => item.kr === char);
        if (element) {
          this.hover_item=element;
        } else {
          element = this.allData.find(item => item.tw === char);
          if (element) {
            this.hover_item=element;
          } 
        }
      }
      
    },
  
  
    computed: {
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
      shape_variant_data() {
        return [
          this.selected_item.kr,
          this.selected_item.tw,
          this.selected_item.cn,
          this.selected_item.jp,
        ];
      },
      shape_property_data() {
        return [
          this.selected_item.畫數,
          this.selected_item.制字+'문자',
          this.selected_item.部首,
          this.selected_item.聲部,
        ];
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
  @import "../styles/usage-table.css";
  @import "../styles/info-table.css";
  @import "../styles/related-table.css";
  @import "../styles/exposition.css";
  @import "../styles/popup.css";
  @import "../styles/flipcard.css";
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

/* Make icon inline with text */
.naver {
  background-color: #f0fff4; /* Light green background */
  border-left: 5px solid #00b300; /* Accent border on the left (darker green) */
  cursor: pointer;
}

.naver-header::before {
  content: "📗"; /* Icon to style it */
}

/* asd */

.text-container {
  position: relative;
}

.hover-text {
  cursor: pointer; /* Indicate that the text is interactive */
}
.popup {
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.5); /* Semi-transparent background */
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: absolute; /* Ensure it follows the mouse position */
  z-index: 1000; /* High z-index to appear above other elements */
  white-space: nowrap; /* Prevent text from wrapping */
  pointer-events: none; /* Prevent the popup from blocking hover events */
  display: inline-block; /* Ensure it wraps around the content */
}


</style>

  
  
  