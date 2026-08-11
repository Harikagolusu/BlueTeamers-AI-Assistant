import { Button } from "@/components/ui/button";
import { Linkedin } from "lucide-react";
import { useEffect, useRef, useState } from "react";

const CTA = () => {
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
    <section ref={ref} className="py-20 relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 bg-gradient-cyber opacity-10 animate-gradient-shift" style={{ backgroundSize: '200% 200%' }} />
      <div className="absolute inset-0 circuit-pattern opacity-5" />

      <div className="container mx-auto px-4 relative z-10">
        <div className={`max-w-3xl mx-auto text-center space-y-8 transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <h2 className="text-4xl md:text-5xl font-bold">
            <span className="gradient-text inline-block bg-[length:200%_auto] animate-gradient-shift">
              Join the Community
            </span>
          </h2>

          <p className={`text-xl text-muted-foreground transition-all duration-500`} style={{ transitionDelay: isVisible ? '0.2s' : '0s' }}>
            Stay updated with the latest in blue team cybersecurity.
            Connect with us on LinkedIn for insights, tips, and discussions.
          </p>

          <div className={`flex justify-center items-center pt-4 transition-all duration-500`} style={{ transitionDelay: isVisible ? '0.4s' : '0s' }}>
            <Button
              size="lg"
              className="bg-[#0077B5] hover:bg-[#0077B5]/90 transition-all duration-300 hover:scale-110 group"
              asChild
            >
              <a
                href="https://www.linkedin.com/company/blueteamers/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2"
              >
                <Linkedin className="w-5 h-5 group-hover:scale-110 transition-transform" />
                LinkedIn
              </a>
            </Button>
          </div>

          <p className={`text-sm text-muted-foreground pt-8 transition-all duration-500`} style={{ transitionDelay: isVisible ? '0.6s' : '0s' }}>
            <span className="inline-block animate-pulse">🔒</span> Defending today, securing tomorrow
          </p>
        </div>
      </div>
    </section>
  );
};

export default CTA;
