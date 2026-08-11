import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const Disclaimer = () => {
  return (
    <main className="min-h-screen bg-background">
      <Navbar />
      <div className="container mx-auto px-4 pt-20 pb-16">
        <h1 className="text-4xl font-bold text-foreground mb-2">⚠️ Disclaimer – BlueTeamers</h1>
        <p className="text-sm text-muted-foreground mb-8">Last Updated: 21-01-2026</p>
        
        <div className="prose prose-invert max-w-none space-y-8 text-muted-foreground">
          <p className="text-lg">
            The information, labs, and training provided on BlueTeamers are intended strictly for
            educational and learning purposes only.
          </p>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">1. Educational Use Only</h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>All cybersecurity labs, alerts, logs, dashboards, and scenarios are simulated and pre-recorded</li>
              <li>No real-world systems are targeted</li>
              <li>No live attacks are performed</li>
              <li>No real malware is deployed</li>
            </ul>
            <p className="text-primary font-medium mt-2">👉 The platform is designed only to teach cybersecurity concepts and SOC analyst skills.</p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">2. No Authorization for Illegal Activity</h2>
            <p>BlueTeamers does not encourage, promote, or authorize:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Hacking real systems</li>
              <li>Unauthorized access</li>
              <li>Exploitation of live networks</li>
              <li>Malicious or illegal activities</li>
            </ul>
            <p className="mt-2 font-medium text-destructive">
              Any actions performed outside this platform using learned knowledge are solely the user's responsibility.
            </p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">3. Limitation of Responsibility</h2>
            <p>BlueTeamers is not responsible for:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Misuse of cybersecurity knowledge</li>
              <li>Illegal actions taken by users</li>
              <li>Damage caused to systems, networks, or data</li>
              <li>Legal consequences faced by users</li>
            </ul>
            <p className="mt-2">Users are responsible for complying with local, national, and international laws.</p>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">4. Accuracy of Content</h2>
            <p>
              While we strive to provide accurate and up-to-date content, BlueTeamers makes no guarantees
              regarding completeness or accuracy.
            </p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Cybersecurity threats and tools evolve constantly.</li>
              <li>Content is provided "as is" without warranties of any kind.</li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">5. Professional Disclaimer</h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>Labs and simulations do not represent real-time production environments</li>
              <li>Results, scores, or outcomes in labs do not guarantee job placement or professional performance</li>
              <li>Certifications provided are educational proof, not legal or professional licenses</li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">6. External Links Disclaimer</h2>
            <p>BlueTeamers may contain links to third-party websites. We are not responsible for:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>External content</li>
              <li>Privacy practices</li>
              <li>Security of third-party sites</li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">7. Consent</h2>
            <p>By using BlueTeamers, you acknowledge that:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>You have read and understood this disclaimer</li>
              <li>You agree to use the platform responsibly</li>
              <li>You accept full responsibility for your actions</li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-foreground">8. Contact Information</h2>
            <p>
              For questions regarding this disclaimer:<br />
              📧 <a href="mailto:support@infosecdairies.com" className="text-primary hover:underline">support@infosecdairies.com</a>
            </p>
          </section>
        </div>
      </div>
      <Footer />
    </main>
  );
};

export default Disclaimer;
