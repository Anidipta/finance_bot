import { useState, useRef } from "react";
import { getGeminiResponse } from "../../hooks/useGetResponse";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Mic, MicOff, Send } from "lucide-react";
import AppNavbar from "../../components/navbars/AppNavbar";

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
        { text: "⚠️ **Error:** Unable to fetch response.", sender: "bot" }
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
      console.error("Speech recognition error:", event);
      setIsListening(false);
    };

    recognition.start();
    recognitionRef.current = recognition;
  };

  return (
    <div className="flex justify-center items-center h-screen w-full">
      <AppNavbar />
      
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

        {/* Input Field & Voice Input */}
        <div className="mt-4 flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 p-2 rounded-l bg-gray-700 border border-gray-600 focus:outline-none"
            placeholder="Ask something..."
          />
          <button
            onClick={startListening}
            className={`p-2 ${isListening ? "bg-red-500" : "bg-gray-600"} rounded`}
          >
            {isListening ? <MicOff size={20} /> : <Mic size={20} />}
          </button>
          <button onClick={handleSend} className="p-2 bg-blue-500 rounded-r hover:bg-blue-600 transition">
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;