<template>
  <v-container class="d-flex fill-height items-center">
    <v-row flex align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card>
          <v-card-title class="headline">Login</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field v-model="username" label="Username" prepend-icon="mdi-account" required></v-text-field>
              <v-text-field v-model="password" label="Password" type="password" prepend-icon="mdi-lock"
                required></v-text-field>
              <v-card-actions class="d-flex justify-space-between">
                <v-btn text @click="goToRegister">Register</v-btn>
                <v-btn color="primary" type="submit">Login</v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
          <v-card-subtitle class="pt-0">
            <v-row class="d-flex  align-center pa-1">
              <v-col >
                <div>username: user<br>password: user</div>
              </v-col>
              <v-col>
                <div class="text-end">username: admin<br>password: admin</div>
              </v-col>
            </v-row>
          </v-card-subtitle>
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

const login = async () => {
  const user = username.value;
  const pass = password.value;
  await store.dispatch('auth/login', { username: user, password: pass });
  router.push('/dashboard');
};

const goToRegister = () => {
  router.push('/register');
};
</script>
