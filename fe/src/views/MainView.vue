<template>
    <v-app >
        <v-app-bar app>
            <v-toolbar-title>Drone Lover  </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn text @click="goTo('/slm')">404</v-btn>
            <v-btn text @click="goTo('/dashboard')">Dashboard</v-btn>
            <v-btn text @click="goTo('/admin')">Secret</v-btn>
            <v-btn @click="logout">Çıkış</v-btn>

        </v-app-bar>

        <v-main class="fill-height">
            <v-container class="fill-height">
                <router-view></router-view>
            </v-container>
        </v-main>
    </v-app>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const store = useStore();
const router = useRouter();

const goTo = (routeName: string) => {
    router.push({ path: routeName });
};

const logout = async () => {
  try {
    await store.dispatch('auth/logout');
    router.push('/login'); 
  } catch (error) {
    console.error('Logout failed', error);
  }
};
</script>

<style scoped>
</style>