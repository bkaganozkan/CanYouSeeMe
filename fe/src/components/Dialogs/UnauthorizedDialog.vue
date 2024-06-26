<template>
  <v-dialog v-model="dialog" max-width="400px">
    <v-card>
      <v-card-title class="headline">{{title}}</v-card-title>
      <v-card-text>{{ message }}</v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="closeDialog">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, defineExpose } from 'vue';

const dialog = ref(false);
const title = ref('');
const message = ref('');

const openDialog = (titleDialog:string,msg: string ) => {
  title.value = titleDialog;
  message.value = msg;
  dialog.value = true;
};

const closeDialog = () => {
  dialog.value = false;
};

defineExpose({ openDialog });
</script>

<style scoped>
</style>
