<template>
  <v-container class="fill-height d-flex align-center justify-center text-center">
    <v-row>
      <v-col>
        <v-card class="pa-4">
          <v-card-title class="headline">404 - Page Not Found</v-card-title>
          <v-card-text>
            The page you are looking for does not exist.
          </v-card-text>
          <v-card-actions class="d-flex justify-center">
            <v-btn color="primary" @click="goHome">Go to Home</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
  
  <script setup lang="ts">
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  const goHome = () => {
    router.push('/dashboard');
  };
  </script>
  
  <style scoped>
  .v-container {
    height: 100vh;
  }
  </style>