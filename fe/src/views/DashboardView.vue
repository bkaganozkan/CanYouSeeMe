<template>
  <v-container fluid class="py-5">
    <v-row>
      <v-col cols="12" md="6">
        <v-card class="pa-4">
          <v-card-title class="subtitle-1">Drone List</v-card-title>
          <drone-list />
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card class="pa-4">
          <v-card-title class="subtitle-1">Task List</v-card-title>
          <task-list />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import DroneList from '@/components/DroneList.vue';
import TaskList from '@/components/TaskList.vue';
</script>

<style scoped>
.headline {
  font-size: 2rem;
  font-weight: bold;
}

.subtitle-1 {
  font-size: 1.25rem;
}

.pa-4 {
  padding: 16px;
}
</style>