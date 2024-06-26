<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="headline">{{ isEditMode ? 'Edit Drone' : 'Add New Drone' }}</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" v-model="valid">
          <v-text-field v-model="drone.name" label="Name" :rules="[rules.required]" required></v-text-field>
          <v-select v-model="drone.model" :items="droneItems" item-title="title" item-value="value" label="Model"
            :rules="[rules.required]" required></v-select>
          <v-select v-model="drone.status" :items="statusItems" item-title="title" item-value="value" label="Status"
            :rules="[rules.required]" required></v-select>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="closeDialog">Cancel</v-btn>
        <v-btn color="blue darken-1" text @click="submitForm">{{ isEditMode ? 'Update' : 'Save' }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, watch, defineEmits, defineExpose, computed, defineProps } from 'vue';
import { useStore } from 'vuex';

const props = defineProps<{
  initialDrone: {
    id?: number;
    name: string;
    model: string;
    status: string;
  } | null;
}>();

const emit = defineEmits(['close']);

const store = useStore();

const dialog = ref(false);
const valid = ref(true);
const formRef = ref(null);

const drone = reactive({
  id: props.initialDrone?.id || null,
  name: props.initialDrone?.name || '',
  model: props.initialDrone?.model || '',
  status: props.initialDrone?.status || ''
});

const droneItems = [
  { title: 'XA-1', value: 'XA-1' },
  { title: 'XA-2', value: 'XA-2' },
  { title: 'KF-1', value: 'KF-1' },
  { title: 'KF-2', value: 'KF-2' },
  { title: 'SB-1', value: 'SB-1' },
];

const statusItems = [
  { title: 'Offline', value: 'offline' },
  { title: 'Online', value: 'online' },
];

const rules = {
  required: (value: string) => !!value || 'Required.',
};

const isEditMode = computed(() => !!drone.id);

const openDialog = () => {
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
  drone.name = '';
  drone.model = '';
  drone.status = '';
  emit('close');
};

const submitForm = async () => {
  const form: HTMLFormElement | any = formRef.value;
  if (form) {
    const isValid = await form.validate();
    if (isValid.valid) {
      try {
        if (isEditMode.value) {
          await store.dispatch('drones/updateDrone', {
            droneData: {
              id: drone.id,
              name: drone.name,
              model: drone.model,
              status: drone.status,
            }
          });
        } else {
          await store.dispatch('drones/createDrone', {
            name: drone.name,
            model: drone.model,
            status: drone.status,
          });
        }
        closeDialog();
      } catch (error: any) {
        console.log(error)
      }
    }
  }
};

defineExpose({ openDialog });

watch(() => props.initialDrone, (newDrone) => {
  if (newDrone) {
    drone.id = newDrone.id || null;
    drone.name = newDrone.name;
    drone.model = newDrone.model;
    drone.status = newDrone.status;
  }
});
</script>

<style scoped></style>
