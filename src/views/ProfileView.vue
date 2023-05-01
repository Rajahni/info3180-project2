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

function getUser(){
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

function follow(user)  {
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

// function follow(user)  {
//   fetch("/api/users/{user_id}/follow", { 
//     method: "POST",
//     headers: {
//       'X-CSRFToken': csrf_token.value
//     }
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       if (!user.followed) {
//         isFollowing = true;
//         console.log(data);
//       } else {
//         throw new Error("Failed to follow user");
//       }
//     })
//     .catch((error) => {
//       console.log(error.message);
//     });
// }

onMounted(() => {
  getCsrfToken();
  getUser();
  getPosts();
  follow();
});
</script>

<style>
.image-grid-item {
  margin-top: 5%;
  padding: 2%;
}

.image-grid-item img {
  width: 400px;
  height: 300px;
}

.profile-container {
  padding: 2%;
  margin: 2%;
  box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
} 

.pp {
  width: 100%;
  height: 100%;
  margin-bottom: 10px;
}

.name-container {
  margin-top: 10%;
  margin-left: 10px;
}

.name-container h3 {
  font-weight: bold;
}

.stats {
  margin-right: 40px;
}

.stats-panel {
    display: flex;
    justify-content: space-between; 
    align-items: center;
    margin-bottom: 15px;
    margin-top: 40%;
    margin-left: 368px;
}

.count {
    font-weight: bold;
    font-size: 20px;
    text-align: center;
    margin-bottom: 0;
}

.follow-btn {
  margin-left: 365px;
}

.followed {
  background-color: green;
  color: white;
}
</style>
