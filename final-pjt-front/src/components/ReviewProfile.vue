<template>
  <div class="profile_review_container" v-if="(limit-1) * 2<= index && index < limit * 2">
    <!-- <h1>{{ review['serializer'].title }}</h1> -->
    <!-- <p>{{ review['movie_title'] }}</p>
    <p>{{ moment(review['serializer'].created_at).format("YYYY-MM-DD hh:mm:ss") }}</p> -->
    

    <div>
        <div no-body class="overflow-hidden" style="margin: auto; width: 800px; height:283px;  background-color: #212529;">
            <b-row no-gutters>
                
            <div style="padding-left: 0px; width:200px; ">
                <router-link :to="{name: 'MovieDetailView', params: {movieId: this.review['serializer']?.movie}}">
                <img style="margin: 0px; " :src="imgSrc" alt="" onerror="this.style.display='none'" id="img">
                </router-link>
            </div>
            <b-col>
                <h3 style="text-align: left; margin-left: 60px; margin-bottom:5px;">{{ review['serializer'].title }}</h3>
                <p style="font-size: 13px; text-align: left; margin-bottom: 0px; margin-left: 60px; margin-right: 50px;">⭐{{ review['serializer'].rank }} <span style="color: gray; font-size: 12px; margin-left: 7px;">📝{{ moment(review['serializer'].created_at).format("YYYY-MM-DD hh:mm:ss") }}</span></p>
                <hr style="width:450px; text-align: left; margin-left: 75px; margin-top:0px;">
                <div style=" text-align: left; margin-left: 60px; margin-right: 50px; ">
                    {{ review['serializer'].content }}
                </div>
                
            </b-col>
            </b-row>
            
        </div>
       
    </div>
    <hr style="margin-bottom: 0px;">
  </div>

</template>

<script>
import moment from "moment"

export default {
  name: 'ReviewProfile',
  props: {
    review: Object,
    index: Number,
    limit: Number,
  },
  data() {
        return {
            moment: moment
        }
    },
    computed: {
    imgSrc() {
        const Url = `https://www.themoviedb.org/t/p/w500/${this.review['movie_poster_path']}`
        // console.log(this.movie)
        // console.log(this.review['serializer']?.movie)
        return Url
    },
    reviewTitle() {
        return this.review['serializer'].title
    },
    },
    
}
</script>

<style>
.profile_review_container {
    width: 1200px;
    margin-top: 20px;
    margin-bottom: 20px;
}
</style>