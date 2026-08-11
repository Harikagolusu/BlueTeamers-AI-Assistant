import { Card } from "@/components/ui/card";
import { useEffect, useRef, useState } from "react";

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

  return (
    <section ref={ref} className="py-20 relative">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <Card className={`bg-card/50 backdrop-blur border-border p-8 md:p-12 relative overflow-hidden group transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            {/* Animated border effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-primary via-secondary to-primary opacity-0 group-hover:opacity-20 transition-opacity duration-500 blur-xl" />
            
            <h2 className="text-3xl md:text-4xl font-bold mb-6 text-center relative z-10">
              <span className="gradient-text inline-block group-hover:scale-105 transition-transform duration-300">
                About BlueTeamers
              </span>
            </h2>
            
            <div className="space-y-6 text-muted-foreground leading-relaxed relative z-10">
              <p className={`text-lg transition-all duration-500 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'}`} style={{ transitionDelay: '0.1s' }}>
                BlueTeamers is your trusted source for blue team cybersecurity knowledge.
                We focus on defensive security strategies, helping security professionals and 
                enthusiasts understand the art of protection, detection, and response.
              </p>
              
              <p className={`text-lg transition-all duration-500 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'}`} style={{ transitionDelay: '0.2s' }}>
                Our mission is to demystify complex security concepts and provide actionable 
                insights that can be applied in real-world scenarios. Whether you're a seasoned 
                security analyst or just starting your journey in cybersecurity, we've got you covered.
              </p>
              
              <div className={`pt-6 transition-all duration-500 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`} style={{ transitionDelay: '0.3s' }}>
                <h3 className="text-xl font-semibold mb-4 gradient-text">What We Cover:</h3>
                <ul className="space-y-3">
                  {[
                    "Security Operations Center (SOC) best practices",
                    "Threat hunting techniques and methodologies",
                    "Digital forensics and incident analysis",
                    "Security tool reviews and tutorials",
                    "Industry news and threat intelligence"
                  ].map((item, index) => (
                    <li 
                      key={index}
                      className={`flex items-start group/item hover:translate-x-2 transition-all duration-300 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'}`}
                      style={{ transitionDelay: `${0.4 + index * 0.1}s` }}
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
  );
};

export default About;
