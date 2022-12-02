<template>
  <div>
    <h1>Sign up</h1>
    <form @submit.prevent="signUp">
      <label for="username" style="margin-bottom: 4px;">username : </label>
      <input type="text" id="username" v-model="username" style="width:350px;" class="form-control" placeholder="username" aria-label="username" aria-describedby="basic-addon1"><br>

      <label for="password1" style="margin-bottom: 4px;"> password : </label>
      <input type="password" id="password1" v-model="password1" style="width:350px;" class="form-control" placeholder="password1" aria-label="password1" aria-describedby="basic-addon1"><br>

      <label for="password2" style="margin-bottom: 4px;"> password confirmation : </label>
      <input type="password" id="password2" v-model="password2" style="width:350px;" class="form-control" placeholder="password2" aria-label="password2" aria-describedby="basic-addon1"><br>
      
      <input type="submit" class="btn btn-danger" value="Sign up">
    </form>
  </div>
</template>

<script>
export default {
  name: 'SignUpView',
  data() {
    return {
      username: null,
      password1: null,
      password2: null,
    }
  },
  methods: {
    signUp() {
      const username = this.username
      const password1 = this.password1
      const password2 = this.password2

      if (username === null || password1 === null || password2 === null) {
        alert('값을 입력해주세요')
      } else if (password1 === password2) {
        const payload = {
          username,
          password1,
          password2,
        }
        this.$store.dispatch('signUp', payload)
      } else {
        alert('비밀번호가 다릅니다')
        this.password1 = null
        this.password2 = null
      }
    }
  }
}
</script>
