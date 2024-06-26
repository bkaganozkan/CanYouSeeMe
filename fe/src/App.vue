<template>
  <v-app class="fill-height">
    <router-view></router-view>
    <UnauthorizedDialog ref="unauthorizedDialog" />
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import UnauthorizedDialog from '@/components/Dialogs/UnauthorizedDialog.vue';
import { setUnauthorizedDialogRef } from '@/utils/unauthorizedHelper';

const unauthorizedDialog = ref<InstanceType<typeof UnauthorizedDialog>>();

onMounted(() => {
  if (unauthorizedDialog.value) {
    setUnauthorizedDialogRef(unauthorizedDialog.value);
  }
});
</script>
