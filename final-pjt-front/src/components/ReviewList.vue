<template>
  <div v-if="(limit-1)*10 <= index && index < limit*10" style="margin:50px;">
    <div v-if="!this.updateStatus" id="review_container">
      <h3 style="margin-top: 15px; margin-bottom: 10px; text-align: left; margin-left: 25px;">{{ review?.title }}</h3>
      <hr style="margin: 1px;">
      <div style="text-align:left;">
      <router-link style="text-decoration: none; color:gray; font-size:13px;" v-if="username" :to="{name: 'ProfileView', params: {username: this.username}}">
        <img id="profile-img" :src="imgSrc">
        {{ this.username }}  
      </router-link>
      <span v-if="!this?.liked">
        <img id="img_comment" style="cursor:pointer" @click="ReviewLike" src="../assets/before_like_blue.png">
      </span>
      <span v-else>
        <img id="img_comment" style="cursor:pointer" @click="ReviewLike" src="../assets/like_blue_full.png">
      </span>
      <!-- <button v-if="this?.liked" @click="ReviewLike">좋아요 취소</button>
      <button v-if="!this?.liked" @click="ReviewLike">좋아요</button> -->
        <a style="cursor:pointer; color:gray; margin-left: 8px; font-size:13px;" v-if="this.userid === this.review.review_user" @click="deleteReview">삭제</a>
        <a style="cursor:pointer; color:gray; margin-left: 8px; font-size:13px;" v-if="this.userid === this.review.review_user" @click="getReviewUpdate">수정</a>
        <span style="margin-left:5px; font-size: 13px;">⭐{{ review?.rank }}</span>
        <span v-if="this.userid === this.review.review_user" style="padding-top: 5px; font-size: 13px; color: gray; margin-left: 460px;">{{ moment(review?.created_at).format("YYYY-MM-DD hh:mm:ss") }}</span>
        <span v-if="this.userid !== this.review.review_user" style="padding-top: 5px; font-size: 13px; color: gray; margin-left: 530px;">{{ moment(review?.created_at).format("YYYY-MM-DD hh:mm:ss") }}</span>
      </div>
      <hr style="margin: 1px;">
      <p style="margin-top: 5px; text-align: left; margin-top:20px; margin-right: 30px; margin-left: 25px;">{{ review?.content }}</p>
    </div>
    <div v-if="this.updateStatus">
      <h1>리뷰 수정</h1>
      <form @submit.prevent="updateReview" class="review-form">
        <label for="title" style="margin-bottom: 5px;">제목</label>
        <input class="form-control" style="width:550px;" placeholder="제목을 입력해주세요" aria-label="Please input the title" aria-describedby="basic-addon1" type="text" id="title" v-model.trim="title"><br>
        <label for="content" style="margin-bottom: 5px;">리뷰 내용</label>
        <b-form-textarea placeholder="내용을 입력해주세요" 
        no-resize id="content" cols="30" rows="10" v-model.trim="content" style="width:550px;">
        </b-form-textarea>
        <div>
            <b-form-rating v-model="rank" variant="warning"></b-form-rating>
          </div>
        <input class="btn btn-danger" style="width: 550px; margin-bottom: 15px;" type="submit" id="submit">
      </form>
    </div>
      <CommentList
      v-for="(comment, index) in comments"
      :key="comment.id"
      :comment="comment"
      :index="index"
      :limit="commentsCurrentPage"
      @delete-comment="getComments"
      @update-comment="getComments"
      />
      
      <div v-if="comments" style="background-color: #2d3442; display: flex; justify-content: center;">
        <b-pagination id="comments_pagination" style="margin-bottom: 0px;"
          v-model="commentsCurrentPage"
          :total-rows="comments.length"
          :per-page="10"
        >
        </b-pagination>  
      </div>

      <CommentForm
      :review="review"
      @get-comment="getComments"
      />
  </div>

</template>

<script>
import CommentForm from '@/components/CommentForm'
import CommentList from '@/components/CommentList'
import axios from 'axios'
import moment from "moment"

const API_URL = "http://127.0.0.1:8000"

export default {
  name: 'ReviewList',
  data () {
    return {
      comments: null,
      liked: false,
      username: null,
      title: null,
      content:  null,
      rank: null,
      updateStatus: false,
      userid: null,
      moment: moment,
      commentsCurrentPage: 1,
      profileImageUrl: null,
    }
  },
  created() {
    this.getComments()
    this.getUserName()
    this.getReviewLike()
  },
  computed: {
    imgSrc() {
      return this.profileImageUrl
    },
  },
  props: {
    review: Object,
    index: Number,
    limit: Number,
  },
  components: {
    CommentForm,
    CommentList,

  },
  methods: {
    getProfileImage() {
      axios({
        method: 'get',
        url: `${API_URL}/accounts/profile_image/${this.review?.review_user}/`,
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
    },
    getUserName() {
      axios({
        method: 'post',
        url: `${API_URL}/accounts/wantname/`,
        data: {
          userid: this.review?.review_user
        },
        headers: { 
            Authorization: `Token ${this.$store.state.token}`
        }
      })
      .then((res) => {
        this.username = res.data.username
        this.userid = res.data.userid
      })
      .then(() => {
        this.getProfileImage()
      })
      .catch((err) => {
        console.log(err)
      })
    },
    getComments() {
      axios({
        method:'get',
        url: `${API_URL}/community/comment/${this.review?.id}/`,
        headers: { 
            Authorization: `Token ${this.$store.state.token}`
        }
      })
      .then((res) => {
        this.comments = res.data
      })
      .catch(() => {
        this.comments = null,
        console.log('댓글이 없습니다.')
      })
    },
    ReviewLike() {
      axios({
        method: 'post',
        url: `${API_URL}/community/reviews/like/${this.review?.id}/`,
        headers: { 
            Authorization: `Token ${this.$store.state.token}`
        }
      })
      .then((res) => {
        this.liked = res.data
      })
      .catch((err) => {
        console.log(err)
      })
    },
    getReviewLike() {
      console.log('응답')
      axios({
        method:'get',
        url: `${API_URL}/community/reviews/like/${this.review?.id}/`,
        headers: { 
            Authorization: `Token ${this.$store.state.token}`
        }
      })
      .then((res) => {
        // console.log(res['data']['liked'])
        this.liked = res['data']['liked']
      })
      .catch((err) => {
        console.log(err)

      })
    },
    deleteReview() {
      axios({
        method: 'delete',
        url: `${API_URL}/community/reviews/detail/${this.review?.id}/`,
        headers: { 
            Authorization: `Token ${this.$store.state.token}`
        }
      })
      .then(() => {
        this.$emit('delete-review')
      })
      .catch((err) => {
        console.log(err)
      })
    },

    getReviewUpdate() {
      axios({
        method: 'get',
        url: `${API_URL}/community/reviews/detail/${this.review?.id}/`,
        headers: { 
            Authorization: `Token ${this.$store.state.token}`
        }
      })
      .then((res) => {
        this.title = res.data.title
        this.content = res.data.content
        this.rank = res.data.rank
        this.updateStatus = true
      })
      .catch((err) => {
        console.log(err)
      })
    },
    setRating(rating) {
        this.rank = rating
    },
    updateReview() {
      axios({
        method: 'put',
        url: `${API_URL}/community/reviews/detail/${this.review?.id}/`,
        data: {
          title: this.title,
          content: this.content,
          rank: this.rank,
        },
        headers: { 
            Authorization: `Token ${this.$store.state.token}`
        }
      })
      .then(() => {
        this.$emit('update-review')
        this.updateStatus = false
      })
      .catch((err) => {
        console.log(err)

      })
    }
  }
}
</script>

<style>
#review_container {
  width: 800px;
  border: 1px solid white;
  /* background-color: white; */
  color: white;
}

.review-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

#img_comment {
  width: 25px;
  margin-left: 5px;
}

#comments_pagination {
  --bs-pagination-border-color:#2d3442 !important;
  --bs-pagination-disabled-border-color: #2d3442 !important;

}

#profile-img{
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
  margin: 5px;
  margin-right: 3px;
  margin-left: 7px;
}



/* .pagination{
  --bs-pagination-color: #ffffff;
  --bs-pagination-bg: none;
  --bs-pagination-border-color:#212529;
  --bs-pagination-active-bg: none;
  --bs-pagination-active-border-color: #ffffff;
  --bs-pagination-disabled-color: none;
  --bs-pagination-disabled-bg: none;
  --bs-pagination-disabled-border-color: #212529;
  --bs-pagination-hover-color: none;
  --bs-pagination-hover-bg: none;
  --bs-pagination-hover-border-color: #ffffff;
  --bs-pagination-focus-color: none;
  --bs-pagination-focus-bg: none;
} */


</style>