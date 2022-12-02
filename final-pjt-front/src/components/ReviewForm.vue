<template>
  <div>
    <h1>리뷰 작성</h1>
    <form @submit.prevent="createReview" class="review-form">
        <label for="title" style="margin-bottom: 5px;">제목</label>
        <input class="form-control" style="width:550px;" placeholder="제목을 입력해주세요" aria-label="Please input the title" aria-describedby="basic-addon1" type="text" id="title" v-model.trim="title"><br>
        <label for="content" style="margin-bottom: 5px;">리뷰 내용</label>
        <b-form-textarea placeholder="내용을 입력해주세요" 
        no-resize id="content" cols="30" rows="10" v-model.trim="content" style="width:550px;">
        </b-form-textarea>
        <div>
          <b-form-rating v-model="rank" variant="warning" style="margin: 15px;"></b-form-rating>
        </div>
        <input class="btn btn-danger" style="width: 550px; margin-bottom: 15px;" type="submit" id="submit">
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import swal from 'sweetalert'


const API_URL = "http://127.0.0.1:8000"

export default {
  name: 'ReviewForm',
  props: {
    movie: Object,
  },
  components: {
  },
  data() {
    return {
        title: null,
        content:  null,
        rank: null,
    }
  },
  methods: {
    createReview() {
        const title = this.title
        const content = this.content
        const rank = this.rank
        if (!title) {
            alert('제목을 입력해주세요!')
            return
        } else if (!content) {
            alert('내용을 입력해주세요!')
            return
        } else if (!rank) {
            alert('별점을 선택해주세요!')
            return
        }
        axios({
            method: 'post',
            url: `${API_URL}/community/reviews/${this.movie.id}/`,
            data: {
                title, content, rank
            },
            headers: { 
            Authorization: `Token ${this.$store.state.token}`
        }
        })
        .then(() => {
            this.$emit('review-create')
            this.title = null
            this.content = null
            this.rank = 0
        })
        .catch(() => {
          swal("리뷰는 하나만 작성 가능합니다!!");
        })
    },
    setRating(rating) {
        this.rank = rating
    },
  }
}
</script>

<style>
.review-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

</style>