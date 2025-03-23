import { useState, useRef } from "react";
import { getGeminiResponse } from "../../hooks/useGetResponse";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Mic, MicOff, Send } from "lucide-react";
import AppNavbar from "../../components/navbars/AppNavbar";
import Sidebar from "../../components/Sidebar";

interface Message {
  text: string;
  sender: "user" | "bot";
}

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
}

const Chat = () => {
  const [input, setInput] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isListening, setIsListening] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const recognitionRef = useRef<SpeechRecognitionEvent | null>(null);

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
        { text: "⚠️ **Error:** Unable to fetch response.", sender: "bot" },
      ]);
      console.log(error);
    }

    setInput("");
  };

  const startListening = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Your browser does not support voice recognition.");
      return;
    }

    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
    };

    recognition.onerror = (event: SpeechRecognitionEvent) => {
      console.log("Speech recognition error:", event);
      setIsListening(false);
    };

    recognition.start();
    recognitionRef.current = recognition;
  };

  return (
    <div className="flex h-screen max-h-screen w-full text-white bg-black overflow-hidden">
      <AppNavbar
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
      />

      {isSidebarOpen && (
        <div className="bg-gray-900 border-r border-gray-700 mt-20 z-10">
          <Sidebar />
        </div>
      )}

      <div className="flex flex-col flex-1 mt-20 md:px-4 z-10">
        <div className="flex flex-col flex-1 overflow-hidden">
          {/* Chat Window */}
          <div className="flex-1 overflow-y-auto px-6 space-y-4 scrollbar-thin scrollbar-thumb-gray-700 pb-10">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-gray-400 text-center">
                  <p className="text-xl mb-2">Welcome to FinGPT</p>
                  <p className="text-sm">Ask me anything related to finance...</p>
                </div>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  className={`max-w-[90%] p-4 rounded-lg shadow-md ${msg.sender === "user"
                    ? "ml-auto bg-blue-600 text-right lg:max-w-[35%] md:max-w-[45%]"
                    : "mr-auto bg-gray-700 text-left lg:max-w-[40%] md:max-w-[65%]"
                    }`}
                >
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.text}
                  </ReactMarkdown>
                </div>
              ))
            )}
          </div>

          {/* Input Field & Voice Input */}
          <div className="p-4 bg-gray-800 flex items-center gap-2 border-t border-gray-700">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 p-3 rounded-lg bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ask something..."
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            />
            <button
              onClick={startListening}
              className={`p-3 rounded-lg ${isListening ? "bg-red-500" : "bg-gray-600 hover:bg-gray-500"
                } transition-colors`}
              title={isListening ? "Stop listening" : "Start voice input"}
            >
              {isListening ? <MicOff size={22} /> : <Mic size={22} />}
            </button>
            <button
              onClick={handleSend}
              className="p-3 bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors"
              title="Send message"
            >
              <Send size={22} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;