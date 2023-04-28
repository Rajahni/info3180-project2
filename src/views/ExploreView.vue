<script setup>
import { ref, onMounted } from "vue";
// define a reactive property to hold the post data
let posts = ref([]);
function fetchPosts() {
    fetch("/api/v1/posts", {
        method: 'GET'
    })
    .then((response) => response.json())
    .then((data) => {
        // update the posts reactive property with the data
        posts.value = data.posts;
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
  <div class="container">
    <div class="post-list">
      <div class="post" v-for="post in posts" :key="post.id">
        <div class="user-info">
          <img :src="post.user.profile_photo" alt="Profile Photo">
          <span class="username">{{ post.user.username }}</span>
        </div>
        <div class="post-image">
          <img :src="post.photo" alt="Post Photo">
        </div>
        <div class="post-info">
          <span class="caption">{{ post.caption }}</span>
          <div class="likes-date">
            <span class="likes">{{ post.likes }} likes</span>
            <span class="date">{{ post.created_on }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="new-post">
      <button @click="newPost">New Post</button>
    </div>
  </div>
</template>

<style>
.post-list {
  justify-content: space-between;
  margin-bottom: 20px;
}

.post {
  margin-bottom: 20px;
  width: 100%;
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
}

.username {
  font-weight: bold;
}

.post-image img {
  max-width: 100%;
}

.caption {
  font-weight: bold;
}

.likes-date {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.likes {
  font-weight: bold;
}

.date {
  font-style: italic;
}

.create-post {
  display: flex;
  justify-content: flex-end;
}
</style>