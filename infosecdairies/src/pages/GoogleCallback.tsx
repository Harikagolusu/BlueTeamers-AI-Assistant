import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { apiUrl } from "@/services/api";

const GoogleCallback = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleCallback = async () => {
      try {
        setError(null);

        // New flow: backend token-redirect passes JWT tokens in URL hash.
        // This avoids the cross-domain SameSite=Lax session cookie problem.
        const hash = window.location.hash;
        if (hash && hash.length > 1) {
          const params = new URLSearchParams(hash.slice(1));
          const access = params.get("access");
          const refresh = params.get("refresh");
          const email = params.get("email");
          const fullName = params.get("full_name") || undefined;
          const authError = params.get("error");

          // Remove tokens from browser history immediately
          window.history.replaceState(null, "", window.location.pathname);

          if (authError) {
            setError("Could not complete Google login. Please try again.");
            return;
          }

          if (access && email) {
            login({ email, fullName, tokens: { access, refresh: refresh || undefined } });
            const raw = sessionStorage.getItem("authRedirect") || "";
            sessionStorage.removeItem("authRedirect");
            const dest = (raw.startsWith("/") && !raw.startsWith("//") && !raw.startsWith("/\\")) ? raw : "/dashboard";
            navigate(dest, { replace: true });
            return;
          }
        }

        // Legacy fallback: session-cookie flow for same-site (infosecdairies.io)
        // or when backend hasn't deployed the new token-redirect view yet.
        const res = await fetch(apiUrl("/api/auth/google/jwt/"), {
          method: "GET",
          credentials: "include",
        });

        if (!res.ok) {
          setError("Could not complete Google login. Please try again.");
          return;
        }

        const data = await res.json();

        if (data.requires_onboarding) {
          if (data.onboarding_token) {
            sessionStorage.setItem("googleOnboardingToken", String(data.onboarding_token));
          } else {
            sessionStorage.removeItem("googleOnboardingToken");
          }
          navigate(`/google/onboarding?email=${encodeURIComponent(data.email || "")}`, { replace: true });
          return;
        }

        if (data.requires_verification) {
          navigate(`/verify-email?email=${encodeURIComponent(data.email)}`, { replace: true });
          return;
        }

        const user = data.user || {};
        const tokens = data.tokens || {};

        if (!user.email || !tokens.access) {
          setError("Invalid response from server during Google login.");
          return;
        }

        login({ email: user.email, fullName: user.full_name, tokens });
        const raw = sessionStorage.getItem("authRedirect") || "";
        sessionStorage.removeItem("authRedirect");
        const dest = (raw.startsWith("/") && !raw.startsWith("//") && !raw.startsWith("/\\")) ? raw : "/dashboard";
        navigate(dest, { replace: true });
      } catch {
        setError("Network error while completing Google login.");
      }
    };

    handleCallback();
  }, [login, navigate]);

  return (
    <main className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="text-center text-foreground">
        <h1 className="text-2xl font-bold mb-2">Completing Google sign-in...</h1>
        <p className="text-muted-foreground mb-4">
          Please wait while we secure your session.
        </p>
        {error && <p className="text-sm text-red-500">{error}</p>}
      </div>
    </main>
  );
};

export default GoogleCallback;
