<template>
  <div id="movie_container" style="cursor:pointer" @click="getHistory">
    <a class="item">
      <img :src="imgSrc" alt="" id="img" onerror="this.style.display='none'">
    </a>
  </div>
</template>

<script>
import axios from 'axios'
const API_URL = "http://127.0.0.1:8000"

export default {
  name: 'GenreMovieList',
  props: {
    movie: Object,
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
#img {
    width: 200px;
    height: 284.8px;
  padding: 0;
  border-radius: 15px;
  margin: 5px;
}

#movie_container {
  display: flex;
  margin-top: 20px;
  margin-right:5px;
  height:230px;
}

#movie_container:hover .item {
  transform: scale(1.1);
}
</style>