<template>
    <div class="register-form-container">
        <h2>Register</h2>
        <div
            v-if="displayFlash"
            v-bind:class="[isSuccess ? alertSuccessClass : alertErrorClass]"
            class="alert">
            {{ flashMessage }}
        </div>
  
        <form @submit.prevent="saveUser" method="post" enctype="multipart/form-data" id="userForm">
            
            <label for="username" class="form-label">Username</label>
            <input type="text" name="username" id="username" class="form-control" >
        
            <label for="pasword" class="form-label">Password</label>
            <input type="text" name="password" id="password" class="form-control" >
        
            <label for="firstname" class="form-label">First Name</label>
            <input type="text" name="firstname" id="firstname" class="form-control" >
            
            <label for="lastname" class="form-label">Last Name</label>
            <input type="text" name="lastname" id="lastname" class="form-control" >
        
            <label for="email" class="form-label">Email</label>
            <input type="email" name="email" id="email" class="form-control" >
        
            <label for="location" class="form-label">Address</label>
            <input type="text" name="location" id="location" class="form-control" >
        
            <label for="biography" class="form-label">Biography</label>
            <textarea type="text" name="biography" id="biography" class="form-control" cols="30" rows="5" ></textarea>
        
            <label for="profile_photo" class="form-label">Photo</label>
            <input type="file" name="profile_photo" id="profile_photo" class="form-control" >
            
            <button type="submit" class="register-btn">Register</button>
        </form>
    </div>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    let csrf_token = ref("");
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
        firstname.value = "";
        lastname.value = "";
        email.value = "";
        location.value = "";
        biography.value = "";
        profile_photo.value = "";
    }
    function saveUser() {
        let userForm = document.getElementById("userForm");
        let form_data = new FormData(userForm);
        fetch("/api/v1/register", {
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
        flashMessage.value = "User added successfully!";
        clearFormFields();
        console.log(data);
        }
        
        })
        .catch(function (error) {
            console.log(error);
        });
    }
</script>

<style>
  .register-form-container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  h2 {
    margin-top: 2rem;
    margin-bottom: 2rem;
    font-size: 2rem;
    font-weight: bold;
  }

  .form-label {
    margin-top: 1rem;
    display: block;
    font-weight: bold;
  }

  .form-control {
    margin-top: 0.5rem;
    width: 100%;
    padding: 0.5rem;
    font-size: 1rem;
    border-radius: 0.3rem;
    border: 1px solid #ccc;
  }

  .register-btn {
    margin-top: 1rem;
    width: 100%;
    background-color: #25c206;
    color: white;
    font-size: 1rem;
    border-radius: 0.3rem;
    border: none;
    padding: 0.5rem;
    cursor: pointer;
  }

  .register-btn:hover {
    background-color: #1e9107;
  }
</style>