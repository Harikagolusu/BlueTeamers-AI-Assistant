import { useMemo, useState, useEffect } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import CourseCard from "@/components/CourseCard";
import { ALL_COURSES_BUNDLE_SLUG, FREE_COURSE_SLUG, getCourseCardData } from "@/data/courses";
import { getLiveCourseCardData } from "@/data/liveCourses";
import { useAuth } from "@/context/AuthContext";
import { useNavigate } from "react-router-dom";
import { apiUrl } from "@/services/api";
import { useCurrency } from "@/context/CurrencyContext";

const Courses = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { prices, symbol } = useCurrency();
  const [activeTab, setActiveTab] = useState<"self-paced" | "live">("self-paced");
  const [hasBundle, setHasBundle] = useState(false);
  const [bundlePromo, setBundlePromo] = useState("");
  
  useEffect(() => {
    const checkBundlePurchase = async () => {
      const accessToken = localStorage.getItem("accessToken");
      if (!accessToken || !user) {
        setHasBundle(false);
        return;
      }
      
      try {
        const res = await fetch(apiUrl("/api/payments/my-purchases/"), {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        
        if (res.ok) {
          const purchases = await res.json();
          const bundlePurchased = purchases.some(
            (p: any) => p.course_slug === ALL_COURSES_BUNDLE_SLUG && p.status === "paid"
          );
          setHasBundle(bundlePurchased);
        }
      } catch {
        setHasBundle(false);
      }
    };
    
    checkBundlePurchase();
  }, [user]);
  
  const selfPacedCourses = useMemo(() => {
    const courses = getCourseCardData();
    const difficultyRank: Record<string, number> = { easy: 0, medium: 1, hard: 2 };
    const priorityOrder = [
      "network-fundamentals",
      "soc-fundamentals",
      "log-analysis",
      "siem-fundamentals",
      "incident-response",
      "soc-analyst-path",
      "network-security-monitoring",
    ];
    const priorityIndex = new Map(priorityOrder.map((id, idx) => [id, idx] as const));

    return [...courses].sort((a, b) => {
      const aPriority = priorityIndex.get(a.courseId);
      const bPriority = priorityIndex.get(b.courseId);
      if (aPriority != null && bPriority != null) return aPriority - bPriority;
      if (aPriority != null) return -1;
      if (bPriority != null) return 1;

      const aRank = difficultyRank[a.difficulty ?? ""] ?? 99;
      const bRank = difficultyRank[b.difficulty ?? ""] ?? 99;

      const aIsAdvanced = aRank >= 2;
      const bIsAdvanced = bRank >= 2;
      if (aIsAdvanced !== bIsAdvanced) return aIsAdvanced ? 1 : -1;

      if (aRank !== bRank) return aRank - bRank;

      return String(a.title).localeCompare(String(b.title));
    });
  }, []);
  const liveCourses = getLiveCourseCardData();

  return (
    <main className="min-h-screen bg-background">
      <Navbar />
      
      <section className="relative overflow-hidden pt-5 md:pt-7 pb-10">
        <div className="absolute inset-0 bg-gradient-to-b from-background via-background to-background/50" />
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-6xl mx-auto">
            <div className="text-center space-y-4 mb-6">
              <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto">
                Master cybersecurity with our comprehensive blue team training programs
              </p>
            </div>

            {/* Tab Selection */}
            <div className="flex justify-center gap-3 mb-6">
              <button 
                onClick={() => setActiveTab("self-paced")} 
                className={`px-5 py-2.5 rounded-lg font-medium text-sm transition-all duration-300 ${
                  activeTab === "self-paced" 
                    ? "bg-primary text-primary-foreground shadow-md shadow-primary/25" 
                    : "bg-card/50 border border-border text-muted-foreground hover:border-primary/50 hover:text-foreground"
                }`}
              >
                Self Paced
              </button>
              <button 
                onClick={() => setActiveTab("live")} 
                className={`px-5 py-2.5 rounded-lg font-medium text-sm transition-all duration-300 ${
                  activeTab === "live" 
                    ? "bg-secondary text-secondary-foreground shadow-md shadow-secondary/25" 
                    : "bg-card/50 border border-border text-muted-foreground hover:border-secondary/50 hover:text-foreground"
                }`}
              >
                Live Training
              </button>
            </div>

            {/* Course Description */}
            <p className="text-center text-muted-foreground mb-6 max-w-2xl mx-auto">
              {activeTab === "self-paced" 
                ? "Learn at your own pace with our comprehensive pre-recorded courses. Access anytime, anywhere." 
                : "Interactive instructor-led sessions with real-time Q&A, hands-on labs, and personalized feedback."
              }
            </p>
            
            {/* Courses Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {activeTab === "self-paced"
                ? selfPacedCourses.map((course, index) => (
                    <CourseCard
                      key={course.courseId}
                      title={course.title}
                      description={course.description}
                      index={index}
                      difficulty={course.difficulty}
                      slug={(course as any).slug ?? course.courseId}
                      thumbnail={course.thumbnail}
                      price={course.courseId === FREE_COURSE_SLUG ? 0 : course.difficulty === "easy" ? prices.easy : course.difficulty === "medium" ? prices.medium : prices.hard}
                      symbol={symbol}
                    />
                  ))
                : liveCourses.map((course, index) => (
                    <CourseCard
                      key={course.id}
                      title={course.title}
                      description={course.description}
                      index={index}
                      slug={course.id}
                      isLiveCourse={true}
                    />
                  ))}
            </div>

            {activeTab === "self-paced" && !hasBundle && (
              <div className="mt-10">
                <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] shadow-lg shadow-black/20">
                  <div className="absolute -inset-[1px] rounded-xl bg-gradient-to-br from-primary/20 via-transparent to-secondary/10 blur-sm pointer-events-none" />
                  <div className="relative px-6 py-5 flex flex-col gap-4">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                      <div>
                        <div className="text-sm text-muted-foreground">All Courses Bundle</div>
                        <div className="text-xs text-muted-foreground/80">Get access to all self-paced courses at one price</div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-lg font-semibold text-primary">{symbol}{prices.bundle}</div>
                        <button
                          type="button"
                          onClick={() => {
                            const accessToken = localStorage.getItem("accessToken");
                            const checkoutUrl = `/courses/${ALL_COURSES_BUNDLE_SLUG}/checkout${bundlePromo.trim() ? `?promo=${encodeURIComponent(bundlePromo.trim().toUpperCase())}` : ""}`;
                            if (!accessToken || !user) {
                              navigate(`/auth?redirect=${encodeURIComponent(checkoutUrl)}`);
                              return;
                            }
                            navigate(checkoutUrl);
                          }}
                          className="px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors"
                        >
                          Get Bundle
                        </button>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <input
                        type="text"
                        placeholder="Promo code"
                        value={bundlePromo}
                        onChange={(e) => setBundlePromo(e.target.value)}
                        className="flex-1 max-w-[200px] px-3 py-1.5 text-sm rounded-md bg-background/60 border border-border/60 text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-primary/60 transition-colors"
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>
      
      <Footer />
    </main>
  );
};

export default Courses;
