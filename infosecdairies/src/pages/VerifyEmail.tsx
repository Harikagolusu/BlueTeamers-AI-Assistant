import { useState, useEffect } from "react";
import { Link, useSearchParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/context/AuthContext";
import { Loader2, Mail, ArrowLeft, RefreshCw } from "lucide-react";
import { apiUrl } from "@/services/api";

const VerifyEmail = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login } = useAuth();
  
  const [email, setEmail] = useState(searchParams.get("email") || "");
  const rawRedirect = searchParams.get("redirect") || "";
  const redirectTo = (rawRedirect.startsWith("/") && !rawRedirect.startsWith("//") && !rawRedirect.startsWith("/\\")) ? rawRedirect : "";
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [resendLoading, setResendLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [resendTimer, setResendTimer] = useState(60);

  const getResendUntilKey = (value: string) => `verifyEmailResendUntil:${value || "_"}`;

  const getRemainingSeconds = (value: string) => {
    const raw = localStorage.getItem(getResendUntilKey(value));
    const until = raw ? Number(raw) : 0;
    if (!Number.isFinite(until) || until <= 0) {
      return 0;
    }
    return Math.max(0, Math.ceil((until - Date.now()) / 1000));
  };

  const startResendCooldown = (value: string, seconds: number) => {
    const until = Date.now() + seconds * 1000;
    localStorage.setItem(getResendUntilKey(value), String(until));
    setResendTimer(seconds);
  };

  useEffect(() => {
    setResendTimer(getRemainingSeconds(email));
  }, [email]);

  // Countdown timer for resend button
  useEffect(() => {
    if (resendTimer > 0) {
      const timer = setTimeout(() => setResendTimer(resendTimer - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [resendTimer]);

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!email || !otp) {
      setError("Email and verification code are required.");
      return;
    }

    if (otp.length !== 6) {
      setError("Please enter a 6-digit code.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(apiUrl(`/api/auth/verify-email/`), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, code: otp }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Invalid or expired code. Please try again.");
        return;
      }

      // Verification successful - log user in
      const tokens = data.tokens;
      const userData = data.user || {};
      
      login({ 
        email: userData.email || email, 
        fullName: userData.full_name, 
        tokens 
      });

      setSuccess("Email verified! Redirecting...");

      setTimeout(() => {
        navigate(redirectTo || "/courses");
      }, 1000);
    } catch (err) {
      setError("Network error. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    if (!email) {
      setError("Please enter your email address.");
      return;
    }

    try {
      setResendLoading(true);
      setError(null);

      const response = await fetch(apiUrl(`/api/auth/resend-verification-otp/`), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      // Always show success for security (don't reveal if email exists)
      setSuccess("If an account exists, a new verification code has been sent.");
      startResendCooldown(email, 60);
    } catch (err) {
      setError("Failed to resend code. Please try again.");
    } finally {
      setResendLoading(false);
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
            <Mail className="w-8 h-8 text-primary" />
          </div>
          <h1 className="text-3xl font-bold">Verify Your Email</h1>
          <p className="text-muted-foreground mt-2">
            Enter the 6-digit code sent to your email
          </p>
        </div>

        <div className="bg-card border border-border rounded-lg p-8 animate-fade-up" style={{ animationDelay: "100ms" }}>
          <form className="space-y-4" onSubmit={handleVerify}>
            <div className="space-y-2">
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                className="bg-background"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="otp">Verification Code</Label>
              <Input
                id="otp"
                type="text"
                inputMode="numeric"
                maxLength={6}
                placeholder="123456"
                className="bg-background text-center text-lg tracking-widest"
                value={otp}
                onChange={(e) => {
                  // Only allow digits
                  const value = e.target.value.replace(/\D/g, "");
                  setOtp(value);
                }}
                disabled={loading}
              />
            </div>

            {error && (
              <div className="p-3 bg-red-500/10 border border-red-500/20 rounded text-red-500 text-sm">
                {error}
              </div>
            )}

            {success && (
              <div className="p-3 bg-green-500/10 border border-green-500/20 rounded text-green-500 text-sm">
                {success}
              </div>
            )}

            <Button
              type="submit"
              className="w-full"
              disabled={loading || otp.length !== 6}
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Verifying...
                </>
              ) : (
                "Verify Email"
              )}
            </Button>

            <div className="flex items-center justify-between pt-2">
              <Link 
                to="/auth" 
                className="text-sm text-muted-foreground hover:text-primary flex items-center"
              >
                <ArrowLeft className="w-4 h-4 mr-1" />
                Back to login
              </Link>

              <button
                type="button"
                onClick={handleResend}
                disabled={resendLoading || resendTimer > 0}
                className="text-sm text-primary hover:text-primary/80 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                {resendLoading ? (
                  <Loader2 className="w-4 h-4 mr-1 animate-spin" />
                ) : (
                  <RefreshCw className="w-4 h-4 mr-1" />
                )}
                Resend code
                {resendTimer > 0 && ` (${resendTimer}s)`}
              </button>
            </div>
          </form>

          <div className="mt-6 pt-4 border-t border-border">
            <p className="text-xs text-muted-foreground text-center">
              Didn't receive the email? Check your spam folder or click resend above.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
};

export default VerifyEmail;
