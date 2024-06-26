<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card>
          <v-card-title class="headline">Register</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="register">
              <v-text-field v-model="username" label="Username" prepend-icon="mdi-account" required></v-text-field>
              <v-text-field v-model="password" label="Password" type="password" prepend-icon="mdi-lock"
                required></v-text-field>
              <v-card-actions class="d-flex justify-space-between">
                <v-btn text @click="goToLogin"> Login</v-btn>
                <v-btn color="primary" type="submit">Register</v-btn>
              </v-card-actions>
              <v-card-subtitle>
                <div>Already have an account?</div>
              </v-card-subtitle>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const username = ref('');
const password = ref('');
const store = useStore();
const router = useRouter();

const register = async () => {
  try {
    await store.dispatch('auth/register', { username: username.value, password: password.value });
    router.push('/dashboard'); 
  } catch (error) {
    console.error("Registration failed:", error);
    
  }
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.v-container {
  height: 100vh;
}
</style>
