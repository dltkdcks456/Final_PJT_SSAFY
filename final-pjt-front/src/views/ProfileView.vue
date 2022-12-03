<template>  
  <div>
    <div>
      <div class="profile-img-container">
        <img id="preview-image" v-show="imgSrc" :src="imgSrc" class="profile-img">
      </div>

      <div v-if="userName === myName || !userName" style="display:flex; justify-content: center;">
        <div class="filebox">
          <input style="display: none;" value="첨부파일" placeholder="첨부파일" id="profile-image" name="profile-image" multiple accept="image/*" type="file" @change="InputImage">
          <label class="input-file-button" for="profile-image">파일찾기</label>
        </div>
        <div>
          <button class="btn btn-danger mx-2" @click="SaveImage">프로필 적용</button>
        </div>
        <div>
          <button class="btn btn-danger" @click="deleteImage">초기화</button>
        </div>
      </div>
    </div>
    <h1 >{{userName}}의 Profile Page</h1>
    <div class="follow-container">
    <div >
      <div v-if="this.followings.length === 0" @click="getFollowingMembers" style="margin-right:15px;" v-b-toggle.sidebar-right>팔로잉 : 
        <span style="color:aquamarine;">{{followings_count}} 명</span></div>
      <div v-else style="margin-right:15px;" v-b-toggle.sidebar-right>팔로잉 : <span style="color:aquamarine;">{{followings_count}} 명</span></div>
      <b-sidebar id="sidebar-right" title="Following Member" right shadow>
        <div class="px-3 py-2">
          <FollowingMembers
          v-for="following in followings"
          :key="following.id"
          :following="following"
          />
          
        </div>
      </b-sidebar>
    </div>
    <div>
      <div v-if="this.followers.length === 0" @click="getFollowerMembers" v-b-toggle.sidebar-follower>팔로워 : <span style="color:aquamarine;">{{followers_count}} 명</span></div>
      <div v-else  v-b-toggle.sidebar-follower>팔로워 : <span style="color:aquamarine;">{{followers_count}} 명</span></div>
      <b-sidebar id="sidebar-follower" title="Follower Member" right shadow>
        <div class="px-3 py-2" >
          <FollowerMembers
          v-for="follower in followers"
          :key="follower.id"
          :follower="follower"
          />
        </div>
      </b-sidebar> 
    </div>
  </div>
    <hr>
    <div v-if="userName === myName || !userName">
      <!-- 나일 때 -->
      <b-button variant="danger" @click="$bvModal.show('modal-logout')" style="margin-right: 10px;">로그아웃</b-button>
      <button class="btn btn-danger" href="" @click="goToProfileChangeView" style="margin-left: 10px;">개인정보 수정</button>
    </div>
    <div v-else>
      <!-- 남일 때 -->
      <button v-if="!isFollowed" @click="follow" class="btn btn-danger">팔로우</button>
      <button v-if="isFollowed" @click="follow" class="btn btn-danger" >팔로우 취소</button>
    </div>
    <hr>
    <div id="list-container">
      <div v-if="likeMovieList.length > 0">
        <h1 v-if="userName !== myName || !userName">{{userName}}의 좋아요</h1>
        <h1 v-else>내가 좋아요 한 영화</h1>
      </div>
      <div v-else>
        <h1 style="margin-top: 40px;"> 좋아하는 영화가 없어요😥</h1>
      </div>
      
      <div id="list-container">
        <div class="list-card">
            <LikeMovieList
            v-for="(movie, index) in likeMovieList"
            :key="movie.id"
            :movie="movie"
            :index="index"
            :limit="likeMovieListCurrentPage"
            />
        </div>
        <div v-if="likeMovieList.length" class="mt-3">
          <b-pagination
            v-model="likeMovieListCurrentPage"
            :total-rows="likeMovieList.length"
            :per-page="12"
          ></b-pagination>  
        </div>
      </div>
      
      
      <hr>
    </div>
    <hr>
    <div id="list-container">
      <div v-if="this.reviewProfile.length > 0">
        <h1 v-if="userName !== myName || !userName">{{userName}}의 리뷰</h1>
        <h1 v-else>내가 남긴 리뷰</h1>
      </div>
      <div v-else>
        <h1 style="margin-top: 40px;">남긴 리뷰가 없어요😯</h1>
      </div>

      <div class="review_movie_list">
        <ReviewProfile
        v-for = "(review, index) in reviewProfile"
        :key="review.id"
        :review="review"
        :index="index"
        :limit="reviewProfileCurrentPage"
        />
        <div v-if="reviewProfile.length" class="mt-3">
          <b-pagination
            v-model="reviewProfileCurrentPage"
            :total-rows="reviewProfile.length"
            :per-page="2"
          ></b-pagination>  
        </div>
      <hr>
      </div>
      <hr>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import LikeMovieList from '@/components/LikeMovieList'
import ReviewProfile from '@/components/ReviewProfile'
import FollowingMembers from '@/components/FollowingMembers'
import FollowerMembers from '@/components/FollowerMembers'
import swal from 'sweetalert'


const API_URL = 'http://127.0.0.1:8000'
export default {
  name: 'ProfileView',
  beforeUpdate() {
    this.myId()
  },
  created() {
    this.getFollowed()
    this.likeMovies()
    this.ReviewProfile()
    if (this.isLogin === false) {
      alert('로그인이 필요한 서비스입니다')
      this.$router.push({ name: 'LogInView'})
    }
    this.getProfileImage()
  },
  data() {
    return {
      userName: this.$route.params.username,
      myName: null,
      isFollowed: false,
      followers_count: 0,
      followings_count: 0,
      likeMovieList: [],
      reviewProfile: [],
      followings: [],
      followers: [],
      likeMovieListCurrentPage: 1,
      reviewProfileCurrentPage: 1,
      image: '',
      profileImageUrl: '',
    }
  },
  components: {
    LikeMovieList,
    ReviewProfile,
    FollowingMembers,
    FollowerMembers,
  },
  computed:{
    isLogin() {
      return this.$store.getters.isLogin
    },
    imgSrc() {
      return this.profileImageUrl
    },
  },
  methods: {
    deleteImage() {
      axios({
        method: 'post',
            url: `${API_URL}/accounts/wantid/`,
            data: {
            username: this.userName
            },
            headers: { 
              Authorization: `Token ${this.$store.state.token}`
            },
      })
      .then((res) => {
        const id = res.data.userid
        axios({
        method: 'delete',
        url: `${API_URL}/accounts/profile_image/${id}/`,
        data: this.image,
        headers: { 
          'Content-Type': 'multipart/form-data',
              Authorization: `Token ${this.$store.state.token}`
            },
        })
        .then(() => {
          this.getProfileImage()
        })
        .then(() => {
          swal("초기화 완료!", "기본 이미지로 대체되었습니다", "info");
        })
        .catch((err) => {
          console.log(err)
        })
    })
    },
    getProfileImage() {
        axios({
        method: 'post',
            url: `${API_URL}/accounts/wantid/`,
            data: {
            username: this.userName
            },
            headers: { 
              Authorization: `Token ${this.$store.state.token}`
            },
      })
      .then((res) => {
        const id = res.data.userid
        axios({
        method: 'get',
        url: `${API_URL}/accounts/profile_image/${id}/`,
        data: this.image,
        headers: { 
          'Content-Type': 'multipart/form-data',
              Authorization: `Token ${this.$store.state.token}`
            },
        })
        .then((res) => {
          this.profileImageUrl=`${API_URL}${res.data.profile_image}`
        })
        .catch((err) => {
          console.log(err)
        })
        })
      .catch((err) => {
        console.log(err)
      })
    },
    SaveImage() {
      if (!this.image) {
        swal("파일 없음!", "파일을 업로드 해주세요!", "warning");
      } else {
        axios({
        method: 'post',
            url: `${API_URL}/accounts/wantid/`,
            data: {
            username: this.userName
            },
            headers: { 
              Authorization: `Token ${this.$store.state.token}`
            },
      })
      .then((res) => {
        const id = res.data.userid
        axios({
        method: 'post',
        url: `${API_URL}/accounts/profile_image/${id}/`,
        data: this.image,
        headers: { 
          'Content-Type': 'multipart/form-data',
              Authorization: `Token ${this.$store.state.token}`
            },
        })
        .then((res) => {
          this.profileImageUrl=`${API_URL}${res.data.profile_image}`
          swal("업로드 완료!", "프로필 편집이 완료되었습니다", "success");
        })
        .catch((err) => {
          console.log(err)
        })
        })
      .catch((err) => {
        console.log(err)
      })
      }
      
    },
    InputImage(e) {
      // console.log(e.target.files)
      const file = e.target.files[0]
      // let url = URL.createObjectURL(file[0])
      // this.image = url
      const fd = new FormData()
      fd.append('image', file)
      this.image = fd

      //미리보기
      const fileReader = new FileReader()
      // fileReader.readAsDataURL(file)
      fileReader.onload = function(e) {
        const previewImage = document.getElementById("preview-image")
        previewImage.src = e.target.result
      }
      fileReader.readAsDataURL(file)
    },
    goToProfileChangeView() {
      this.$router.push({name: 'ProfileChangeView' }).catch(() =>{})
    },
    getFollowingMembers() {
      axios({
        method: 'post',
            url: `${API_URL}/accounts/wantid/`,
            data: {
            username: this.userName
            },
            headers: { 
              Authorization: `Token ${this.$store.state.token}`
            },
      })
      .then((res) => {
              const id = res.data.userid
              axios({
                method: 'get',
                url: `${API_URL}/accounts/following/profile/${id}/`,
                headers: { 
                Authorization: `Token ${this.$store.state.token}`
                },
              })
              .then((res) => {
                this.followings = res.data
              })
              .catch(() => {})
            })
      .catch((err) => {
        console.log(err)
      })
    },
    getFollowerMembers() {
      axios({
        method: 'post',
            url: `${API_URL}/accounts/wantid/`,
            data: {
            username: this.userName
            },
            headers: { 
              Authorization: `Token ${this.$store.state.token}`
            },
      })
      .then((res) => {
              const id = res.data.userid
              axios({
                method: 'get',
                url: `${API_URL}/accounts/follower/profile/${id}/`,
                headers: { 
                Authorization: `Token ${this.$store.state.token}`
                },
              })
              .then((res) => {
                // console.log('응답 받았어요~!!!')
                // console.log(res.data)
                this.followers = res.data
              })
              .catch(() => {})
            })
      .catch((err) => {
        console.log(err)
      })
    },
    likeMovies() {
      axios({
        method: 'get',
        url: `${API_URL}/api/v1/movies/like/list/${this.userName}/`,
      })
      .then((res) => {
        this.likeMovieList = res.data
      })
      .catch((err) => {
        console.log(err)
      })
    },
    ReviewProfile() {
      axios({
            method: 'post',
            url: `${API_URL}/accounts/wantid/`,
            data: {
            username: this.userName
            },
            headers: { 
              Authorization: `Token ${this.$store.state.token}`
            },
            })
            .then((res) => {
              const id = res.data.userid
              axios({
                method: 'get',
                url: `${API_URL}/community/reviews/profile/${id}/`,
                headers: { 
                Authorization: `Token ${this.$store.state.token}`
                },
              })
              .then((res) => {
                // console.log(res.data)
                this.reviewProfile = res.data
              })
              .catch((err) => {
              console.log(err)
              })
            })
            .catch((err) => {
              console.log(err)
          })
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
    
    follow() {
      axios({
        method: 'post',
        url: `${API_URL}/accounts/wantid/`,
        data: {
            username: this.userName
        },
        headers: { 
          Authorization: `Token ${this.$store.state.token}`
        },
        })
        .then((res) => {
          // follow
          axios({
            method: 'post',
            url: `${API_URL}/accounts/follow/${res.data.userid}/`,
            headers: { 
              Authorization: `Token ${this.$store.state.token}`
            },
            })
            .then((res2) => {
              this.isFollowed = res2.data
              axios({
                  method: 'get',
                  url: `${API_URL}/accounts/followcount/${res.data.userid}`,
                })
                .then((res3) => {
                  this.followers_count = res3.data.followers_count
                  this.followings_count = res3.data.followings_count
                })
                .catch((err) => {
                  // console.log('followcount error')
                  console.log(err)
                })
            })
            .catch((err) => {
              // console.log('follow error')
              console.log(err)
            })
        })
        .catch((err) => {
          console.log(err)
        })
    },
    getFollowed() {
      axios({
        method: 'post',
        url: `${API_URL}/accounts/wantid/`,
        data: {
            username: this.userName
        },
        headers: { 
          Authorization: `Token ${this.$store.state.token}`
        },
        })
        .then((res) => {
          // getFollowed
          axios({
            method: 'get',
            url: `${API_URL}/accounts/follow/${res.data.userid}/`,
            headers: { 
              Authorization: `Token ${this.$store.state.token}`
            },
            })
            .then((res) => {
              this.isFollowed = res.data
            })
            .catch((err) => {
              console.log(err)
            })
          // followCount
          axios({
              method: 'get',
              url: `${API_URL}/accounts/followcount/${res.data.userid}`,
            })
            .then((res) => {
              this.followers_count = res.data.followers_count
              this.followings_count = res.data.followings_count
            })
            .catch((err) => {
              // console.log('followcount errer')
              console.log(err)
            })
        })
        .catch((err) => {
          console.log(err)
        })
    },
    
  },
}
</script>

<style>
  #list-container {
    margin-top: 15px;
    width: 1400px;
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
}
.movie_list {
  display: flex;
  justify-content: center;
}
.review_movie_list {
  display: flex;
  justify-content: center;
  width: 1200px;
  flex-wrap: wrap;
}
.follow-container {
  display:flex;
  justify-content: center;
}

.pagination{
  --bs-pagination-color: #ffffff !important;
  --bs-pagination-bg: none !important;
  --bs-pagination-border-color:#212529 !important;
  --bs-pagination-active-bg: none !important;
  --bs-pagination-active-border-color: #ffffff !important;
  --bs-pagination-disabled-color: none !important;
  --bs-pagination-disabled-bg: none !important;
  --bs-pagination-disabled-border-color: #212529 !important;
  --bs-pagination-hover-color: none !important;
  --bs-pagination-hover-bg: none !important;
  --bs-pagination-hover-border-color: #ffffff !important;
  --bs-pagination-focus-color: none !important;
  --bs-pagination-focus-bg: none !important;
}

.profile-img-container {
  display: flex;
  justify-content: center;
}

.profile-img{
  width: 180px;
  height: 180px;
  border-radius: 50%;
  object-fit: cover;
  margin: 15px;
}

.input-file-button{
  padding: 6px 25px;
  background-color:rgba(255, 255, 255, 0.877);
  border-radius: 4px;
  color: gray;
  cursor: pointer;
}
</style>