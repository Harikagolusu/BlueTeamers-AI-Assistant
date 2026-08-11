import { useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import CourseCard from "@/components/CourseCard";
import { getCourseCardData } from "@/data/courses";
import { getLiveCourseCardData } from "@/data/liveCourses";

const Courses = () => {
  const [activeTab, setActiveTab] = useState<"self-paced" | "live">("self-paced");
  
  const selfPacedCourses = getCourseCardData();
  const liveCourses = getLiveCourseCardData();

  return (
    <main className="min-h-screen bg-background">
      <Navbar />
      
      <section className="relative min-h-screen overflow-hidden py-20">
        <div className="absolute inset-0 bg-gradient-to-b from-background via-background to-background/50" />
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-6xl mx-auto">
            <div className="text-center space-y-6 mb-12">
              <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto">
                Master cybersecurity with our comprehensive blue team training programs
              </p>
            </div>

            {/* Tab Selection */}
            <div className="flex justify-center gap-3 mb-12">
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
            <p className="text-center text-muted-foreground mb-10 max-w-2xl mx-auto">
              {activeTab === "self-paced" 
                ? "Learn at your own pace with our comprehensive pre-recorded courses. Access anytime, anywhere." 
                : "Interactive instructor-led sessions with real-time Q&A, hands-on labs, and personalized feedback."
              }
            </p>
            
            {/* Courses Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {activeTab === "self-paced" 
                ? selfPacedCourses.map((course, index) => (
                    <CourseCard 
                      key={course.courseId} 
                      title={course.title} 
                      description={course.description} 
                      index={index} 
                      difficulty={course.difficulty}
                      courseId={course.courseId}
                      thumbnail={course.thumbnail}
                    />
                  ))
                : liveCourses.map((course, index) => (
                    <CourseCard 
                      key={course.id} 
                      title={course.title} 
                      description={course.description} 
                      index={index}
                      courseId={course.id}
                      isLiveCourse={true}
                    />
                  ))
              }
            </div>
          </div>
        </div>
      </section>
      
      <Footer />
    </main>
  );
};

export default Courses;
