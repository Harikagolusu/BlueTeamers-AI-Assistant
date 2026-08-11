import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { ArrowLeft, Eye, EyeOff, Loader2, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { apiUrl } from "@/services/api";

const GoogleOnboarding = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const passwordRules = useMemo(() => {
    const value = password || "";
    return {
      minLen: value.length >= 10,
      upper: /[A-Z]/.test(value),
      lower: /[a-z]/.test(value),
      digit: /\d/.test(value),
      symbol: /[^A-Za-z0-9]/.test(value),
    };
  }, [password]);

  const email = useMemo(() => searchParams.get("email") || "", [searchParams]);

  useEffect(() => {
    if (!email) {
      navigate("/auth", { replace: true });
      return;
    }
    // New flow: backend passes onboarding token via ?ot= query param.
    // Store it in sessionStorage so the existing submit handler finds it.
    const ot = searchParams.get("ot");
    if (ot) {
      sessionStorage.setItem("googleOnboardingToken", ot);
    }
  }, [email, navigate, searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!firstName || !lastName || !password || !confirmPassword) {
      setError("All fields are required.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    const onboardingToken = sessionStorage.getItem("googleOnboardingToken") || "";
    if (!onboardingToken) {
      setError("Authentication required. Please sign in with Google again.");
      return;
    }

    try {
      setLoading(true);

      const res = await fetch(apiUrl("/api/auth/google/onboarding/"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${onboardingToken}`,
        },
        credentials: "include",
        body: JSON.stringify({ first_name: firstName, last_name: lastName, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        const msg = data.detail;
        if (Array.isArray(msg)) {
          setError(msg[0] || "Could not complete signup.");
        } else {
          setError(msg || "Could not complete signup.");
        }
        return;
      }

      if (data.requires_verification) {
        sessionStorage.removeItem("googleOnboardingToken");
        const rawRedirect = sessionStorage.getItem("authRedirect") || "";
        sessionStorage.removeItem("authRedirect");
        const redirectParam = rawRedirect.startsWith("/") && !rawRedirect.startsWith("//") && !rawRedirect.startsWith("/\\") ? rawRedirect : "";
        setSuccess("Verification code sent! Redirecting...");
        setTimeout(() => {
          const verifyUrl = `/verify-email?email=${encodeURIComponent(data.email || email)}${redirectParam ? `&redirect=${encodeURIComponent(redirectParam)}` : ""}`;
          navigate(verifyUrl, { replace: true });
        }, 800);
        return;
      }

      setError("Unexpected response from server.");
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="absolute inset-0 circuit-pattern opacity-5" />

      <div className="w-full max-w-md relative z-10">
        <div className="text-center mb-8 animate-fade-up">
          <Link to="/" className="inline-flex items-center gap-2 mb-4 group">
            <span className="font-bold text-2xl gradient-text">BlueTeamers</span>
          </Link>
          <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
            <User className="w-8 h-8 text-primary" />
          </div>
          <h1 className="text-3xl font-bold">Complete Signup</h1>
          <p className="text-muted-foreground mt-2">Set up your profile and password</p>
          {email && (
            <p className="text-xs text-muted-foreground mt-2">{email}</p>
          )}
        </div>

        <div className="bg-card border border-border rounded-lg p-8 animate-fade-up" style={{ animationDelay: "100ms" }}>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <Label htmlFor="firstName">First Name</Label>
              <Input
                id="firstName"
                type="text"
                placeholder="First name"
                className="bg-background"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                disabled={loading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="lastName">Last Name</Label>
              <Input
                id="lastName"
                type="text"
                placeholder="Last name"
                className="bg-background"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                disabled={loading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  className="bg-background pr-10"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute inset-y-0 right-0 flex items-center pr-3 text-muted-foreground hover:text-foreground"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              <div className="mt-2 rounded-md border border-border bg-background/40 p-3">
                <p className="text-xs text-muted-foreground mb-2">Password must include:</p>
                <div className="space-y-1 text-xs">
                  <div className={passwordRules.minLen ? "text-green-500" : "text-muted-foreground"}>
                    At least 10 characters
                  </div>
                  <div className={passwordRules.upper ? "text-green-500" : "text-muted-foreground"}>
                    One uppercase letter (A-Z)
                  </div>
                  <div className={passwordRules.lower ? "text-green-500" : "text-muted-foreground"}>
                    One lowercase letter (a-z)
                  </div>
                  <div className={passwordRules.digit ? "text-green-500" : "text-muted-foreground"}>
                    One number (0-9)
                  </div>
                  <div className={passwordRules.symbol ? "text-green-500" : "text-muted-foreground"}>
                    One symbol (!@#$...)
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirmPassword">Confirm Password</Label>
              <div className="relative">
                <Input
                  id="confirmPassword"
                  type={showConfirmPassword ? "text" : "password"}
                  placeholder="••••••••"
                  className="bg-background pr-10"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword((prev) => !prev)}
                  className="absolute inset-y-0 right-0 flex items-center pr-3 text-muted-foreground hover:text-foreground"
                  aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                >
                  {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {error && <p className="text-sm text-red-500">{error}</p>}
            {success && <p className="text-sm text-green-500">{success}</p>}

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Continuing...
                </>
              ) : (
                "Next"
              )}
            </Button>

            <div className="mt-2 text-center">
              <Link to="/auth" className="text-sm text-muted-foreground hover:text-primary transition-colors inline-flex items-center">
                <ArrowLeft className="w-4 h-4 mr-1" />
                Back to login
              </Link>
            </div>
          </form>
        </div>
      </div>
    </main>
  );
};

export default GoogleOnboarding;
