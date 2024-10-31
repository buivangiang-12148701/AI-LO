import { render, screen, fireEvent } from "@testing-library/react";
import { Chatbot } from "../components/Chatbot";

describe("Chatbot Component", () => {
  it("renders chatbot interface", () => {
    render(<Chatbot />);
    expect(
      screen.getByPlaceholder("Nhập câu hỏi của bạn...")
    ).toBeInTheDocument();
  });

  it("handles user input", async () => {
    render(<Chatbot />);
    const input = screen.getByPlaceholder("Nhập câu hỏi của bạn...");
    fireEvent.change(input, { target: { value: "xin chào" } });
    fireEvent.submit(input);

    // Wait for response
    const response = await screen.findByText(/Xin chào/i);
    expect(response).toBeInTheDocument();
  });

  it("shows loading state", () => {
    render(<Chatbot />);
    const input = screen.getByPlaceholder("Nhập câu hỏi của bạn...");
    fireEvent.change(input, { target: { value: "test" } });
    fireEvent.submit(input);

    expect(screen.getByText("Đang nhập...")).toBeInTheDocument();
  });
});
