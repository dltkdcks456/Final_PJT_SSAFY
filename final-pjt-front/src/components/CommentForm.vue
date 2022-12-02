<template>
  <div >
    <form @submit.prevent="createComment" style="border-radius:0px; height:50px;  display:flex; justify-content: space-between; width: 100px;">
      <div>
      <input class="form-control" style="width:742px; " placeholder="댓글을 입력해주세요" aria-label="Please input the title" aria-describedby="basic-addon1" type="text" id="title"  v-model.trim="inputData">
    </div>
    <div>
      <input class="btn btn-danger" type="submit">
    </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

const API_URL = "http://127.0.0.1:8000"

export default {
  name: 'CommentForm',
  props: {
    review: Object,
  },
  data() {
    return {
        inputData: null,
    }
  },
  methods: {
    createComment() {
        const content = this.inputData
        if (!content) {
            alert('댓글을 입력해주세요')
            return
        }
        axios({
            method: 'post',
            url: `${API_URL}/community/comment/${this.review.id}/`,
            data: {
                content,
            },
            headers: { 
            Authorization: `Token ${this.$store.state.token}`
        }
        })
        .then(() => {
            // console.log(res)
            this.$emit('get-comment')
            this.inputData=null
        })
        .catch((err) => {
            console.log(err)
        })
    }
  }
}
</script>

<style>

</style>