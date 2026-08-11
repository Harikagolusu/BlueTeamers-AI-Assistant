import React, { useEffect, useState } from "react";

type ConsentLevel = "all" | "essential" | "none";

const STORAGE_KEY = "cookie_consent";

function getStored(): ConsentLevel | null {
  return localStorage.getItem(STORAGE_KEY) as ConsentLevel | null;
}

const CookieConsent: React.FC = () => {
  const [visible, setVisible] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    if (!getStored()) setVisible(true);
  }, []);

  const accept = (level: ConsentLevel) => {
    localStorage.setItem(STORAGE_KEY, level);
    setVisible(false);
  };

  if (!visible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 p-4 md:p-6">
      <div className="max-w-4xl mx-auto bg-gray-900 border border-gray-700 rounded-xl shadow-2xl p-5 md:p-6">
        <div className="flex items-start gap-3 mb-4">
          <span className="text-2xl mt-0.5">🍪</span>
          <div className="flex-1">
            <p className="text-white font-semibold text-sm md:text-base mb-1">
              We use cookies & local storage
            </p>
            <p className="text-gray-400 text-xs md:text-sm leading-relaxed">
              We use essential storage to keep you logged in and remember your progress.
              Analytics cookies help us improve the platform.{" "}
              <button
                onClick={() => setShowDetails((v) => !v)}
                className="text-blue-400 hover:text-blue-300 underline"
              >
                {showDetails ? "Hide details" : "Learn more"}
              </button>
            </p>

            {showDetails && (
              <div className="mt-3 space-y-2 text-xs text-gray-400 border-t border-gray-700 pt-3">
                <div className="flex gap-2">
                  <span className="text-green-400 font-bold shrink-0">✓ Essential</span>
                  <span>Auth tokens, session data, course progress — always active, required for login to work.</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-blue-400 font-bold shrink-0">~ Analytics</span>
                  <span>Anonymous usage data to help us improve courses and platform experience.</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-gray-500 font-bold shrink-0">✗ Marketing</span>
                  <span>We do not use advertising or marketing cookies.</span>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-2 justify-end">
          <button
            onClick={() => accept("none")}
            className="px-4 py-2 text-xs sm:text-sm text-gray-400 border border-gray-600 rounded-lg hover:border-gray-400 hover:text-gray-200 transition-colors"
          >
            Essential only
          </button>
          <button
            onClick={() => accept("essential")}
            className="px-4 py-2 text-xs sm:text-sm text-gray-300 border border-gray-500 rounded-lg hover:border-gray-300 hover:text-white transition-colors"
          >
            Accept limited
          </button>
          <button
            onClick={() => accept("all")}
            className="px-4 py-2 text-xs sm:text-sm font-semibold text-white bg-blue-600 hover:bg-blue-500 rounded-lg transition-colors"
          >
            Accept all
          </button>
        </div>
      </div>
    </div>
  );
};

export default CookieConsent;

/** Returns the current consent level, or null if not yet set. */
export function getCookieConsent(): ConsentLevel | null {
  return getStored();
}
