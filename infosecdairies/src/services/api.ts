const RAW_API_BASE = import.meta.env.VITE_API_BASE_URL;
const API_BASE = (RAW_API_BASE || "").replace(/\/$/, "");

export function apiUrl(path: string) {
  if (!path.startsWith("/")) {
    path = `/${path}`;
  }

  // No base URL set: use relative paths so Vite proxy (dev) and Vercel rewrites (prod) handle routing.
  if (!RAW_API_BASE && path.startsWith("/api/")) {
    return path;
  }

  return `${API_BASE}${path}`;
}

export async function fetchCourses() {
  const res = await fetch(apiUrl(`/api/courses/`));
  if (!res.ok) {
    throw new Error("Failed to fetch courses");
  }
  const data = await res.json();

  // Support both paginated (with `results`) and plain list responses
  return Array.isArray(data) ? data : data.results;
}

export async function fetchCourseBySlug(slug: string) {
  const res = await fetch(apiUrl(`/api/courses/${slug}/`));
  if (!res.ok) {
    throw new Error("Course not found");
  }
  return res.json();
}
