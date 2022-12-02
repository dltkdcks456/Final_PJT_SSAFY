<template>
  <div class="content-container">
    <a style="cursor:pointer" @click="poster()"><img id="img-detail" :src="imgSrc" alt=""></a>
    <!-- <h2>{{ movie?.title }}</h2> -->
    <h5 style="margin-top: 8px;">📅{{ movie?.release_date }}</h5>
    <div style="justify-content:center; align-items:center;">
      <div class="overview">{{ movie?.overview }}</div>
    </div>
    <div class="genre_name">
      <span>🎬</span>
      <p style="margin-right: 15px; margin-bottom: 3px;" v-for="genreid in movie?.genres" :key="genreid">{{genreids[genreid]}}</p>
    </div>
    <div>
      TMDB 평점: ⭐{{ movie?.vote_average | toFixed(1) }}  /  10
    </div>
    <div v-if="this?.average_rank">
      WHAT FLIX 평점: ⭐ {{ this?.average_rank }}  /  5
    </div>
    <a v-if="this.actors[0]" class="a-detail" href="#" @click="actors_0()">{{ this.actors[0]?.name }}</a>
    <a v-if="this.actors[1]" class="a-detail" href="#" @click="actors_1()">{{ this.actors[1]?.name }}</a>
    <a v-if="this.actors[2]" class="a-detail" href="#" @click="actors_2()">{{ this.actors[2]?.name }}</a>
    <a v-if="this.actors[3]" class="a-detail" href="#" @click="actors_3()">{{ this.actors[3]?.name }}</a>
    <a v-if="this.directing[0]" class="a-detail" href="#" @click="directing_0()">🎥 {{ this.directing[0]?.name }}</a>
    <div style="display:flex; justify-content:center; align-itmes:center; margin-top:5px; margin-bottom: 5px;">
      <ProviderMovie
      v-for="provider in this.providers"
      :key="provider.id"
      :provider="provider"
      />
    </div>
    <h5 style="text-align: left; margin-top:5px; margin-left:15px;">포스터</h5>
    <div class="poster">
      <PostersMovie
      v-for="poster in this.posters"
      :key="poster.id"
      :poster="poster"
      style="margin-right: 8px; margin-bottom: 5px;"
      />
    </div>
  </div>
</template>

<script>

import PostersMovie from '@/components/PostersMovie'
import ProviderMovie from '@/components/ProviderMovie'

export default {
  name: 'SideContent',
  components: {
    PostersMovie,
    ProviderMovie,
  },
  data() {
    return {
      genreids: this.$store.state.genres,
      
    }
  },
  props: {
    movie: Object,
    actors: Array,
    directing: Array,
    posters: Array,
    average_rank: Number,
    providers: Array,
  },
  computed: {
    imgSrc () {
        const Url = `https://www.themoviedb.org/t/p/original/${this.movie?.poster_path}`
        return Url
    },
  },
  methods: {
    poster() {
      window.open(this.imgSrc)
    },
    actors_0() {
      window.open(this.actors[0]?.credit_id)
    },
    actors_1() {
      window.open(this.actors[1]?.credit_id)
    },
    actors_2() {
      window.open(this.actors[2]?.credit_id)
    },
    actors_3() {
      window.open(this.actors[3]?.credit_id)
    },
    directing_0() {
      window.open(this.directing[0]?.credit_id)
    },
  },
  filters: {
    toFixed: function(val, num) {
      return parseFloat(val).toFixed(num);
    },
  },
}
</script>

<style>
.a-detail:link, .a-detail:visited {
    background-color: #3c3850;
    color: #EAEAEA;
    padding: 5px 10px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 12px;
    margin: 3px;
    border-radius: 5px;
}

.a-detail:hover, a:active {
    background-color: #141212;
}

.poster {
  display:flex;
  justify-content: center;
  align-items:center;
  margin: 7px;
  flex-wrap: wrap;
}

#img-detail{
  width:300px;
}

.content-container {
  width: 600px;
}

.genre_name {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.overview {
  width: 450px;
  text-align: left;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5px;
  margin-bottom: 5px;

}
</style>