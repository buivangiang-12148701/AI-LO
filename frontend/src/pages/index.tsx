import { Chatbot } from "@/components/Chatbot";

export default function Home() {
  return (
    <main className="min-h-screen p-4 bg-gray-100">
      <div className="container mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">
          Trợ lý Ẩm thực Việt Nam
        </h1>
        <Chatbot />
      </div>
    </main>
  );
}
