import { IoMdArrowRoundBack } from "react-icons/io";
import { FaMagnifyingGlass } from "react-icons/fa6";
import { Link } from "react-router-dom";
import getAuthInitials from "../../utils/getAuthInitials";
import { useAuthContext } from "../../context/AuthContext";
import { useState } from "react";

const Stocks = () => {
	const { authUser } = useAuthContext();
	const [search, setSearch] = useState<string>("");

	const handleSearch = async () => {
		console.log(search);
	}

	return (
		<div className="flex flex-col w-full text-white overflow-hidden">
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

			<div className="w-full px-8 py-2">
				<div className="flex items-center gap-2 bg-gray-800 text-white rounded-full py-3 px-6 w-full md:w-1/2 lg:w-[40%]">
					<input
						type="text"
						placeholder="Search for Stocks by their Stock Symbol..."
						className="w-full bg-transparent outline-none text-sm placeholder-gray-400"
						value={search}
						onChange={(e) => setSearch(e.target.value)}
					/>
					<button
						className="border-none outline-none cursor-pointer"
						onClick={handleSearch}
					>
						<FaMagnifyingGlass className="text-gray-400 text-lg" />
					</button>
				</div>
			</div>
		</div>
	);
};

export default Stocks;