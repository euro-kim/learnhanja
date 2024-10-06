<template>
    <div >
      <SearchBar @emitted_searchbar="handle_emitted_searchbar"/>
      <SearchOption 
        :show_searchresult="show_searchresult"
        @emitted_searchbar="handle_emitted_searchoption"/>
      <SearchResult 
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
        @emitted_searchresult="handle_emitted_searchresult" />
      <SearchInfo 
        :selected_item="selected_item" 
        :show_searchinfo="show_searchinfo"
        @emitted_searchinfo="handle_emitted_searchinfo"/>
      <SearchRelated 
        :selected_item="selected_item" 
        :show_searchinfo="show_searchinfo"
        :sortby_active="sortby_active"
        :filter_active_chinalev="filter_active_chinalev"
        :filter_active_readlev="filter_active_readlev"
        :filter_active_writelev="filter_active_writelev"
        :checkbox_active="checkbox_active"
        :toggle_active="toggle_active"
        @emitted_searchrelated="handle_emitted_searchrelated"/>
    </div>
  </template>
  
  <script>
  
  import SearchBar from '../components/SearchBar.vue'
  import SearchOption from '../components/SearchOption.vue'
  import SearchResult from '../components/SearchResult.vue'
  import SearchInfo from '../components/SearchInfo.vue'
  import SearchRelated from '../components/SearchRelated.vue'
  export default {
    name: 'SearchPage',
    components: {
      SearchBar,
      SearchOption,
      SearchResult,
      SearchInfo,
      SearchRelated
    },
    data() {
      return {
        searched_item:'',
        searchby_active:[],
        
        sortby_active: [],
        filter_active_chinalev: [],
        filter_active_readlev: [],
        filter_active_writelev: [],
        checkbox_active: '',
        toggle_active: false,
        
        selected_item:{},
        
        show_searchresult:false,
        show_searchinfo: false,
      };
    },
    methods: {
      handle_emitted_searchbar({searched_item,searchby_active}){
        this.searched_item=searched_item
        this.searchby_active=searchby_active
        this.show_searchresult=true
        this.show_searchinfo=false
      },
      handle_emitted_searchoption({sortby_active, filter_active_chinalev,filter_active_readlev, filter_active_writelev, checkbox_active, toggle_active}){
        this.sortby_active=sortby_active,
        this.filter_active_chinalev=filter_active_chinalev,
        this.filter_active_readlev=filter_active_readlev,
        this.filter_active_writelev=filter_active_writelev,
        this.checkbox_active=checkbox_active,
        this.toggle_active=toggle_active
      },
      handle_emitted_searchresult({selected_item}){
        this.selected_item=selected_item
        this.show_searchresult=false
        this.show_searchinfo=true
      },
      handle_emitted_searchinfo({updated_selected_item}){
        this.selected_item=updated_selected_item
      },
      handle_emitted_searchrelated({updated_selected_item}){
        this.selected_item=updated_selected_item
      }

  
    }
  }
  </script>
 