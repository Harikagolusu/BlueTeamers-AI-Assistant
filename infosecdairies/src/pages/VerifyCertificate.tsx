import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { CheckCircle, Award, Search, ArrowLeft } from "lucide-react";
import Navbar from "@/components/Navbar";
import { Helmet } from "react-helmet-async";
import { apiUrl } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface VerificationData {
  courseTitle: string;
  studentName: string;
  issueDate: string;
  verified: boolean;
  certId?: string;
}

export default function VerifyCertificate() {
  const { slug, emailHash, certId: urlCertId } = useParams<{ slug: string; emailHash: string; certId: string }>();
  const [data, setData] = useState<VerificationData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [inputCertId, setInputCertId] = useState(urlCertId || "");
  const [hasSearched, setHasSearched] = useState(false);

  useEffect(() => {
    if (urlCertId) {
      setInputCertId(urlCertId);
      handleVerify(urlCertId);
    } else if (slug && emailHash) {
      handleLegacyVerify();
    }
  }, [urlCertId, slug, emailHash]);

  const handleVerify = async (certIdToVerify: string) => {
    if (!certIdToVerify) return;
    setLoading(true);
    setError(null);
    setHasSearched(true);
    try {
      const response = await fetch(apiUrl(`/api/certificates/lookup/${certIdToVerify}/`));
      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          setData({
            courseTitle: result.courseName,
            studentName: result.studentName,
            issueDate: result.issueDate,
            verified: result.verified,
            certId: result.certId
          });
        } else {
          setError(result.error || "Certificate not found");
          setData(null);
        }
      } else {
        setError("Certificate not found or invalid");
        setData(null);
      }
    } catch (err) {
      setError("Failed to verify certificate");
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLegacyVerify = async () => {
    if (!slug || !emailHash) return;
    setLoading(true);
    setError(null);
    setHasSearched(true);
    try {
      const response = await fetch(apiUrl(`/api/certificates/verify/${slug}/${emailHash}`));
      if (response.ok) {
        const verificationData = await response.json();
        setData(verificationData);
      } else {
        setError("Certificate not found");
        setData(null);
      }
    } catch (err) {
      setError("Failed to verify certificate");
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchAgain = () => {
    setData(null);
    setError(null);
    setHasSearched(false);
    setInputCertId("");
  };

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleVerify(inputCertId);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950">
      <Helmet>
        <title>Verify Certificate</title>
      </Helmet>
      <Navbar />
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto">
          <div className="bg-gradient-to-br from-blue-500/10 to-purple-500/10 backdrop-blur-xl rounded-2xl border border-white/10 p-8">
            <div className="text-center mb-8">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <Search className="w-10 h-10 text-blue-500" />
              </div>
              <h1 className="text-3xl font-bold text-white mb-2">Verify Certificate</h1>
              <p className="text-gray-400">Enter a certificate ID to verify its authenticity</p>
            </div>

            {!data && (
              <form onSubmit={onSubmit} className="space-y-6 mb-8">
                <div className="flex gap-2">
                  <Input
                    type="text"
                    placeholder="Enter Certificate ID (e.g., INFOD-SOC-2025-001)"
                    value={inputCertId}
                    onChange={(e) => setInputCertId(e.target.value)}
                    className="flex-1 bg-white/5 border-white/10 text-white placeholder:text-gray-500"
                    disabled={loading}
                  />
                  <Button
                    type="submit"
                    disabled={!inputCertId || loading}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {loading ? (
                      <span className="animate-spin mr-2">⏳</span>
                    ) : (
                      <Search className="w-4 h-4 mr-2" />
                    )}
                    Verify
                  </Button>
                </div>
                <p className="text-sm text-gray-500 text-center">
                  Example: INFOD-SOC-2025-001
                </p>
              </form>
            )}

            {loading && (
              <div className="text-center py-8">
                <div className="animate-spin w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
                <p className="text-gray-400">Verifying certificate...</p>
              </div>
            )}

            {error && hasSearched && !loading && (
              <div className="text-center py-8">
                <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-red-500 text-2xl">✕</span>
                </div>
                <h2 className="text-xl font-bold text-white mb-2">Certificate Not Found</h2>
                <p className="text-gray-400 mb-6">{error}</p>
                <Button
                  onClick={handleSearchAgain}
                  variant="outline"
                  className="border-white/20 text-white hover:bg-white/10"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Search Again
                </Button>
              </div>
            )}

            {data && !loading && (
              <div className="space-y-6">
                <div className="text-center">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <CheckCircle className="w-10 h-10 text-green-500" />
                  </div>
                  <h2 className="text-2xl font-bold text-white mb-1">Certificate Verified</h2>
                  <p className="text-gray-400">This certificate is authentic and valid</p>
                </div>

                <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                  <div className="flex items-center gap-4 mb-4">
                    <Award className="w-6 h-6 text-blue-400" />
                    <h3 className="text-xl font-semibold text-white">Certificate Details</h3>
                  </div>
                  
                  <div className="space-y-4">
                    {data.certId && (
                      <div className="flex items-center justify-between py-2 border-b border-white/5">
                        <span className="text-gray-400">Certificate ID</span>
                        <span className="text-white font-medium font-mono">{data.certId}</span>
                      </div>
                    )}
                    <div className="flex items-center justify-between py-2 border-b border-white/5">
                      <span className="text-gray-400">Course</span>
                      <span className="text-white font-medium">{data.courseTitle}</span>
                    </div>
                    <div className="flex items-center justify-between py-2 border-b border-white/5">
                      <span className="text-gray-400">Student</span>
                      <span className="text-white font-medium">{data.studentName}</span>
                    </div>
                    <div className="flex items-center justify-between py-2 border-b border-white/5">
                      <span className="text-gray-400">Issue Date</span>
                      <span className="text-white font-medium">{data.issueDate}</span>
                    </div>
                    <div className="flex items-center justify-between py-2">
                      <span className="text-gray-400">Status</span>
                      <span className="flex items-center gap-2 text-green-400 font-medium">
                        <CheckCircle className="w-4 h-4" />
                        Verified
                      </span>
                    </div>
                  </div>
                </div>

                <div className="text-center">
                  <Button
                    onClick={handleSearchAgain}
                    variant="outline"
                    className="border-white/20 text-white hover:bg-white/10"
                  >
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Verify Another Certificate
                  </Button>
                </div>

                <p className="text-sm text-gray-500 text-center">
                  This certificate was issued by BlueTeamers upon successful completion of the course.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
