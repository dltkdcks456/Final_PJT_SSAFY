<template>
  <div>
    <a style="cursor:pointer" @click="poster_mini()"><img :src="imgSrc" style="width: 200px;"></a>
  </div>
</template>

<script>
export default {
  name: 'PostersMovie',
  props: {
    poster: Object,
  },
  computed: {
    imgSrc() {
      return this.poster.file_path
    }
  },
  methods: {
    poster_mini() {
      window.open(this.imgSrc)
    },
  },
}
</script>

<style>
.poster {
  display:flex;
  justify-content: center;
  align-items:center;
  
}
</style>