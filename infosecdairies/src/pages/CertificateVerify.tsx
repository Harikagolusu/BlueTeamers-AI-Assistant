import { useState } from "react";
import { Link } from "react-router-dom";
import { Search, CheckCircle, XCircle, ArrowLeft, Award, Calendar, User, BookOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

interface CertificateData {
  id: string;
  recipientName: string;
  courseName: string;
  issueDate: string;
  status: "valid" | "expired" | "revoked";
}

const sampleCertificates: Record<string, CertificateData> = {
  "INFD-BSF-2026-001": {
    id: "INFD-BSF-2026-001",
    recipientName: "Ahmed Al-Rashid",
    courseName: "Blue Team & SOC Fundamentals",
    issueDate: "2026-01-15",
    status: "valid",
  },
  "INFD-SOC-2026-002": {
    id: "INFD-SOC-2026-002",
    recipientName: "Sarah Mitchell",
    courseName: "SOC Analyst Practical Course",
    issueDate: "2026-02-10",
    status: "valid",
  },
  "INFD-IR-2025-003": {
    id: "INFD-IR-2025-003",
    recipientName: "James Park",
    courseName: "Incident Response Fundamentals",
    issueDate: "2025-06-20",
    status: "expired",
  },
};

const CertificateVerify = () => {
  const [certificateId, setCertificateId] = useState("");
  const [result, setResult] = useState<CertificateData | null>(null);
  const [notFound, setNotFound] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleVerify = () => {
    const trimmed = certificateId.trim().toUpperCase();
    if (!trimmed) return;
    setSearched(true);
    const found = sampleCertificates[trimmed] || null;
    setResult(found);
    setNotFound(!found);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") handleVerify();
  };

  const statusConfig = {
    valid: { label: "Valid", icon: CheckCircle, className: "text-secondary bg-secondary/10 border-secondary/30" },
    expired: { label: "Expired", icon: XCircle, className: "text-yellow-400 bg-yellow-400/10 border-yellow-400/30" },
    revoked: { label: "Revoked", icon: XCircle, className: "text-destructive bg-destructive/10 border-destructive/30" },
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="pt-20 pb-16">
        <div className="container mx-auto px-4 max-w-2xl">
          <Link to="/" className="inline-flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors mb-8">
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>

          <div className="text-center mb-10">
            <h1 className="text-3xl md:text-4xl font-bold gradient-text mb-3">Certificate Verification</h1>
            <p className="text-muted-foreground max-w-md mx-auto">
              Enter a certificate ID to verify its authenticity and view details.
            </p>
          </div>

          {/* Search Input */}
          <Card className="bg-card/30 backdrop-blur-lg border-white/[0.08] mb-8">
            <CardContent className="p-6">
              <div className="flex gap-3">
                <Input
                  value={certificateId}
                  onChange={(e) => {
                    setCertificateId(e.target.value);
                    if (searched) { setSearched(false); setResult(null); setNotFound(false); }
                  }}
                  onKeyDown={handleKeyDown}
                  placeholder="e.g. INFD-BSF-2026-001"
                  className="bg-background/50 border-white/[0.1] text-foreground placeholder:text-muted-foreground"
                  maxLength={30}
                />
                <Button onClick={handleVerify} disabled={!certificateId.trim()} className="shrink-0 gap-2">
                  <Search className="w-4 h-4" />
                  Verify
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Result */}
          {result && (
            <Card className="bg-card/30 backdrop-blur-lg border-white/[0.08] animate-fade-in">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg font-semibold text-foreground">Certificate Details</CardTitle>
                  <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border ${statusConfig[result.status].className}`}>
                    {(() => { const Icon = statusConfig[result.status].icon; return <Icon className="w-3.5 h-3.5" />; })()}
                    {statusConfig[result.status].label}
                  </span>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-4">
                  <div className="flex items-start gap-3">
                    <Award className="w-4 h-4 text-primary mt-0.5 shrink-0" />
                    <div>
                      <p className="text-xs text-muted-foreground">Certificate ID</p>
                      <p className="text-sm font-mono text-foreground">{result.id}</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <User className="w-4 h-4 text-primary mt-0.5 shrink-0" />
                    <div>
                      <p className="text-xs text-muted-foreground">Recipient</p>
                      <p className="text-sm text-foreground">{result.recipientName}</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <BookOpen className="w-4 h-4 text-primary mt-0.5 shrink-0" />
                    <div>
                      <p className="text-xs text-muted-foreground">Course</p>
                      <p className="text-sm text-foreground">{result.courseName}</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Calendar className="w-4 h-4 text-primary mt-0.5 shrink-0" />
                    <div>
                      <p className="text-xs text-muted-foreground">Issued On</p>
                      <p className="text-sm text-foreground">{new Date(result.issueDate).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {notFound && (
            <Card className="bg-card/30 backdrop-blur-lg border-destructive/20 animate-fade-in">
              <CardContent className="p-6 text-center">
                <XCircle className="w-10 h-10 text-destructive mx-auto mb-3" />
                <h3 className="text-foreground font-semibold mb-1">Certificate Not Found</h3>
                <p className="text-sm text-muted-foreground">
                  No certificate matches the ID <span className="font-mono text-foreground">"{certificateId.trim().toUpperCase()}"</span>. Please check and try again.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default CertificateVerify;
