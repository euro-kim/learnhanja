<template>
  <div class="survey-page">

      <h1>설문조사</h1>
  
    <form @submit.prevent="submitSurvey">
      <div class="div-questions">
        <label for="question0" class="label-question">개인정보를 입력해주세요</label>
        <br>
        <label class="label-answer"> 기프티콘 증정용으로만 사용됩니다. <br> 원하시지 않으면 빈칸으로 두셔도 됩니다.</label>
        <div class="div-options">
          <input type="text" id="q0q1" v-model="name" placeholder="실명(경비집행 요구사항)">
        </div>
        <div class="div-options">
          <input type="text" id="q0q2" v-model="answers.question0" placeholder="01012345678">
        </div>
        <label class="label-answer"> </label>
      </div>
    </form>
 
    <form @submit.prevent="submitSurvey">
      <div class="div-questions">
        <label for="question1" class="label-question">한자에 대해 얼마나 알고 계신가요?</label>
        <div class="div-options">
          <div class="form-answer">
            <input type="radio" id="q1o1" :value="1" v-model="answers.question1">
            <label for="q1o1">잘 알고 있음(상위 급수 취득 등)</label>
          </div>
          <div class="form-answer">
            <input type="radio" id="q1o2" :value="2" v-model="answers.question1">
            <label for="q1o2">어느정도 알고 있음(급수 취득 등)</label>
          </div>
          <div class="form-answer">
            <input type="radio" id="q1o3" :value="3" v-model="answers.question1">
            <label for="q1o3">보통(한문 수업 이수 등)</label>
          </div>
          <div class="form-answer">
            <input type="radio" id="q1o4" :value="4" v-model="answers.question1">
            <label for="q1o4">잘 모름</label>
          </div>
          <div class="form-answer">
            <input type="radio" id="q1o5" :value="5" v-model="answers.question1">
            <label for="q1o5">아예 모름</label>
          </div>
        </div>
      </div>
    </form>

    <form @submit.prevent="submitSurvey" class="form1">
      <div class="div-questions">
        <label for="question2" class="label-question">한자의 제자원리에 대해 알고 계신가요?</label>
        <div class="form-answer">
          <input type="radio" id="q2o1" :value="1" v-model="answers.question2">
          <label for="q2o1">잘 알고 있음</label>
        </div>
        <div class="form-answer">
          <input type="radio" id="q2o2" :value="2" v-model="answers.question2">
          <label for="q2o2">어느정도 알고 있음</label>
        </div>
        <div class="form-answer">
          <input type="radio" id="q2o3" :value="3" v-model="answers.question2">
          <label for="q2o3">보통</label>
        </div>
        <div class="form-answer">
          <input type="radio" id="q2o4" :value="4" v-model="answers.question2">
          <label for="q2o4">잘 모름</label>
        </div>
        <div class="form-answer">
          <input type="radio" id="q2o5" :value="5" v-model="answers.question2">
          <label for="q2o5">아예 모름</label>
        </div>
      </div>
    </form>

    <form @submit.prevent="TakeTest" class="form-container">
      <div class="button-container">
        <button @click="submitSurvey">제출</button>
      </div>
    </form>
    
  </div>
</template>

<script>
export default {
  name: 'SurveyPage',
  data() {
    return {
      name:'',
      answers: {
        question0: '',
        question1: null,
        question2: null
      }
    };
  },
  methods: {
    submitSurvey() {
      if (this.answers.question1 === null || this.answers.question2 === null) {
        alert('설문지를 완료해주세요');
      } else {
        this.$router.push({
          path: '/memory',
          query: { 
            name: this.name,
            phone: this.answers.question0,
            know_hanja: this.answers.question1,
            know_component: this.answers.question2,
          }
        });
      }
    }
  }
}
</script>
  
  <style scoped>
.survey-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f5f5;
}

/*button*/
button {
    margin-top: 0px;
    font-size: 18px;
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  button:hover {
    background-color: #3464d4;
  }
  .button-container {
    display: flex;
    justify-content: center;
    width: 100%; /* Ensure the button container spans the full width */
  }

  /*form*/
  form {
    justify-content: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: #f9f9f9;
    border: 3px solid #ddd;
    border-radius: 8px;
    width: 300px;
    margin: 0 auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .form-questions {
    display: flex;
    flex-direction: column;
    margin-bottom: 2px;
  }

  .form-answer {
    margin-top: 10px;
    display: flex;
    align-items: flex-start;
    margin-bottom: 1px;
  }
  
/* label */
  label {
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 14px;
    color: #333;
  }
  .label-question {
    margin-bottom: 5px;
    font-weight: light;
    font-size: 18px;
    color: #333;
    margin-bottom: 3px;
  }
  .label-answer {
    margin-bottom: 5px;
    font-weight:lighter;
    font-size: 12px;
    color: #333;
  }

/*input*/
  input[type="text"] {
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: border-color 0.3s ease;
  }
  input[type="text"]:focus {
    border-color: #66afe9;
    outline: none;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 8px rgba(102, 175, 233, 0.6);
  }

</style>