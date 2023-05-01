<template>
  <div class="profile-container">
    <div v-for="user in user_data">
      <div class="card">
        <div class="row g-0">
          <div class="col-sm-3">
            <img
              :src="user.profile_photo"
              class="card-img-left"
              alt="Profile Picture"
            />
          </div>
          <div class="col-lg-7">
            <div class="card-body">
              <h5 id="name" class="card-title">
                {{ user.username }} {{ user.username }}
              </h5>
              <br />
              <p class="card-text">{{ user.location }} lorem epsom</p>
              <p class="card-text">
                Member since {{ user.joined }} lorem epsom
              </p>
              <p class="card-text">{{ user.bio }} lorem epsom</p>
            </div>
          </div>
          <div class="col-sm-2">
            <div class="card-body">
              <div class="row align-items-start">
                <div class="col">Posts_Num</div>
                <div class="col">Followers_Num</div>
                <div class="col">Post</div>
                <div class="col">Follows</div>
                <br />
                <br />
                <br />
                <a href="#" class="btn btn-primary">Follow</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <br />
    <div class="container text-center">
      <div class="row">
        <div class="col" v-for="post in posts" :key="post.id">
          <img :src="post.photo" alt="Post Photo" />
          <div class="row align-items-start">
            <div class="col">{{ post.likes }} likes</div>
            <div class="col">
              {{ post.created_on }}
            </div>
          </div>
          {{ post.caption }}
        </div>
      </div>
    </div>
  </div>

  <!--<img :src="user.profile_photo" class="pp" alt="Profile Picture" />
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
      </div>-->
</template>

<script setup>
import { ref, onMounted } from "vue";
// let user = ref("");
// let user_id = ref("");
let user_data = ref([]);
let isFollowing = ref(false);
let posts = ref([]);
let csrf_token = ref("");

function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      csrf_token.value = data.csrf_token;
    });
}

onMounted(() => {
  getCsrfToken();
  getUser();
  getPosts();
  getFollowers();
});

function getUser() {
  fetch("/api/v1/users/{user_id}", {
    method: "GET",
    headers: { "X-CSRFToken": csrf_token.value },
  })
    .then((response) => response.json())
    .then((data) => {
      user_data.value = data;
      //console.log(data)
    })
    .catch((error) => {
      console.log(error);
    });
}

function getPosts() {
  fetch("/api/v1/users/user_id/posts", {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(posts);
      posts.value = data.posts;
      console.log("posts", posts);
    })
    .catch((error) => {
      console.log(error);
    });
}

function getFollowers() {
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
img {
  height: 300px;
  width: 300px;
}
</style>
