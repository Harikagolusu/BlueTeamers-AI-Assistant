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

// Matrix-green accent applied (via prose CSS custom properties) ONLY while the
// response is actively streaming. The wrapper is display:contents so it adds
// no box and cannot disturb typography margins/layout, and the style is
// dropped the moment streaming completes so completed messages stay untouched.
const STREAMING_COLOR_VARS: Record<string, string> = {
  "--tw-prose-body": "hsl(152 100% 55%)",
  "--tw-prose-headings": "hsl(152 100% 64%)",
  "--tw-prose-bold": "hsl(152 100% 64%)",
  "--tw-prose-emphasis": "hsl(152 100% 52%)",
  "--tw-prose-links": "hsl(152 100% 58%)",
  "--tw-prose-quotes": "hsl(152 100% 56%)",
  "--tw-prose-counters": "hsl(152 100% 50%)",
  "--tw-prose-bullets": "hsl(152 100% 50%)",
  "--tw-prose-hr": "hsl(152 60% 38%)",
  "--tw-prose-quote-borders": "hsl(152 60% 38%)",
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
      style={
        {
          ...STREAMING_COLOR_VARS,
          textShadow: "0 0 14px hsla(152 100% 60% / 0.3)",
        } as React.CSSProperties
      }
    >
      {markdown}
    </div>
  );
}

export default ChatMarkdown;
