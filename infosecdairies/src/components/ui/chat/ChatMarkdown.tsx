import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Components } from "react-markdown";

const markdownComponents: Components = {
  table: ({ node, ...props }) => (
    <div className="not-prose my-2 overflow-x-auto rounded-lg border border-zinc-700/60 bg-zinc-950/40">
      <table className="w-full border-collapse text-sm" {...props} />
    </div>
  ),
  thead: ({ node, ...props }) => (
    <thead className="bg-zinc-800/60" {...props} />
  ),
  th: ({ node, ...props }) => (
    <th
      className="border-b border-zinc-700 px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide text-muted-foreground"
      {...props}
    />
  ),
  td: ({ node, ...props }) => (
    <td className="border-b border-zinc-800/80 px-3 py-2 align-top" {...props} />
  ),
  tr: ({ node, ...props }) => (
    <tr className="hover:bg-zinc-800/30" {...props} />
  ),
  pre: ({ node, ...props }) => (
    <pre
      className="not-prose my-2 overflow-x-auto rounded-lg border border-zinc-700/60 bg-zinc-950/80 p-3 text-xs leading-relaxed text-zinc-100"
      {...props}
    />
  ),
  code: ({ node, className, children, ...props }) => {
    const isBlock = !!className?.includes("language-");
    if (isBlock) {
      return (
        <code className={className} {...props}>
          {children}
        </code>
      );
    }
    return (
      <code
        className="rounded bg-zinc-800 px-1.5 py-0.5 text-[0.85em] text-cyan-300"
        {...props}
      >
        {children}
      </code>
    );
  },
  blockquote: ({ node, ...props }) => (
    <blockquote
      className="my-2 border-l-2 border-primary/60 pl-3 italic text-zinc-300"
      {...props}
    />
  ),
  input: ({ node, ...props }) => (
    <input
      className="mr-1.5 inline h-3.5 w-3.5 rounded border-zinc-600 align-middle accent-cyan-400"
      {...props}
    />
  ),
};

// Streaming keeps the exact same typography colors as a completed response
// (the .bt-cyber-message prose variables: foreground text, border rules) so
// the AI answer looks identical while it streams and after it finishes. The
// wrapper is display:contents so it adds no box and cannot disturb typography
// margins/layout, and the style is dropped the moment streaming completes.
const STREAMING_COLOR_VARS: Record<string, string> = {
  "--tw-prose-body": "hsl(var(--foreground))",
  "--tw-prose-headings": "hsl(var(--foreground))",
  "--tw-prose-bold": "hsl(var(--foreground))",
  "--tw-prose-emphasis": "hsl(var(--foreground))",
  "--tw-prose-links": "hsl(var(--foreground))",
  "--tw-prose-quotes": "hsl(var(--foreground))",
  "--tw-prose-counters": "hsl(var(--foreground))",
  "--tw-prose-bullets": "hsl(var(--foreground))",
  "--tw-prose-hr": "hsl(var(--border))",
  "--tw-prose-quote-borders": "hsl(var(--border))",
};

interface ChatMarkdownProps {
  children: string;
  isStreaming?: boolean;
}

function normalizeMarkdown(s: string): string {
  if (!s) return s;
  let out = s;
  // Table fixes (only when "|" present)
  if (out.includes("|")) {
    if (out.includes("---")) {
      out = out.replace(/\|\s*\|\s*/g, "|\n|");
    } else if (out.includes("||")) {
      out = out.replace(/\|\s*\|\s*(?=-)/g, "|\n|");
    }
    out = out.replace(/([^\n])\s+(\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|)/g, (m, p1, p2) =>
      p2.includes("---") ? p1 + "\n" + p2.trimStart() : m
    );
    out = out.replace(/(\|[-:\s|]+\|)\s+(\|)/g, (m, a, b) => (a.includes("---") ? a + "\n" + b : m));
    if (out.includes("||")) {
      out = out.replace(/\|\|\s*/g, "|\n|");
    }
    out = out.replace(/([^\n])\n(\| [^\n]*\|[^\n]*\n\|[-:\s|]+\|)/g, "$1\n\n$2");
  }
  // Bullet list fixes: "here are 5 key points:- Collection" or "entry point.- Parsing" -> need newline before "- "
  if (out.includes("- ")) {
    // "analyst:- Collection" / "analyst: - Collection" -> "analyst:\n\n- Collection"
    out = out.replace(/([^\n]):\s*-\s+(?=[A-Z*•])/g, "$1:\n\n- ");
    // "entry point.- Parsing" / "entry point. - Parsing" -> "entry point.\n- Parsing"
    out = out.replace(/([^\n])\.\s*-\s+(?=[A-Z*•])/g, "$1.\n- ");
    // Generic bullet-to-bullet without newline: "Ingestion – ...- Parsing" where previous bullet ends and next starts "- "
    // Detect "point.- Parsing" already, also "point. - Parsing" and "point - Parsing" with en-dash bullet context
    // Fallback: any " - " that is bullet start after previous bullet text, ensure newline
    // Only when out looks like a list (has at least one bullet at line start or " - **")
    if (out.includes("\n- ") || out.match(/(^|\n)\s*-\s+\*\*/)) {
      // Fix remaining collapsed " - **" or " - Collection" inside same line: "entry point.- Parsing" -> already, also "– Pulls...- Parsing"
      out = out.replace(/([^\n\u2013])\s+-\s+(?=\*\*|[A-Z])/g, (m, p1) => {
        // Avoid breaking " - " inside tables or code; only when out has list markers
        if (out.includes("\n- ") && !m.includes("|")) return `${p1}\n- `;
        return m;
      });
    }
    // Ensure first bullet after intro paragraph has blank line (defense for streaming inter-token)
    out = out.replace(/([^\n:])\n(- \*\*[^\n]*)/g, "$1\n\n$2");
    // Bullet list -> paragraph after list: last bullet "tools.Real-world example:" without blank line
    // Image showed "Investigation Pivot – ...tools.Real-world example: 20 login..." inside same bullet
    if (out.includes("\n- ")) {
      out = out.replace(/([^\n])\s*(\*\*Real-world example:)/g, "$1\n\n$2");
      out = out.replace(/([^\n])\s*(From a SOC analyst's perspective:)/g, "$1\n\n$2");
      out = out.replace(/([^\n])\s*(### Continue Learning)/g, "$1\n\n$2");
      out = out.replace(/([^\n])\s*(This topic is covered in:)/g, "$1\n\n$2");
      // Generic bullet->paragraph: bullet line ending then paragraph without blank line
      out = out.replace(/(\n- [^\n]*)\n(?!\n)(?=\*\*|From a SOC|###|This topic|> \*\*)/g, "$1\n\n");
      // Fix "tools.Real-world" collapsed without space/newline: "tools.Real-world"
      out = out.replace(/([a-z0-9\.])\s*(\*\*Real-world)/g, "$1\n\n$2");
      out = out.replace(/([a-z\.])\s*(From a SOC)/g, "$1\n\n$2");
    }
  }
  out = out.replace(/\n{3,}/g, "\n\n");
  return out;
}

export function ChatMarkdown({ children, isStreaming = false }: ChatMarkdownProps) {
  const content = normalizeMarkdown(children || "");
  const markdown = (
    <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
      {content}
    </ReactMarkdown>
  );

  if (!isStreaming) return markdown;

  return (
    <div
      className="bt-streaming"
      style={STREAMING_COLOR_VARS as React.CSSProperties}
    >
      {markdown}
    </div>
  );
}

export default ChatMarkdown;
