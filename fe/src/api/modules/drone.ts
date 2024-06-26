import apiClient, { handleError, handleResponse } from '@/api/config';

export interface Drone {
  id: number;
  name: string;
  model: string;
  status: 'offline' | 'online' | 'assigned' | 'on-mission';
}

export const getDrones = async (): Promise<Drone[]> => {
  try {
    const response = await apiClient.get('/drones');
    return handleResponse(response);
  } catch (error: any) {
    return handleError(error);
  }
};

export const droneUpdate = async (droneData: Partial<Drone>): Promise<Drone> => {
  try {
    const response = await apiClient.put(`/drones`, droneData);
    return handleResponse(response);
  } catch (error: any) {
    return handleError(error);
  }
};

export const droneCreate = async (droneData: Partial<Drone>): Promise<Drone> => {
  try {
    const response = await apiClient.post('/drones', droneData);
    return handleResponse(response);
  } catch (error: any) {
    return handleError(error);
  }
};

export const droneDelete = async (droneId: number): Promise<void> => {
  try {
    const response = await apiClient.delete(`/drones/${droneId}`);
    return handleResponse(response);
  } catch (error: any) {
    return handleError(error);
  }
};
