import { Link } from "react-router-dom"

const About = () => {
	return (
		<div id="about" className="mt-10 w-full items-center justify-center p-4">
			<div className="w-full flex flex-col gap-1 items-center justify-center">
				<h1 className="text-[39px] lg:text-[50px] text-secondary">About</h1>
				<p className="text-subhead">What We Do is What we Are!</p>
			</div>

			<div className="flex flex-col lg:flex-row gap-4 lg:gap-8 mt-10 items-center justify-center">
				<img src="/about.png" alt="about" className="w-[60%] lg:w-[45%] z-20" />

				<div className="flex flex-col items-center justify-center lg:items-start gap-2 mt-5 lg:mt-0">
					<h1 className="text-tertiary text-4xl lg:text-5xl">Welcome to <span className="!text-blue-300">FinGPT</span></h1>
					<p className="para lg:!text-left">
						India has hundreds of millions of new investors, but financial literacy remains low. There is no scalable way to educate and guide these users. Manual advisory is impractical, and existing platforms focus on experienced investors. <strong>FinGPT</strong> bridges this gap with <i>AI-powered, personalized investment guidance—making smart investing accessible for everyone.</i>
					</p>

					<div className="w-full flex items-center justify-center mt-2">
						<Link to="/signup" className="btn-primary py-3 px-8">Get Started</Link>
					</div>
				</div>
			</div>
		</div>
	)
}

export default About