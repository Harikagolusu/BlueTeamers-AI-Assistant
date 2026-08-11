import { Users, BookOpen, Target, Zap } from "lucide-react";
import { useEffect, useRef, useState } from "react";
const features = [{
  icon: Target,
  title: "Blue Team Focused",
  description: "Dedicated entirely to defensive security - no distractions, pure defense mastery"
}, {
  icon: BookOpen,
  title: "Real-World Labs",
  description: "Hands-on environments simulating actual SOC scenarios and threat landscapes"
}, {
  icon: Users,
  title: "Community Driven",
  description: "Learn alongside fellow defenders, share insights, and grow together"
}, {
  icon: Zap,
  title: "Always Current",
  description: "Content updated with the latest threats, tools, and defensive techniques"
}];
const WhyChooseUs = () => {
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
      {/* Background elements */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-muted/20 to-background" />
      <div className="absolute inset-0 circuit-pattern opacity-5" />
      
      <div className="container mx-auto px-4 relative z-10">
        <div className={`text-center mb-16 transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="gradient-text">Why BlueTeamers?</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">We're not just another cybersecurity platform we're your defensive headquarters</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
          const Icon = feature.icon;
          return <div key={index} className={`relative group p-6 rounded-xl border border-border bg-card/30 backdrop-blur hover:border-primary/50 transition-all duration-500 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`} style={{
            transitionDelay: `${index * 0.1}s`
          }}>
                {/* Hover gradient overlay */}
                <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/10 to-secondary/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                
                <div className="relative z-10">
                  <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center mb-4 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300">
                    <Icon className="w-7 h-7 text-primary-foreground" />
                  </div>
                  
                  <h3 className="text-lg font-semibold mb-2 text-foreground group-hover:text-primary transition-colors duration-300">
                    {feature.title}
                  </h3>
                  
                  <p className="text-sm text-muted-foreground group-hover:text-foreground/80 transition-colors duration-300">
                    {feature.description}
                  </p>
                </div>
                
                {/* Corner accent */}
                <div className="absolute bottom-0 right-0 w-16 h-16 bg-gradient-to-tl from-primary/20 to-transparent rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              </div>;
        })}
        </div>
      </div>
    </section>;
};
export default WhyChooseUs;