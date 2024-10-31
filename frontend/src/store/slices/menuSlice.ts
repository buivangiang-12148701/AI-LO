import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { apiService } from "@/services/api.service";
import { MenuItem } from "@/types/api";

interface MenuState {
  items: MenuItem[];
  categories: string[];
  loading: boolean;
  error: string | null;
}

const initialState: MenuState = {
  items: [],
  categories: [],
  loading: false,
  error: null,
};

export const fetchMenu = createAsyncThunk("menu/fetchMenu", async () => {
  const response = await apiService.getMenu();
  return response.data;
});

export const searchDishes = createAsyncThunk(
  "menu/searchDishes",
  async (query: string) => {
    const response = await apiService.searchDishes(query);
    return response.data;
  }
);

const menuSlice = createSlice({
  name: "menu",
  initialState,
  reducers: {
    setCategories: (state, action) => {
      state.categories = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchMenu.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchMenu.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchMenu.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Có lỗi xảy ra";
      })
      .addCase(searchDishes.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(searchDishes.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(searchDishes.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Có lỗi xảy ra";
      });
  },
});

export const { setCategories } = menuSlice.actions;
export default menuSlice.reducer;
