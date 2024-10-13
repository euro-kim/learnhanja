<template>
    <div>
      <!-- Display paginated items -->
      <ul>
        <li v-for="(item, index) in paginatedItems" :key="index">{{ item.kr }}</li>
      </ul>
  
      <!-- Pagination buttons -->
      <div>
        <button 
          v-for="page in totalPages" 
          :key="page" 
          @click="currentPage = page"
          :class="{ active: page === currentPage }"
        >
          {{ page }}
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import data from '../data/hanja.json'; // Import your JSON file
  
  export default {
    data() {
      return {
        items: data,       // Load data from JSON
        currentPage: 1,    // Track the current page
        itemsPerPage: 100, // Number of items per page
      };
    },
    computed: {
      // Calculate total pages based on number of items
      totalPages() {
        return Math.ceil(this.items.length / this.itemsPerPage);
      },
      // Return items for the current page
      paginatedItems() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.items.slice(start, end);
      }
    }
  };
  </script>
  

  