<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { stringifyQuery } from 'vue-router';

definePageMeta({
  layout: 'view',
});

const user_id = useCookie('user_id');
const username = ref('');
const email = ref('');
const birthday = ref('');
const friends_string = ref('');

interface Friend {
  username: string;
}

axios({
  method: "get",
  url: "http://localhost:8000/users/get_user_by_id?id=" + user_id.value,
  params: {
    limit: 5
  }
}).then(function (response) {
  console.log(response.data);
  username.value = response.data['username'];
  email.value = response.data['email'];
  birthday.value = response.data['birthday'];
});

axios({
  method: "get",
  url: "http://localhost:8000/users/get_all_user_friends?user_id=" + user_id.value,
  params: {
    limit: 5
  }
}).then(function (response) {
  console.log(response.data);
  const friends: Friend[] = response.data;
  friends.forEach((friend) => {
    console.log(`Username: ${friend.username}`);
    friends_string.value = friends_string.value + friend.username + ` `;
    console.log(`lista friends: ${friends_string.value}`);
});
});

</script>

<template>
  <div>
    <div class="imageContainer">
      <img src="public/default_profile.png">
    </div>

    <div class="usernameContainer">
      <p class="text2">
        {{ username }}
      </p>
    </div>
  </div>

  <div class="auth-card">
    <h1>Information</h1>
    <form>
      <div class="form">
        <label for="e-mail">E-Mail:</label>
        <p class="text">
          {{ email }}
        </p>
      </div>

      <div>
        <label for="birthdate">Birthdate:</label>
        <p class="text">
          {{ birthday }}
        </p>
      </div>

      <div>
        <button type="submit" class="change-button">
          Change Password
        </button>
      </div>
    </form>
  </div>

  <div class="friends-card">
    <h1>Friends</h1>
    <form>
      <div class="list">
        <p class="text2">
          {{ friends_string }}
        </p>
      </div>

      <div class="list">
        <p class="text2">
          Marcysia
        </p>
      </div>

      <div class="list">
        <p class="text2">
          Piecharka
        </p>
      </div>

      <div>
        <button type="submit" class="add-button">
          Add
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 1rem;
}

.list {
  display: flex;
  justify-content: center;
  align-content: center;
  flex-direction: column;
  width: 100%;
}

.change-button {
  padding: 0.3rem;
  width: 250px;
  height: 60px;
  border: none;
  border-radius: 25px;
  background-color: white;
  color: #895D5D;
  cursor: pointer;
  font-size: 1.5rem;
  border-style: solid;
  border-color: #895D5D;
  border-width: 1px;
}

.add-button {
  padding: 0.3rem;
  width: 8rem;
  height: 3rem;
  border: none;
  border-radius: 25px;
  background-color: white;
  color: #895D5D;
  cursor: pointer;
  font-size: 1.5rem;
  border-style: solid;
  border-color: #895D5D;
  border-width: 1px;
}

.back-button{
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

.button-container {
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
  color: #6F3C3C;
  font-size: 1.8rem;
}

.text
{
  font-size: 1.5rem;
  color: #895D5D;
}

.text2
{
  font-size: 2rem;
  font-weight: bold;
  color: #542a2a;
}

.auth-card {
    display: flex;
    margin: 48px 0px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #FEEAEAEA;
    padding: 2rem;
    border-radius: 50px;
    border: 1px solid #ccc;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-style: solid;
    border-color: #895D5D;
    border-width: 1px;
  }

  .friends-card {
    display: flex;
    width: 15rem;
    margin: 48px 0px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #D0A6A6;
    padding: 2rem;
    border-radius: 50px;
    border: 1px solid #ccc;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .imageContainer {
    width: 20rem;
    height: 20rem;
    border-color: #542a2a;
    border-style: dotted;
    border-radius: 50%;
  }
  .imageContainer img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
  }

  .usernameContainer {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50px;
    border-style: solid;
    border-color: #895D5D;
    border-width: 1px;
    margin: 48px 0px;
    background-color: white;
    height: 3.5rem;
  }
</style>
