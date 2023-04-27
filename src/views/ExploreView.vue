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
    <div class="post">
      <div class="post-header">
        <img :src="userPhoto" alt="User Photo">
        <h3>{{ username }}</h3>
      </div>
      <img :src="photo" alt="Post Photo">
      <div class="post-footer">
        <i :class="{ 'fas fa-heart': liked, 'far fa-heart': !liked }" @click="like"></i>
        <span>{{ likes }}</span>
        <p>{{ createdOn }}</p>
      </div>
    </div>
  </template>

<style>
.post {
  border: 1px solid #dbdbdb;
  border-radius: 3px;
  margin-bottom: 20px;
  background-color: #fff;
}

.post img {
  width: 100%;
}

.post-header {
  display: flex;
  align-items: center;
  padding: 10px;
}

.post-header img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
}

.post-header h3 {
  font-size: 14px;
}

.post-footer {
  display: flex;
  align-items: center;
  padding: 10px;
}

.post-footer i {
  font-size: 20px;
  color: #dbdbdb;
  margin-right: 10px;
  cursor: pointer;
}

.post-footer i:hover {
  color: #ed4956;
}

.post-footer span {
  font-size: 14px;
  margin-right: 10px;
}

.post-footer p {
  font-size: 14px;
}
</style>