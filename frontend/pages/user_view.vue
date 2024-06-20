<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { stringifyQuery } from 'vue-router'
import Popup from '../components/friend_request_popup.vue'

definePageMeta({
  layout: 'view',
})

const user_id = useCookie('user_id')
const username = ref('')
const email = ref('')
const birthday = ref('')
const friends_string = ref('')
const isOpen = ref(false)
let submittedUsername = ''
const friend_id = ref('')

interface Friend {
  username: string
}

const friends_list = ref<string[]>([])

try {
  axios({
    method: 'get',
    url: `http://localhost:8000/users/get_user_by_id?id=${user_id.value}`,
    params: {
      limit: 5,
    },
  }).then((response) => {
    console.log(response.data)
    username.value = response.data.username
    email.value = response.data.email
    birthday.value = response.data.birthday
  })
}
catch (error) {
  console.error('Error fetching user ID:', error)
  if (error.response.status == 422)
    alert('Failed to found user. Try logging in again.')

  else
    alert('An unexpected user error occured. Please try again later.')
}

axios({
  method: 'get',
  url: `http://localhost:8000/users/get_all_user_friends?user_id=${user_id.value}`,
}).then((response) => {
  // console.log(response.data);
  const friends: Friend[] = response.data
  friends.forEach((friend) => {
    console.log(`Username: ${friend.username}`)
    const friend_username = friend.username
    friends_string.value = `${friends_string.value + friend.username} `
    // friends_list.value.push(friend_username);
    addFriend(friend.username)
  })
  console.log(friends_list)
})

function addFriend(username: string) {
  friends_list.value.push(username)
}

async function getFriendID(input: string): Promise<string> {
  try {
    const response = await axios({
      method: 'get',
      url: `http://localhost:8000/users/get_user_by_username?username=${input}`,
    })
    friend_id.value = response.data.user_id
    return friend_id.value
  }
  catch (error) {
    console.error('Error fetching friend ID:', error)
    if (axios.isAxiosError(error)) {
      if (error.response && error.response.status === 422)
        alert('User not found!')
      else
        alert('An unexpected error occurred. Please try again later.')
    }
    else {
      alert('User not found!')
    }
    throw error
  }
}

async function postFriendRequest(input: string) {
  try {
    const friend_id_string = await getFriendID(input)
    if (!friend_id_string) {
      alert('User not found!')
      return
    }
    console.log(friend_id_string)
    console.log(user_id.value)
    const response = await axios({
      method: 'post',
      url: `http://localhost:8000/friends/send?sender_id=${user_id.value}&recipient_id=${friend_id_string}`,
      // data: {
      //  sender_id: user_id.value,
      //  recipient_id: friend_id_string
      // }
    })
    console.log('Post response:', response.data)
    alert('Succesfully added a friend!')
  }
  catch (error) {
    console.error('Error posting friend request:', error)
    if (error.response.status == 409) {
      alert('You are already friends!')
    }
    else {
      // alert('An unexpected error occurred. Please try again later.');
    }
  }
}

function handleSubmit(value: string) {
  submittedUsername = value
  console.log('Submitted value:', submittedUsername)
  postFriendRequest(submittedUsername)
}
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
    </form>
    <div>
      <button type="submit" class="change-button">
        Change Password
      </button>
    </div>
  </div>

  <div class="friends-card">
    <h1>Friends</h1>
    <form class="scroll">
      <div v-for="friend in friends_list" class="list">
        <p class="text2">
          {{ friend }}
        </p>
      </div>
    </form>
    <div>
      <button class="add-button" @click="isOpen = true">
        Add
      </button>
      <Popup v-if="isOpen" :visible="isOpen" @close="isOpen = false" @submit="handleSubmit" />
    </div>
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
  justify-content: center;
  align-items: center;
  width: 100%;
  margin-right: 1rem;
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

  .scroll
  {
    overflow:auto;
    overflow-x:hidden

  }

  .scroll::-webkit-scrollbar {
    width: 12px;
}

.scroll::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
    border-radius: 10px;
}

.scroll::-webkit-scrollbar-thumb {
    border-radius: 10px;
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.5);
}

  .friends-card {
    display: flex;
    width: 15rem;
    height: 26rem;
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
