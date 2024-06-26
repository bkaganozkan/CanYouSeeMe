<template>
  <div>
    <v-container v-if="!loading && task" fluid class="pa-0" :style="containerStyle">
      <v-row no-gutters class="">
        <v-col cols="12" md="6" lg="4" v-for="drone in lastImages" :key="drone.drone_id" class="pa-2 d-flex">
          <v-card class="d-flex flex-column" style="min-height: 250px; width: 400px; max-width: 100%;">
            <v-card-title>
              Drone ID: {{ drone.drone_id }} - {{ drone.drone_name }}
            </v-card-title>
            <v-card-text class="d-flex flex-grow-1 justify-center align-center">
              <img v-if="drone.last_image" :src="drone.last_image.image_path" alt="Drone Image" class="w-100">
              <div v-else class="w-100 text-center">No image available</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <div v-else>Loading...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';

const store = useStore();
const route = useRoute();

const taskId = computed(() => {
  return Number(route.params.id)
});

const task = computed(() => store.getters['images/getRootTask']);
const loading = computed(() => store.getters['images/isLoading']);
const lastImages = computed(() => store.getters['images/getLastImagesByTaskId'](taskId.value));


onMounted(() => {
  store.dispatch('images/fetchTaskImages', taskId.value);
});

onUnmounted(() => {
  store.dispatch('images/stopSSE');
});

const containerStyle = computed(() => {
  const cardHeight = 300; // Her kartın yüksekliği (piksel cinsinden)
  const rows = Math.ceil(lastImages.value.length / 3); // Kartların satır sayısı
  return {
    maxHeight: `${rows * cardHeight}px`
  };
});
</script>

<style scoped>
.fill-height {
  height: 100vh;
}

.pa-0 {
  padding: 0;
}

.w-100 {
  width: 100%;
}
</style>
