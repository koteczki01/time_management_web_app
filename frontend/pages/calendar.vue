<script setup lang="ts">
const user_id = useCookie('user_id')
const events = ref([])
const isOpen = ref(false)
const router = useRouter()

// Redirect to /signin if user_id is empty
onMounted(async () => {
  if (!user_id.value)
    router.push('/signin')
  else
    await fetchUserEvents()
})

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
        <td />
        <td v-for="day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']" :key="day">
          <div v-if="events.length > 0">
            <div v-for="event in events" :key="event.event_id">
              <template v-if="getDayOfWeek(event.event_date_end) === day">
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
</style>
