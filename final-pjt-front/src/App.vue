<template>
  <div  id="app" >
    <div  style="position: fixed; width:100%; top:0px; left:0px; right:0px;">
      <b-navbar  type="dark" variant="dark" style="padding:20px; margin:0px; width:100%">
        <a href="" @click="goToMain"> <img src="./assets/logo.png" alt=""></a>
        <b-navbar-nav >
          <b-nav-item-dropdown style="cursor:pointer" text="Main" right>
            <b-dropdown-item style="cursor:pointer" @click="goToMovie">Movie</b-dropdown-item>
            <b-dropdown-item style="cursor:pointer" @click="goToGenre">Genre</b-dropdown-item>
            <b-dropdown-item style="cursor:pointer" @click="goToCinema">Cinema</b-dropdown-item>
          </b-nav-item-dropdown>
    
          <b-nav-item-dropdown v-if="token" style="cursor:pointer" text="Profile" right>
            <b-dropdown-item style="cursor:pointer" @click="goToProfileView">Profile</b-dropdown-item>
            <div>
              <b-dropdown-item @click="$bvModal.show('modal-logout')">로그아웃</b-dropdown-item>

              <b-modal id="modal-logout">
                <!-- 헤더 -->
                <template #modal-header>
                  <h3>로그아웃</h3>
                </template>
                <!-- 바디 -->
                <template #default>
                  <br>
                  <h5>로그아웃 하시겠습니까?</h5>
                  <br>
                </template>
                <!-- 풋터 -->
                <template #modal-footer="{cancel}">
                  <b-button size="m" variant="danger" @click="logOut()">
                    로그아웃
                  </b-button>
                  <b-button size="m" variant="dark" @click="cancel()">
                    취소
                  </b-button>
                </template>

              </b-modal>
            </div>
            <b-dropdown-item style="cursor:pointer" @click="goToProfileChangeView" >정보 변경</b-dropdown-item>
          </b-nav-item-dropdown>

          <!-- <b-nav-item v-if="token" style="cursor:pointer" @click="goToProfileView">Profile</b-nav-item> -->
          <b-nav-item v-if="!token" style="cursor:pointer" @click="goToSignUpView">Sign up</b-nav-item>
          <b-nav-item v-if="!token" style="cursor:pointer" @click="goToLogInView">Login</b-nav-item>
          <span @click="GoToSearch" style="color: #FFFFFF8C; font-size: 20px; cursor:pointer;  margin-top:5px; margin-left: 15px;;"><i style="color: #FFFFFF8C; font-size: 25px;" class="fa-solid fa-magnifying-glass"></i></span>
      </b-navbar-nav>
    </b-navbar>
  </div>


    <!-- <nav>
      
      <router-link v-if="token" :to="{ name: 'ProfileView', params: {username : myName} }">Profile</router-link>
      <router-link v-if="!token" :to="{ name: 'SignUpView' }">| SignUpPage</router-link>
      <router-link v-if="!token" :to="{ name: 'LogInView' }">| LogInPage</router-link>
    </nav> -->
    <div id="total-container">
    <router-view
    :key="$route.fullPath"
    />
    </div>
    <footer style="color: #BDBDBD;">
      <hr>
      <p style="margin:0px;">© 2022 Project from SSAFY</p>
      <p style="margin:0px;">junsoo & sangchan Company</p>
    </footer>
</div>

</template>

<script>
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'

export default {
  name: 'app',
  created() {
    this.getGenre()
    this.startPage()
  },
  beforeUpdate() {
    this.myId()
  },
  data() {
    return {
      myName: null,
    }
  },
  computed: {
    token() {
      return this.$store.state.token
    },
    img() {
      return this.$store.state.image.file_path

    }
  },
  methods: {
    startPage() {
      this.$router.push({name: 'MainView'}).catch(() =>{})
    },
    myId() {
      axios({
        method: 'get',
        url: `${API_URL}/user/`,
        headers: { 
          Authorization: `Token ${this.$store.state.token}`
        },
        })
        .then((res) => {
          this.myName = res.data.username
        })
        .catch((err) => {
          console.log(err)
      })
    },
    getGenre() {
      this.$store.dispatch('getGenres')
    },
    GoToSearch() {
      this.$router.push({name: 'SearchView' }).catch(() =>{})
    },
    goToCinema() {
      this.$router.push({name: 'CinemaView'}).catch(() =>{})
    },
    goToMain() {
      this.$router.push({name: 'MovieView' }).catch(() =>{})
    },
    goToProfileView() {
      this.$router.push({ name: 'ProfileView', params: {username : this.myName} }).catch(() =>{})
    },
    goToSignUpView() {
      this.$router.push({name: 'SignUpView' }).catch(() =>{})
    },
    goToLogInView() {
      this.$router.push({name: 'LogInView' }).catch(() =>{})
    },
    goToMovie() {
      this.$router.push({name: 'MovieView' }).catch(() =>{})
    },
    goToGenre() {
      this.$router.push({name: 'GenreView' }).catch(() =>{})
    },
    goToProfileChangeView() {
      this.$router.push({name: 'ProfileChangeView' }).catch(() =>{})
    },
    logOut() {
      this.$store.dispatch('logOut')
      this.$cookies.remove("csrftoken")
    },
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin:0px;
  height: 100%;
}

nav {
  padding: 70px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
.background{
  border:0;
  padding:0;
  margin:0;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  min-height: 100%;
}

#total-container {
  margin-right: auto;
  margin-left: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #EAEAEA;
  margin-top: 100px;
  /* font-family: 'Courier New', Courier, monospace; */
/* font-family: Helvetica, Arial, sans-serif; */
/* background-color: #212529; */
}



</style>
