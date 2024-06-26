import axios from "axios";
import router from "../router";
import { showUnauthorizedDialog } from "@/utils/unauthorizedHelper";
import store from "@/store";

const API_BASE_URL = process.env.VUE_APP_API_BASE_URL;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 3000,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("authToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.resolve(error);
  }
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const token = localStorage.getItem("authToken");
    const user = store.getters["auth/userRole"];

    if (error.response && error.response.status == 403) {
      showUnauthorizedDialog("Unauthorized", "You are not authorized");
    } else if (error.response && error.response.status === 401) {
      if (
        error.response?.data?.error &&
        error.response?.data?.error == "Signature has expired"
      ) {
        localStorage.removeItem("authToken"); // Clean TOKEN
      }
      if (token && user) {
        // User logged in but unauthorized
        showUnauthorizedDialog("Unauthorized", "Unauthorized Request");
      } else if (!token || !user) {
        // User not logged in
        localStorage.removeItem("authToken"); // Clean TOKEN
        router.push("/login");
      }
    } else if (error.response.status == 408) {
      showUnauthorizedDialog("Error", "Connection Lost Refresh the page");
    } else {
      showUnauthorizedDialog(
        "Error",
        error.response.data.error || "Unkown Error"
      );
    }
    return Promise.resolve("Error");
  }
);

export const handleResponse = (response: any) => {
  if (response.status >= 200 && response.status < 300) {
    return response.data;
  } else {
    throw new Error(response.data.message || "Unknown error");
  }
};

export const handleError = (error: any) => {
  if (error.response) {
    throw new Error(error.response.data.message || "An error occurred");
  } else if (error.request) {
    throw new Error("No response received from server");
  } else {
    // localStorage.removeItem('authToken'); // Clean TOKEN
    // localStorage.removeItem('authToken'); // Clean TOKEN

    throw new Error(error.message || "An unknown error occurred");
  }
};

export default apiClient;
