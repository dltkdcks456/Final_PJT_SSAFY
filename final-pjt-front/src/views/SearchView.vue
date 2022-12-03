<template>
  <div >
    <form  >
        <div style="display: flex; justify-content: center; align-items: center;">
            <div style=" width: 400px;">
              <input class="form-control" type="text" @input="SearchData" placeholder="제목, 배우명(영문) 검색">
              </div>
              <div>
              
            </div>
        </div>
    </form>
    <LoadingSpinner v-if="isLoading"></LoadingSpinner>
    <ul v-else>
      <div v-if="searchMovies.length===0" style="height:295px;"></div>
      <div class="search-container">
        <SearchMovie
        v-for="movie in searchMovies"
        :key="`s-${movie.id}`"
        :movie="movie"
        />
      </div>
    </ul>
  </div>
</template>

<script>
import SearchMovie from '@/components/SearchMovie.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'

export default {
  name: 'SearchView',
  data() {
    return {
        searchMovies: [],
        currentData: null,
        isLoading: false,
    }
  },
  components: {
    SearchMovie,
    LoadingSpinner,
  },
  methods: {
    SearchData(e) {
      //뭔가를 걸어준다.시간 지연 -> 최적화 필요//
      //동작이 매끄럽지 않고 버그가 생길 수 있음//
      
      const inputData = e.target.value
      this.currentData = e.target.value

      //입력이 없을 경우 로딩 버튼이 생기지 않게 설정//
      if (inputData.length === 0) {
        this.isLoading = false
        this.searchMovies = []
      } else {
        // 입력 후 2500ms의 간격을 주고 검색을 진행//
        // 현재 입력값과 찾을 입력값이 다르면 진행 하지 않는다(고객이 계속 입력 중이라는 의미) //
        setTimeout(() => {
          if (inputData === this.currentData) {
            this.isLoading = true
            axios({
              method: 'get',
              url: `${API_URL}/api/v1/movies/search/${inputData}/`
          })
          .then((res) => {
            // 이전에 요청한 데이터가 뒤늦게 화면에 출력될 경우가 있음//
            // 예전의 입력값이 현재의 입력값과 같으면 화면에 출력하고, 그렇지 않으면 바로 return할 수 있게 하면서 뒤늦게 출력되는 것을 방지//
            if (inputData === this.currentData) {
              this.searchMovies = res.data
              this.isLoading = false
            } else {
              return
            }
          })
          .catch(() => {
              this.searchMovies = []
          })
          } else {
            return
          }
        }, 2500)
      }
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