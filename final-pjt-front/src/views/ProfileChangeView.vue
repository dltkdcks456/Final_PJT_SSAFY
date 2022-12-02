<template>
  <div>
    <br><br>
    <button class="btn btn-danger" style="cursor:pointer" @click="goToBack">돌아가기</button>
    <hr>
    <br>
    <PasswordChange/>
    <br>
    <hr>
    <br>
    <LeaveView/>
    <br>
  </div>
</template>

<script>
import PasswordChange from '@/components/PasswordChange'
import LeaveView from '@/components/LeaveView'
export default {
  name: 'ProfileChangeView',
  components: {
    PasswordChange,
    LeaveView,
  },
  methods: {
    goToBack() {
      window.history.back()
    },
  }
}
</script>