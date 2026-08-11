// LOCAL TESTING ONLY. Requires VITE_TESTING_MODE=true in .env.local (gitignored,
// never present in Vercel/production env vars) AND import.meta.env.DEV, which Vite
// hardcodes to false for any production build (`vite build`). So even if this file
// were committed and deployed, TESTING_MODE evaluates to false on the live site
// regardless of what's in someone's local .env.local.
export const TESTING_MODE =
  import.meta.env.DEV && import.meta.env.VITE_TESTING_MODE === "true";

// Defense-in-depth: independently verify at module load that this flag can
// never be active in a production build, even if the DEV check above were
// ever removed or weakened by a future edit. This check does not rely on
// TESTING_MODE itself, so it still catches misconfiguration if that
// definition changes.
if (import.meta.env.PROD && import.meta.env.VITE_TESTING_MODE === "true") {
  throw new Error(
    "VITE_TESTING_MODE must never be true in a production build. " +
    "Remove it from the deployment environment's variables."
  );
}
