import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const TermsOfService = () => {
  return (
    <main className="min-h-screen bg-background">
      <Navbar />
      <div className="container mx-auto px-4 pt-20 pb-16">
        <h1 className="text-4xl font-bold text-foreground mb-2">📜 Terms of Service – BlueTeamers</h1>
        <p className="text-sm text-muted-foreground mb-8">Last Updated: 21-01-2026</p>
        
        <div className="prose prose-invert max-w-none space-y-8 text-muted-foreground">
          <p className="text-lg">
            By accessing or using BlueTeamers, you agree to these Terms of Service.
          </p>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">1. Purpose of the Platform</h2>
            <p>BlueTeamers provides:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Cybersecurity learning content</li>
              <li>Simulated SOC labs</li>
              <li>Educational training environments</li>
            </ul>
            <p className="text-primary font-medium mt-2">👉 This platform is strictly for educational purposes only.</p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">2. User Responsibilities</h2>
            <p>By using this platform, you agree that:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>You will not misuse the knowledge gained</li>
              <li>You will not attempt real-world hacking or exploitation</li>
              <li>You will not attack real systems using lab knowledge</li>
              <li>You will not share your account with others</li>
            </ul>
            <p className="mt-2 font-medium text-destructive">Violation may result in account suspension or termination.</p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">3. Lab Environment Rules</h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>Labs use pre-recorded and simulated data</li>
              <li>No live attacks are conducted</li>
              <li>No real malware is used</li>
              <li>Actions taken in labs are for learning only</li>
            </ul>
            <p className="mt-2">BlueTeamers is not responsible for misuse of skills outside the platform.</p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">4. Intellectual Property</h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>All lab content, dashboards, explanations, and designs belong to BlueTeamers</li>
              <li>You may not copy, redistribute, or resell any content</li>
              <li>Certificates are for personal use only</li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">5. Payments & Refunds (If Applicable)</h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>Paid access is subject to the Refund Policy</li>
              <li>Refunds may not be available after lab access is granted</li>
              <li>Certificate issuance may void refund eligibility</li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">6. Account Termination</h2>
            <p>We reserve the right to:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Suspend or terminate accounts</li>
              <li>Restrict access without notice</li>
            </ul>
            <p className="mt-2">If terms are violated or misuse is detected.</p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">7. Limitation of Liability</h2>
            <p>BlueTeamers is not liable for:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Any illegal activity done using learned skills</li>
              <li>Any damage caused by misuse of information</li>
              <li>Losses arising from reliance on lab outcomes</li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">8. Changes to Terms</h2>
            <p>
              We may update these Terms at any time. Continued use means acceptance of updated terms.
            </p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">9. Contact Information</h2>
            <p>
              📧 <a href="mailto:support@infosecdairies.com" className="text-primary hover:underline">support@infosecdairies.com</a>
            </p>
          </section>
        </div>
      </div>
      <Footer />
    </main>
  );
};

export default TermsOfService;
