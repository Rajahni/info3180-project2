<script setup>
import { ref, onMounted } from "vue";
let posts = ref([]);

function fetchPosts() {
    fetch("/api/v1/users/{user_id}/posts", {
        method: 'GET'
    })
    .then((response) => response.json())
    .then((data) => {
      posts.value = data.posts.map(post => {
        if (post.user === null) {
          post.user = {
            profile_photo: "",
            username: ""
          }
        }
        else if (!post.user) {
          post.user = {
            profile_photo: "",
            username: "Unknown User"
          }
        }
        post.liked = false;
        return post;
      });
    })
    .catch((error) => {
        console.log(error);
    });
}

function likePost(post) {
  fetch("/api/v1/posts/post_id/like", {
    method: 'POST'
  })
  .then((response) => response.json())
  .then(function (data) {
    if (!post.liked) {
      post.liked = true;
      post.likes += 1;
      console.log(data);
    }
  })
  .catch((error) => {
    console.log(error);
  });
}

onMounted(() => {
    fetchPosts();
});
</script>

<template>
  <div class="explore-container">
    <div class="post-list">
      <div class="post" v-for="post in posts" :key="post.id">
        <div class="user-info">
          <img :src="post.user.profile_photo" alt="Profile Photo" class="profile-photo">
          <span class="username">{{ post.user.username }}</span>
        </div>
        <div class="post-image">
          <img :src="post.photo" alt="Post Photo" class="post-photo">
        </div>
        <div class="post-info">
          <span class="caption">{{ post.caption }}</span>
          <div class="likes-date">
            <span class="heart-icon" :class="{ liked: post.liked }" @click="likePost(post)">
              <svg class="heart" viewBox="0 0 32 29.6">
                <path d="M23.6,0c-3.4,0-6.3,2.7-7.6,5.6C14.7,2.7,11.8,0,8.4,0C3.8,0,0,3.8,0,8.4c0,9.4,9.5,11.9,16,21.2
              c6.1-9.3,16-12.1,16-21.2C32,3.8,28.2,0,23.6,0z"/>
            </svg>
            </span>
            <span class="likes">{{ post.likes }} likes</span>
            <span class="date">{{ post.created_on }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="new-post">
      <a href="/posts/new"><button class="newpost">New Post</button></a>
    </div>
  </div>
</template>

<style>
.explore-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  justify-content: flex-end;
}

.post-list {
  justify-content: space-between;
  margin-bottom: 20px;
}

.post {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #bbbab8;
  border-radius: 6px;
  box-shadow: 0px 4px 10px 2px #bbbab8;
  background-color: white;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.user-info img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
}

.username {
  font-weight: bold;
}

.post-image img {
  width: 100%;
  height: 100%;
  margin-bottom: 10px;
}

.likes-date {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.heart-icon {
  display: inline-block;
  cursor: pointer;
}

.heart {
  fill: lightgray;
  position: relative;
  width: 20px;
  animation: pulse 1s ease infinite;
}

.heart.liked {
  fill: red;
}

/* @keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); }
} */

.likes {
  font-weight: bold;
  margin-right: 225px;
}

.date {
  font-style: italic;
}

.new-post {
  margin-left: 30px;
}
</style>