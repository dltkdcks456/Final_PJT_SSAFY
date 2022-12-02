<template>
  <div>
    <a style="cursor:pointer" @click="providerLink">
      <img :src="providerLogo" width="30" id="provider-img">
    </a>
  </div>
</template>

<script>
export default {
  name: 'ProviderMovie',
  props: {
    provider: Object,
  },
  computed: {
    providerLogo() {
        return this.provider.provider_logo_path
    },
  },
  methods: {
    providerLink() {
      window.open(this.provider.provider_link)
    },
  }
}
</script>

<style>
#provider-img {
    margin-right: 15px;
    border-radius: 4px;
}
</style>