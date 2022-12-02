<template>
  <div style="margin-bottom: 10px;">
    <a @click="goToProfile" style="text-decoration:none; color:black; font-weight: bolder; font-size:17px; cursor:pointer; margin-bottom: 35px;" >
      <img id="profile-img" :src="imgSrc">
      {{ following.username }}</a>
  </div>
</template>

<script>
import axios from 'axios'
const API_URL = "http://127.0.0.1:8000"

export default {
  name: 'FollowingMembers',
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
    following: Object,
  },
  methods: {
    goToProfile() {
        this.$router.push({name: 'ProfileView', params: {username: this.following.username}});

    },
    getProfileImage() {
      console.log(this.following)
      axios({
        method: 'get',
        url: `${API_URL}/accounts/profile_image/${this.following.id}/`,
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