import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Components } from "react-markdown";

const markdownComponents: Components = {
  table: ({ node, ...props }) => (
    <div className="not-prose my-3 overflow-x-auto rounded-lg border border-zinc-700/60 bg-zinc-950/40">
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
      className="not-prose my-3 overflow-x-auto rounded-lg border border-zinc-700/60 bg-zinc-950/80 p-3 text-xs leading-relaxed text-zinc-100"
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
      className="my-3 border-l-2 border-primary/60 pl-3 italic text-zinc-300"
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

export function ChatMarkdown({ children, isStreaming = false }: ChatMarkdownProps) {
  const content = children || "";
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
