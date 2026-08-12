import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Shield, PanelLeft, UserCircle2, Menu, X } from "lucide-react";
import logo from "@/assets/logo.png";
import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/button";


const NAV_LINKS = [
  { to: "/", label: "Home" },
  { to: "/courses", label: "Certifications" },
  { to: "/labs", label: "Practice" },
  { to: "/about", label: "About" },
];

interface NavbarProps {
  /** "floating" renders a slimmer, glassy bar used as the top row of the AI Workspace.
   *  It sits in the normal layout flow (no overlay) so the Navbar and Workspace form one
   *  continuous surface with a single dividing line between them. */
  variant?: "default" | "floating";
    /** When provided (AI Workspace), renders a button that toggles the workspace sidebar. */
  onToggleSidebar?: () => void;
}

const Navbar = ({ variant = "default", onToggleSidebar }: NavbarProps) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [logoFailed, setLogoFailed] = useState(false);

  const isFloating = variant === "floating";
  const isChatPage = location.pathname === "/chat";

  // Show a shadow under the floating navbar only once the page scrolls.
  useEffect(() => {
    if (!isFloating) return;
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [isFloating]);

  const isActive = (path: string) => location.pathname === path;

  const linkClass = (path: string) =>
    `text-sm font-medium transition-colors ${
      isActive(path) ? "text-[#7bff81]" : "text-[#00ffc8] hover:text-[#7bff81]"
    }`;

  // Build auth link that returns user to current page after login.
  // Skip redirect for auth-flow pages themselves so we don't loop.
  const AUTH_FLOW_PATHS = ["/auth", "/verify-email", "/forgot-password", "/google/onboarding", "/auth/google-callback"];
  const isAuthPage = AUTH_FLOW_PATHS.some((p) => location.pathname.startsWith(p));
  const authLink = isAuthPage ? "/auth" : `/auth?redirect=${encodeURIComponent(location.pathname)}`;

  const closeMenu = () => setMenuOpen(false);

  return (
    <nav
      className={`w-full relative z-50 ${
        isFloating
          ? `border-b border-white/10 bg-[#020817]/40 backdrop-blur-md transition-shadow duration-300 ${
              scrolled ? "shadow-lg shadow-black/30" : ""
            }`
          : ""
      }`}
    >
      <div className="w-full px-4 md:px-6">
        <div className="flex items-center justify-between h-14 md:h-16">
          {/* Left: workspace sidebar toggle + brand */}
          <div className="flex items-center gap-2 sm:gap-3 min-w-0">
                        {onToggleSidebar && (
              <Button
                variant="outline"
                size="icon"
                onClick={onToggleSidebar}
                title="Toggle Sidebar"
                className="h-9 w-9 shrink-0 rounded-lg border-border hover:bg-primary/10 hover:text-primary hover:border-primary/30 transition-all duration-300"
              >
                <PanelLeft className="w-4 h-4" />
              </Button>
            )}

            {/* Logo (brand) — hidden in the AI Workspace navbar so the clean
                "AI Workspace" title reads on its own. */}
            {!isFloating && (
            <Link
              to="/"
              onClick={closeMenu}
              aria-label="BlueTeamers home"
              className="flex-shrink-0 flex items-center group"
            >
              {logoFailed ? (
                <span className="flex items-center gap-2">
                  <Shield className="w-6 h-6 md:w-7 md:h-7 text-[#00ffc8]" />
                  <span className="text-lg md:text-xl font-bold gradient-text">BlueTeamers</span>
                </span>
              ) : (
                <img
                  src={logo}
                  alt="BlueTeamers"
                  className={`w-auto object-contain ${isFloating ? "h-9 md:h-10" : "h-12 md:h-16"}`}
                  onError={() => setLogoFailed(true)}
                />
              )}
            </Link>
            )}

            {/* Workspace brand (AI Workspace page only) */}
            {isChatPage && (
              <div className="min-w-0 leading-tight">
                <span className="font-semibold text-sm md:text-base text-foreground tracking-wide truncate">
                  BlueTeamers <span className="gradient-text">AI Workspace</span>
                </span>
              </div>
            )}
          </div>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-8 ml-auto">
            {NAV_LINKS.map(({ to, label }) => (
              <Link key={to} to={to} className={linkClass(to)}>
                {label}
              </Link>
            ))}
            {!isAuthenticated ? (
              <Link to={authLink} className="text-sm font-medium text-[#00ffc8] hover:text-[#7bff81] transition-colors">
                Login / Sign Up
              </Link>
            ) : (
              <div className="relative group">
                <button
                  type="button"
                  className="flex items-center gap-2 text-sm font-medium text-[#00ffc8] hover:text-[#7bff81] transition-colors"
                >
                  <UserCircle2 className="w-6 h-6" />
                  <span>{user?.fullName || user?.email?.split("@")[0] || "Profile"}</span>
                </button>
                <div className="absolute right-0 mt-2 w-44 rounded-md bg-[#020817] border border-[#00ffc8]/20 shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                  <button
                    type="button"
                    className="w-full text-left px-4 py-2 text-sm text-[#00ffc8] hover:bg-[#020B1B]"
                    onClick={() => navigate("/dashboard")}
                  >
                    My Dashboard
                  </button>
                  <button
                    type="button"
                    className="w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-[#200910]"
                    onClick={logout}
                  >
                    Logout
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Mobile hamburger */}
          <button
            type="button"
            className="md:hidden ml-auto text-[#00ffc8] p-2"
            onClick={() => setMenuOpen((o) => !o)}
            aria-label="Toggle menu"
          >
            {menuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile slide-down menu */}
      {menuOpen && (
        <div className="md:hidden absolute top-full left-0 w-full bg-[#020817] border-t border-[#00ffc8]/20 z-50 shadow-xl">
          <div className="flex flex-col px-6 py-4 gap-4">
            {NAV_LINKS.map(({ to, label }) => (
              <Link key={to} to={to} className={linkClass(to)} onClick={closeMenu}>
                {label}
              </Link>
            ))}
            {!isAuthenticated ? (
              <Link
                to={authLink}
                className="text-sm font-medium text-[#00ffc8] hover:text-[#7bff81] transition-colors"
                onClick={closeMenu}
              >
                Login / Sign Up
              </Link>
            ) : (
              <>
                <button
                  type="button"
                  className="text-left text-sm font-medium text-[#00ffc8] hover:text-[#7bff81] transition-colors"
                  onClick={() => { navigate("/dashboard"); closeMenu(); }}
                >
                  My Dashboard
                </button>
                <button
                  type="button"
                  className="text-left text-sm font-medium text-red-400 hover:text-red-300 transition-colors"
                  onClick={() => { logout(); closeMenu(); navigate("/"); }}
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
