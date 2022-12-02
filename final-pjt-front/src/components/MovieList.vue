<template>
  <div class="movie_container" style="cursor:pointer" @click="getHistory" v-if="index < limit">
      <a class="item" >
      <img :src="imgSrc" onerror="this.style.display='none'" id="img">
      </a>
  </div>
</template>

<script>

import axios from 'axios'
const API_URL = "http://127.0.0.1:8000"

export default {
  name: 'MovieList',
  props: {
    movie: Object,
    index: Number,
    limit: Number, 
  },
  computed: {
    imgSrc() {
        const Url = `https://www.themoviedb.org/t/p/w500/${this.movie.poster_path}`
        // console.log(this.movie)
        return Url
    }
  },
  methods: {
    getHistory() {
      if (this.$store.state.token === null) {
        alert('로그인이 필요한 서비스입니다')
        this.$router.push({ name: 'LogInView'})
      } else {
      axios({
        method: 'post',
        url:`${API_URL}/api/v1/movies/history/${this.movie?.movie_id}/`,
        headers: { 
            Authorization: `Token ${this.$store.state.token}`
        }
      })
      .then(() => {
        // console.log(this.movie.id)
        this.$router.push({ name : 'MovieDetailView', params: {movieId: this.movie.id} })
      })
      .catch((err) => {
        console.log(err)
      })
    }
    },
  }
}
</script>

<style>
.movie_container {
  display: flex;
  margin-top: 20px;
  margin-right:5px;
}

.item {
  z-index: -1;
  display: block;

  transition: transform 500ms;
}

.movie_container:hover .item {
  transform: scale(1.1);
}
</style>