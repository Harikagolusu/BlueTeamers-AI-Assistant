import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const PrivacyPolicy = () => {
  return (
    <main className="min-h-screen bg-background">
      <Navbar />
      <div className="container mx-auto px-4 pt-20 pb-16">
        <h1 className="text-4xl font-bold text-foreground mb-2">🔐 Privacy Policy – BlueTeamers</h1>
        <p className="text-sm text-muted-foreground mb-8">Last Updated: 21-01-2026</p>
        
        <div className="prose prose-invert max-w-none space-y-8 text-muted-foreground">
          <p className="text-lg">
            BlueTeamers ("we", "our", "us") values your privacy. This Privacy Policy explains how we collect,
            use, and protect your information when you use our website, labs, and services.
          </p>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">1. Information We Collect</h2>
            <p>We may collect the following information:</p>
            
            <div className="space-y-4 pl-4">
              <div>
                <h3 className="text-lg font-medium text-foreground">a) Personal Information</h3>
                <ul className="list-disc pl-6 space-y-1 mt-2">
                  <li>Name</li>
                  <li>Email address</li>
                  <li>Login credentials (encrypted)</li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-lg font-medium text-foreground">b) Usage Information</h3>
                <ul className="list-disc pl-6 space-y-1 mt-2">
                  <li>Pages visited</li>
                  <li>Lab activity (alerts handled, progress, scores)</li>
                  <li>Login timestamps</li>
                  <li>IP address (for security purposes)</li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-lg font-medium text-foreground">c) Cookies & Tracking</h3>
                <ul className="list-disc pl-6 space-y-1 mt-2">
                  <li>Session cookies for login</li>
                  <li>Analytics cookies to understand user behavior</li>
                </ul>
              </div>
            </div>
            
            <p className="text-primary font-medium">👉 We do not sell or rent your personal data to anyone.</p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">2. How We Use Your Information</h2>
            <p>We use collected information to:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Provide access to labs and learning content</li>
              <li>Improve user experience</li>
              <li>Track lab progress and scores</li>
              <li>Generate certificates</li>
              <li>Maintain platform security</li>
              <li>Communicate important updates</li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">3. Cybersecurity Lab Data Disclaimer</h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>All logs, alerts, and incidents shown in labs are pre-recorded and simulated</li>
              <li>No real attacks are performed</li>
              <li>No real systems are accessed</li>
              <li>Lab data is for educational purposes only</li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">4. Data Security</h2>
            <p>We take reasonable security measures to protect your data:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Secure authentication mechanisms</li>
              <li>Encrypted passwords</li>
              <li>Restricted access to sensitive data</li>
            </ul>
            <p className="mt-2">However, no online platform can guarantee 100% security.</p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">5. Third-Party Services</h2>
            <p>We may use third-party services for:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Analytics</li>
              <li>Payments (if applicable)</li>
              <li>Email communication</li>
            </ul>
            <p className="mt-2">These services follow their own privacy policies.</p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">6. Your Rights</h2>
            <p>You have the right to:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Access your personal data</li>
              <li>Request correction or deletion</li>
              <li>Deactivate your account</li>
            </ul>
            <p className="mt-2">
              You can contact us at: <a href="mailto:support@infosecdairies.com" className="text-primary hover:underline">support@infosecdairies.com</a>
            </p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">7. Changes to This Policy</h2>
            <p>
              We may update this Privacy Policy from time to time. Changes will be posted on this page.
            </p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">8. Contact Us</h2>
            <p>
              For any privacy-related questions:<br />
              📧 <a href="mailto:support@infosecdairies.com" className="text-primary hover:underline">support@infosecdairies.com</a>
            </p>
          </section>
        </div>
      </div>
      <Footer />
    </main>
  );
};

export default PrivacyPolicy;
