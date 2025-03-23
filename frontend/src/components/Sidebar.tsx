const Sidebar = () => {
	return (
		<div className="w-55 lg:w-70 h-screen bg-gray-900 text-white p-4 overflow-y-auto pb-20">
			<div className="flex items-center gap-3">
				<img src="/Logo.png" alt="Logo" className="w-10" />
				<div className="text-lg font-normal">FinGPT</div>
			</div>

			<div className="mt-4">
				<h2 className="text-gray-400 text-xs uppercase">Today</h2>
				<button className="w-full text-left p-2 bg-gray-800 rounded-md hover:bg-gray-700 mt-2">
					Navbar Dropdown Implement…
				</button>
			</div>

			<div className="mt-6 border-t border-gray-700 pt-4">
				<h2 className="text-gray-400 text-xs uppercase">All Chats</h2>
				<div className="mt-2 space-y-2">
					{[
						"Headless Browser Scraping",
						"Responsive Grid Layout",
						"Prim's Algorithm in C",
						"Graph Creation Debugging",
						"New Chat",
						"Intelligent Traffic Management",
						"GSAP Framer Motion Parallax",
						"React Stock Price Charts",
						"Real-Time Stock Chart React",
						"Customer Journey Mapping",
						"GSAP Framer Motion Parallax",
						"React Stock Price Charts",
						"Real-Time Stock Chart React",
						"Customer Journey Mapping",
					].map((chat, index) => (
						<button
							key={index}
							className="w-full text-left p-2 rounded-md hover:bg-gray-700"
						>
							{chat}
						</button>
					))}
				</div>
			</div>
		</div>
	);
};

export default Sidebar;