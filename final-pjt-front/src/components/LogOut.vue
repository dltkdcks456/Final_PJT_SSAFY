<template>
  <div>
    <h1>LogOut Page</h1>
    <form @submit.prevent="logOut">
        <input type="submit" class="btn btn-danger" value="logOut">
      </form>
  </div>
</template>

<script>
export default {
  name: 'LogOut',
  data() {
    return {
      
    }
  },
  methods: {
    logOut() {
      this.$store.dispatch('logOut')
      this.$cookies.remove("csrftoken")
    },
  }
}
</script>
