<template>
  <div v-if="visible" class="popup-overlay" @click="closePopup">
    <div class="popup-content" @click.stop>
      <h2>Create a new password</h2>
      <div class="input-container">
        <input type="password" placeholder="Enter new password" v-model="newPassword" />
      </div>
      <div class="input-container">
        <input type="password" placeholder="Confirm password" v-model="newPassword2" />
      </div>
      <button @click="submit">Change password</button>
      <button @click="closePopup">Close</button>
    </div>
  </div>
</template>
  
<script>
export default {
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      newPassword: '',
      newPassword2: '',
    };
  },
  methods: {
    closePopup() {
      this.$emit('close');
    },
    submit() {
      this.$emit('submit', this.newPassword, this.newPassword2);
      //this.closePopup();
    },
  },
};
</script>
  
  <style scoped>
  .popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .popup-content {
    display: flex;
    margin: 48px 0px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 50px;
    border: 1px solid #ccc;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-style: solid;
    border-color: #895D5D;
    border-width: 1px;
  }

  .input-container {
    display: flex;
    padding-bottom: 1rem;
    width: 100%;
  }

  input {
  box-sizing: border-box;
  padding: 1rem;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 20px;
  font-size: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
}
button {
  padding: 0.3rem;
  width: 200px;
  border: none;
  border-radius: 25px;
  background-color: #9E7E9B;
  color: white;
  cursor: pointer;
  font-size: 1.5rem;
  margin: 0.3rem;
}
  </style>
  