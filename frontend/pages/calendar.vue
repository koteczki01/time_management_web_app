<template>
  <div class="top-bar">
    <div class="left-top-bar">
      <img src="public/image.png" alt="Quanta logo" class="logo">
      <h1>Quanta</h1>
    </div>
    <div class="right-top-bar">
      <button class="plus">+</button>
      <h1>Add</h1>
    </div>
  </div>
  <div class="calendar-bar">
    <div class="friends">
      <h1>Friends</h1>
    </div>
    <div>
    <h1>Monday</h1>
    </div>
    <div>
    <h1>Tuesday</h1>
    </div>
    <div>
    <h1>Wednesday</h1>
    </div>
    <div>
    <h1>Thursday</h1>
    </div>
    <div>
    <h1>Friday</h1>
    </div>
    <div>
    <h1>Saturday</h1>
    </div>
    <div>
    <h1>Sunday</h1>
    </div>
  </div>
  <div class="friends_names">
    <div class="name" v-for="friend in numberOfFriends" :key="friend">
      Natalia
    </div>
  </div>

</template>

<style>
body{
  margin: 0;
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
.top-bar h1,
.top-bar plus {
  color: #fff;
  -webkit-text-stroke: 1px rgb(85, 68, 76);
  text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
 
}
.logo{
  height: 60px;
  margin: 20px;
}
.left-top-bar{
  font-size: 1.7rem;
  width: 100%;
  height: 10%;
  background-color: #FFE8E8;
  display: flex;
  font-family: 'Lao Muang Don', sans-serif;
  justify-content: left;
  align-items: center;
}
.right-top-bar{
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
.calendar-bar{
  display: flex;
  align-items: flex-start;
}
.calendar-bar div:not(.friends) {
  border-right: 2px solid #CCB2C6;
  border-bottom: none;
  display: flex;
  justify-content: center;
  width: 12.4%;
}
.calendar-bar div h1{
  -webkit-text-stroke: 1px rgb(85, 68, 76);
  text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
  font-family: 'Lao Muang Don', sans-serif;
  color: #fff;
  font-size: 1.7rem;
}
.friends{
  background-color: #FFE8E8;
  width:12.5%;
  border-right: 2px solid #CCB2C6;
  border-bottom: none;
  display: flex;
  justify-content: center;
}
.friends_names {
  border-right: 2px solid #CCB2C6;
  width: 12.5%;
  color: white;
  -webkit-text-stroke: 1px rgb(85, 68, 76);
  text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
  font-family: 'Lao Muang Don', sans-serif;
  background-color: #FFE8E8;
  padding: 0;
  margin: 0;
}
.name {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding-bottom: 5px;
  margin-bottom: 10px;
  height: 33.33vh;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
  font-size: 1.6rem;
  background-color: #cfb2d4;
}
</style>

<script lang="ts">
  import { defineComponent } from 'vue';

  export default defineComponent({
    data() {
      return {
        numberOfFriends: 3
      };
    }
  });
</script>