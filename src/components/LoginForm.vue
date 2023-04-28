<template>
    <div style="display: flex; justify-content: center;">
        <form @submit.prevent="login" method="post" enctype="multipart/form-data" id="loginForm" style="width: 400px;">
            <h2>Login</h2>
            <div
                v-if="displayFlash"
                v-bind:class="[isSuccess ? alertSuccessClass : alertErrorClass]"
                class="alert">
                {{ flashMessage }}
            </div>
            <label for="username" class="form-label">Enter Username</label>
            <input v-model="username" type="text" name="username" id="username" class="form-control">

            <label for="password" class="form-label">Enter Password</label>
            <input v-model="password" type="password" name="password" id="password" class="form-control">

            <button class="btn btn-lg btn-primary w-100 mt-3" type="submit">Login</button>
        </form>
    </div>
</template>
<script setup>
    import { ref, onMounted } from "vue";
    let csrf_token = ref("");
    let username = ref("");
    let password = ref("");

    // flash elements
    let flashMessage = ref("");
    let displayFlash = ref(false);
    let isSuccess = ref(false);
    let alertSuccessClass = ref("alert-success");
    let alertErrorClass = ref("alert-danger");
    onMounted(() => {
        getCsrfToken();
    });

    function getCsrfToken() {
        fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
        })
    }
    
    function clearFormFields() {
        username.value = "";
        password.value = "";
    }

    function login() {
        let loginForm = document.getElementById("loginForm");
        let form_data = new FormData(loginForm);
        fetch("/api/v1/auth/login", {
            method: 'POST', 
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value
            }
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
      console.log(data);
      if ("errors" in data) {
        flashMessage.value = [...data.errors];
        isSuccess.value = false;
        displayFlash.value = true;
        } 
      else {
        displayFlash.value = true;
        isSuccess.value = true;
        flashMessage.value = "Login successful";
        clearFormFields();
        console.log(data);
        }
        
        })
        .catch(function (error) {
            console.log(error);
        });
    }
</script>