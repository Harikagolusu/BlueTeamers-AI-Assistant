import { Shield } from "lucide-react";
import { cn } from "@/lib/utils";
import { Link } from "react-router-dom";

const navItems = [
  { label: "Dashboard", href: "/labs" },
  { label: "Alerts", href: "/labs/alerts" },
  { label: "Incidents", href: "/labs/incidents" },
  { label: "Logs", href: "/labs/logs" },
  { label: "Endpoints", href: "/labs/endpoints" },
  { label: "Threat Intel", href: "/labs/threat-intel" },
  { label: "Email Security", href: "/labs/email-security" },
  { label: "Settings", href: "/labs/settings" },
];

interface SOCSidebarProps {
  activeItem?: string;
  locked?: boolean;
}

const SOCSidebar = ({ activeItem = "Dashboard", locked = false }: SOCSidebarProps) => {
  return (
    <aside className="w-16 lg:w-56 bg-card/25 backdrop-blur-lg border-r border-white/[0.08] flex flex-col shrink-0">
      <div className="p-4 border-b border-white/[0.06]">
        <h2 className="hidden lg:block text-lg font-bold gradient-text">SOC Labs</h2>
        <Shield className="lg:hidden w-8 h-8 text-primary mx-auto" />
      </div>

      <nav className="flex-1 py-4">
        {navItems.map((item) => {
          const isActive = item.label === activeItem;
          const isLocked = locked && item.label !== "Dashboard";
          if (isLocked) {
            return (
              <span
                key={item.label}
                className={cn(
                  "w-full flex items-center gap-3 px-4 py-3 text-sm cursor-not-allowed",
                  "text-muted-foreground/30"
                )}
              >
                <span className="text-center lg:text-left">{item.label}</span>
              </span>
            );
          }
          return (
            <Link
              key={item.label}
              to={item.href}
              className={cn(
                "w-full flex items-center gap-3 px-4 py-3 text-sm transition-all duration-200",
                "hover:bg-white/[0.04] hover:text-primary",
                isActive
                  ? "bg-primary/10 text-primary border-l-2 border-primary"
                  : "text-muted-foreground"
              )}
            >
              <span className="text-center lg:text-left">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-white/[0.06]">
        <div className="hidden lg:flex items-center gap-2 text-xs text-muted-foreground">
          <div className="w-2 h-2 bg-secondary rounded-full animate-pulse" />
          <span>System Online</span>
        </div>
      </div>
    </aside>
  );
};

export default SOCSidebar;
