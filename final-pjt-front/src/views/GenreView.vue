<template>
  <div id="genre-container">
    <div id="select-form" style="width:100%">
      <form @submit.prevent="getMovies" style="display:flex; align-items:center;">
        <div>
          <select v-model="onePick" class="form-select form-select mb-3" style="margin-top:15px;">
            <option value=18>드라마</option>
            <option value=12>모험</option>
            <option value=14>판타지</option>
            <option value=16>애니메이션</option>
            <option value=27>공포</option>
            <option value=28>액션</option>
            <option value=35>코미디</option>
            <option value=36>역사</option>
            <option value=37>서부</option>
            <option value=53>스릴러</option>
            <option value=80>범죄</option>
            <option value=99>다큐멘터리</option>
            <option value=878>SF</option>
            <option value=9648>미스터리</option>
            <option value=10402	>음악</option>
            <option value=10749>로맨스</option>
            <option value=10751>가족</option>
            <option value=10752>전쟁</option>
            <option value=10770>TV 영화</option>
        </select>
      </div>
      <div>
        <input class= "btn btn-danger" style="margin-left:20px;" type="submit" value="영화 찾기"><br>
      </div>
      </form>
    </div>
    <div id="img-container">
      <div class="list-card">
        <GenreMovieList
          v-for="movie in selectMovie"
            :key="`kd-${movie.movie_id}`"
            :movie="movie"
          />
        </div>
      </div>
      <infinite-loading spinner="default" @infinite="infiniteHandler"></infinite-loading>  
      <div style="height:10px;"></div>

  </div>
</template>

<script>
import axios from 'axios'
import GenreMovieList from '@/components/GenreMovieList'
import InfiniteLoading from 'vue-infinite-loading'

const API_URL = "http://127.0.0.1:8000"

export default {
  name: 'GenreView',
  data() {
    return {
        onePick: 18,
        selectMovie: [],
        page: 0,
    }
  },
  components: { 
    GenreMovieList,
    InfiniteLoading,
  },
  created() {
    this.getMovies()
  },
  methods: {
    getMovies() {
      this.selectMovie = []
      const number = Number(this.onePick)
      axios({
        method:'get',
        url: `${API_URL}/api/v1/movies/genre/${number}/${this.page}/`
      })
      .then((res) => {
        res.data.forEach((movie) => {
          this.selectMovie.push(movie)
        })
      })
      .catch((err) => {
        console.log(err)
      })
    },
    infiniteHandler($state) {
      this.page += 1
      const number = Number(this.onePick)
      axios({
        method:'get',
        url: `${API_URL}/api/v1/movies/genre/${number}/${this.page}/`
      })
      .then((res) => {
        setTimeout(() => {
          if (res.data.length > 0) {
            res.data.forEach((movie) => {
            this.selectMovie.push(movie)
            })
            $state.loaded()
          } else {
            $state.complete()
          }
        }, 1000)
      })
      .catch((err) => {
        console.log(err)
      })
    },
  }
}
</script>

<style>
#img-container {
  display: flex;
  justify-content: center;
  /* align-items: center; */
  flex-wrap: wrap;
}

#select-form {
  display: flex;
  margin-left: 80px;
  margin-bottom: 70px;
  margin-right: 20px;
  justify-content: center;
  align-items: center;
}

#genre-container {
  width:1000px;
  display:flex;
  flex-wrap: wrap;
  flex-direction: column;
}

.submit-btn {
  margin-left: 20px;
}
</style>