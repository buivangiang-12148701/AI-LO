export interface ChatMessage {
  id: string;
  text: string;
  sender: "user" | "bot";
  timestamp: Date;
}

export interface ChatResponse {
  response: string;
  confidence: number;
  suggestions: string[];
  metadata?: Record<string, any>;
}

export interface MenuItem {
  name: string;
  description: string;
  price: string;
  category: string;
  image?: string;
}

export interface ApiError {
  message: string;
  error_code?: string;
  status: number;
}
