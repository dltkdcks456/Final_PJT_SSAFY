<template>
  <div style="margin-bottom: 10px;">
    <a @click="goToProfile" style="text-decoration:none; font-weight: bolder; color:black; font-size:17px; cursor:pointer;" >
      <img id="profile-img" :src="imgSrc">
      {{ this.follower.username }} </a>
  </div>
</template>

<script>
import axios from 'axios'
const API_URL = "http://127.0.0.1:8000"

export default {
  name: 'FollowerMembers',
  data() {
    return {
      profileImageUrl: null,
    }
  },
  created() {
    this.getProfileImage()
  },
  computed: {
    imgSrc() {
      return this.profileImageUrl
    },
  },
  props: {
    follower: Object,
  },
  methods: {
    goToProfile() {
        this.$router.push({name: 'ProfileView', params: {username: this.follower.username}});

    },
    getProfileImage() {
      console.log(this.following)
      axios({
        method: 'get',
        url: `${API_URL}/accounts/profile_image/${this.follower.id}/`,
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
  }
}
</script>

<style>

</style>