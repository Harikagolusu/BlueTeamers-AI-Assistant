import { useParams, useNavigate } from "react-router-dom";
import { Clock, Users, Calendar, ChevronRight, CheckCircle2, BookOpen, Target, GraduationCap, Send, Loader2 } from "lucide-react";
import { useState, useEffect } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { getLiveCourseById } from "@/data/liveCourses";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/context/AuthContext";
import { apiUrl } from "@/services/api";

const LiveCourseDetail = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  const { user, isAuthenticated } = useAuth();
  const course = getLiveCourseById(courseId || "");

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    message: ""
  });
  const [phoneError, setPhoneError] = useState("");
  const [autofilled, setAutofilled] = useState(false);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isAuthenticated && user) {
      setFormData(prev => ({
        ...prev,
        name: user.fullName || user.email || "",
        email: user.email || "",
      }));
      setAutofilled(true);
    }
  }, [isAuthenticated, user]);

  if (!course) {
    navigate("/courses");
    return null;
  }

  const sanitizeText = (val: string) =>
    val.replace(/[<>"'`]/g, "").slice(0, 2000);

  const PHONE_RE = /^[+\d][\d\s\-(). ]{5,19}$/;

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const raw = e.target.value.replace(/[^+\d\s\-().]/g, "").slice(0, 20);
    setFormData({ ...formData, phone: raw });
    setPhoneError(raw && !PHONE_RE.test(raw) ? "Enter a valid phone number." : "");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (phoneError) return;
    setLoading(true);

    try {
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
      };
      const token = localStorage.getItem("accessToken");
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch(apiUrl("/api/leads/create/"), {
        method: "POST",
        headers,
        body: JSON.stringify({
          course_name: sanitizeText(course.title),
          name: sanitizeText(formData.name),
          email: formData.email,
          phone: formData.phone,
          message: sanitizeText(formData.message),
          country: "",
          city: ""
        }),
      });

      if (response.ok) {
        toast({
          title: "Inquiry Submitted!",
          description: "We'll contact you shortly to discuss enrollment.",
        });
        setFormData(prev => ({ ...prev, phone: "", message: "" }));
      } else {
        const data = await response.json();
        toast({
          title: "Submission Failed",
          description: data.detail || "Please check your details and try again.",
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Network Error",
        description: "Please check your connection and try again.",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-background">
      <Navbar />

      {/* Hero Section */}
      <section className="relative pt-20 pb-16 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-background to-secondary/10" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/5 via-transparent to-transparent" />
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 text-primary mb-6">
              <Calendar className="w-4 h-4" />
              <span className="text-sm font-medium">Live Training Program</span>
            </div>
            
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 bg-gradient-to-r from-foreground via-primary to-secondary bg-clip-text text-transparent">
              {course.title}
            </h1>
            
            <p className="text-xl md:text-2xl text-primary/80 font-medium mb-6">
              {course.tagline}
            </p>
            
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto mb-8">
              {course.description}
            </p>

            {/* Course Meta */}
            <div className="flex flex-wrap justify-center gap-4 md:gap-8">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Clock className="w-5 h-5 text-primary" />
                <span>{course.duration}</span>
              </div>
              <div className="flex items-center gap-2 text-muted-foreground">
                <Users className="w-5 h-5 text-primary" />
                <span>{course.batchSize}</span>
              </div>
              <div className="flex items-center gap-2 text-muted-foreground">
                <Calendar className="w-5 h-5 text-primary" />
                <span>{course.format}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Price Banner */}
      <section className="py-6 bg-gradient-to-r from-primary/20 via-primary/10 to-secondary/20 border-y border-primary/20">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-8">
            <div className="text-center md:text-left">
              <p className="text-sm text-muted-foreground uppercase tracking-wider">Course Fee</p>
              <p className="text-3xl md:text-4xl font-bold text-primary">{course.fee}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
            
            {/* Left Column - Course Details */}
            <div className="lg:col-span-2 space-y-12">
              
              {/* What You'll Learn */}
              <div className="bg-card/30 backdrop-blur-lg rounded-2xl border border-border p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 rounded-lg bg-primary/10">
                    <Target className="w-6 h-6 text-primary" />
                  </div>
                  <h2 className="text-2xl font-bold">What You'll Learn</h2>
                </div>
                <div className="grid md:grid-cols-2 gap-4">
                  {course.whatYouWillLearn.map((item, index) => (
                    <div key={index} className="flex items-start gap-3">
                      <CheckCircle2 className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
                      <span className="text-muted-foreground">{item}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Who Is It For */}
              <div className="bg-card/30 backdrop-blur-lg rounded-2xl border border-border p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 rounded-lg bg-secondary/10">
                    <Users className="w-6 h-6 text-secondary" />
                  </div>
                  <h2 className="text-2xl font-bold">Who Is This For?</h2>
                </div>
                <div className="space-y-3">
                  {course.whoIsItFor.map((item, index) => (
                    <div key={index} className="flex items-center gap-3 p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors">
                      <ChevronRight className="w-4 h-4 text-secondary" />
                      <span className="text-muted-foreground">{item}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Course Roadmap */}
              <div className="bg-card/30 backdrop-blur-lg rounded-2xl border border-border p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 rounded-lg bg-primary/10">
                    <BookOpen className="w-6 h-6 text-primary" />
                  </div>
                  <h2 className="text-2xl font-bold">Complete Roadmap</h2>
                </div>
                <div className="space-y-6">
                  {course.roadmap.map((module, index) => (
                    <div 
                      key={index} 
                      className="relative pl-8 pb-6 border-l-2 border-primary/30 last:border-l-0 last:pb-0"
                    >
                      {/* Timeline dot */}
                      <div className="absolute left-0 top-0 w-4 h-4 -translate-x-1/2 rounded-full bg-primary shadow-lg shadow-primary/50" />
                      
                      <div className="bg-muted/20 rounded-xl p-5 hover:bg-muted/30 transition-colors">
                        <div className="flex items-center gap-3 mb-3">
                          <span className="px-3 py-1 text-xs font-bold rounded-full bg-primary/10 text-primary">
                            Week {module.week}
                          </span>
                          <h3 className="text-lg font-semibold">{module.title}</h3>
                        </div>
                        <ul className="space-y-2 ml-4">
                          {module.topics.map((topic, topicIndex) => (
                            <li key={topicIndex} className="flex items-start gap-2 text-sm text-muted-foreground">
                              <span className="text-primary mt-1">•</span>
                              {topic}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Prerequisites */}
              <div className="bg-card/30 backdrop-blur-lg rounded-2xl border border-border p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 rounded-lg bg-amber-500/10">
                    <GraduationCap className="w-6 h-6 text-amber-500" />
                  </div>
                  <h2 className="text-2xl font-bold">Prerequisites</h2>
                </div>
                <div className="grid md:grid-cols-2 gap-4">
                  {course.prerequisites.map((item, index) => (
                    <div key={index} className="flex items-start gap-3 p-3 rounded-lg bg-amber-500/5 border border-amber-500/10">
                      <CheckCircle2 className="w-5 h-5 text-amber-500 mt-0.5 flex-shrink-0" />
                      <span className="text-muted-foreground">{item}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Certification */}
              <div className="bg-gradient-to-r from-primary/10 to-secondary/10 rounded-2xl border border-primary/20 p-8">
                <div className="flex items-center gap-3 mb-4">
                  <GraduationCap className="w-8 h-8 text-primary" />
                  <h2 className="text-2xl font-bold">Certification</h2>
                </div>
                <p className="text-muted-foreground">{course.certificationDetails}</p>
              </div>
            </div>

            {/* Right Column - Contact Form */}
            <div className="lg:col-span-1">
              <div className="sticky top-24 bg-card/50 backdrop-blur-lg rounded-2xl border border-border p-6">
                <h3 className="text-xl font-bold mb-2">Enroll Now</h3>
                <p className="text-sm text-muted-foreground mb-6">
                  Fill the form below for enrollment details.
                </p>

                {autofilled && (
                  <div className="mb-4 px-3 py-2 rounded-lg bg-primary/10 border border-primary/20 text-xs text-primary">
                    Details pre-filled from your account
                  </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="text-sm font-medium mb-1.5 block">Full Name</label>
                    <Input
                      placeholder="Enter your name"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-1.5 block">Email</label>
                    <Input
                      type="email"
                      placeholder="Enter your email"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-1.5 block">Phone Number</label>
                    <Input
                      type="tel"
                      placeholder="e.g. +91 98765 43210"
                      value={formData.phone}
                      onChange={handlePhoneChange}
                      maxLength={20}
                      required
                    />
                    {phoneError && (
                      <p className="text-xs text-destructive mt-1">{phoneError}</p>
                    )}
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-1.5 block">Message (Optional)</label>
                    <Textarea
                      placeholder="Any questions or specific requirements?"
                      value={formData.message}
                      onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                      rows={3}
                    />
                  </div>
                  <Button type="submit" className="w-full gap-2" disabled={loading}>
                    {loading ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Send className="w-4 h-4" />
                    )}
                    {loading ? "Submitting..." : "Submit Inquiry"}
                  </Button>
                </form>

                <div className="mt-6 p-4 rounded-lg bg-muted/30">
                  <h4 className="font-semibold mb-2">Course Fee</h4>
                  <p className="text-3xl font-bold text-primary mb-1">{course.fee}</p>
                  <p className="text-xs text-muted-foreground">One-time payment • Lifetime access to recordings</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
};

export default LiveCourseDetail;
