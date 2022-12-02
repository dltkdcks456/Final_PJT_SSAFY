<template>
  <div>
    <h1>비밀번호 변경</h1>
    <br>
    <form @submit.prevent="passwordChange" style="display: flex; flex-direction: column; align-items: center;">
      <label for="old_password ">기존 비밀번호</label>
      <input type="password" id="old_password " style="width:350px;" v-model="old_password" class="form-control" placeholder="old_password" aria-label="old_password" aria-describedby="basic-addon1"><br>

      <label for="new_password1"> 새 비밀번호</label>
      <input type="password" id="new_password1" style="width:350px;" v-model="new_password1" class="form-control" placeholder="new_password1" aria-label="new_password1" aria-describedby="basic-addon1"><br>

      <label for="new_password2"> 새 비밀번호 확인</label>
      <input type="password" id="new_password2" style="width:350px;" v-model="new_password2" class="form-control" placeholder="new_password2" aria-label="new_password2" aria-describedby="basic-addon1"><br>

      <input type="submit" class="btn btn-danger" value="비밀번호 변경하기">
    </form>
  </div>
</template>

<script>
export default {
  name: 'PasswordChange',
  data() {
    return {
      new_password1: null,
      new_password2: null,
      old_password: null,
    }
  },
  methods: {
    passwordChange() {
      const new_password1 = this.new_password1
      const new_password2 = this.new_password2
      const old_password = this.old_password

      const payload = {
        new_password1,
        new_password2,
        old_password,
      }
      if (new_password1 === null || new_password2 === null || old_password === null) {
        alert('비밀번호를 입력 해주세요')
        this.old_password = null
        this.new_password1 = null
        this.new_password2 = null
      } else if (new_password1 === new_password2){
        this.$store.commit('PASSWORD_CHANGE', payload)
        alert('비밀번호가 변경되었습니다')
        this.old_password = null
        this.new_password1 = null
        this.new_password2 = null
      } else {
        alert('비밀번호가 다릅니다')
        this.old_password = null
        this.new_password1 = null
        this.new_password2 = null
      }
    }
  }
}
</script>
