<script setup lang="ts">
const numberOfFriends = ref(2)
const numberOfRows = ref(numberOfFriends)
</script>

<template>
  <div class="top-bar">
    <div class="left-top-bar">
      <img src="public/image.png" alt="Quanta logo" class="logo">
      <h1>Quanta</h1>
    </div>
    <div class="right-top-bar">
      <button class="plus">
        +
      </button>
      <h1>Add</h1>
    </div>
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
  </table>

  <table v-for="row in numberOfRows" id="main-table">
    <tr class="color">
      <td rowspan="5" class="box">
        <h1 id="name">
          <h1 />
          Natalia
        </h1>
      </td>
      <td>
        <div id="work">
          Work
        </div>
      </td> <td>
        <div id="work">
          Work
        </div>
      </td><td>
        <div id="work">
          Work
        </div>
      </td><td /><td /><td /><td />
    </tr>
    <tr>
      <td /> <td /><td /><td /><td /><td /><td />
    </tr>
    <tr class="color">
      <td /> <td /><td>
        <div id="work">
          Work
        </div>
      </td><td /><td /><td /><td />
    </tr>
    <tr>
      <td /> <td /><td /><td /><td /><td /><td />
    </tr>
    <tr class="color">
      <td /> <td /><td /><td /><td>
        <div id="work">
          Work
        </div>
      </td><td /><td />
    </tr>
    <tr id="gap">
      <td id="diff_color" />
      <td colspan="7" />
    </tr>
  </table>
</template>

<style>
body{
  margin: 0;
}
table, th, td,tr {
  border-right: 2px solid #CCB2C6;
  border-bottom: 2px solid #CCB2C6;
  text-align: center;
  -webkit-text-stroke: 1px rgb(85, 68, 76);
  text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
  font-family: 'Lao Muang Don', sans-serif;
  color: #fff;
  font-size: 1.7rem;
}

#work{
  background-color:#1569df39;
  border-radius:40px ;
}

table {
  border-collapse: collapse;
  width:100%;
}
td {
  height: 40px;
  width:12.5%;
}

.main-content {
  display: flex;
}
.box{
  background-color: #cfb2d4;
}
#main-table{
  border-collapse: collapse;
}
#diff_color{
  background-color: #FFE8E8;
}
.main-calendar{
  display:inline-grid;
  width:100%;
  grid-template-columns: repeat(8, 100px);
  grid-template-rows: repeat(auto-fill, 100px);
  /* border-right: 2px solid #CCB2C6; */
}
.color{
  background-color: #cfb2d439;
}
.gap{
  font-size: 65px;
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
#calendar-bar {
  display: table-cell;
  justify-content: center;
  width: 12.5%;
  font-size: 35px;
}
#friends{
  background-color: #FFE8E8;
  width: 12.5%;
  display: table-cell;
  justify-content: center;
  font-size: 35px;
}
#name {
  display: table-cell;
  justify-content: center;
  align-items: center;
  padding-bottom: 0;
  margin-left: 0;
  height: 33vh;
  font-size:40px;
  text-align: center;
  background-color: #cfb2d4;
}
</style>
