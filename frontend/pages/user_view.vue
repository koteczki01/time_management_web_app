<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { stringifyQuery } from 'vue-router'
import Popup from '../components/friend_request_popup.vue'
import Popup2 from '../components/change_password_popup.vue'

definePageMeta({
  layout: 'view',
})

const user_id = useCookie('user_id')
const username = ref('')
const email = ref('')
const birthday = ref('')
const friends_string = ref('')
const isOpen = ref(false)
const isOpen2 = ref(false)
let submittedUsername = ''
let submittedNewPassword = ''
let submittedNewPassword2 = ''
const friend_id = ref('')

const router = useRouter();

interface Friend {
  username: string
}

const friends_list = ref<string[]>([])

// Redirect to /signin if user_id is empty
onMounted(() => {
  if (!user_id.value) {
    router.push('/signin')
  }
})

try {
  axios({
    method: 'get',
    url: `http://localhost:8000/users/get_user_by_id?id=${user_id.value}`,
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
async function postChangePassword(input: string) {
  try {
    console.log(`http://localhost:8000/users/change_password?user_id=${user_id.value}&password=${input}`);
    const response = await axios({
      method: 'put',
      url: `http://localhost:8000/users/change_password?user_id=${user_id.value}&password=${input}`,
    })
    console.log('Post response:', response.data)
    alert('Succesfully changed password!')
  }
  catch (error) {
    console.error('Error changing password:', error)
    alert('Unexpected error occured. Please try again later')
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
function handleSubmit2(value: string, value2: string) {
  submittedNewPassword = value
  submittedNewPassword2 = value2
  console.log('Submitted value:', submittedNewPassword)
  console.log('Submitted value2:', submittedNewPassword2)
  if (submittedNewPassword == submittedNewPassword2) {
    postChangePassword(submittedNewPassword)
  }
  else {
    alert('Entered passwords are not the same')
  }
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
      <button type="submit" class="change-button" @click="isOpen2 = true">
        Change Password
      </button>
      <Popup2 v-if="isOpen2" :visible="isOpen2" @close="isOpen2 = false" @submit="handleSubmit2" />
    </div>
  </div>

  <div class="friends-card">
    <h1>Friends</h1>
    <div class="scroll">
      <div v-for="friend in friends_list" class="list">
        <div class="text2">
          {{ friend }}
        </div>
      </div>
    </div>
    <div>
      <button class="add-button" @click="isOpen = true">
        Add
      </button>
      <Popup v-if="isOpen" :visible="isOpen" @close="isOpen = false" @submit="handleSubmit" />
    </div>
  </div>
</template>

<style scoped>

.list {
  width: 100%;
  justify-content: center;
  height: 5rem;
  display: flex;
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
  margin: 1rem;
}

label {
  color: #6F3C3C;
  font-size: 1.8rem;
  padding-top: 1rem;
  display: flex;
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
  justify-content: center;
  display: flex;
  padding: 5px;
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
    overflow-x:hidden;
    width: 16rem;
    display: flex;
    flex-direction: column;
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
    height: 25rem;
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
