<template>
  <div class="detail-container">
    <!-- <div v-if="isLoading" class="loading-container">
      <div class="loading">
        <Fade-loader />
      </div>
    </div> -->
    <LoadingSpinner v-if="isLoading"></LoadingSpinner>
    <ul v-else>
    <div class="head">
      <div style="margin-right:25px;">
      <div v-if="!this?.liked">
      <img id="img_like" style="cursor:pointer;"  @click="movieLike" src="../assets/before_like_red.png" >
      <!-- <button  @click="movieLike" >좋아요</button> -->
      </div>
      <div v-else>
      <img id="img_like" style="cursor:pointer;"  @click="movieLike" src="../assets/like_red_full.png" >
      <!-- <button @click="movieLike">좋아요 취소</button> -->
      </div>
      </div>
      <h1>{{ movie?.title }}</h1>
    </div>
    <hr class="hr_main">
    <div >
      <div class="movie-detail-container">
    <SideContent
    :movie="movie"
    :actors="actors"
    :directing="directing"
    :posters="posters"
    :average_rank="average_rank"
    :providers="providers"
    />
    <div>
      <VideoContent
      :movieVideo="movie?.video_path"
      />
      <h3 style="text-align: left; margin-left: 80px; margin-top: 15px;">관련 추천 영화</h3>
      <div class="list-card">
      <RelatedMovieVue
      v-for="(movie, idx) in relateMovies"
      :key="`qqsda-${idx}`"
      :movie="movie"
      />
      </div>
    </div>
  </div>
  <div>
    좋아요
    <div v-if="!this?.liked">
    <img id="img_like" style="cursor:pointer;"  @click="movieLike" src="../assets/before_like_red.png" alt="">
    <!-- <button  @click="movieLike" >좋아요</button> -->
    </div>
    <div v-else>
    <img id="img_like" style="cursor:pointer;"  @click="movieLike" src="../assets/like_red_full.png" alt="">
    <!-- <button @click="movieLike">좋아요 취소</button> -->
    </div>
  </div>
    <ReviewForm
    :movie="movie"
    @review-create="getReviewList"
    />
    <br>
  <div>
    <button class="btn btn-primary" style="width: 550px; margin-bottom: 15px;" v-if="!reviewCurtain" @click="Curtain">리뷰 보러 가기 🔍</button>
    <button class="btn btn-primary" style="width: 550px; margin-bottom: 15px;" v-if="reviewCurtain" @click="Curtain">리뷰 숨기기</button>
  </div>
  
  <div>
    <div v-if="reviewCurtain" style="display:flex; justify-content: center; flex-direction: column; align-items: center;">
      <ReviewList
      v-for="(review, index) in reviews"
      :key="`ss-${review?.id}`"
      :review="review"
      :index="index"
      :limit="reviewsCurrentPage"
      @delete-review="getReviewList"
      @update-review="getReviewList"
      />
      <div v-if="reviews" class="mt-3">
        <b-pagination
        v-model="reviewsCurrentPage"
        :total-rows="reviews.length"
        :per-page="10"
        ></b-pagination>  
      </div>
    </div>
  </div>
  </div>
  </ul>
</div>
</template>

<script>
import axios from 'axios'
import SideContent from '@/components/SideContent.vue'
import VideoContent from '@/components/VideoContent.vue'
import ReviewForm from '@/components/ReviewForm.vue'
import ReviewList from '@/components/ReviewList.vue'
import RelatedMovieVue from '@/components/RelatedMovie.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
// import FadeLoader from 'vue-spinner/src/FadeLoader.vue'

const API_URL = "http://127.0.0.1:8000"

export default {
  name: 'MovieDetailView',
  beforeMount() {
      if (this.isLogin === false) {
        alert('로그인이 필요한 서비스입니다')
        this.$router.push({ name: 'LogInView'})
      } 
    },

  data() {
    return {
      movie: null,
      reviews: null,
      liked: false,
      reviewCurtain: false,
      actors: [],
      directing: [],
      posters: [],
      average_rank: null,
      reviewsCurrentPage: 1,
      providers: [],
      isLoading: false,
    }
  },
  components: {
    SideContent,
    VideoContent,
    ReviewForm,
    ReviewList,
    RelatedMovieVue,
    LoadingSpinner,
    // FadeLoader,
  },
  created() {
    this.getMovieDetail()
  },
  computed:{
    isLogin() {
      return this.$store.getters.isLogin
    },
    relateMovies() {
      return this.$store.state?.relatedMovies
    }
  },
  methods: {
    relatedMovies() {
      this.$store.dispatch('relatedMovies', this.movie?.movie_id)
    },
    getPoster() {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/poster/${this.movie?.movie_id}`
      })
      .then((res) => {
        this.posters = res.data
      })
      .catch((err) => {
        console.log(err)
      })
    },
    getMovieDetail() {
      this.isLoading = true
      axios( {
        method: 'get',
        url: `${API_URL}/api/v1/movies/${this.$route.params?.movieId}`,
        headers: { 
          Authorization: `Token ${this.$store.state?.token}`
        }
      })
      .then((res) => {
          this.movie = res.data
      })
      .then(() => {
        this.getMovieLike()
      })
      .then(() => {
        this.getCasts()
      })
      .then(() => {
        this.getPoster()
      })
      .then(() => {
        this.relatedMovies()
      })
      .then(() => {
        this.getReviewList()
      })
      .then(() => {
        this.getProvider()
      })
      .then(() => {
        this.isLoading = false
      })
      .catch(() => {
        this.isLoading = false
      })
    },
    getProvider() {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/provieder/${this.movie?.id}/`,
      })
      .then((res) => {
        this.providers = res.data

      })
      .catch((err) => {
        console.log(err)
      })
    },
    getReviewList() {
      axios({
        method: 'get',
        url: `${API_URL}/community/reviews/${this.$route.params?.movieId}/`,
        headers: { 
          Authorization: `Token ${this.$store.state?.token}`
        }
      })
      .then((res) => {
        this.reviews = res.data['serializer']
        this.average_rank = res.data['average_rank']
      })
      .catch(() => {
        console.log('게시글이 존재하지 않습니다.')
        this.reviews = null
      })
    },
    getMovieLike() {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/like/${this.movie?.id}/`,
        headers: { 
          Authorization: `Token ${this.$store.state?.token}`
        }
      })
      .then((res) => {
        this.liked = res['data']['liked']
      })
      .catch(() => {
      })
    },
    movieLike () {
      axios({
        method: 'post',
        url: `${API_URL}/api/v1/movies/like/${this?.movie.id}/`,
        headers: { 
          Authorization: `Token ${this.$store.state?.token}`
        }
      })
      .then((res) => {
        if (res.data['liked']) {
          this.liked = true
          this.getHistory()
        } else {
          this.liked = false
        }
      })
      .catch(() => {
      })
    },
    Curtain() {
      this.reviewCurtain = !this.reviewCurtain
    },
    getHistory() {
      axios({
        method: 'post',
        url:`${API_URL}/api/v1/movies/history/${this.movie?.movie_id}/`,
        headers: { 
            Authorization: `Token ${this.$store.state.token}`
        }
      })
      .then(() => {
        // this.$router.push({ name : 'MovieDetailView', params: {movieId: this.movie.id} })
      })
      .catch(() => {
      })
    },
    getCasts() {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/casts/${this.movie.movie_id}/`
      })
      .then((res) => {
        const casts = res.data
        const actors = casts.filter((cast) => {
          return cast.known_for_department === "Acting"
        })
        const directing = casts.filter((cast) => {
          return cast.known_for_department === "Directing"
        })
        this.actors = actors
        this.directing = directing
      })
      .catch(() => {
      })
    }
  
}
}
</script>

<style>
.movie-detail-container {
  display: flex;
}

.detail-container {
  width: 1240px;
}

#img_like {
  width: 50px;
  /* height: 150px; */
  object-fit: cover;
}

.list-card{
      display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.head{
  display: flex;
}

.hr_main{
  height: 2.5px;
  background-color: #EAEAEA;
}

.loading {
  z-index: 1000 !important;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow: rgba(0, 0, 0, 0.1) 0 0 0 9999px;
}
</style>