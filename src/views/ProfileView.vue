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

          <div v-for="post in posts" :key="post.id">
            <img :src="post.photo" alt="Post Photo" />
            <p>{{ post.caption }}</p>
            <p>{{ post.created_on }}</p>
            <p>{{ post.likes }} likes</p>
          </div>
        </div>
      </div>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
let user = ref("");
let user_id = ref("");
let isFollowing = ref(false);
let posts = ref([]);

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
    })
}

onMounted(() => {
  getCsrfToken();
  getUser();
  getPosts();
  getFollowers();
});

function getUser(){
  fetch("/api/v1/users/user_id", {
        method: 'GET'
    })
    .then((response) => response.json())
    .then((data) => {
      user_id.value = data.user_id;
    })
    .catch((error) => {
      console.log(error);
    });
}

function getPosts(){
  fetch("/api/v1/users/user_id/posts", {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      console.log(posts);
      posts.value = data.posts;
    })
    .catch(error => {
      console.log(error);
    });
}

function getFollowers(){
  fetch("/api/v1/users/user_id/follow")
    .then((response) => response.json())
    .then((data) => {
      isFollowing.value = data.isFollowing;
    })
    .catch((error) => {
      console.log(error);
    });
}

</script>

<style>
/* add your styling here */
</style>

