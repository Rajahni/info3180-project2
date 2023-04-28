<script setup>
import { ref } from "vue";

let message = ref("Hello World! This is Group B's Photogram app.")

</script>

<template>
  <div class="home-container">
    <div class="left">
      <img src="rbridge.jpg" alt="Photo">
    </div>
    <div class="right">
      <div class="logo">
        <img src="logo.png" alt="Photogram Logo">
        <h2>Photogram</h2>
        <hr>
      </div>
      <p>Share photos of your favourite moments with friends, family and the world.</p>
      <div class="buttons">
        <a href="/register"><button class="register">Register</button></a>
        <a href="/login"><button class="login">Login</button></a>
      </div>
    </div>
  </div>
</template>

<style>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 6%;
}

.left img {
  width: 500px;
  height: 500px;
} 

.left, .right {
  width: 500px;
  height: 500px;
  margin: 0 auto;
  border-radius: 4px;
}

.right {
  padding: 2%;
  text-align: center;
  margin-left: 10px;
  background-color: white;
  border: 1px solid #bbbab8;
  border-radius: 6px;
  box-shadow: 0px 4px 10px 2px #bbbab8;
}

.logo img {
  width: 70px;
  height: 50px;
  display: inline-block;
  vertical-align: middle;
}

h2 {
  display: inline-block;
  vertical-align: middle;
}

p {
  margin-top: 10px;
}

.buttons {
  margin-top: 20px;
  display: inline-block;
}

.register {
  background-color: #25c206;
}

.register:hover {
  background-color: #1e9107;
}

button {
  margin-right: 10px;
  padding: 10px 20px;
  border-radius: 4px;
  border: none;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
  width: 150px;
}

button:hover {
  background-color: #0062cc;
}
</style>