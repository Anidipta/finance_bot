import { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import About from "../../components/landing/About";
import LandingNavbar from "../../components/navbars/LandingNavbar";
import Services from "../../components/landing/Services";
import Contact from "../../components/landing/Contact";
import Footer from "../../components/Footer";

gsap.registerPlugin(ScrollTrigger);

const Landing = () => {
  const sectionRef = useRef(null);
  const imageRef = useRef(null);
  const headingRef = useRef(null);
  const backgroundRef = useRef(null);
  const contentRef = useRef(null);

  useEffect(() => {
    gsap.from(imageRef.current, {
      opacity: 0,
      y: -50,
      duration: 1,
      ease: "power3.out",
    });

    gsap.from(headingRef.current, {
      opacity: 0,
      y: 50,
      duration: 1,
      delay: 0.5,
      ease: "power3.out",
    });

    // Parallax effect - background moves slower than content
    gsap.to(backgroundRef.current, {
      yPercent: -20,
      ease: "none",
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top top",
        end: "bottom top",
        scrub: true,
      },
    });

    // Content moves faster for enhanced parallax effect
    gsap.to(contentRef.current, {
      yPercent: -5,
      ease: "none",
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top top",
        end: "bottom top",
        scrub: true,
      },
    });

    // Overall section movement
    gsap.to(sectionRef.current, {
      yPercent: -10,
      ease: "none",
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top top",
        scrub: true,
      },
    });
  }, []);

  return (
    <>
      <LandingNavbar />

      <div
        ref={sectionRef}
        className="relative pt-20 lg:pt-32 p-4 flex flex-col items-center justify-center w-full h-screen overflow-hidden"
      >
        <div
          ref={backgroundRef}
          className="absolute inset-0 bg-[url('/bg.jpeg')] bg-cover bg-center bg-no-repeat"
        >
          <div className="absolute inset-0 bg-black/65"></div>
        </div>

        <div
          ref={contentRef}
          className="relative z-10 flex items-center justify-center flex-col gap-3"
        >
          <motion.img
            ref={imageRef}
            src="/Logo.png"
            alt="logo"
            className="w-48 -mt-20 -mb-8"
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, ease: "easeOut" }}
          />
          <motion.h1
            ref={headingRef}
            className="text-primary text-[80px] lg:text-[100px]"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.5, ease: "easeOut" }}
          >
            FinGPT
          </motion.h1>
          <p className="text-subhead text-center max-w-lg">
            A One-stop solution for all your finance, economics & investment doubts & automation.
          </p>
        </div>
      </div>

      <About />
      <Services />
      <Contact />
      <Footer />
    </>
  );
};

export default Landing;