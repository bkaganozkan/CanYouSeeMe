<template>
    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="headline">All Images for Task</span>
        </v-card-title>
        <v-card-text>
          <v-carousel>
            <v-carousel-item v-for="image in allImages" :key="image.id">
              <v-img :src="image.image_path" aspect-ratio="1.75"></v-img>
            </v-carousel-item>
          </v-carousel>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, defineProps, defineEmits } from 'vue';
  import { useStore } from 'vuex';
  
  const props = defineProps<{
    showDialog: boolean;
    taskId: number;
  }>();
  
  const emit = defineEmits(['close']);
  
  const store = useStore();
  
  const dialog = computed({
    get: () => props.showDialog,
    set: (value) => emit('close', value)
  });
  
  const allImages = computed(() => {
    const task = store.getters['tasks/getTaskById'](props.taskId);
    if (task) {
      return task.drones.flatMap((drone: any) => drone.images);
    }
    return [];
  });
  
  const closeDialog = () => {
    dialog.value = false;
  };
  </script>
  
  <style scoped>
 
  </style>
  