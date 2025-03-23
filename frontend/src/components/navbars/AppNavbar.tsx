import { useState } from "react";
import { BiSolidEdit } from "react-icons/bi";
import { TbLayoutSidebarLeftCollapse, TbLayoutSidebarRightCollapse } from "react-icons/tb";
import { FaChevronDown } from "react-icons/fa";

interface DropDownProps {
	id: string;
	name: string;
	description: string;
}

interface AppNavbarProps {
	isSidebarOpen: boolean;
	setIsSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const AppNavbar = ({ isSidebarOpen, setIsSidebarOpen }: AppNavbarProps) => {
	const dropdownOptions = [
		{
			id: "Gemini-2.0 flash",
			name: "Gemini-2.0 flash",
			description: "Our smartest model & more",
		},
		{
			id: "Gemini-2.0",
			name: "Gemini-2.0",
			description: "Great for everyday tasks",
		},
	];

	const [isDialogOpen, setIsDialogOpen] = useState(false);
	const [selectedOption, setSelectedOption] = useState<DropDownProps>(dropdownOptions[1]);

	const handleSelect = (option: DropDownProps) => {
		setSelectedOption(option);
		setIsDialogOpen(false);
		console.log("Selected Option:", option);
	};

	return (
		<div className="py-2 px-4 fixed left-0 top-0 w-full text-white flex items-center justify-between bg-transparent z-20">
			<div className="flex items-center gap-2 md:gap-4 lg:gap-6">
				<button className="border-none outline-none bg-transparent cursor-pointer text-xl md:text-2xl hover:bg-gray-700 p-1.5 md:p-2 rounded-md flex items-center justify-center" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
					{isSidebarOpen ? (
						<TbLayoutSidebarLeftCollapse />
					) : (
						<TbLayoutSidebarRightCollapse />
					)}
				</button>
				<button className="border-none outline-none bg-transparent cursor-pointer text-xl md:text-2xl hover:bg-gray-700 p-1.5 md:p-2 rounded-md flex items-center justify-center">
					<BiSolidEdit />
				</button>
			</div>

			<div className="flex items-center gap-4">
				<img src="/Logo.png" alt="logo" className="w-[40px] md:w-[45px]" />

				<div className="relative">
					<button
						onClick={() => setIsDialogOpen(!isDialogOpen)}
						className="flex items-center gap-2 px-4 py-2 hover:bg-gray-700 rounded-md transition-all cursor-pointer"
					>
						<span className="text-sm md:text-lg font-medium">{selectedOption.name}</span>
						<FaChevronDown className={`transition-transform ${isDialogOpen ? "rotate-180" : ""}`} />
					</button>

					{isDialogOpen && (
						<div className="absolute left-0 mt-2 min-w-[220px] w-max bg-gray-900 border border-gray-700 rounded-lg shadow-lg">
							<div className="p-3 flex flex-col gap-2">
								{dropdownOptions.map((option) => (
									<div
										key={option.id}
										onClick={() => handleSelect(option)}
										className="flex items-center justify-between p-3 rounded-md bg-gray-800 hover:bg-gray-700 cursor-pointer"
									>
										<div>
											<p className="text-sm md:text-base font-semibold">{option.name}</p>
											<p className="text-xs md:text-sm text-gray-400">{option.description}</p>
										</div>
										{selectedOption.id === option.id && <span className="text-white">✔</span>}
									</div>
								))}
							</div>
						</div>
					)}
				</div>
			</div>

			<div className="rounded-full bg-pink-500 p-2">
				<h1 className="text-sm md:text-2xl font-semibold">TD</h1>
			</div>
		</div>
	);
};

export default AppNavbar;