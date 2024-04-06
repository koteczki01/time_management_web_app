<script setup lang="ts">
definePageMeta({
  layout: 'user',
})
</script>

<template>
  <h1>Create an Account</h1>
  <form class="auth-form">
    <label>Username:</label>
    <input type="text" required />
    <label>E-Mail:</label>
    <input type="text" required />
    <div class="pass-form">
      <div class="password-container">
        <label>Password:</label>
        <input type="password" id="password" required />
      </div>
      <div class="password-container">
        <label>Repeat Password:</label>
        <input type="password" id="repeat-password" required />
      </div>
    </div>
    <div class="pass-form">
      <div class="date-birth">
        <label>Date of Birth:</label>
        <input type="date">
      </div>
      <div class="checkbox-container flex items-center">
        <input type="checkbox" id="agree-terms">
        <label for="agree-terms" class="text">I read and agree with the terms and conditions</label>
      </div>
    </div>
    <div class="login-button-container">
      <button type="submit" class="login-button">Go Back</button>
      <button type="submit" class="login-button">Register</button>
    </div>
  </form>
</template>

<style scoped>
.auth-form {
  display: flex;
  flex-direction: column;
  width: 100%;
}
input {
  margin-bottom: 1rem;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 20px;
  font-size: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
}
.forgot-password, .create-account {
  color: #887398;
  font-size: 0.8rem;
}
.login-button {
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
.login-button-container {
  display: flex;
  align-items: center;
  justify-content: center;
}
h1 {
  color: #fff; 
  font-size: 3rem; 
  -webkit-text-stroke: 1px rgb(85, 68, 76); 
  text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
}
label {
  color: #fff; 
  font-size: 1.8rem; 
  -webkit-text-stroke: 0.8px rgb(85, 68, 76); 
}
.pass-form {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.date-birth {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50%;
}
.password-container {
  display: flex;
  flex-direction: column;
  width: 50%;
  align-items: center; 
  justify-content: center; 
  margin-right: 2rem;
}

.checkbox-container {
  display: flex;
  width: 50%;
  align-items: center; 
  justify-content: flex-start;
  margin-left: 2rem; 
}

.text {
  font-size: 1.3rem;
}
</style>
