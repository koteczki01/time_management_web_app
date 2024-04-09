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
</template>

<style scoped>
.auth-container {
  opacity: 0.5;
  display: flex;
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
  border-bottom: 2px solid #42A5F5;
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
  height: 30px;
  background-color: #FFF8F8;
  border-top: 2px solid #42A5F5;
}

.auth-card {
  display: flex;
  margin: 48px 0px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #FEEAEAEA;
  padding: 2rem;
  border-radius: 20px;
  border: 1px solid #ccc;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
