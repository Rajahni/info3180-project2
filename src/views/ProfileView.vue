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
          <img :src="image.url" alt="uplaoded photo"/>
        </div>
      </div>
      </div>
    </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  setup() {
    // define a reactive property to hold the user data
    const user = ref(null);
    // define a reactive property to track whether the current user is following the profile
    const isFollowing = ref(false);

    // fetch user data from the server on component mount
    onMounted(() => {
      fetch("/api/v1/users/1") // replace 1 with the user id of the current profile being viewed
        .then((response) => response.json())
        .then((data) => {
          user.value = data.user;
        })
        .catch((error) => {
          console.log(error);
        });
    });

    return { user, isFollowing };
  },
};
</script>

<style>
/* add your styling here */
</style>

<style>
/* add your styling here */
</style>

  