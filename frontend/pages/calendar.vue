<script setup lang="ts">
import axios from 'axios'

const user_id = useCookie('user_id')
const events = ref([])
const friend_events = ref([])
const isOpen = ref(false)
const username = ref('')
const router = useRouter()

let friend_events_list = ref([])

const friends_list = ref<FriendObj[]>([])
const friends_id_list = ref<string[]>([])

class FriendObj {
        public user_id: string;
        public username: string;
        constructor(user_id: string, username: string) {
          this.user_id  =user_id;
          this.username = username;
        }
      }

// Redirect to /signin if user_id is empty
onMounted(async () => {
  if (!user_id.value)
    router.push('/signin')
  else
    await fetchUserEvents()

  axios({
    method: 'get',
    url: `http://localhost:8000/users/get_all_user_friends?user_id=${user_id.value}`,
  }).then((response) => {
    console.log(response.data);
    const friends: Friend[] = response.data
    friends.forEach((friend) => {
      console.log(`Username: ${friend.username}`)
      const friend_username = friend.username
      // friends_list.value.push(friend_username);
      friends_list.value.push(new FriendObj(friend.user_id, friend.username))
      console.log('FRIEND OBJ:', friends_list)
      
      addFriendID(friend.user_id)
    })
    console.log(friends_list)
    console.log(friends_id_list)
    //fetchFriendsEvents()
  })

  try {
    axios({
      method: 'get',
      url: `http://localhost:8000/users/get_user_by_id?id=${user_id.value}`,
    }).then((response) => {
      console.log(response.data)
      username.value = response.data.username
    })
  }
  catch (error) {
    console.error('Error fetching user ID:', error)
    if (error.response.status == 422)
      alert('Failed to found user. Try logging in again.')

    else
      alert('An unexpected user error occured. Please try again later.')
  }

})

function addFriend(username: string) {
  friends_list.value.push(username)
}

function addFriendID(id: string) {
  friends_id_list.value.push(id)
}

async function fetchUserEvents() {
  try {
    const response = await fetch(`http://localhost:8000/events/get_user_events?user_id=${user_id.value}`)
    if (response.ok)
      events.value = await response.json()
    else
      console.error('Failed to fetch events')
  }
  catch (error) {
    console.error('Error fetching events:', error)
  }
}

async function fetchFriendsEvents(id: string) {
  //console.log(`Friends_id_list:`, friends_id_list)
    console.log(`Fetching friend_id: ${id} events in progress.`)
    try {
      const response = await fetch(`http://localhost:8000/events/get_user_events?user_id=${id}`)
      if (response.ok)
      {
        friend_events.value = await response.json()
        return friend_events;
      }
      else
        console.error('Failed to fetch events')
    }
    catch (error) {
      console.error('Error fetching events:', error)
    }
  console.log(`Friends events:`, friend_events)
}

function goProfile() {
  window.location.href = '/user_view'
}

function logOut()
{
  user_id.value = '';
  window.location.href = '/signin'
}

function submitEvent(newEvent) {
  events.value.push(newEvent)
  isOpen.value = false
}

function getDayOfWeek(dateString) {
  const date = new Date(dateString)
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
  return days[date.getDay()]
}
</script>

<template>
  <div>
    <div class="top-bar">
      <div class="left-top-bar">
        <img src="public/image.png" alt="Quanta logo" class="logo">
        <h1>Quanta</h1>
      </div>
      <div class="right-top-bar">
        <button class="plus" @click="isOpen = true">
          +
        </button>
        <h1>Add</h1>
        <button class="imageContainer" @click="goProfile">
          <img src="public/default_profile.png">
        </button>
        <button class="log-out-button" @click="logOut">
          Log out
        </button>
      </div>
      <AddEventPopup :visible="isOpen" @close="isOpen = false" @submit="submitEvent" />
    </div>

    <table>
      <tr>
        <td id="friends">
          Friends
        </td>
        <td id="calendar-bar">
          Monday
        </td>
        <td id="calendar-bar">
          Tuesday
        </td>
        <td id="calendar-bar">
          Wednesday
        </td>
        <td id="calendar-bar">
          Thursday
        </td>
        <td id="calendar-bar">
          Friday
        </td>
        <td id="calendar-bar">
          Saturday
        </td>
        <td id="calendar-bar">
          Sunday
        </td>
      </tr>
      <tr>
        <td>{{ username }}</td>
        <td v-for="day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']" :key="day">
          <div v-if="events.length > 0">
            <div v-for="event in events" :key="event.event_id">
              <template v-if="getDayOfWeek(event.event_date_start) === day">
                {{ event.event_name }}
              </template>
            </div>
          </div>
        </td>
      </tr>
      <tr v-for="friend in friends_list">
        <td>{{ friend.username }}</td>
        <td v-for="day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']" :key="day">
          <div>
            <div v-for="event in friend_events" :key="event.event_id">
              <template v-if="getDayOfWeek(event.event_date_start) === day">
                {{ event.event_name }}
              </template>
            </div>
          </div>
        </td>
      </tr>
    </table>
  </div>
</template>

<style>
body {
  margin: 0;
}
table, th, td, tr {
  border-right: 2px solid #CCB2C6;
  border-bottom: 2px solid #CCB2C6;
  text-align: center;
  -webkit-text-stroke: 1px rgb(85, 68, 76);
  text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
  font-family: 'Lao Muang Don', sans-serif;
  color: #fff;
  font-size: 1.7rem;
}

#work {
  background-color: #1569df39;
  border-radius: 40px;
}

table {
  border-collapse: collapse;
  width: 100%;
}
td {
  height: 40px;
  width: 12.5%;
}

.top-bar {
  width: 100%;
  height: 13vh;
  background-color: #FFE8E8;
  display: flex;
  justify-content: center;
  align-items: center;
  border-bottom: 2px solid #CCB2C6;
}
.top-bar h1, .top-bar plus {
  color: #fff;
  -webkit-text-stroke: 1px rgb(85, 68, 76);
  text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
}
.logo {
  height: 60px;
  margin: 20px;
}
.left-top-bar {
  font-size: 1.7rem;
  width: 100%;
  height: 10%;
  background-color: #FFE8E8;
  display: flex;
  font-family: 'Lao Muang Don', sans-serif;
  justify-content: left;
  align-items: center;
}
.right-top-bar {
  width: 100%;
  height: 10%;
  background-color: #FFE8E8;
  display: flex;
  font-family: 'Lao Muang Don', sans-serif;
  justify-content: right;
  align-items: center;
  font-size: 1.3rem;
  margin-right: 30px;
}
.plus {
  margin-right: 20px;
  background-color: #9E7E9B;
  width: 40px;
  height: 40px;
  border-radius: 25px;
  border: 0px;
  color: white;
  cursor: pointer;
  -webkit-text-stroke: 1px rgb(85, 68, 76);
  text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
#calendar-bar {
  display: table-cell;
  justify-content: center;
  width: 12.5%;
  font-size: 35px;
}
#friends {
  background-color: #FFE8E8;
  width: 12.5%;
  display: table-cell;
  justify-content: center;
  font-size: 35px;
}
.imageContainer {
    width: 5rem;
    height: 5rem;
    border-color: #542a2a;
    border-style: dotted;
    border-radius: 50%;
    margin-left: 2rem;
    margin-right: 2rem;
    cursor: pointer;
  }
  .imageContainer img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
  }
  .log-out-button{
  padding: 0.3rem;
  width: 9rem;
  height: 3rem;
  margin-right: 1rem;
  border: none;
  border-radius: 25px;
  background-color: #9E7E9B;
  color: white;
  cursor: pointer;
  font-size: 1.5rem;
}
</style>
