const Services = () => {
	const cards = [
		{
			img: "/question.png",
			desc: "Answer investment-related questions in simple language"
		},
		{
			img: "/literacy.png",
			desc: "Guide users on financial literacy without technical jargon"
		},
		{
			img: "/suggestion.png",
			desc: "Suggest suitable investment options based on their needs"
		},
		{
			img: "/insights.png",
			desc: "Provide real-time market insights using free Google tools"
		},
	];

	return (
		<div id="services" className="mt-10 w-full items-center justify-center p-4">
			<div className="w-full flex flex-col gap-1 items-center justify-center">
				<h1 className="text-[39px] lg:text-[50px] text-secondary">Services</h1>
				<p className="text-subhead">Our AI can do the following!</p>
			</div>

			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-10 items-center justify-center py-4 px-6">
				{cards.map((card, _idx) => (
					<div key={_idx} className="bg-white/25 flex flex-col items-center justify-center p-4 rounded-lg">
						<img src={card.img} alt={`${card.img}-${_idx}`} className="size-50" />
						<p className="para">{card.desc}</p>
					</div>
				))}
			</div>
		</div>
	)
}

export default Services