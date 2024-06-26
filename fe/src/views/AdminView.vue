<template>
  <v-container class="d-flex flex-column align-center justify-center fill-height">
    <v-card class="pa-4 text-center">
      <v-card-title class="headline">Admin Page</v-card-title>
      <v-card-subtitle class="subtitle-1">Restricted Area</v-card-subtitle>
      <v-icon color="red" size="large">mdi-lock</v-icon>
      <v-card-text>YOU HAVE SEEN TOP SECRET INFORMATIONS </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
</script>

<style scoped>
.v-card {
  max-width: 500px;
  width: 100%;
}

.headline {
  font-size: 2rem;
  font-weight: bold;
}

.subtitle-1 {
  font-size: 1.25rem;
  color: red;
  margin-bottom: 16px;
}
</style>