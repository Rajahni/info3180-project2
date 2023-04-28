<template>
    <div class="logout-page">
        <div
            v-if="errorMessage"
            class="alert alert-danger">
            {{ errorMessage }}
        </div>

        <div
            v-if="successMessage"
            class="alert alert-success">
            {{ successMessage }}
        </div>

        <div class="logout-box">
        
        <h1>Logging Out?</h1>
        <p>Are you sure you want to logout?</p>
        <button @click="logout()">Yes</button>
        <a href="/"><button >NO</button></a>

        </div>
    </div>

</template>

<script setup>
import { ref, onMounted } from "vue";

let loggedIn = ref(false);
let csrf_token = ref("");
let errorMessage = ref("");
let successMessage = ref("");

function getCsrfToken() {
    
    fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
    })
 }

function logout(){
    fetch("/api/v1/auth/logout", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token.value
            },
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            loggedIn.value = true;
            successMessage.value = "Logout Successful";
            window.location.href = '/';
        })
        .catch(function (error){
            console.log(error);
            errorMessage.value = "Logout Unsuccessful. Please Try Again";
        });

}

onMounted(() => {
        getCsrfToken();
    });

</script>

<style>
.logout-page{
    display: flex;
    align-items: center;
    justify-content: center;
    height: 350px;

}

.logout-box{
    border: 1px solid black;
    padding: 1rem;
    text-align: center;
}

.button{
    margin-top: 1rem;
}
</style>