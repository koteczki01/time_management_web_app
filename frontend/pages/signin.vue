<script setup lang="ts">
definePageMeta({
  layout: 'user',
})
</script>

<template>
  <h1>Log in</h1>
  <form class="auth-form">
    <label>User:</label>
      <input type="text" required />
    <label>Password:</label>
      <input type="password" required />
    <div class="links">
      <a href="#" class="forgot-password">Forgot Password?</a>
      <a href="#" class="create-account">Create an account!</a>
    </div>
      <div class="login-button-container">
        <button type="submit" class="login-button">Log in</button>
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
  margin-bottom: 1em;
  padding: 1em;
  border: 1px solid #ccc;
  border-radius: 20px;
  font-size: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
}

.links {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 2em;
}

.forgot-password, .create-account {
  color: #887398;
  font-size: 0.8rem;
}

.login-button {
  padding: 0.3em;
  width: 200px;
  border: none;
  border-radius: 25px;
  background-color: #9E7E9B;
  color: white;
  cursor: pointer;
  font-size: 1.5rem;
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

label{
  color: #fff; 
  font-size: 1.8rem; 
  -webkit-text-stroke: 0.8px rgb(85, 68, 76); 
}

</style>
