import apiClient, { handleError, handleResponse } from '@/api/config';
import SSEClient from '../sse';

export interface Image {
  id: number;
  image_path: string;
}

export interface Drone {
  id: number;
  name: string;
  model: string;
  status: 'offline' | 'online' | 'assigned' | 'on-mission';
  images?: Image[];
}

export interface Task {
  id: number;
  task_name: string;
  description: string;
  status: 'not-assigned' | 'assigned' | 'on-progress' | 'completed';
  drones?: Drone[];
  drone_ids: number[];
}

export const getTasks = async (): Promise<Task[]> => {
  try {
    const response = await apiClient.get('/tasks');
    return handleResponse(response);
  } catch (error: any) {
    return handleError(error);
  }
};

export const getTaskById = async (taskId: number): Promise<Task> => {
  try {
    const response = await apiClient.get(`/tasks/${taskId}`);
    return handleResponse(response);
  } catch (error: any) {
    return handleError(error);
  }
};

export const taskUpdate = async (taskData: Partial<Task>): Promise<Task> => {
  try {
    const response = apiClient.put(`/tasks`, taskData)
    return handleResponse(response);
  } catch (error: any) {
    return handleError(error);
  }
};

export const taskCreate = async (taskData: Partial<Task>): Promise<Task> => {
  try {
    const response = await apiClient.post('/tasks', taskData);
    return handleResponse(response);
  } catch (error: any) {
    return handleError(error);
  }
};

export const taskDelete = async (taskId: number): Promise<void> => {
  try {
    const response = await apiClient.delete(`/tasks/${taskId}`);
    return handleResponse(response);
  } catch (error: any) {
    return handleError(error);
  }
};

export const taskExecute = async (taskId: number): Promise<void> => {
  try {
    const response = await apiClient.post(`/tasks/${taskId}/execute`);
    return handleResponse(response);
  } catch (error: any) {
    return handleError(error);
  }
};