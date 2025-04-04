import React, { useEffect, useRef, useState } from "react";
import io from "socket.io-client";
import CandlestickChart, { StockData } from "../../components/CandleStickChart";
import { IoMdArrowRoundBack } from "react-icons/io";
import { FaMagnifyingGlass } from "react-icons/fa6";
import { Link } from "react-router-dom";
import getAuthInitials from "../../utils/getAuthInitials";
import { useAuthContext } from "../../context/AuthContext";

const Stocks: React.FC = () => {
	const { authUser } = useAuthContext();
	const [search, setSearch] = useState<string>("NVDA");
	const [monitorInterval, setMonitorInterval] = useState<number>(30);
	const [stockData, setStockData] = useState<StockData | null>(null);
	const socketRef = useRef<ReturnType<typeof io> | null>(null);
	const SOCKET_URL = import.meta.env.VITE_SOCKET_URL;

	useEffect(() => {
		const socket = io(SOCKET_URL);
		socketRef.current = socket;

		socket.on("stock_update", (data: StockData) => {
			setStockData(data);
		});

		// Monitor NVDA by default
		socket.emit("start_monitoring", { symbol: "NVDA", interval: 30 });

		return () => {
			socket.disconnect();
		};
	}, []);

	const handleMonitor = () => {
		if (socketRef.current) {
			socketRef.current.emit("start_monitoring", {
				symbol: search.toUpperCase(),
				interval: monitorInterval,
			});
		}
	};

	const handleSearch = () => {
		console.log("Search query:", search);
	};

	return (
		<div className="flex flex-col w-full text-white overflow-hidden">
			{/* Header */}
			<div className="w-full px-6 py-3 flex items-center justify-between">
				<Link to="/chat" className="flex items-center gap-2 text-gray-300 hover:text-white transition">
					<IoMdArrowRoundBack className="text-lg" />
					<span className="text-sm md:text-base">Back</span>
				</Link>
				<div className="flex items-center gap-3">
					<img src="/Logo.png" alt="logo" className="w-10 md:w-12" />
					<h1 className="text-lg md:text-xl font-semibold">FinGPT</h1>
				</div>
				<div className="rounded-full bg-pink-500 p-2">
					<h1 className="text-sm md:text-2xl font-semibold">{getAuthInitials(authUser?.name)}</h1>
				</div>
			</div>

			<div className="w-full flex flex-col items-center justify-center py-4">
				<h1 className="text-2xl font-semibold text-gray-200">Explore Stocks</h1>
				<div className="w-[95%] h-[1px] mt-3 bg-gray-500" />
			</div>

			<div className="w-full px-8 py-4 flex flex-col md:flex-row md:items-center gap-4">
				<div className="flex items-center gap-2 bg-gray-800 text-white rounded-full py-3 px-6 w-full md:max-w-sm">
					<input
						type="text"
						placeholder="Search for Stocks by their Stock Symbol..."
						className="w-full bg-transparent outline-none text-sm placeholder-gray-400"
						value={search}
						onChange={(e) => setSearch(e.target.value)}
					/>
					<button onClick={handleSearch} className="border-none outline-none cursor-pointer">
						<FaMagnifyingGlass className="text-gray-400 text-lg" />
					</button>
				</div>

				<div className="flex items-center gap-2">
					<input
						type="number"
						placeholder="Interval (s)"
						className="bg-gray-800 text-sm px-3 py-2 rounded outline-none w-24"
						value={monitorInterval}
						onChange={(e) => setMonitorInterval(Number(e.target.value))}
					/>
					<button
						onClick={handleMonitor}
						className="bg-blue-600 px-4 py-2 rounded text-sm hover:bg-blue-700 transition"
					>
						Start Monitoring
					</button>
				</div>
			</div>

			<div className="w-full px-8 py-2">
				<div className="bg-gray-900 p-4 rounded-lg">
					<CandlestickChart stockData={stockData} />
					{stockData && (
						<div className="mt-2 text-gray-400 text-sm">
							Last Updated: {new Date(stockData.timestamp).toLocaleString()}
						</div>
					)}
				</div>
			</div>
		</div>
	);
};

export default Stocks;