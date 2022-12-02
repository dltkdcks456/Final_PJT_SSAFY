<template>
  <div>
    <iframe id="player" type="text/html" width="640" height="360" showinfo=0
  modestbranding=1 allowfullscreen
  :src="videoSrc"></iframe>
  </div>
</template>

<script>
export default {
  name: 'VideoContent',
  props: {
    movieVideo: String,
  },
  computed: {
    videoSrc() {
      const url = `${this.movieVideo}?autoplay=1&mute=1&loop=1&controls=0&modestbranding=1`
      return url
    }
  }
}
</script>

<style>
#player {
  border: 0;
}
</style>