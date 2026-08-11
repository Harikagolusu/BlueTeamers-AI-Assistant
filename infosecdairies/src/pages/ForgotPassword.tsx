import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { ArrowLeft, Eye, EyeOff, Loader2, Mail, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/context/AuthContext";
import { apiUrl } from "@/services/api";

const ForgotPassword = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login } = useAuth();

  const [step, setStep] = useState<"request" | "confirm">("request");
  const [email, setEmail] = useState(searchParams.get("email") || "");
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [resendLoading, setResendLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [resendTimer, setResendTimer] = useState(0);

  const getResendUntilKey = (value: string) => `forgotPasswordResendUntil:${value || "_"}`;

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

  useEffect(() => {
    if (resendTimer > 0) {
      const timer = setTimeout(() => setResendTimer(resendTimer - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [resendTimer]);

  const requestReset = async () => {
    if (!email) {
      setError("Email is required.");
      return;
    }

    setError(null);
    setSuccess(null);

    try {
      setLoading(true);

      const response = await fetch(apiUrl(`/api/auth/password-reset/request/`), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        setError(data.detail || "Failed to send reset code. Please try again.");
        return;
      }

      setSuccess("If an account exists, a password reset code has been sent.");
      setStep("confirm");
      startResendCooldown(email, 60);
    } catch (e) {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const confirmReset = async () => {
    if (!email || !otp || !newPassword || !confirmPassword) {
      setError("All fields are required.");
      return;
    }

    if (otp.length !== 6) {
      setError("Please enter a 6-digit code.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setError(null);
    setSuccess(null);

    try {
      setLoading(true);

      const response = await fetch(apiUrl(`/api/auth/password-reset/confirm/`), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, code: otp, new_password: newPassword }),
      });

      const data = await response.json();

      if (!response.ok) {
        const msg = data.detail;
        if (Array.isArray(msg)) {
          setError(msg[0] || "Password reset failed.");
        } else {
          setError(msg || "Password reset failed.");
        }
        return;
      }

      const tokens = data.tokens;
      const userData = data.user || {};
      login({ email: userData.email || email, fullName: userData.full_name, tokens });

      setSuccess("Password reset successful. Redirecting...");
      setTimeout(() => navigate("/courses"), 800);
    } catch (e) {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    if (!email) {
      setError("Email is required.");
      return;
    }

    try {
      setResendLoading(true);
      setError(null);
      setSuccess(null);

      await fetch(apiUrl(`/api/auth/password-reset/request/`), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      setSuccess("If an account exists, a password reset code has been sent.");
      startResendCooldown(email, 60);
    } catch (e) {
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
          <h1 className="text-3xl font-bold">Forgot Password</h1>
          <p className="text-muted-foreground mt-2">
            {step === "request"
              ? "Enter your email to receive a reset code"
              : "Enter the code and choose a new password"}
          </p>
        </div>

        <div className="bg-card border border-border rounded-lg p-8 animate-fade-up" style={{ animationDelay: "100ms" }}>
          <form
            className="space-y-4"
            onSubmit={(e) => {
              e.preventDefault();
              if (step === "request") {
                requestReset();
              } else {
                confirmReset();
              }
            }}
          >
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
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

            {step === "confirm" && (
              <>
                <div className="space-y-2">
                  <Label htmlFor="otp">Reset Code</Label>
                  <Input
                    id="otp"
                    type="text"
                    inputMode="numeric"
                    maxLength={6}
                    placeholder="123456"
                    className="bg-background text-center text-lg tracking-widest"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))}
                    disabled={loading}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="newPassword">New Password</Label>
                  <div className="relative">
                    <Input
                      id="newPassword"
                      type={showPassword ? "text" : "password"}
                      placeholder="••••••••"
                      className="bg-background pr-10"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
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
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirm New Password</Label>
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
              </>
            )}

            {error && <p className="text-sm text-red-500">{error}</p>}
            {success && <p className="text-sm text-green-500">{success}</p>}

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  {step === "request" ? "Sending..." : "Resetting..."}
                </>
              ) : step === "request" ? (
                "Send Reset Code"
              ) : (
                "Reset Password"
              )}
            </Button>

            {step === "confirm" && (
              <div className="flex items-center justify-between pt-2">
                <button
                  type="button"
                  onClick={() => setStep("request")}
                  className="text-sm text-muted-foreground hover:text-primary transition-colors flex items-center"
                  disabled={loading}
                >
                  <ArrowLeft className="w-4 h-4 mr-1" />
                  Change email
                </button>

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
            )}

            <div className="mt-2 text-center">
              <Link to="/auth" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                Back to sign in
              </Link>
            </div>
          </form>
        </div>
      </div>
    </main>
  );
};

export default ForgotPassword;
