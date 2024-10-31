import React, { useState, useRef, useEffect } from "react";
import { useAppDispatch, useAppSelector } from "@/hooks";
import { sendMessage, clearChat } from "@/store/slices/chatSlice";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { ErrorBoundary } from "@/components/ErrorBoundary";

interface SuggestionProps {
  text: string;
  onClick: (text: string) => void;
}

const Suggestion: React.FC<SuggestionProps> = ({ text, onClick }) => (
  <button
    onClick={() => onClick(text)}
    className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-full 
               hover:bg-blue-200 transition-colors"
  >
    {text}
  </button>
);

export const Chatbot: React.FC = () => {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const dispatch = useAppDispatch();
  const { messages, loading, error, suggestions } = useAppSelector(
    (state) => state.chat
  );

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    dispatch(sendMessage(input));
    setInput("");
    inputRef.current?.focus();
  };

  const handleSuggestionClick = (text: string) => {
    dispatch(sendMessage(text));
  };

  const renderMessage = (message: ChatMessage) => {
    const isUser = message.sender === "user";
    return (
      <div
        key={message.id}
        className={`flex ${isUser ? "justify-end" : "justify-start"}`}
      >
        <div
          className={`max-w-[80%] p-3 rounded-lg ${
            isUser
              ? "bg-blue-500 text-white rounded-br-none"
              : "bg-gray-100 rounded-bl-none"
          }`}
        >
          {message.text}
        </div>
      </div>
    );
  };

  return (
    <ErrorBoundary>
      <div className="flex flex-col h-[600px] w-full max-w-lg mx-auto bg-white rounded-lg shadow-lg">
        {/* Header */}
        <div className="p-4 border-b bg-blue-600 text-white rounded-t-lg">
          <h2 className="text-xl font-semibold">Trợ lý Ẩm thực Việt Nam</h2>
          <p className="text-sm opacity-75">Hỏi đáp về món ăn Việt Nam</p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map(renderMessage)}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 p-3 rounded-lg">
                <LoadingSpinner size="small" />
              </div>
            </div>
          )}

          {error && (
            <div className="text-red-500 text-center p-2 bg-red-50 rounded">
              {error}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions */}
        {suggestions.length > 0 && (
          <div className="px-4 py-2 border-t flex gap-2 flex-wrap">
            {suggestions.map((suggestion) => (
              <Suggestion
                key={suggestion}
                text={suggestion}
                onClick={handleSuggestionClick}
              />
            ))}
          </div>
        )}

        {/* Input form */}
        <form onSubmit={handleSubmit} className="p-4 border-t">
          <div className="flex space-x-2">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Nhập câu hỏi của bạn..."
              className="flex-1 p-2 border rounded-lg focus:outline-none 
                         focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg 
                         hover:bg-blue-700 disabled:opacity-50
                         transition-colors"
            >
              Gửi
            </button>
          </div>
        </form>
      </div>
    </ErrorBoundary>
  );
};
