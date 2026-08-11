import { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { Loader2, ArrowLeft, CreditCard } from "lucide-react";
import Navbar from "@/components/Navbar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/context/AuthContext";
import { useCurrency } from "@/context/CurrencyContext";
import { ALL_COURSES_BUNDLE_SLUG, getCourseBySlug } from "@/data/courses";
import { apiUrl } from "@/services/api";

declare global {
  interface Window {
    Razorpay: any;
  }
}

const CourseCheckout = () => {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const { countryCode, symbol, prices, loading: currencyLoading } = useCurrency();
  const [course, setCourse] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [name, setName] = useState(user?.fullName || user?.email?.split("@")[0] || "");
  const [error, setError] = useState<string | null>(null);
  const [displayAmount, setDisplayAmount] = useState<number | null>(null);
  const [originalAmount, setOriginalAmount] = useState<number | null>(null);
  const [discountPercent, setDiscountPercent] = useState<number>(0);
  const [promoCode, setPromoCode] = useState("");
  const [promoApplied, setPromoApplied] = useState(false);
  const [promoError, setPromoError] = useState<string | null>(null);
  const [cachedOrder, setCachedOrder] = useState<any | null>(null);
  const [applyingPromo, setApplyingPromo] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const promoParam = params.get("promo");
    if (promoParam) {
      setPromoCode(promoParam.toUpperCase());
    }
  }, [location.search]);

  useEffect(() => {
    if (!slug || currencyLoading) return;

    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      navigate(`/auth?redirect=${encodeURIComponent(`/courses/${slug}/checkout${location.search}`)}`);
      return;
    }

    // Check if already enrolled — if so, send them straight to the course
    if (slug !== ALL_COURSES_BUNDLE_SLUG) {
      fetch(apiUrl(`/api/courses/${slug}/enrollment/`), {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
        .then((r) => r.json())
        .then((data) => {
          if (data.status === "enrolled") navigate(`/courses/${slug}`, { replace: true });
        })
        .catch(() => {});
    }

    if (slug === ALL_COURSES_BUNDLE_SLUG) {
      setCourse({ title: "All Courses Bundle", difficulty: "easy" });
      setDisplayAmount(prices.bundle);
      setOriginalAmount(prices.bundle);
      setLoading(false);
      return;
    }

    const staticCourse = getCourseBySlug(slug);
    if (staticCourse) {
      const price =
        staticCourse.difficulty === "easy" ? prices.easy
        : staticCourse.difficulty === "medium" ? prices.medium
        : prices.hard;
      setCourse(staticCourse);
      setDisplayAmount(price);
      setOriginalAmount(price);
    }
    setLoading(false);
  }, [slug, currencyLoading, prices]);

  const loadRazorpayScript = () => {
    return new Promise<boolean>((resolve) => {
      if (window.Razorpay) {
        resolve(true);
        return;
      }
      const script = document.createElement("script");
      script.src = "https://checkout.razorpay.com/v1/checkout.js";
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  };

  const applyPromoCode = async () => {
    setPromoError(null);
    setError(null);
    const trimmedCode = promoCode.trim().toUpperCase();
    if (!trimmedCode) return;

    if (!slug || !course) {
      setPromoError("Course not loaded yet, please wait.");
      return;
    }
    if (!name.trim()) {
      setPromoError("Please enter your full name first.");
      return;
    }

    let accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      navigate(`/auth?redirect=${encodeURIComponent(`/courses/${slug}/checkout`)}`);
      return;
    }

    const createOrder = async (token: string) =>
      fetch(apiUrl("/api/payments/create-order/"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          course_slug: slug,
          full_name: name.trim(),
          promo_code: trimmedCode,
          country_code: countryCode,
        }),
      });

    try {
      setApplyingPromo(true);
      let res = await createOrder(accessToken);

      if (res.status === 401 || res.status === 403) {
        const newAccess = await refreshAccessToken();
        if (!newAccess) {
          handleAuthFailure();
          return;
        }
        accessToken = newAccess;
        res = await createOrder(accessToken);
      }

      const data = await parseResponse(res);
      if (!res.ok) {
        const rawDetail = data?.detail;
        const detail =
          typeof rawDetail === "string" && rawDetail.trim().startsWith("<!doctype")
            ? `API error: ${res.status} ${res.statusText} (server returned HTML - check backend URL/deploy)`
            : rawDetail || `Error: ${res.status} ${res.statusText}`;
        setPromoError(detail);
        setPromoApplied(false);
        setCachedOrder(null);
        setDiscountPercent(0);
        setDisplayAmount(originalAmount);
        return;
      }

      setPromoCode(trimmedCode);
      setPromoApplied(true);
      setDiscountPercent(typeof data.discount_percent === "number" ? data.discount_percent : (data.free ? 100 : 0));
      if (data.free) {
        // Enrollment already created by backend; show 0 so user can click "Get Free Access".
        setDisplayAmount(0);
        setCachedOrder(null);
      } else {
        const displayAmt = typeof data.amount_display === "number" ? data.amount_display : data.amount_inr;
        if (typeof displayAmt === "number") {
          setDisplayAmount(displayAmt);
        }
        setCachedOrder(data);
      }
    } catch (err: any) {
      setPromoError(err?.message || "Failed to apply promo code");
      setPromoApplied(false);
      setCachedOrder(null);
      setDiscountPercent(0);
      setDisplayAmount(originalAmount);
    } finally {
      setApplyingPromo(false);
    }
  };

  const removePromoCode = () => {
    setPromoApplied(false);
    setPromoCode("");
    setPromoError(null);
    setDiscountPercent(0);
    setCachedOrder(null);
    // Reset to original price
    setDisplayAmount(originalAmount);
  };

  useEffect(() => {
    // If user changes inputs after applying promo, force a recalculation.
    if (!promoApplied) return;
    setCachedOrder(null);
  }, [name, slug, promoApplied]);

  const refreshAccessToken = async (): Promise<string | null> => {
    const refreshToken = localStorage.getItem("refreshToken");
    if (!refreshToken) return null;
    const res = await fetch(apiUrl("/api/auth/token/refresh/"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });
    if (!res.ok) return null;
    const data = await res.json();
    if (!data?.access) return null;
    localStorage.setItem("accessToken", data.access);
    if (data.refresh) {
      localStorage.setItem("refreshToken", data.refresh);
    }
    return data.access as string;
  };

  const handleAuthFailure = () => {
    logout();
    navigate(`/auth?redirect=${encodeURIComponent(`/courses/${slug}/checkout`)}`);
  };

  const parseResponse = async (res: Response): Promise<any> => {
    const contentType = res.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      return await res.json();
    }
    const text = await res.text();
    return { detail: text };
  };

  const handlePay = async () => {
    if (!slug || !course) return;
    if (!name.trim()) {
      setError("Please enter your name");
      return;
    }

    // Free promo already enrolled the user at apply-time — navigate directly.
    if (promoApplied && displayAmount === 0) {
      if (slug === ALL_COURSES_BUNDLE_SLUG) {
        navigate("/courses");
      } else {
        navigate(`/courses/${slug}`);
      }
      return;
    }

    setSubmitting(true);
    setError(null);

    let accessToken = localStorage.getItem("accessToken");
    if (!accessToken) {
      navigate(`/auth?redirect=${encodeURIComponent(`/courses/${slug}/checkout`)}`);
      setSubmitting(false);
      return;
    }

    try {
      // 1) Create order
      const createOrder = async (token: string) =>
        fetch(apiUrl("/api/payments/create-order/"), {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            course_slug: slug,
            full_name: name.trim(),
            promo_code: promoApplied ? promoCode.trim().toUpperCase() : undefined,
            country_code: countryCode,
          }),
        });

      let data: any = null;
      let res: Response | null = null;

      if (promoApplied && cachedOrder && promoCode.trim()) {
        data = cachedOrder;
      } else {
        res = await createOrder(accessToken);

        if (res.status === 401 || res.status === 403) {
          const newAccess = await refreshAccessToken();
          if (!newAccess) {
            handleAuthFailure();
            setSubmitting(false);
            return;
          }
          accessToken = newAccess;
          res = await createOrder(accessToken);
        }

        data = await parseResponse(res);
      }

      if (res && !res.ok) {
        const rawDetail = data?.detail;
        const detail =
          typeof rawDetail === "string" && rawDetail.trim().startsWith("<!doctype")
            ? `API error: ${res.status} ${res.statusText} (server returned HTML - check backend URL/deploy)`
            : rawDetail || `Error: ${res.status} ${res.statusText}`;
        if ((detail as string).toLowerCase().includes("token") || (detail as string).toLowerCase().includes("credential")) {
          setError(detail);
          handleAuthFailure();
        } else if ((detail as string).toLowerCase().includes("promo")) {
          // Only show in the promo section, not as a duplicate top-level error.
          setPromoError(detail);
          setPromoApplied(false);
          setDiscountPercent(0);
          setDisplayAmount(originalAmount);
        } else {
          setError(detail);
        }
        setSubmitting(false);
        return;
      }

      const displayAmt = typeof data.amount_display === "number" ? data.amount_display : data.amount_inr;
      if (typeof displayAmt === "number") {
        setDisplayAmount(displayAmt);
        if (data.discount_percent) {
          setDiscountPercent(data.discount_percent);
        }
      }

      if (data.free) {
        if (slug === ALL_COURSES_BUNDLE_SLUG) {
          navigate("/courses");
        } else {
          navigate(`/courses/${slug}`);
        }
        setSubmitting(false);
        return;
      }

      // Test mode: skip Razorpay and auto-verify
      if (data.test_mode) {
        const verify = async (token: string) =>
          fetch(apiUrl("/api/payments/verify/"), {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              razorpay_order_id: data.order_id,
              razorpay_payment_id: "generic_payment_id",
              razorpay_signature: "generic_signature",
            }),
          });

        let verifyRes = await verify(accessToken);
        if (verifyRes.status === 401 || verifyRes.status === 403) {
          const newAccess = await refreshAccessToken();
          if (!newAccess) {
            handleAuthFailure();
            setSubmitting(false);
            return;
          }
          accessToken = newAccess;
          verifyRes = await verify(accessToken);
        }

        const verifyData = await parseResponse(verifyRes);
        if (!verifyRes.ok) {
          const rawDetail = verifyData?.detail;
          const detail =
            typeof rawDetail === "string" && rawDetail.trim().startsWith("<!doctype")
              ? `API error: ${verifyRes.status} ${verifyRes.statusText} (server returned HTML - check backend URL/deploy)`
              : rawDetail || "Payment verification failed";
          setError(detail);
          setSubmitting(false);
          return;
        }

        if (slug === ALL_COURSES_BUNDLE_SLUG) {
          navigate("/courses");
        } else {
          navigate(`/courses/${slug}`);
        }
        setSubmitting(false);
        return;
      }

      // 2) Load Razorpay script
      const scriptLoaded = await loadRazorpayScript();
      if (!scriptLoaded) {
        setError("Failed to load payment gateway");
        setSubmitting(false);
        return;
      }

      // 3) Open Razorpay Checkout
      const options = {
        key: data.key_id,
        amount: data.amount,
        currency: data.currency,
        name: course.title,
        description: "Enrollment payment",
        order_id: data.order_id,
        handler: async (response: any) => {
          const verify = async (token: string) =>
            fetch(apiUrl("/api/payments/verify/"), {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature,
              }),
            });

          let verifyRes = await verify(accessToken as string);
          if (verifyRes.status === 401 || verifyRes.status === 403) {
            const newAccess = await refreshAccessToken();
            if (!newAccess) {
              handleAuthFailure();
              setSubmitting(false);
              return;
            }
            accessToken = newAccess;
            verifyRes = await verify(accessToken);
          }

          const verifyData = await parseResponse(verifyRes);
          if (!verifyRes.ok) {
            const rawDetail = verifyData?.detail;
            const detail =
              typeof rawDetail === "string" && rawDetail.trim().startsWith("<!doctype")
                ? `API error: ${verifyRes.status} ${verifyRes.statusText} (server returned HTML - check backend URL/deploy)`
                : rawDetail || "Payment verification failed";
            setError(detail);
            setSubmitting(false);
            return;
          }

          if (slug === ALL_COURSES_BUNDLE_SLUG) {
            navigate("/courses");
          } else {
            navigate(`/courses/${slug}`);
          }
        },
        prefill: {
          email: user?.email,
          name: name.trim(),
        },
        theme: {
          color: "#334155",
        },
        modal: {
          ondismiss: () => {
            setSubmitting(false);
          },
        },
      };

      const rzp = new window.Razorpay(options);
      rzp.open();
    } catch (err: any) {
      console.error("Payment error:", err);
      setError(err?.message || "Something went wrong. Please try again.");
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-background">
        <Navbar />
        <div className="pt-20 pb-16 px-4 md:px-8 max-w-7xl mx-auto flex items-center justify-center">
          <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
        </div>
      </main>
    );
  }

  if (!course) {
    return (
      <main className="min-h-screen bg-background">
        <Navbar />
        <div className="pt-20 pb-16 px-4 md:px-8 max-w-7xl mx-auto text-center">
          <h1 className="text-2xl font-bold mb-4">Course not found</h1>
          <Button onClick={() => navigate("/courses")}>Browse Courses</Button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-background">
      <Navbar />
      <div className="pt-20 pb-16 px-4 md:px-8 max-w-7xl mx-auto">
        <div className="mb-6">
          <Button variant="ghost" onClick={() => navigate(`/courses/${slug}`)} className="mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to course
          </Button>
          <h1 className="text-3xl font-bold">{course.title}</h1>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CreditCard className="w-5 h-5" />
                Checkout
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">Email (registered)</label>
                <Input value={user?.email || ""} disabled />
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Full name</label>
                <Input
                  placeholder="Enter your full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>

              {/* Promo Code Section */}
              <div className="pt-2 border-t border-border">
                <label className="text-sm font-medium text-muted-foreground">Promo Code</label>
                <div className="flex gap-2 mt-1">
                  <Input
                    placeholder="Enter promo code"
                    value={promoCode}
                    onChange={(e) => setPromoCode(e.target.value)}
                    disabled={promoApplied}
                    className="flex-1"
                  />
                  {!promoApplied ? (
                    <Button
                      type="button"
                      variant="outline"
                      onClick={applyPromoCode}
                      disabled={!promoCode.trim() || applyingPromo}
                    >
                      {applyingPromo ? "Applying..." : "Apply"}
                    </Button>
                  ) : (
                    <Button
                      type="button"
                      variant="ghost"
                      onClick={removePromoCode}
                      className="text-red-500 hover:text-red-600"
                    >
                      Remove
                    </Button>
                  )}
                </div>
                {promoError && <p className="text-sm text-red-500 mt-1">{promoError}</p>}
                {promoApplied && (
                  <p className="text-sm text-green-500 mt-1">Promo code applied.</p>
                )}
              </div>

              {error && <p className="text-sm text-red-500">{error}</p>}
              <Button
                onClick={handlePay}
                disabled={submitting}
                className="w-full"
                size="lg"
              >
                {submitting ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Processing...
                  </>
                ) : promoApplied && displayAmount === 0 ? (
                  "Get Free Access"
                ) : (
                  `Pay ${typeof displayAmount === "number" ? `${symbol}${displayAmount}` : ""}`
                )}
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Order Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between">
                <span>Course</span>
                <span className="font-medium">{course.title}</span>
              </div>
              <div className="flex justify-between">
                <span>Price</span>
                <span className="font-medium line-through text-muted-foreground">
                  {symbol}{originalAmount || 0}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Discounted Price</span>
                <span className="font-medium text-green-600">
                  {typeof displayAmount === "number" ? `${symbol}${displayAmount}` : "-"}
                </span>
              </div>
              {promoApplied && originalAmount && displayAmount !== originalAmount && (
                <div className="flex justify-between text-green-600 text-sm">
                  <span>You save ({discountPercent || 50}% off)</span>
                  <span className="font-medium">-{symbol}{((originalAmount ?? 0) - (displayAmount ?? 0)).toFixed(2)}</span>
                </div>
              )}
              <div className="flex justify-between border-t pt-2 mt-2">
                <span className="font-bold">Total</span>
                <span className="font-bold text-lg">
                  {typeof displayAmount === "number" ? `${symbol}${displayAmount}` : "-"}
                </span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
};

export default CourseCheckout;
