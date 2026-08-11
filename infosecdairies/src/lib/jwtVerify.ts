// RSA-2048 public key — safe to ship in the browser bundle (it's public).
// The server signs every JWT with the matching private key (RS256).
// Verification here is 100% local: no HTTP call, no response to intercept.
// An attacker CANNOT forge a token that passes this check without the private key.
const JWT_PUBLIC_KEY_PEM = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0gmE1vPCsGBMiqZlrr1B
c2bRurrBVyQB+oYnTBLssrRPbeIkwX6Vte9lRd7F99di3yKczfY6iY5iumfv08Yf
NvCQeZt10rjNstnlXAoX7BvqOJFJqWPQYPSsg/gr7smUk5QkfolJq1fp2iZDkZCI
oc+Fzg5H03nZ3XpTtDhK/A1PExMvEhUUbFZgwm8cuV/GDWhdDuRitz1h0HR7IKf1
uYyUtwWSgNbcJhK+NXhhdI6pnJPsHcZavnIFG7Q6hhQcawrPL01E+iC0nw5Z7WOb
GPgQzIKiJQuYcgoDzKoHxFG209X+SGv/QFfGhIjzouzwg0Cfk4eiic5qJRr15tze
nQIDAQAB
-----END PUBLIC KEY-----`;

let _cachedKey: CryptoKey | null = null;

async function getPublicKey(): Promise<CryptoKey> {
  if (_cachedKey) return _cachedKey;

  // Strip PEM header/footer and decode base64
  const pem = JWT_PUBLIC_KEY_PEM.replace(/-----BEGIN PUBLIC KEY-----/, "")
    .replace(/-----END PUBLIC KEY-----/, "")
    .replace(/\s+/g, "");

  const der = Uint8Array.from(atob(pem), (c) => c.charCodeAt(0));

  _cachedKey = await crypto.subtle.importKey(
    "spki",
    der.buffer,
    { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
    false,
    ["verify"]
  );
  return _cachedKey;
}

export interface VerifiedJwtPayload {
  email?: string;
  user_id?: number;
  exp?: number;
  [key: string]: unknown;
}

function decodeB64Url(b64url: string): string {
  const b64 = b64url.replace(/-/g, "+").replace(/_/g, "/");
  const padded = b64 + "=".repeat((4 - (b64.length % 4)) % 4);
  return atob(padded);
}

/**
 * Verify a JWT and return its payload. Throws if the token is expired or tampered.
 *
 * Only RS256 is accepted. Full cryptographic signature verification using the embedded
 * public key — an attacker cannot forge these without the server's private key.
 * Any other algorithm (HS256, none, etc.) is rejected outright to prevent algorithm
 * confusion attacks where an attacker forges a token with an arbitrary payload.
 */
export async function verifyJwtLocally(token: string): Promise<VerifiedJwtPayload> {
  const parts = token.split(".");
  if (parts.length !== 3) throw new Error("Malformed token");

  const [headerB64, payloadB64, signatureB64] = parts;

  // Decode header to read the algorithm
  const header = JSON.parse(decodeB64Url(headerB64)) as { alg?: string };

  // Decode payload
  const payload: VerifiedJwtPayload = JSON.parse(decodeB64Url(payloadB64));

  // Always check expiry
  if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) {
    throw new Error("Token expired");
  }

  // Only RS256 is accepted. Allowing HS256/none lets an attacker forge a token with
  // any payload (we can't verify HMAC without the server secret), bypass the local
  // check, and access all static lesson/quiz content without a paid account.
  if (header.alg !== "RS256") {
    throw new Error(`Unsupported token algorithm: ${header.alg}. Only RS256 is accepted.`);
  }

  const signatureBytes = Uint8Array.from(
    decodeB64Url(signatureB64),
    (c) => c.charCodeAt(0)
  );
  const signedData = new TextEncoder().encode(`${headerB64}.${payloadB64}`);
  const publicKey = await getPublicKey();
  const valid = await crypto.subtle.verify(
    "RSASSA-PKCS1-v1_5",
    publicKey,
    signatureBytes,
    signedData
  );
  if (!valid) throw new Error("Invalid token signature");

  return payload;
}
