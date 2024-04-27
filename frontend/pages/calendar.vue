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
    <div>
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
</template>

<style>
.top-bar {
  width: 100%;
  height: 70px;
  background-color: #FFF8F8;
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
  height: 50px;
  margin: 30px;
}
.left-top-bar{
  font-size: 1.7rem;
  width: 100%;
  height: 50px;
  background-color: #FFF6F6;
  display: flex;
  font-family: 'Lao Muang Don', sans-serif;
  justify-content: left;
  align-items: center;
}
.right-top-bar{
  width: 100%;
  height: 50px;
  background-color: #FFF6F6;
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
    border-radius: 20px;
    border: 0px;
    color: white;
    cursor: pointer;
    -webkit-text-stroke: 1px rgb(85, 68, 76);
    text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
    font-size: 3.3rem;
    padding: 0.3rem;
    display: flex;
    align-items: center;
    justify-content: center;
}
.calendar-bar{
    width: 100%;
    height: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-bottom: 2px solid #CCB2C6;
    widht: 1rem;
}
.calendar-bar div{
    border-right: 2px solid #CCB2C6;
    margin: 0px;
    width: 12.5%;
    height: 60px;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px;
}
.calendar-bar div h1{
    -webkit-text-stroke: 1px rgb(85, 68, 76);
    text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
    font-family: 'Lao Muang Don', sans-serif;
    color: #fff;
    font-size: 1.7rem;
}
</style>