import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";
import { apiService } from "@/services/api.service";
import { ChatMessage, ChatResponse } from "@/types/api";

interface ChatState {
  messages: ChatMessage[];
  loading: boolean;
  error: string | null;
  suggestions: string[];
}

const initialState: ChatState = {
  messages: [],
  loading: false,
  error: null,
  suggestions: [],
};

// Optimized thunk
export const sendMessage = createAsyncThunk(
  "chat/sendMessage",
  async (message: string, { rejectWithValue }) => {
    try {
      const response = await apiService.chatWithBot(message);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data);
    }
  },
  {
    condition: (message, { getState }) => {
      const { chat } = getState() as RootState;
      return !chat.loading; // Prevent multiple requests
    },
  }
);

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    clearChat: (state) => {
      state.messages = [];
      state.suggestions = [];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.loading = false;
        state.messages.push({
          id: Date.now().toString(),
          text: action.payload.response,
          sender: "bot",
          timestamp: new Date(),
        });
        state.suggestions = action.payload.suggestions;
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.message || "Error occurred";
      });
  },
});

export const { clearChat } = chatSlice.actions;
export default chatSlice.reducer;
