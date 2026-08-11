import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { useEffect, useRef, useState } from "react";
import { Users, Target, BookOpen, Award, Globe } from "lucide-react";

const About = () => {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.1 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, []);

  const values = [
    {
      icon: Target,
      title: "Defense First",
      description: "We believe the best offense is a strong defense. Our content focuses on building impenetrable security postures."
    },
    {
      icon: Users,
      title: "Community Driven",
      description: "Learning happens best together. Our LinkedIn community fosters collaboration and knowledge sharing."
    },
    {
      icon: Target,
      title: "Practical Focus",
      description: "Theory meets practice. Every concept we teach is backed by real-world applications and hands-on labs."
    },
    {
      icon: BookOpen,
      title: "Continuous Learning",
      description: "The threat landscape evolves daily. We keep you updated with the latest techniques and tools."
    }
  ];

  const stats = [
    { number: "5000+", label: "Community Members" },
    { number: "50+", label: "Tutorials Published" },
    { number: "24/7", label: "Learning Access" },
    { number: "100%", label: "Free Resources" }
  ];

  return (
    <main className="min-h-screen bg-background">
      <Navbar />
      
      {/* Hero Section */}
      <section className="pt-20 pb-16 relative">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              <span className="gradient-text">About BlueTeamers</span>
            </h1>
            <p className="text-xl text-muted-foreground leading-relaxed">
              Your gateway to mastering blue team cybersecurity. We're on a mission to 
              democratize defensive security knowledge and build a community of skilled defenders.
            </p>
          </div>
        </div>
      </section>

      {/* Main About Section */}
      <section ref={ref} className="py-16 relative">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <Card className={`bg-card/50 backdrop-blur border-border p-8 md:p-12 relative overflow-hidden group transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
              <div className="absolute inset-0 bg-gradient-to-r from-primary via-secondary to-primary opacity-0 group-hover:opacity-20 transition-opacity duration-500 blur-xl" />
              
              <h2 className="text-3xl md:text-4xl font-bold mb-6 text-center relative z-10">
                <span className="gradient-text inline-block group-hover:scale-105 transition-transform duration-300">
                  Our Story
                </span>
              </h2>
              
              <div className="space-y-6 text-muted-foreground leading-relaxed relative z-10">
                <p className={`text-lg transition-all duration-500 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'}`} style={{ transitionDelay: '0.1s' }}>
                  BlueTeamers was born from a simple observation: while offensive security gets the spotlight,
                  defensive security professionals are the unsung heroes keeping organizations safe 24/7. We 
                  created this platform to give blue teamers the recognition and resources they deserve.
                </p>
                
                <p className={`text-lg transition-all duration-500 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'}`} style={{ transitionDelay: '0.2s' }}>
                  Our mission is to demystify complex security concepts and provide actionable 
                  insights that can be applied in real-world scenarios. Whether you're a seasoned 
                  security analyst or just starting your journey in cybersecurity, we've got you covered.
                </p>

                <p className={`text-lg transition-all duration-500 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'}`} style={{ transitionDelay: '0.3s' }}>
                  What started as a simple idea has grown into a thriving community where defenders from
                  around the world connect, learn, and share their experiences on LinkedIn. Every day,
                  we're helping security professionals level up their skills.
                </p>
                
                <div className={`pt-6 transition-all duration-500 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`} style={{ transitionDelay: '0.4s' }}>
                  <h3 className="text-xl font-semibold mb-4 gradient-text">What We Cover:</h3>
                  <ul className="space-y-3">
                    {[
                      "Security Operations Center (SOC) best practices",
                      "Threat hunting techniques and methodologies",
                      "Digital forensics and incident analysis",
                      "Security tool reviews and tutorials",
                      "Industry news and threat intelligence",
                      "SIEM configuration and log analysis",
                      "Malware analysis fundamentals",
                      "Incident response playbooks"
                    ].map((item, index) => (
                      <li 
                        key={index}
                        className={`flex items-start group/item hover:translate-x-2 transition-all duration-300 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'}`}
                        style={{ transitionDelay: `${0.5 + index * 0.1}s` }}
                      >
                        <span className="text-primary mr-2 group-hover/item:text-secondary transition-colors">▸</span>
                        <span className="group-hover/item:text-foreground transition-colors">{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 relative">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {stats.map((stat, index) => (
              <Card 
                key={index}
                className="bg-card/50 backdrop-blur border-border p-6 text-center hover:border-primary/50 transition-all duration-300 hover:-translate-y-1"
              >
                <div className="text-3xl md:text-4xl font-bold gradient-text mb-2">{stat.number}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-16 relative">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold mb-12 text-center">
            <span className="gradient-text">Our Core Values</span>
          </h2>
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {values.map((value, index) => (
              <Card 
                key={index}
                className="bg-card/50 backdrop-blur border-border p-6 hover:border-primary/50 transition-all duration-300 group hover:-translate-y-1"
              >
                <div className="flex items-start gap-4">
                  <div className="p-3 rounded-lg bg-primary/10 group-hover:bg-primary/20 transition-colors">
                    <value.icon className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2 group-hover:text-primary transition-colors">{value.title}</h3>
                    <p className="text-muted-foreground">{value.description}</p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Join Community Section */}
      <section className="py-16 relative">
        <div className="container mx-auto px-4">
          <Card className="max-w-4xl mx-auto bg-gradient-to-r from-primary/10 via-secondary/10 to-primary/10 border-primary/20 p-8 md:p-12 text-center">
            <Globe className="w-12 h-12 mx-auto mb-6 text-primary" />
            <h2 className="text-2xl md:text-3xl font-bold mb-4">
              <span className="gradient-text">Join Our Global Community</span>
            </h2>
            <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
              Connect with thousands of security professionals on LinkedIn.
              Share knowledge, ask questions, and stay updated with the latest in defensive security.
            </p>
            <a
              href="https://www.linkedin.com/company/blueteamers/"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
            >
              Follow on LinkedIn
            </a>
          </Card>
        </div>
      </section>

      <Footer />
    </main>
  );
};

export default About;
