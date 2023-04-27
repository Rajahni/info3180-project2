<script setup>
import { ref } from "vue";

let message = ref("Hello World! This is Group B's Photogram app.")

</script>

<template>
  <div class="container">
    <div class="left">
      <img src="rbridge.jpg" alt="Photo">
    </div>
    <div class="right">
      <div class="logo">
        <img src="" alt="Photogram Logo">
        <h2>Photogram</h2>
      </div>
      <p>Share photos of your favourite moments with friends, family and the world.</p>
      <div class="buttons">
        <button class="register">Register</button>
        <button class="login">Login</button>
      </div>
    </div>
  </div>
</template>

<style>
.container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
}

.left img {
  width: 50%;
  height: auto;
}

.right {
  text-align: center;
  border: 1px solid black;
  width: 100%;
}

.logo img {
  width: 100px;
  height: 100px;
  display: inline-block;
  margin-right: 10px;
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