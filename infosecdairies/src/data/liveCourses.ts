export interface LiveCourseModule {
  week: number;
  title: string;
  topics: string[];
}

export interface LiveCourse {
  id: string;
  title: string;
  tagline: string;
  description: string;
  duration: string;
  format: string;
  batchSize: string;
  fee: string;
  whoIsItFor: string[];
  whatYouWillLearn: string[];
  roadmap: LiveCourseModule[];
  prerequisites: string[];
  certificationDetails: string;
}

export const liveCourses: LiveCourse[] = [
  {
    id: "soc-analyst",
    title: "SOC Analyst",
    tagline: "Become a Battle-Ready Security Operations Center Analyst",
    description: "This intensive live training transforms you into a skilled SOC Analyst capable of detecting, analyzing, and responding to cyber threats in real-time. Learn from practitioners who work in active SOC environments and gain hands-on experience with industry-standard tools and methodologies.",
    duration: "8 Weeks",
    format: "Live Online Sessions (Weekends)",
    batchSize: "Limited to 20 participants",
    fee: "₹15,000",
    whoIsItFor: [
      "Fresh graduates aspiring to enter cybersecurity",
      "IT professionals transitioning to security roles",
      "Network administrators seeking SOC expertise",
      "Help desk technicians wanting career advancement",
      "Anyone passionate about defending against cyber threats"
    ],
    whatYouWillLearn: [
      "Master the SOC analyst workflow from alert triage to incident escalation",
      "Analyze security events across Windows, Linux, and network devices",
      "Investigate phishing attacks, malware infections, and unauthorized access",
      "Create detection rules and correlation searches in SIEM platforms",
      "Document incidents professionally and communicate with stakeholders",
      "Understand attacker tactics using the MITRE ATT&CK framework",
      "Build threat intelligence feeds and IOC management processes",
      "Handle real-world scenarios through simulated attack exercises"
    ],
    roadmap: [
      {
        week: 1,
        title: "SOC Foundations & Security Fundamentals",
        topics: [
          "Understanding the SOC ecosystem and analyst responsibilities",
          "Security operations metrics and KPIs that matter",
          "Introduction to log sources: firewalls, IDS/IPS, endpoints",
          "Setting up your analysis workstation and tools"
        ]
      },
      {
        week: 2,
        title: "Log Analysis & Event Investigation",
        topics: [
          "Windows event log deep-dive: authentication, process creation, PowerShell",
          "Linux syslog analysis: auth logs, cron, application logs",
          "Network traffic analysis fundamentals with Wireshark",
          "Correlating events across multiple log sources"
        ]
      },
      {
        week: 3,
        title: "SIEM Operations & Alert Management",
        topics: [
          "SIEM architecture and data flow understanding",
          "Writing effective search queries and filters",
          "Alert triage methodology: true positive vs false positive",
          "Building dashboards for operational visibility"
        ]
      },
      {
        week: 4,
        title: "Threat Detection & MITRE ATT&CK",
        topics: [
          "MITRE ATT&CK framework navigation and application",
          "Detecting reconnaissance and initial access techniques",
          "Identifying persistence and privilege escalation",
          "Lateral movement and data exfiltration detection"
        ]
      },
      {
        week: 5,
        title: "Phishing & Email Security Analysis",
        topics: [
          "Email header analysis and sender verification",
          "URL and attachment analysis techniques",
          "Phishing campaign identification and tracking",
          "Building email security playbooks"
        ]
      },
      {
        week: 6,
        title: "Endpoint Detection & Response",
        topics: [
          "Understanding EDR solutions and their capabilities",
          "Investigating suspicious process behavior",
          "Memory analysis fundamentals for malware detection",
          "Endpoint isolation and containment procedures"
        ]
      },
      {
        week: 7,
        title: "Incident Response & Documentation",
        topics: [
          "Incident classification and severity assessment",
          "Evidence collection and chain of custody",
          "Writing clear and actionable incident reports",
          "Post-incident review and lessons learned"
        ]
      },
      {
        week: 8,
        title: "Capstone Project & Career Preparation",
        topics: [
          "Full-scale simulated attack scenario investigation",
          "Building your SOC analyst portfolio",
          "Resume optimization and interview preparation",
          "Certification roadmap: Security+, CySA+, BTL1"
        ]
      }
    ],
    prerequisites: [
      "Basic understanding of networking concepts (TCP/IP, DNS, HTTP)",
      "Familiarity with Windows and Linux operating systems",
      "Enthusiasm to learn and dedication to practice",
      "Laptop with minimum 8GB RAM for lab exercises"
    ],
    certificationDetails: "Certificate of Completion awarded upon finishing all modules and capstone project. This training prepares you for CompTIA CySA+ and BTL1 certifications."
  },
  {
    id: "splunk-engineer",
    title: "Splunk Engineer",
    tagline: "Master Enterprise Security Intelligence with Splunk",
    description: "Transform raw data into actionable security intelligence with Splunk. This hands-on training covers everything from basic searches to advanced SPL, dashboard creation, and enterprise security monitoring. Learn to build correlation rules, create alerts, and optimize Splunk for maximum performance.",
    duration: "6 Weeks",
    format: "Live Online Sessions (Weekends)",
    batchSize: "Limited to 15 participants",
    fee: "₹15,000",
    whoIsItFor: [
      "SOC analysts wanting to specialize in SIEM",
      "System administrators managing log infrastructure",
      "Security engineers building detection capabilities",
      "Data analysts interested in security analytics",
      "IT professionals preparing for Splunk certifications"
    ],
    whatYouWillLearn: [
      "Navigate Splunk interface and understand data ingestion pipeline",
      "Write powerful SPL queries from basic to advanced level",
      "Create stunning visualizations and interactive dashboards",
      "Build correlation searches for threat detection",
      "Configure alerts and automated response actions",
      "Optimize search performance and manage index storage",
      "Implement role-based access control and data governance",
      "Deploy Splunk Enterprise Security (ES) apps and add-ons"
    ],
    roadmap: [
      {
        week: 1,
        title: "Splunk Architecture & Data Ingestion",
        topics: [
          "Understanding Splunk components: indexers, search heads, forwarders",
          "Data onboarding: syslog, file monitoring, API inputs",
          "Index management and data retention policies",
          "Sourcetype configuration and field extraction"
        ]
      },
      {
        week: 2,
        title: "SPL Fundamentals & Search Mastery",
        topics: [
          "Search processing language (SPL) syntax and structure",
          "Statistical commands: stats, chart, timechart, top",
          "Transformation commands: eval, rex, replace, lookup",
          "Subsearch and join operations for complex analysis"
        ]
      },
      {
        week: 3,
        title: "Advanced SPL & Field Operations",
        topics: [
          "Regular expressions for field extraction",
          "Transaction and session analysis techniques",
          "Macro creation and knowledge object management",
          "Calculated fields and field aliases"
        ]
      },
      {
        week: 4,
        title: "Visualizations & Dashboard Development",
        topics: [
          "Chart types and when to use them effectively",
          "Building interactive dashboards with drilldowns",
          "Dashboard Studio and classic dashboard comparison",
          "Token-based filtering and dynamic panels"
        ]
      },
      {
        week: 5,
        title: "Alerting & Security Monitoring",
        topics: [
          "Creating effective alert conditions",
          "Scheduled searches and real-time alerting",
          "Correlation searches for multi-stage attacks",
          "Integration with ticketing and SOAR platforms"
        ]
      },
      {
        week: 6,
        title: "Enterprise Security & Optimization",
        topics: [
          "Splunk Enterprise Security (ES) overview",
          "Notable events and investigation workflows",
          "Performance tuning and search optimization",
          "Splunk certification exam preparation"
        ]
      }
    ],
    prerequisites: [
      "Basic understanding of log formats and data structures",
      "Familiarity with command-line interfaces",
      "Understanding of security concepts and terminology",
      "Access to a system capable of running Splunk (provided for labs)"
    ],
    certificationDetails: "Certificate of Completion provided. This course prepares you for Splunk Core Certified User and Splunk Core Certified Power User certifications."
  },
  {
    id: "digital-forensics",
    title: "Digital Forensics",
    tagline: "Investigate Cybercrime Like a Professional Forensic Analyst",
    description: "Dive deep into the world of digital forensics and learn to investigate cybercrimes systematically. From evidence acquisition to courtroom-ready reporting, this training covers disk forensics, memory analysis, and network forensics using industry-standard tools and methodologies.",
    duration: "10 Weeks",
    format: "Live Online Sessions (Weekends)",
    batchSize: "Limited to 15 participants",
    fee: "₹15,000",
    whoIsItFor: [
      "Security professionals expanding into forensics",
      "Law enforcement officers investigating cybercrime",
      "Incident responders needing forensic skills",
      "IT auditors performing investigations",
      "Students pursuing careers in digital forensics"
    ],
    whatYouWillLearn: [
      "Apply forensic methodology while maintaining evidence integrity",
      "Create forensically sound disk images and verify their authenticity",
      "Analyze Windows artifacts: registry, prefetch, event logs, browser history",
      "Investigate Linux systems: bash history, logs, user activity",
      "Perform memory acquisition and analysis for malware detection",
      "Recover deleted files and analyze file system structures",
      "Conduct network traffic analysis for breach investigation",
      "Document findings and prepare court-admissible reports"
    ],
    roadmap: [
      {
        week: 1,
        title: "Digital Forensics Fundamentals",
        topics: [
          "Introduction to digital forensics and its applications",
          "Legal considerations and chain of custody procedures",
          "Types of digital evidence and handling protocols",
          "Setting up your forensic workstation"
        ]
      },
      {
        week: 2,
        title: "Evidence Acquisition & Imaging",
        topics: [
          "Write blocking and forensic imaging concepts",
          "Creating forensic images with FTK Imager and dd",
          "Hash verification and evidence integrity",
          "Working with different storage media types"
        ]
      },
      {
        week: 3,
        title: "File System Analysis",
        topics: [
          "Understanding NTFS, FAT, and ext file systems",
          "Master File Table (MFT) analysis",
          "File recovery and carving techniques",
          "Analyzing alternate data streams and timestamps"
        ]
      },
      {
        week: 4,
        title: "Windows Forensic Artifacts",
        topics: [
          "Registry analysis: user activity, installed programs, USB devices",
          "Prefetch and Shimcache investigation",
          "LNK files and jump lists analysis",
          "Browser forensics: history, cookies, cached data"
        ]
      },
      {
        week: 5,
        title: "Windows Event Log Analysis",
        topics: [
          "Security event log investigation",
          "Logon analysis and lateral movement detection",
          "PowerShell and process execution logging",
          "Timeline analysis and event correlation"
        ]
      },
      {
        week: 6,
        title: "Linux Forensics",
        topics: [
          "Linux file system and directory structure",
          "User activity artifacts: bash history, .recently-used",
          "Log analysis: auth, syslog, application logs",
          "Investigating web servers and databases"
        ]
      },
      {
        week: 7,
        title: "Memory Forensics",
        topics: [
          "Memory acquisition techniques",
          "Volatility framework fundamentals",
          "Process and network connection analysis",
          "Detecting malware and rootkits in memory"
        ]
      },
      {
        week: 8,
        title: "Network Forensics",
        topics: [
          "Packet capture and analysis fundamentals",
          "Reconstructing network sessions and file transfers",
          "Analyzing malicious traffic patterns",
          "C2 communication identification"
        ]
      },
      {
        week: 9,
        title: "Malware Forensics & Triage",
        topics: [
          "Static analysis: PE headers, strings, imports",
          "Dynamic analysis in isolated environments",
          "Identifying indicators of compromise (IOCs)",
          "Malware family classification and reporting"
        ]
      },
      {
        week: 10,
        title: "Reporting & Capstone Investigation",
        topics: [
          "Writing professional forensic reports",
          "Presenting findings to non-technical stakeholders",
          "Full-scale investigation simulation",
          "Career paths and certification guidance"
        ]
      }
    ],
    prerequisites: [
      "Strong understanding of Windows and Linux operating systems",
      "Basic networking knowledge",
      "Familiarity with command-line operations",
      "Laptop with 16GB RAM and 100GB free space for forensic VMs"
    ],
    certificationDetails: "Certificate of Completion awarded. This training prepares you for certifications like CHFI, GCFE, and EnCE."
  },
  {
    id: "grc",
    title: "GRC (Governance, Risk & Compliance)",
    tagline: "Build and Manage Enterprise Security Programs",
    description: "Master the strategic side of cybersecurity with comprehensive GRC training. Learn to develop security policies, conduct risk assessments, manage compliance programs, and align security initiatives with business objectives. Perfect for those transitioning into security management roles.",
    duration: "8 Weeks",
    format: "Live Online Sessions (Weekends)",
    batchSize: "Limited to 20 participants",
    fee: "₹15,000",
    whoIsItFor: [
      "Security professionals moving into management",
      "IT managers responsible for compliance",
      "Risk analysts and internal auditors",
      "Consultants advising on security frameworks",
      "Anyone pursuing CISM, CRISC, or CGEIT certifications"
    ],
    whatYouWillLearn: [
      "Understand governance structures and security program management",
      "Conduct comprehensive risk assessments using proven methodologies",
      "Implement and manage compliance programs for multiple frameworks",
      "Develop security policies, standards, and procedures",
      "Manage third-party and vendor risk effectively",
      "Prepare for and navigate security audits successfully",
      "Build business cases for security investments",
      "Align security initiatives with organizational objectives"
    ],
    roadmap: [
      {
        week: 1,
        title: "Security Governance Fundamentals",
        topics: [
          "Understanding corporate governance and security's role",
          "Security program structure and organizational placement",
          "Roles and responsibilities: CISO, security team, business units",
          "Security strategy development and roadmap planning"
        ]
      },
      {
        week: 2,
        title: "Risk Management Principles",
        topics: [
          "Risk management frameworks: NIST, ISO 31000, FAIR",
          "Risk identification and threat modeling",
          "Qualitative vs quantitative risk assessment",
          "Risk treatment options and acceptance criteria"
        ]
      },
      {
        week: 3,
        title: "Security Frameworks Deep-Dive",
        topics: [
          "NIST Cybersecurity Framework implementation",
          "ISO 27001/27002 controls and certification",
          "CIS Controls prioritization and mapping",
          "Framework selection and customization strategies"
        ]
      },
      {
        week: 4,
        title: "Compliance Management",
        topics: [
          "Regulatory landscape: GDPR, HIPAA, PCI-DSS, SOX",
          "Building a compliance program from scratch",
          "Evidence collection and documentation practices",
          "Managing multiple compliance requirements efficiently"
        ]
      },
      {
        week: 5,
        title: "Policy Development & Management",
        topics: [
          "Policy hierarchy: policies, standards, procedures, guidelines",
          "Writing effective security policies",
          "Policy lifecycle management and exceptions",
          "Communicating policies to the organization"
        ]
      },
      {
        week: 6,
        title: "Third-Party Risk Management",
        topics: [
          "Vendor risk assessment methodology",
          "Due diligence questionnaires and evaluations",
          "Contract security requirements",
          "Ongoing monitoring and risk reassessment"
        ]
      },
      {
        week: 7,
        title: "Audit Management & Reporting",
        topics: [
          "Preparing for external audits",
          "Internal audit program development",
          "Managing audit findings and remediation",
          "Executive reporting and metrics that matter"
        ]
      },
      {
        week: 8,
        title: "Business Continuity & Program Maturity",
        topics: [
          "Business continuity and disaster recovery basics",
          "Security awareness program development",
          "Measuring and improving program maturity",
          "Career paths in GRC and certification preparation"
        ]
      }
    ],
    prerequisites: [
      "Basic understanding of information security concepts",
      "Some professional experience in IT or security",
      "Interest in security management and strategy",
      "Strong communication and documentation skills"
    ],
    certificationDetails: "Certificate of Completion provided. This training aligns with CISM, CRISC, and CGRC certification requirements."
  },
  {
    id: "bug-bounty",
    title: "Bug Bounty Hunter",
    tagline: "Discover Vulnerabilities and Earn While You Learn",
    description: "Enter the exciting world of bug bounty hunting where you get paid to find security vulnerabilities. This practical training teaches you reconnaissance, web application testing, and responsible disclosure. Learn the techniques used by successful bug bounty hunters to find high-impact vulnerabilities.",
    duration: "8 Weeks",
    format: "Live Online Sessions (Weekends)",
    batchSize: "Limited to 15 participants",
    fee: "₹15,000",
    whoIsItFor: [
      "Security enthusiasts wanting to earn through bug bounties",
      "Web developers interested in security testing",
      "Penetration testers expanding their skills",
      "Students aspiring to become ethical hackers",
      "Anyone curious about finding security vulnerabilities"
    ],
    whatYouWillLearn: [
      "Navigate bug bounty platforms and understand program rules",
      "Perform comprehensive reconnaissance and asset discovery",
      "Identify and exploit web application vulnerabilities",
      "Test authentication and authorization mechanisms",
      "Find business logic flaws that automated tools miss",
      "Write professional vulnerability reports that get accepted",
      "Understand responsible disclosure and legal boundaries",
      "Build a sustainable bug bounty hunting methodology"
    ],
    roadmap: [
      {
        week: 1,
        title: "Bug Bounty Fundamentals",
        topics: [
          "Understanding the bug bounty ecosystem",
          "Platform selection: HackerOne, Bugcrowd, Intigriti",
          "Reading and understanding program scope",
          "Setting up your testing environment safely"
        ]
      },
      {
        week: 2,
        title: "Reconnaissance & Asset Discovery",
        topics: [
          "Subdomain enumeration techniques",
          "Port scanning and service identification",
          "Technology fingerprinting and stack analysis",
          "Finding hidden endpoints and parameters"
        ]
      },
      {
        week: 3,
        title: "Web Application Security Basics",
        topics: [
          "HTTP protocol deep-dive",
          "Understanding cookies, sessions, and tokens",
          "Proxy setup and traffic interception",
          "Common vulnerability classes overview (OWASP Top 10)"
        ]
      },
      {
        week: 4,
        title: "Injection Vulnerabilities",
        topics: [
          "SQL injection: detection and exploitation",
          "Cross-Site Scripting (XSS): reflected, stored, DOM-based",
          "Command injection and template injection",
          "XXE and other XML-based attacks"
        ]
      },
      {
        week: 5,
        title: "Authentication & Authorization Flaws",
        topics: [
          "Authentication bypass techniques",
          "IDOR and broken access control",
          "JWT and token-based auth vulnerabilities",
          "OAuth and SSO misconfiguration"
        ]
      },
      {
        week: 6,
        title: "Advanced Vulnerability Discovery",
        topics: [
          "Server-Side Request Forgery (SSRF)",
          "Business logic vulnerabilities",
          "Race conditions and timing attacks",
          "Subdomain takeover hunting"
        ]
      },
      {
        week: 7,
        title: "Reporting & Communication",
        topics: [
          "Writing impactful vulnerability reports",
          "Proof of concept development",
          "Communicating with security teams effectively",
          "Handling disputes and escalations"
        ]
      },
      {
        week: 8,
        title: "Building Your Bug Bounty Career",
        topics: [
          "Developing your hunting methodology",
          "Automation and tool development",
          "Managing time and avoiding burnout",
          "Success stories and community involvement"
        ]
      }
    ],
    prerequisites: [
      "Basic understanding of web technologies (HTML, JavaScript, HTTP)",
      "Familiarity with command-line interfaces",
      "Ethical mindset and commitment to legal testing only",
      "Laptop with ability to run virtual machines"
    ],
    certificationDetails: "Certificate of Completion awarded. This training provides a strong foundation for OSCP, OSWE, and eWPT certifications."
  }
];

export interface LiveCourseCardData {
  id: string;
  title: string;
  description: string;
}

const liveCoursesCardData: LiveCourseCardData[] = liveCourses.map(course => ({
  id: course.id,
  title: course.title,
  description: course.description.substring(0, 150) + "..."
}));

export const getLiveCourseCardData = (): LiveCourseCardData[] => {
  return liveCoursesCardData;
};

export const getLiveCourseById = (id: string): LiveCourse | undefined => {
  return liveCourses.find(course => course.id === id);
};
