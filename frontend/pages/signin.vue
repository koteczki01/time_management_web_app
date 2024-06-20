<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { stringifyQuery } from 'vue-router';

definePageMeta({
  layout: 'user',
});

const username = ref('');
const password = ref('');
const user_id = useCookie('user_id');

const login = async () => {
  try {
    const response = await axios.post('http://localhost:8000/login', {
      username: username.value,
      password_hash: password.value,
    });
    console.log(response.data);
    user_id.value = response.data['user_id'];
    alert('Login successful');
    
  } catch (error) {
    console.error(error);
    if (error.response && error.response.status === 401) {
      alert('Incorrect username or password');
    } else {
      alert('An error occurred. Please try again later.');
    }
  }
};
</script>

<template>
  <h1>Log in</h1>
  <form class="auth-form" @submit.prevent="login">
    <div class="form-group">
      <label for="user">User:</label>
      <input id="user" type="text" v-model="username" required />
    </div>

    <div class="form-group">
      <label for="password">Password:</label>
      <input id="password" type="password" v-model="password" required />
    </div>

    <div class="links">
      <a href="#" class="forgot-password">Forgot Password?</a>
      <a href="#" class="create-account">Create an account!</a>
    </div>
    <div class="login-button-container">
      <button type="submit" class="login-button">
        Log in
      </button>
    </div>
  </form>
</template>

<style scoped>
.auth-form {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.form-group {
  margin-bottom: 1rem;
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

.links {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 2rem;
}

.forgot-password,
.create-account {
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
  text-shadow: 2px 2px 2px rgba(85, 68, 76, 0.6);
}

label {
  color: #fff;
  font-size: 1.8rem;
  -webkit-text-stroke: 0.8px rgb(85, 68, 76);
}
</style>