<template>
    <div class="profile-container">
      <div class="profile-info">
        <img :src="user.profile_photo" class="pp" alt="Profile Picture" />
        <h3>{{ user.name }}</h3>
        <p>@{{ user.username }}</p>
        <p>{{ user.location }}</p>
        <p>Member since {{ user.joined }}</p>
      </div>
      <p class="para">{{ user.bio }}</p>
      <div class="stats-panel">
        <div class="stats">
          <h6 class="count">{{ user.posts }}</h6>
          <span>Posts</span>
        </div>
        <div class="stats">
          <h6 class="count">{{ user.following }}</h6>
          <span>Following</span>
        </div>
        <div class="stats">
          <h6 class="count">{{ user.followers }}</h6>
          <span>Followers</span>
        </div>
      </div>
      <div class="follow-btn">
        <button>{{ isFollowing ? 'Unfollow' : 'Follow' }}</button>
      </div>
      <div class="image-grid-container">
      <div class="image-grid">
        <div v-for="image in images" :key="image.id" class="image-grid-item">
          <img :src="image.url" alt="uploaded photo"/>
        </div>
      </div>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
const user = ref(null);
const isFollowing = ref(false);

onMounted(() => {
  fetch("/api/v1/users/${route.params.user_id}")
    .then((response) => response.json())
    .then((data) => {
      user.value = data.user;
      isFollowing.value = data.isFollowing;
    })
    .catch((error) => {
      console.log(error);
    });
});
</script>

<style>
/* add your styling here */
</style>


  