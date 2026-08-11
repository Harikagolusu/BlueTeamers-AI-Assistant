import { useMemo, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { Eye, EyeOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/context/AuthContext";
import { apiUrl } from "@/services/api";
import { verifyJwtLocally } from "@/lib/jwtVerify";

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const passwordRules = useMemo(() => {
    const value = password || "";
    return {
      minLen: value.length >= 10,
      maxLen: value.length <= 15 && value.length > 0,
      upper: /[A-Z]/.test(value),
      lower: /[a-z]/.test(value),
      digit: /\d/.test(value),
      symbol: /[^A-Za-z0-9]/.test(value),
    };
  }, [password]);

  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const isSafeRedirect = (p: string) => p.startsWith("/") && !p.startsWith("//") && !p.startsWith("/\\");
  const rawRedirect = searchParams.get("redirect") || "";
  const redirectTo = isSafeRedirect(rawRedirect) ? rawRedirect : "";
  const { login } = useAuth();

  const handleGoogleLogin = () => {
    if (redirectTo) sessionStorage.setItem("authRedirect", redirectTo);
    const frontendCallback = `${window.location.origin}/auth/google-callback`;
    const tokenRedirectPath = `/api/auth/google/token-redirect/?target=${encodeURIComponent(frontendCallback)}`;
    window.location.href = apiUrl(`/accounts/google/login/?next=${encodeURIComponent(tokenRedirectPath)}`);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!email || !password) {
      setError("Email and password are required.");
      return;
    }

    if (!isLogin) {
      if (!firstName || !lastName) {
        setError("First name and last name are required for sign up.");
        return;
      }
      if (password.length > 15) {
        setError("Password must be at most 15 characters.");
        return;
      }
      if (password !== confirmPassword) {
        setError("Passwords do not match.");
        return;
      }
    }

    try {
      setLoading(true);

      const url = isLogin
        ? `/api/auth/login/`
        : `/api/auth/register/`;

      const body = isLogin
        ? { email, password }
        : { full_name: `${firstName} ${lastName}`.trim(), email, password };

      const response = await fetch(apiUrl(url), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        if (data && typeof data === "object") {
          const firstErrorKey = Object.keys(data)[0];
          const firstErrorValue =
            firstErrorKey && Array.isArray(data[firstErrorKey])
              ? data[firstErrorKey][0]
              : data[firstErrorKey] || data.detail || "Something went wrong. Please try again.";
          setError(String(firstErrorValue));
        } else {
          setError("Something went wrong. Please try again.");
        }
        return;
      }

      // After registration ALWAYS go to email verification — never trust the server flag.
      // An attacker could change requires_verification:true → false in Burp to skip OTP.
      // The backend enforces is_active=False so login would fail anyway, but we also
      // enforce the redirect here so the UX is consistent and the account is usable.
      if (!isLogin) {
        setSuccess("Verification code sent! Redirecting to verification page...");
        setTimeout(() => {
          const verifyUrl = `/verify-email?email=${encodeURIComponent(data.email || email)}${redirectTo ? `&redirect=${encodeURIComponent(redirectTo)}` : ""}`;
          navigate(verifyUrl);
        }, 1000);
        return;
      }

      const tokens = data.tokens;

      if (!tokens?.access) {
        setError("Authentication failed. Please try again.");
        setLoading(false);
        return;
      }

      // PRIMARY SECURITY LAYER — RS256 local signature verification.
      // When the server has JWT_PRIVATE_KEY configured it signs with RS256 and we verify
      // the signature entirely in-browser using the hardcoded public key (zero-network,
      // nothing to intercept or replay).
      // If the server is misconfigured and falls back to HS256 we cannot verify locally
      // (the HMAC secret is server-side only), so we skip local verification and let the
      // server verify endpoint be the sole authority.
      let localVerifyOk = false;
      let verifiedPayload: Awaited<ReturnType<typeof verifyJwtLocally>> | null = null;
      try {
        verifiedPayload = await verifyJwtLocally(tokens.access);
        localVerifyOk = true;
      } catch (e) {
        const msg = e instanceof Error ? e.message : "";
        // Algorithm mismatch = server is using HS256 fallback — not a forged token.
        // Fall through to the server verify endpoint which will validate it properly.
        if (!msg.toLowerCase().includes("algorithm") && !msg.toLowerCase().includes("unsupported")) {
          setError("Authentication failed: invalid token signature.");
          setLoading(false);
          return;
        }
      }

      // When RS256 local verify succeeded, confirm the email claim matches.
      if (localVerifyOk && verifiedPayload) {
        if (
          !verifiedPayload.email ||
          verifiedPayload.email.toLowerCase() !== email.toLowerCase().trim()
        ) {
          setError("Authentication failed. Please try again.");
          setLoading(false);
          return;
        }
      }

      // SERVER VERIFY — validates token against backend (blacklist check + HS256 fallback path).
      const verifyResponse = await fetch(apiUrl("/api/auth/verify/"), {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${tokens.access}`,
          "Content-Type": "application/json",
        },
      });

      if (!verifyResponse.ok) {
        setError("Invalid session. Please try logging in again.");
        setLoading(false);
        return;
      }

      const verifyData = await verifyResponse.json();
      if (!verifyData.valid) {
        setError("Session validation failed. Please try again.");
        setLoading(false);
        return;
      }

      const userData = data.user || {};
      const userEmail: string = userData.email || email;
      const fullNameFromApi: string | undefined =
        userData.full_name || `${firstName} ${lastName}`.trim() || undefined;

      login({ email: userEmail, fullName: fullNameFromApi, tokens });

      setSuccess(isLogin ? "Logged in successfully." : "Account created successfully.");

      setTimeout(() => {
        navigate(redirectTo || "/courses");
      }, 800);
    } catch (err) {
      setError("Network error. Please check your connection and try again.");
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
          <h1 className="text-3xl font-bold mt-4">
            {isLogin ? "Welcome Back" : "Create Account"}
          </h1>
          <p className="text-muted-foreground mt-2">
            {isLogin
              ? "Enter your credentials to access your account"
              : "Sign up to start your blue team journey"}
          </p>
        </div>

        <div className="bg-card border border-border rounded-lg p-8 animate-fade-up" style={{ animationDelay: "100ms" }}>
          <form className="space-y-4" onSubmit={handleSubmit}>
            {!isLogin && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="firstName">First Name</Label>
                  <Input
                    id="firstName"
                    type="text"
                    placeholder="First name"
                    className="bg-background"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
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
                  />
                </div>
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                className="bg-background"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
                  maxLength={15}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute inset-y-0 right-0 flex items-center pr-3 text-muted-foreground hover:text-foreground"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4" />
                  ) : (
                    <Eye className="w-4 h-4" />
                  )}
                </button>
              </div>
              {!isLogin && (
                <div className="mt-2 rounded-md border border-border bg-background/40 p-3">
                  <p className="text-xs text-muted-foreground mb-2">Password must include:</p>
                  <div className="space-y-1 text-xs">
                    <div className={passwordRules.minLen ? "text-green-500" : "text-muted-foreground"}>
                      At least 10 characters
                    </div>
                    <div className={password.length === 0 ? "text-muted-foreground" : passwordRules.maxLen ? "text-green-500" : "text-red-500"}>
                      At most 15 characters
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
              )}
            </div>

            {!isLogin && (
              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirm Password</Label>
                <div className="relative">
                  <Input
                    id="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder="••••••••"
                    className="bg-background pr-10"
                    value={confirmPassword}
                    maxLength={15}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword((prev) => !prev)}
                    className="absolute inset-y-0 right-0 flex items-center pr-3 text-muted-foreground hover:text-foreground"
                    aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="w-4 h-4" />
                    ) : (
                      <Eye className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>
            )}

            {error && (
              <p className="text-sm text-red-500">{error}</p>
            )}

            {success && (
              <p className="text-sm text-green-500">{success}</p>
            )}

            <Button type="submit" className="w-full" disabled={loading}>
              {loading
                ? isLogin
                  ? "Signing in..."
                  : "Creating account..."
                : isLogin
                  ? "Sign In"
                  : "Sign Up"}
            </Button>

            {isLogin && (
              <div className="text-right">
                <Link
                  to={`/forgot-password?email=${encodeURIComponent(email || "")}`}
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                  Forgot password?
                </Link>
              </div>
            )}

            <div className="mt-4 flex items-center justify-center">
              <button
                type="button"
                onClick={handleGoogleLogin}
                className="w-full inline-flex items-center justify-center gap-2 rounded-md border border-[#00ffc8]/60 text-sm font-medium text-[#00ffc8] hover:bg-[#00ffc8]/10 transition-colors py-2"
              >
                <span>Continue with Google</span>
              </button>
            </div>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              {isLogin
                ? "Don't have an account? Sign up"
                : "Already have an account? Sign in"}
            </button>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Auth;
