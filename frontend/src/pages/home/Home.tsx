import { useState } from "react";
import { getGeminiResponse } from "../../hooks/useGetResponse";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Message {
  text: string;
  sender: "user" | "bot";
}

const Home = () => {
  const [input, setInput] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const botReply = await getGeminiResponse(input);
      setMessages((prev) => [...prev, { text: botReply, sender: "bot" }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { text: "⚠️ **Error:** Unable to fetch response.", sender: "bot" }
      ]);
      console.log(error);
    }

    setInput("");
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-900 text-white">
      <div className="w-full max-w-md bg-gray-800 p-6 rounded-lg shadow-lg">
        {/* Chat Window */}
        <div className="h-80 overflow-y-auto space-y-2 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`p-3 rounded-lg max-w-[80%] ${msg.sender === "user"
                ? "ml-auto bg-blue-600 text-right"
                : "mr-auto bg-gray-700 text-left"
                }`}
            >
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.text}</ReactMarkdown>
            </div>
          ))}
        </div>

        {/* Input Field */}
        <div className="mt-4 flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 p-2 rounded-l bg-gray-700 border border-gray-600 focus:outline-none"
            placeholder="Ask something..."
          />
          <button
            onClick={handleSend}
            className="p-2 bg-blue-500 rounded-r hover:bg-blue-600 transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;