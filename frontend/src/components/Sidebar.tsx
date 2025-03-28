import { useEffect, useState } from "react";
import { ChatHistory, Messages } from "../types";
import useGetMyChatHistory from "../hooks/useGetMyChatHistory";
import isToday from "../utils/isToday";
import useGetChatById from "../hooks/useGetChatById";
import { MdLogout } from "react-icons/md";
import useLogout from "../hooks/useLogout";
import Spinner from "./Spinner";

interface SidebarProps {
	setMessages: React.Dispatch<React.SetStateAction<Messages>>;
}

const Sidebar = ({ setMessages }: SidebarProps) => {
	const [history, setHistory] = useState<ChatHistory[]>([]);
	const { loading, chatHistory } = useGetMyChatHistory();
	const { chat } = useGetChatById();
	const { loading: loggingOut, logout } = useLogout();

	const getChatHistory = async () => {
		const data = await chatHistory();
		setHistory(data);
	};

	const fetchChat = async (id: string) => {
		const data = await chat(id);
		setMessages(data);
	}

	useEffect(() => {
		getChatHistory();
	}, []);

	const todayChats = history.filter(chat => isToday(chat.createdAt));
	const allChats = history.filter(chat => !isToday(chat.createdAt));

	return (
		<div className="w-55 lg:w-70 h-screen bg-gray-900 text-white flex flex-col">
			<div className="p-4 flex items-center gap-3">
				<img src="/Logo.png" alt="Logo" className="w-10" />
				<div className="text-lg font-normal">FinGPT</div>
			</div>

			<div className="flex-1 overflow-y-auto pb-40 px-4">
				{loading ? (
					<div className="mt-4 text-gray-400 text-sm">Loading chat history...</div>
				) : history.length === 0 ? (
					<div className="mt-4 text-gray-500 text-sm text-center">
						No chats available.
					</div>
				) : (
					<>
						{/* Today's Chats */}
						{todayChats.length > 0 && (
							<div className="mt-4">
								<h2 className="text-gray-400 text-xs uppercase">Today</h2>
								{todayChats.map(chat => (
									<button
										key={chat.id}
										className="w-full text-left p-2 bg-gray-800 rounded-md hover:bg-gray-700 mt-2 truncate cursor-pointer"
										title={chat.header}
										onClick={() => {
											fetchChat(chat.id);
										}}
									>
										{chat.header}
									</button>
								))}
							</div>
						)}

						{/* All Chats */}
						{allChats.length > 0 && (
							<div className="mt-6 border-t border-gray-700 pt-4">
								<h2 className="text-gray-400 text-xs uppercase">All Chats</h2>
								<div className="mt-2 space-y-2">
									{allChats.map(chat => (
										<button
											key={chat.id}
											className="w-full text-left p-2 rounded-md hover:bg-gray-700 truncate cursor-pointer"
											title={chat.header}
											onClick={() => {
												fetchChat(chat.id);
											}}
										>
											{chat.header}
										</button>
									))}
								</div>
							</div>
						)}
					</>
				)}
			</div>

			<div className="p-4 w-55 lg:w-70 bg-gray-800 fixed bottom-0 left-0 flex justify-start">
				<div className="flex items-center justify-center gap-1">
					<button
						className="text-xl cursor-pointer"
						disabled={loggingOut}
						onClick={logout}
					>
						{loggingOut ? (
							<Spinner size="small" color="secondary" />
						) : (
							<MdLogout />
						)}
					</button>
					<h2 className="text-gray-400 text-xs uppercase">LOGOUT</h2>
				</div>
			</div>
		</div>
	);
};

export default Sidebar;