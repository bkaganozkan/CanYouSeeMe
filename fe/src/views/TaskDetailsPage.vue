<template>
  <v-container v-if="!loading && taskFromStore" fluid class="fill-height pa-0">
    <v-row no-gutters class="fill-height">
      <v-col class="fill-height">
        <v-card-title class="d-flex align-center justify-space-between">
          <div>{{ taskFromStore.task_name }}</div>
          <div>
            <span class="mr-4">{{ taskFromStore.status }}</span>
          </div>
        </v-card-title>
        <v-row class="fill-height">
          <v-col cols="12" md="8" class="">
            <TaskImages :taskId="taskId" />
          </v-col>
          <v-col cols="12" md="4" class="pa-4">
            <v-card class="fill-height d-flex flex-column">
              <v-card-text>
                <v-data-table v-if="assignedDrones" :headers="droneHeaders" :items="assignedDrones"
                  class="elevation-2 fill-height">
                  <template v-slot:[`item.status`]="{ item }">
                    <v-chip :color="getStatusColor(item.status)" dark>
                      {{ item.status }}
                    </v-chip>
                  </template>
                </v-data-table>
              </v-card-text>
              <v-card-actions class="flex justify-space-between">
                <v-btn color="blue" @click="openEditDialog">Edit Task</v-btn>
                <v-btn @click="showAllImages">See All Images</v-btn>
                <v-btn color="red" @click="executeTask">EXECUTE</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
        <v-card class="mt-4">
          <v-card-title>Description of Task</v-card-title>
          <v-card-text>{{ taskFromStore.description }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <TaskImagesCarousel :show-dialog="showCarousel" :task-id="taskFromStore.id" @close="showCarousel = false" />
    <AddTaskDialog :showDialog="showAddTaskDialog" :initialTask="currentTask" @close="closeAddTaskDialog"
      @save="closeAddTaskDialog" />
  </v-container>
  <div v-else>Loading...</div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, defineProps } from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';

import AddTaskDialog from '@/components/Dialogs/AddTaskDialog.vue';
import TaskImages from '@/components/TaskDetailsComponent/TaskImages.vue';
import TaskImagesCarousel from '@/components/Dialogs/TaskImagesCarousel.vue';

const store = useStore();
const route = useRoute();

const loading = ref(false);
const error = ref<string | null>(null);

const props = defineProps<{
  id: number;
}>();

const taskId = computed(() => Number(route.params.id));
const taskFromStore = computed(() => store.getters['tasks/getTaskById'](taskId.value));
const assignedDrones = computed(() => store.getters['drones/getDronesByTaskId'](taskId.value));

const showAddTaskDialog = ref(false);
const currentTask = ref({
  id: props.id,
  task_name: taskFromStore.value?.task_name,
  description: taskFromStore.value?.description,
  drones: taskFromStore.value?.drone_ids,
});

const showCarousel = ref(false);

const showAllImages = () => {
  showCarousel.value = true;
};


const droneHeaders = [
  { title: 'ID', value: 'id' },
  { title: 'Drone Name', value: 'name' },
  { title: 'Drone Model', value: 'model' },
  { title: 'Status', value: 'status' }
];

const getStatusColor = (status: string) => {
  switch (status) {
    case 'offline':
      return 'grey';
    case 'online':
      return 'green';
    case 'assigned':
      return 'blue';
    case 'on-mission':
      return 'orange';
    default:
      return 'grey';
  }
};

const openEditDialog = () => {
  currentTask.value = taskFromStore.value;
  showAddTaskDialog.value = true;
};

const closeAddTaskDialog = () => {
  showAddTaskDialog.value = false;
}

const fetchTask = async () => {
  loading.value = true;
  try {
    if (!taskFromStore.value) {
      await store.dispatch('tasks/fetchTaskById', taskId.value);
    }
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const executeTask = () => store.dispatch('tasks/executeTask', taskId.value)


watch(taskId, fetchTask);

onMounted(fetchTask);

</script>

<style scoped></style>