<template>
  <div class="image-uploader">
    <input type="file" @change="onFileChange" accept="image/*" />
    <div v-if="imageUrl" class="preview">
      <img :src="imageUrl" alt="Image Preview" />
    </div>
    <button v-if="imageUrl" @click="uploadImage">Upload Image</button>
    <p v-if="uploadStatus">{{ uploadStatus }}</p>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import axios from 'axios';

export default {
  name: 'ImageUploader',
  setup() {
    const imageUrl = ref<string | null>(null);
    const uploadStatus = ref<string | null>(null);

    const onFileChange = (event: Event) => {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files.length > 0) {
        const file = target.files[0];
        imageUrl.value = URL.createObjectURL(file);
      }
    };

    const uploadImage = async () => {
      if (!imageUrl.value) return;

      const formData = new FormData();
      const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
      if (fileInput.files) {
        formData.append('file', fileInput.files[0]);
      }

      try {
        const response = await axios.post('/api/v1/members/assets', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        uploadStatus.value = 'Upload successful: ' + response.data.url;
      } catch (error) {
        uploadStatus.value = 'Upload failed: ' + error.message;
      }
    };

    return {
      imageUrl,
      uploadStatus,
      onFileChange,
      uploadImage,
    };
  },
};
</script>

<style scoped>
.image-uploader {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.preview {
  margin-top: 10px;
}

img {
  max-width: 100%;
  height: auto;
}
</style>