<template>
    <h1>HI</h1>

    <div v-if="errorMessage" class="alert alert-danger">
        <ul>
            <li v-for="error in errorMessage">{{ error }}</li>
        </ul>
    </div>

    <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

    <form id="newPost" @submit.prevent="uploadPost">

        <div class="form-group mb-3">
        <label for="photo" class="form-label">Photo</label>
        <input
            id="photo"
            type="file"
            name="photo"
            accept="image/png, image/jpeg, image/jpg"
            class="formcontrol"
        />
        </div>

        <div class="form-group mb-3">
            <label for="caption" class="form-label">Caption</label>
            <textarea 
                v-model="text" 
                placeholder="Write a caption..."
                id="caption"
                name="caption" 
                class="formcontrol" 
            >
            </textarea>
        </div>

        

        <button class="btn btn-primary" type="submit">Submit</button>


    </form>


</template>

<script setup>
import { ref, onMounted } from "vue";
let csrf_token = ref("");
let errorMessage = ref("");
let successMessage = ref("");

onMounted(() => {
    getCsrfToken();
});

function uploadPost(){

let newPost = document.getElementById('newPost');
let form_data = new FormData(newPost);

fetch("/api/v1/users/{user_id}/posts", {
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
        
        if ("errors" in data){
            errorMessage.value = [...data.errors];
        } else {
            successMessage.value = "Successfully created a new post";
            resetFormFields();
        }

        console.log(data);
    })
    .catch(function (error) {
        console.log(error);
    });


}

function resetFormFields(){
    errorMessage.value = "";
    photo.value = "";
    caption.value = "";
}

function getCsrfToken() {
    
    fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
    })
}


</script>