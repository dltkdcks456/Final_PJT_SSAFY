<template>
  <div>
    <div class="list-container">
      <div v-if="recommendMovies.length > 0" class="main-text">
        <h1>당신을 위한 영화</h1>
      </div>
      <div v-if="recommendMovies.length > 0" class="list-card">
        <LikeToRecommend
        v-for="(movie,index) in recommendMovies"
        :key="index"
        :movie="movie"
        />
      </div>
      <hr v-if="recommendMovies.length > 0">
    </div>
    
    <div class="list-container">
      <div v-if="followMovies.length > 0" class="main-text">
        <h1>팔로우의 선택</h1>
      </div>
      <div v-if="followMovies.length > 0" class="list-card">
        <FollowLikeMovies
        v-for="movie in followMovies"
        :key="movie.id"
        :movie="movie"
        />
      </div>
      <hr v-if="followMovies.length > 0" >
    </div>

    <div class="list-container">
      <div v-if="trendMovies.length > 0" class="main-text">
        <h1>WHAT FLIX HOT MOVIE</h1>
      </div>
      <div v-if="trendMovies.length > 0" class="list-card">
        <LikeToRecommend
        v-for="movie in trendMovies"
        :key="`s-${movie?.id}`"
        :movie="movie"
        />
      </div>
    </div>
    <hr>
    <div class="list-container">
      <div class="main-text">
        <h1>현재 상영작</h1>
      </div>
      <div class="list-card">
        <UpcomingMovie
        v-for="movie in upcomingMovies"
        :key="`a-${movie?.id}`"
        :movie="movie"
        />
      </div>
    </div>
    <hr>
      <div class="list-container">
        <div class="main-text">
          <h1>전체 영화</h1>
        </div>
        <div class="list-card">
          <MovieList
            v-for="movie in movies_infinite"
            :key="`b-${movie?.id}`"
            :movie="movie"
          />
        </div>
        </div>
        <infinite-loading spinner="waveDots" id="movie" @infinite="infiniteHandler">
        </infinite-loading>  
  </div>
</template>

<script>
import MovieList from '@/components/MovieList.vue'
import UpcomingMovie from '@/components/UpcomingMovie.vue'
import LikeToRecommend from '@/components/LikeToRecommend.vue'
import InfiniteLoading from 'vue-infinite-loading'
import FollowLikeMovies from '@/components/FollowLikeMovies.vue'
import axios from 'axios'

const API_URL = "http://127.0.0.1:8000"

export default {
  name: 'MovieView',
  components: {
    MovieList,
    UpcomingMovie,
    LikeToRecommend,
    InfiniteLoading,
    FollowLikeMovies,
  },
  data() {
    return {
      page: -1,
      isLoading: 0,
      movies_infinite: []
    }
  },
  computed: {
    cnt() {
      return this.$store.state.cnt
    },
    movies() {
        return this.$store.state.movies
    },
    upcomingMovies() {
      return this.$store.state.upcomingMovies
    },
    recommendMovies() {
      return this.$store.state.recommendMovies
    },
    trendMovies() {
      return this.$store.state.trendMovies
    },
    followMovies() {
      return this.$store.state.followMovies
    }
  },
  created() {
    this.getMovies()
    this.getUpcomingMovie()
    this.LikeToRecommend()
    this.TrendMovies()
    this.getFollowMovies()
  },
  methods: {
    getFollowMovies() {
      this.$store.dispatch('getFollowMovies')
    },
    getMovies() {
       if (this.cnt === 0) {
         this.$store.dispatch('getMovies')
         this.$store.commit('RESET_MOVIES')
       } else {
        this.$store.commit('RESET_MOVIES')
       }
    },
    getUpcomingMovie() {
        this.$store.dispatch('getUpcomingMovie')
    },
    LikeToRecommend() {
      this.$store.dispatch('likeToRecommend')
    },
    TrendMovies() {
      this.$store.dispatch('trendMovies')
    },
    infiniteHandler($state) {
      this.page += 1
      axios({
        method: 'GET',
        url: `${API_URL}/api/v1/movies/list/${this.page}/`
      })
      .then((res) => {
        // console.log(res.data)
        // console.log(res.data.length)
        setTimeout(() => {
          if (res.data.length > 0) {
            res.data.forEach((movie) => {
              this.movies_infinite.push(movie)
            })
            // console.log(this.movies_infinite)
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
    // infiniteHandler($state) {
    //   if (this.limit < this.$store.state.movies.length) {
    //     setTimeout(this.limit += 30, 2000)
    //     $state.loaded()
    //   } else {
    //     $state.complete()
    //   }
    // }
  },  
}
</script>

<style>
  .list-container {
    width: 1200px;
    /* display: flex; */
    
}
.list-card{
      display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.main-text {
text-align: left; 
margin-left: 68px;
}
</style>
