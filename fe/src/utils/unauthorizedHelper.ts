import { ref } from 'vue';
import UnauthorizedDialog from '@/components/UnauthorizedDialog.vue';

const unauthorizedDialog = ref<InstanceType<typeof UnauthorizedDialog>>();

export const setUnauthorizedDialogRef = (refInstance: InstanceType<typeof UnauthorizedDialog>) => {
  unauthorizedDialog.value = refInstance;
};

export const showUnauthorizedDialog = (title:string,message: string) => {
  unauthorizedDialog.value?.openDialog(title,message);
};
