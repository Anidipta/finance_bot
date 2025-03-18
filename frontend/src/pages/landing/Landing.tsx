import About from "../../components/landing/About";
import LandingNavbar from "../../components/navbars/LandingNavbar";

const Landing = () => {
  return (
    <>
      <LandingNavbar />

      <div className="pt-20 lg:pt-32 p-4 flex flex-col items-center justify-center w-full h-screen bg-[url('/bg.jpeg')] bg-cover bg-center bg-no-repeat">
        <div className="absolute inset-0 bg-black/65"></div>

        <div className="relative z-10 flex items-center justify-center flex-col gap-3">
          <img src="/Logo.png" alt="logo" className="w-48 -mt-20 -mb-8" />
          <h1 className="text-primary text-[80px] lg:text-[100px]">FinGPT</h1>
          <p className="text-subhead text-center max-w-lg">
            A One-stop solution for all your finance, economics & investment doubts & automation.
          </p>
        </div>
      </div>

      <About />
    </>
  )
}

export default Landing;