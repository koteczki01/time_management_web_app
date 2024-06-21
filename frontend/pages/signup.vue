<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'

definePageMeta({
  layout: 'user',
})

const username = ref('')
const email = ref('')
const password = ref('')
const repeatPassword = ref('')
const birthday = ref('')
const agreeTerms = ref(false)

async function registerUser() {
  try {
    const response = await axios.post('http://localhost:8000/register', {
      username: username.value,
      password: password.value,
      email: email.value,
      birthday: birthday.value,
    })
    if (response.status === 201)
      alert('Rejestracja zakończona pomyślnie!')
    else
      console.error('Błąd rejestracji:', response.data.message)
  }
  catch (error) {
    console.error('Wystąpił błąd podczas rejestracji:', error)
  }
}
</script>

<template>
  <section>
    <h1>Create an Account</h1>
    <form class="auth-form" @submit.prevent="registerUser">
      <div class="form-group">
        <label for="username">Username:</label>
        <input id="username" v-model="username" type="text" required>
      </div>

      <div class="form-group">
        <label for="email">E-Mail:</label>
        <input id="email" v-model="email" type="text" required>
      </div>

      <div class="group">
        <div class="form-group-one">
          <label for="password">Password:</label>
          <input id="password" v-model="password" type="password" required>
        </div>

        <div class="form-group-one">
          <label for="repeat-password">Repeat Password:</label>
          <input id="repeat-password" v-model="repeatPassword" type="password" required>
        </div>
      </div>

      <div class="group">
        <div class="form-group-one">
          <label for="dob">Date of Birth:</label>
          <input id="dob" v-model="birthday" type="date">
        </div>

        <div class="checkbox-container">
          <input id="agree-terms" v-model="agreeTerms" type="checkbox">
          <label for="agree-terms">I read and agree with the terms and conditions</label>
        </div>
      </div>

      <div class="button-container">
        <button type="button" @click="goBack">
          Go Back
        </button>
        <button type="submit">
          Register
        </button>
      </div>
    </form>
  </section>
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

.group {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.form-group-one {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-items: center;
  width: 50%;
  margin-bottom: 1rem;
}

input[type="text"],
input[type="password"],
input[type="date"] {
  box-sizing: border-box;
  padding: 1rem;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 20px;
  font-size: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
}

.button-container {
  display: flex;
  justify-content: space-between;
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

h1 {
  color: #fff;
  font-size: 3rem;
  -webkit-text-stroke: 1px rgb(85, 68, 76);
  text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
  text-align: center;
}

label {
  color: #fff;
  font-size: 1.8rem;
  -webkit-text-stroke: 0.8px rgb(85, 68, 76);
}

.checkbox-container {
  display: flex;
  align-items: center;
  margin-left: 2rem;
  width: 50%;
}
</style>
