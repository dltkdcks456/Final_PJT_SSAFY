<template>
  <div>
    <h1>회원탈퇴</h1>
    <br>
    <div>
      <b-button class="btn btn-danger" @click="$bvModal.show('modal-leave')">회원탈퇴</b-button>

      <b-modal id="modal-leave">
        <!-- 헤더 -->
        <template #modal-header>
          <h4>회원탈퇴</h4>
        </template>
        <!-- 바디 -->
        <template #default>
          <p>아래에 '회원탈퇴'를 입력한뒤, 탈퇴하기 버튼을 누르세요.</p>
          탈퇴 시 복구할 수 없습니다.
          <br>
          <br>
            <b-input
              v-model="name"
            ></b-input>
        </template>
        <!-- 풋터 -->
        <template #modal-footer="{cancel}">
          <b-button v-if="name === '회원탈퇴'" size="sm" variant="danger" @click="leave()">
            탈퇴하기
          </b-button>
          <b-button size="sm" variant="dark" @click="cancel()" >
            취소</b-button>
        </template>

      </b-modal>
    </div>
    <!-- <form  @submit.prevent="leave">
      <input type="submit" class="btn btn-danger"  value="회원탈퇴">
    </form> -->
  </div>
</template>

<script>
export default {
  name: 'LeaveView',
  data() {
    return {
      name: '',
    }
  },
  methods: {
    leave() {
      alert('탈퇴되었습니다.')
      this.$store.dispatch('leave')
      this.$cookies.remove("csrftoken")
    },
  }
}
</script>