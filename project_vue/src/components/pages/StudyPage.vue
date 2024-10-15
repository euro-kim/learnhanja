<template>
  <div >
    <SearchOption 
      :show_searchresult="show_searchresult"
      @emitted_searchbar="handle_emitted_searchoption"/>
    <StudyEomunhoe 
      :searched_item="searched_item" 
      :searchby_active="searchby_active" 
      :show_searchresult="show_searchresult"
      :show_searchinfo="show_searchinfo"
      :sortby_active="sortby_active"
      :filter_active_chinalev="filter_active_chinalev"
      :filter_active_readlev="filter_active_readlev"
      :filter_active_writelev="filter_active_writelev"
      :checkbox_active="checkbox_active"
      :toggle_active="toggle_active"
      @emitted_searchresult="handle_emitted_searcheomunhoe" />
  </div>
</template>

<script>

import SearchOption from '../SearchOption.vue'
import StudyEomunhoe from '../StudyEomunhoe.vue'
export default {
  name: 'StudyPage',
  components: {
    SearchOption,
    StudyEomunhoe
  },
  data() {
    return {
      searched_item:'',
      searchby_active:[],
      
      sortby_active: [],
      filter_active_chinalev: [],
      filter_active_readlev: ['읽기8급'],
      filter_active_writelev: [],
      checkbox_active: '',
      toggle_active: false,
      
      selected_item:{},
      
      show_searchresult:true,
      show_searchinfo: false,
    };
  },
  methods: {
    handle_emitted_searchoption({sortby_active, filter_active_chinalev,filter_active_readlev, filter_active_writelev, checkbox_active, toggle_active}){
      this.sortby_active=sortby_active,
      this.filter_active_chinalev=filter_active_chinalev,
      this.filter_active_readlev=filter_active_readlev,
      this.filter_active_writelev=filter_active_writelev,
      this.checkbox_active=checkbox_active,
      this.toggle_active=toggle_active
    },
    handle_emitted_searcheomunhoe({selected_item}){
      this.selected_item=selected_item
      this.show_searchresult=false
      this.show_searchinfo=true
    },
  }
}
</script>
