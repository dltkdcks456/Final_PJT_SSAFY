<template>
  <div>
    <!-- <router-view :key="$route.fullPath"></router-view> -->
    <router-view/>
    <nav v-show="this.hide">
      <router-link  :to="{name: 'MovieView'}"></router-link>
      <router-link  :to="{name: 'GenreView'}"></router-link>
      <router-link  :to="{name: 'CinemaView'}"></router-link>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'MainView',
  data() {
    return {
      hide: false,
    }
  },
  created() {
    this.startPage()
  },
  methods: {
    startPage() {
      this.$router.push({name: 'MovieView'}).catch(() =>{})
    },
  }
}
</script>

<style>

</style>