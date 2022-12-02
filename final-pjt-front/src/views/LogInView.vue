<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="logIn">
      <label for="username" style="margin-bottom: 4px;">username : </label>
      <input type="text" id="username" v-model="username" style="width:350px;" class="form-control" placeholder="username" aria-label="username" aria-describedby="basic-addon1"><br>

      <label for="password" style="margin-bottom: 4px;"> password : </label>
      <input type="password" id="password" v-model="password" style="width:350px;" class="form-control" placeholder="password" aria-label="password" aria-describedby="basic-addon1"><br>

      <input type="submit" class="btn btn-danger" value="Login">
    </form>
  </div>
</template>

<script>
export default {
  name: 'LogInView',
  data() {
    return {
      username: null,
      password: null,
    }
  },
  methods: {
    logIn() {
      const username = this.username
      const password = this.password

      const payload = {
        username,
        password,
      }
      this.$store.dispatch('logIn', payload)
    }
  }
}
</script>
