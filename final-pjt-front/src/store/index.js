import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import createPersistedState from 'vuex-persistedstate'
import router from '@/router'

Vue.use(Vuex)


const API_URL = 'http://127.0.0.1:8000'


export default new Vuex.Store({
  plugins: [
    createPersistedState()
  ],
  state: {
    token: null,
    movies: [
    ],
    upcomingMovies: [
    ],
    genres:{
    },
    recommendMovies: [
    ],
    relatedMovies: [
    ],
    trendMovies: [
    ],
    followMovies: [
    ],
    cnt: 0,
  },
  getters: {
    isLogin(state) {
      return state.token ? true : false
    }
  },
  mutations: {
    // 회원가입 & 로그인
    SAVE_TOKEN(state, token) {
      state.token = token
      router.push({ name: 'MovieView' })
    },
    LOSE_TOKEN(state) {
      state.token = null
      router.push({ name: 'LogInView' })
    },
    PASSWORD_CHANGE(state, payload) {
      axios({
        method: 'post',
        url: `${API_URL}/password/change/`,
        data: {
          new_password1: payload.new_password1,
          new_password2: payload.new_password2,
          // old_password: payload.old_password,
        },
        headers: { 
          Authorization: `Token ${state.token}`
        },
        })
        .catch((err) => {
          console.log(err)
      })
    },
    LIKE_TO_RECOMMEND(state, movies) {
      state.recommendMovies = movies
    },
    RESET_MOVIES(state) {
      state.cnt += 1
      if (state.cnt === 10) {
        state.cnt = 0
      }
    },
    GET_MOVIES(state, movies) {
      state.movies = movies
    },
    GET_UPCOMING_MOVIES(state, movies) {
      state.upcomingMovies = movies
    },

    GET_GENRES(state, genre) {
      state.genres[genre['id']] = genre['name']
    },
    RELATED_MOVIES(state, movies) {
      state.relatedMovies = movies
    },
    GET_TREND_MOVIES(state, movies) {
      state.trendMovies = movies
    },
    GET_FOLLOW_MOVIES(state, movies) {
      state.followMovies = movies
    }
  },
  actions: {
    getFollowMovies(context) {
      if (context.state.token == null) {
        context.commit('GET_FOLLOW_MOVIES', [])
      } else {
      // user id 받기
      axios({
        method: 'get',
        url: `${API_URL}/user/`,
        headers: { 
          Authorization: `Token ${this.state.token}`
        },
        })
        .then((res) => {
          // user id 장고로 보내기
          const user_id = res.data.pk
          axios({
            method: 'get',
            url: `${API_URL}/api/v1/movies/follow/movies/${user_id}/`
          })
          .then((res) => {
            context.commit('GET_FOLLOW_MOVIES', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        })
        .catch((err) => {
          console.log(err)
      })
    }},
    getMovies(context) {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/`,
      })
      .then((res) => {
        context.commit('GET_MOVIES', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    relatedMovies(context, movie_id) {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/related/${movie_id}/`,
        headers: { 
          Authorization: `Token ${context.state.token}`
        },
      })
      .then((res) => {
        context.commit('RELATED_MOVIES', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    likeToRecommend(context) {
      if (context.state.token == null) {
        context.commit('LIKE_TO_RECOMMEND', [])
      } else {
        axios({
          method: 'get',
          url: `${API_URL}/api/v1/movies/likerecommend/`,
          headers: { 
            Authorization: `Token ${context.state.token}`
          },
        })
        .then((res) => {
          context.commit('LIKE_TO_RECOMMEND', res.data)
        })
        .catch((err) => {
          console.log(err)
        })
      }
    },
    trendMovies(context) {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/trend/`
      })
      .then((res) => {
        context.commit('GET_TREND_MOVIES', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    getUpcomingMovie(context) {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/upcoming/`
      })
      .then((res) => {
        context.commit('GET_UPCOMING_MOVIES', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    getGenres(context) {
      axios({
              method: 'get',
              url: `${API_URL}/api/v1/movies/genres/`
            })
      .then((res) => {
        for (const genre of res.data) {
          context.commit('GET_GENRES', genre)
        }
      })
      .catch((err) => {
        console.log('store 장르 받기 에러')
        console.log(err)
      })
    },

    signUp(context, payload) {
      axios({
        method: 'post',
        url: `${API_URL}/signup/`,
        data: {
          username: payload.username,
          password1: payload.password1,
          password2: payload.password2,         
        }
      })
        .then((res) => {
          // console.log(res)
          context.commit('SAVE_TOKEN', res.data.key)
        })
        .catch((err) => {
          console.log(err)
        })
    },
    logIn(context, payload) {
      axios({
        method: 'post',
        url: `${API_URL}/login/`,
        data: {
          username: payload.username,
          password: payload.password,
        }
      })
        .then((res) => {
          // console.log(res)
          context.commit('SAVE_TOKEN', res.data.key)
        })
        .catch((err) => {
          console.log(err)
        })
    },
    logOut(context) {
      axios({
        method: 'post',
        url: `${API_URL}/logout/`,
        })
        .then(() => {
          // console.log(res)
          context.commit('LOSE_TOKEN')
        })
        .catch((err) => {
          console.log(err)
      })
    },
    leave(context) {
      // console.log(context.state.username)
      axios({
        method: 'post',
        url: `${API_URL}/accounts/leave/`,
        headers: { 
          Authorization: `Token ${context.state.token}`
        },
        })
        .then(() => {
          // console.log(res)
          context.commit('LOSE_TOKEN')
        })
        .catch((err) => {
          console.log(err)
        })
    },
  },

})
