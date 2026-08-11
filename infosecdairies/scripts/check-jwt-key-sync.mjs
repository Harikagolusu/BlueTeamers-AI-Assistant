#!/usr/bin/env node
// Fails the build if the RS256 public key hardcoded in src/lib/jwtVerify.ts
// (used for local, offline JWT signature verification in the browser) has
// drifted from infosec-backend/backend/jwt_public.pem (the key paired with
// whichever private key the backend actually signs tokens with in dev/CI).
//
// This exact drift previously caused every login to fail with
// "invalid token signature" (commit 8fbef57) because the two files are
// edited independently and nothing enforced they stay in sync.
import { createPublicKey } from "node:crypto";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const jwtVerifyPath = path.join(rootDir, "src/lib/jwtVerify.ts");
const backendPemPath = path.join(rootDir, "infosec-backend/backend/jwt_public.pem");

function fail(message) {
  console.error(`\n JWT public key sync check failed\n\n${message}\n`);
  process.exit(1);
}

const jwtVerifySource = readFileSync(jwtVerifyPath, "utf8");
const match = jwtVerifySource.match(
  /const JWT_PUBLIC_KEY_PEM = `(-----BEGIN PUBLIC KEY-----[\s\S]*?-----END PUBLIC KEY-----)`/
);
if (!match) {
  fail(`Could not find JWT_PUBLIC_KEY_PEM in ${path.relative(rootDir, jwtVerifyPath)}. Did its format change?`);
}
const frontendPem = match[1];
const backendPem = readFileSync(backendPemPath, "utf8").trim();

let frontendKey, backendKey;
try {
  frontendKey = createPublicKey({ key: frontendPem, format: "pem" });
} catch (e) {
  fail(`${path.relative(rootDir, jwtVerifyPath)} does not contain a valid PEM public key: ${e.message}`);
}
try {
  backendKey = createPublicKey({ key: backendPem, format: "pem" });
} catch (e) {
  fail(`${path.relative(rootDir, backendPemPath)} does not contain a valid PEM public key: ${e.message}`);
}

const frontendDer = frontendKey.export({ type: "spki", format: "der" });
const backendDer = backendKey.export({ type: "spki", format: "der" });

if (!frontendDer.equals(backendDer)) {
  fail(
    `${path.relative(rootDir, jwtVerifyPath)} and ${path.relative(rootDir, backendPemPath)} contain DIFFERENT keys.\n` +
      "These must always match: the frontend verifies JWTs locally using this hardcoded\n" +
      "public key, and it must be the pair of whatever private key the backend signs with.\n" +
      "A mismatch makes every login fail with 'invalid token signature'.\n\n" +
      "Fix: copy the current infosec-backend/backend/jwt_public.pem contents into the\n" +
      "JWT_PUBLIC_KEY_PEM constant in src/lib/jwtVerify.ts (or vice versa if the backend\n" +
      "key is the stale one), then re-run this check.\n\n" +
      "Note: this only checks the committed jwt_public.pem against jwtVerify.ts. If your\n" +
      "production backend (e.g. Railway) is configured with a JWT_PUBLIC_KEY /\n" +
      "JWT_PRIVATE_KEY env var pair instead of the .pem files, verify those match too —\n" +
      "this script cannot see env vars set outside the repo."
  );
}

console.log("JWT public key sync check passed: jwtVerify.ts matches jwt_public.pem.");
