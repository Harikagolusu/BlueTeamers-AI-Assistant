import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { apiUrl } from "@/services/api";

interface CurrencyPrices {
  easy: number;
  medium: number;
  hard: number;
  bundle: number;
}

interface CurrencyState {
  countryCode: string;
  currency: string;
  symbol: string;
  prices: CurrencyPrices;
  loading: boolean;
}

const DEFAULT_STATE: CurrencyState = {
  countryCode: "IN",
  currency: "INR",
  symbol: "₹",
  prices: { easy: 499, medium: 799, hard: 1199, bundle: 3999 },
  loading: true,
};

const CurrencyContext = createContext<CurrencyState>(DEFAULT_STATE);

const SESSION_KEY = "geo_currency_v2";
const CACHE_TTL_MS = 6 * 60 * 60 * 1000; // 6 hours

async function detectCountry(): Promise<string> {
  try {
    const res = await fetch("https://ipapi.co/json/", { signal: AbortSignal.timeout(4000) });
    if (!res.ok) return "IN";
    const data = await res.json();
    return (data.country_code as string) || "IN";
  } catch {
    return "IN";
  }
}

export function CurrencyProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<CurrencyState>(DEFAULT_STATE);

  useEffect(() => {
    const cached = sessionStorage.getItem(SESSION_KEY);
    if (cached) {
      try {
        const parsed = JSON.parse(cached) as CurrencyState & { cachedAt?: number };
        const age = Date.now() - (parsed.cachedAt ?? 0);
        if (age < CACHE_TTL_MS) {
          setState({ ...parsed, loading: false });
          return;
        }
      } catch {
        // fall through to fetch
      }
    }

    (async () => {
      const countryCode = await detectCountry();
      try {
        const res = await fetch(apiUrl(`/api/payments/pricing/?country=${countryCode}`));
        if (!res.ok) throw new Error("pricing fetch failed");
        const data = await res.json();
        const next: CurrencyState = {
          countryCode: data.country_code,
          currency: data.currency,
          symbol: data.symbol,
          prices: data.prices,
          loading: false,
        };
        setState(next);
        sessionStorage.setItem(SESSION_KEY, JSON.stringify({ ...next, cachedAt: Date.now() }));
      } catch {
        setState({ ...DEFAULT_STATE, countryCode, loading: false });
      }
    })();
  }, []);

  return <CurrencyContext.Provider value={state}>{children}</CurrencyContext.Provider>;
}

export function useCurrency() {
  return useContext(CurrencyContext);
}
