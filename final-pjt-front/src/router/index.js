import Vue from 'vue'
import VueRouter from 'vue-router'
import ProfileView from '@/views/ProfileView'
import ProfileChangeView from '@/views/ProfileChangeView'
import SignUpView from '@/views/SignUpView'
import LogInView from '@/views/LogInView'
import MovieView from '@/views/MovieView'
import MovieDetailView from '@/views/MovieDetailView'
import MainView from '@/views/MainView'
import GenreView from '@/views/GenreView'
import SearchView from '@/views/SearchView'
import CinemaView from '@/views/CinemaView'


Vue.use(VueRouter)

const routes = [
  {
    path: '/main',
    name: 'MainView',
    component: MainView,
  },
  {
    path: '/cinema',
    name: 'CinemaView',
    component: CinemaView,
  },
  {
    path: '/profile/:username',
    name: 'ProfileView',
    component: ProfileView
  },
  {
    path: '/search',
    name: 'SearchView',
    component: SearchView,
  },
  {
    path: '/signup',
    name: 'SignUpView',
    component: SignUpView
  },

  {
    path: '/login',
    name: 'LogInView',
    component: LogInView
  },
  {
    path: '/movies',
    name: 'MovieView',
    component: MovieView,
  },
  {
    path: '/genres',
    name: 'GenreView',
    component: GenreView,
  },
  {
    path: '/movies/detail/:movieId',
    name: 'MovieDetailView',
    component: MovieDetailView,
  },

  {
    path: '/profile/:username/change',
    name: 'ProfileChangeView',
    component: ProfileChangeView,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  scrollBehavior() { 
    return { x: 0, y: 0 } 
  },
})


export default router
