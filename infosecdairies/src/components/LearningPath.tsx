import { useEffect, useRef, useState } from "react";
import { ArrowRight, GraduationCap, Briefcase, Award, Rocket } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
const steps = [{
  icon: GraduationCap,
  title: "Learn the Fundamentals",
  description: "Start with core SOC concepts, log analysis basics, and threat understanding",
  tag: "Beginner"
}, {
  icon: Briefcase,
  title: "Hands-On Practice",
  description: "Apply skills in realistic lab environments with real security tools",
  tag: "Intermediate"
}, {
  icon: Award,
  title: "Master the Craft",
  description: "Deep dive into SIEM, threat hunting, and advanced incident response",
  tag: "Advanced"
}, {
  icon: Rocket,
  title: "Join the Frontlines",
  description: "Become a defender. Protect organizations from real-world threats",
  tag: "Expert"
}];
const LearningPath = () => {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setIsVisible(true);
      }
    }, {
      threshold: 0.1
    });
    if (ref.current) {
      observer.observe(ref.current);
    }
    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, []);
  return <section ref={ref} className="py-20 relative overflow-hidden">
      {/* Animated scanlines */}
      <div className="absolute inset-0 bg-[linear-gradient(transparent_50%,rgba(0,255,200,0.02)_50%)] bg-[length:100%_4px]" />
      
      <div className="container mx-auto px-4 relative z-10">
        <div className={`text-center mb-16 transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="gradient-text">Your Defender Journey</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">From curious beginner to seasoned blue teamer, we'll guide you every step</p>
        </div>

        {/* Timeline */}
        <div className="relative max-w-4xl mx-auto">
          {/* Connecting line */}
          <div className="hidden md:block absolute left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-primary via-secondary to-primary opacity-30" />
          
          {steps.map((step, index) => {
          const Icon = step.icon;
          const isLeft = index % 2 === 0;
          return <div key={index} className={`relative flex items-center mb-12 last:mb-0 ${isLeft ? 'md:flex-row' : 'md:flex-row-reverse'} transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`} style={{
            transitionDelay: `${index * 0.15}s`
          }}>
                {/* Content */}
                <div className={`flex-1 ${isLeft ? 'md:pr-12 md:text-right' : 'md:pl-12 md:text-left'}`}>
                  <div className={`group p-6 rounded-xl border border-border bg-card/50 backdrop-blur hover:border-primary/50 transition-all duration-300 hover:glow-cyan`}>
                    <span className="inline-block px-3 py-1 text-xs font-medium rounded-full bg-primary/20 text-primary mb-3">
                      {step.tag}
                    </span>
                    <h3 className="text-xl font-semibold mb-2 text-foreground group-hover:text-primary transition-colors">
                      {step.title}
                    </h3>
                    <p className="text-muted-foreground text-sm">
                      {step.description}
                    </p>
                  </div>
                </div>
                
                {/* Center icon */}
                <div className="hidden md:flex w-16 h-16 rounded-full bg-gradient-to-br from-primary to-secondary items-center justify-center z-10 shrink-0 shadow-lg">
                  <Icon className="w-7 h-7 text-primary-foreground" />
                </div>
                
                {/* Mobile icon */}
                <div className="md:hidden absolute -left-2 top-6 w-12 h-12 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center z-10">
                  <Icon className="w-5 h-5 text-primary-foreground" />
                </div>
                
                {/* Spacer for alternating layout */}
                <div className="hidden md:block flex-1" />
              </div>;
        })}
        </div>

        {/* CTA */}
        <div className={`text-center mt-16 transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`} style={{
        transitionDelay: '0.6s'
      }}>
          <Button asChild size="lg" className="bg-gradient-to-r from-primary to-secondary hover:opacity-90 transition-all duration-300 group">
            <Link to="/courses" className="flex items-center gap-2">
              Start Your Journey
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
          </Button>
        </div>
      </div>
    </section>;
};
export default LearningPath;