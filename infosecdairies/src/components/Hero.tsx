import { Button } from "@/components/ui/button";
import { ChevronDown } from "lucide-react";
import logo from "@/assets/logo.png";

import FloatingParticles from "./FloatingParticles";
import AnimatedCounter from "./AnimatedCounter";
const Hero = () => {
  const scrollToContent = () => {
    window.scrollTo({
      top: window.innerHeight,
      behavior: 'smooth'
    });
  };
  return <section className="relative min-h-screen flex items-start justify-center overflow-hidden pt-14 md:pt-20">
      {/* Dark base with subtle gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-black via-slate-950 to-black" />
      
      {/* Animated scanlines */}
      <div className="absolute inset-0 bg-[linear-gradient(transparent_50%,rgba(0,255,200,0.03)_50%)] bg-[length:100%_4px] animate-scan" />
      
      {/* Hexagon pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTYiIGhlaWdodD0iMTAwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0yOCAwTDAgMjVWNzVMMjggMTAwTDU2IDc1VjI1WiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDBmZmM4IiBzdHJva2Utd2lkdGg9IjEiLz48L3N2Zz4=')] bg-[length:56px_100px]" />
      </div>
      
      {/* Vignette effect */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_0%,rgba(0,0,0,0.7)_100%)]" />
      
      <div className="relative z-10 container mx-auto px-4 text-center">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Logo with float animation */}
          
          
          {/* Heading with shimmer effect */}
          <h1 className="text-4xl sm:text-5xl md:text-7xl font-bold mb-6 animate-fade-up">
            <span className="gradient-text inline-block bg-[length:200%_auto] animate-gradient-shift">
              BlueTeamers
            </span>
          </h1>
          
          {/* Tagline with staggered animation */}
          <p className="text-base sm:text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto leading-relaxed animate-fade-up px-2" style={{
          animationDelay: '0.2s'
        }}>Hands-on Blue Team & SOC Training. Learn Detection, Threat Hunting, and Incident Response from Real Practitioners</p>

          {/* Animated Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-10 md:pt-16 max-w-2xl mx-auto">
            <div className="space-y-2 group hover:scale-110 transition-transform duration-300 animate-slide-right" style={{
            animationDelay: '0.6s'
          }}>
              <div className="w-8 h-8 mx-auto text-primary flex items-center justify-center text-2xl group-hover:animate-pulse">🛡️</div>
              <p className="text-2xl font-bold gradient-text">
                <AnimatedCounter end={100} suffix="%" />
              </p>
              <p className="text-sm text-muted-foreground">Blue Team Focus</p>
            </div>
            <div className="space-y-2 group hover:scale-110 transition-transform duration-300 animate-fade-up" style={{
            animationDelay: '0.7s'
          }}>
              <div className="w-8 h-8 mx-auto text-primary flex items-center justify-center text-2xl group-hover:animate-pulse">🛡️</div>
              <p className="text-2xl font-bold gradient-text">Real-World</p>
              <p className="text-sm text-muted-foreground">Detection & Response</p>
            </div>
            <div className="space-y-2 group hover:scale-110 transition-transform duration-300 animate-slide-left" style={{
            animationDelay: '0.8s'
          }}>
              <div className="w-8 h-8 mx-auto text-primary flex items-center justify-center text-2xl group-hover:animate-pulse">🔐</div>
              <p className="text-2xl font-bold gradient-text">Practitioner-Led</p>
              <p className="text-sm text-muted-foreground">Training</p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Scroll indicator */}
      <button onClick={scrollToContent} className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce cursor-pointer bg-transparent border-none text-primary hover:text-secondary transition-colors" aria-label="Scroll to content">
        <ChevronDown className="w-8 h-8" />
      </button>
    </section>;
};
export default Hero;