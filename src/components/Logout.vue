<template>
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

    <div class="logout-page">
        
        <div class="logout-box">
        
        <h1>Logging Out?</h1>
        <p>Are you sure you want to logout?</p>

        <div class="buttons">
            <button @click="logout()" class="btn btn-lg btn-primary">YES</button>
            <a href="/"><button class="btn btn-lg btn-primary ">NO</button></a>

        </div>
       

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
                'X-CSRFToken': csrf_token.value,
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            loggedIn.value = true;
            successMessage.value = "Logout Successful";
            localStorage.removeItem('token');
            window.location.href = '/';
        })
        .catch(function (error){
            console.log(error);
            errorMessage.value = "Logout Unsuccessful. Are you sure you are logged in?";
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
    padding: 300px;

}

.logout-box{
    border: 1px solid #bbbab8;
    border-radius: 6px;
    box-shadow: 0px 4px 10px 2px #bbbab8;
    padding: 1rem;
    text-align: center;
    background-color: white;
    width: 450px;
    height: 350px;
}

.button{
    margin-top: 1rem;
}

h1{
    padding-top: 40px;
    padding-bottom: 30px;
}

p{
    padding: 10px;
}

.button-container{
    display: flex;
    justify-content: space-between;
    margin-top: 1rem;
}
</style>