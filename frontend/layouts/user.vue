<template>
  <div class="top-bar">
    <div class="center-top-bar">
      <h1>Quanta</h1>
      <img src="public/image.png" alt="Quanta logo" class="logo">
    </div>
  </div>
  <div class="auth-container">
    <div class="auth-card">
      <slot />
    </div>
  </div>
  <footer>
    Quanta
  </footer>
</template>

<style scoped>
* {
  font-family: Arial, Helvetica, sans-serif;
}
.auth-container {
  opacity: 0.5;
  display: flex;
  min-height: 83.5vh;
  background-image: url('public/background.jpg');
  background-size: cover;
  align-items: center;
  justify-content: center;
}
.top-bar {
  width: 100%;
  height: 160px;
  background-color: #FFF8F8;
  display: flex;
  justify-content: center;
  align-items: center;
}
.top-bar h1 {
  color: #fff;
  font-size: 6rem;
  -webkit-text-stroke: 1px rgb(85, 68, 76);
  text-shadow: 2px 2px 2px rgb(85, 68, 76, 0.6);
}
.center-top-bar{
  width: 100%;
  height: 115px;
  background-color: #FFF6F6;
  display: flex;
  font-family: 'Lao Muang Don', sans-serif;
  justify-content: center;
  align-items: center;
  border: 2px solid #dccfda;
}
.logo{
  height: 100px;
  margin: 30px;
}
footer{
  width: 100%;
  height: 2rem;
  background-color: #FFF8F8;
  border-top: 2px solid #f3ebf1;
  color:#dccfda;
  text-align: center;

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
</style>
