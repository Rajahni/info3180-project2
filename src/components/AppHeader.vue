<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-light fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/" style="display: flex; align-items: center;">
          <!-- <span class="nav-icon"><img alt="Photogram logo" class="nav-logo" src="logo.png"/></span> --> #should comment back in at some point before final push
          <span class="Nav-name">Photogram</span>
        </a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link" exact-active-class="active">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore" exact-active-class="active">Explore</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/users/user_id" exact-active-class="active">My Profile</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/login" exact-active-class="active">Login</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style>
nav{
  background-color: #4a90e2;
}

img{
  width: 60px;  
  height: 40px;
  padding-right: 5px;
  margin-top: 0;
}

.Nav-name {
  font-weight: bold;
  font-size: 27px;
  color: white;
}

.navbar-nav li a {
  color: white;
  font-weight: bold;
}
</style>