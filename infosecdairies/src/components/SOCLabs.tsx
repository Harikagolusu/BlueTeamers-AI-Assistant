import { Terminal, Activity, Eye, ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";
import socLabsHero from "@/assets/soc-labs-hero.jpg";
const SOCLabs = () => {
  const features = [
    {
      icon: Terminal,
      title: "Real-Time Alert Triage",
      description: "Analyze live security alerts just like a SOC analyst would in production environments.",
    },
    {
      icon: Activity,
      title: "Threat Investigation",
      description: "Deep dive into suspicious activities, correlate events, and build incident timelines.",
    },
    {
      icon: Eye,
      title: "SIEM Mastery",
      description: "Get hands-on experience with dashboards, queries, and detection rules used by top security teams.",
    },
  ];
  return (
    <section className="py-20 relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-muted/20 to-background" />

      <div className="container mx-auto px-4 relative z-10">
        {/* Section Header */}
        <div className="text-center mb-12">
          <span className="inline-block px-4 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-sm font-medium mb-4">
            Hands-On Training
          </span>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Step Into a <span className="gradient-text">Real SOC Environment</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto text-lg">
            Stop watching. Start defending. Our practical labs simulate the exact workflows used by Security Operations
            Centers worldwide.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Image Section */}
          <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-primary/50 to-secondary/50 rounded-2xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity duration-500" />
            <div className="relative rounded-xl overflow-hidden border border-border">
              <img src={socLabsHero} alt="SOC Labs Dashboard" className="w-full h-auto object-cover" />
              {/* Overlay with stats */}
              <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-background/95 to-transparent p-6">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                    <span className="text-muted-foreground">Live Lab Environment</span>
                  </div>
                  <span className="text-primary font-mono">24/7 Access</span>
                </div>
              </div>
            </div>
          </div>

          {/* Features Grid */}
          <div className="space-y-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group flex gap-4 p-4 rounded-lg bg-card/50 border border-border/50 hover:border-primary/30 hover:bg-card transition-all duration-300"
              >
                <div>
                  <h3 className="font-semibold text-foreground mb-1">{feature.title}</h3>
                  <p className="text-sm text-muted-foreground">{feature.description}</p>
                </div>
              </div>
            ))}

            {/* CTA Button */}
            <Link
              to="/labs"
              className="inline-flex items-center gap-2 mt-4 px-6 py-3 bg-primary text-primary-foreground font-medium rounded-lg hover:bg-primary/90 transition-colors group"
            >
              Explore the Labs
              <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};
export default SOCLabs;
