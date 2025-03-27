import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Mic, MicOff, Send, Loader2 } from "lucide-react";
import AppNavbar from "../../components/navbars/AppNavbar";
import Sidebar from "../../components/Sidebar";
import { ChatProps, Messages } from "../../types";
import useGetResponse from "../../hooks/useGetResponse";
import useCreateChatStream from "../../hooks/useCreateChatStream";
import useAppendChats from "../../hooks/useAppendChats";
import Spinner from "../../components/Spinner";

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
}

interface BotReply {
  intent: string;
  response: string
}

const Chat = () => {
  const [input, setInput] = useState<string>("");
  const [messages, setMessages] = useState<Messages>({
    _id: "",
    userId: "",
    chats: [],
    header: "",
    createdAt: "",
    updatedAt: ""
  });
  const [isListening, setIsListening] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const recognitionRef = useRef<SpeechRecognitionEvent | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const { loading: responseLoading, getResponse } = useGetResponse();
  const { loading: streamLoading, createStream } = useCreateChatStream();
  const { loading: chatLoading, append } = useAppendChats();

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages.chats, responseLoading]);

  const handleSend = async () => {
    if (!input.trim() || isSubmitting) return;

    setIsSubmitting(true);

    try {
      let messageData;
      if (!messages._id) {
        messageData = await createStream() as Messages;
        setMessages(messageData);
      }
      const inputCpy = input;
      setInput("");

      const userMessage: ChatProps = {
        id: messages._id || messageData!._id,
        message: inputCpy,
        sender: "user"
      };
      const userChat = await append(userMessage);

      setMessages(prev => ({
        ...prev,
        chats: [...(prev.chats || []), userChat]
      }));

      try {
        const botReply = await getResponse(inputCpy) as BotReply;

        const agentMessage: ChatProps = {
          id: messages._id || messageData!._id,
          message: botReply.response,
          sender: "agent"
        };
        const agentChat = await append(agentMessage);

        setMessages(prev => ({
          ...prev,
          chats: [...(prev.chats || []), agentChat]
        }));
      } catch (error) {
        setMessages(prev => ({
          ...prev,
          chats: [...(prev.chats || []), {
            message: "⚠️ **Error:** Unable to fetch response.",
            sender: "agent",
            _id: Date.now().toString()
          }]
        }));
        console.log(error);
      }
    } catch (error) {
      console.log("Error in message sending process", error);
    } finally {
      setIsSubmitting(false);
    }
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

  console.log(messages);

  return (
    <div className="flex h-screen max-h-screen w-full text-white bg-black overflow-hidden">
      <AppNavbar
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
      />

      {isSidebarOpen && (
        <div className="bg-gray-900 border-r border-gray-700 mt-20 z-10">
          <Sidebar
            setMessages={setMessages}
          />
        </div>
      )}

      <div className="flex flex-col flex-1 mt-20 md:px-4 z-10">
        <div className="flex flex-col flex-1 overflow-hidden">
          <div
            ref={chatContainerRef}
            className="flex-1 overflow-y-auto px-6 space-y-4 scrollbar-thin scrollbar-thumb-gray-700 pb-10"
          >
            {messages.chats.length === 0 && !streamLoading ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-gray-400 text-center">
                  <p className="text-xl mb-2">Welcome to FinGPT</p>
                  <p className="text-sm">Ask me anything related to finance...</p>
                </div>
              </div>
            ) : (
              messages?.chats?.map((msg) => (
                <div
                  key={msg?._id}
                  className={`max-w-[95%] p-4 rounded-lg shadow-md ${msg?.sender === "user"
                    ? "ml-auto bg-blue-600 text-right lg:max-w-[35%] md:max-w-[50%]"
                    : "mr-auto bg-gray-700 text-left lg:max-w-[40%] md:max-w-[75%]"
                    }`}
                >
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg?.message}
                  </ReactMarkdown>
                </div>
              ))
            )}

            {responseLoading && (
              <div className="flex items-right mr-auto rounded-lg max-w-[40%]">
                <Spinner />
              </div>
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
              disabled={isSubmitting || streamLoading || responseLoading}
            />
            <button
              onClick={startListening}
              className={`p-3 rounded-lg ${isListening ? "bg-red-500" : "bg-gray-600 hover:bg-gray-500"
                } transition-colors`}
              title={isListening ? "Stop listening" : "Start voice input"}
              disabled={isSubmitting || streamLoading || responseLoading}
            >
              {isListening ? <MicOff size={22} /> : <Mic size={22} />}
            </button>
            <button
              onClick={handleSend}
              className="p-3 bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors"
              title="Send message"
              disabled={!input.trim() || isSubmitting || streamLoading || responseLoading}
            >
              {isSubmitting || streamLoading || responseLoading ? (
                <Loader2 className="animate-spin" size={22} />
              ) : (
                <Send size={22} />
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;