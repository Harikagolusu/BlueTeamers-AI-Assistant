import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Eye, AlertTriangle, FileSearch, Lock, Activity, Target } from "lucide-react";
import { useState } from "react";

const topics = [
  {
    icon: Target,
    title: "Threat Detection",
    description: "Advanced techniques for identifying and analyzing security threats in real-time",
    color: "from-primary to-secondary"
  },
  {
    icon: Eye,
    title: "Security Monitoring",
    description: "Continuous surveillance and analysis of network traffic and system activities",
    color: "from-secondary to-primary"
  },
  {
    icon: AlertTriangle,
    title: "Incident Response",
    description: "Structured approaches to handling and recovering from security incidents",
    color: "from-primary to-accent"
  },
  {
    icon: FileSearch,
    title: "Log Analysis",
    description: "Deep dive into security logs to uncover anomalies and potential threats",
    color: "from-accent to-secondary"
  },
  {
    icon: Lock,
    title: "Access Control",
    description: "Implementing robust authentication and authorization mechanisms",
    color: "from-secondary to-accent"
  },
  {
    icon: Activity,
    title: "SIEM Solutions",
    description: "Security Information and Event Management best practices and tools",
    color: "from-accent to-primary"
  }
];

const Topics = () => {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  return (
    <section className="py-20 relative">
      <div className="absolute inset-0 circuit-pattern opacity-5" />
      
      <div className="container mx-auto px-4 relative z-10">
        <div className="text-center mb-16 animate-fade-up">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="gradient-text">Blue Team Topics</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Comprehensive coverage of defensive cybersecurity concepts and practices
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {topics.map((topic, index) => {
            const Icon = topic.icon;
            const isHovered = hoveredIndex === index;
            
            return (
              <Card 
                key={index} 
                className="bg-card/50 backdrop-blur border-border hover:border-primary/50 transition-all duration-500 group cursor-pointer relative overflow-hidden animate-fade-up"
                style={{ animationDelay: `${index * 0.1}s` }}
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
              >
                {/* Animated background gradient */}
                <div 
                  className={`absolute inset-0 bg-gradient-to-br ${topic.color} opacity-0 group-hover:opacity-10 transition-opacity duration-500`}
                />
                
                {/* Shimmer effect on hover */}
                {isHovered && (
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/10 to-transparent animate-shimmer" 
                       style={{ backgroundSize: '200% 100%' }} />
                )}
                
                <CardHeader className="relative z-10">
                  <div className="w-12 h-12 rounded-lg bg-gradient-cyber flex items-center justify-center mb-4 group-hover:scale-110 group-hover:rotate-6 transition-all duration-300 glow-cyan">
                    <Icon className="w-6 h-6 text-primary-foreground" />
                  </div>
                  <CardTitle className="text-xl gradient-text group-hover:scale-105 transition-transform duration-300 inline-block">
                    {topic.title}
                  </CardTitle>
                </CardHeader>
                <CardContent className="relative z-10">
                  <CardDescription className="text-muted-foreground group-hover:text-foreground transition-colors duration-300">
                    {topic.description}
                  </CardDescription>
                </CardContent>
                
                {/* Corner accent */}
                <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-primary/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Topics;
