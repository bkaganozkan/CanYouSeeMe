<template>
    <v-container>
        <v-row>
            <v-col>
                <v-card>
                    <v-card-title>Tasks List</v-card-title>
                    <v-card-text>
                        <v-data-table :headers="headers" :items="tasks" class="elevation-1" item-value="id">
                            <template v-slot:top>
                                <v-toolbar flat>
                                    <v-toolbar-title>Tasks</v-toolbar-title>
                                    <v-divider class="mx-4" inset vertical></v-divider>
                                    <v-spacer></v-spacer>
                                    <v-btn color="primary" @click="openAddTaskDialog">Add Task</v-btn>
                                </v-toolbar>
                            </template>
                            <template v-slot:[`item.description`]="{ item }">
                                {{ truncateDescription(item.description) }}
                            </template>
                            <template v-slot:[`item.status`]="{ item }">
                                <v-chip :color="getStatusColor(item.status)" dark>
                                    {{ item.status }}
                                </v-chip>
                            </template>
                            <template v-slot:[`item.actions`]="{ item }">
                                <v-btn @click="showDetails(Number(item.id))">
                                    Details
                                </v-btn>
                            </template>
                        </v-data-table>
                        <v-progress-circular v-if="loading" indeterminate color="primary"></v-progress-circular>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <AddTaskDialog :showDialog="showAddTaskDialog" :initialTask="currentTask" @close="closeAddTaskDialog"
            @save="closeAddTaskDialog" />

    </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import AddTaskDialog from './Dialogs/AddTaskDialog.vue';


const store = useStore();
const router = useRouter();

const headers = [
    { title: 'ID', value: 'id' },
    { title: 'Task Name', value: 'task_name' },
    { title: 'Description', value: 'description' },
    { title: 'Status', value: 'status' },
    { title: 'Actions', value: 'actions', sortable: false }
];

const tasks = computed(() => store.getters['tasks/tasks']);
const loading = computed(() => store.getters['tasks/loading']);

const showAddTaskDialog = ref(false);
const currentTask = ref({ id: 0, task_name: '', description: '', drone_ids: [] });


const openAddTaskDialog = () => {
    currentTask.value = { id: 0, task_name: '', description: '', drone_ids: [] };
    showAddTaskDialog.value = true;
};

const closeAddTaskDialog = () => {
    showAddTaskDialog.value = false;
}

const truncateDescription = (description: string) => {
    const maxLength = 20;
    if (description.length > maxLength) {
        return description.slice(0, maxLength) + '...';
    }
    return description;
};
const getStatusColor = (status: string) => {
    switch (status) {
        case 'assigned':
            return 'blue';
        case 'not-assigned':
            return 'grey';
        case 'on-progress':
            return 'orange';
        case 'completed':
            return 'green';
        default:
            return 'grey';
    }
};

const deleteDialog = ref(false);
const confirmDeleteId = ref<number | null>(null);

const showDetails = (taskId: number) => {
    router.push({ name: 'TaskDetailsPage', params: { id: taskId } });

};

onMounted(() => {
    store.dispatch('tasks/fetchTasks');
});
</script>

<style scoped>
.v-container {
    height: 100vh;
}
</style>