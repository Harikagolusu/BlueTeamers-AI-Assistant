import Navbar from "@/components/Navbar";
import SOCSidebar from "@/components/soc/SOCSidebar";
import { Bell, User, Search, Mail, Shield, ShieldAlert, ShieldCheck, ShieldX, Paperclip, ExternalLink, Clock, Filter, Eye, AlertTriangle, XCircle, MailWarning } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";

type EmailVerdict = "Clean" | "Suspicious" | "Malicious" | "Quarantined";

interface EmailEntry {
  id: string;
  from: string;
  to: string;
  subject: string;
  date: string;
  time: string;
  direction: "Inbound" | "Outbound";
  verdict: EmailVerdict;
  hasAttachment: boolean;
  attachmentName?: string;
  spfResult: "Pass" | "Fail" | "None";
  dkimResult: "Pass" | "Fail" | "None";
  dmarcResult: "Pass" | "Fail" | "None";
  senderIP: string;
  threatType?: string;
  body?: string;
}

const emailData: EmailEntry[] = [
  {
    id: "EM-001", from: "hr-department@company-update[.]xyz", to: "john.smith@corp.local", subject: "Urgent: Verify Your Account Credentials",
    date: "Feb 19, 2026", time: "09:14 AM", direction: "Inbound", verdict: "Malicious", hasAttachment: true, attachmentName: "verify_account.html",
    spfResult: "Fail", dkimResult: "Fail", dmarcResult: "Fail", senderIP: "185.220.101.34",
    threatType: "Credential Phishing",
    body: "Dear Employee,\n\nYour corporate account has been flagged for suspicious activity. Please verify your credentials immediately by opening the attached file.\n\nFailure to verify within 24 hours will result in account suspension.\n\nRegards,\nHR Department",
  },
  {
    id: "EM-002", from: "noreply@microsoft.com", to: "lisa.johnson@corp.local", subject: "Your Microsoft 365 Subscription Renewal",
    date: "Feb 19, 2026", time: "08:47 AM", direction: "Inbound", verdict: "Clean", hasAttachment: false,
    spfResult: "Pass", dkimResult: "Pass", dmarcResult: "Pass", senderIP: "40.107.22.131",
    body: "Hello Lisa,\n\nYour Microsoft 365 Business subscription has been renewed successfully. Your next billing date is March 19, 2026.\n\nThank you,\nMicrosoft Team",
  },
  {
    id: "EM-003", from: "invoices@quickbooks-billing[.]net", to: "accounting@corp.local", subject: "Invoice #INV-2026-0847 - Payment Due",
    date: "Feb 19, 2026", time: "08:32 AM", direction: "Inbound", verdict: "Suspicious", hasAttachment: true, attachmentName: "Invoice_2026_0847.pdf",
    spfResult: "None", dkimResult: "Fail", dmarcResult: "None", senderIP: "91.234.99.117",
    threatType: "Potential BEC / Invoice Fraud",
    body: "Please find attached the invoice for services rendered. Payment is due within 3 business days.\n\nNote: We have updated our bank details. Please use the new account information on the invoice.\n\nBest,\nAccounting Team",
  },
  {
    id: "EM-004", from: "admin@corp.local", to: "all-staff@corp.local", subject: "System Maintenance Window - Feb 20",
    date: "Feb 19, 2026", time: "08:15 AM", direction: "Outbound", verdict: "Clean", hasAttachment: false,
    spfResult: "Pass", dkimResult: "Pass", dmarcResult: "Pass", senderIP: "10.0.0.5",
    body: "Team,\n\nPlease note there will be a scheduled maintenance window on February 20, 2026 from 2:00 AM to 6:00 AM EST.\n\nDuring this time, email and VPN services may be intermittently unavailable.\n\nIT Operations",
  },
  {
    id: "EM-005", from: "security-alert@bank0famerica[.]com", to: "mike.chen@corp.local", subject: "Unusual Login Activity Detected",
    date: "Feb 18, 2026", time: "11:58 PM", direction: "Inbound", verdict: "Malicious", hasAttachment: true, attachmentName: "security_report.exe",
    spfResult: "Fail", dkimResult: "Fail", dmarcResult: "Fail", senderIP: "172.16.88.200",
    threatType: "Malware Delivery",
    body: "Dear Customer,\n\nWe detected unusual login activity on your account. Please review the attached security report immediately.\n\nClick here to verify your identity.\n\nBank of America Security Team",
  },
  {
    id: "EM-006", from: "sarah.williams@corp.local", to: "external-partner@vendor.com", subject: "Q1 Project Deliverables Update",
    date: "Feb 18, 2026", time: "04:30 PM", direction: "Outbound", verdict: "Clean", hasAttachment: true, attachmentName: "Q1_deliverables.xlsx",
    spfResult: "Pass", dkimResult: "Pass", dmarcResult: "Pass", senderIP: "10.0.0.42",
    body: "Hi Team,\n\nPlease find attached the updated Q1 deliverables spreadsheet. Let me know if you have any questions.\n\nBest regards,\nSarah",
  },
  {
    id: "EM-007", from: "support@dropbox-share[.]info", to: "alex.taylor@corp.local", subject: "Someone shared a file with you",
    date: "Feb 18, 2026", time: "03:22 PM", direction: "Inbound", verdict: "Quarantined", hasAttachment: false,
    spfResult: "Fail", dkimResult: "None", dmarcResult: "Fail", senderIP: "195.22.127.93",
    threatType: "Phishing Link",
    body: "Alex Taylor,\n\nJohn from your organization has shared a document with you. Click below to access it:\n\n[View Document]\n\nThis link will expire in 24 hours.\n\nDropbox Team",
  },
  {
    id: "EM-008", from: "newsletter@techcrunch.com", to: "dev-team@corp.local", subject: "TechCrunch Daily: AI Breakthroughs This Week",
    date: "Feb 18, 2026", time: "02:00 PM", direction: "Inbound", verdict: "Clean", hasAttachment: false,
    spfResult: "Pass", dkimResult: "Pass", dmarcResult: "Pass", senderIP: "198.51.100.23",
    body: "Today's top stories:\n\n1. New AI model achieves breakthrough in code generation\n2. Cloud security market expected to reach $80B by 2027\n3. Zero-trust architecture adoption surges\n\nRead more at techcrunch.com",
  },
  {
    id: "EM-009", from: "ceo@corp-executive[.]org", to: "finance@corp.local", subject: "Wire Transfer Request - Confidential",
    date: "Feb 18, 2026", time: "01:15 PM", direction: "Inbound", verdict: "Quarantined", hasAttachment: false,
    spfResult: "Fail", dkimResult: "Fail", dmarcResult: "Fail", senderIP: "103.235.46.19",
    threatType: "Business Email Compromise",
    body: "Hi Finance Team,\n\nI need you to process an urgent wire transfer of $47,500 to the following account. This is time-sensitive and confidential.\n\nBank: First National\nAccount: 8274910384\nRouting: 021000021\n\nPlease confirm once done.\n\nRegards,\nCEO",
  },
  {
    id: "EM-010", from: "it-helpdesk@corp.local", to: "new-hire@corp.local", subject: "Welcome! Your IT Onboarding Checklist",
    date: "Feb 18, 2026", time: "10:00 AM", direction: "Outbound", verdict: "Clean", hasAttachment: true, attachmentName: "onboarding_checklist.pdf",
    spfResult: "Pass", dkimResult: "Pass", dmarcResult: "Pass", senderIP: "10.0.0.5",
    body: "Welcome to the team!\n\nPlease find attached your IT onboarding checklist. Complete all items within your first week.\n\nContact IT Helpdesk if you need assistance.\n\nBest,\nIT Support",
  },
];

const verdictConfig: Record<EmailVerdict, { icon: typeof Shield; color: string; bg: string; border: string }> = {
  Clean: { icon: ShieldCheck, color: "text-emerald-400", bg: "bg-emerald-500/15", border: "border-emerald-500/25" },
  Suspicious: { icon: ShieldAlert, color: "text-yellow-400", bg: "bg-yellow-500/15", border: "border-yellow-500/25" },
  Malicious: { icon: ShieldX, color: "text-destructive", bg: "bg-destructive/15", border: "border-destructive/25" },
  Quarantined: { icon: AlertTriangle, color: "text-orange-400", bg: "bg-orange-500/15", border: "border-orange-500/25" },
};

const authBadge = (result: string) => {
  switch (result) {
    case "Pass": return <span className="text-[9px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Pass</span>;
    case "Fail": return <span className="text-[9px] px-1.5 py-0.5 rounded bg-destructive/10 text-destructive border border-destructive/20">Fail</span>;
    default: return <span className="text-[9px] px-1.5 py-0.5 rounded bg-muted/20 text-muted-foreground border border-white/[0.06]">None</span>;
  }
};

const EmailSecurity = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [verdictFilter, setVerdictFilter] = useState<EmailVerdict | "All">("All");
  const [selectedEmail, setSelectedEmail] = useState<EmailEntry | null>(null);

  const filtered = emailData.filter((e) => {
    const matchesSearch =
      e.from.toLowerCase().includes(searchQuery.toLowerCase()) ||
      e.to.toLowerCase().includes(searchQuery.toLowerCase()) ||
      e.subject.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesVerdict = verdictFilter === "All" || e.verdict === verdictFilter;
    return matchesSearch && matchesVerdict;
  });

  const stats = {
    total: emailData.length,
    clean: emailData.filter((e) => e.verdict === "Clean").length,
    suspicious: emailData.filter((e) => e.verdict === "Suspicious").length,
    malicious: emailData.filter((e) => e.verdict === "Malicious").length,
    quarantined: emailData.filter((e) => e.verdict === "Quarantined").length,
  };

  return (
    <main className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <SOCSidebar activeItem="Email Security" />
        <div className="flex-1 flex flex-col min-w-0">
          <header className="bg-card/25 backdrop-blur-lg border-b border-white/[0.08] px-6 py-4 flex items-center justify-between">
            <div>
              <h1 className="text-xl font-semibold text-foreground">Email Security</h1>
              <p className="text-sm text-muted-foreground">Email gateway monitoring and threat analysis</p>
            </div>
            <div className="flex items-center gap-3">
              <div className="relative hidden md:block">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input type="text" placeholder="Search emails..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="bg-background/50 border border-white/[0.08] rounded-lg pl-10 pr-4 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/25 w-64 transition-colors backdrop-blur-sm" />
              </div>
              <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors rounded-lg hover:bg-white/[0.04]"><Bell className="w-5 h-5" /><span className="absolute top-1 right-1 w-2 h-2 bg-destructive rounded-full" /></button>
              <button className="w-8 h-8 bg-primary/10 border border-primary/25 rounded-full flex items-center justify-center text-primary hover:bg-primary/20 transition-colors"><User className="w-4 h-4" /></button>
            </div>
          </header>

          <div className="flex-1 p-6 overflow-auto">
            <div className="space-y-6">
              {/* Summary Cards */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {[
                  { label: "Total Emails", count: stats.total, icon: Mail, color: "text-foreground" },
                  { label: "Clean", count: stats.clean, icon: ShieldCheck, color: "text-emerald-400" },
                  { label: "Suspicious", count: stats.suspicious, icon: ShieldAlert, color: "text-yellow-400" },
                  { label: "Malicious", count: stats.malicious, icon: ShieldX, color: "text-destructive" },
                  { label: "Quarantined", count: stats.quarantined, icon: AlertTriangle, color: "text-orange-400" },
                ].map((s) => (
                  <div key={s.label} className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-4 shadow-lg shadow-black/20 cursor-pointer hover:bg-card/35 hover:border-white/[0.12] transition-all" onClick={() => setVerdictFilter(s.label === "Total Emails" ? "All" : s.label as EmailVerdict)}>
                    <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                    <div className="flex items-center justify-between mb-2">
                      <p className="text-xs text-muted-foreground uppercase tracking-wide">{s.label}</p>
                      <s.icon className={cn("w-4 h-4", s.color)} />
                    </div>
                    <span className={cn("text-2xl font-bold", s.color)}>{s.count}</span>
                  </div>
                ))}
              </div>

              {/* Filter Pills */}
              <div className="flex items-center gap-2">
                <Filter className="w-4 h-4 text-muted-foreground" />
                {(["All", "Clean", "Suspicious", "Malicious", "Quarantined"] as const).map((v) => (
                  <button key={v} onClick={() => setVerdictFilter(v)} className={cn("px-3 py-1.5 rounded-lg text-xs font-medium transition-all", verdictFilter === v ? "bg-primary/15 text-primary border border-primary/25" : "text-muted-foreground hover:text-foreground hover:bg-white/[0.04] border border-transparent")}>
                    {v}
                  </button>
                ))}
              </div>

              {/* Email List + Detail Split */}
              <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                <div className={cn("relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] shadow-lg shadow-black/20", selectedEmail ? "lg:col-span-3" : "lg:col-span-5")}>
                  <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-white/[0.06]">
                          <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Verdict</th>
                          <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">From</th>
                          <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">To</th>
                          <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Subject</th>
                          <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Date</th>
                          <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3 text-center">Att.</th>
                        </tr>
                      </thead>
                      <tbody>
                        {filtered.map((email) => {
                          const vc = verdictConfig[email.verdict];
                          const VIcon = vc.icon;
                          return (
                            <tr key={email.id} onClick={() => setSelectedEmail(email)} className={cn("border-b border-white/[0.03] last:border-b-0 hover:bg-white/[0.03] transition-colors cursor-pointer group", selectedEmail?.id === email.id && "bg-primary/5 border-l-2 border-l-primary")}>
                              <td className="px-4 py-3">
                                <span className={cn("inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-full border font-medium", vc.bg, vc.color, vc.border)}>
                                  <VIcon className="w-3 h-3" />
                                  {email.verdict}
                                </span>
                              </td>
                              <td className="px-4 py-3"><span className="text-xs text-foreground font-mono truncate max-w-[180px] block">{email.from}</span></td>
                              <td className="px-4 py-3"><span className="text-xs text-muted-foreground font-mono truncate max-w-[140px] block">{email.to}</span></td>
                              <td className="px-4 py-3"><span className="text-xs text-foreground group-hover:text-primary transition-colors truncate max-w-[220px] block">{email.subject}</span></td>
                              <td className="px-4 py-3 whitespace-nowrap">
                                <span className="text-[10px] text-muted-foreground flex items-center gap-1"><Clock className="w-3 h-3" />{email.time}</span>
                                <span className="text-[9px] text-muted-foreground/60">{email.date}</span>
                              </td>
                              <td className="px-4 py-3 text-center">{email.hasAttachment && <Paperclip className="w-3.5 h-3.5 text-muted-foreground mx-auto" />}</td>
                            </tr>
                          );
                        })}
                        {filtered.length === 0 && (
                          <tr><td colSpan={6} className="px-4 py-12 text-center text-sm text-muted-foreground">No emails match your filters</td></tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Detail Panel */}
                {selectedEmail && (
                  <div className="lg:col-span-2 relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] shadow-lg shadow-black/20">
                    <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                    <div className="p-5 space-y-5 overflow-auto max-h-[calc(100vh-300px)]">
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <h3 className="text-sm font-semibold text-foreground mb-1 break-words">{selectedEmail.subject}</h3>
                          <p className="text-[10px] text-muted-foreground">{selectedEmail.id} · {selectedEmail.date} {selectedEmail.time}</p>
                        </div>
                        <button onClick={() => setSelectedEmail(null)} className="p-1 text-muted-foreground hover:text-foreground transition-colors">
                          <XCircle className="w-4 h-4" />
                        </button>
                      </div>

                      {(() => {
                        const vc = verdictConfig[selectedEmail.verdict];
                        const VIcon = vc.icon;
                        return (
                          <div className={cn("flex items-center gap-2 px-3 py-2 rounded-lg border", vc.bg, vc.border)}>
                            <VIcon className={cn("w-5 h-5", vc.color)} />
                            <div>
                              <p className={cn("text-sm font-semibold", vc.color)}>{selectedEmail.verdict}</p>
                              {selectedEmail.threatType && <p className="text-[10px] text-muted-foreground">{selectedEmail.threatType}</p>}
                            </div>
                          </div>
                        );
                      })()}

                      <div className="space-y-2">
                        <div>
                          <p className="text-[10px] text-muted-foreground uppercase tracking-wide mb-1">From</p>
                          <p className="text-xs text-foreground font-mono break-all">{selectedEmail.from}</p>
                          <p className="text-[10px] text-muted-foreground/60 mt-0.5">IP: {selectedEmail.senderIP}</p>
                        </div>
                        <div>
                          <p className="text-[10px] text-muted-foreground uppercase tracking-wide mb-1">To</p>
                          <p className="text-xs text-foreground font-mono break-all">{selectedEmail.to}</p>
                        </div>
                      </div>

                      <div>
                        <p className="text-[10px] text-muted-foreground uppercase tracking-wide mb-2">Email Authentication</p>
                        <div className="flex gap-4">
                          <div className="text-center"><p className="text-[9px] text-muted-foreground mb-1">SPF</p>{authBadge(selectedEmail.spfResult)}</div>
                          <div className="text-center"><p className="text-[9px] text-muted-foreground mb-1">DKIM</p>{authBadge(selectedEmail.dkimResult)}</div>
                          <div className="text-center"><p className="text-[9px] text-muted-foreground mb-1">DMARC</p>{authBadge(selectedEmail.dmarcResult)}</div>
                        </div>
                      </div>

                      {selectedEmail.hasAttachment && (
                        <div>
                          <p className="text-[10px] text-muted-foreground uppercase tracking-wide mb-2">Attachment</p>
                          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-background/50 border border-white/[0.06]">
                            <Paperclip className="w-3.5 h-3.5 text-muted-foreground" />
                            <span className="text-xs text-foreground font-mono">{selectedEmail.attachmentName}</span>
                            {(selectedEmail.verdict === "Malicious" || selectedEmail.verdict === "Quarantined") && (
                              <span className="text-[9px] px-1.5 py-0.5 rounded bg-destructive/10 text-destructive border border-destructive/20 ml-auto">Blocked</span>
                            )}
                          </div>
                        </div>
                      )}

                      {selectedEmail.body && (
                        <div>
                          <p className="text-[10px] text-muted-foreground uppercase tracking-wide mb-2">Email Body</p>
                          <div className="px-3 py-3 rounded-lg bg-background/50 border border-white/[0.06]">
                            <pre className="text-xs text-foreground/80 whitespace-pre-wrap font-sans leading-relaxed">{selectedEmail.body}</pre>
                          </div>
                        </div>
                      )}

                      <div className="flex gap-2 pt-2">
                        <button className="flex-1 px-3 py-2 rounded-lg text-xs font-medium bg-primary/10 text-primary border border-primary/25 hover:bg-primary/20 transition-colors flex items-center justify-center gap-1.5">
                          <Eye className="w-3.5 h-3.5" /> Investigate
                        </button>
                        {selectedEmail.verdict !== "Clean" && (
                          <button className="flex-1 px-3 py-2 rounded-lg text-xs font-medium bg-destructive/10 text-destructive border border-destructive/25 hover:bg-destructive/20 transition-colors flex items-center justify-center gap-1.5">
                            <ShieldX className="w-3.5 h-3.5" /> Block Sender
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default EmailSecurity;
