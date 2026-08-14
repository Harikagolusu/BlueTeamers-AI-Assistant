import { useParams, Link, Navigate } from "react-router-dom";
import { ChevronLeft, Printer, FileText } from "lucide-react";
import Navbar from "@/components/Navbar";
import { getCourseById } from "@/data/courses";
import { getResourceContent } from "@/data/resourceContent";
import logo from "@/assets/logo.png";

// Escape HTML then apply a minimal inline markdown subset. Escaping first means
// any raw markup in content renders as literal text instead of executable DOM
// (stored-XSS). The tags we inject are generated here, so they always pass through.
const escapeHtml = (s: string) =>
  s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");

const renderInline = (s: string) =>
  escapeHtml(s)
    .replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.5 rounded bg-primary/10 text-primary text-xs font-mono">$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong class="text-foreground font-semibold">$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>');


const ResourceViewer = () => {
  const { courseId, resourceId } = useParams<{ courseId: string; resourceId: string }>();
  const course = getCourseById(courseId || "");
  const resource = getResourceContent(courseId || "", resourceId || "");
  const resourceMeta = course?.resources?.find(r => r.id === resourceId);

  if (!course || !resource || !resourceMeta) {
    return <Navigate to={`/courses/${courseId || ""}`} replace />;
  }

  const handlePrint = () => {
    window.print();
  };

  // Simple markdown-to-JSX renderer
  const renderMarkdown = (md: string) => {
    const lines = md.trim().split("\n");
    const elements: JSX.Element[] = [];
    let i = 0;
    let tableRows: string[][] = [];
    let inTable = false;
    let inCodeBlock = false;
    let codeLines: string[] = [];
    let codeLang = "";

    const flushTable = () => {
      if (tableRows.length < 2) return;
      const headers = tableRows[0];
      const dataRows = tableRows.slice(2); // skip separator row
      elements.push(
        <div key={`table-${elements.length}`} className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="border-b border-white/[0.12]">
                {headers.map((h, j) => (
                  <th key={j} className="text-left py-2 px-3 text-primary font-semibold text-xs uppercase tracking-wider">{h.trim()}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {dataRows.map((row, ri) => (
                <tr key={ri} className="border-b border-white/[0.06] hover:bg-white/[0.02]">
                  {row.map((cell, ci) => (
                    <td key={ci} className="py-2 px-3 text-foreground/80">
                      <span dangerouslySetInnerHTML={{ __html: renderInline(cell.trim()) }} />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
      tableRows = [];
      inTable = false;
    };

    while (i < lines.length) {
      const line = lines[i];

      // Code blocks
      if (line.trim().startsWith("```")) {
        if (inCodeBlock) {
          elements.push(
            <div key={`code-${elements.length}`} className="my-4 rounded-lg bg-background/80 border border-white/[0.08] overflow-hidden">
              {codeLang && <div className="px-4 py-1.5 border-b border-white/[0.06] text-[10px] text-muted-foreground uppercase tracking-wider">{codeLang}</div>}
              <pre className="p-4 overflow-x-auto text-sm font-mono text-foreground/80 leading-relaxed">
                <code>{codeLines.join("\n")}</code>
              </pre>
            </div>
          );
          inCodeBlock = false;
          codeLines = [];
          codeLang = "";
        } else {
          if (inTable) flushTable();
          inCodeBlock = true;
          codeLang = line.trim().slice(3);
        }
        i++;
        continue;
      }

      if (inCodeBlock) {
        codeLines.push(line);
        i++;
        continue;
      }

      // Tables
      if (line.includes("|") && line.trim().startsWith("|")) {
        const cells = line.split("|").filter((_, idx, arr) => idx > 0 && idx < arr.length - 1);
        if (!inTable) inTable = true;
        tableRows.push(cells);
        i++;
        continue;
      } else if (inTable) {
        flushTable();
      }

      // Headers
      if (line.startsWith("## ")) {
        elements.push(<h2 key={`h2-${i}`} className="text-xl font-bold text-foreground mt-8 mb-4 pb-2 border-b border-white/[0.08]">{line.slice(3)}</h2>);
        i++;
        continue;
      }
      if (line.startsWith("### ")) {
        elements.push(<h3 key={`h3-${i}`} className="text-lg font-semibold text-foreground mt-6 mb-3">{line.slice(4)}</h3>);
        i++;
        continue;
      }
      if (line.startsWith("#### ")) {
        elements.push(<h4 key={`h4-${i}`} className="text-base font-semibold text-foreground mt-5 mb-2">{line.slice(5)}</h4>);
        i++;
        continue;
      }

      // Horizontal rule
      if (line.trim() === "---") {
        elements.push(<hr key={`hr-${i}`} className="my-6 border-white/[0.08]" />);
        i++;
        continue;
      }

      // Checklist
      if (line.trim().startsWith("- [ ]") || line.trim().startsWith("- [x]")) {
        const checked = line.trim().startsWith("- [x]");
        const text = line.trim().slice(5).trim();
        elements.push(
          <div key={`check-${i}`} className="flex items-start gap-2 py-1 pl-2">
            <div className={`w-4 h-4 rounded border mt-0.5 flex-shrink-0 ${checked ? "bg-primary border-primary" : "border-white/20"}`} />
            <span className="text-foreground/80 text-sm" dangerouslySetInnerHTML={{ __html: renderInline(text) }} />
          </div>
        );
        i++;
        continue;
      }

      // Bullet list
      if (line.trim().startsWith("- ") || line.trim().startsWith("* ")) {
        const text = line.trim().slice(2);
        elements.push(
          <div key={`li-${i}`} className="flex items-start gap-2 py-1 pl-2">
            <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 flex-shrink-0" />
            <span className="text-foreground/80 text-sm" dangerouslySetInnerHTML={{ __html: renderInline(text) }} />
          </div>
        );
        i++;
        continue;
      }

      // Numbered list
      if (/^\d+\.\s/.test(line.trim())) {
        const match = line.trim().match(/^(\d+)\.\s(.+)/);
        if (match) {
          elements.push(
            <div key={`ol-${i}`} className="flex items-start gap-3 py-1 pl-2">
              <span className="text-primary font-semibold text-sm min-w-[1.5rem]">{match[1]}.</span>
              <span className="text-foreground/80 text-sm" dangerouslySetInnerHTML={{ __html: renderInline(match[2]) }} />
            </div>
          );
        }
        i++;
        continue;
      }

      // Empty line
      if (line.trim() === "") {
        i++;
        continue;
      }

      // Paragraph
      elements.push(
        <p key={`p-${i}`} className="text-foreground/80 text-sm leading-relaxed my-2" dangerouslySetInnerHTML={{ __html: renderInline(line) }} />
      );
      i++;
    }

    if (inTable) flushTable();

    return elements;
  };

  const typeLabel = {
    pdf: "Reference Document",
    cheatsheet: "Cheat Sheet",
    template: "Template",
    tool: "Tool Guide",
    link: "External Link",
  };

  return (
    <>
      {/* Screen version */}
      <main className="min-h-screen bg-background print:hidden">
        <Navbar />
        <div className="container mx-auto px-4 pt-20 pb-16">
          <div className="max-w-4xl mx-auto">
            {/* Breadcrumb */}
            <Link to={`/courses/${courseId}`} className="inline-flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors mb-6">
              <ChevronLeft className="w-4 h-4" />
              <span>{course.title}</span>
              <span className="text-muted-foreground/50">›</span>
              <span>Resources</span>
            </Link>

            {/* Document card */}
            <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] shadow-lg shadow-black/20">
              <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
              <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.03] via-transparent to-secondary/[0.02] pointer-events-none" />

              {/* Header */}
              <div className="relative border-b border-white/[0.08] px-8 py-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <img src={logo} alt="BlueTeamers" className="h-10 w-auto" />
                    <div>
                      <h1 className="text-xl font-bold text-foreground">{resourceMeta.title}</h1>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs bg-primary/10 text-primary border border-primary/20">
                          <FileText className="w-3 h-3" />
                          {typeLabel[resourceMeta.type] || resourceMeta.type}
                        </span>
                        <span className="text-xs text-muted-foreground">{course.shortTitle}</span>
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={handlePrint}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 transition-colors text-sm"
                  >
                    <Printer className="w-4 h-4" />
                    Print / Save PDF
                  </button>
                </div>
              </div>

              {/* Content */}
              <div className="relative px-8 py-6">
                {renderMarkdown(resource.content)}
              </div>

              {/* Footer */}
              <div className="relative border-t border-white/[0.08] px-8 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <img src={logo} alt="BlueTeamers" className="h-6 w-auto opacity-60" />
                  <span className="text-xs text-muted-foreground">BlueTeamers — {course.title}</span>
                </div>
                <span className="text-xs text-muted-foreground">© {new Date().getFullYear()} BlueTeamers. All rights reserved.</span>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Print version */}
      <div className="hidden print:block p-8">
        <div className="flex items-center justify-between mb-6 pb-4 border-b-2 border-gray-300">
          <div className="flex items-center gap-3">
            <img src={logo} alt="BlueTeamers" className="h-8 w-auto" />
            <div>
              <h1 className="text-xl font-bold text-black">{resourceMeta.title}</h1>
              <p className="text-sm text-gray-600">{course.title} — {typeLabel[resourceMeta.type] || resourceMeta.type}</p>
            </div>
          </div>
        </div>
        <div className="prose prose-sm max-w-none text-black">
          {renderMarkdown(resource.content)}
        </div>
        <div className="mt-8 pt-4 border-t border-gray-300 flex items-center justify-between">
          <span className="text-xs text-gray-500">BlueTeamers — {course.title}</span>
          <span className="text-xs text-gray-500">© {new Date().getFullYear()} BlueTeamers</span>
        </div>
      </div>
    </>
  );
};

export default ResourceViewer;
