<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>Drones List</v-card-title>
          <v-card-text>
            <v-data-table :headers="headers" :items="drones" class="elevation-1" item-value="id">
              <template v-slot:top>
                <v-toolbar flat>
                  <v-toolbar-title>Drones</v-toolbar-title>
                  <v-divider class="mx-4" inset vertical></v-divider>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" @click="openDialog">Add Drone</v-btn>
                </v-toolbar>
              </template>
              <template v-slot:[`item.status`]="{ item }">
                <v-chip :color="getStatusColor(item.status)" dark>
                  {{ item.status }}
                </v-chip>
              </template>
              <template v-slot:[`item.actions`]="{ item }">
                <v-btn icon @click="openEditDialog(item)" class="mr-2">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="confirmDelete(item.id)">
                  <v-icon color="error">mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
            <v-progress-circular v-if="loading" indeterminate color="primary"></v-progress-circular>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <AddDroneDialog ref="addDroneDialog" :initialDrone="null" @close="onDialogClose" />
    <AddDroneDialog ref="editDroneDialog" :initialDrone="selectedDrone" @close="onDialogClose" />

    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">Confirm Delete</span>
        </v-card-title>
        <v-card-text>
          Are you sure you want to delete this drone?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="deleteDialog = false">No</v-btn>
          <v-btn color="red darken-1" text @click="deleteDrone">Yes</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import AddDroneDialog from './Dialogs/AddDroneDialog.vue';
import { Drone } from '@/api/modules/drone'

const store = useStore();

const headers = [
  { title: 'ID', value: 'id' },
  { title: 'Name', value: 'name' },
  { title: 'Model', value: 'model' },
  { title: 'Status', value: 'status' },
  { title: 'Actions', value: 'actions', sortable: false }

];

const drones = computed(() => store.getters['drones/allDrones']);
const loading = computed(() => store.getters['drones/isLoading']);
const error = computed(() => store.getters['drones/error']);

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

const addDroneDialog = ref<InstanceType<typeof AddDroneDialog>>();
const editDroneDialog = ref<InstanceType<typeof AddDroneDialog>>();
const selectedDrone = ref(null);


const deleteDialog = ref(false);
const confirmDeleteId = ref<number | null>(null);
const confirmDelete = (droneId: number) => {
  confirmDeleteId.value = droneId;
  deleteDialog.value = true;
};
const onDialogClose = () => {
  selectedDrone.value = null;
};

const openDialog = () => {
  addDroneDialog.value?.openDialog();
};

const openEditDialog = (drone: any) => {
  selectedDrone.value = drone;
  editDroneDialog.value?.openDialog();
};

const deleteDrone = async () => {
  deleteDialog.value = false;
  if (confirmDeleteId.value !== null) {
    await store.dispatch('drones/deleteDrone', confirmDeleteId.value);
  }
};

onMounted(() => {
  store.dispatch('drones/fetchDrones');
});
</script>

<style scoped>
.v-container {
  height: 100vh;
}
</style>