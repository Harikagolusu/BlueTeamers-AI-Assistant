import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { AiAssistantProvider } from "./context/AiAssistantContext";
import { CurrencyProvider } from "./context/CurrencyContext";
import { HelmetProvider } from "react-helmet-async";
import Index from "./pages/Index";
import Courses from "./pages/Courses";
import CourseDetail from "./pages/CourseDetail";
import LiveCourseDetail from "./pages/LiveCourseDetail";
import LessonViewer from "./pages/LessonViewer";
import QuizPage from "./pages/QuizPage";
import Labs from "./pages/Labs";
import Alerts from "./pages/Alerts";
import Incidents from "./pages/Incidents";
import Endpoints from "./pages/Endpoints";
import ThreatIntel from "./pages/ThreatIntel";
import EmailSecurity from "./pages/EmailSecurity";
import Settings from "./pages/Settings";
import LabsLogs from "./pages/LabsLogs";
import Auth from "./pages/Auth";
import About from "./pages/About";
import Dashboard from "./pages/Dashboard";
import GoogleCallback from "./pages/GoogleCallback";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import TermsOfService from "./pages/TermsOfService";
import Disclaimer from "./pages/Disclaimer";
import NotFound from "./pages/NotFound";
import VerifyCertificate from "./pages/VerifyCertificate";
import ResourceViewer from "./pages/ResourceViewer";
import CourseCheckout from "./pages/CourseCheckout";
import VerifyEmail from "./pages/VerifyEmail";
import ForgotPassword from "./pages/ForgotPassword";
import GoogleOnboarding from "./pages/GoogleOnboarding";
import CookieConsent from "./components/CookieConsent";
import ChatPage from "./pages/ChatPage";

const queryClient = new QueryClient();

const App = () => (
  <HelmetProvider>
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <CookieConsent />
        <AuthProvider>
          <CurrencyProvider>
          <BrowserRouter>
            <AiAssistantProvider>
            <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/about" element={<About />} />
            <Route path="/courses" element={<Courses />} />
            <Route path="/courses/:slug" element={<CourseDetail />} />
            <Route path="/live-courses/:courseId" element={<LiveCourseDetail />} />
            <Route path="/courses/:slug/lesson/:lessonId" element={<LessonViewer />} />
            <Route path="/courses/:slug/quiz/:quizId" element={<QuizPage />} />
            <Route path="/courses/:slug/checkout" element={<CourseCheckout />} />
            <Route path="/courses/:courseId/resources/:resourceId" element={<ResourceViewer />} />
            <Route path="/courses/:courseId/resource/:resourceId" element={<ResourceViewer />} />
            <Route path="/labs" element={<Labs />} />
            <Route path="/labs/alerts" element={<Alerts />} />
            <Route path="/labs/incidents" element={<Incidents />} />
            <Route path="/labs/endpoints" element={<Endpoints />} />
            <Route path="/labs/threat-intel" element={<ThreatIntel />} />
            <Route path="/labs/email-security" element={<EmailSecurity />} />
            <Route path="/labs/settings" element={<Settings />} />
            <Route path="/labs/logs" element={<LabsLogs />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/verify-email" element={<VerifyEmail />} />
            <Route path="/google/onboarding" element={<GoogleOnboarding />} />
            <Route path="/auth/google-callback" element={<GoogleCallback />} />
            <Route path="/privacy" element={<PrivacyPolicy />} />
            <Route path="/terms" element={<TermsOfService />} />
            <Route path="/disclaimer" element={<Disclaimer />} />
            <Route path="/verify/:slug/:emailHash" element={<VerifyCertificate />} />
            <Route path="/verify" element={<VerifyCertificate />} />
            <Route path="/Verify" element={<VerifyCertificate />} />
            <Route path="/VerifyCertificate" element={<Navigate to="/Verify" replace />} />
            <Route path="/verify-certificate/*" element={<Navigate to="/Verify" replace />} />
            <Route path="/cert/*" element={<Navigate to="/Verify" replace />} />
            <Route path="/chat" element={<ChatPage />} />
            {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
            <Route path="*" element={<NotFound />} />
          </Routes>
            </AiAssistantProvider>
        </BrowserRouter>
          </CurrencyProvider>
        </AuthProvider>
      </TooltipProvider>
    </QueryClientProvider>
  </HelmetProvider>
);

export default App;
