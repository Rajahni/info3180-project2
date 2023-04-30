<template>
  <div class="profile-container">
    <div v-for="u in user" :key="u.id" class="profile-info">
      <div class="pp-container">
        <img :src="u.profile_photo" class="pp" alt="profile picture" />
      </div>
      <div class="info-container">
        <h3>{{ u.firstname }} {{ u.lastname }}</h3>
        <p>{{ u.location }}</p>
        <p>Member since {{ u.joined_on }}</p>
        <p class="para">{{ u.biography }}</p>
      </div>
    </div>
    <div class="stats-panel">
      <div class="stats">
        <h6 class="count">{{ u.posts }}</h6>
        <span>Posts</span>
      </div>
      <div class="stats">
        <h6 class="count">{{ u.followers }}</h6>
        <span>Followers</span>
      </div>
    </div>
    <div class="follow-btn">
      <button @click="follow">{{ isFollowing ? 'Unfollow' : 'Follow' }}</button>
    </div>
  </div>
  <div class="image-grid-container">
    <div class="image-grid">
      <div v-for="post in posts" :key="post.id" class="image-grid-item">
        <img :src="post.photo" alt="Uploaded photo"/>
        <!-- <div v-for="post in posts" :key="post.id">
          <img :src="post.photo" alt="Post Photo" />
          <p>{{ post.caption }}</p>
          <p>{{ post.created_on }}</p>
          <p>{{ post.likes }} likes</p>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let user = ref({});
let posts = ref([]);
let user_id = ref(null);
let csrf_token = ref("");
let isFollowing = ref(false);

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
        csrf_token.value = data.csrf_token;
    })
}


function getUser(user_id){
  fetch(`/api/v1/users/${user_id}`, {  
        method: 'GET'
    })
    .then((response) => response.json())
    .then((data) => {
      user.value = data.user;
      user_id.value = data.user_id;

      follow(user.value.id, current_user_id.value);
    })
    .catch((error) => {
      console.log(error);
    });
}

function getPosts(){
  fetch(`/api/v1/users/${user_id.value}/posts`, { 
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      posts.value = data.posts;
    })
    .catch(error => {
      console.log(error);
    });
}

function follow(user_id, follower_id) {
  fetch(`/api/users/${user_id}/follow`, { 
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': csrf_token.value
    },
    body: JSON.stringify({ id: user_id, follower_id: follower_id }),
  })
    .then((response) => {
      if (response.ok) {
        isFollowing.value = !isFollowing.value;
        return response.json();
      } else {
        throw new Error("Failed to follow user");
      }
    })
    .then((data) => {
      console.log(data.message);
    })
    .catch((error) => {
      console.log(error.message);
    });
}

onMounted(() => {
  getCsrfToken();
  getUser(user_id.value);
  getPosts();
});

</script>

<style>
/* add your styling here */
</style>