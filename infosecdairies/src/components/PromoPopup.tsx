import { useEffect, useState } from "react";
import { X, Copy, Check } from "lucide-react";
import { useNavigate } from "react-router-dom";

const PROMO_CODE = "INFOSEC10";
const DELAY_MS = 1500;

const PromoPopup = () => {
  const [visible, setVisible] = useState(false);
  const [entered, setEntered] = useState(false);
  const [leaving, setLeaving] = useState(false);
  const [copied, setCopied] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const t = setTimeout(() => {
      setVisible(true);
      // Trigger enter animation on next paint
      requestAnimationFrame(() => requestAnimationFrame(() => setEntered(true)));
    }, DELAY_MS);
    return () => clearTimeout(t);
  }, []);

  const dismiss = () => {
    setLeaving(true);
    setEntered(false);
    setTimeout(() => {
      setVisible(false);
      setLeaving(false);
    }, 350);
  };

  const copy = async () => {
    await navigator.clipboard.writeText(PROMO_CODE);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const claim = () => {
    dismiss();
    setTimeout(() => navigate("/courses"), 350);
  };

  if (!visible) return null;

  const overlayStyle: React.CSSProperties = {
    opacity: entered && !leaving ? 1 : 0,
    transition: "opacity 350ms ease",
  };

  const cardStyle: React.CSSProperties = {
    opacity: entered && !leaving ? 1 : 0,
    transform: entered && !leaving ? "scale(1) translateY(0)" : "scale(0.88) translateY(24px)",
    transition: "opacity 350ms cubic-bezier(0.34,1.56,0.64,1), transform 350ms cubic-bezier(0.34,1.56,0.64,1)",
    background: "hsl(220 40% 6%)",
    border: "1px solid hsl(186 100% 42% / 0.5)",
    boxShadow:
      "0 0 40px hsl(186 100% 42% / 0.2), 0 0 80px hsl(186 100% 42% / 0.08), 0 25px 60px rgba(0,0,0,0.6)",
  };

  return (
    <div
      className="fixed inset-0 z-[60] flex items-center justify-center p-4"
      style={overlayStyle}
      onClick={dismiss}
    >
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" />

      {/* Card */}
      <div
        className="relative z-10 w-full max-w-md rounded-2xl overflow-hidden"
        style={cardStyle}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Hex bg pattern */}
        <div
          className="absolute inset-0 opacity-5 pointer-events-none"
          style={{
            backgroundImage:
              "url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTYiIGhlaWdodD0iMTAwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0yOCAwTDAgMjVWNzVMMjggMTAwTDU2IDc1VjI1WiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDBmZmM4IiBzdHJva2Utd2lkdGg9IjEiLz48L3N2Zz4=')",
            backgroundSize: "56px 100px",
          }}
        />

        {/* Scanline */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: "linear-gradient(transparent 50%, rgba(0,255,200,0.025) 50%)",
            backgroundSize: "100% 4px",
          }}
        />

        {/* Top gradient bar */}
        <div
          className="h-1 w-full"
          style={{
            background:
              "linear-gradient(90deg, hsl(186 100% 42%), hsl(84 81% 44%), hsl(186 100% 42%))",
            backgroundSize: "200% auto",
            animation: "gradient-shift 3s linear infinite",
          }}
        />

        {/* Close */}
        <button
          onClick={dismiss}
          className="absolute top-4 right-4 z-20 p-1.5 rounded-lg text-muted-foreground hover:text-white hover:bg-white/10 transition-colors"
          aria-label="Close"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="relative p-8 text-center space-y-6">
          {/* Badge only — no shield icon */}
          <div className="flex justify-center">
            <span
              className="text-xs font-bold tracking-widest uppercase px-3 py-1 rounded-full"
              style={{
                background: "hsl(84 81% 44% / 0.15)",
                border: "1px solid hsl(84 81% 44% / 0.4)",
                color: "hsl(84 81% 44%)",
              }}
            >
              Limited Time Offer
            </span>
          </div>

          {/* Headline */}
          <div className="space-y-2">
            <p className="text-sm text-muted-foreground uppercase tracking-widest font-medium">
              Exclusive Discount
            </p>
            <h2
              className="text-5xl font-extrabold gradient-text"
              style={{ backgroundSize: "200% auto", animation: "gradient-shift 3s linear infinite" }}
            >
              50% OFF
            </h2>
            <p className="text-base text-foreground/80 leading-relaxed">
              Get 50% off on{" "}
              <span className="text-white font-semibold">any course</span> or the{" "}
              <span className="text-white font-semibold">All Courses Bundle</span>
            </p>
          </div>

          {/* Promo code pill */}
          <div className="space-y-2">
            <p className="text-xs text-muted-foreground">Use code at checkout</p>
            <button
              onClick={copy}
              className="w-full flex items-center justify-between px-5 py-3 rounded-xl transition-all duration-200 hover:brightness-110"
              style={{
                background: "hsl(220 35% 10%)",
                border: "1px dashed hsl(186 100% 42% / 0.6)",
              }}
            >
              <span
                className="text-xl font-mono font-bold tracking-widest"
                style={{ color: "hsl(186 100% 42%)" }}
              >
                {PROMO_CODE}
              </span>
              <span
                className="flex items-center gap-1.5 text-xs font-medium transition-colors"
                style={{ color: copied ? "hsl(84 81% 44%)" : "hsl(186 100% 42%)" }}
              >
                {copied ? (
                  <><Check className="w-3.5 h-3.5" /> Copied!</>
                ) : (
                  <><Copy className="w-3.5 h-3.5" /> Copy</>
                )}
              </span>
            </button>
          </div>

          {/* CTA */}
          <button
            onClick={claim}
            className="w-full py-3.5 rounded-xl font-bold text-sm tracking-wide transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
            style={{
              background: "linear-gradient(135deg, hsl(186 100% 42%), hsl(84 81% 44%))",
              color: "hsl(220 40% 6%)",
              boxShadow: "0 4px 20px hsl(186 100% 42% / 0.35)",
            }}
          >
            Claim Discount → Explore Courses
          </button>

          <p className="text-xs text-muted-foreground">
            One-time use per account &nbsp;·&nbsp; All courses included
          </p>
        </div>
      </div>
    </div>
  );
};

export default PromoPopup;
