import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import Topics from "@/components/Topics";
import SOCLabs from "@/components/SOCLabs";
import WhyChooseUs from "@/components/WhyChooseUs";
import LearningPath from "@/components/LearningPath";
import Certifications from "@/components/Certifications";
import CTA from "@/components/CTA";
import Footer from "@/components/Footer";
const Index = () => {
  return (
    <main className="min-h-screen bg-background">
      <Navbar />
      <Hero />
      <Topics />
      <SOCLabs />
      <LearningPath />
      <WhyChooseUs />
      <Certifications />
      <CTA />
      
      <Footer />
    </main>
  );
};

export default Index;
