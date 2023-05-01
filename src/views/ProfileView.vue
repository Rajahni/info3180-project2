<template>
  <div class="profile-container">
    <div class="col-lg-8">
      <div v-for="user in user_data" class="profile-info">
        <div class="row g-0">
          <div class="col-sm-3">
            <img :src="user.profile_photo" class="pp" alt="Profile Picture" />
          </div>
          <div class="col-6">
            <div class="name-container">
              <h3>{{ user.firstname }} {{ user.lastname }}</h3>
              <p>{{ user.location }}</p>
              <p class="bio">{{ user.biography }}</p>
              <p>Member since {{ user.joined_on }}</p>
            </div>
          </div>
          <div class="col-3">
            <div class="stats-panel">
              <div class="stats">
                <h6 class="count">1</h6>
                <span>Posts</span>
              </div>
              <div class="stats">
                <h6 class="count">99</h6>
                <span>Followers</span>
              </div>
            </div>
            <div class="follow-btn">
              <button :class="{ followed: user.followed }" @click="follow(user)">{{ isFollowing ? 'Following' : 'Follow' }}</button>
              <!-- <button :class="{ 'followed': isFollowing }" @click="follow">{{ isFollowing ? 'Following' : 'Follow' }}</button> -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="image-grid-container">
    <div class="image-grid">
      <div v-for="post in posts" :key="post.id" class="image-grid-item">
        <img :src="post.photo" alt="Uploaded photo"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
// // let user = ref("");
// // let user_id = ref("");
let follow = ref
let user_data = ref([]);
//let isFollowing = ref(false);
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

function follow(user_id, follower_id)  {
  fetch("/api/users/{user_id}/follow", { 
    method: "POST",
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.ok) {
        isFollowing.value = !isFollowing.value;
        console.log(data)
        return response.json();
      } else {
        throw new Error("Failed to follow user");
      }
    })
    .catch((error) => {
      console.log(error.message);
    });
}
onMounted(() => {
  getCsrfToken();
  getUser();
  getPosts();
  //follow();
});
</script>

<style>
.image-grid-container {
  /* margin-top: 5%; */
  margin: 0 auto;
  width: 50%;
  height: 570px;

  /* border: 1px solid black; */
}

.image-grid-item {
  margin-top: 5%;
  padding: 2%;
  /* border: 1px solid black; */
}

.image-grid-item img {
  width: 50%;
  height: 50%;
}

.profile-container {
    margin: 0 auto;
    width: 50%;
    height: 570px;
    border-radius: 4px;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    padding: 0;
} 

.profile-info {
  display: flex;
  /* border: 1px solid black; */
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.pp {
  width: 200px;
  height: 200px;
  margin-bottom: 10px;
  margin-top: 15px;
}

.name-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.name-container h3 {
  font-weight: bold;
  margin-bottom: none;
  padding-bottom: none;
}

.name-container p {
  padding: none;
  margin: none;
}

.stats-panel {
    display: flex;
    justify-content: space-between; 
    align-items: center;
    margin-bottom: 15px;
}

.stats {
  margin-right: 20px;
  margin-left: 25px;
}

.count {
    font-weight: bold;
    font-size: 20px;
    text-align: center;
    margin-bottom: 0;
}

.bio {
  margin: 0 20px;
  padding: 0;
}

.f-btn {
  width: 250px;
}

.followed {
  background-color: green;
  color: white;
}
</style>
