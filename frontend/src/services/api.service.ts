import axios, { AxiosInstance, AxiosResponse, AxiosError } from "axios";
import { API_CONFIG } from "@/config/api.config";
import { ChatResponse, ApiError } from "@/types/api";

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create(API_CONFIG);

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        // Add auth token if needed
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        if (error.response) {
          // Server error response
          const apiError: ApiError = {
            message: error.response.data.message || "Có lỗi xảy ra",
            error_code: error.response.data.error_code,
            status: error.response.status,
          };
          return Promise.reject(apiError);
        }
        // Network error
        return Promise.reject({
          message: "Không thể kết nối đến server",
          status: 0,
        });
      }
    );
  }

  async chatWithBot(
    message: string,
    sessionId?: string
  ): Promise<AxiosResponse<ChatResponse>> {
    try {
      return await this.api.post<ChatResponse>("/api/chat", {
        message,
        session_id: sessionId,
        language: "vi",
      });
    } catch (error) {
      console.error("Chat error:", error);
      throw error;
    }
  }

  async getMenu(): Promise<AxiosResponse<MenuItem[]>> {
    try {
      return await this.api.get("/api/menu");
    } catch (error) {
      console.error("Menu error:", error);
      throw error;
    }
  }

  async searchDishes(query: string): Promise<AxiosResponse<MenuItem[]>> {
    try {
      return await this.api.get(
        `/api/dishes/search?q=${encodeURIComponent(query)}`
      );
    } catch (error) {
      console.error("Search error:", error);
      throw error;
    }
  }
}

export const apiService = new ApiService();
