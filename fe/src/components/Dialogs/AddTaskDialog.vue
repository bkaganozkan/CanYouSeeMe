<template>
    <v-dialog v-model="dialog" max-width="600px">
        <v-card>
            <v-card-title>
                <span class="headline">{{ isEditMode ? 'Edit Task' : 'Add New Task' }}</span>
            </v-card-title>
            <v-card-text>
                <v-form ref="formRef" v-model="valid">
                    <v-text-field v-model="task.taskName" label="Task Name" :rules="[rules.required]"
                        required></v-text-field>
                    <v-textarea v-model="task.description" label="Description" :rules="[rules.required]"
                        required></v-textarea>
                    <v-select v-model="task.drones" :items="drones" label="Select Drones" item-title="name"
                        item-value="id" multiple></v-select>
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
import { ref, computed, defineProps, defineEmits, reactive, watch, defineExpose, onMounted } from 'vue';
import { useStore } from 'vuex';

const props = defineProps<{
    initialTask: {
        id?: number;
        task_name: string;
        description: string;
        drones: number[];
    } | null;
    showDialog: boolean;
}>();

const emit = defineEmits(['close', 'save']);

const store = useStore();
const dialog = computed({
    get: () => props.showDialog,
    set: (value) => emit('close', value)
});

const valid = ref(true);
const formRef = ref(null);



const task = reactive({
    id: props.initialTask?.id || null,
    taskName: props.initialTask?.task_name || '',
    description: props.initialTask?.description || '',
    drones: props.initialTask?.drones || []
});

const drones = computed(() => {
    const allDrones = store.getters['drones/allDrones'];
    return allDrones;
});

const isEditMode = computed(() => !!props.initialTask && !!props.initialTask.id);


const rules = {
    required: (value: string) => !!value || 'Required.',
};

const openDialog = () => {
    dialog.value = true;
};
const closeDialog = () => {
    if (!isEditMode.value) {
        dialog.value = false;
        task.taskName = '';
        task.description = '';
        task.drones = [];
    }
    emit('close');
};
const submitForm = async () => {
    const form: HTMLFormElement | any = formRef.value;
    if (form) {
        const isValid = await form.validate();
        if (isValid.valid) {
            try {
                const taskData = {
                    id: task.id,
                    task_name: task.taskName,
                    description: task.description,
                    drone_ids: task.drones
                };
                if (isEditMode.value) {
                    await store.dispatch('tasks/updateTask', taskData);
                } else {
                    await store.dispatch('tasks/createTask', taskData);
                }
                emit('save', taskData);
                closeDialog();
            } catch (error: any) {
                console.error(error);
            }
        }
    }
};

const captureDrones = async () => {
    await store.dispatch('drones/fetchDrones')
}
defineExpose({ openDialog });

onMounted(() => {
    captureDrones()
})

watch(() => props.initialTask, (newTask) => {
    if (newTask) {
        task.id = newTask.id || null;
        task.taskName = newTask.task_name;
        task.description = newTask.description;
        task.drones = newTask.drones;
    }
}, { immediate: true });
</script>

<style scoped>
.headline {
    font-weight: bold;
}
</style>