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
      eventName: '',
      eventDateStart: '',
      createdBy: useCookie('user_id').value,
      eventDescription: 'Default event description',
      eventDateEnd: '2024-06-23T15:00:00', // Mockup end date
      eventLocation: 'Default location',
      privacy: 'private', // or 'private'
      recurrence: 'daily', // or 'weekly', 'monthly', 'yearly'
      nextEventDate: '2024-06-24T13:00:00', // Mockup next event date
      categories: [],
    }
  },
  methods: {
    closePopup() {
      this.$emit('close')
    },
    submit() {
      const payload = {
        event_name: this.eventName,
        created_by: this.createdBy,
        event_date_start: this.eventDateStart,
        event_description: this.eventDescription,
        event_date_end: this.eventDateEnd,
        event_location: this.eventLocation,
        privacy: this.privacy,
        recurrence: this.recurrence,
        next_event_date: this.nextEventDate,
        categories: this.categories,
      }

      fetch('http://localhost:8000/event/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })
        .then(response => response.json())
        .then((data) => {
          this.$emit('submit', data)
        // this.closePopup();
        alert("Event added.")
        })
        .catch((error) => {
          alert("An unexpected error occured. Please try again later.")
          console.error('Error:', error)
        })
    },
  },
}
</script>

<template>
  <div v-if="visible" class="popup-overlay" @click="closePopup">
    <div class="popup-content" @click.stop>
      <h2>Create Event</h2>
      <div class="input-container">
        <input v-model="eventName" type="text" placeholder="Event Name">
      </div>
      <div class="input-container">
        <input v-model="eventDateStart" type="datetime-local" placeholder="Event Start Date">
      </div>
      <button @click="submit">
        Create Event
      </button>
      <button @click="closePopup">
        Close
      </button>
    </div>
  </div>
</template>

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
