<template>
  <div >
    <form  >
        <div style="display: flex; justify-content: center; align-items: center;">
            <div style=" width: 400px;">
              <input class="form-control" type="text" @input="SearchData" placeholder="제목, 줄거리, 배우명(영문) 검색">
              </div>
              <div>
              
            </div>
        </div>
    </form>
    <div v-if="searchMovies.length===0" style="height:295px;"></div>
    <div class="search-container">
      <SearchMovie
      v-for="movie in searchMovies"
      :key="`s-${movie.id}`"
      :movie="movie"
      />
    </div>
  </div>
</template>

<script>
import SearchMovie from '@/components/SearchMovie.vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'

export default {
  name: 'SearchView',
  data() {
    return {
        searchMovies: [],
    }
  },
  components: {
    SearchMovie,
  },
  methods: {
    SearchData(e) {
      //뭔가를 걸어준다.시간 지연 -> 최적화 필요//
      //동작이 매끄럽지 않고 버그가 생길 수 있음//
        axios({
            method: 'get',
            url: `${API_URL}/api/v1/movies/search/${e.target.value}/`
        })
        .then((res) => {
            this.searchMovies = res.data
        })
        .catch(() => {
            this.searchMovies = []
        })
    }
  }
}
</script>

<style>
.search-container {
    width: 1200px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;;
}

.empty {
    margin: 500px;
}
</style>