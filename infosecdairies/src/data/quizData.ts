export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
}

export interface QuizData {
  quizId: string;
  courseId: string;
  title: string;
  description: string;
  questions: QuizQuestion[];
  passingScore: number;
  timeLimit?: number; // in minutes
}

export const quizzes: QuizData[] = [
  {
    quizId: "q1",
    courseId: "soc-fundamentals",
    title: "SOC Fundamentals Quiz",
    description: "Test your understanding of SOC operations, team roles, and basic workflows.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      {
        id: "q1-1",
        question: "What is the primary mission of a Security Operations Center (SOC)?",
        options: [
          "To train employees on computer basics",
          "To develop new software applications",
          "To detect, analyze, and respond to cybersecurity incidents",
          "To manage the company's IT infrastructure"
        ],
        correctAnswer: 2,
        explanation: "The SOC's primary mission is to detect, analyze, and respond to cybersecurity incidents using technology and defined processes."
      },
      {
        id: "q1-2",
        question: "What does MTTD stand for in SOC metrics?",
        options: [
          "Mean Time To Detect",
          "Mean Time To Document",
          "Maximum Time To Deploy",
          "Minimum Time To Destroy"
        ],
        correctAnswer: 0,
        explanation: "MTTD stands for Mean Time To Detect - the average time it takes to identify a security threat after it enters the environment."
      },
      {
        id: "q1-3",
        question: "Which SOC tier is responsible for initial alert triage?",
        options: [
          "Tier 3 - Senior Analyst",
          "Tier 2 - Incident Responder",
          "SOC Manager",
          "Tier 1 - SOC Analyst"
        ],
        correctAnswer: 3,
        explanation: "Tier 1 SOC Analysts are on the front lines, responsible for monitoring alerts and performing initial triage."
      },
      {
        id: "q1-4",
        question: "What is SIEM an acronym for?",
        options: [
          "Secure Internet and Email Management",
          "Server Infrastructure and Endpoint Monitoring",
          "Security Information and Event Management",
          "System Integration and Event Monitoring"
        ],
        correctAnswer: 2,
        explanation: "SIEM stands for Security Information and Event Management - systems that collect, analyze, and correlate security event data."
      },
      {
        id: "q1-5",
        question: "Which of the following is NOT a core function of a SOC?",
        options: [
          "Threat Intelligence",
          "Incident Response",
          "Software Development",
          "Continuous Monitoring"
        ],
        correctAnswer: 2,
        explanation: "Software Development is not a core SOC function. The SOC focuses on monitoring, detection, response, and threat intelligence."
      },
      {
        id: "q1-6",
        question: "What type of SOC model combines internal staff with external managed services?",
        options: [
          "Hybrid SOC",
          "Managed SOC",
          "Internal SOC",
          "Virtual SOC"
        ],
        correctAnswer: 0,
        explanation: "A Hybrid SOC combines an internal team with external MSSP services, often used for 24/7 coverage."
      },
      {
        id: "q1-7",
        question: "What is EDR?",
        options: [
          "External Data Repository",
          "Email Detection and Response",
          "Endpoint Detection and Response",
          "Event Driven Reporting"
        ],
        correctAnswer: 2,
        explanation: "EDR stands for Endpoint Detection and Response - technology that provides visibility and response capabilities on endpoints."
      },
      {
        id: "q1-8",
        question: "Which characteristic is essential for a SOC analyst?",
        options: [
          "Preference for routine tasks only",
          "Curiosity and attention to detail",
          "Avoidance of documentation",
          "Ability to work in isolation"
        ],
        correctAnswer: 1,
        explanation: "Successful SOC analysts need curiosity (always asking why) and attention to detail (small anomalies can indicate big threats)."
      },
      {
        id: "q1-9",
        question: "What is the purpose of a shift handover in SOC operations?",
        options: [
          "To ensure continuity and prevent dropped incidents",
          "To delete old alerts",
          "To assign blame for incidents",
          "To reduce the number of analysts"
        ],
        correctAnswer: 0,
        explanation: "Shift handovers ensure smooth transitions and continuity of operations, preventing incidents from being dropped between shifts."
      },
      {
        id: "q1-10",
        question: "What does SOAR stand for?",
        options: [
          "Secure Operations and Risk",
          "Security Orchestration, Automation, and Response",
          "Security Operations and Reporting",
          "System Orchestration and Response"
        ],
        correctAnswer: 1,
        explanation: "SOAR stands for Security Orchestration, Automation, and Response - platforms that automate repetitive security tasks."
      },
      {
        id: "q1-11",
        question: "When should a Tier 1 analyst immediately escalate an alert?",
        options: [
          "When they're unsure about any alert",
          "Never - Tier 1 should handle everything",
          "Only at the end of their shift",
          "When confirmed malware execution or active data exfiltration is detected"
        ],
        correctAnswer: 3,
        explanation: "Immediate escalation is required for confirmed malware execution, active data exfiltration, ransomware, or compromised privileged accounts."
      },
      {
        id: "q1-12",
        question: "What is a TIP in the context of SOC tools?",
        options: [
          "Threat Intelligence Platform",
          "Technical Integration Point",
          "Targeted Intrusion Prevention",
          "Triage Information Protocol"
        ],
        correctAnswer: 0,
        explanation: "TIP stands for Threat Intelligence Platform - tools that aggregate and operationalize threat intelligence for SOC use."
      },
      {
        id: "q1-13",
        question: "Which document should an analyst create when handing over their shift?",
        options: [
          "Training certificate",
          "Company newsletter",
          "Shift handover summary with active incidents and pending items",
          "Performance review"
        ],
        correctAnswer: 2,
        explanation: "A proper shift handover summary includes statistics, active incidents, pending items, and situational awareness notes."
      },
      {
        id: "q1-14",
        question: "What is the role of a Tier 2 analyst?",
        options: [
          "Managing the SOC budget",
          "Only monitoring dashboards",
          "Deep-dive investigation of escalated alerts and containment",
          "Writing company policies"
        ],
        correctAnswer: 2,
        explanation: "Tier 2 analysts perform deeper investigation of escalated alerts, including containment actions and incident documentation."
      },
      {
        id: "q1-15",
        question: "What is MTTR in SOC metrics?",
        options: [
          "Mean Time To Review",
          "Maximum Time To Report",
          "Minimum Time To Recover",
          "Mean Time To Respond"
        ],
        correctAnswer: 3,
        explanation: "MTTR stands for Mean Time To Respond - the average time taken to respond to and begin addressing a security incident."
      }
    ]
  },
  {
    quizId: "q2",
    courseId: "soc-fundamentals",
    title: "Threat Landscape Assessment",
    description: "Evaluate your knowledge of threat actors, attack vectors, and MITRE ATT&CK.",
    passingScore: 70,
    timeLimit: 25,
    questions: [
      {
        id: "q2-1",
        question: "Which type of threat actor is typically state-sponsored and highly sophisticated?",
        options: [
          "Nation-State Actors (APT)",
          "Script Kiddies",
          "Insider Threats",
          "Hacktivists"
        ],
        correctAnswer: 0,
        explanation: "Nation-State Actors (APTs) are state-sponsored, extremely well-resourced, and use highly sophisticated techniques."
      },
      {
        id: "q2-2",
        question: "What percentage of successful cyber attacks start with phishing?",
        options: [
          "About 75%",
          "About 50%",
          "Over 90%",
          "About 25%"
        ],
        correctAnswer: 2,
        explanation: "Over 90% of successful cyber attacks begin with phishing, making it the most common initial access vector."
      },
      {
        id: "q2-3",
        question: "What is the primary motivation of cybercriminal groups?",
        options: [
          "Environmental activism",
          "Political ideology",
          "Recognition and fame",
          "Financial gain"
        ],
        correctAnswer: 3,
        explanation: "Cybercriminals are primarily financially motivated, conducting activities like ransomware attacks, BEC, and credential theft."
      },
      {
        id: "q2-4",
        question: "Which attack involves targeting a third-party vendor to reach the ultimate target?",
        options: [
          "Brute force attack",
          "DDoS attack",
          "Supply chain attack",
          "Phishing attack"
        ],
        correctAnswer: 2,
        explanation: "Supply chain attacks target trusted vendors or software providers to compromise their customers (e.g., SolarWinds)."
      },
      {
        id: "q2-5",
        question: "What is 'spear phishing'?",
        options: [
          "USB-based attacks",
          "Mass email spam",
          "Phone-based phishing",
          "Targeted phishing at specific individuals"
        ],
        correctAnswer: 3,
        explanation: "Spear phishing is targeted phishing aimed at specific individuals, using personalized information to appear legitimate."
      },
      {
        id: "q2-6",
        question: "What is a 'watering hole' attack?",
        options: [
          "Flooding a network with traffic",
          "Poisoning DNS records",
          "Compromising websites frequently visited by targets",
          "Attacking water treatment facilities"
        ],
        correctAnswer: 2,
        explanation: "A watering hole attack compromises websites that the target group frequently visits, infecting visitors with malware."
      },
      {
        id: "q2-7",
        question: "Which type of insider threat is most dangerous due to legitimate access?",
        options: [
          "Script kiddies",
          "Hacktivists",
          "External hackers",
          "Malicious insiders with authorized access"
        ],
        correctAnswer: 3,
        explanation: "Malicious insiders are dangerous because they have legitimate access, knowledge of systems, and are trusted by security controls."
      },
      {
        id: "q2-8",
        question: "What does RCE stand for in vulnerability types?",
        options: [
          "Remote Control Environment",
          "Rapid Containment Effort",
          "Risk Control Evaluation",
          "Remote Code Execution"
        ],
        correctAnswer: 3,
        explanation: "RCE stands for Remote Code Execution - the most dangerous vulnerability type that allows attackers to run code on remote systems."
      },
      {
        id: "q2-9",
        question: "What is 'credential stuffing'?",
        options: [
          "Using leaked credentials to exploit password reuse",
          "Creating fake credentials",
          "Encrypting credentials",
          "Deleting user accounts"
        ],
        correctAnswer: 0,
        explanation: "Credential stuffing uses leaked username/password pairs from breaches to try logging into other services, exploiting password reuse."
      },
      {
        id: "q2-10",
        question: "Which threat actor group is typically motivated by ideology and seeks publicity?",
        options: [
          "Nation-State Actors",
          "Hacktivists",
          "Cybercriminals",
          "Insider Threats"
        ],
        correctAnswer: 1,
        explanation: "Hacktivists are ideologically motivated and often seek publicity for their causes through attacks like website defacement and data leaks."
      },
      {
        id: "q2-11",
        question: "What is 'password spraying'?",
        options: [
          "Encrypting passwords",
          "Trying a few common passwords against many accounts",
          "Stealing passwords from memory",
          "Trying all possible password combinations"
        ],
        correctAnswer: 1,
        explanation: "Password spraying tries a small number of common passwords against many accounts to avoid lockouts while still finding weak passwords."
      },
      {
        id: "q2-12",
        question: "What framework maps adversary tactics, techniques, and procedures?",
        options: [
          "OWASP Top 10",
          "NIST Framework",
          "ISO 27001",
          "MITRE ATT&CK"
        ],
        correctAnswer: 3,
        explanation: "MITRE ATT&CK is a framework that maps adversary behavior into tactics, techniques, and procedures (TTPs) for threat analysis."
      },
      {
        id: "q2-13",
        question: "What is 'vishing'?",
        options: [
          "Video-based phishing",
          "Voice/phone-based phishing",
          "Virtual reality phishing",
          "Verified phishing"
        ],
        correctAnswer: 1,
        explanation: "Vishing is voice phishing - phone-based social engineering attacks where attackers impersonate legitimate entities."
      },
      {
        id: "q2-14",
        question: "Which malware type encrypts files and demands payment?",
        options: [
          "Worm",
          "Rootkit",
          "Trojan",
          "Ransomware"
        ],
        correctAnswer: 3,
        explanation: "Ransomware encrypts victim files and demands payment (usually cryptocurrency) for the decryption key."
      },
      {
        id: "q2-15",
        question: "What is a common indicator of a compromised insider?",
        options: [
          "Unusual access patterns and large data downloads",
          "Regular vacation requests",
          "Normal working hours",
          "Accessing only needed resources"
        ],
        correctAnswer: 0,
        explanation: "Warning signs of insider threats include unusual access patterns, large data downloads, after-hours activity, and accessing unneeded resources."
      },
      {
        id: "q2-16",
        question: "What is 'smishing'?",
        options: [
          "Social media phishing",
          "Smart device phishing",
          "SMS-based phishing",
          "Smoke and mirrors phishing"
        ],
        correctAnswer: 2,
        explanation: "Smishing is SMS-based phishing - sending malicious text messages to trick users into clicking links or revealing information."
      },
      {
        id: "q2-17",
        question: "What type of attack floods a target with traffic to make it unavailable?",
        options: [
          "SQL Injection",
          "DDoS",
          "Man-in-the-middle",
          "Phishing"
        ],
        correctAnswer: 1,
        explanation: "DDoS (Distributed Denial of Service) attacks flood a target with traffic from multiple sources to overwhelm and disable it."
      },
      {
        id: "q2-18",
        question: "What is 'typosquatting' in phishing attacks?",
        options: [
          "Registering domains similar to legitimate ones (e.g., g00gle.com)",
          "Correcting spelling errors",
          "Making typos in emails",
          "Typing too fast"
        ],
        correctAnswer: 0,
        explanation: "Typosquatting registers domain names similar to legitimate ones (using typos or look-alike characters) to deceive users."
      },
      {
        id: "q2-19",
        question: "Which APT group is attributed to North Korea?",
        options: [
          "APT33",
          "Lazarus Group",
          "APT29 (Cozy Bear)",
          "APT41"
        ],
        correctAnswer: 1,
        explanation: "Lazarus Group is attributed to North Korea and is known for targeting financial institutions and cryptocurrency."
      },
      {
        id: "q2-20",
        question: "What is 'Business Email Compromise' (BEC)?",
        options: [
          "Email server failure",
          "Fraud using compromised or spoofed business email accounts",
          "Email backup process",
          "Legitimate business communication"
        ],
        correctAnswer: 1,
        explanation: "BEC is a sophisticated scam targeting businesses using compromised or spoofed email accounts, often for wire transfer fraud."
      }
    ]
  },
  {
    quizId: "q3",
    courseId: "soc-fundamentals",
    title: "Log Analysis Challenge",
    description: "Practical quiz on Windows, Linux, and network log analysis.",
    passingScore: 70,
    timeLimit: 30,
    questions: [
      {
        id: "q3-1",
        question: "Which Windows Event ID indicates a successful logon?",
        options: [
          "4624",
          "4625",
          "4688",
          "4720"
        ],
        correctAnswer: 0,
        explanation: "Event ID 4624 indicates a successful account logon in Windows Security logs."
      },
      {
        id: "q3-2",
        question: "Which Windows Event ID indicates a failed logon attempt?",
        options: [
          "4625",
          "4648",
          "4624",
          "4634"
        ],
        correctAnswer: 0,
        explanation: "Event ID 4625 indicates a failed logon attempt, useful for detecting brute force attacks."
      },
      {
        id: "q3-3",
        question: "What does Windows Event ID 4688 record?",
        options: [
          "Account lockout",
          "User logon",
          "New process creation",
          "File deletion"
        ],
        correctAnswer: 2,
        explanation: "Event ID 4688 records new process creation, essential for tracking executed commands and programs."
      },
      {
        id: "q3-4",
        question: "Which Linux log file contains authentication events?",
        options: [
          "/var/log/auth.log",
          "/var/log/messages",
          "/var/log/apache2/access.log",
          "/var/log/boot.log"
        ],
        correctAnswer: 0,
        explanation: "The auth.log file (or secure on RHEL/CentOS) contains authentication-related events including SSH logins."
      },
      {
        id: "q3-5",
        question: "What is syslog used for in Linux systems?",
        options: [
          "User interface design",
          "Network routing",
          "Compiling code",
          "Centralized logging and log management"
        ],
        correctAnswer: 3,
        explanation: "Syslog is a standard for computer message logging, providing centralized logging capabilities in Linux/Unix systems."
      },
      {
        id: "q3-6",
        question: "Which Windows Event ID indicates a user account was created?",
        options: [
          "4720",
          "4624",
          "4688",
          "4634"
        ],
        correctAnswer: 0,
        explanation: "Event ID 4720 indicates a new user account was created, important for detecting unauthorized account creation."
      },
      {
        id: "q3-7",
        question: "What type of information do firewall logs typically contain?",
        options: [
          "Employee schedules",
          "User passwords",
          "Application source code",
          "Source/destination IPs and allow/deny decisions"
        ],
        correctAnswer: 3,
        explanation: "Firewall logs record network traffic decisions including source/destination IPs, ports, and allow/deny actions."
      },
      {
        id: "q3-8",
        question: "What does 'Logon Type 10' indicate in Windows Event 4624?",
        options: [
          "Remote Desktop (RDP) logon",
          "Network logon",
          "Service account logon",
          "Local console logon"
        ],
        correctAnswer: 0,
        explanation: "Logon Type 10 indicates a Remote Desktop (RDP) session, which could indicate lateral movement if unexpected."
      },
      {
        id: "q3-9",
        question: "Which Linux log would you check for cron job execution?",
        options: [
          "/var/log/cron or /var/log/syslog",
          "/var/log/boot.log",
          "/var/log/apache2/error.log",
          "/var/log/auth.log"
        ],
        correctAnswer: 0,
        explanation: "Cron job execution is logged in /var/log/cron (RHEL) or /var/log/syslog (Debian/Ubuntu)."
      },
      {
        id: "q3-10",
        question: "What information can DNS logs reveal about potential threats?",
        options: [
          "Only legitimate website visits",
          "User passwords",
          "Hardware specifications",
          "Command and control (C2) communication and DGA domains"
        ],
        correctAnswer: 3,
        explanation: "DNS logs can reveal C2 communications, domain generation algorithm (DGA) activity, and data exfiltration via DNS tunneling."
      },
      {
        id: "q3-11",
        question: "Which Windows Event ID indicates a member was added to a security-enabled global group?",
        options: [
          "4688",
          "4624",
          "4732",
          "4625"
        ],
        correctAnswer: 2,
        explanation: "Event ID 4732 indicates a member was added to a security-enabled local group, important for privilege escalation detection."
      },
      {
        id: "q3-12",
        question: "What is the significance of 'Logon Type 3' in Windows logs?",
        options: [
          "Remote desktop logon",
          "Batch job logon",
          "Network logon (accessing shared resources)",
          "Interactive local logon"
        ],
        correctAnswer: 2,
        explanation: "Logon Type 3 indicates a network logon, commonly seen when accessing network shares or resources."
      },
      {
        id: "q3-13",
        question: "What would multiple 4625 events from the same source IP indicate?",
        options: [
          "Successful authentication",
          "Potential brute force attack",
          "System maintenance",
          "Normal user activity"
        ],
        correctAnswer: 1,
        explanation: "Multiple failed logon attempts (4625) from the same source IP is a strong indicator of a brute force attack."
      },
      {
        id: "q3-14",
        question: "Which proxy log field is most useful for identifying malicious downloads?",
        options: [
          "Timestamp only",
          "User agent only",
          "Source IP only",
          "URL and content type"
        ],
        correctAnswer: 3,
        explanation: "URL and content type fields help identify malicious downloads by revealing the actual resources accessed and their file types."
      },
      {
        id: "q3-15",
        question: "What Linux command shows the last logged-in users?",
        options: [
          "top",
          "grep",
          "last",
          "ls -la"
        ],
        correctAnswer: 2,
        explanation: "The 'last' command shows a list of last logged-in users by reading /var/log/wtmp."
      }
    ]
  },
  {
    quizId: "q4",
    courseId: "soc-fundamentals",
    title: "SIEM & Alert Triage Quiz",
    description: "Test your knowledge of SIEM operations, search queries, and alert triage processes.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      {
        id: "q4-1",
        question: "What is the primary purpose of a SIEM?",
        options: [
          "To block network traffic",
          "To manage employee passwords",
          "To aggregate logs and provide centralized security monitoring",
          "To replace antivirus software"
        ],
        correctAnswer: 2,
        explanation: "SIEM aggregates logs from multiple sources, correlates events, and provides centralized security monitoring and alerting."
      },
      {
        id: "q4-2",
        question: "What is a correlation rule in SIEM?",
        options: [
          "Logic that identifies patterns across multiple events to detect threats",
          "A rule that deletes old logs",
          "A backup procedure",
          "A rule for password complexity"
        ],
        correctAnswer: 0,
        explanation: "Correlation rules analyze multiple events together to identify attack patterns that single events wouldn't reveal."
      },
      {
        id: "q4-3",
        question: "What is the first step in the alert triage process?",
        options: [
          "Delete the alert",
          "Understand what triggered the alert",
          "Immediately escalate to management",
          "Reset user passwords"
        ],
        correctAnswer: 1,
        explanation: "The first step is to understand what triggered the alert by reading the alert details, checking the detection rule, and gathering initial context."
      },
      {
        id: "q4-4",
        question: "What does a 'false positive' mean in alert triage?",
        options: [
          "A confirmed security incident",
          "A missed attack",
          "A system malfunction",
          "An alert triggered by benign activity"
        ],
        correctAnswer: 3,
        explanation: "A false positive is an alert that fired on benign activity - it looks suspicious but is actually legitimate behavior."
      },
      {
        id: "q4-5",
        question: "What should you do after determining an alert is a true positive?",
        options: [
          "Document findings and initiate response/escalation",
          "Ignore it until the next shift",
          "Delete the logs",
          "Close the ticket immediately"
        ],
        correctAnswer: 0,
        explanation: "After confirming a true positive, document your findings thoroughly and initiate the appropriate response or escalation."
      },
      {
        id: "q4-6",
        question: "Which SIEM search operator is used to filter results?",
        options: [
          "WHERE or search filters",
          "BACKUP",
          "RESTART",
          "DELETE"
        ],
        correctAnswer: 0,
        explanation: "WHERE clauses and search filters are used to narrow down results to specific criteria in SIEM queries."
      },
      {
        id: "q4-7",
        question: "What is 'enrichment' in the context of alert triage?",
        options: [
          "Compressing log files",
          "Creating backup copies",
          "Adding context and intelligence to alerts for better decision-making",
          "Deleting unnecessary data"
        ],
        correctAnswer: 2,
        explanation: "Enrichment adds context like threat intelligence, asset information, and user details to help analysts make better decisions."
      },
      {
        id: "q4-8",
        question: "When should you immediately escalate an alert?",
        options: [
          "Only on Mondays",
          "Never - handle everything yourself",
          "For every alert received",
          "When you detect active malware, ransomware, or data exfiltration"
        ],
        correctAnswer: 3,
        explanation: "Immediate escalation is required for confirmed active threats like ransomware, data exfiltration, or compromised privileged accounts."
      },
      {
        id: "q4-9",
        question: "What is alert fatigue?",
        options: [
          "Decreased vigilance due to overwhelming volume of alerts",
          "Physical tiredness from work",
          "Network congestion",
          "A type of malware"
        ],
        correctAnswer: 0,
        explanation: "Alert fatigue occurs when analysts become desensitized due to high volumes of alerts, potentially causing them to miss real threats."
      },
      {
        id: "q4-10",
        question: "What information should be included in alert documentation?",
        options: [
          "Only the alert title",
          "Timeline, findings, evidence, verdict, and actions taken",
          "Just the date and time",
          "Analyst's personal opinions only"
        ],
        correctAnswer: 1,
        explanation: "Complete documentation includes timeline, investigation steps, findings, evidence collected, verdict, and actions taken."
      }
    ]
  },
  {
    quizId: "q5",
    courseId: "soc-fundamentals",
    title: "Threat Intelligence Quiz",
    description: "Evaluate your understanding of threat intelligence, IOCs, and OSINT techniques.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      {
        id: "q5-1",
        question: "What are the four types of threat intelligence?",
        options: [
          "Red, Blue, Green, Yellow",
          "Primary, Secondary, Tertiary, Quaternary",
          "Internal, External, Public, Private",
          "Strategic, Tactical, Operational, Technical"
        ],
        correctAnswer: 3,
        explanation: "The four types are Strategic (high-level trends), Tactical (TTPs), Operational (campaign details), and Technical (IOCs)."
      },
      {
        id: "q5-2",
        question: "What does IOC stand for?",
        options: [
          "Intrusion of Command",
          "Internet of Computers",
          "Internal Operations Center",
          "Indicator of Compromise"
        ],
        correctAnswer: 3,
        explanation: "IOC stands for Indicator of Compromise - forensic artifacts that identify potentially malicious activity."
      },
      {
        id: "q5-3",
        question: "According to the Pyramid of Pain, which IOC type is hardest for attackers to change?",
        options: [
          "Domain names",
          "TTPs (Tactics, Techniques, Procedures)",
          "IP addresses",
          "Hash values"
        ],
        correctAnswer: 1,
        explanation: "TTPs are at the top of the Pyramid of Pain - they represent how attackers operate and are hardest to change."
      },
      {
        id: "q5-4",
        question: "What is OSINT?",
        options: [
          "Offensive Security Integration",
          "Open Source Intelligence - publicly available information",
          "Online System Integration",
          "Operating System Intelligence"
        ],
        correctAnswer: 1,
        explanation: "OSINT (Open Source Intelligence) refers to intelligence gathered from publicly available sources."
      },
      {
        id: "q5-5",
        question: "Which platform is commonly used for file hash and URL analysis?",
        options: [
          "VirusTotal",
          "Microsoft Word",
          "Excel",
          "Photoshop"
        ],
        correctAnswer: 0,
        explanation: "VirusTotal is a widely used platform for analyzing files, URLs, IPs, and domains against multiple security engines."
      },
      {
        id: "q5-6",
        question: "What is a TIP (Threat Intelligence Platform)?",
        options: [
          "A typing improvement program",
          "A platform that aggregates and operationalizes threat data",
          "A gratuity calculator",
          "A network scanner"
        ],
        correctAnswer: 1,
        explanation: "A TIP aggregates, normalizes, enriches, and helps operationalize threat intelligence from multiple sources."
      },
      {
        id: "q5-7",
        question: "What is a red flag when analyzing a domain?",
        options: [
          "It was recently registered and uses privacy protection",
          "It's hosted by a major cloud provider",
          "It's been registered for 10 years",
          "It has valid SSL certificates"
        ],
        correctAnswer: 0,
        explanation: "Recently registered domains with privacy protection are often suspicious, especially if they mimic legitimate brands."
      },
      {
        id: "q5-8",
        question: "What hash algorithm is the current standard for file identification?",
        options: [
          "SHA1",
          "CRC32",
          "MD5",
          "SHA256"
        ],
        correctAnswer: 3,
        explanation: "SHA256 is the current standard - MD5 and SHA1 are being phased out due to collision vulnerabilities."
      },
      {
        id: "q5-9",
        question: "What is pivoting in threat intelligence?",
        options: [
          "Rotating your chair",
          "Deleting old data",
          "Moving from one indicator to discover related indicators",
          "Changing passwords"
        ],
        correctAnswer: 2,
        explanation: "Pivoting means using one indicator (like an IP) to find related indicators (domains, hashes) and uncover the full threat picture."
      },
      {
        id: "q5-10",
        question: "What is AbuseIPDB used for?",
        options: [
          "Managing IP addresses",
          "Creating VPNs",
          "Checking IP reputation and abuse reports",
          "Assigning IP addresses"
        ],
        correctAnswer: 2,
        explanation: "AbuseIPDB is a community-driven database for checking and reporting malicious IP addresses."
      },
      {
        id: "q5-11",
        question: "Which type of threat intelligence is consumed by executives?",
        options: [
          "Tactical",
          "Technical",
          "Operational",
          "Strategic"
        ],
        correctAnswer: 3,
        explanation: "Strategic intelligence provides high-level trends and risk assessments intended for executive and management consumption."
      },
      {
        id: "q5-12",
        question: "What is a DGA (Domain Generation Algorithm)?",
        options: [
          "A method to create legitimate websites",
          "A domain registration service",
          "A security certification",
          "Malware technique that generates random domain names for C2"
        ],
        correctAnswer: 3,
        explanation: "DGA is used by malware to generate random-looking domain names for command and control, making blocking difficult."
      }
    ]
  },
  {
    quizId: "q6",
    courseId: "soc-fundamentals",
    title: "Incident Response Quiz",
    description: "Test your knowledge of the incident response lifecycle, containment, and documentation.",
    passingScore: 70,
    timeLimit: 25,
    questions: [
      {
        id: "q6-1",
        question: "What are the four phases of the NIST Incident Response lifecycle?",
        options: [
          "Identify, Protect, Detect, Respond",
          "Alert, Investigate, Close, Report",
          "Preparation, Detection & Analysis, Containment/Eradication/Recovery, Post-Incident",
          "Plan, Do, Check, Act"
        ],
        correctAnswer: 2,
        explanation: "NIST defines four phases: Preparation, Detection & Analysis, Containment/Eradication/Recovery, and Post-Incident Activity."
      },
      {
        id: "q6-2",
        question: "What is the purpose of the containment phase?",
        options: [
          "To delete all evidence",
          "To stop the attack from spreading while preserving evidence",
          "To ignore the incident",
          "To notify the press"
        ],
        correctAnswer: 1,
        explanation: "Containment stops the attack from spreading to other systems while preserving evidence for investigation."
      },
      {
        id: "q6-3",
        question: "If active ransomware encryption is detected on multiple systems, what severity level should be assigned?",
        options: [
          "High",
          "Low",
          "Medium",
          "Critical"
        ],
        correctAnswer: 3,
        explanation: "Active ransomware encryption is a Critical (Severity 1) incident requiring immediate, all-hands response."
      },
      {
        id: "q6-4",
        question: "What is the first containment action for a compromised user account?",
        options: [
          "Send an email to the user",
          "Reset password and terminate active sessions",
          "Delete the account",
          "Wait for management approval"
        ],
        correctAnswer: 1,
        explanation: "For account compromise, immediately reset the password and terminate all active sessions to prevent further unauthorized access."
      },
      {
        id: "q6-5",
        question: "What should you NOT do when ransomware is detected?",
        options: [
          "Isolate affected systems immediately",
          "Alert the IR team",
          "Preserve ransom notes and file samples",
          "Immediately reboot the infected machine"
        ],
        correctAnswer: 3,
        explanation: "Don't reboot - it may trigger more encryption or destroy volatile evidence. Focus on isolation and preservation first."
      },
      {
        id: "q6-6",
        question: "What is the purpose of a post-incident review?",
        options: [
          "To learn and improve processes for future incidents",
          "To delete incident records",
          "To assign blame",
          "To award bonuses"
        ],
        correctAnswer: 0,
        explanation: "Post-incident reviews focus on lessons learned and process improvement, not blame, to prevent similar incidents."
      },
      {
        id: "q6-7",
        question: "What is an incident playbook?",
        options: [
          "A list of employee contacts",
          "A standardized procedure for responding to specific incident types",
          "A children's game",
          "A software application"
        ],
        correctAnswer: 1,
        explanation: "Playbooks provide standardized, step-by-step procedures for responding to common incident types like phishing or malware."
      },
      {
        id: "q6-8",
        question: "What should be included in incident documentation?",
        options: [
          "Timeline, affected systems, actions taken, and evidence collected",
          "Just the close date",
          "Only the incident title",
          "Personal opinions about the attacker"
        ],
        correctAnswer: 0,
        explanation: "Documentation should include timeline, affected systems/users, all actions taken, evidence collected, and findings."
      },
      {
        id: "q6-9",
        question: "When responding to phishing with credential entry, what must you check for?",
        options: [
          "The user's vacation schedule",
          "Only reset the password",
          "Nothing else is needed",
          "Email forwarding rules and account activity since compromise"
        ],
        correctAnswer: 3,
        explanation: "Always check for malicious email forwarding rules and review all account activity since the compromise occurred."
      },
      {
        id: "q6-10",
        question: "What is 'eradication' in incident response?",
        options: [
          "Deleting all company data",
          "Removing malware, patching vulnerabilities, and resetting credentials",
          "Shutting down the company",
          "Firing employees"
        ],
        correctAnswer: 1,
        explanation: "Eradication involves removing malware, patching vulnerabilities, resetting compromised credentials, and cleaning affected systems."
      },
      {
        id: "q6-11",
        question: "What is the 'chain of custody' in incident response?",
        options: [
          "The order of incident responders",
          "Documentation tracking who handled evidence and when",
          "A type of malware",
          "The management hierarchy"
        ],
        correctAnswer: 1,
        explanation: "Chain of custody documents who collected, handled, and stored evidence, ensuring its integrity for potential legal proceedings."
      },
      {
        id: "q6-12",
        question: "How should severity be adjusted based on affected systems?",
        options: [
          "Decrease severity for servers",
          "Severity is never changed",
          "All systems are equal",
          "Increase severity for critical assets like domain controllers"
        ],
        correctAnswer: 3,
        explanation: "Critical assets like domain controllers, databases with sensitive data, and executive systems warrant increased severity."
      }
    ]
  },
  {
    quizId: "q7",
    courseId: "soc-fundamentals",
    title: "EDR & Endpoint Security Quiz",
    description: "Test your understanding of EDR technology, alerts, and process analysis.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      {
        id: "q7-1",
        question: "What is the main advantage of EDR over traditional antivirus?",
        options: [
          "Behavioral detection and rich telemetry for investigation",
          "It only works on Macs",
          "It's cheaper",
          "It doesn't require installation"
        ],
        correctAnswer: 0,
        explanation: "EDR provides behavioral detection (not just signatures) and rich telemetry including process, file, network, and registry data."
      },
      {
        id: "q7-2",
        question: "What does a process tree show in EDR?",
        options: [
          "A list of files",
          "Parent-child relationships between processes",
          "Network topology",
          "User permissions"
        ],
        correctAnswer: 1,
        explanation: "Process trees show parent-child relationships, revealing how processes spawned each other - essential for understanding attack chains."
      },
      {
        id: "q7-3",
        question: "Which scenario is suspicious in a process tree?",
        options: [
          "Explorer launching Notepad",
          "Services.exe starting a Windows service",
          "Word or Excel spawning PowerShell or cmd.exe",
          "Chrome spawning Chrome processes"
        ],
        correctAnswer: 2,
        explanation: "Office applications (Word, Excel) spawning scripting engines (PowerShell, cmd) is a classic malware delivery indicator."
      },
      {
        id: "q7-4",
        question: "What type of EDR response action isolates a host?",
        options: [
          "Process termination",
          "User logout",
          "Network containment/isolation",
          "File deletion"
        ],
        correctAnswer: 2,
        explanation: "Network containment/isolation blocks all network traffic except EDR communication, containing the threat."
      },
      {
        id: "q7-5",
        question: "What does T1059.001 represent in MITRE ATT&CK?",
        options: [
          "PowerShell execution technique",
          "A ticket number",
          "A file hash",
          "A user account"
        ],
        correctAnswer: 0,
        explanation: "T1059.001 is the MITRE ATT&CK technique ID for PowerShell execution under the Command and Scripting Interpreter tactic."
      },
      {
        id: "q7-6",
        question: "What should you check when analyzing a suspicious process?",
        options: [
          "Just the timestamp",
          "Only the process name",
          "Command line arguments, parent process, file location, and network connections",
          "The user's email"
        ],
        correctAnswer: 2,
        explanation: "Analyze command line arguments, parent process legitimacy, file location, digital signature, and network connections."
      },
      {
        id: "q7-7",
        question: "What is a LOLBAS/LOLBIN?",
        options: [
          "A type of malware",
          "Legitimate system binaries abused for malicious purposes",
          "A security certification",
          "A logging format"
        ],
        correctAnswer: 1,
        explanation: "LOLBAS (Living Off The Land Binaries and Scripts) are legitimate system tools like certutil or mshta abused by attackers."
      },
      {
        id: "q7-8",
        question: "Which PowerShell flag combination is commonly used for evasion?",
        options: [
          "-Update",
          "-Help",
          "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass",
          "-Version"
        ],
        correctAnswer: 2,
        explanation: "These flags hide the window, bypass security policies, and avoid loading profiles - classic evasion techniques."
      },
      {
        id: "q7-9",
        question: "What does LSASS access typically indicate?",
        options: [
          "Normal Windows operation only",
          "Antivirus update",
          "Potential credential dumping attack",
          "System shutdown"
        ],
        correctAnswer: 2,
        explanation: "Unusual access to LSASS (Local Security Authority Subsystem Service) often indicates credential dumping like Mimikatz."
      },
      {
        id: "q7-10",
        question: "What telemetry type shows registry persistence?",
        options: [
          "Network telemetry",
          "Registry telemetry",
          "File telemetry only",
          "User telemetry"
        ],
        correctAnswer: 1,
        explanation: "Registry telemetry captures modifications to registry keys, including those used for persistence like Run keys."
      },
      {
        id: "q7-11",
        question: "What is the purpose of the EDR confidence score?",
        options: [
          "How likely the detection represents actual malicious activity",
          "Storage capacity",
          "User satisfaction rating",
          "Network speed measurement"
        ],
        correctAnswer: 0,
        explanation: "Confidence score indicates how likely the detection represents actual malicious activity based on the detection logic."
      },
      {
        id: "q7-12",
        question: "After containing a threat via EDR, what should you do?",
        options: [
          "Nothing - job is done",
          "Collect evidence and document the investigation",
          "Delete all logs",
          "Immediately reimage the system"
        ],
        correctAnswer: 1,
        explanation: "After containment, collect evidence (memory, files, logs), document your investigation, and coordinate further response."
      }
    ]
  },
  {
    quizId: "q8",
    courseId: "soc-fundamentals",
    title: "Network Security Quiz",
    description: "Test your knowledge of network security monitoring, IDS/IPS, and traffic analysis.",
    passingScore: 70,
    timeLimit: 25,
    questions: [
      {
        id: "q8-1",
        question: "What is the difference between IDS and IPS?",
        options: [
          "They are the same thing",
          "IDS only alerts; IPS can block traffic",
          "Neither can detect threats",
          "IPS only alerts; IDS can block traffic"
        ],
        correctAnswer: 1,
        explanation: "IDS (Detection System) monitors and alerts passively; IPS (Prevention System) sits inline and can actively block traffic."
      },
{
  id: "q8-2",
        question: "What port does SMB use?",
        options: [
          "80",
          "443",
          "445",
          "22"
        ],
        correctAnswer: 2,
        explanation: "SMB (Server Message Block) uses port 445 and is commonly used in lateral movement attacks."
      },
      {
        id: "q8-3",
        question: "What is beaconing in network traffic?",
        options: [
          "Normal web browsing",
          "File downloads",
          "Regular-interval callbacks from malware to C2 servers",
          "Email sending"
        ],
        correctAnswer: 2,
        explanation: "Beaconing is regular-interval communication from infected hosts to command and control servers, a key malware indicator."
      },
      {
        id: "q8-4",
        question: "What is DNS tunneling used for?",
        options: [
          "Data exfiltration or C2 communication via DNS queries",
          "Faster DNS resolution",
          "Improving network speed",
          "Email delivery"
        ],
        correctAnswer: 0,
        explanation: "DNS tunneling encodes data in DNS queries/responses to bypass security controls for exfiltration or C2 communication."
      },
      {
        id: "q8-5",
        question: "What does a high volume of NXDomain responses indicate?",
        options: [
          "Fast internet connection",
          "Excellent network health",
          "Normal DNS activity",
          "Potential DGA (Domain Generation Algorithm) malware"
        ],
        correctAnswer: 3,
        explanation: "High NXDomain (non-existent domain) responses may indicate DGA malware trying to reach algorithmically generated domains."
      },
      {
        id: "q8-6",
        question: "What is NetFlow used for?",
        options: [
          "Blocking malware",
          "Managing users",
          "Capturing connection metadata for traffic analysis",
          "Replacing firewalls"
        ],
        correctAnswer: 2,
        explanation: "NetFlow captures connection metadata (IPs, ports, bytes, timing) for traffic analysis without storing full packet content."
      },
      {
        id: "q8-7",
        question: "What network pattern indicates port scanning?",
        options: [
          "Email traffic",
          "Large file downloads",
          "Single source connecting to many destinations on multiple ports",
          "Normal web traffic"
        ],
        correctAnswer: 2,
        explanation: "Port scanning shows a single source systematically connecting to many targets across multiple ports for reconnaissance."
      },
      {
        id: "q8-8",
        question: "What is the purpose of network segmentation?",
        options: [
          "To limit lateral movement between zones",
          "To remove firewalls",
          "To slow down the network",
          "To increase attack surface"
        ],
        correctAnswer: 0,
        explanation: "Network segmentation limits lateral movement by separating network zones with access controls between them."
      },
      {
        id: "q8-9",
        question: "Which protocol is commonly abused for C2 because it's rarely blocked?",
        options: [
          "Telnet",
          "SMTP",
          "DNS or HTTPS",
          "FTP"
        ],
        correctAnswer: 2,
        explanation: "DNS and HTTPS are commonly abused for C2 because they're rarely blocked and can blend with legitimate traffic."
      },
      {
        id: "q8-10",
        question: "What does a SYN flood attack target?",
        options: [
          "Server resources by sending many SYN packets without completing handshakes",
          "User passwords",
          "DNS records",
          "Email servers only"
        ],
        correctAnswer: 0,
        explanation: "SYN flood attacks exhaust server resources by sending many SYN packets without completing TCP handshakes."
      },
      {
        id: "q8-11",
        question: "What is signature-based detection's main limitation?",
        options: [
          "It's too accurate",
          "It works too fast",
          "It cannot detect unknown or new attacks",
          "It's too cheap"
        ],
        correctAnswer: 2,
        explanation: "Signature-based detection only identifies known attacks with existing signatures; it cannot detect zero-day or novel attacks."
      },
      {
        id: "q8-12",
        question: "What should you check when investigating a suspicious external connection?",
        options: [
          "Only the destination IP",
          "The user's lunch schedule",
          "Just the timestamp",
          "IP reputation, domain age, traffic patterns, and related alerts"
        ],
        correctAnswer: 3,
        explanation: "Investigate IP/domain reputation, when it was registered, traffic patterns, related alerts, and whether it's expected behavior."
      },
      {
        id: "q8-13",
        question: "What is WMI commonly used for in lateral movement?",
        options: [
          "Remote process execution on Windows systems",
          "File compression",
          "Web browsing",
          "Email delivery"
        ],
        correctAnswer: 0,
        explanation: "WMI (Windows Management Instrumentation) is commonly abused for remote process execution during lateral movement."
      },
      {
        id: "q8-14",
        question: "Which port is used for RDP?",
        options: [
          "8080",
          "3389",
          "443",
          "22"
        ],
        correctAnswer: 1,
        explanation: "RDP (Remote Desktop Protocol) uses port 3389 and is frequently targeted for unauthorized remote access."
      },
      {
        id: "q8-15",
        question: "What indicates potential data exfiltration in network traffic?",
        options: [
          "Normal browsing patterns",
          "Inbound email traffic",
          "Software updates",
          "Large outbound transfers to unknown destinations, especially after hours"
        ],
        correctAnswer: 3,
        explanation: "Large outbound data transfers to unknown destinations, especially outside business hours, may indicate data exfiltration."
      }
    ]
  },
  {
    quizId: "q9",
    courseId: "soc-fundamentals",
    title: "SOC Best Practices Quiz",
    description: "Final assessment covering investigation skills, career development, and analyst wellness.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      {
        id: "q9-1",
        question: "What is the recommended investigation approach?",
        options: [
          "Guess and move on",
          "Observe, hypothesize, test, and conclude",
          "Only escalate everything",
          "Jump to conclusions immediately"
        ],
        correctAnswer: 1,
        explanation: "A systematic approach: observe the evidence, form hypotheses, test them with additional data, then conclude based on findings."
      },
      {
        id: "q9-2",
        question: "What is 'confirmation bias' in investigations?",
        options: [
          "Seeking only evidence that supports your initial theory",
          "Confirming alerts correctly",
          "A type of malware",
          "Good documentation practice"
        ],
        correctAnswer: 0,
        explanation: "Confirmation bias is seeking only evidence supporting your initial theory. Counter it by actively looking for contradicting data."
      },
      {
        id: "q9-3",
        question: "What is alert fatigue?",
        options: [
          "Decreased vigilance due to overwhelming alert volume",
          "Being tired at work",
          "Slow network connections",
          "A type of attack"
        ],
        correctAnswer: 0,
        explanation: "Alert fatigue occurs when analysts become desensitized to alerts due to high volumes, potentially missing real threats."
      },
      {
        id: "q9-4",
        question: "What is a key sign of analyst burnout?",
        options: [
          "Taking notes",
          "Chronic fatigue, cynicism, and decreased performance",
          "Asking many questions",
          "Excitement about work"
        ],
        correctAnswer: 1,
        explanation: "Burnout signs include chronic fatigue, cynicism about work, feeling ineffective, and decreased performance."
      },
      {
        id: "q9-5",
        question: "What is 'pivoting' in an investigation?",
        options: [
          "Changing careers",
          "Rotating your chair",
          "Moving from one indicator to discover related indicators",
          "Closing tickets"
        ],
        correctAnswer: 2,
        explanation: "Pivoting means using one indicator to find related ones - like finding domains that resolve to a suspicious IP."
      },
      {
        id: "q9-6",
        question: "What is the recommended certification for entry-level SOC analysts?",
        options: [
          "CISSP",
          "No certification needed",
          "CompTIA Security+ or BTL1",
          "PhD in Computer Science"
        ],
        correctAnswer: 2,
        explanation: "CompTIA Security+ or Blue Team Level 1 (BTL1) are excellent entry-level certifications for aspiring SOC analysts."
      },
      {
        id: "q9-7",
        question: "What should you do during work breaks?",
        options: [
          "Continue monitoring alerts",
          "Step away from screens and take actual breaks",
          "Skip breaks to handle more alerts",
          "Work on personal projects"
        ],
        correctAnswer: 1,
        explanation: "Taking actual breaks away from screens is essential for preventing burnout and maintaining effectiveness."
      },
      {
        id: "q9-8",
        question: "What makes good investigation notes?",
        options: [
          "Personal opinions only",
          "Only the final conclusion",
          "Brief with no details",
          "Timestamped entries with observations, actions, and reasoning"
        ],
        correctAnswer: 3,
        explanation: "Good notes include timestamps, detailed observations, actions taken, reasoning, and evidence references."
      },
      {
        id: "q9-9",
        question: "What is the typical L1 to L2 analyst progression timeline?",
        options: [
          "2-4 years",
          "10+ years",
          "1 week",
          "Never possible"
        ],
        correctAnswer: 0,
        explanation: "Typically, analysts progress from L1 to L2 over 2-4 years as they develop deeper investigation and response skills."
      },
      {
        id: "q9-10",
        question: "What is essential for continuous learning in cybersecurity?",
        options: [
          "Nothing - skills don't change",
          "Combination of hands-on practice, certifications, and staying current with threats",
          "Just reading news",
          "Only formal training"
        ],
        correctAnswer: 1,
        explanation: "Continuous learning requires hands-on practice, certifications, reading threat intel, and staying current with evolving threats."
      },
      {
        id: "q9-11",
        question: "Which platform provides free SOC analyst practice labs?",
        options: [
          "TryHackMe or LetsDefend",
          "Microsoft Word",
          "YouTube only",
          "Facebook"
        ],
        correctAnswer: 0,
        explanation: "TryHackMe and LetsDefend offer free (and paid) SOC analyst training paths with hands-on labs and challenges."
      },
      {
        id: "q9-12",
        question: "What should you do if you're experiencing burnout symptoms?",
        options: [
          "Quit immediately",
          "Ignore them and work harder",
          "Seek support from EAP, mental health professionals, or trusted colleagues",
          "Hide the symptoms"
        ],
        correctAnswer: 2,
        explanation: "Seeking support is a sign of strength. Use EAP programs, mental health resources, or trusted colleagues when needed."
      }
    ]
  },
  {
    quizId: "la-q1",
    courseId: "log-analysis",
    title: "Log Fundamentals Quiz",
    description: "Test your understanding of log basics, formats, and importance in security.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      {
        id: "la-q1-1",
        question: "What is the primary purpose of log files in IT systems?",
        options: [
          "To store user passwords securely",
          "To record events, activities, and system states for analysis",
          "To replace backup systems",
          "To slow down system performance"
        ],
        correctAnswer: 1,
        explanation: "Log files record events, activities, and system states, providing crucial information for troubleshooting, security analysis, and compliance."
      },
      {
        id: "la-q1-2",
        question: "Which log format uses key=value pairs for structured data?",
        options: [
          "XML",
          "JSON",
          "Key-Value (KV)",
          "CSV"
        ],
        correctAnswer: 2,
        explanation: "Key-Value format uses key=value pairs (e.g., user=admin action=login) making it easy to parse and search."
      },
      {
        id: "la-q1-3",
        question: "What does the term 'log rotation' refer to?",
        options: [
          "Automatically archiving old logs and creating new ones to manage disk space",
          "Spinning hard drives that store logs",
          "Changing log file permissions",
          "Rotating between different log formats"
        ],
        correctAnswer: 0,
        explanation: "Log rotation automatically archives old log files and creates new ones to prevent disk space exhaustion and maintain manageability."
      },
      {
        id: "la-q1-4",
        question: "Which timestamp format is considered the international standard for log files?",
        options: [
          "Unix epoch only",
          "MM/DD/YYYY",
          "ISO 8601 (YYYY-MM-DDTHH:MM:SS)",
          "DD-MM-YYYY"
        ],
        correctAnswer: 2,
        explanation: "ISO 8601 (YYYY-MM-DDTHH:MM:SS) is the international standard that provides unambiguous, sortable timestamps."
      },
      {
        id: "la-q1-5",
        question: "What is centralized log management?",
        options: [
          "Deleting logs after 24 hours",
          "Storing logs only on local machines",
          "Encrypting all log files",
          "Collecting logs from multiple sources into a single location for analysis"
        ],
        correctAnswer: 3,
        explanation: "Centralized log management collects logs from multiple sources into a single location, enabling correlation, analysis, and long-term retention."
      },
      {
        id: "la-q1-6",
        question: "Which log level indicates a serious problem that needs immediate attention?",
        options: [
          "ERROR/CRITICAL",
          "INFO",
          "WARNING",
          "DEBUG"
        ],
        correctAnswer: 0,
        explanation: "ERROR and CRITICAL levels indicate serious problems requiring immediate attention, while DEBUG and INFO are for routine information."
      },
      {
        id: "la-q1-7",
        question: "What is the main advantage of JSON-formatted logs?",
        options: [
          "They are structured and easily parsed by machines",
          "They cannot contain nested data",
          "They are human-readable only",
          "They are smaller in size"
        ],
        correctAnswer: 0,
        explanation: "JSON logs are structured, machine-parseable, and can contain nested data, making them ideal for automated analysis."
      },
      {
        id: "la-q1-8",
        question: "Why is consistent timestamping important in log analysis?",
        options: [
          "It's required by all operating systems",
          "It enables accurate event correlation across multiple systems",
          "It reduces storage requirements",
          "It makes logs look professional"
        ],
        correctAnswer: 1,
        explanation: "Consistent timestamps enable accurate event correlation across multiple systems, critical for incident investigation and timeline reconstruction."
      },
      {
        id: "la-q1-9",
        question: "What is a log aggregator?",
        options: [
          "A tool that collects and consolidates logs from multiple sources",
          "A type of malware",
          "A log encryption tool",
          "A tool that deletes logs"
        ],
        correctAnswer: 0,
        explanation: "A log aggregator collects and consolidates logs from multiple sources, making centralized analysis and searching possible."
      },
      {
        id: "la-q1-10",
        question: "Which of the following is NOT a common log source in enterprise environments?",
        options: [
          "Firewalls and IDS/IPS",
          "Authentication systems",
          "User personal diaries",
          "Web servers and applications"
        ],
        correctAnswer: 2,
        explanation: "Common enterprise log sources include firewalls, IDS/IPS, web servers, applications, and authentication systems - not personal documents."
      }
    ]
  },
  {
    quizId: "la-q2",
    courseId: "log-analysis",
    title: "Windows Log Analysis",
    description: "Master Windows Event Log analysis including Security, System, and Application logs.",
    passingScore: 70,
    timeLimit: 25,
    questions: [
      {
        id: "la-q2-1",
        question: "Which Windows Event ID indicates a successful user logon?",
        options: [
          "4625",
          "4624",
          "4634",
          "4648"
        ],
        correctAnswer: 1,
        explanation: "Event ID 4624 records successful logon events. 4625 is failed logon, 4634 is logoff, and 4648 is explicit credential logon."
      },
      {
        id: "la-q2-2",
        question: "What does Windows Event ID 4625 indicate?",
        options: [
          "Password change",
          "Successful logon",
          "Account lockout",
          "Failed logon attempt"
        ],
        correctAnswer: 3,
        explanation: "Event ID 4625 indicates a failed logon attempt, critical for detecting brute force attacks and unauthorized access attempts."
      },
      {
        id: "la-q2-3",
        question: "Which logon type value (in Event 4624) indicates interactive logon at the console?",
        options: [
          "Type 7",
          "Type 10",
          "Type 3",
          "Type 2"
        ],
        correctAnswer: 3,
        explanation: "Logon Type 2 is interactive logon at the console. Type 3 is network, Type 10 is RemoteInteractive (RDP), Type 7 is unlock."
      },
      {
        id: "la-q2-4",
        question: "What Windows Event ID should you monitor for new user account creation?",
        options: [
          "4624",
          "4672",
          "4720",
          "4688"
        ],
        correctAnswer: 2,
        explanation: "Event ID 4720 indicates a new user account was created. This is important for detecting unauthorized account creation."
      },
      {
        id: "la-q2-5",
        question: "Which Event ID indicates a process was created (process tracking)?",
        options: [
          "4625",
          "4624",
          "4688",
          "4720"
        ],
        correctAnswer: 2,
        explanation: "Event ID 4688 records process creation events, essential for tracking what programs are executed on a system."
      },
      {
        id: "la-q2-6",
        question: "What does Event ID 4672 indicate?",
        options: [
          "User logoff",
          "Account disabled",
          "Password reset",
          "Special privileges assigned to new logon"
        ],
        correctAnswer: 3,
        explanation: "Event ID 4672 indicates special privileges (like admin rights) were assigned to a new logon session."
      },
      {
        id: "la-q2-7",
        question: "Which Windows log stores security-related events like logons and audit events?",
        options: [
          "Application Log",
          "Security Log",
          "System Log",
          "Setup Log"
        ],
        correctAnswer: 1,
        explanation: "The Security Log stores security-related events including logons, logoffs, policy changes, and audit events."
      },
      {
        id: "la-q2-8",
        question: "What is the significance of multiple 4625 events followed by a 4624 from the same source?",
        options: [
          "Possible successful brute force attack",
          "Log corruption",
          "Normal user behavior",
          "System error"
        ],
        correctAnswer: 0,
        explanation: "Multiple failed logons (4625) followed by a successful logon (4624) from the same source may indicate a successful brute force attack."
      },
      {
        id: "la-q2-9",
        question: "Which Event ID indicates an account was added to a security-enabled group?",
        options: [
          "4728",
          "4720",
          "4624",
          "4625"
        ],
        correctAnswer: 0,
        explanation: "Event ID 4728 indicates a member was added to a security-enabled global group, important for privilege escalation detection."
      },
      {
        id: "la-q2-10",
        question: "What tool is commonly used to view Windows Event Logs?",
        options: [
          "Event Viewer",
          "Task Manager",
          "Device Manager",
          "Registry Editor"
        ],
        correctAnswer: 0,
        explanation: "Event Viewer (eventvwr.msc) is the built-in Windows tool for viewing and analyzing Windows Event Logs."
      },
      {
        id: "la-q2-11",
        question: "What does Logon Type 3 indicate in Windows Event 4624?",
        options: [
          "Remote Desktop logon",
          "Service account logon",
          "Local console logon",
          "Network logon (accessing shared folders)"
        ],
        correctAnswer: 3,
        explanation: "Logon Type 3 indicates network logon, typically when accessing shared folders, printers, or other network resources."
      },
      {
        id: "la-q2-12",
        question: "Which Event ID indicates Windows Defender detected malware?",
        options: [
          "4624",
          "7045",
          "4688",
          "1116"
        ],
        correctAnswer: 3,
        explanation: "Event ID 1116 in Microsoft-Windows-Windows Defender/Operational log indicates malware detection."
      }
    ]
  },
  {
    quizId: "la-q3",
    courseId: "log-analysis",
    title: "Linux & Network Log Analysis",
    description: "Analyze Linux system logs and network traffic patterns for security events.",
    passingScore: 70,
    timeLimit: 25,
    questions: [
      {
        id: "la-q3-1",
        question: "Where are authentication logs typically stored on Linux systems?",
        options: [
          "/var/log/syslog",
          "/var/log/messages",
          "/var/log/kern.log",
          "/var/log/auth.log or /var/log/secure"
        ],
        correctAnswer: 3,
        explanation: "Authentication logs are stored in /var/log/auth.log (Debian/Ubuntu) or /var/log/secure (RHEL/CentOS)."
      },
      {
        id: "la-q3-2",
        question: "Which Linux command displays the last logged in users?",
        options: [
          "ps",
          "who",
          "last",
          "top"
        ],
        correctAnswer: 2,
        explanation: "The 'last' command shows a list of last logged in users by reading from /var/log/wtmp."
      },
      {
        id: "la-q3-3",
        question: "What does the Linux log message 'Failed password for invalid user admin' indicate?",
        options: [
          "Password policy violation",
          "System error",
          "Successful admin login",
          "Login attempt for a non-existent user called 'admin'"
        ],
        correctAnswer: 3,
        explanation: "This message indicates someone tried to log in with username 'admin' which doesn't exist on the system - a common brute force indicator."
      },
      {
        id: "la-q3-4",
        question: "Which facility in syslog handles authentication messages?",
        options: [
          "auth/authpriv",
          "kern",
          "daemon",
          "mail"
        ],
        correctAnswer: 0,
        explanation: "The auth and authpriv facilities handle authentication and security-related messages in syslog."
      },
      {
        id: "la-q3-5",
        question: "What information is typically found in Apache access logs?",
        options: [
          "Database queries",
          "Server configuration",
          "Only error messages",
          "Client IP, timestamp, request method, URL, status code, user agent"
        ],
        correctAnswer: 3,
        explanation: "Apache access logs contain client IP, timestamp, HTTP method, requested URL, status code, size, and user agent."
      },
      {
        id: "la-q3-6",
        question: "Which HTTP status code in web logs indicates a successful request?",
        options: [
          "403",
          "200",
          "500",
          "404"
        ],
        correctAnswer: 1,
        explanation: "HTTP 200 indicates success. 404 is not found, 500 is server error, and 403 is forbidden."
      },
      {
        id: "la-q3-7",
        question: "What could multiple HTTP 404 errors from the same IP suggest?",
        options: [
          "Normal browsing",
          "Directory enumeration or scanning activity",
          "Successful file downloads",
          "Server overload"
        ],
        correctAnswer: 1,
        explanation: "Multiple 404 errors from one IP may indicate directory enumeration, vulnerability scanning, or reconnaissance activity."
      },
      {
        id: "la-q3-8",
        question: "In firewall logs, what does 'DENY' or 'DROP' indicate?",
        options: [
          "Firewall is offline",
          "Traffic was blocked by firewall rules",
          "Traffic was allowed",
          "Connection was successful"
        ],
        correctAnswer: 1,
        explanation: "DENY or DROP in firewall logs indicates the traffic was blocked according to firewall rules."
      },
      {
        id: "la-q3-9",
        question: "Which command would you use to follow a Linux log file in real-time?",
        options: [
          "less /var/log/auth.log",
          "tail -f /var/log/auth.log",
          "cat /var/log/auth.log",
          "head /var/log/auth.log"
        ],
        correctAnswer: 1,
        explanation: "The 'tail -f' command follows a file in real-time, showing new entries as they're written."
      },
      {
        id: "la-q3-10",
        question: "What does a sudden spike in DNS queries to unusual domains suggest?",
        options: [
          "Normal network activity",
          "Possible malware communication or data exfiltration",
          "Improved network performance",
          "DNS server upgrade"
        ],
        correctAnswer: 1,
        explanation: "Unusual DNS query patterns may indicate malware C2 communication, DNS tunneling, or data exfiltration attempts."
      },
      {
        id: "la-q3-11",
        question: "Which Linux log file contains kernel messages?",
        options: [
          "/var/log/apache2/access.log",
          "/var/log/mail.log",
          "/var/log/auth.log",
          "/var/log/kern.log or dmesg"
        ],
        correctAnswer: 3,
        explanation: "Kernel messages are stored in /var/log/kern.log and can be viewed with the 'dmesg' command."
      },
      {
        id: "la-q3-12",
        question: "What would you investigate if you see 'Accepted publickey for root' in auth.log?",
        options: [
          "Disable SSH immediately",
          "Nothing, this is normal",
          "Increase logging verbosity",
          "Verify the SSH key is authorized and the source IP is legitimate"
        ],
        correctAnswer: 3,
        explanation: "Root SSH access via public key should be verified - ensure the key is authorized and the source IP is expected and legitimate."
      }
    ]
  },
    {
    quizId: "la-q4",
    courseId: "log-analysis",
    title: "Attack Pattern Recognition",
    description: "Identify and analyze common attack patterns in log data.",
    passingScore: 70,
    timeLimit: 30,
    questions: [
{
        id: "la-q4-1",
        question: "What log pattern indicates a potential brute force attack?",
        options: [
          "Successful logins from multiple locations",
          "Single failed login followed by success",
          "Regular password changes",
          "Multiple failed login attempts from the same source in rapid succession"
        ],
        correctAnswer: 3,
        explanation: "Brute force attacks show multiple rapid failed login attempts from the same source, often targeting the same or multiple accounts."
      },
{
        id: "la-q4-2",
        question: "Which web log pattern might indicate SQL injection attempts?",
        options: [
          "Requests containing 'SELECT', 'UNION', 'OR 1=1', or encoded SQL syntax",
          "Static file requests",
          "Empty user-agent strings",
          "Normal page requests"
        ],
        correctAnswer: 0,
        explanation: "SQL injection attempts often contain SQL keywords like SELECT, UNION, OR 1=1, and encoded variations in URL parameters."
      },
{
        id: "la-q4-3",
        question: "What does 'password spraying' look like in logs?",
        options: [
          "Normal authentication patterns",
          "Few common passwords tried across many accounts",
          "Account lockouts on all accounts",
          "Millions of attempts on one account"
        ],
        correctAnswer: 1,
        explanation: "Password spraying shows few attempts per account but across many accounts, often avoiding lockout thresholds."
      },
{
        id: "la-q4-4",
        question: "Which pattern suggests directory traversal attack attempts?",
        options: [
          "Normal file paths",
          "HTTPS requests",
          "Paths containing '../' or '..\\' sequences",
          "Large file uploads"
        ],
        correctAnswer: 2,
        explanation: "Directory traversal attempts contain '../' or '..\\' sequences trying to access files outside the web root."
      },
{
        id: "la-q4-5",
        question: "What might multiple 'net user' commands in Windows logs indicate?",
        options: [
          "Normal IT operations",
          "User enumeration or reconnaissance by an attacker",
          "System updates",
          "Antivirus activity"
        ],
        correctAnswer: 1,
        explanation: "Multiple 'net user' commands might indicate an attacker enumerating users for privilege escalation or lateral movement."
      },
{
        id: "la-q4-6",
        question: "Which log entry pattern suggests potential data exfiltration?",
        options: [
          "Inbound email traffic",
          "Normal web browsing",
          "Large outbound data transfers, especially to unusual destinations",
          "Software updates"
        ],
        correctAnswer: 2,
        explanation: "Data exfiltration often shows as large outbound transfers to unusual IPs, cloud storage, or during off-hours."
      },
{
        id: "la-q4-7",
        question: "What does a 'golden ticket' attack look like in Kerberos logs?",
        options: [
          "TGS requests without corresponding TGT requests, or tickets with very long lifetimes",
          "Password reset requests",
          "Normal ticket requests",
          "Account lockouts"
        ],
        correctAnswer: 0,
        explanation: "Golden ticket attacks may show TGS requests without AS-REQ, unusual ticket lifetimes, or tickets for non-existent users."
      },
{
        id: "la-q4-8",
        question: "Which pattern indicates potential web shell activity?",
        options: [
          "Regular web page requests",
          "CSS file requests",
          "Image file requests",
          "POST requests to unusual files with command-like parameters"
        ],
        correctAnswer: 3,
        explanation: "Web shells often show as POST requests to unusual file paths (like .php files in unexpected locations) with command parameters."
      },
{
        id: "la-q4-9",
        question: "What might 'scheduled task created' events combined with persistence mechanisms indicate?",
        options: [
          "Normal system administration",
          "Routine maintenance",
          "User preference changes",
          "Potential malware establishing persistence"
        ],
        correctAnswer: 3,
        explanation: "Attackers often create scheduled tasks for persistence. Combined with suspicious executables, this indicates compromise."
      },
{
        id: "la-q4-10",
        question: "Which log pattern suggests Pass-the-Hash attacks?",
        options: [
          "Kerberos ticket requests",
          "Password changes",
          "NTLM authentication without prior password entry, especially Type 3 logons",
          "Normal interactive logons"
        ],
        correctAnswer: 2,
        explanation: "Pass-the-Hash attacks show NTLM authentications using stolen hashes, often appearing as Type 3 network logons without interactive login."
      },
{
        id: "la-q4-11",
        question: "What does PowerShell downloading and executing code in logs suggest?",
        options: [
          "System updates",
          "Normal scripting",
          "Scheduled maintenance",
          "Potential 'living off the land' attack technique"
        ],
        correctAnswer: 3,
        explanation: "PowerShell downloading and executing code (DownloadString, IEX) is a common 'living off the land' technique used by attackers."
      },
{
        id: "la-q4-12",
        question: "Which indicator in proxy logs might reveal C2 communication?",
        options: [
          "Social media access",
          "Beaconing patterns - regular, timed connections to the same domain",
          "Large file downloads",
          "Regular HTTP GET requests"
        ],
        correctAnswer: 1,
        explanation: "C2 beaconing shows regular, timed connections (e.g., every 60 seconds) to specific domains, often with similar payload sizes."
      }
    ]
  },
  {
    quizId: "la-q5",
    courseId: "log-analysis",
    title: "Final Certification Exam",
    description: "Comprehensive exam covering all log analysis modules. Required for certification.",
    passingScore: 80,
    timeLimit: 45,
    questions: [
{
        id: "la-q5-1",
        question: "Which Linux command is best for searching text patterns in log files?",
        options: [
          "cd",
          "ls",
          "grep",
          "mkdir"
        ],
        correctAnswer: 2,
        explanation: "The 'grep' command is essential for searching text patterns in files. It supports regex for complex pattern matching."
      },
{
        id: "la-q5-2",
        question: "What does the command 'grep -i \"failed\" /var/log/auth.log' do?",
        options: [
          "Deletes lines containing 'failed'",
          "Searches case-insensitively for 'failed' in auth.log",
          "Creates a file called 'failed'",
          "Counts the lines in auth.log"
        ],
        correctAnswer: 1,
        explanation: "grep -i performs a case-insensitive search for the pattern 'failed' in the auth.log file."
      },
{
        id: "la-q5-3",
        question: "Which command would count the number of failed SSH attempts?",
        options: [
          "head /var/log/auth.log",
          "tail /var/log/auth.log",
          "grep -c 'Failed password' /var/log/auth.log",
          "cat /var/log/auth.log"
        ],
        correctAnswer: 2,
        explanation: "grep -c counts the number of lines matching the pattern. This counts how many failed password entries exist."
      },
{
        id: "la-q5-4",
        question: "What is the purpose of log normalization?",
        options: [
          "To delete old logs",
          "To encrypt log files",
          "To convert different log formats into a consistent, standard format",
          "To compress log storage"
        ],
        correctAnswer: 2,
        explanation: "Log normalization converts diverse log formats into a consistent structure, enabling correlation and unified analysis."
      },
{
        id: "la-q5-5",
        question: "Why is establishing a baseline important in log analysis?",
        options: [
          "To increase storage space",
          "To encrypt sensitive data",
          "To understand normal behavior so anomalies can be detected",
          "To delete old logs automatically"
        ],
        correctAnswer: 2,
        explanation: "Baselines define normal behavior patterns. Deviations from baselines help identify anomalies and potential security incidents."
      },
{
        id: "la-q5-6",
        question: "What command combines 'sort' and 'uniq -c' for log analysis?",
        options: [
          "Encrypts the output",
          "Compresses the file",
          "Deletes duplicate lines",
          "Counts unique occurrences of sorted lines"
        ],
        correctAnswer: 3,
        explanation: "Piping through 'sort | uniq -c' sorts lines and counts unique occurrences - useful for finding top talkers or common events."
      },
{
        id: "la-q5-7",
        question: "What is log correlation?",
        options: [
          "Connecting events from multiple sources to identify patterns",
          "Compressing log files",
          "Copying logs to backup",
          "Deleting related logs"
        ],
        correctAnswer: 0,
        explanation: "Log correlation connects events from multiple sources to identify relationships, patterns, and reconstruct attack timelines."
      },
{
        id: "la-q5-8",
        question: "Which regex pattern would match an IPv4 address?",
        options: [
          "[a-z]+",
          "[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}",
          "[A-Z]*",
          "\\s+"
        ],
        correctAnswer: 1,
        explanation: "The pattern [0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3} matches IPv4 addresses (groups of 1-3 digits separated by dots)."
      },
{
        id: "la-q5-9",
        question: "What should be included in a log analysis report?",
        options: [
          "Raw logs only",
          "System specifications",
          "Only the analyst's name",
          "Executive summary, timeline, findings, evidence, and recommendations"
        ],
        correctAnswer: 3,
        explanation: "A complete log analysis report includes executive summary, timeline of events, detailed findings, evidence, and actionable recommendations."
      },
{
        id: "la-q5-10",
        question: "What is the 'awk' command commonly used for in log analysis?",
        options: [
          "File encryption",
          "Text processing and extracting specific fields from structured data",
          "Network scanning",
          "Compressing files"
        ],
        correctAnswer: 1,
        explanation: "awk is powerful for text processing, particularly extracting and manipulating specific fields from structured log data."
      },
{
        id: "la-q5-11",
        question: "Why should log analysis findings be documented with timestamps?",
        options: [
          "For aesthetic purposes",
          "To establish timeline accuracy and enable recreation of events",
          "For alphabetical ordering",
          "To increase file size"
        ],
        correctAnswer: 1,
        explanation: "Timestamps establish timeline accuracy, enable event recreation, and provide audit trails for incident response and legal proceedings."
      },
{
        id: "la-q5-12",
        question: "What is the benefit of using a SIEM for log analysis?",
        options: [
          "It replaces all other security tools",
          "It eliminates the need for analysts",
          "It provides centralized collection, correlation, alerting, and visualization",
          "It automatically fixes security issues"
        ],
        correctAnswer: 2,
        explanation: "SIEMs provide centralized log collection, real-time correlation, alerting, dashboards, and long-term storage for efficient analysis."
      }
    ]
  },
  {
    quizId: "siem-q1",
    courseId: "siem-fundamentals",
    title: "SIEM Fundamentals Quiz",
    description: "Test your understanding of SIEM architecture, components, and basic concepts.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
{
        id: "siem-q1-1",
        question: "What does SIEM stand for?",
        options: [
          "System Integration and Endpoint Management",
          "Secure Infrastructure and Event Mapping",
          "Security Intelligence and Event Monitoring",
          "Security Information and Event Management"
        ],
        correctAnswer: 3,
        explanation: "SIEM stands for Security Information and Event Management — a platform that combines log aggregation, real-time monitoring, correlation, and alerting."
      },
{
        id: "siem-q1-2",
        question: "Which component of a SIEM is responsible for collecting and forwarding log data?",
        options: [
          "Search Head",
          "Forwarder / Data Collector",
          "Dashboard Engine",
          "Indexer"
        ],
        correctAnswer: 1,
        explanation: "Forwarders (or data collectors/agents) are deployed on endpoints and network devices to collect and send log data to the SIEM for processing."
      },
{
        id: "siem-q1-3",
        question: "What is the primary purpose of a SIEM in a SOC?",
        options: [
          "Automate patch management",
          "Manage employee access permissions",
          "Centralize log collection, correlation, and alerting for threat detection",
          "Replace all other security tools"
        ],
        correctAnswer: 2,
        explanation: "A SIEM centralizes log data from across the environment, correlates events, and generates alerts to help SOC analysts detect and respond to threats."
      },
{
        id: "siem-q1-4",
        question: "Which SIEM platform uses SPL (Search Processing Language)?",
        options: [
          "Microsoft Sentinel",
          "Elastic SIEM",
          "Splunk",
          "IBM QRadar"
        ],
        correctAnswer: 2,
        explanation: "Splunk uses SPL (Search Processing Language) as its query language for searching, filtering, and analyzing data."
      },
{
        id: "siem-q1-5",
        question: "What query language does Microsoft Sentinel use?",
        options: [
          "SQL",
          "KQL (Kusto Query Language)",
          "AQL",
          "SPL"
        ],
        correctAnswer: 1,
        explanation: "Microsoft Sentinel uses KQL (Kusto Query Language) for querying data stored in Azure Log Analytics workspaces."
      },
{
        id: "siem-q1-6",
        question: "What is the role of an indexer in a SIEM?",
        options: [
          "Sending alerts to analysts",
          "Displaying dashboards",
          "Processing, indexing, and storing incoming data for fast searching",
          "Collecting logs from endpoints"
        ],
        correctAnswer: 2,
        explanation: "The indexer receives data from forwarders, parses it, creates indexes for efficient searching, and stores it according to retention policies."
      },
{
        id: "siem-q1-7",
        question: "Which of the following is NOT a common SIEM use case?",
        options: [
          "Incident investigation and forensics",
          "Application development",
          "Threat detection and alerting",
          "Compliance reporting"
        ],
        correctAnswer: 1,
        explanation: "Application development is not a SIEM use case. SIEMs are used for threat detection, compliance, incident response, and forensic investigations."
      },
{
        id: "siem-q1-8",
        question: "What does 'correlation' mean in SIEM context?",
        options: [
          "Deleting duplicate logs",
          "Sending logs to a backup server",
          "Compressing log files",
          "Linking related events from different sources to identify patterns or attacks"
        ],
        correctAnswer: 3,
        explanation: "Correlation links related events from multiple data sources to identify attack patterns, suspicious behaviors, or security incidents."
      },
{
        id: "siem-q1-9",
        question: "Which SIEM platform is cloud-native and built on Azure?",
        options: [
          "ArcSight",
          "IBM QRadar",
          "Splunk Enterprise",
          "Microsoft Sentinel"
        ],
        correctAnswer: 3,
        explanation: "Microsoft Sentinel is a cloud-native SIEM built on Azure, offering scalable log analytics, threat intelligence, and SOAR capabilities."
      },
{
        id: "siem-q1-10",
        question: "What is EPS in SIEM licensing?",
        options: [
          "Encrypted Protocol Standard",
          "External Processing Server",
          "Events Per Second — a measure of data ingestion rate",
          "Endpoint Protection Suite"
        ],
        correctAnswer: 2,
        explanation: "EPS (Events Per Second) measures the rate of data ingestion and is commonly used in SIEM licensing models to determine capacity and cost."
      },
{
        id: "siem-q1-11",
        question: "What is the search head responsible for in Splunk's architecture?",
        options: [
          "Processing search queries and presenting results to users",
          "Forwarding data between indexers",
          "Storing raw data",
          "Collecting logs from endpoints"
        ],
        correctAnswer: 0,
        explanation: "The search head handles search requests from users, distributes them to indexers, merges results, and presents them through the UI."
      },
{
        id: "siem-q1-12",
        question: "Which query language does IBM QRadar use?",
        options: [
          "AQL (Ariel Query Language)",
          "SPL",
          "KQL",
          "Lucene"
        ],
        correctAnswer: 0,
        explanation: "IBM QRadar uses AQL (Ariel Query Language), a SQL-like language for querying its Ariel database of security events and flows."
      },
{
        id: "siem-q1-13",
        question: "What advantage does a cloud-native SIEM offer over on-premises?",
        options: [
          "Elastic scalability and reduced infrastructure management",
          "No internet required",
          "Lower data quality",
          "Faster local network speeds"
        ],
        correctAnswer: 0,
        explanation: "Cloud-native SIEMs offer elastic scalability, reduced infrastructure overhead, automatic updates, and pay-as-you-go pricing models."
      },
{
        id: "siem-q1-14",
        question: "What is 'log normalization'?",
        options: [
          "Encrypting log data",
          "Backing up logs to tape",
          "Deleting old logs",
          "Converting logs from different sources into a common format"
        ],
        correctAnswer: 3,
        explanation: "Log normalization converts logs from various formats and sources into a standardized schema so they can be consistently searched and correlated."
      },
{
        id: "siem-q1-15",
        question: "Which open-source search engine powers Elastic SIEM?",
        options: [
          "Redis",
          "Elasticsearch",
          "Apache Solr",
          "MongoDB"
        ],
        correctAnswer: 1,
        explanation: "Elastic SIEM is built on Elasticsearch, an open-source distributed search and analytics engine optimized for log and event data."
      }
    ]
  },
  {
    quizId: "siem-q2",
    courseId: "siem-fundamentals",
    title: "Data Ingestion Assessment",
    description: "Evaluate your knowledge of log collection, normalization, and data management.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
{
        id: "siem-q2-1",
        question: "What is the difference between agent-based and agentless log collection?",
        options: [
          "Agent-based only works on Windows",
          "Agent-based installs software on the source; agentless pulls data remotely via protocols like Syslog or WMI",
          "Agentless is always more reliable",
          "There is no difference"
        ],
        correctAnswer: 1,
        explanation: "Agent-based collection installs a lightweight forwarder on the source system, while agentless collection uses protocols like Syslog, WMI, or APIs to pull data remotely."
      },
{
        id: "siem-q2-2",
        question: "What port does Syslog traditionally use?",
        options: [
          "UDP 161",
          "TCP 80",
          "TCP 443",
          "UDP 514"
        ],
        correctAnswer: 3,
        explanation: "Syslog traditionally uses UDP port 514 for sending log messages. Modern implementations often use TCP 514 or TCP 6514 (with TLS) for reliability."
      },
{
        id: "siem-q2-3",
        question: "What is field extraction in SIEM data processing?",
        options: [
          "Parsing raw log data to identify and label specific data elements like IP, username, and action",
          "Encrypting sensitive fields",
          "Deleting unnecessary fields from logs",
          "Exporting fields to a spreadsheet"
        ],
        correctAnswer: 0,
        explanation: "Field extraction parses raw log data to identify and label key data elements like IP addresses, usernames, timestamps, and actions for structured searching."
      },
{
        id: "siem-q2-4",
        question: "What is a 'source type' in Splunk?",
        options: [
          "A category that defines the format and parsing rules for incoming data",
          "The physical server generating logs",
          "The user who created the search",
          "A type of dashboard"
        ],
        correctAnswer: 0,
        explanation: "A source type in Splunk categorizes data by format, telling Splunk how to parse and extract fields from that specific log type."
      },
{
        id: "siem-q2-5",
        question: "What is 'hot/warm/cold' storage in SIEM data management?",
        options: [
          "Tiered storage where recent data is fast-access and older data moves to slower, cheaper storage",
          "Types of encryption",
          "Temperature monitoring of servers",
          "Network speed tiers"
        ],
        correctAnswer: 0,
        explanation: "Hot/warm/cold storage tiers balance performance and cost: hot for recent, frequently accessed data; warm for less frequent; cold for archival and compliance."
      },
{
        id: "siem-q2-6",
        question: "Why is timestamp normalization important in SIEM?",
        options: [
          "It ensures events from different time zones can be accurately correlated chronologically",
          "It makes logs look prettier",
          "It reduces storage costs",
          "It speeds up network traffic"
        ],
        correctAnswer: 0,
        explanation: "Timestamp normalization ensures events from systems in different time zones are aligned to a common reference (usually UTC) for accurate correlation."
      },
{
        id: "siem-q2-7",
        question: "What is a Universal Forwarder in Splunk?",
        options: [
          "A full Splunk instance on every endpoint",
          "A type of dashboard",
          "A cloud-based storage service",
          "A lightweight agent that collects and forwards data to indexers with minimal resource usage"
        ],
        correctAnswer: 3,
        explanation: "A Universal Forwarder is a lightweight Splunk agent designed to collect and forward data to indexers while consuming minimal CPU and memory."
      },
{
        id: "siem-q2-8",
        question: "What does CEF stand for in log formatting?",
        options: [
          "Central Event Filter",
          "Centralized Extraction Function",
          "Common Event Format",
          "Common Encryption Framework"
        ],
        correctAnswer: 2,
        explanation: "CEF (Common Event Format) is a standardized log format developed by ArcSight that provides a common structure for security event data across vendors."
      },
{
        id: "siem-q2-9",
        question: "Which data collection method is best for cloud services like AWS or Azure?",
        options: [
          "Physical serial connection",
          "Syslog over UDP",
          "API-based integration",
          "Manual log upload"
        ],
        correctAnswer: 2,
        explanation: "API-based integration is ideal for cloud services, using REST APIs to pull logs from platforms like AWS CloudTrail, Azure Activity Logs, or Office 365."
      },
{
        id: "siem-q2-10",
        question: "What is data enrichment in SIEM?",
        options: [
          "Converting data to JSON format",
          "Adding context to events such as geolocation, threat intelligence, or asset information",
          "Compressing data for storage",
          "Deleting duplicate events"
        ],
        correctAnswer: 1,
        explanation: "Data enrichment adds contextual information to raw events — like geolocation for IPs, threat intel scores, or asset criticality — improving analysis."
      },
{
        id: "siem-q2-11",
        question: "What is the purpose of data retention policies in SIEM?",
        options: [
          "To encrypt stored data",
          "To delete data immediately after collection",
          "To define how long different types of data are stored based on compliance and operational needs",
          "To keep all data forever"
        ],
        correctAnswer: 2,
        explanation: "Retention policies define storage durations for different data types, balancing compliance requirements, operational needs, and storage costs."
      },
{
        id: "siem-q2-12",
        question: "What protocol provides reliable, encrypted syslog delivery?",
        options: [
          "Syslog over TLS (TCP 6514)",
          "SNMP",
          "UDP Syslog",
          "FTP"
        ],
        correctAnswer: 0,
        explanation: "Syslog over TLS (typically on TCP port 6514) provides both reliable delivery (TCP) and encryption (TLS) for secure log transmission."
      },
{
        id: "siem-q2-13",
        question: "What is an index in SIEM data storage?",
        options: [
          "A table of contents for documentation",
          "A structured repository where processed and searchable event data is stored",
          "A list of all SIEM users",
          "A backup location"
        ],
        correctAnswer: 1,
        explanation: "An index is a structured data store within the SIEM where processed events are organized and optimized for fast searching and retrieval."
      },
{
        id: "siem-q2-14",
        question: "What happens if logs arrive at the SIEM with incorrect timestamps?",
        options: [
          "Logs are automatically deleted",
          "The SIEM automatically corrects all timestamps",
          "Nothing — the SIEM ignores timestamps",
          "Events may be placed out of order, making correlation and investigation inaccurate"
        ],
        correctAnswer: 3,
        explanation: "Incorrect timestamps cause events to appear in the wrong order, breaking correlation rules and making incident timelines unreliable."
      },
{
        id: "siem-q2-15",
        question: "What is 'parsing' in the context of SIEM data ingestion?",
        options: [
          "Deleting malformed logs",
          "Breaking raw log data into structured fields that can be searched and analyzed",
          "Compressing log files",
          "Sending data to a backup server"
        ],
        correctAnswer: 1,
        explanation: "Parsing breaks raw, unstructured log data into structured, labeled fields (timestamp, source IP, action, etc.) for efficient querying."
      }
    ]
  },
  {
    quizId: "siem-q3",
    courseId: "siem-fundamentals",
    title: "Search & Query Mastery",
    description: "Practical quiz on writing SIEM queries and search techniques.",
    passingScore: 75,
    timeLimit: 25,
    questions: [
{
        id: "siem-q3-1",
        question: "In SPL, what does the 'stats count by src_ip' command do?",
        options: [
          "Counts the number of events for each unique source IP address",
          "Sorts events alphabetically by source IP",
          "Filters out all source IP fields",
          "Deletes events grouped by source IP"
        ],
        correctAnswer: 0,
        explanation: "The 'stats count by src_ip' command aggregates events, counting how many occurrences exist for each unique source IP address."
      },
{
        id: "siem-q3-2",
        question: "What does the wildcard character '*' do in a SIEM search?",
        options: [
          "Exports results to CSV",
          "Marks results as favorites",
          "Deletes all matching results",
          "Matches zero or more characters in a search term"
        ],
        correctAnswer: 3,
        explanation: "The wildcard '*' matches zero or more characters, enabling partial matching. For example, 'fail*' matches 'failed', 'failure', 'failing', etc."
      },
{
        id: "siem-q3-3",
        question: "In KQL, what does '| where TimeGenerated > ago(1h)' do?",
        options: [
          "Filters results to events from the last 1 hour",
          "Groups events by hour",
          "Deletes events older than 1 hour",
          "Shows events from more than 1 hour ago only"
        ],
        correctAnswer: 0,
        explanation: "The 'where TimeGenerated > ago(1h)' filter returns only events generated within the last hour."
      },
{
        id: "siem-q3-4",
        question: "What is the purpose of the 'table' command in SPL?",
        options: [
          "Displays only the specified fields in a tabular format",
          "Creates a database table",
          "Joins two data sources",
          "Sorts data into tables by time"
        ],
        correctAnswer: 0,
        explanation: "The 'table' command in SPL displays results showing only the specified fields in a clean tabular format."
      },
{
        id: "siem-q3-5",
        question: "How do you search for an exact phrase in most SIEM platforms?",
        options: [
          "Using parentheses: (exact phrase)",
          "Using double quotes: \"exact phrase\"",
          "Using brackets: [exact phrase]",
          "Using asterisks: *exact phrase*"
        ],
        correctAnswer: 1,
        explanation: "Double quotes are used across most SIEM platforms to search for exact phrases, ensuring the words appear together in that order."
      },
{
        id: "siem-q3-6",
        question: "What does the SPL command 'dedup src_ip' do?",
        options: [
          "Removes duplicate events, keeping only the first occurrence per unique source IP",
          "Counts duplicate IPs",
          "Sorts IPs in descending order",
          "Duplicates all source IP events"
        ],
        correctAnswer: 0,
        explanation: "The 'dedup' command removes duplicate events based on the specified field, keeping only the first occurrence of each unique value."
      },
{
        id: "siem-q3-7",
        question: "In KQL, what does the 'summarize' operator do?",
        options: [
          "Summarizes the SIEM configuration",
          "Aggregates data using functions like count(), avg(), sum() grouped by specified fields",
          "Displays a text summary of the query",
          "Compresses query results"
        ],
        correctAnswer: 1,
        explanation: "The 'summarize' operator in KQL performs aggregation, similar to SQL's GROUP BY."
      },
{
        id: "siem-q3-8",
        question: "What is the Boolean operator to exclude results in SIEM searches?",
        options: [
          "AND",
          "OR",
          "NOT",
          "XOR"
        ],
        correctAnswer: 2,
        explanation: "The NOT operator excludes matching results from the search."
      },
{
        id: "siem-q3-9",
        question: "What does 'earliest=-24h latest=now' specify in a Splunk search?",
        options: [
          "Schedule a search to run every 24 hours",
          "Delete data from the last 24 hours",
          "Limit results to 24 entries",
          "The time range for the search: from 24 hours ago to the current time"
        ],
        correctAnswer: 3,
        explanation: "These time modifiers set the search window from 24 hours ago to the present moment."
      },
{
        id: "siem-q3-10",
        question: "What is the pipe character '|' used for in SIEM queries?",
        options: [
          "Separating field names from values",
          "Indicating a comment in the query",
          "Chaining commands, sending the output of one command as input to the next",
          "Marking the end of a query"
        ],
        correctAnswer: 2,
        explanation: "The pipe '|' chains commands together in a pipeline, where each command processes the output of the previous one."
      },
{
        id: "siem-q3-11",
        question: "How would you search for failed login attempts from a specific subnet in SPL?",
        options: [
          "search failed AND login AND src_ip LIKE 192.168.1",
          "Both A and C are valid approaches",
          "failed login src_ip=192.168.1.*",
          "index=security action=failure src_ip=192.168.1.0/24"
        ],
        correctAnswer: 1,
        explanation: "Both wildcard matching (192.168.1.*) and CIDR notation (192.168.1.0/24) are valid approaches in SPL to search within a subnet."
      },
{
        id: "siem-q3-12",
        question: "What does 'head 10' do in a SIEM query?",
        options: [
          "Creates 10 copies of each event",
          "Shows the first 10 results from the search",
          "Runs the search 10 times",
          "Deletes the top 10 events"
        ],
        correctAnswer: 1,
        explanation: "The 'head' command limits output to the first N results, useful for quickly viewing the most relevant events."
      },
{
        id: "siem-q3-13",
        question: "In KQL, what does 'project' do?",
        options: [
          "Projects future trends",
          "Creates a new project in Sentinel",
          "Selects specific columns to display in the output",
          "Archives the query"
        ],
        correctAnswer: 2,
        explanation: "The 'project' operator in KQL selects which columns to include in the output, similar to SELECT in SQL."
      },
{
        id: "siem-q3-14",
        question: "What is a subsearch (or subquery) in SIEM?",
        options: [
          "A backup copy of a search",
          "A search performed by a subordinate analyst",
          "A nested search whose results feed into the outer/main search",
          "A search that runs below the main search bar"
        ],
        correctAnswer: 2,
        explanation: "A subsearch is a nested query that executes first, and its results are used as input for the outer search."
      },
{
        id: "siem-q3-15",
        question: "What does the 'sort' command do in SPL?",
        options: [
          "Counts sorted fields",
          "Removes sorted data",
          "Groups similar events together",
          "Orders results by specified fields in ascending or descending order"
        ],
        correctAnswer: 3,
        explanation: "The 'sort' command orders results by one or more fields. Use '-' prefix for descending order."
      },
{
        id: "siem-q3-16",
        question: "How do you use a lookup table in Splunk?",
        options: [
          "By manually typing reference data",
          "By importing a CSV file into the dashboard",
          "Using the 'lookup' command to enrich events with data from an external table",
          "Lookups are not supported in Splunk"
        ],
        correctAnswer: 2,
        explanation: "The 'lookup' command enriches search results by matching field values against an external lookup table."
      },
{
        id: "siem-q3-17",
        question: "What is the 'transaction' command used for in SPL?",
        options: [
          "Creating database transactions",
          "Grouping related events into single transactions based on shared fields and time proximity",
          "Processing financial transactions",
          "Logging purchase orders"
        ],
        correctAnswer: 1,
        explanation: "The 'transaction' command groups related events into single transactions based on shared fields and time windows."
      },
{
        id: "siem-q3-18",
        question: "What is the advantage of using 'tstats' over regular 'stats' in Splunk?",
        options: [
          "tstats works only in cloud deployments",
          "tstats is significantly faster because it searches indexed metadata rather than raw events",
          "There is no advantage",
          "tstats provides more accurate results"
        ],
        correctAnswer: 1,
        explanation: "tstats queries indexed metadata (tsidx files) rather than raw events, making it significantly faster for large datasets."
      },
{
        id: "siem-q3-19",
        question: "In KQL, what does 'extend' do?",
        options: [
          "Creates a new calculated column based on an expression",
          "Extends the query timeout",
          "Increases the result limit",
          "Extends the data retention period"
        ],
        correctAnswer: 0,
        explanation: "The 'extend' operator in KQL creates new calculated columns based on expressions."
      },
{
        id: "siem-q3-20",
        question: "What is the best practice for optimizing SIEM search performance?",
        options: [
          "Avoid using the pipe character",
          "Use the narrowest time range, specific indexes, and filter early in the search pipeline",
          "Use only wildcard searches for flexibility",
          "Always search all indexes without time filters"
        ],
        correctAnswer: 1,
        explanation: "Optimize by specifying the narrowest time range, targeting specific indexes, and filtering early to reduce data processed by subsequent commands."
      }
    ]
  },
  {
    quizId: "siem-q4",
    courseId: "siem-fundamentals",
    title: "Dashboards & Alerts Quiz",
    description: "Test your skills on visualization, dashboards, and alert configuration.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
{
        id: "siem-q4-1",
        question: "What is the primary purpose of a SOC dashboard?",
        options: [
          "To store log data",
          "To manage user accounts",
          "To provide real-time visibility into security events, trends, and operational status",
          "To replace all other monitoring tools"
        ],
        correctAnswer: 2,
        explanation: "SOC dashboards provide at-a-glance visibility into security posture, showing real-time event trends, alert status, and key metrics."
      },
{
        id: "siem-q4-2",
        question: "Which visualization type is best for showing trends over time?",
        options: [
          "Table",
          "Single value panel",
          "Pie chart",
          "Line chart or area chart"
        ],
        correctAnswer: 3,
        explanation: "Line charts and area charts are ideal for showing how values change over time."
      },
{
        id: "siem-q4-3",
        question: "What is a 'drilldown' in a SIEM dashboard?",
        options: [
          "Clicking a dashboard element to navigate to more detailed data or a new search",
          "Drilling into physical hardware",
          "A type of attack technique",
          "Removing data from the dashboard"
        ],
        correctAnswer: 0,
        explanation: "Drilldowns allow users to click on dashboard elements to navigate to detailed views or run more specific searches."
      },
{
        id: "siem-q4-4",
        question: "What is alert fatigue?",
        options: [
          "When dashboard refreshes are too slow",
          "When alerts stop being generated",
          "When analysts become desensitized due to excessive false positive alerts",
          "When the SIEM runs out of storage"
        ],
        correctAnswer: 2,
        explanation: "Alert fatigue occurs when analysts are overwhelmed by too many alerts (especially false positives), causing them to miss genuine threats."
      },
{
        id: "siem-q4-5",
        question: "What is a correlation rule in SIEM alerting?",
        options: [
          "A rule for organizing dashboard panels",
          "A rule that correlates employee schedules",
          "A data backup policy",
          "A detection rule that triggers when specific conditions across multiple events are met"
        ],
        correctAnswer: 3,
        explanation: "Correlation rules define conditions across multiple events that, when met together, trigger an alert."
      },
{
        id: "siem-q4-6",
        question: "Which visualization is best for showing the proportion of alert types?",
        options: [
          "Pie chart or donut chart",
          "Gauge",
          "Scatter plot",
          "Line chart"
        ],
        correctAnswer: 0,
        explanation: "Pie and donut charts effectively show proportional distribution of alert categories or severity levels."
      },
{
        id: "siem-q4-7",
        question: "What is a 'token' in Splunk dashboard context?",
        options: [
          "A dynamic variable that allows user input to filter dashboard panels interactively",
          "A physical security device",
          "An authentication credential",
          "A type of alert"
        ],
        correctAnswer: 0,
        explanation: "Dashboard tokens are dynamic variables populated by user inputs that filter data across multiple panels."
      },
{
        id: "siem-q4-8",
        question: "What is the recommended approach to reduce false positives in SIEM alerts?",
        options: [
          "Regularly review and tune detection rules by adding exceptions and adjusting thresholds",
          "Increase alert severity for all rules",
          "Only use pre-built alerts without modification",
          "Disable all alerts"
        ],
        correctAnswer: 0,
        explanation: "Reducing false positives requires ongoing tuning: adding whitelists, adjusting thresholds, enriching with context, and reviewing performance metrics."
      },
{
        id: "siem-q4-9",
        question: "What is a 'heatmap' useful for in security dashboards?",
        options: [
          "Visualizing data density or activity patterns across two dimensions",
          "Monitoring server room temperature",
          "Showing network cable layouts",
          "Heating up cold storage data"
        ],
        correctAnswer: 0,
        explanation: "Heatmaps visualize data density across two dimensions using color intensity, ideal for spotting anomalous activity patterns."
      },
{
        id: "siem-q4-10",
        question: "What should a well-designed alert include?",
        options: [
          "Just the alert name",
          "The analyst's personal notes",
          "Only the raw log data",
          "Severity, description, affected assets, recommended response actions, and relevant context"
        ],
        correctAnswer: 3,
        explanation: "Effective alerts include severity level, clear description, affected assets, recommended investigation steps, and contextual information."
      },
{
        id: "siem-q4-11",
        question: "What is a 'scheduled search' in SIEM alerting?",
        options: [
          "A search scheduled for deletion",
          "A search saved for personal reference",
          "A manual search run by an analyst",
          "A search that runs automatically at defined intervals and triggers alerts when conditions are met"
        ],
        correctAnswer: 3,
        explanation: "Scheduled searches run automatically at configured intervals, evaluating results against conditions to generate alerts."
      },
{
        id: "siem-q4-12",
        question: "What is alert throttling?",
        options: [
          "Speeding up alert delivery",
          "Limiting how frequently the same alert can fire within a time window to prevent flooding",
          "Increasing alert severity",
          "Disabling alerts permanently"
        ],
        correctAnswer: 1,
        explanation: "Alert throttling prevents alert flooding by suppressing duplicate alerts within a defined time window."
      },
{
        id: "siem-q4-13",
        question: "When should you use a geographic map visualization?",
        options: [
          "When showing CPU usage",
          "Only for internal network traffic",
          "When displaying data with geographic context like source IPs or login locations",
          "For all types of data"
        ],
        correctAnswer: 2,
        explanation: "Geographic maps are ideal for displaying location-based data such as attack origins or VPN login locations."
      },
{
        id: "siem-q4-14",
        question: "What is a 'notable event' in Splunk Enterprise Security?",
        options: [
          "A deleted event",
          "A scheduled report",
          "A high-priority security event generated by correlation searches that requires investigation",
          "Any regular log event"
        ],
        correctAnswer: 2,
        explanation: "Notable events are security-significant events generated by correlation searches in Splunk ES, appearing in the incident review queue."
      },
{
        id: "siem-q4-15",
        question: "What is the best practice for dashboard refresh intervals?",
        options: [
          "Balance between timely data and system performance — typically 1-5 minutes for operational dashboards",
          "Refresh only when manually triggered",
          "Never refresh — use static snapshots only",
          "Refresh every second for real-time data"
        ],
        correctAnswer: 0,
        explanation: "Dashboard refresh intervals should balance timeliness with performance. Operational SOC dashboards typically refresh every 1-5 minutes."
      }
    ]
  },
  {
    quizId: "siem-q5",
    courseId: "siem-fundamentals",
    title: "Final Certification Exam",
    description: "Comprehensive exam covering all SIEM fundamentals modules. Required for certification.",
    passingScore: 80,
    timeLimit: 45,
    questions: [
{
        id: "siem-q5-1",
        question: "A SOC analyst notices 500 failed login attempts from a single IP within 10 minutes. What SIEM feature detected this?",
        options: [
          "Correlation rule with threshold-based detection",
          "Dashboard visualization",
          "Data normalization",
          "Log retention policy"
        ],
        correctAnswer: 0,
        explanation: "Threshold-based correlation rules detect when event counts exceed defined limits within a time window."
      },
{
        id: "siem-q5-2",
        question: "Which SPL query would find the top 10 source IPs generating failed authentication events?",
        options: [
          "search * | filter src_ip",
          "search failed auth | head 10",
          "index=security | delete failed | top 10",
          "index=security action=failure | stats count by src_ip | sort -count | head 10"
        ],
        correctAnswer: 3,
        explanation: "This query searches security events for failures, counts per source IP, sorts descending, and limits to the top 10."
      },
{
        id: "siem-q5-3",
        question: "What is the MITRE ATT&CK tactic that SIEM is most directly aligned to detect?",
        options: [
          "Resource Development",
          "Multiple tactics across the kill chain via log correlation",
          "Physical access attacks",
          "Reconnaissance"
        ],
        correctAnswer: 1,
        explanation: "SIEM can detect activities across multiple ATT&CK tactics by correlating logs from various sources."
      },
{
        id: "siem-q5-4",
        question: "An analyst sees an 'Impossible Travel' alert — login from New York, then London 30 minutes later. What should they do first?",
        options: [
          "Ignore it — it's probably a VPN",
          "Investigate by checking VPN/proxy usage, verifying with the user, and reviewing session details",
          "Delete the alert",
          "Immediately disable the user account"
        ],
        correctAnswer: 1,
        explanation: "The analyst should investigate before acting: check for VPN/proxy usage, contact the user, and review session details."
      },
{
        id: "siem-q5-5",
        question: "What is the difference between real-time and historical SIEM searches?",
        options: [
          "Real-time searches continuously monitor incoming events; historical searches query stored data",
          "Real-time searches only work on dashboards",
          "There is no difference",
          "Historical searches are always faster"
        ],
        correctAnswer: 0,
        explanation: "Real-time searches monitor events as they arrive; historical searches query already-indexed data for investigation."
      },
{
        id: "siem-q5-6",
        question: "Which KQL query finds sign-in events from outside the United States in the last 24 hours?",
        options: [
          "SigninLogs | where Location != 'US'",
          "search SigninLogs NOT US",
          "SigninLogs | summarize by Location",
          "SigninLogs | where TimeGenerated > ago(24h) | where LocationDetails.countryOrRegion != 'US'"
        ],
        correctAnswer: 3,
        explanation: "This KQL query filters SigninLogs to the last 24 hours and excludes US-based sign-ins."
      },
{
        id: "siem-q5-7",
        question: "What is 'lateral movement' and how can SIEM detect it?",
        options: [
          "Physical movement of servers; detected by cameras",
          "Staff relocations; detected by HR systems",
          "Attackers moving between systems; detected by correlating authentication logs across hosts",
          "Network cable rearrangement; detected by port monitoring"
        ],
        correctAnswer: 2,
        explanation: "Lateral movement is when attackers move between internal systems. SIEM detects it by correlating authentication events across hosts."
      },
{
        id: "siem-q5-8",
        question: "You need a dashboard showing daily login trends, top failed IPs, and geographic distribution. Which visualizations?",
        options: [
          "Three single-value panels",
          "Line chart for trends, bar chart for top IPs, geographic map for distribution",
          "Three tables",
          "Three pie charts"
        ],
        correctAnswer: 1,
        explanation: "Use each visualization for its strength: line charts for trends, bar charts for rankings, and maps for geographic data."
      },
{
        id: "siem-q5-9",
        question: "What is the purpose of a SIEM use case library?",
        options: [
          "A software code repository",
          "A documented catalog of detection rules mapped to threats, with queries and response procedures",
          "A collection of books about SIEM",
          "A list of SIEM vendors"
        ],
        correctAnswer: 1,
        explanation: "A use case library catalogs all detection rules with their purpose, associated threats, queries, and response procedures."
      },
{
        id: "siem-q5-10",
        question: "What does 'data onboarding' involve in a SIEM project?",
        options: [
          "Purchasing new hardware",
          "Training new employees",
          "Uninstalling old software",
          "Identifying, collecting, normalizing, and validating new data sources for ingestion"
        ],
        correctAnswer: 3,
        explanation: "Data onboarding integrates new log sources: identifying data, configuring collection, defining parsing, and validating quality."
      },
{
        id: "siem-q5-11",
        question: "An alert fires for 'PowerShell Download Cradle Detected'. What SPL query likely generated this?",
        options: [
          "search powershell download",
          "index=security powershell",
          "index=network http download",
          "index=endpoint process_name=powershell.exe (commandline=*downloadstring* OR commandline=*invoke-webrequest*)"
        ],
        correctAnswer: 3,
        explanation: "This query searches endpoint logs for PowerShell processes with download-related command-line arguments."
      },
{
        id: "siem-q5-12",
        question: "What is the 'kill chain' approach to SIEM detection?",
        options: [
          "A chain of SIEM servers",
          "Creating detection rules aligned to each stage of an attack lifecycle",
          "Removing unused detection rules",
          "A method to delete old alerts"
        ],
        correctAnswer: 1,
        explanation: "The kill chain approach creates layered detection rules at each attack stage, increasing the chance of catching attackers."
      },
{
        id: "siem-q5-13",
        question: "How should you handle a detection rule with a 90% false positive rate?",
        options: [
          "Delete the rule entirely",
          "Keep it — 10% true positive is acceptable",
          "Analyze false positives for patterns, refine the rule logic, add exceptions, and retest",
          "Lower the severity and ignore it"
        ],
        correctAnswer: 2,
        explanation: "Identify common FP patterns, refine query logic, add contextual conditions or exceptions, then retest to improve fidelity."
      },
{
        id: "siem-q5-14",
        question: "What is 'pivoting' in SIEM investigation?",
        options: [
          "Rotating dashboard panels",
          "Switching between SIEM platforms",
          "Changing the search time range",
          "Using a discovered indicator to search for related events and expand the investigation"
        ],
        correctAnswer: 3,
        explanation: "Pivoting uses discovered artifacts as new search terms to find related events and uncover the full attack scope."
      },
{
        id: "siem-q5-15",
        question: "What is the recommended approach for building a new detection rule?",
        options: [
          "Develop, test against historical data, tune to reduce false positives, then deploy with monitoring",
          "Copy rules from the internet without modification",
          "Only use vendor-provided rules",
          "Write it and immediately put it in production"
        ],
        correctAnswer: 0,
        explanation: "Best practice: develop, test against historical data, tune thresholds/exceptions, then deploy with ongoing monitoring."
      },
{
        id: "siem-q5-16",
        question: "What is the difference between a 'saved search' and an 'alert' in SIEM?",
        options: [
          "Alerts cannot be saved",
          "A saved search is a reusable query; an alert is a saved search that triggers notifications",
          "Saved searches are faster",
          "They are the same thing"
        ],
        correctAnswer: 1,
        explanation: "A saved search is a stored query. An alert builds on a saved search by adding trigger conditions and notification actions."
      },
{
        id: "siem-q5-17",
        question: "During an incident, what is the best SIEM approach to build a timeline?",
        options: [
          "Only check the last hour of logs",
          "Use transaction grouping and time-sorted searches across relevant data sources",
          "Ask colleagues to remember what happened",
          "Screenshot each alert individually"
        ],
        correctAnswer: 1,
        explanation: "Building timelines requires time-sorted, correlated searches across multiple data sources to reconstruct the complete event sequence."
      },
{
        id: "siem-q5-18",
        question: "What metric measures the percentage of alerts that are actual security incidents?",
        options: [
          "Data Ingestion Volume",
          "True Positive Rate / Alert Fidelity",
          "MTTR (Mean Time To Respond)",
          "EPS (Events Per Second)"
        ],
        correctAnswer: 1,
        explanation: "True Positive Rate measures the percentage of alerts that represent real security incidents."
      },
{
        id: "siem-q5-19",
        question: "What is the role of threat intelligence feeds in SIEM?",
        options: [
          "They manage user authentication",
          "They replace the need for correlation rules",
          "They provide external indicators for automatic matching against incoming events",
          "They generate dashboards automatically"
        ],
        correctAnswer: 2,
        explanation: "Threat intelligence feeds supply external IOCs that the SIEM matches against incoming events to detect known threats."
      },
{
        id: "siem-q5-20",
        question: "You're investigating potential data exfiltration. Which SIEM data sources are most relevant?",
        options: [
          "Only email logs",
          "Only authentication logs",
          "Only SIEM configuration logs",
          "Firewall/proxy logs, DLP alerts, endpoint logs, and DNS queries"
        ],
        correctAnswer: 3,
        explanation: "Data exfiltration investigation requires correlating outbound traffic, DLP alerts, endpoint activity, and DNS queries."
      },
{
        id: "siem-q5-21",
        question: "What is a 'detection gap' in SIEM operations?",
        options: [
          "Time between dashboard refreshes",
          "A threat scenario that the SIEM currently has no detection rule for",
          "A physical gap in the server rack",
          "Network latency"
        ],
        correctAnswer: 1,
        explanation: "A detection gap is a threat without detection coverage. Gap analysis against MITRE ATT&CK helps identify and prioritize new rules."
      },
{
        id: "siem-q5-22",
        question: "What is the benefit of SIEM integration with SOAR?",
        options: [
          "SOAR automates response actions triggered by SIEM alerts, reducing response time",
          "SOAR improves SIEM search speed",
          "SOAR replaces the SIEM entirely",
          "SOAR provides better data storage"
        ],
        correctAnswer: 0,
        explanation: "SOAR automates repetitive response actions triggered by SIEM alerts, reducing MTTR and freeing analysts for complex investigations."
      },
{
        id: "siem-q5-23",
        question: "What is 'log source health monitoring' in SIEM?",
        options: [
          "Monitoring the physical health of servers",
          "Running antivirus on log files",
          "Checking log file formatting",
          "Tracking whether expected log sources are actively sending data and alerting if ingestion stops"
        ],
        correctAnswer: 3,
        explanation: "Log source health monitoring tracks active ingestion and alerts when data stops flowing — missing logs create detection blind spots."
      },
{
        id: "siem-q5-24",
        question: "Which represents the most mature SIEM deployment?",
        options: [
          "Comprehensive data sources, customized detection mapped to ATT&CK, automated response, continuous tuning",
          "Collecting logs from one data source with no alerts",
          "Collecting from multiple sources with vendor-default rules only",
          "Using SIEM only for compliance reporting"
        ],
        correctAnswer: 0,
        explanation: "A mature SIEM features comprehensive data coverage, customized detections, SOAR integration, and continuous improvement."
      },
{
        id: "siem-q5-25",
        question: "What is the most critical factor for SIEM success in a SOC?",
        options: [
          "Skilled analysts who understand the data, tune rules, and continuously improve detection coverage",
          "Ingesting the maximum amount of data possible",
          "Using only automated responses without human review",
          "Having the most expensive SIEM platform"
        ],
        correctAnswer: 0,
        explanation: "The most critical factor is skilled analysts who understand the environment, tune detection rules, and drive continuous improvement — technology alone is insufficient."
      }
    ]
  },
  {
    quizId: "nsm-q1",
    courseId: "network-security-monitoring",
    title: "NSM Foundations Quiz",
    description: "Test your knowledge of NSM philosophy, network protocols, OSI model, and sensor placement.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
{
        id: "nsm-q1-1",
        question: "What distinguishes Network Security Monitoring from traditional intrusion detection?",
        options: [
          "NSM only monitors wireless networks",
          "NSM only uses signature-based detection",
          "NSM focuses on collection, detection, AND analysis of network data for situational awareness",
          "NSM replaces the need for endpoint security entirely"
        ],
        correctAnswer: 2,
        explanation: "NSM goes beyond simple alerting by combining data collection, detection, and human-driven analysis to build comprehensive situational awareness of network activity."
      },
{
        id: "nsm-q1-2",
        question: "During a TCP three-way handshake, what is the correct sequence of flags?",
        options: [
          "SYN → SYN-ACK → ACK",
          "ACK → SYN → SYN-ACK",
          "SYN → ACK → SYN-ACK",
          "FIN → SYN → ACK"
        ],
        correctAnswer: 0,
        explanation: "The TCP three-way handshake proceeds: client sends SYN, server responds with SYN-ACK, client completes with ACK — establishing a reliable connection."
      },
{
        id: "nsm-q1-3",
        question: "Why is UDP significant from a security monitoring perspective?",
        options: [
          "UDP cannot be used for data exfiltration",
          "UDP is always encrypted",
          "UDP's connectionless nature makes it harder to track sessions and easier for attackers to spoof",
          "UDP traffic is automatically blocked by firewalls"
        ],
        correctAnswer: 2,
        explanation: "UDP is connectionless with no handshake, making it difficult to track sessions and easy for attackers to spoof source addresses — commonly abused in DNS amplification attacks and covert channels."
      },
{
        id: "nsm-q1-4",
        question: "At which OSI layer does a network TAP operate to capture traffic?",
        options: [
          "Layer 3 – Network",
          "Layer 1 – Physical",
          "Layer 7 – Application",
          "Layer 4 – Transport"
        ],
        correctAnswer: 1,
        explanation: "Network TAPs operate at the Physical layer (Layer 1), creating an exact electrical or optical copy of all traffic passing through a link without introducing latency."
      },
{
        id: "nsm-q1-5",
        question: "What is the primary disadvantage of using a SPAN/mirror port compared to a network TAP?",
        options: [
          "SPAN ports are more expensive than TAPs",
          "SPAN ports only capture Layer 2 traffic",
          "SPAN ports can drop packets under heavy load and may miss full-duplex traffic",
          "SPAN ports require custom hardware"
        ],
        correctAnswer: 2,
        explanation: "SPAN ports mirror traffic via the switch CPU, which can drop packets under load. They may also not capture Layer 1 errors, malformed frames, or full-duplex conversations accurately."
      },
{
        id: "nsm-q1-6",
        question: "Which DNS record type maps a domain name to an IPv4 address?",
        options: [
          "TXT record",
          "CNAME record",
          "MX record",
          "A record"
        ],
        correctAnswer: 3,
        explanation: "The A (Address) record maps a domain name to an IPv4 address. AAAA records serve the same purpose for IPv6 addresses."
      },
{
        id: "nsm-q1-7",
        question: "What is the purpose of the TTL field in an IP packet header from a defender's perspective?",
        options: [
          "It limits the packet's lifetime and can reveal OS fingerprinting and routing anomalies",
          "It specifies the packet's priority level",
          "It determines the maximum segment size",
          "It encrypts the packet payload"
        ],
        correctAnswer: 0,
        explanation: "TTL (Time to Live) limits how many hops a packet can traverse. Different operating systems set different initial TTL values, enabling passive OS fingerprinting. Unusual TTL values can also indicate tunneling or spoofing."
      },
{
        id: "nsm-q1-8",
        question: "Which sensor placement strategy provides the broadest visibility of external threats?",
        options: [
          "On individual endpoint machines",
          "Behind the internal firewall only",
          "At the network perimeter between the external firewall and the internet",
          "Only on the DMZ segment"
        ],
        correctAnswer: 2,
        explanation: "Placing sensors at the network perimeter captures all inbound and outbound traffic before internal filtering, providing maximum visibility of external threat actor activity."
      },
{
        id: "nsm-q1-9",
        question: "What does the term 'full content data' mean in NSM?",
        options: [
          "Only metadata about connections",
          "Summary statistics of network flows",
          "Firewall logs only",
          "Complete packet captures including headers and payloads"
        ],
        correctAnswer: 3,
        explanation: "Full content data refers to complete packet captures (PCAPs) that include all headers and payloads — the most detailed form of network evidence, essential for forensic analysis."
      },
{
        id: "nsm-q1-10",
        question: "Which protocol typically uses port 443 and obscures payload content from network monitors?",
        options: [
          "HTTPS/TLS",
          "DNS",
          "HTTP",
          "FTP"
        ],
        correctAnswer: 0,
        explanation: "HTTPS uses TLS encryption on port 443, making payload inspection impossible without TLS interception. Attackers frequently use HTTPS for C2 to blend with legitimate traffic."
      }
    ]
  },
  {
    quizId: "nsm-q2",
    courseId: "network-security-monitoring",
    title: "Packet Capture & Analysis Quiz",
    description: "Assess your Wireshark skills, TCP stream analysis, DNS and HTTP traffic inspection.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
{
        id: "nsm-q2-1",
        question: "What is the difference between a Wireshark capture filter and a display filter?",
        options: [
          "Display filters are applied before capture begins",
          "Capture filters only work on wireless interfaces",
          "Capture filters use BPF syntax and limit what is recorded; display filters use Wireshark syntax and filter what is shown from already captured data",
          "They are identical in syntax and function"
        ],
        correctAnswer: 2,
        explanation: "Capture filters (BPF syntax, e.g., 'host 10.0.0.1') determine what packets are saved to disk. Display filters (Wireshark syntax, e.g., 'ip.addr == 10.0.0.1') filter the view of already-captured data."
      },
{
        id: "nsm-q2-2",
        question: "Which Wireshark display filter shows only HTTP GET requests?",
        options: [
          "http.request.method == \"GET\"",
          "tcp.port == 80",
          "filter http get",
          "http contains GET"
        ],
        correctAnswer: 0,
        explanation: "The display filter 'http.request.method == \"GET\"' precisely targets HTTP GET requests by filtering on the parsed HTTP request method field."
      },
{
        id: "nsm-q2-3",
        question: "When reconstructing a TCP stream in Wireshark, what feature do you use?",
        options: [
          "Edit → Preferences → TCP",
          "Analyze → Expert Info",
          "Right-click a packet → Follow → TCP Stream",
          "Statistics → Flow Graph"
        ],
        correctAnswer: 2,
        explanation: "Right-clicking a TCP packet and selecting Follow → TCP Stream reassembles the entire conversation between client and server, showing the data exchanged in order."
      },
{
        id: "nsm-q2-4",
        question: "What does a high number of TCP RST packets from a single source IP likely indicate?",
        options: [
          "Successful file transfers",
          "Port scanning or connection probing",
          "DNS resolution activity",
          "Normal web browsing activity"
        ],
        correctAnswer: 1,
        explanation: "Large volumes of RST packets from one source typically indicate port scanning — the source is probing closed ports or services that reject the connection attempt."
      },
{
        id: "nsm-q2-5",
        question: "Which indicator in DNS traffic suggests possible DNS tunneling?",
        options: [
          "PTR record lookups for internal IPs",
          "SOA queries during zone transfers",
          "Standard A record queries to well-known domains",
          "Unusually long subdomain labels, high query volume to a single domain, and TXT record queries"
        ],
        correctAnswer: 3,
        explanation: "DNS tunneling encodes data in subdomain labels (creating abnormally long queries), generates high query volumes, and often uses TXT records to carry larger response payloads."
      },
{
        id: "nsm-q2-6",
        question: "What is the Wireshark display filter to show all packets from or to subnet 192.168.1.0/24?",
        options: [
          "net 192.168.1.0/24",
          "ip.src == 192.168.1.0/24",
          "ip.addr == 192.168.1.0/24",
          "host 192.168.1.*"
        ],
        correctAnswer: 2,
        explanation: "The display filter 'ip.addr == 192.168.1.0/24' matches any packet where either the source or destination IP falls within the specified CIDR range."
      },
{
        id: "nsm-q2-7",
        question: "How can you extract files transferred over HTTP from a PCAP in Wireshark?",
        options: [
          "File → Export Objects → HTTP",
          "Statistics → Endpoints",
          "Edit → Find Packet → String",
          "Analyze → Follow HTTP Stream"
        ],
        correctAnswer: 0,
        explanation: "File → Export Objects → HTTP lists all files transferred over HTTP in the capture, allowing you to save them individually — critical for extracting malware samples or exfiltrated documents."
      },
{
        id: "nsm-q2-8",
        question: "What does TCP retransmission indicate in a packet capture?",
        options: [
          "The connection is encrypted",
          "Packet loss occurred and the sender is resending unacknowledged segments",
          "The application is sending duplicate data intentionally",
          "The firewall is blocking traffic"
        ],
        correctAnswer: 1,
        explanation: "TCP retransmissions occur when the sender doesn't receive an ACK within the timeout period, indicating packet loss due to network congestion, faulty hardware, or potential interference."
      },
{
        id: "nsm-q2-9",
        question: "Which BPF capture filter captures only traffic on port 53?",
        options: [
          "dns.port == 53",
          "port 53",
          "tcp.port == 53",
          "filter port=53"
        ],
        correctAnswer: 1,
        explanation: "The BPF capture filter 'port 53' captures both TCP and UDP traffic on port 53 (DNS). BPF syntax differs from Wireshark display filter syntax."
      },
{
        id: "nsm-q2-10",
        question: "What suspicious pattern would you look for in HTTP traffic to detect a webshell?",
        options: [
          "JavaScript file downloads",
          "Large image downloads",
          "Standard GET requests to the homepage",
          "POST requests to unusual file paths with command-like parameters and small response sizes"
        ],
        correctAnswer: 3,
        explanation: "Webshells often manifest as POST requests to odd file paths (e.g., /uploads/shell.php) with command parameters (cmd=whoami), returning small text responses — distinct from normal web traffic patterns."
      }
    ]
  },
  {
    quizId: "nsm-q3",
    courseId: "network-security-monitoring",
    title: "Intrusion Detection with Suricata Quiz",
    description: "Evaluate your understanding of Suricata architecture, rule writing, and alert tuning.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
{
        id: "nsm-q3-1",
        question: "What is the basic structure of a Suricata rule?",
        options: [
          "IF-THEN-ELSE conditional blocks",
          "Action, Header (protocol/IPs/ports/direction), and Rule Options (in parentheses)",
          "JSON objects with match criteria",
          "XML-formatted detection signatures"
        ],
        correctAnswer: 1,
        explanation: "Suricata rules follow: ACTION PROTOCOL SRC_IP SRC_PORT -> DST_IP DST_PORT (options;). For example: alert http $HOME_NET any -> $EXTERNAL_NET any (msg:\"Suspicious UA\"; content:\"evil\"; sid:100001;)."
      },
{
        id: "nsm-q3-2",
        question: "What does the 'content' keyword do in a Suricata rule?",
        options: [
          "Defines the rule category",
          "Sets the logging output format",
          "Specifies the file type to inspect",
          "Matches a specific byte pattern or string within the packet payload or header"
        ],
        correctAnswer: 3,
        explanation: "The 'content' keyword performs pattern matching against packet data. It can match ASCII strings or hex byte sequences (e.g., content:|de ad be ef|;) and supports modifiers like nocase, depth, and offset."
      },
{
        id: "nsm-q3-3",
        question: "What is the purpose of the 'flow' keyword in Suricata rules?",
        options: [
          "To count the number of packets in a session",
          "To measure network bandwidth",
          "To specify the direction and state of the connection (established, to_server, to_client)",
          "To define flow chart diagrams"
        ],
        correctAnswer: 2,
        explanation: "The 'flow' keyword matches on TCP session state and direction. 'flow:established,to_server;' targets data sent from client to server on established connections, reducing false positives on handshake traffic."
      },
{
        id: "nsm-q3-4",
        question: "How does the 'threshold' keyword help reduce alert fatigue?",
        options: [
          "It disables alerts permanently",
          "It deletes alerts automatically after a set time",
          "It increases the priority of all alerts",
          "It limits alerting frequency, e.g., alerting once per source IP within a time window instead of per-packet"
        ],
        correctAnswer: 3,
        explanation: "Thresholds control alert rate — 'threshold:type limit,track by_src,count 1,seconds 300;' fires only once per source IP every 5 minutes, preventing alert floods from repetitive activity."
      },
{
        id: "nsm-q3-5",
        question: "What is the difference between Suricata running in IDS mode versus IPS mode?",
        options: [
          "IPS requires more rules than IDS",
          "There is no difference",
          "IDS passively monitors and alerts; IPS is inline and can actively block or drop malicious traffic",
          "IDS blocks traffic; IPS only monitors"
        ],
        correctAnswer: 2,
        explanation: "In IDS mode, Suricata passively copies and analyzes traffic. In IPS (inline) mode, traffic flows through Suricata, enabling 'drop' and 'reject' actions to block malicious packets in real time."
      },
{
        id: "nsm-q3-6",
        question: "Which Suricata rule action would you use to silently discard a malicious packet in IPS mode?",
        options: [
          "alert",
          "drop",
          "pass",
          "log"
        ],
        correctAnswer: 1,
        explanation: "The 'drop' action silently discards the matching packet and generates an alert. 'reject' also sends a reset/ICMP unreachable to the sender. 'pass' whitelists the traffic."
      },
{
        id: "nsm-q3-7",
        question: "What does the 'pcre' keyword allow you to do in Suricata rules?",
        options: [
          "Use Perl Compatible Regular Expressions for complex pattern matching",
          "Compress packet data",
          "Convert packets to PDF format",
          "Parse PCAP files directly"
        ],
        correctAnswer: 0,
        explanation: "The 'pcre' keyword enables regex-based matching for complex patterns that simple content matches can't express, like variable-length strings or pattern alternatives."
      },
{
        id: "nsm-q3-8",
        question: "What is a 'suppress' rule in Suricata used for?",
        options: [
          "To encrypt alert output",
          "To forward alerts to another system",
          "To prevent specific alerts from being generated for certain IPs or subnets without disabling the rule entirely",
          "To increase the severity of an alert"
        ],
        correctAnswer: 2,
        explanation: "Suppress rules silence alerts for specific track conditions (e.g., suppress gen_id 1, sig_id 2001, track by_src, ip 10.0.0.5) — useful for whitelisting known-good sources without disabling the detection globally."
      },
{
        id: "nsm-q3-9",
        question: "What does the 'sid' keyword represent in a Suricata rule?",
        options: [
          "Signature ID — a unique identifier for each rule",
          "Source ID — identifying the traffic source",
          "Security Impact Descriptor",
          "Session Identifier"
        ],
        correctAnswer: 0,
        explanation: "SID (Signature ID) is a unique numeric identifier for each Suricata rule. Custom rules typically use SID values starting at 1000000 to avoid conflicts with community rulesets."
      },
{
        id: "nsm-q3-10",
        question: "Which Suricata feature enables extraction and logging of TLS certificate metadata without decryption?",
        options: [
          "file-store module",
          "DNS parser",
          "HTTP log module",
          "TLS/SSL parser logging fields like tls.subject, tls.issuer, tls.ja3.hash"
        ],
        correctAnswer: 3,
        explanation: "Suricata's TLS parser extracts certificate metadata (subject, issuer, serial, JA3/JA3S fingerprints) from the handshake without requiring decryption — powerful for detecting suspicious certificates and known-bad TLS fingerprints."
      }
    ]
  },
  {
    quizId: "nsm-q4",
    courseId: "network-security-monitoring",
    title: "Network Metadata with Zeek Quiz",
    description: "Test your knowledge of Zeek logs, threat hunting with metadata, and Zeek scripting.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
{
        id: "nsm-q4-1",
        question: "What makes Zeek fundamentally different from Suricata in its approach to network analysis?",
        options: [
          "Zeek replaces the need for packet capture",
          "Zeek focuses on generating rich metadata logs about every connection rather than signature-based alerting",
          "Zeek can only analyze offline PCAPs",
          "Zeek is only a firewall"
        ],
        correctAnswer: 1,
        explanation: "Zeek generates structured metadata logs (conn.log, dns.log, http.log, etc.) about all network activity. While it supports scripting-based detection, its primary strength is comprehensive network visibility through logs."
      },
{
        id: "nsm-q4-2",
        question: "What is the 'uid' field in Zeek's conn.log used for?",
        options: [
          "The Unix user running the Zeek process",
          "User identification for authentication",
          "A unique connection identifier that correlates entries across all Zeek log files for the same session",
          "A checksum of the packet payload"
        ],
        correctAnswer: 2,
        explanation: "The UID is a unique string assigned to each connection. The same UID appears in conn.log, dns.log, http.log, files.log, etc., allowing analysts to trace all activity belonging to a single session."
      },
{
        id: "nsm-q4-3",
        question: "In Zeek's conn.log, what does a connection with 'conn_state: S0' indicate?",
        options: [
          "A UDP connection with data exchange",
          "A fully established and closed connection",
          "An established connection that was reset",
          "A SYN was sent but no SYN-ACK was received — the connection attempt was unanswered"
        ],
        correctAnswer: 3,
        explanation: "S0 means a SYN was sent with no reply, indicating the target port is filtered, the host is unreachable, or a stealthy scan is in progress. Large volumes of S0 connections from one source strongly suggest port scanning."
      },
{
        id: "nsm-q4-4",
        question: "Which Zeek log would you analyze to detect DNS tunneling?",
        options: [
          "conn.log",
          "dns.log — looking for unusually long queries, high volume to single domains, and TXT responses",
          "smtp.log",
          "ssl.log"
        ],
        correctAnswer: 1,
        explanation: "dns.log records all DNS queries and responses. DNS tunneling indicators in this log include abnormally long query strings, high query frequency to a single parent domain, and TXT record abuse."
      },
{
        id: "nsm-q4-5",
        question: "What information does Zeek's ssl.log provide that is valuable for threat detection?",
        options: [
          "Certificate details, JA3/JA3S fingerprints, server name (SNI), and validation status",
          "The decrypted content of HTTPS sessions",
          "Firewall rule match results",
          "Only the source and destination IPs"
        ],
        correctAnswer: 0,
        explanation: "ssl.log records TLS handshake metadata: certificate subject/issuer, JA3/JA3S hashes, SNI values, and validation status — enabling detection of self-signed certs, expired certs, and known malicious TLS fingerprints."
      },
{
        id: "nsm-q4-6",
        question: "How would you use Zeek logs to identify potential C2 beaconing?",
        options: [
          "Check smtp.log for outbound emails",
          "Analyze conn.log for connections with regular time intervals, consistent byte sizes, and long durations to the same destination",
          "Review notice.log for system errors",
          "Look for connections with large file downloads"
        ],
        correctAnswer: 1,
        explanation: "C2 beacons produce regular connection patterns visible in conn.log: consistent intervals between connections, similar request/response sizes, long session durations, and persistence to the same external IP."
      },
{
        id: "nsm-q4-7",
        question: "What is the purpose of Zeek's files.log?",
        options: [
          "Listing Zeek configuration files",
          "Logging filesystem changes on the Zeek server",
          "Recording metadata about every file transferred over the network, including hashes and MIME types",
          "Tracking log file rotation"
        ],
        correctAnswer: 2,
        explanation: "files.log records metadata for every file transferred over monitored protocols: SHA256/MD5 hashes, MIME types, file sizes, source/destination, and extraction status — enabling malware detection via hash matching."
      },
{
        id: "nsm-q4-8",
        question: "What does a Zeek 'notice' represent?",
        options: [
          "A notification about Zeek software updates",
          "A debug message for developers",
          "A higher-level detection event generated by Zeek's analysis framework when policy-relevant activity is observed",
          "A system error in the Zeek process"
        ],
        correctAnswer: 2,
        explanation: "Notices are Zeek's built-in detection mechanism — generated when the analysis framework identifies policy-relevant activity like SSL certificate issues, scan detection, or protocol violations."
      },
{
        id: "nsm-q4-9",
        question: "Which Zeek command-line option reads a PCAP file for offline analysis?",
        options: [
          "zeek --offline capture.pcap",
          "zeek --import capture.pcap",
          "zeek --live",
          "zeek -r capture.pcap"
        ],
        correctAnswer: 3,
        explanation: "The '-r' flag reads a PCAP file for offline analysis: 'zeek -r capture.pcap' processes the file and generates all applicable log files — the same analysis as live monitoring."
      },
{
        id: "nsm-q4-10",
        question: "What is a practical use case for Zeek scripting?",
        options: [
          "Replacing Suricata entirely",
          "Creating custom log fields, triggering notices on specific conditions, or enriching data with external intelligence feeds",
          "Generating firewall rules automatically",
          "Compiling packet captures into video"
        ],
        correctAnswer: 1,
        explanation: "Zeek scripts extend analysis capabilities: adding custom fields to logs, creating detection logic (e.g., alerting on connections to threat intel IPs), computing statistics, or extracting files matching specific criteria."
      }
    ]
  },
  {
    quizId: "nsm-q5",
    courseId: "network-security-monitoring",
    title: "Network Attack Detection Quiz",
    description: "Assess your ability to detect reconnaissance, C2, lateral movement, and exfiltration.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
{
        id: "nsm-q5-1",
        question: "Which network behavior most strongly indicates a TCP SYN scan (half-open scan)?",
        options: [
          "Large volumes of UDP traffic",
          "ICMP echo requests to multiple hosts",
          "Completed TCP handshakes followed by data transfer",
          "SYN packets to many ports with RST responses and no completed handshakes"
        ],
        correctAnswer: 3,
        explanation: "A SYN scan sends SYN packets to target ports. Open ports reply SYN-ACK (scanner sends RST), closed ports reply RST. No handshakes complete — visible as many S0/REJ states in Zeek conn.log."
      },
{
        id: "nsm-q5-2",
        question: "What is JA3 fingerprinting and why is it useful for detecting C2?",
        options: [
          "A method to block all HTTPS traffic",
          "A DNS-based threat intelligence feed",
          "A technique to decrypt TLS traffic",
          "An MD5 hash of specific TLS Client Hello parameters that uniquely identifies client applications regardless of IP or domain"
        ],
        correctAnswer: 3,
        explanation: "JA3 hashes the TLS version, cipher suites, extensions, and elliptic curves from the Client Hello. Malware families produce consistent JA3 fingerprints, enabling detection even when attackers rotate domains and IPs."
      },
{
        id: "nsm-q5-3",
        question: "How does C2 beaconing typically appear in network traffic?",
        options: [
          "Periodic connections at regular or near-regular intervals to the same destination with consistent packet sizes",
          "One-time large file downloads",
          "Inbound connections from multiple countries simultaneously",
          "Random connections to many different destinations"
        ],
        correctAnswer: 0,
        explanation: "Beaconing produces a rhythmic pattern: connections at fixed intervals (with possible jitter), similar request/response sizes, to the same destination — distinguishable from human-driven traffic's irregular patterns."
      },
{
        id: "nsm-q5-4",
        question: "Which network protocol is commonly abused for lateral movement using PsExec?",
        options: [
          "SMTP on port 25",
          "HTTP on port 80",
          "SMB on port 445",
          "DNS on port 53"
        ],
        correctAnswer: 2,
        explanation: "PsExec uses SMB (port 445) to copy an executable to the target's ADMIN$ share and create a remote service. Detecting SMB writes to ADMIN$ followed by service creation is a key lateral movement indicator."
      },
{
        id: "nsm-q5-5",
        question: "What network-level indicator suggests RDP-based lateral movement?",
        options: [
          "ICMP traffic between servers",
          "HTTP POST requests between internal hosts",
          "Internal-to-internal connections on port 3389, especially from hosts that don't normally initiate RDP",
          "DNS queries for external domains"
        ],
        correctAnswer: 2,
        explanation: "RDP lateral movement appears as port 3389 connections between internal hosts. Baselines of normal RDP usage help identify anomalous sessions — especially from workstations to servers or unusual source hosts."
      },
{
        id: "nsm-q5-6",
        question: "Which technique uses DNS queries to secretly extract data from a network?",
        options: [
          "DNS amplification attack",
          "DNS cache poisoning",
          "DNS exfiltration — encoding stolen data in subdomain labels of queries to attacker-controlled domains",
          "DNS zone transfer"
        ],
        correctAnswer: 2,
        explanation: "DNS exfiltration encodes data in subdomain queries (e.g., base64data.evil.com). Since DNS is rarely blocked, attackers can slowly extract data — detectable by monitoring query length, volume, and entropy."
      },
{
        id: "nsm-q5-7",
        question: "What is a 'low and slow' exfiltration technique designed to evade?",
        options: [
          "Volume-based and rate-based network detection thresholds",
          "Endpoint antivirus scans",
          "Physical security controls",
          "User authentication systems"
        ],
        correctAnswer: 0,
        explanation: "Low-and-slow exfiltration sends small amounts of data over long periods to stay under volume thresholds and rate-based alerts. Detection requires baselining normal traffic patterns and looking for cumulative anomalies."
      },
{
        id: "nsm-q5-8",
        question: "How can you detect pass-the-hash attacks on the network?",
        options: [
          "By detecting NTLM authentication over SMB/RPC where the same NTLM hash authenticates to multiple systems in a short timeframe",
          "By monitoring HTTP headers",
          "By checking DNS query patterns",
          "By analyzing email attachments"
        ],
        correctAnswer: 0,
        explanation: "Pass-the-hash uses stolen NTLM hashes for authentication. Network indicators include NTLM (not Kerberos) authentication, the same account authenticating to many systems rapidly, and type-3 NTLM messages without prior type-1/type-2."
      },
{
        id: "nsm-q5-9",
        question: "Which of the following would indicate potential data staging before exfiltration?",
        options: [
          "Standard software update downloads",
          "Unusual SMB file copy activity to a single internal host followed by large outbound transfers from that host",
          "Normal email traffic patterns",
          "Routine backup traffic to designated servers"
        ],
        correctAnswer: 1,
        explanation: "Attackers often stage data by copying files from multiple internal sources to a single collection point, then exfiltrating from there — visible as unusual inbound SMB activity followed by anomalous outbound connections."
      },
{
        id: "nsm-q5-10",
        question: "What makes ICMP tunneling difficult to detect without proper monitoring?",
        options: [
          "ICMP traffic is never logged by any tool",
          "ICMP only works on internal networks",
          "ICMP is always encrypted",
          "ICMP echo requests/replies are common and often allowed through firewalls, but the data payload field can carry hidden communication"
        ],
        correctAnswer: 3,
        explanation: "ICMP echo (ping) is universally allowed. Attackers embed data in the payload field. Detection requires inspecting ICMP payload sizes (abnormally large), content (non-standard patterns), and session frequency."
      }
    ]
  },
  {
    quizId: "nsm-q6",
    courseId: "network-security-monitoring",
    title: "Practical NSM Operations Quiz",
    description: "Evaluate your understanding of NSM workflows, network forensics, and best practices.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
{
        id: "nsm-q6-1",
        question: "What is the recommended architecture for integrating Zeek and Suricata into a SIEM?",
        options: [
          "Deploy both on sensors with a log shipper (e.g., Filebeat) forwarding to a centralized SIEM for correlation and alerting",
          "Store all data locally on each sensor without centralization",
          "Run both tools on the SIEM server itself",
          "Only use one tool at a time, never both"
        ],
        correctAnswer: 0,
        explanation: "Best practice is sensor-based deployment with centralized analysis: Zeek and Suricata run on network sensors, Filebeat ships logs to a SIEM (e.g., Elastic/Splunk), enabling cross-source correlation and unified alerting."
      },
{
        id: "nsm-q6-2",
        question: "When preserving network evidence for forensic investigation, which principle is most critical?",
        options: [
          "Immediately analyze all PCAPs on the production sensor",
          "Delete old captures to save disk space",
          "Maintain chain of custody with hashing, timestamps, and write-protected copies of original evidence",
          "Share raw PCAPs via email to the legal team"
        ],
        correctAnswer: 2,
        explanation: "Forensic integrity requires chain of custody: hash original PCAPs immediately (SHA256), record collection timestamps, work on copies only, document every access, and store originals on write-protected media."
      },
{
        id: "nsm-q6-3",
        question: "How do you construct a network forensics timeline from Zeek logs?",
        options: [
          "Correlate events across Zeek logs using timestamps and UIDs to build a chronological sequence of attacker actions",
          "Rely solely on firewall logs",
          "Only use conn.log and ignore other log types",
          "Sort alerts by severity only"
        ],
        correctAnswer: 0,
        explanation: "Timeline construction uses Zeek's UID to link conn.log → dns.log → http.log → files.log entries for the same session, then orders all correlated events chronologically to reconstruct the attacker's progression."
      },
{
        id: "nsm-q6-4",
        question: "What is the primary risk of running Suricata with outdated rule sets?",
        options: [
          "The system will crash",
          "New attack techniques and malware variants will go undetected while only known-old threats are caught",
          "Network performance will degrade",
          "Log files will become corrupted"
        ],
        correctAnswer: 1,
        explanation: "Outdated rules miss new CVE exploits, recent malware C2 patterns, and evolving TTPs. Best practice is automated daily rule updates (e.g., suricata-update) combined with custom rules for environment-specific threats."
      },
{
        id: "nsm-q6-5",
        question: "Which metric best indicates the health and coverage of an NSM deployment?",
        options: [
          "Number of Suricata rules loaded",
          "Total PCAP storage consumed",
          "Percentage of network segments with sensor coverage combined with mean time to detect simulated attacks",
          "Total number of alerts generated per day"
        ],
        correctAnswer: 2,
        explanation: "Effective NSM metrics combine coverage (what percentage of network traffic is monitored) with detection effectiveness (how quickly simulated or red team attacks are identified) — not just raw alert volume."
      },
{
        id: "nsm-q6-6",
        question: "What is the purpose of traffic baselining in NSM operations?",
        options: [
          "To encrypt all network traffic",
          "To throttle network bandwidth",
          "To reduce the number of network users",
          "To establish normal traffic patterns so that deviations indicating potential threats can be identified"
        ],
        correctAnswer: 3,
        explanation: "Baselining documents normal traffic patterns (volume, protocols, endpoints, time-of-day patterns). Deviations from baseline — such as new protocols, unusual hours, or unexpected destinations — signal potential threats.",
      },
{
        id: "nsm-q6-7",
        question: "During a multi-stage intrusion investigation, what should be your first step after receiving an alert?",
        options: [
          "Restart the IDS sensor",
          "Pivot from the alert to collect full context: check Zeek logs for the connection UID, review related sessions, and determine scope before taking action",
          "Immediately block the source IP on the firewall",
          "Delete the alert and wait for more"
        ],
        correctAnswer: 1,
        explanation: "Effective triage starts with context gathering: trace the alert's connection through Zeek logs, identify related sessions, check for lateral movement, and determine blast radius before containment actions."
      },
{
        id: "nsm-q6-8",
        question: "What challenge does TLS encryption present for NSM, and how is it addressed?",
        options: [
          "TLS has no impact on monitoring capabilities",
          "TLS prevents payload inspection; analysts compensate using metadata analysis (JA3, SNI, certificate info, connection patterns) and optional TLS inspection proxies",
          "TLS makes all traffic invisible to sensors",
          "TLS is only used on external traffic"
        ],
        correctAnswer: 1,
        explanation: "TLS encrypts payloads but metadata remains visible: JA3 fingerprints, SNI values, certificate details, connection timing/sizes. Combined with optional TLS interception proxies at the perimeter, effective monitoring is maintained."
      },
{
        id: "nsm-q6-9",
        question: "What is the recommended PCAP retention strategy for a production NSM environment?",
        options: [
          "Only keep PCAPs from weekdays",
          "Delete PCAPs immediately after analysis",
          "Keep all PCAPs forever",
          "Tiered retention: full PCAP for days/weeks on fast storage, Zeek metadata for months, alert-related PCAPs archived for years based on compliance requirements"
        ],
        correctAnswer: 3,
        explanation: "Tiered retention balances storage costs with investigative needs: short-term full PCAP on fast storage, medium-term Zeek metadata, and long-term archival of incident-related captures — aligned with regulatory requirements."
      },
{
        id: "nsm-q6-10",
        question: "In a final capstone investigation, which approach demonstrates mature NSM analysis?",
        options: [
          "Focusing only on the most recent alert",
          "Correlating alerts, Zeek metadata, and PCAP evidence across time to reconstruct the full attack chain from initial access through exfiltration",
          "Responding to each alert individually without connecting them",
          "Forwarding all alerts to management without analysis"
        ],
        correctAnswer: 1,
        explanation: "Mature NSM analysis correlates all data sources: Suricata alerts identify suspicious events, Zeek logs provide session context and connection history, and PCAP provides packet-level proof — together revealing the complete attack narrative."
      }
    ]
  },
  {
    quizId: "ir-q1",
    courseId: "incident-response",
    title: "IR Foundations & Frameworks Quiz",
    description: "Test your knowledge of IR lifecycle models, NIST and SANS frameworks, and team structure.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
{ id: "ir-q1-1", question: "What distinguishes a security incident from a security event?", options: ["An incident is a violation or imminent threat of violation of security policies", "Incidents only involve data loss", "Incidents are always caused by external attackers", "Events are more severe than incidents"], correctAnswer: 0, explanation: "A security incident is defined as a violation or imminent threat of violation of security policies." },
{ id: "ir-q1-2", question: "What are the four phases of the NIST SP 800-61 incident response lifecycle?", options: ["Prevention, Detection, Response, Recovery", "Identify, Protect, Detect, Respond", "Preparation, Detection & Analysis, Containment/Eradication/Recovery, Post-Incident Activity", "Assessment, Containment, Remediation, Reporting"], correctAnswer: 2, explanation: "NIST SP 800-61 defines four phases operating as a continuous improvement cycle." },
{ id: "ir-q1-3", question: "How does SANS PICERL differ from NIST regarding containment, eradication, and recovery?", options: ["SANS only uses containment and recovery", "SANS separates them into three distinct phases", "SANS combines all three into one phase", "SANS skips eradication"], correctAnswer: 1, explanation: "SANS PICERL treats Containment, Eradication, and Recovery as three separate phases." },
{ id: "ir-q1-4", question: "What does 'R' stand for in a RACI matrix?", options: ["Recovering", "Reviewing", "Reporting", "Responsible"], correctAnswer: 3, explanation: "R stands for Responsible — the person who does the work." },
{ id: "ir-q1-5", question: "Which IR team model uses a core team augmented by on-call specialists?", options: ["Distributed IR Team", "Hybrid / Virtual Team", "Outsourced / Retainer", "Central IR Team"], correctAnswer: 1, explanation: "A Hybrid/Virtual Team maintains a core IR team augmented by on-call specialists from different departments." },
{ id: "ir-q1-6", question: "What is the average dwell time reported by industry studies?", options: ["24 hours", "7 days", "30 days", "200+ days"], correctAnswer: 3, explanation: "Industry reports show average dwell times exceeding 200 days." },
{ id: "ir-q1-7", question: "Which framework is NOT an IR framework but essential for understanding adversary TTPs?", options: ["MITRE ATT&CK", "NIST SP 800-61", "ISO 27035", "SANS PICERL"], correctAnswer: 0, explanation: "MITRE ATT&CK is a knowledge base of adversary TTPs, not an IR framework." },
{ id: "ir-q1-8", question: "What is the primary purpose of the NIST Post-Incident Activity phase?", options: ["Feeding lessons back into Preparation for continuous improvement", "Restoring systems", "Notifying regulators", "Prosecuting the attacker"], correctAnswer: 0, explanation: "Post-Incident Activity closes the loop by feeding improvements back into Preparation." },
{ id: "ir-q1-9", question: "Organizations without formal IR capability face approximately how much higher breach costs?", options: ["63%", "90%", "40%", "25%"], correctAnswer: 0, explanation: "Approximately 63% higher breach costs according to the IBM Cost of a Data Breach Report." },
{ id: "ir-q1-10", question: "Which stakeholder handles breach notification and regulatory compliance?", options: ["Communications / PR", "HR", "IT Operations", "Legal / General Counsel"], correctAnswer: 3, explanation: "Legal/General Counsel handles breach notification, regulatory compliance, and privilege considerations." }
    ]
  },
  {
    quizId: "ir-q2",
    courseId: "incident-response",
    title: "Preparation & Planning",
    description: "Test your understanding of IR documentation hierarchy, jump bags, communication protocols, and legal considerations.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "ir-q2-1", question: "What is the correct hierarchy of IR documentation?", options: ["Playbook → Plan → Policy", "Plan → Policy → Playbook", "Policy → Plan → Playbook", "Policy → Playbook → Plan"], correctAnswer: 2, explanation: "Policy (high-level) → Plan (detailed procedures) → Playbook (step-by-step guides)." },
      { id: "ir-q2-2", question: "Why should IR teams use out-of-band communication during an incident?", options: ["Because compromised systems may be monitored by the attacker", "To save money", "To avoid documentation", "Because normal channels are too slow"], correctAnswer: 0, explanation: "Compromised systems may be monitored, so out-of-band channels prevent the attacker from observing IR coordination." },
      { id: "ir-q2-3", question: "Under GDPR, what is the breach notification timeline?", options: ["24 hours", "72 hours", "48 hours", "7 days"], correctAnswer: 1, explanation: "GDPR Article 33 requires notification within 72 hours of becoming aware of a personal data breach." },
      { id: "ir-q2-4", question: "What is the primary purpose of a write blocker?", options: ["Prevent modification of evidence drives during imaging", "Encrypt evidence", "Speed up imaging", "Compress forensic images"], correctAnswer: 0, explanation: "Write blockers prevent any write operations to evidence drives, maintaining integrity and admissibility." },
      { id: "ir-q2-5", question: "In a tabletop exercise, what is an 'inject'?", options: ["A type of malware", "A report document", "A technical attack tool", "A timed scenario element introducing new information or escalation"], correctAnswer: 3, explanation: "Injects are timed scenario elements that introduce new information and force participants to adapt." },
      { id: "ir-q2-6", question: "Which tool is designed for rapid triage artifact collection?", options: ["Wireshark", "KAPE", "Nmap", "Burp Suite"], correctAnswer: 1, explanation: "KAPE is specifically designed for rapid triage collection of forensic artifacts from endpoints." },
      { id: "ir-q2-7", question: "How often should an IR jump bag be validated?", options: ["After incidents only", "Annually", "Monthly with quarterly exercises", "When new tools release"], correctAnswer: 2, explanation: "Monthly validation ensures tools are updated; quarterly exercises test deployment readiness." },
      { id: "ir-q2-8", question: "A SEV-1 incident includes which of the following?", options: ["Policy violations", "Active data exfiltration or ransomware spreading", "Malware on isolated system", "Suspicious unconfirmed activity"], correctAnswer: 1, explanation: "SEV-1 covers active exfiltration, spreading ransomware, and complete service outages." },
      { id: "ir-q2-9", question: "What is the most common finding from tabletop exercises?", options: ["Inadequate tools", "Insufficient budgets", "Lack of certifications", "Unclear or outdated escalation paths"], correctAnswer: 3, explanation: "Common findings include unclear escalation paths, outdated contacts, and disagreements about authority." },
      { id: "ir-q2-10", question: "Why establish attorney-client privilege for IR communications?", options: ["To protect IR communications from legal discovery", "To avoid documenting incidents", "To bypass regulatory requirements", "To limit access to the IR plan"], correctAnswer: 0, explanation: "Privilege protects sensitive investigation details from being discoverable in litigation." }
    ]
  },
  {
    quizId: "ir-q3",
    courseId: "incident-response",
    title: "Detection & Analysis",
    description: "Test your understanding of detection sources, triage, indicator analysis, and root cause analysis.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "ir-q3-1", question: "In the Pyramid of Pain, which indicator is HARDEST for attackers to change?", options: ["Hash values", "IP addresses", "TTPs", "Domain names"], correctAnswer: 2, explanation: "TTPs are fundamental to how attackers operate; changing them requires completely retooling." },
      { id: "ir-q3-2", question: "What is the difference between an IOC and an IOA?", options: ["IOCs are artifacts; IOAs are behavioral patterns during an attack", "IOCs are behavioral; IOAs are artifacts", "IOAs are more specific", "No difference"], correctAnswer: 0, explanation: "IOCs are forensic artifacts left behind; IOAs are behavioral patterns detected during an attack." },
      { id: "ir-q3-3", question: "What response time SLA is expected for SEV-1 initial response?", options: ["1 hour", "30 minutes", "15 minutes", "4 hours"], correctAnswer: 2, explanation: "SEV-1 requires 15-minute initial response with updates every 30 minutes." },
      { id: "ir-q3-4", question: "The 5 Whys technique aims to identify:", options: ["The responsible individual", "Five mitigations", "Five attack vectors", "The systemic failure that allowed the attack"], correctAnswer: 3, explanation: "The 5 Whys drills from symptoms to the underlying systemic/organizational failure." },
      { id: "ir-q3-5", question: "Which source often FIRST detects BEC attacks?", options: ["User reports", "EDR", "SIEM rules", "NDR tools"], correctAnswer: 0, explanation: "Users who receive suspicious emails often provide the first detection for BEC and social engineering." },
      { id: "ir-q3-6", question: "What is 'anchoring bias' in incident triage?", options: ["Prioritizing specific data sources", "Assuming the first hypothesis is correct", "Only investigating during business hours", "Focusing only on high-severity alerts"], correctAnswer: 1, explanation: "Anchoring bias means interpreting all subsequent evidence to confirm the initial hypothesis." },
      { id: "ir-q3-7", question: "In a fishbone diagram, 'missing EDR coverage' falls under which category?", options: ["People", "Technology", "Process", "Policy"], correctAnswer: 1, explanation: "Missing EDR coverage is a Technology contributing factor." },
      { id: "ir-q3-8", question: "What is the target MTTD for a high-performing IR team?", options: ["< 1 hour", "< 30 days", "< 7 days", "< 24 hours"], correctAnswer: 3, explanation: "High-performing teams target MTTD under 24 hours vs. the industry average of ~200 days." },
      { id: "ir-q3-9", question: "Which correlation technique groups events by time window?", options: ["Entity correlation", "Temporal correlation", "TTP mapping", "Behavioral correlation"], correctAnswer: 1, explanation: "Temporal correlation groups events by time window to build chronological attack timelines." },
      { id: "ir-q3-10", question: "Impact assessment during triage evaluates which triad?", options: ["Confidentiality, Integrity, Availability", "People, Process, Technology", "Detection, Response, Recovery", "Risk, Threat, Vulnerability"], correctAnswer: 0, explanation: "Impact is assessed across the CIA triad: was data accessed (C), modified (I), or services disrupted (A)?" }
    ]
  },
  {
    quizId: "ir-q4",
    courseId: "incident-response",
    title: "Containment Strategies",
    description: "Test your knowledge of containment, evidence preservation, and decision-making frameworks.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "ir-q4-1", question: "Why should you NEVER power off a compromised system before capturing memory?", options: ["It damages the hard drive", "The OS won't boot again", "You lose volatile evidence: RAM, processes, network connections", "It triggers attacker dead man switches"], correctAnswer: 2, explanation: "Powering off destroys volatile evidence including RAM, running processes, and network connections." },
      { id: "ir-q4-2", question: "How many times must KRBTGT be reset to remediate Golden Ticket attacks?", options: ["Twice with 12+ hour gap", "Once", "Three times over 48 hours", "Depends on domain controllers"], correctAnswer: 0, explanation: "KRBTGT must be reset twice with 12+ hours between to invalidate tickets from both old and new hashes." },
      { id: "ir-q4-3", question: "What is a DNS sinkhole used for during containment?", options: ["Speed up DNS for IR team", "Encrypt DNS queries", "Block all DNS traffic", "Redirect malicious domains to reveal other infected systems"], correctAnswer: 3, explanation: "DNS sinkholes redirect malicious domain resolutions, blocking C2 and revealing other infected systems." },
      { id: "ir-q4-4", question: "In the order of volatility, which should be collected FIRST?", options: ["Running memory (RAM)", "Log files", "Disk contents", "Backup media"], correctAnswer: 0, explanation: "RAM is the most practically collectible volatile evidence and is lost on power-off." },
      { id: "ir-q4-5", question: "When is monitoring preferred over immediate isolation?", options: ["When ransomware is spreading", "When the attacker is dormant and you need intelligence", "When data is being exfiltrated", "When legal requires immediate action"], correctAnswer: 1, explanation: "Monitoring is preferred when the attacker is dormant, allowing intelligence gathering about scope and TTPs." },
      { id: "ir-q4-6", question: "Chain of custody documentation includes:", options: ["Collector, time, tool, storage location, and every transfer", "Only the hash value", "Only analyst name and date", "Only description and case number"], correctAnswer: 0, explanation: "Full chain of custody tracks collector, time, tool, hash, storage, and every subsequent transfer." },
      { id: "ir-q4-7", question: "Why is coordinated simultaneous containment important?", options: ["It's faster", "It prevents attackers from adapting to individual containment actions", "It reduces tools needed", "It simplifies documentation"], correctAnswer: 1, explanation: "Sequential containment lets sophisticated attackers detect and adapt; simultaneous containment prevents this." },
      { id: "ir-q4-8", question: "Which containment method maintains management connectivity while isolating endpoints?", options: ["Disabling NICs", "VLAN isolation", "Firewall blocking", "EDR isolation"], correctAnswer: 3, explanation: "EDR isolation blocks all network traffic except the EDR management connection." },
      { id: "ir-q4-9", question: "Which hash algorithms should verify forensic images?", options: ["MD5 only", "SHA-1 only", "MD5 + SHA-256", "CRC32"], correctAnswer: 2, explanation: "Using both MD5 and SHA-256 provides stronger verification expected in legal contexts." },
      { id: "ir-q4-10", question: "What should always happen before issuing a litigation hold?", options: ["Complete the investigation", "Consult legal counsel on preservation requirements", "Notify law enforcement", "Power off affected systems"], correctAnswer: 1, explanation: "Legal counsel determines preservation requirements before issuing holds to prevent routine data destruction." }
    ]
  },
  {
    quizId: "ir-q5",
    courseId: "incident-response",
    title: "Eradication & Recovery",
    description: "Test your knowledge of malware removal, system restoration, validation, and business resumption.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "ir-q5-1", question: "When should you REBUILD rather than clean a system?", options: ["Only when outdated", "Only for compliance", "Only when malware is found", "When rootkits are detected, DCs are compromised, or scope is unclear"], correctAnswer: 3, explanation: "Rebuilding is required for rootkits, compromised DCs, or unclear scope — re-compromise risk is too high." },
      { id: "ir-q5-2", question: "Which persistence mechanism achieves fileless execution via WMI?", options: ["Registry Run Keys", "WMI Event Subscriptions", "Scheduled Tasks", "DLL Hijacking"], correctAnswer: 1, explanation: "WMI Event Subscriptions create fileless persistence that traditional AV may not detect." },
      { id: "ir-q5-3", question: "What is the correct phased restoration order?", options: ["Workstations → Critical → Core", "All simultaneously", "Core infrastructure → Critical business → Workstations → Non-critical", "Non-critical first"], correctAnswer: 2, explanation: "Start with core infrastructure (AD, DNS), then critical business systems, then workstations, then non-critical." },
      { id: "ir-q5-4", question: "What must happen BEFORE reconnecting a restored system?", options: ["Patch vulnerabilities, install EDR, configure enhanced logging", "Notify users", "Complete the final report", "Hold lessons learned meeting"], correctAnswer: 0, explanation: "All patches, EDR, enhanced logging, credential rotation, and scanning must be done before reconnection." },
      { id: "ir-q5-5", question: "How long should enhanced monitoring continue post-incident?", options: ["1 week", "2 weeks", "30-90 days", "6 months"], correctAnswer: 2, explanation: "30-90 days of enhanced monitoring allows detection of missed persistence or attacker re-entry." },
      { id: "ir-q5-6", question: "What distinguishes business resumption from technical recovery?", options: ["Recovery focuses on systems; resumption focuses on business processes and user productivity", "No difference", "Resumption happens first", "Recovery is owned by business units"], correctAnswer: 0, explanation: "Systems running doesn't mean users are productive — resumption ensures business processes function." },
      { id: "ir-q5-7", question: "Which re-compromise sign requires IMMEDIATE escalation?", options: ["Normal logins", "Slow performance", "More help desk tickets", "Connections to previously blocked attacker infrastructure from new sources"], correctAnswer: 3, explanation: "New sources connecting to blocked attacker infrastructure indicates missed persistence or new compromise." },
      { id: "ir-q5-8", question: "When restoring from backup, what must NOT be skipped?", options: ["Restore the most recent backup", "Verify backup predates compromise and scan for malware", "Restore to original hardware", "Notify users first"], correctAnswer: 1, explanation: "Backups created after compromise may contain attacker persistence mechanisms." },
      { id: "ir-q5-9", question: "What marks formal transition from IR to normal operations?", options: ["Executive sign-off", "Report published", "Systems restored", "Enhanced monitoring ends"], correctAnswer: 0, explanation: "Executive sign-off ensures leadership has reviewed the response and accepted residual risk." },
      { id: "ir-q5-10", question: "A common business resumption challenge is:", options: ["Systems running too fast", "Application dependencies blocking processes even when individual systems work", "Too many IT staff", "Users adapting too quickly"], correctAnswer: 1, explanation: "Complex interdependencies between applications can prevent business processes from functioning." }
    ]
  },
  {
    quizId: "ir-q6",
    courseId: "incident-response",
    title: "Post-Incident Activities",
    description: "Test your knowledge of lessons learned, report writing, metrics, and continuous improvement.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "ir-q6-1", question: "What is the fundamental principle of a blameless post-mortem?", options: ["No one is responsible", "Only managers attend", "Focus on systemic improvements, not individual blame", "No documentation"], correctAnswer: 2, explanation: "Blameless post-mortems create psychological safety by focusing on systems, not individuals." },
      { id: "ir-q6-2", question: "When should lessons learned meetings be held?", options: ["24 hours", "1 month", "Within 2 weeks", "3 months"], correctAnswer: 2, explanation: "Within 2 weeks while details are fresh in participants' minds." },
      { id: "ir-q6-3", question: "Every action item should include:", options: ["A single owner, specific deadline, and success criteria", "Only a description", "Budget and ROI", "CEO approval"], correctAnswer: 0, explanation: "Single owner, specific deadline, and clear success criteria ensure accountability." },
      { id: "ir-q6-4", question: "Which metric measures total attacker presence time?", options: ["MTTD", "MTTR", "MTTE", "Dwell Time"], correctAnswer: 3, explanation: "Dwell time = total time from compromise to eradication. Target: < 7 days; average: ~200 days." },
      { id: "ir-q6-5", question: "The Executive Summary of an incident report should contain:", options: ["Full IOC lists", "Complete forensic methodology", "Only MITRE mapping", "Plain-language summary, business impact, key decisions, top recommendations"], correctAnswer: 3, explanation: "Executive summaries are 1 page, written in plain language for leadership." },
      { id: "ir-q6-6", question: "What does 're-compromise rate' measure?", options: ["How often eradication fails and the attacker returns", "New incident frequency", "Patch frequency", "False positive rate"], correctAnswer: 0, explanation: "High re-compromise rate indicates insufficient eradication thoroughness." },
      { id: "ir-q6-7", question: "If MTTD is trending up, invest in:", options: ["More handlers", "Detection capabilities (SIEM, EDR, threat intel)", "Eradication tools", "Faster backups"], correctAnswer: 1, explanation: "Increasing MTTD means slower detection — invest in detection capabilities." },
      { id: "ir-q6-8", question: "What timestamp format should incident reports use?", options: ["UTC", "Analyst's local time", "EST/EDT", "Affected system timezone"], correctAnswer: 0, explanation: "UTC prevents confusion when correlating events across systems and locations." },
      { id: "ir-q6-9", question: "At which maturity level does IR become metrics-driven?", options: ["Developing (2)", "Managed (4)", "Defined (3)", "Optimizing (5)"], correctAnswer: 1, explanation: "Level 4 (Managed) features metrics-driven continuous improvement and integrated threat intel." },
      { id: "ir-q6-10", question: "'Deploy EDR on uncovered systems' is which improvement category?", options: ["Detection", "Technology", "Process", "People"], correctAnswer: 1, explanation: "Deploying tools and expanding coverage falls under Technology improvements." }
    ]
  },
  {
    quizId: "th-q1",
    courseId: "threat-hunting",
    title: "Hunting Methodology & Frameworks",
    description: "Test your understanding of threat hunting methodology, the Hunting Maturity Model, and hypothesis-driven hunting.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "th-q1-1", question: "What is the primary difference between threat hunting and traditional detection?", options: ["Hunting uses automated alerts only", "Hunting is proactive and hypothesis-driven", "Hunting replaces SIEM entirely", "Hunting focuses on compliance"], correctAnswer: 1, explanation: "Threat hunting is proactive — analysts form hypotheses and actively search for threats rather than waiting for alerts." },
      { id: "th-q1-2", question: "How many levels does the Hunting Maturity Model (HMM) define?", options: ["3", "5", "4", "6"], correctAnswer: 1, explanation: "The HMM defines 5 levels: HM0 (Initial), HM1 (Minimal), HM2 (Procedural), HM3 (Innovative), and HM4 (Leading)." },
      { id: "th-q1-3", question: "At which HMM level does an organization begin routine data collection but lacks structured hunting?", options: ["HM0", "HM2", "HM1", "HM3"], correctAnswer: 2, explanation: "HM1 (Minimal) means the org collects data routinely but hunting is ad-hoc and relies on indicators." },
      { id: "th-q1-4", question: "What is the first step of hypothesis-driven hunting?", options: ["Formulate a testable hypothesis", "Collect evidence", "Write a report", "Deploy a new tool"], correctAnswer: 0, explanation: "Hypothesis-driven hunting begins with a testable hypothesis based on threat intelligence, experience, or anomaly patterns." },
      { id: "th-q1-5", question: "Which of the following is a characteristic of a good hunting hypothesis?", options: ["It is vague and broad", "It is based on gut feeling alone", "It requires no data", "It is testable and falsifiable"], correctAnswer: 3, explanation: "A good hypothesis is specific, testable, falsifiable, and grounded in threat intelligence or data patterns." },
      { id: "th-q1-6", question: "What does 'TTP' stand for in the context of threat hunting?", options: ["Tactics, Techniques, and Procedures", "Total Threat Prevention", "Threat Tracking Protocol", "Triage, Test, and Publish"], correctAnswer: 0, explanation: "TTP stands for Tactics, Techniques, and Procedures — the behavioral patterns of adversaries mapped in frameworks like MITRE ATT&CK." },
      { id: "th-q1-7", question: "Which hunting approach starts with known threat intelligence indicators?", options: ["Baseline hunting", "Intel-driven hunting", "Anomaly-based hunting", "Compliance hunting"], correctAnswer: 1, explanation: "Intel-driven hunting uses known IOCs, TTPs, or threat reports as starting points for investigation." },
      { id: "th-q1-8", question: "What is 'baseline hunting'?", options: ["Establishing normal behavior and looking for deviations", "Hunting for the newest malware", "Using only signature-based detection", "Hunting during business hours only"], correctAnswer: 0, explanation: "Baseline hunting establishes what 'normal' looks like in an environment and then searches for anomalous deviations." },
      { id: "th-q1-9", question: "At HM4 (Leading), what distinguishes the organization?", options: ["No automation", "Hunting is fully automated with no analysts", "They outsource all hunting", "Continuous hunting with custom tooling and automation feeding back into detection"], correctAnswer: 3, explanation: "HM4 organizations run continuous hunts with custom tooling and systematically convert findings into automated detections." },
      { id: "th-q1-10", question: "Why should hunt findings be documented even when no threat is found?", options: ["To blame analysts", "To justify headcount", "To refine baselines, improve hypotheses, and demonstrate coverage", "Documentation is optional"], correctAnswer: 2, explanation: "Documenting all hunts — including negatives — refines baselines, improves future hypotheses, and demonstrates security coverage." }
    ]
  },
  {
    quizId: "th-q2",
    courseId: "threat-hunting",
    title: "Threat Intelligence for Hunters",
    description: "Assess your knowledge of the Pyramid of Pain, IOC types, and intelligence-driven hunting.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "th-q2-1", question: "In David Bianco's Pyramid of Pain, which indicator is at the top (hardest for adversaries to change)?", options: ["Hash values", "IP addresses", "Domain names", "TTPs"], correctAnswer: 3, explanation: "TTPs sit at the top — changing behavior and tradecraft is far more costly for adversaries than rotating IPs or hashes." },
      { id: "th-q2-2", question: "Which indicator type is at the bottom of the Pyramid of Pain (easiest for attackers to change)?", options: ["Hash values", "Tools", "TTPs", "Network artifacts"], correctAnswer: 0, explanation: "Hash values are trivial to change — a single-bit modification produces a completely different hash." },
      { id: "th-q2-3", question: "What is a 'Diamond Model' used for in threat intelligence?", options: ["Pricing threat feeds", "Mapping relationships between adversary, capability, infrastructure, and victim", "Grading analyst performance", "Designing network architecture"], correctAnswer: 1, explanation: "The Diamond Model maps intrusion events across four vertices: adversary, capability, infrastructure, and victim." },
      { id: "th-q2-4", question: "What type of IOC is 'c:\\users\\public\\malware.exe'?", options: ["Network indicator", "Behavioral indicator", "Host-based indicator (file path)", "Email indicator"], correctAnswer: 2, explanation: "File paths are host-based indicators — they point to specific artifacts on an endpoint." },
      { id: "th-q2-5", question: "Why are IP-based IOCs considered low-value for long-term hunting?", options: ["They are too expensive", "Adversaries rotate IPs frequently and cheaply", "SIEM cannot ingest them", "They cause false negatives"], correctAnswer: 1, explanation: "IP addresses are cheap and easy for attackers to change, making them unreliable for sustained hunting." },
      { id: "th-q2-6", question: "What is 'threat intelligence enrichment'?", options: ["Adding context (reputation, geo, relationships) to raw indicators", "Deleting old IOCs", "Encrypting threat feeds", "Sharing IOCs publicly"], correctAnswer: 0, explanation: "Enrichment adds context like reputation scores, geolocation, WHOIS data, and relationships to raw indicators." },
      { id: "th-q2-7", question: "Which level of threat intelligence is most useful for SOC analysts and hunters?", options: ["Strategic", "Tactical/Operational", "Political", "Financial"], correctAnswer: 1, explanation: "Tactical and operational intelligence provides actionable IOCs, TTPs, and campaign details for day-to-day hunting." },
      { id: "th-q2-8", question: "What is a YARA rule used for?", options: ["Network monitoring", "User authentication", "Pattern-based malware identification using string/byte patterns", "Log rotation"], correctAnswer: 2, explanation: "YARA rules identify malware by matching string patterns, byte sequences, and conditions within files." },
      { id: "th-q2-9", question: "In the Pyramid of Pain, where do 'Tools' fall?", options: ["Middle-upper", "Middle-lower", "Bottom", "Top"], correctAnswer: 0, explanation: "Tools sit in the middle-upper region — replacing custom tooling is costly but not as hard as changing TTPs." },
      { id: "th-q2-10", question: "What is 'indicator fatigue'?", options: ["Running out of storage", "Network congestion", "Hardware failure", "Analysts overwhelmed by excessive low-quality IOCs reducing effectiveness"], correctAnswer: 3, explanation: "Indicator fatigue occurs when analysts are overwhelmed by massive volumes of low-quality IOCs, reducing detection effectiveness." }
    ]
  },
  {
    quizId: "th-q3",
    courseId: "threat-hunting",
    title: "Techniques & Tradecraft",
    description: "Quiz on adversary techniques including LOLBins, JA3 fingerprinting, and evasion methods.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "th-q3-1", question: "What are LOLBins?", options: ["A type of malware", "Linux-only tools", "Logging libraries", "Legitimate OS binaries abused by attackers to execute malicious actions"], correctAnswer: 3, explanation: "LOLBins (Living Off the Land Binaries) are legitimate system tools like PowerShell, certutil, and mshta abused by attackers." },
      { id: "th-q3-2", question: "Which Windows binary is commonly abused to download files from the internet?", options: ["notepad.exe", "explorer.exe", "calc.exe", "certutil.exe"], correctAnswer: 3, explanation: "certutil.exe has a -urlcache flag that attackers abuse to download payloads from remote servers." },
      { id: "th-q3-3", question: "What does JA3 fingerprinting identify?", options: ["TLS client configuration to fingerprint applications", "User identity", "File hashes", "Email headers"], correctAnswer: 0, explanation: "JA3 creates a hash of TLS client hello parameters, uniquely fingerprinting applications regardless of IP or domain." },
      { id: "th-q3-4", question: "What is 'process hollowing'?", options: ["Deleting processes", "Replacing the code inside a legitimate process with malicious code", "Creating new user accounts", "Clearing event logs"], correctAnswer: 1, explanation: "Process hollowing creates a legitimate process in suspended state, replaces its memory with malicious code, then resumes it." },
      { id: "th-q3-5", question: "Which MITRE ATT&CK tactic involves maintaining access after initial compromise?", options: ["Initial Access", "Persistence", "Exfiltration", "Reconnaissance"], correctAnswer: 1, explanation: "Persistence ensures the attacker maintains access across reboots, credential changes, or other disruptions." },
      { id: "th-q3-6", question: "What is 'DLL side-loading'?", options: ["Placing a malicious DLL where a legitimate program will load it", "Installing DLLs normally", "Updating system DLLs", "Compiling DLLs"], correctAnswer: 0, explanation: "DLL side-loading exploits the DLL search order by placing a malicious DLL in a location searched before the legitimate one." },
      { id: "th-q3-7", question: "What is the JA3S hash used for?", options: ["Client fingerprinting", "DNS resolution", "Server TLS configuration fingerprinting", "File integrity"], correctAnswer: 2, explanation: "JA3S fingerprints the server-side TLS hello response, complementing JA3 for full client-server profiling." },
      { id: "th-q3-8", question: "Which technique involves running malicious code entirely in memory without touching disk?", options: ["Disk encryption", "Fileless malware / in-memory execution", "File compression", "Normal installation"], correctAnswer: 1, explanation: "Fileless attacks execute entirely in memory, evading traditional file-based antivirus and leaving minimal forensic artifacts." },
      { id: "th-q3-9", question: "What Windows event log is most valuable for detecting LOLBin abuse?", options: ["Application log", "System log", "Sysmon (with process creation logging)", "Setup log"], correctAnswer: 2, explanation: "Sysmon provides detailed process creation, command-line, and parent-child relationship logging essential for LOLBin detection." },
      { id: "th-q3-10", question: "What is 'timestomping'?", options: ["Modifying file timestamps to blend in with legitimate files", "Changing system time zone", "Setting up NTP", "Creating time-based alerts"], correctAnswer: 0, explanation: "Timestomping changes file creation/modification times to make malicious files appear as if they've existed longer, evading timeline analysis." }
    ]
  },
  {
    quizId: "th-q4",
    courseId: "threat-hunting",
    title: "Endpoint Hunting",
    description: "Test your skills in hunting for threats on endpoints using process trees, autoruns, and memory analysis.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "th-q4-1", question: "What is the most important artifact to examine when hunting on endpoints?", options: ["Desktop wallpaper", "Process execution and parent-child relationships", "Screen resolution", "Installed fonts"], correctAnswer: 1, explanation: "Process trees reveal anomalous parent-child relationships, like Word spawning PowerShell, which indicate malicious activity." },
      { id: "th-q4-2", question: "Which parent process spawning cmd.exe is suspicious?", options: ["explorer.exe", "services.exe", "cmd.exe", "winword.exe"], correctAnswer: 3, explanation: "Microsoft Word (winword.exe) spawning cmd.exe is highly suspicious — it suggests macro-based malware execution." },
      { id: "th-q4-3", question: "What are 'autoruns' in the context of endpoint hunting?", options: ["Automatic software updates", "Persistence mechanisms that execute code at startup or login", "Automated scan schedules", "Auto-reply email rules"], correctAnswer: 1, explanation: "Autoruns are registry keys, startup folders, scheduled tasks, and services that execute automatically — common persistence locations." },
      { id: "th-q4-4", question: "Which tool is commonly used to enumerate Windows autorun locations?", options: ["Wireshark", "Nmap", "Sysinternals Autoruns", "Burp Suite"], correctAnswer: 2, explanation: "Sysinternals Autoruns comprehensively lists all auto-starting locations in Windows for persistence analysis." },
      { id: "th-q4-5", question: "What does an unsigned binary running from a temp directory suggest?", options: ["Normal software behavior", "A system update", "Potential malware — legitimate software is usually signed and installed properly", "A scheduled backup"], correctAnswer: 2, explanation: "Unsigned binaries in temp directories are a strong indicator of malware — legitimate software is typically signed and installed in standard locations." },
      { id: "th-q4-6", question: "What is 'stack ranking' in endpoint hunting?", options: ["Counting frequency of artifacts to find rare/anomalous ones", "Ranking analysts", "Prioritizing patches", "Stacking network packets"], correctAnswer: 0, explanation: "Stack ranking counts how often specific values appear — rare values (process names, paths, hashes) are more likely malicious." },
      { id: "th-q4-7", question: "Which Windows event ID logs process creation?", options: ["4624", "4688", "4720", "1102"], correctAnswer: 1, explanation: "Event ID 4688 logs process creation with details like process name, PID, and parent PID when auditing is enabled." },
      { id: "th-q4-8", question: "What is a suspicious indicator in scheduled task hunting?", options: ["Tasks created by Group Policy", "Tasks with Microsoft as publisher", "Tasks running Windows Update", "Tasks running binaries from user-writable directories with encoded commands"], correctAnswer: 3, explanation: "Scheduled tasks executing from user-writable paths with encoded PowerShell commands are strong persistence indicators." },
      { id: "th-q4-9", question: "What is 'memory forensics' useful for in hunting?", options: ["Detecting fileless malware, injected code, and hidden processes", "Increasing RAM", "Upgrading hardware", "Disk cleanup"], correctAnswer: 0, explanation: "Memory forensics captures running processes, injected code, network connections, and artifacts invisible to disk-based analysis." },
      { id: "th-q4-10", question: "Which tool is widely used for memory forensics?", options: ["Volatility", "Excel", "Notepad", "Paint"], correctAnswer: 0, explanation: "Volatility is the industry-standard open-source framework for memory forensics, supporting process, network, and malware analysis." }
    ]
  },
  {
    quizId: "th-q5",
    courseId: "threat-hunting",
    title: "Network & Cloud Hunting",
    description: "Assess your ability to hunt threats across network traffic and cloud environments.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "th-q5-1", question: "What is DNS beaconing?", options: ["Normal DNS resolution", "Updating DNS records", "DNS server maintenance", "Malware periodically querying a C2 domain at regular intervals"], correctAnswer: 3, explanation: "DNS beaconing is malware communicating with C2 via periodic DNS queries, often at suspiciously regular intervals." },
      { id: "th-q5-2", question: "Which network artifact helps detect DNS tunneling?", options: ["Short DNS queries", "Normal A record lookups", "Unusually long DNS query names with high entropy", "DHCP leases"], correctAnswer: 2, explanation: "DNS tunneling encodes data in query names, resulting in unusually long, high-entropy subdomain strings." },
      { id: "th-q5-3", question: "What is a 'long tail' analysis in network hunting?", options: ["Analyzing the longest cables", "Examining rare/infrequent connections that deviate from common patterns", "Studying network latency", "Measuring bandwidth"], correctAnswer: 1, explanation: "Long tail analysis focuses on rare connections — the uncommon destinations or patterns that are statistically anomalous and potentially malicious." },
      { id: "th-q5-4", question: "Which protocol is commonly abused for data exfiltration due to being rarely inspected?", options: ["All of the above", "DNS", "SMTP", "HTTP"], correctAnswer: 0, explanation: "DNS, HTTP, HTTPS, and SMTP are all commonly abused — DNS is particularly stealthy since it's rarely blocked or deeply inspected." },
      { id: "th-q5-5", question: "In cloud hunting, what is the most critical log source?", options: ["Cloud provider audit/activity logs (CloudTrail, Azure Activity Log)", "Application logs only", "Desktop event logs", "Print logs"], correctAnswer: 0, explanation: "Cloud audit logs (AWS CloudTrail, Azure Activity Log, GCP Audit Logs) record all API calls and are essential for cloud hunting." },
      { id: "th-q5-6", question: "What does an unusually high volume of outbound traffic to a single IP suggest?", options: ["Potential data exfiltration", "Normal backup", "Software update", "Email delivery"], correctAnswer: 0, explanation: "Large outbound transfers to a single IP, especially outside business hours, are a strong exfiltration indicator." },
      { id: "th-q5-7", question: "What is 'east-west traffic' in network hunting?", options: ["Traffic between continents", "Internet browsing", "North-south traffic", "Lateral movement traffic between internal systems"], correctAnswer: 3, explanation: "East-west traffic is internal lateral communication — hunting here reveals lateral movement after initial compromise." },
      { id: "th-q5-8", question: "Which cloud-specific threat involves misconfigured storage buckets?", options: ["DDoS", "Phishing", "Data exposure through publicly accessible storage (S3, Blob)", "Brute force"], correctAnswer: 2, explanation: "Misconfigured cloud storage (open S3 buckets, Azure Blobs) is a major cloud threat causing data exposure." },
      { id: "th-q5-9", question: "What is 'impossible travel' detection in cloud environments?", options: ["Detecting VPN usage", "Flagging logins from geographically distant locations in impossibly short timeframes", "Tracking flight bookings", "Monitoring travel expenses"], correctAnswer: 1, explanation: "Impossible travel flags when a user logs in from two distant locations faster than physically possible, indicating credential compromise." },
      { id: "th-q5-10", question: "What network hunting technique examines TLS certificate anomalies?", options: ["Packet size analysis", "Certificate transparency log analysis and self-signed cert detection", "MAC address lookup", "VLAN hopping"], correctAnswer: 1, explanation: "Analyzing TLS certificates for self-signed certs, unusual issuers, or short validity periods helps detect C2 infrastructure." }
    ]
  },
  {
    quizId: "th-q6",
    courseId: "threat-hunting",
    title: "Hunt Operations & Reporting",
    description: "Test your knowledge of hunt planning, automation, metrics, and reporting best practices.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "th-q6-1", question: "What should a hunt plan document include?", options: ["Hypothesis, data sources, techniques, tools, expected artifacts, and success criteria", "Only the hypothesis", "Just the analyst's name", "A list of all company assets"], correctAnswer: 0, explanation: "A complete hunt plan includes hypothesis, required data sources, analysis techniques, tools, expected artifacts, and success criteria." },
      { id: "th-q6-2", question: "What is the main benefit of converting hunt findings into automated detections?", options: ["Reduces headcount", "Eliminates the need for hunting", "Scales the hunt outcome so the same threat is automatically detected in the future", "Saves storage"], correctAnswer: 2, explanation: "Converting hunts into detections means the threat is automatically caught going forward, multiplying the value of each hunt." },
      { id: "th-q6-3", question: "Which tool/platform is commonly used for hunt automation and notebooks?", options: ["Microsoft Paint", "Notepad", "Calculator", "Jupyter Notebooks with MSTICPy"], correctAnswer: 3, explanation: "Jupyter Notebooks with MSTICPy provide reproducible, shareable hunt workflows with built-in security analysis capabilities." },
      { id: "th-q6-4", question: "What is the 'detection gap' metric?", options: ["Time between alerts", "The difference between known threats and what the organization can actually detect", "Network latency", "Analyst shift gaps"], correctAnswer: 1, explanation: "Detection gap measures the difference between threats that exist and those the org can detect — hunting directly reduces this gap." },
      { id: "th-q6-5", question: "What should a hunt report's executive summary contain?", options: ["High-level findings, business impact, risk assessment, and recommended actions", "Raw log data", "Only IOCs", "Tool configuration"], correctAnswer: 0, explanation: "Executive summaries provide leadership with findings, business impact, risk context, and clear recommended actions." },
      { id: "th-q6-6", question: "How should hunt metrics demonstrate program value?", options: ["Track hunts completed, findings discovered, detections created, and coverage improvements", "Count only hours worked", "Report only failures", "Count emails sent"], correctAnswer: 0, explanation: "Effective metrics include hunts completed, unique findings, new detections created, MITRE coverage improvements, and mean time to detect." },
      { id: "th-q6-7", question: "What is the purpose of a 'hunt backlog'?", options: ["Storing old data", "Maintaining a prioritized queue of hypotheses and hunt ideas for future execution", "Tracking employee PTO", "Archiving reports"], correctAnswer: 1, explanation: "A hunt backlog is a prioritized list of hypotheses and ideas, ensuring continuous hunting coverage aligned with threat landscape." },
      { id: "th-q6-8", question: "When should IOCs discovered during a hunt be shared?", options: ["Never", "Only internally", "Only after 6 months", "Immediately with the SOC/IR team and relevant threat intel sharing communities"], correctAnswer: 3, explanation: "IOCs should be shared immediately with SOC/IR for blocking and with threat intel sharing communities (ISACs) for collective defense." },
      { id: "th-q6-9", question: "What does 'MITRE ATT&CK coverage mapping' help hunters understand?", options: ["Network topology", "Employee skills", "Which adversary techniques the organization can and cannot detect, revealing blind spots", "Budget allocation"], correctAnswer: 2, explanation: "ATT&CK coverage mapping visualizes detection capabilities against known techniques, highlighting gaps to prioritize hunts." },
      { id: "th-q6-10", question: "What is the relationship between threat hunting and detection engineering?", options: ["They are unrelated", "Hunt findings feed detection engineering; detection gaps inform hunt priorities — a continuous cycle", "Hunting replaces detection", "Detection replaces hunting"], correctAnswer: 1, explanation: "Hunting and detection engineering form a virtuous cycle: hunts discover threats → detections are built → gaps inform new hunts." }
    ]
  },
  // ===================== Detection Engineering Basics =====================
  {
    quizId: "de-q1",
    courseId: "detection-engineering",
    title: "Detection Fundamentals",
    description: "Test your understanding of detection philosophy, coverage models, and alert quality.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "de-q1-1", question: "What is the most durable type of detection on the detection spectrum?", options: ["Anomaly-based", "Signature-based", "Behavioral", "Hash-based"], correctAnswer: 0, explanation: "Anomaly-based detections using statistical baselines are the most durable, lasting years compared to hash-based detections that last hours." },
      { id: "de-q1-2", question: "What is the 'assume breach' principle in detection engineering?", options: ["Assume all software has bugs", "Assume adversaries are already inside and validate controls through detection", "Assume breaches are unavoidable so don't invest in prevention", "Assume every alert is a breach"], correctAnswer: 1, explanation: "Assume breach means building detections that validate whether controls are working, not just blocking at the perimeter." },
      { id: "de-q1-3", question: "What is a good target false positive rate for a high-fidelity detection?", options: ["<50%", "<30%", "<5%", "<15%"], correctAnswer: 2, explanation: "High-fidelity detections should have a FP rate below 5% — analysts must trust alerts to be actionable." },
      { id: "de-q1-4", question: "What does 'detection as a product' mean?", options: ["Selling detections commercially", "Treating detections like software: requirements, testing, versioning, documentation, lifecycle management", "Only using commercial detection tools", "Detecting product defects"], correctAnswer: 1, explanation: "Detection as a product applies software engineering practices: requirements, testing, version control, and lifecycle management." },
      { id: "de-q1-5", question: "Why are behavior-based detections preferred over IOC-based detections?", options: ["Behaviors are more durable — attackers change IOCs easily but changing TTPs is costly", "They are easier to write", "They have zero false positives", "They require less data"], correctAnswer: 0, explanation: "Behaviors (TTPs) sit at the top of the Pyramid of Pain — changing tradecraft is far more costly for adversaries than rotating IOCs." },
      { id: "de-q1-6", question: "What is the primary cost of false positives in a SOC?", options: ["Storage costs", "Licensing fees", "Network bandwidth", "Analyst fatigue leading to missed real threats"], correctAnswer: 3, explanation: "False positives cause analyst fatigue and alert blindness, directly leading to missed real threats." },
      { id: "de-q1-7", question: "What framework is most commonly used to map detection coverage?", options: ["NIST CSF", "CIS Controls", "ISO 27001", "MITRE ATT&CK"], correctAnswer: 3, explanation: "MITRE ATT&CK maps adversary techniques and is the standard framework for measuring detection coverage." },
      { id: "de-q1-8", question: "What should you verify BEFORE writing any detection rule?", options: ["Budget approval", "Manager approval", "That the required log source is enabled and ingested", "That similar rules exist"], correctAnswer: 2, explanation: "No data = no detection. Always verify the log source is enabled, ingested into SIEM, and normalized before writing rules." },
      { id: "de-q1-9", question: "What is the '5-day rule' for noisy detections?", options: ["Review all rules every 5 days", "If a rule fires >5 FPs/day for 5 consecutive days, disable it immediately", "Deploy rules for 5 days before production", "Write 5 rules per day"], correctAnswer: 1, explanation: "The 5-day rule prevents persistent noise: disable immediately and schedule a rewrite rather than letting noise accumulate." },
      { id: "de-q1-10", question: "What is the detection engineering lifecycle order?", options: ["Requirements → Design → Development → Testing → Deployment → Operations → Retirement", "Deploy → Test → Design → Requirements", "Write → Deploy → Forget", "Test → Build → Ship"], correctAnswer: 0, explanation: "The full lifecycle is: Requirements → Design → Development → Testing → Deployment → Operations → Retirement." }
    ]
  },
  {
    quizId: "de-q2",
    courseId: "detection-engineering",
    title: "SIGMA Rules",
    description: "Assess your knowledge of SIGMA syntax, modifiers, and rule conversion.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "de-q2-1", question: "What format are SIGMA rules written in?", options: ["JSON", "XML", "YAML", "TOML"], correctAnswer: 2, explanation: "SIGMA rules use YAML format, making them human-readable and version-control friendly." },
      { id: "de-q2-2", question: "What is the purpose of the 'logsource' field in SIGMA?", options: ["Define the output format", "Specify what data to search (category + product)", "Set the rule severity", "Define the author"], correctAnswer: 1, explanation: "The logsource field abstracts the data source using category (process_creation) and product (windows), enabling vendor-neutral rules." },
      { id: "de-q2-3", question: "What does the SIGMA modifier 'endswith' do?", options: ["Marks end of rule", "Terminates processing", "Matches values ending with the specified string", "Counts endings"], correctAnswer: 2, explanation: "The endswith modifier performs a suffix match — e.g., Image|endswith: '\\powershell.exe' matches any path ending with that string." },
      { id: "de-q2-4", question: "How do you exclude false positives in a SIGMA rule?", options: ["Use a filter selection with 'not' in the condition", "Delete the rule", "Ignore them", "Email the SOC manager"], correctAnswer: 0, explanation: "Define a filter selection containing FP patterns, then use 'condition: selection and not filter' to exclude them." },
      { id: "de-q2-5", question: "What tool converts SIGMA rules to SIEM-specific queries?", options: ["pySigma / sigma-cli", "Wireshark", "Nmap", "Volatility"], correctAnswer: 0, explanation: "pySigma (sigma-cli) converts SIGMA rules to Splunk SPL, Elastic KQL, Sentinel KQL, and other SIEM query languages." },
      { id: "de-q2-6", question: "What does 'condition: 1 of selection*' mean?", options: ["Only the first selection", "Select one field", "Exactly one match required", "Any selection matching the wildcard pattern triggers the rule"], correctAnswer: 3, explanation: "'1 of selection*' means any selection whose name starts with 'selection' can trigger the rule — useful for multiple variants." },
      { id: "de-q2-7", question: "What is a SIGMA processing pipeline?", options: ["A data backup process", "Field name translation between SIGMA and target SIEM", "A network protocol", "A CI/CD tool"], correctAnswer: 1, explanation: "Processing pipelines map SIGMA's generic field names to SIEM-specific fields (e.g., Image → process.executable in ECS)." },
      { id: "de-q2-8", question: "How does SIGMA handle aggregation?", options: ["It cannot aggregate", "Using count(), sum() with timeframe in conditions", "Only in premium version", "Through external tools only"], correctAnswer: 1, explanation: "SIGMA supports aggregation functions like count() with timeframes — e.g., 'count(user) by src_ip > 10' in a 5m window." },
      { id: "de-q2-9", question: "What does the 'tags' field in SIGMA typically contain?", options: ["HTML tags", "Network tags", "File tags", "MITRE ATT&CK technique IDs"], correctAnswer: 3, explanation: "Tags map to ATT&CK techniques (e.g., attack.t1059.001) and tactics (e.g., attack.execution) for coverage mapping." },
      { id: "de-q2-10", question: "What is SigmaHQ?", options: ["The official community repository with 2000+ SIGMA detection rules", "A security company", "A SIEM product", "A certification body"], correctAnswer: 0, explanation: "SigmaHQ is the official open-source repository containing thousands of community-maintained SIGMA detection rules." }
    ]
  },
  {
    quizId: "de-q3",
    courseId: "detection-engineering",
    title: "YARA Signatures",
    description: "Quiz on YARA rule structure, pattern matching, and conditions.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "de-q3-1", question: "What are the three main sections of a YARA rule?", options: ["Header, body, footer", "Meta, strings, condition", "Input, process, output", "Name, pattern, action"], correctAnswer: 1, explanation: "YARA rules consist of meta (metadata), strings (patterns to match), and condition (logic determining a match)." },
      { id: "de-q3-2", question: "What does the YARA modifier 'wide' do?", options: ["Matches UTF-16 encoded strings", "Makes the rule apply to more files", "Increases scan width", "Broadens the condition"], correctAnswer: 0, explanation: "The 'wide' modifier matches UTF-16 encoded strings, which is how Windows often stores text internally." },
      { id: "de-q3-3", question: "What does 'uint16(0) == 0x5A4D' check in a YARA condition?", options: ["File size", "String count", "Whether the file is a PE executable (MZ header)", "Network port"], correctAnswer: 2, explanation: "0x5A4D is the MZ magic number at offset 0, indicating a Windows PE executable file." },
      { id: "de-q3-4", question: "What does the YARA 'xor' modifier do?", options: ["Encrypts the rule", "Disables the string", "Performs exclusive OR on results", "Automatically generates XOR-rotated variants of a string for matching"], correctAnswer: 3, explanation: "The xor modifier generates all (or specified range) XOR-rotated variants, detecting simple obfuscation automatically." },
      { id: "de-q3-5", question: "What does high entropy (>7.5) in a PE section indicate?", options: ["Normal text content", "Packed or encrypted content", "Empty section", "Debug information"], correctAnswer: 1, explanation: "Entropy above 7.5 strongly indicates packed, encrypted, or compressed content — common in malware." },
      { id: "de-q3-6", question: "Which YARA module is used to analyze PE file structure?", options: ["math", "hash", "elf", "pe"], correctAnswer: 3, explanation: "The pe module provides access to PE headers, sections, imports, exports, and signature information." },
      { id: "de-q3-7", question: "What is the purpose of hex wildcards (??) in YARA strings?", options: ["Match any byte value at that position", "Comment markers", "Error indicators", "Section delimiters"], correctAnswer: 0, explanation: "Hex wildcards (??) match any byte, handling variable opcodes or data within otherwise fixed byte patterns." },
      { id: "de-q3-8", question: "How should YARA rules be optimized for production scanning?", options: ["Use anchors, filesize filters, and avoid expensive regex", "Use only regex patterns", "Scan every file regardless of size", "Disable all modules"], correctAnswer: 0, explanation: "Optimized rules use 'at 0' anchors, filesize limits, and simple patterns to minimize scan time at scale." },
      { id: "de-q3-9", question: "What does '#suspicious_api > 5' check in a YARA condition?", options: ["String length", "Whether the string 'suspicious_api' appears more than 5 times", "File offset", "Rule priority"], correctAnswer: 1, explanation: "The # operator counts string occurrences — #suspicious_api > 5 checks if the string appears more than 5 times." },
      { id: "de-q3-10", question: "What is the recommended naming convention for YARA rules?", options: ["Random names", "Sequential numbers", "APT_Group_Technique_Description.yar", "Date-based only"], correctAnswer: 2, explanation: "Descriptive naming like APT_Group_Technique_Description.yar enables quick identification and organized rule management." }
    ]
  },
  {
    quizId: "de-q4",
    courseId: "detection-engineering",
    title: "Log Source Mastery",
    description: "Test your knowledge of Windows, Linux, network, and cloud log sources.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "de-q4-1", question: "Which Windows Event ID indicates a successful logon?", options: ["4624", "4625", "4688", "4698"], correctAnswer: 0, explanation: "Event ID 4624 logs successful authentication events with logon type, source, and account details." },
      { id: "de-q4-2", question: "Why is Sysmon essential for Windows detection?", options: ["It's built into Windows", "It only logs errors", "It replaces the event log service", "It provides detailed process creation, network, and registry logging beyond native auditing"], correctAnswer: 3, explanation: "Sysmon captures process command lines, hashes, network connections, and parent-child relationships that native auditing misses." },
      { id: "de-q4-3", question: "Which Sysmon event ID detects DLL side-loading?", options: ["Sysmon 1", "Sysmon 7 (Image Loaded)", "Sysmon 3", "Sysmon 10"], correctAnswer: 1, explanation: "Sysmon Event ID 7 logs DLL/image loads with hash and signature information, enabling DLL side-loading detection." },
      { id: "de-q4-4", question: "What Zeek log file captures DNS queries?", options: ["conn.log", "dns.log", "http.log", "ssl.log"], correctAnswer: 1, explanation: "Zeek's dns.log captures all DNS queries and responses with full detail for DNS-based threat detection." },
      { id: "de-q4-5", question: "Which cloud log source records all AWS API calls?", options: ["VPC Flow Logs", "CloudWatch", "S3 Access Logs", "CloudTrail"], correctAnswer: 3, explanation: "AWS CloudTrail records every API call made in the AWS account, essential for cloud security detection." },
      { id: "de-q4-6", question: "What is the purpose of log normalization?", options: ["Deleting duplicate logs", "Compressing logs", "Mapping diverse log formats to a common schema for consistent querying", "Encrypting logs"], correctAnswer: 2, explanation: "Normalization maps different field names (SourceIP, src_ip, srcaddr) to a common schema (source.ip) for cross-source correlation." },
      { id: "de-q4-7", question: "What does ECS stand for in the context of log normalization?", options: ["Elastic Common Schema", "Enterprise Control System", "Event Classification Standard", "Endpoint Collection Service"], correctAnswer: 0, explanation: "ECS (Elastic Common Schema) provides standardized field names for consistent log normalization across sources." },
      { id: "de-q4-8", question: "Which Linux log file records SSH authentication events?", options: ["/var/log/messages", "/var/log/kern.log", "/var/log/auth.log", "/var/log/boot.log"], correctAnswer: 2, explanation: "/var/log/auth.log (Debian/Ubuntu) or /var/log/secure (RHEL) records all authentication events including SSH." },
      { id: "de-q4-9", question: "What type of cloud detection identifies logins from geographically impossible locations?", options: ["Impossible travel detection", "DDoS detection", "Brute force detection", "Data loss prevention"], correctAnswer: 0, explanation: "Impossible travel flags logins from distant locations in impossibly short timeframes, indicating credential compromise." },
      { id: "de-q4-10", question: "What does log enrichment add to raw events?", options: ["More raw data", "Context: asset info, threat intel, GeoIP, user details", "Compression", "Encryption"], correctAnswer: 1, explanation: "Enrichment adds reputation, geolocation, asset criticality, and user context — transforming raw logs into actionable intelligence." }
    ]
  },
  {
    quizId: "de-q5",
    courseId: "detection-engineering",
    title: "Detection-as-Code",
    description: "Assess your understanding of version control, CI/CD, and testing for detections.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "de-q5-1", question: "Why should detection rules be stored in Git?", options: ["For history tracking, code review, rollback, and collaboration", "Because it's trendy", "Because SIEM storage is unreliable", "To encrypt them"], correctAnswer: 0, explanation: "Git provides change history, pull request reviews, instant rollback, team collaboration, and CI/CD automation." },
      { id: "de-q5-2", question: "What is Atomic Red Team?", options: ["A penetration testing company", "A SIEM product", "An open-source library of small, focused attack simulations mapped to ATT&CK", "A firewall rule set"], correctAnswer: 2, explanation: "Atomic Red Team provides pre-built, small attack tests for each ATT&CK technique to validate that detections fire correctly." },
      { id: "de-q5-3", question: "What should a detection CI/CD pipeline include?", options: ["Only deployment", "Lint, validate, convert, test (TP + FP), stage, deploy, and monitor", "Only testing", "Only linting"], correctAnswer: 1, explanation: "A complete pipeline covers YAML linting, schema validation, SIEM conversion, TP/FP testing, staged deployment, and monitoring." },
      { id: "de-q5-4", question: "What is a 'quality gate' in a detection pipeline?", options: ["A firewall rule", "An analyst approval form", "A SIEM license check", "A checkpoint that blocks deployment if criteria aren't met (e.g., missing tests)"], correctAnswer: 3, explanation: "Quality gates enforce standards: valid syntax, required fields, passing TP tests, and approved reviews before deployment." },
      { id: "de-q5-5", question: "How often should critical detections be validated?", options: ["Annually", "Quarterly", "Monthly", "Daily"], correctAnswer: 3, explanation: "Critical detections (credential theft, ransomware) should be validated daily to ensure they still fire correctly." },
      { id: "de-q5-6", question: "What is a True Negative (TN) test for a detection?", options: ["Verifying legitimate activity doesn't trigger the detection", "Testing when the rule fails", "Testing network connectivity", "Testing rule deletion"], correctAnswer: 0, explanation: "TN tests run benign activity similar to the attack pattern and verify the detection correctly stays silent." },
      { id: "de-q5-7", question: "What is the benefit of Infrastructure as Code for SIEM?", options: ["Faster queries", "Lower licensing costs", "Repeatable deployment, disaster recovery, auditing, and environment consistency", "Better dashboards"], correctAnswer: 2, explanation: "IaC enables rebuilding entire SIEM configurations from code, audit trails, and consistent dev/staging/production environments." },
      { id: "de-q5-8", question: "What branching strategy works best for detection rules?", options: ["No branches, commit to main", "Feature branches with pull requests merged to develop, then to main", "One branch per analyst", "Random branches"], correctAnswer: 1, explanation: "Feature branches (feature/detect-kerberoasting) with PR reviews ensure quality before merging to staging and production." },
      { id: "de-q5-9", question: "What should happen automatically when a detection is deployed?", options: ["Nothing", "Notifications to SOC team, JIRA ticket for playbook update, coverage dashboard update", "Delete old rules", "Restart SIEM"], correctAnswer: 1, explanation: "Automated notifications keep the SOC informed, playbook tickets ensure documentation, and dashboards reflect current coverage." },
      { id: "de-q5-10", question: "How does purple teaming relate to detection testing?", options: ["Red team executes techniques, blue team validates detections, gaps drive new detections", "They are unrelated", "Purple team replaces detection engineers", "Purple team only does compliance"], correctAnswer: 0, explanation: "Purple teaming directly validates detections: red executes, blue validates, gaps are identified, and new detections are built." }
    ]
  },
  {
    quizId: "de-q6",
    courseId: "detection-engineering",
    title: "Detection Operations",
    description: "Quiz on tuning, metrics, coverage mapping, and detection lifecycle management.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "de-q6-1", question: "How long should a detection run in alert-only mode before production?", options: ["1 day", "3 months", "1-2 weeks", "No alert-only period needed"], correctAnswer: 2, explanation: "1-2 weeks in alert-only mode allows observation of FP patterns and tuning before enabling full alerting." },
      { id: "de-q6-2", question: "What is 'detection decay'?", options: ["Detections losing effectiveness over time due to environment changes and adversary evolution", "Rules getting slower", "Storage degradation", "Network latency increase"], correctAnswer: 0, explanation: "Detection decay occurs as environments change, adversaries evolve, data sources drift, and configurations shift." },
      { id: "de-q6-3", question: "What ATT&CK coverage percentage indicates a mature detection program?", options: ["10-20%", "20-30%", "100%", "50-70%"], correctAnswer: 3, explanation: "Mature programs achieve 50-70% coverage of priority techniques. 100% is unrealistic; 20-30% is average." },
      { id: "de-q6-4", question: "What is the coverage scoring for 'IOC-based only, easily evaded'?", options: ["Score 0 (None)", "Score 1 (Minimal)", "Score 2 (Partial)", "Score 3 (Good)"], correctAnswer: 1, explanation: "Score 1 (Minimal) means only IOC-based detection exists — it's easily evaded and needs behavioral detection." },
      { id: "de-q6-5", question: "When should a detection rule be retired?", options: ["Never", "When the technique is no longer relevant, replaced by better detection, or data source is deprecated", "After 30 days", "When the analyst who wrote it leaves"], correctAnswer: 1, explanation: "Retire when: technique irrelevant, better replacement exists, data source deprecated, or persistent FPs despite tuning." },
      { id: "de-q6-6", question: "What is 'layered coverage' in detection engineering?", options: ["Multiple SIEM instances", "Multiple detections per technique using different data sources", "Layer 7 monitoring only", "Multiple analyst shifts"], correctAnswer: 1, explanation: "Layered coverage means having multiple detections for the same technique across different data sources — if one fails, others still detect." },
      { id: "de-q6-7", question: "What is a healthy detection engineering velocity?", options: ["1 rule per year", "100 rules per day", "8-12 new rules shipped per month", "Only during incidents"], correctAnswer: 2, explanation: "8-12 new production detections per month, combined with 15-20 tuned and 2-5 retired, represents healthy velocity." },
      { id: "de-q6-8", question: "What should a detection health check verify?", options: ["Only FP rate", "Only coverage mapping", "Only query syntax", "Still firing, still accurate, still needed, still performant, documentation current"], correctAnswer: 3, explanation: "Health checks verify five dimensions: firing (not broken), accurate (TP works), needed (relevant), performant (fast), documented (current)." },
      { id: "de-q6-9", question: "How often should a full detection audit be performed?", options: ["Annually", "Monthly", "Quarterly", "Weekly"], correctAnswer: 0, explanation: "Full detection inventory audits should occur annually, while alert quality is reviewed weekly and coverage assessed quarterly." },
      { id: "de-q6-10", question: "At which maturity level does a detection engineering program use CI/CD pipelines and testing?", options: ["Level 3 (Managed)", "Level 2 (Defined)", "Level 1 (Ad-hoc)", "Level 5 (Leading)"], correctAnswer: 0, explanation: "Level 3 (Managed) features CI/CD pipelines, automated testing, and metrics-driven detection engineering." }
    ]
  },
  // ==================== MALWARE ANALYSIS FUNDAMENTALS ====================

  {
    quizId: "ma-q1",
    courseId: "malware-analysis",
    title: "Malware Landscape & Lab Setup",
    description: "Test your knowledge of malware categories, threat actors, and safe analysis environments.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "ma-q1-1", question: "Which malware type self-replicates across networks without requiring user interaction?", options: ["Rootkit", "Trojan", "Virus", "Worm"], correctAnswer: 3, explanation: "Worms propagate autonomously by exploiting network vulnerabilities, unlike viruses that need a host program or trojans that rely on social engineering." },
      { id: "ma-q1-2", question: "What distinguishes a wiper from ransomware?", options: ["Wipers encrypt files for ransom", "Wipers require user interaction to execute", "Wipers only target Linux systems", "Wipers permanently destroy data with no recovery mechanism"], correctAnswer: 3, explanation: "Wipers are designed to permanently destroy data. NotPetya masqueraded as ransomware but was actually a wiper with no functional decryption." },
      { id: "ma-q1-3", question: "In a RaaS ecosystem, what role do Initial Access Brokers (IABs) play?", options: ["Sell compromised credentials and VPN access to affiliates", "Negotiate ransom payments", "Provide hosting for C2 servers", "Develop the ransomware code"], correctAnswer: 0, explanation: "IABs specialize in gaining initial access to organizations and selling that access to ransomware affiliates who carry out the attacks." },
      { id: "ma-q1-4", question: "Which VM distribution is specifically designed for Windows-based malware analysis?", options: ["SIFT Workstation", "REMnux", "FlareVM", "Kali Linux"], correctAnswer: 2, explanation: "FlareVM by Mandiant is a Windows-based distribution that installs analysis tools like x64dbg, Ghidra, and PE-bear on a Windows VM." },
      { id: "ma-q1-5", question: "Why should malware analysis VMs use host-only networking?", options: ["To improve analysis speed", "To prevent malware from reaching the real internet", "To enable cloud sandbox integration", "To allow remote access to the lab"], correctAnswer: 1, explanation: "Host-only networking isolates VMs so malware cannot reach the internet, preventing accidental infections and C2 communication with real infrastructure." },
      { id: "ma-q1-6", question: "What service does REMnux's INetSim provide in a malware analysis lab?", options: ["Real-time threat intelligence feeds", "Virtual machine management", "Simulated internet services (DNS, HTTP, SMTP)", "Automated malware classification"], correctAnswer: 2, explanation: "INetSim simulates DNS, HTTP, SMTP, and other internet services so malware behaves as if it has internet connectivity in an isolated environment." },
      { id: "ma-q1-7", question: "What is the standard password used for malware sample ZIP archives?", options: ["infected", "analysis", "malware", "password123"], correctAnswer: 0, explanation: "The convention is to use 'infected' as the password for password-protected ZIP archives containing malware samples." },
      { id: "ma-q1-8", question: "Which platform is a community-driven malware sample repository by abuse.ch?", options: ["VirusTotal", "MalwareBazaar", "Hybrid Analysis", "ANY.RUN"], correctAnswer: 1, explanation: "MalwareBazaar by abuse.ch is a free, community-driven repository where researchers share and download malware samples." },
      { id: "ma-q1-9", question: "What should you always do before executing malware in your analysis VM?", options: ["Update the OS", "Disable the firewall", "Connect to the internet", "Take a snapshot"], correctAnswer: 3, explanation: "Taking a snapshot before execution ensures you can revert to a clean state after analysis, preventing contamination between sessions." },
      { id: "ma-q1-10", question: "Which threat actor category typically uses the most sophisticated custom malware?", options: ["Script kiddies", "Hacktivists", "State-sponsored APT groups", "Financially motivated eCrime"], correctAnswer: 2, explanation: "State-sponsored APT groups have significant resources, enabling custom tooling, zero-day exploits, and sophisticated operational security." }
    ]
  },
  {
    quizId: "ma-q2",
    courseId: "malware-analysis",
    title: "Static Analysis Techniques",
    description: "Assess your understanding of file identification, string analysis, PE headers, and packing detection.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "ma-q2-1", question: "What are the magic bytes (hex) for a Windows PE executable?", options: ["4D 5A", "25 50 44 46", "7F 45 4C 46", "50 4B"], correctAnswer: 0, explanation: "4D 5A (MZ) is the DOS header signature for PE executables. 50 4B is ZIP, 7F 45 4C 46 is ELF, and 25 50 44 46 is PDF." },
      { id: "ma-q2-2", question: "What does ssdeep provide that SHA256 cannot?", options: ["Fuzzy matching to find similar files", "Faster computation", "Digital signatures", "Collision resistance"], correctAnswer: 0, explanation: "ssdeep generates fuzzy hashes that can identify similar files even with minor modifications, unlike cryptographic hashes which change completely with any alteration." },
      { id: "ma-q2-3", question: "What does an imphash identify?", options: ["The operating system version", "Samples built with the same import table", "The file's encryption algorithm", "Network communication patterns"], correctAnswer: 1, explanation: "Import hash (imphash) generates a hash of the imported functions, so samples from the same malware builder or toolkit share identical imphash values." },
      { id: "ma-q2-4", question: "What tool recovers obfuscated strings that basic extraction misses?", options: ["file command", "hexdump", "FLOSS", "strings command"], correctAnswer: 2, explanation: "FLOSS (FireEye Labs Obfuscated String Solver) automatically deobfuscates runtime-decoded and stack-constructed strings." },
      { id: "ma-q2-5", question: "In PE analysis, what does high section entropy (>7.0) indicate?", options: ["The file is digitally signed", "The section is likely encrypted or packed", "The file was compiled in debug mode", "The file has many imports"], correctAnswer: 1, explanation: "Entropy above 7.0 (near random) strongly suggests the section content is encrypted, compressed, or packed, hiding the original code." },
      { id: "ma-q2-6", question: "Which PE import combination strongly suggests process injection?", options: ["RegSetValueEx + RegCreateKeyEx", "VirtualAllocEx + WriteProcessMemory + CreateRemoteThread", "InternetOpenA + HttpSendRequest", "CreateFileA + ReadFile"], correctAnswer: 1, explanation: "This classic injection sequence allocates memory in another process, writes code there, and creates a remote thread to execute it." },
      { id: "ma-q2-7", question: "What does Detect It Easy (DiE) primarily identify?", options: ["Encryption algorithms", "Malware families", "Network protocols", "Packers, compilers, and protectors"], correctAnswer: 3, explanation: "DiE analyzes binary signatures to identify packers (UPX, Themida), compilers, and protectors used on the executable." },
      { id: "ma-q2-8", question: "A PE file with very few imports (only LoadLibrary and GetProcAddress) likely indicates what?", options: ["A simple utility program", "A .NET application", "A kernel driver", "A packed or dynamically-resolving binary"], correctAnswer: 3, explanation: "Minimal imports with LoadLibrary/GetProcAddress suggest the binary dynamically resolves API calls at runtime to hide its true capabilities from static analysis." },
      { id: "ma-q2-9", question: "How do you unpack a UPX-packed binary?", options: ["Run upx -d sample.exe", "Extract strings with FLOSS", "Manually debug with x64dbg", "Use Ghidra's decompiler"], correctAnswer: 0, explanation: "UPX provides a built-in decompression command (upx -d) that restores the original binary, making it one of the easiest packers to handle." },
      { id: "ma-q2-10", question: "What does a PE Rich header hash help identify?", options: ["The C2 server address", "The malware family", "The target operating system", "The build environment and toolchain"], correctAnswer: 3, explanation: "The Rich header records the compiler and linker versions used, linking samples compiled with the same development environment." }
    ]
  },
  {
    quizId: "ma-q3",
    courseId: "malware-analysis",
    title: "Dynamic & Behavioral Analysis",
    description: "Test your sandbox, process monitoring, and network capture skills.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "ma-q3-1", question: "Which sandbox allows real-time interactive analysis with manual clicking?", options: ["Cuckoo Sandbox", "VirusTotal Sandbox", "Joe Sandbox Cloud", "ANY.RUN"], correctAnswer: 3, explanation: "ANY.RUN provides an interactive mode where analysts can click through dialogs and installers in real-time during analysis." },
      { id: "ma-q3-2", question: "How does malware commonly detect it's running in a virtual machine?", options: ["Checking CPU speed", "Checking display resolution only", "Checking registry keys and MAC addresses", "Checking file sizes"], correctAnswer: 2, explanation: "Malware checks VM-specific registry keys (VMware, VirtualBox), MAC address prefixes, and hardware identifiers to detect virtualization." },
      { id: "ma-q3-3", question: "What Sysinternals tool captures real-time filesystem, registry, and process activity?", options: ["Process Monitor (ProcMon)", "Autoruns", "Process Hacker", "TCPView"], correctAnswer: 0, explanation: "Process Monitor captures detailed real-time filesystem, registry, process, and thread activity with powerful filtering." },
      { id: "ma-q3-4", question: "In Process Hacker, what does RWX memory permissions in a process indicate?", options: ["Read-only data section", "Kernel mode access", "Normal application behavior", "Possible code injection"], correctAnswer: 3, explanation: "Read-Write-Execute (RWX) memory regions are suspicious because legitimate code rarely needs all three permissions — it often indicates injected shellcode." },
      { id: "ma-q3-5", question: "What tool takes registry snapshots before and after malware execution?", options: ["ProcMon", "Regshot", "RegRipper", "Autoruns"], correctAnswer: 1, explanation: "Regshot takes two registry snapshots and compares them, revealing all keys and values added, modified, or deleted during execution." },
      { id: "ma-q3-6", question: "What does FakeNet-NG do in a malware analysis environment?", options: ["Scans files for viruses", "Intercepts and simulates network services locally", "Monitors CPU usage", "Decompiles binaries"], correctAnswer: 1, explanation: "FakeNet-NG intercepts all network traffic and simulates DNS, HTTP, SMTP, and other services so malware operates as if connected to the internet." },
      { id: "ma-q3-7", question: "Which Wireshark filter shows only DNS queries?", options: ["http.request", "ip.proto == 17", "tcp.port == 53", "dns"], correctAnswer: 3, explanation: "The 'dns' display filter shows all DNS traffic including queries and responses, useful for identifying C2 domains and DGA patterns." },
      { id: "ma-q3-8", question: "What network pattern indicates C2 beaconing?", options: ["Random burst traffic", "Single large data transfer", "Only outbound UDP traffic", "Regular interval connections with slight jitter"], correctAnswer: 3, explanation: "C2 beaconing shows regular check-in intervals (e.g., every 60 seconds) with slight random jitter to avoid detection." },
      { id: "ma-q3-9", question: "svchost.exe spawned by a non-services.exe parent process is a sign of what?", options: ["Driver installation", "Windows Update running", "Normal Windows behavior", "Malicious process masquerading"], correctAnswer: 3, explanation: "Legitimate svchost.exe is always spawned by services.exe. Any other parent indicates a malicious process impersonating svchost." },
      { id: "ma-q3-10", question: "Which API sequence indicates classic process injection?", options: ["OpenProcess → VirtualAllocEx → WriteProcessMemory → CreateRemoteThread", "WSAStartup → connect → send → recv", "CreateFile → ReadFile → CloseHandle", "RegOpenKeyEx → RegSetValueEx → RegCloseKey"], correctAnswer: 0, explanation: "This sequence opens a target process, allocates memory in it, writes shellcode, and creates a thread to execute it — the classic injection pattern." }
    ]
  },
  {
    quizId: "ma-q4",
    courseId: "malware-analysis",
    title: "Document & Script Malware",
    description: "Evaluate your ability to analyze macro-based documents, PDFs, and script threats.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "ma-q4-1", question: "Which VBA subroutine name causes automatic execution when a Word document is opened?", options: ["Sub Initialize()", "Sub Main()", "Sub AutoOpen()", "Sub OnLoad()"], correctAnswer: 2, explanation: "AutoOpen() and Document_Open() are VBA auto-execution triggers that run macros automatically when the document is opened." },
      { id: "ma-q4-2", question: "What tool extracts and analyzes VBA macros from Office documents?", options: ["Wireshark", "FLOSS", "olevba", "pdf-parser"], correctAnswer: 2, explanation: "olevba (part of oletools) extracts VBA macros, identifies suspicious patterns, and attempts automatic deobfuscation." },
      { id: "ma-q4-3", question: "What VBA obfuscation technique uses Chr(80) & Chr(111) & Chr(119)?", options: ["String reversal", "Base64 encoding", "XOR encryption", "Character code concatenation"], correctAnswer: 3, explanation: "Chr() converts ASCII codes to characters, building strings character-by-character to avoid string-based detection (Chr(80)&Chr(111)&Chr(119) = 'Pow')." },
      { id: "ma-q4-4", question: "Which PDF object type triggers automatic code execution on document open?", options: ["/Metadata", "/Pages", "/OpenAction", "/Encrypt"], correctAnswer: 2, explanation: "/OpenAction specifies actions to execute automatically when the PDF is opened, commonly used to trigger JavaScript payloads." },
      { id: "ma-q4-5", question: "What tool safely emulates VBA macro execution without opening Office?", options: ["ViperMonkey", "oletools", "CyberChef", "pdf-parser"], correctAnswer: 0, explanation: "ViperMonkey emulates VBA macro execution, revealing shell commands, downloaded URLs, and dropped files without running Office applications." },
      { id: "ma-q4-6", question: "In PowerShell deobfuscation, what should you replace IEX with for safe analysis?", options: ["Remove-Item", "Write-Output", "Set-Variable", "Start-Process"], correctAnswer: 1, explanation: "Replacing IEX (Invoke-Expression) with Write-Output prints the decoded command instead of executing it, safely revealing the payload." },
      { id: "ma-q4-7", question: "What is HTML smuggling?", options: ["Encoding malware in HTML comments", "JavaScript constructing and downloading payloads client-side", "Using HTML forms for phishing", "Injecting HTML into emails"], correctAnswer: 1, explanation: "HTML smuggling uses JavaScript to construct malicious payloads (via atob, Blob, createObjectURL) in the browser, bypassing email gateway scanning." },
      { id: "ma-q4-8", question: "How are malicious LNK files typically disguised?", options: ["With folder icons and innocent names", "As system updates", "As certificate files", "As font files"], correctAnswer: 0, explanation: "Malicious LNK files use folder icons from shell32.dll and names like 'Important Documents' to trick users into clicking." },
      { id: "ma-q4-9", question: "What tool safely analyzes malicious JScript files?", options: ["node.js", "Babel", "V8 debugger", "box-js"], correctAnswer: 3, explanation: "box-js is a JavaScript sandbox that safely emulates WScript/JScript execution, extracting URLs, dropped files, and shell commands." },
      { id: "ma-q4-10", question: "What typically comes inside an ISO file delivered via HTML smuggling?", options: ["Browser extensions", "Encrypted PDF documents", "A LNK file paired with a DLL payload", "Linux executables"], correctAnswer: 2, explanation: "HTML-smuggled ISO containers typically contain a malicious LNK shortcut that executes a co-located DLL via rundll32." }
    ]
  },
  {
    quizId: "ma-q5",
    courseId: "malware-analysis",
    title: "Reverse Engineering Fundamentals",
    description: "Test your knowledge of assembly, Ghidra, debugging, and C2 protocol analysis.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "ma-q5-1", question: "What does the x86 instruction 'XOR EAX, EAX' accomplish?", options: ["Sets EAX to zero", "Copies EAX to memory", "Encrypts EAX", "Compares EAX with zero"], correctAnswer: 0, explanation: "XOR-ing a register with itself always produces zero. This is the standard pattern for zeroing registers because it's faster than MOV EAX, 0." },
      { id: "ma-q5-2", question: "In x64 Windows calling convention, which register holds the first function argument?", options: ["RDI", "RDX", "RCX", "RAX"], correctAnswer: 2, explanation: "x64 Windows (fastcall) passes the first four arguments in RCX, RDX, R8, R9. Linux System V uses RDI, RSI, RDX, RCX." },
      { id: "ma-q5-3", question: "What does Ghidra's decompiler provide?", options: ["String decryption", "Network traffic analysis", "C-like pseudocode from binary disassembly", "Sandbox execution"], correctAnswer: 2, explanation: "Ghidra's decompiler converts assembly instructions back into readable C-like pseudocode, dramatically speeding up analysis." },
      { id: "ma-q5-4", question: "What technique should you use aggressively while analyzing code in Ghidra?", options: ["Renaming functions and variables", "Deleting unused code", "Running the sample", "Patching instructions"], correctAnswer: 0, explanation: "Renaming functions (FUN_00401000 → decrypt_config) and variables as you understand them makes the decompiled code progressively more readable." },
      { id: "ma-q5-5", question: "In x64dbg, what does F7 do?", options: ["Step Into (follow function calls)", "Toggle breakpoint", "Run to cursor", "Step Over (skip function calls)"], correctAnswer: 0, explanation: "F7 steps into function calls, following execution into the called function. F8 steps over, treating the call as a single instruction." },
      { id: "ma-q5-6", question: "Why are hardware breakpoints preferred when debugging packed malware?", options: ["They are faster", "They can monitor network traffic", "They work on Linux only", "They survive self-modifying code and are undetectable"], correctAnswer: 3, explanation: "Hardware breakpoints use CPU debug registers, so they survive code modification and aren't detectable by common anti-debugging techniques." },
      { id: "ma-q5-7", question: "What x64dbg plugin defeats most anti-debugging techniques automatically?", options: ["ScyllaHide", "IDA Sync", "x64dbg Automation", "OllyDump"], correctAnswer: 0, explanation: "ScyllaHide patches PEB flags, timing functions, and NTDLL hooks to automatically defeat IsDebuggerPresent, NtQueryInformationProcess, and timing checks." },
      { id: "ma-q5-8", question: "What is the most common encryption method used by malware for C2 communication?", options: ["AES-256", "Blowfish", "XOR", "RSA"], correctAnswer: 2, explanation: "XOR encryption is the most common in malware due to simplicity — it's trivially reversible but effective enough against basic detection." },
      { id: "ma-q5-9", question: "What is a Domain Generation Algorithm (DGA)?", options: ["An algorithm to register legitimate domains", "Code that generates pseudo-random domain names for C2", "A DNS security protocol", "A method to encrypt domain queries"], correctAnswer: 1, explanation: "DGAs generate pseudo-random domain names using seeds like dates, allowing malware to find C2 servers even if known domains are taken down." },
      { id: "ma-q5-10", question: "When malware calls LoadLibraryA + GetProcAddress repeatedly, what is it doing?", options: ["Checking for debuggers", "Installing device drivers", "Dynamically resolving API functions at runtime", "Loading configuration files"], correctAnswer: 2, explanation: "Dynamic API resolution loads DLLs and resolves function addresses at runtime, hiding the malware's true capabilities from the import table." }
    ]
  },
  {
    quizId: "ma-q6",
    courseId: "malware-analysis",
    title: "Reporting & Threat Intelligence",
    description: "Assess your malware reporting, IOC extraction, and attribution skills.",
    passingScore: 70,
    timeLimit: 15,
    questions: [
      { id: "ma-q6-1", question: "Which IOC type is considered 'atomic' (easily searchable)?", options: ["Attack timelines", "Behavioral patterns", "File hashes and IP addresses", "MITRE ATT&CK techniques"], correctAnswer: 2, explanation: "Atomic indicators like file hashes, IPs, and domains are simple, searchable values that can be directly queried in security tools." },
      { id: "ma-q6-2", question: "What format is the industry standard for machine-readable threat intelligence?", options: ["YAML", "STIX 2.1", "XML", "CSV"], correctAnswer: 1, explanation: "STIX (Structured Threat Information Expression) 2.1 is the standard JSON-based format for expressing and sharing cyber threat intelligence." },
      { id: "ma-q6-3", question: "What protocol enables automated IOC sharing between organizations?", options: ["SMTP", "LDAP", "TAXII", "SNMP"], correctAnswer: 2, explanation: "TAXII (Trusted Automated Exchange of Intelligence Information) is the transport protocol for sharing STIX-formatted threat intelligence." },
      { id: "ma-q6-4", question: "In a YARA rule, what does 'uint16(0) == 0x5A4D' check?", options: ["That the file is a PE executable (MZ header)", "String encoding", "File size", "Section count"], correctAnswer: 0, explanation: "This condition checks that the first two bytes are 0x4D5A (MZ in little-endian), confirming the file is a PE executable." },
      { id: "ma-q6-5", question: "What should a malware analysis report's executive summary focus on?", options: ["Tool configuration details", "Non-technical risk assessment and recommended actions", "Complete IOC listing", "Detailed assembly analysis"], correctAnswer: 1, explanation: "Executive summaries are for non-technical leadership and should focus on what the malware does, the risk level, and recommended actions." },
      { id: "ma-q6-6", question: "Which framework maps malware behaviors to standardized tactics and techniques?", options: ["NIST CSF", "MITRE ATT&CK", "OWASP", "ISO 27001"], correctAnswer: 1, explanation: "MITRE ATT&CK maps observed adversary behaviors to standardized tactics, techniques, and procedures, providing a shared language for threat reporting." },
      { id: "ma-q6-7", question: "What YARA string modifier matches both ASCII and UTF-16LE encodings?", options: ["ascii wide", "fullword", "nocase", "base64"], correctAnswer: 0, explanation: "Using both 'ascii' and 'wide' modifiers on a string ensures it matches whether encoded as ASCII or UTF-16LE (common in Windows)." },
      { id: "ma-q6-8", question: "For attribution, what confidence level requires multiple independent technical overlaps?", options: ["High", "Medium", "Confirmed", "Low"], correctAnswer: 1, explanation: "Medium confidence requires multiple technical overlaps such as code similarity AND infrastructure reuse. High adds operational and historical consistency." },
      { id: "ma-q6-9", question: "What tool compares two binaries for shared functions at the code level?", options: ["ssdeep", "BinDiff", "YARA", "CyberChef"], correctAnswer: 1, explanation: "BinDiff compares binary executables at the function level, identifying shared code between samples to link them to the same author or family." },
      { id: "ma-q6-10", question: "What does passive DNS data reveal about threat actor infrastructure?", options: ["Encryption keys", "Victim identities", "Malware source code", "Historical domain-to-IP mappings showing infrastructure reuse"], correctAnswer: 3, explanation: "Passive DNS records historical domain resolutions, revealing when domains pointed to which IPs and identifying infrastructure overlap between campaigns." }
    ]
  },
  // SOC ANALYST LEARNING PATH QUIZZES

  {
    quizId: "sap-q1",
    courseId: "soc-analyst-path",
    title: "SOC Analyst Foundations Quiz",
    description: "Test your understanding of the SOC analyst role, maturity models, and compliance.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "sap-q1-1", question: "What is the primary purpose of a SOC maturity model?", options: ["To determine salaries", "To assess and improve SOC capabilities", "To select SIEM vendors", "To rank analysts"], correctAnswer: 1, explanation: "SOC maturity models assess capabilities across People, Process, Technology, Services, and Governance." },
      { id: "sap-q1-2", question: "GDPR requires breach notification within how many hours?", options: ["24", "48", "72", "96"], correctAnswer: 2, explanation: "GDPR mandates 72-hour breach notification to supervisory authority." },
      { id: "sap-q1-3", question: "What is the minimum log retention under PCI-DSS?", options: ["7 years", "1 year", "3 years", "6 months"], correctAnswer: 1, explanation: "PCI-DSS requires 1 year retention with 3 months immediately available." },
      { id: "sap-q1-4", question: "Which NIST CSF functions are the SOC's primary focus?", options: ["Recover and Govern", "Identify and Protect", "Detect and Respond", "Protect and Recover"], correctAnswer: 2, explanation: "Detect and Respond are the primary SOC functions in NIST CSF." },
      { id: "sap-q1-5", question: "How many alerts should a typical L1 analyst triage per shift?", options: ["100-200", "10-20", "5-10", "30-60"], correctAnswer: 3, explanation: "A typical L1 analyst targets 30-60 alerts per shift." },
      { id: "sap-q1-6", question: "What percentage of alerts should typically be escalated?", options: ["1-3%", "25-35%", "50-60%", "5-15%"], correctAnswer: 3, explanation: "Typically 5-15% of alerts are escalated from L1 to L2." },
      { id: "sap-q1-7", question: "What compliance framework addresses healthcare data?", options: ["GDPR", "PCI-DSS", "SOX", "HIPAA"], correctAnswer: 3, explanation: "HIPAA addresses protection of healthcare data (ePHI)." },
      { id: "sap-q1-8", question: "SOX compliance applies to which organizations?", options: ["Educational institutions", "Healthcare providers", "Publicly traded companies", "Non-profits"], correctAnswer: 2, explanation: "SOX applies to publicly traded companies." },
      { id: "sap-q1-9", question: "What is the relationship between compliance and security?", options: ["They're the same", "Compliance is the floor — security goes beyond", "Security is unnecessary if compliant", "Compliance is the ceiling"], correctAnswer: 1, explanation: "Compliance is the minimum — true security goes beyond regulatory requirements." },
      { id: "sap-q1-10", question: "What should you do with an investigation VM after analyzing malware?", options: ["Keep using it", "Share with colleagues", "Connect to production", "Revert to clean snapshot"], correctAnswer: 3, explanation: "Always revert to clean snapshot after malware analysis." },
      { id: "sap-q1-11", question: "What is the first step in alert triage?", options: ["Run full forensic analysis", "Block source IP", "Escalate to management", "Review alert details and assess"], correctAnswer: 3, explanation: "First review alert details and initial assessment before any action." },
      { id: "sap-q1-12", question: "What is the purpose of shift handover?", options: ["Ensure continuity between shifts", "Report to management", "Evaluate performance", "Assign blame"], correctAnswer: 0, explanation: "Handovers ensure smooth transitions and prevent dropped incidents." },
      { id: "sap-q1-13", question: "Which tool is essential for a SOC analyst's toolkit?", options: ["Photoshop", "VirusTotal", "Social media", "Microsoft Word"], correctAnswer: 1, explanation: "VirusTotal is essential for analyzing hashes, URLs, IPs, and domains." },
      { id: "sap-q1-14", question: "How many SOC-CMM maturity levels exist?", options: ["3", "6", "4", "5"], correctAnswer: 1, explanation: "SOC-CMM has 6 levels (0-5): Incomplete through Optimizing." },
      { id: "sap-q1-15", question: "What does PCI-DSS Requirement 10 mandate?", options: ["Physical security", "Penetration testing", "Track and monitor all access to network resources", "Background checks"], correctAnswer: 2, explanation: "Req 10 mandates tracking and monitoring all access to network resources and cardholder data." }
    ]
  },
  {
    quizId: "sap-q2",
    courseId: "soc-analyst-path",
    title: "Network Traffic Analysis Quiz",
    description: "Evaluate your TCP/IP analysis, DNS threats, and packet inspection skills.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "sap-q2-1", question: "What indicates a SYN scan?", options: ["SYN→SYN-ACK→RST (no final ACK)", "ACK only", "FIN+PSH+URG", "SYN→ACK→RST"], correctAnswer: 0, explanation: "SYN scan sends SYN, receives SYN-ACK, sends RST without completing handshake." },
      { id: "sap-q2-2", question: "What indicates C2 beaconing?", options: ["Regular intervals with consistent sizes to same destination", "Random connections to many IPs", "DNS to google.com", "Large CDN downloads"], correctAnswer: 0, explanation: "C2 beaconing shows regular timing with consistent packet sizes to the same destination." },
      { id: "sap-q2-3", question: "Windows systems typically use what TTL value?", options: ["128", "64", "255", "32"], correctAnswer: 0, explanation: "Windows uses TTL=128, Linux uses TTL=64." },
      { id: "sap-q2-4", question: "What is DNS tunneling?", options: ["DNS over HTTPS", "Encrypting DNS", "Encoding data in DNS queries to bypass firewalls", "Blocking DNS"], correctAnswer: 2, explanation: "DNS tunneling encodes data in subdomain labels to communicate covertly." },
      { id: "sap-q2-5", question: "What indicates DGA malware?", options: ["High bandwidth", "DNS misconfiguration", "Normal browsing", "Excessive NXDomain responses from one host"], correctAnswer: 3, explanation: "DGA generates many domains, most of which don't resolve (NXDomain)." },
      { id: "sap-q2-6", question: "What does fast-flux DNS involve?", options: ["Slow resolution", "Rapid IP rotation with very low TTL", "DNS caching", "Static IPs"], correctAnswer: 1, explanation: "Fast-flux rapidly rotates IPs (every 30-60s) using very low TTL." },
      { id: "sap-q2-7", question: "Which User-Agent is suspicious?", options: ["Python-urllib/3.8", "Chrome/120.0", "Safari/537.36", "Mozilla/5.0 (Windows NT 10.0)"], correctAnswer: 0, explanation: "Python-urllib indicates automated scripting, unusual for normal browsing." },
      { id: "sap-q2-8", question: "Wireshark filter for HTTP POST requests?", options: ["filter.http.post", "http.post", "tcp.method == POST", "http.request.method == \"POST\""], correctAnswer: 3, explanation: "The correct filter is http.request.method == \"POST\"." },
      { id: "sap-q2-9", question: "What is JA3 fingerprinting used for?", options: ["Identifying TLS client implementations/malware", "DNS", "Passwords", "File types"], correctAnswer: 0, explanation: "JA3 fingerprints TLS client hellos to identify specific malware families." },
      { id: "sap-q2-10", question: "Which port is used for SMB lateral movement?", options: ["445", "22", "80", "443"], correctAnswer: 0, explanation: "Port 445 (SMB) is commonly used for lateral movement and ransomware." },
      { id: "sap-q2-11", question: "What DNS indicator suggests tunneling?", options: ["Standard A records", "Business hours queries", "Long subdomains with high entropy", "Short queries"], correctAnswer: 2, explanation: "DNS tunneling creates long, high-entropy subdomain labels." },
      { id: "sap-q2-12", question: "How to follow a TCP conversation in Wireshark?", options: ["Edit → Preferences", "Right-click → Follow → TCP Stream", "Statistics → Conversations", "Analyze → Stream"], correctAnswer: 1, explanation: "Right-click a packet and Follow → TCP Stream reconstructs the conversation." },
      { id: "sap-q2-13", question: "What does XMAS scan send?", options: ["No flags", "FIN + PSH + URG", "ACK only", "SYN only"], correctAnswer: 1, explanation: "XMAS scan sets FIN, PSH, and URG flags — unusual combination for evasion." },
      { id: "sap-q2-14", question: "Purpose of proxy log analysis in SOC?", options: ["Network speed", "Employee productivity", "Bandwidth management", "Detecting web threats, exfiltration, and C2"], correctAnswer: 3, explanation: "Proxy logs detect web threats, data exfiltration, and C2 communication." },
      { id: "sap-q2-15", question: "What is a DGA domain characteristic?", options: ["Only .com TLD", "High entropy random characters", "Static IP", "Long meaningful words"], correctAnswer: 1, explanation: "DGA domains have high entropy (random-looking characters) like xkq8r3m2p.com." }
    ]
  },
  {
    quizId: "sap-q3",
    courseId: "soc-analyst-path",
    title: "SIEM Mastery Assessment",
    description: "Test SIEM queries, correlation rules, and dashboard skills.",
    passingScore: 70,
    timeLimit: 25,
    questions: [
      { id: "sap-q3-1", question: "What function counts unique values in SIEM?", options: ["dc() / distinct_count()", "count()", "sum()", "avg()"], correctAnswer: 0, explanation: "dc() counts unique values, useful for finding hosts accessed by a single IP." },
      { id: "sap-q3-2", question: "Best approach to designing correlation rules?", options: ["Start with MITRE ATT&CK technique", "Single-event rules only", "Copy from others", "Start with log sources"], correctAnswer: 0, explanation: "Threat-informed design starts with the attack technique, then maps to data sources." },
      { id: "sap-q3-3", question: "Why is multi-event correlation better?", options: ["Easier to write", "More alerts", "Reduces false positives", "Less resources"], correctAnswer: 2, explanation: "Multiple conditions produce higher confidence alerts." },
      { id: "sap-q3-4", question: "Process chain indicating macro attack?", options: ["lsass→csrss", "explorer→chrome", "winword→cmd→powershell", "svchost→services"], correctAnswer: 2, explanation: "Office apps spawning CLI tools indicates macro execution." },
      { id: "sap-q3-5", question: "Max panels for a SOC dashboard?", options: ["2-4", "20-30", "As many as possible", "8-10"], correctAnswer: 3, explanation: "Limit to 8-10 panels to prevent information overload." },
      { id: "sap-q3-6", question: "First step in log source onboarding?", options: ["Write rules", "Identify source and log format", "Create dashboards", "Install agent"], correctAnswer: 1, explanation: "First identify the device, events, format, and expected volume." },
      { id: "sap-q3-7", question: "What is field normalization?", options: ["Encrypting values", "Mapping vendor fields to common schema", "Deleting fields", "Reducing count"], correctAnswer: 1, explanation: "Normalization maps source-specific fields to unified schema for cross-source correlation." },
      { id: "sap-q3-8", question: "How to handle high FP rate on a rule?", options: ["Blame vendor", "Add whitelists, adjust thresholds, add context", "Delete rule", "Ignore alerts"], correctAnswer: 1, explanation: "Tune with whitelists, adjusted thresholds, and context conditions." },
      { id: "sap-q3-9", question: "What makes a dashboard 'actionable'?", options: ["Colorful charts", "Drill-down links to detailed searches", "Many data points", "Complex visuals"], correctAnswer: 1, explanation: "Actionable dashboards allow clicking any panel to drill into underlying data." },
      { id: "sap-q3-10", question: "SIEM query detecting RDP lateral movement?", options: ["Count distinct targets per source for logon type 10", "Filter by user agent", "Count total logins", "Search failed passwords"], correctAnswer: 0, explanation: "Count distinct target hosts per source IP for RDP (logon type 10)." },
      { id: "sap-q3-11", question: "What is a cool-down period?", options: ["Time between updates", "Suppression window preventing repeated alerts", "SIEM restart time", "User timeout"], correctAnswer: 1, explanation: "Cool-downs suppress repeated alerts for the same condition within a time window." },
      { id: "sap-q3-12", question: "What to validate after log source onboarding?", options: ["Only event receipt", "Only connection", "Just field names", "Timestamps, parsing, volume, searchability, no gaps"], correctAnswer: 3, explanation: "Validate timestamps, field parsing, volume, searchability, and absence of gaps." },
      { id: "sap-q3-13", question: "First query optimization technique?", options: ["Search all indices", "Remove all filters", "Apply time and source filters early", "Regex everywhere"], correctAnswer: 2, explanation: "Filter early to reduce data the SIEM needs to process." },
      { id: "sap-q3-14", question: "Ransomware detection rule is based on?", options: ["Email volume", "High file renames with known ransomware extensions", "Network volume", "Login patterns"], correctAnswer: 1, explanation: "Detect rapid file renames (>50 in 5 min) with extensions like .encrypted, .locked." },
      { id: "sap-q3-15", question: "What is baseline deviation used for?", options: ["Deleting logs", "User accounts", "SIEM setup", "Detecting anomalies vs historical norms"], correctAnswer: 3, explanation: "Baseline deviation compares current behavior to historical averages for anomaly detection." }
    ]
  },
  {
    quizId: "sap-q4",
    courseId: "soc-analyst-path",
    title: "Endpoint Investigation Quiz",
    description: "Assess endpoint forensics on Windows and Linux.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "sap-q4-1", question: "Expected parent of svchost.exe?", options: ["services.exe", "explorer.exe", "csrss.exe", "winlogon.exe"], correctAnswer: 0, explanation: "svchost.exe should always be a child of services.exe." },
      { id: "sap-q4-2", question: "What are LOLBins?", options: ["Linux commands", "Logging binaries", "Legitimate Windows binaries abused by attackers", "Malware types"], correctAnswer: 2, explanation: "LOLBins are legitimate tools (certutil, mshta) abused for malicious purposes." },
      { id: "sap-q4-3", question: "Common persistence registry key?", options: ["HKLM\\SAM", "HKLM\\HARDWARE", "HKLM\\...\\CurrentVersion\\Run", "HKCU\\Console"], correctAnswer: 2, explanation: "Run keys auto-start programs listed there." },
      { id: "sap-q4-4", question: "What is process hollowing?", options: ["Running hollow executable", "Monitoring memory", "Deleting process", "Creating suspended process, replacing memory with malicious code"], correctAnswer: 3, explanation: "Process hollowing replaces legitimate process memory with malicious code." },
      { id: "sap-q4-5", question: "Linux command for network connections with PIDs?", options: ["ls -la", "ss -tnp", "df -h", "cat /etc/passwd"], correctAnswer: 1, explanation: "ss -tnp shows TCP connections with associated process IDs." },
      { id: "sap-q4-6", question: "Volatility plugin for injected code?", options: ["netscan", "hivelist", "malfind", "pslist"], correctAnswer: 2, explanation: "malfind finds suspicious RWX memory regions and PE headers." },
      { id: "sap-q4-7", question: "Why capture memory before shutdown?", options: ["It's faster", "Memory is permanent", "Volatile data is lost on shutdown", "Save disk space"], correctAnswer: 2, explanation: "Running processes, connections, and decrypted data disappear on shutdown." },
      { id: "sap-q4-8", question: "Linux persistence through user login?", options: ["/home/user/.bashrc", "/boot/grub/grub.cfg", "/etc/hostname", "/var/log/syslog"], correctAnswer: 0, explanation: ".bashrc executes every bash shell — attackers add malicious commands." },
      { id: "sap-q4-9", question: "PAGE_EXECUTE_READWRITE indicates?", options: ["Potentially injected code", "Normal behavior", "Kernel protection", "Memory corruption"], correctAnswer: 0, explanation: "RWX permissions are unusual and often indicate injected shellcode." },
      { id: "sap-q4-10", question: "Find recently modified PHP files?", options: ["grep php /etc/passwd", "find /var/www -name '*.php' -mtime -7", "cat index.php", "ls /var/www"], correctAnswer: 1, explanation: "find with -mtime -7 finds PHP files modified in last 7 days for web shell detection." },
      { id: "sap-q4-11", question: "Tool showing ALL Windows autostart locations?", options: ["Process Explorer", "Process Monitor", "Autoruns", "TCPView"], correctAnswer: 2, explanation: "Autoruns shows every autostart location including Run keys, services, tasks, drivers, WMI." },
      { id: "sap-q4-12", question: "Key indicator of certutil abuse?", options: ["Verifying signatures", "Viewing cert stores", "Certificate management", "-urlcache -split -f to download from external URLs"], correctAnswer: 3, explanation: "certutil with -urlcache -split -f downloading from external URLs is common LOLBin abuse." },
      { id: "sap-q4-13", question: "pslist vs psscan comparison reveals?", options: ["Memory usage", "File system", "Hidden/unlinked processes", "Bandwidth"], correctAnswer: 2, explanation: "psscan scans all memory while pslist uses active lists — differences reveal hidden processes." },
      { id: "sap-q4-14", question: "WMI persistence namespace?", options: ["root/cimv2", "root/security", "root/subscription", "root/default"], correctAnswer: 2, explanation: "root/subscription contains WMI event subscriptions for fileless persistence." },
      { id: "sap-q4-15", question: "First triage step on compromised Linux server?", options: ["Reinstall OS", "Reboot", "Delete logs", "Check processes, network, and logins"], correctAnswer: 3, explanation: "Check ps auxf, ss -tnp, and last/w before any remediation." }
    ]
  },
  {
    quizId: "sap-q5",
    courseId: "soc-analyst-path",
    title: "Phishing & Email Analysis Quiz",
    description: "Validate email header analysis and phishing response skills.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "sap-q5-1", question: "Email headers should be read in which order?", options: ["By type", "Alphabetically", "Bottom to top", "Top to bottom"], correctAnswer: 2, explanation: "Bottom-to-top — oldest entries are at the bottom." },
      { id: "sap-q5-2", question: "What does SPF verify?", options: ["Content", "Encryption", "Recipient identity", "Whether sending IP is authorized for the domain"], correctAnswer: 3, explanation: "SPF verifies that the sending IP is authorized for the sender's domain." },
      { id: "sap-q5-3", question: "Strong BEC/phishing indicator in headers?", options: ["From differs from Reply-To", "Standard X-Mailer", "Valid DKIM", "SPF pass"], correctAnswer: 0, explanation: "Mismatched From and Reply-To means replies go to attacker's address." },
      { id: "sap-q5-4", question: "Tool for extracting VBA macros?", options: ["Wireshark", "Nmap", "Autoruns", "olevba (oletools)"], correctAnswer: 3, explanation: "olevba extracts and analyzes VBA macros from Office documents." },
      { id: "sap-q5-5", question: "Why use ISO/IMG as attachments?", options: ["Bypass Mark-of-the-Web", "Better compression", "Smaller files", "Easier to create"], correctAnswer: 0, explanation: "Files inside ISO don't get MOTW flag, allowing execution without warnings." },
      { id: "sap-q5-6", question: "What is HTML smuggling?", options: ["Compressing HTML", "Hiding HTML in images", "Blocking HTML", "Base64 payloads in JavaScript that auto-download"], correctAnswer: 3, explanation: "HTML smuggling uses JavaScript to decode and auto-download Base64 payloads." },
      { id: "sap-q5-7", question: "First action with suspicious URL?", options: ["Block immediately", "Click it", "Share in chat", "Defang it"], correctAnswer: 3, explanation: "Always defang URLs first to prevent accidental clicking." },
      { id: "sap-q5-8", question: "What is a homoglyph attack?", options: ["Encrypting domains", "Similar characters from different alphabets to spoof domains", "Expired domains", "Long domains"], correctAnswer: 1, explanation: "Homoglyphs use visually similar characters (Cyrillic 'а' vs Latin 'a')." },
      { id: "sap-q5-9", question: "After credentials entered on phishing page?", options: ["Just monitor", "Wait 24h", "Send warning", "Reset passwords, revoke sessions, check forwarding rules"], correctAnswer: 3, explanation: "Immediate reset, session revocation, and forwarding rule check are critical." },
      { id: "sap-q5-10", question: "AutoOpen in VBA indicates?", options: ["Macro runs when document opens", "Auto-save", "Document auto-opens", "Auto-update"], correctAnswer: 0, explanation: "AutoOpen() executes VBA code automatically when the document is opened." },
      { id: "sap-q5-11", question: "What to do with phishing beyond reported email?", options: ["Forward to IT", "Delete reported only", "Ignore", "Purge similar emails from ALL mailboxes"], correctAnswer: 3, explanation: "Search for and purge all instances across all mailboxes." },
      { id: "sap-q5-12", question: "What does DMARC combine?", options: ["DNS and HTTP", "SPF and DKIM", "Encryption and signing", "AV and firewall"], correctAnswer: 1, explanation: "DMARC combines SPF and DKIM for policy-level authentication." },
      { id: "sap-q5-13", question: "What determines phishing severity?", options: ["Time of day", "Sender country", "Email length", "Recipients, clicks, payload type, target dept"], correctAnswer: 3, explanation: "Severity considers recipient count, clicks, payload type, and target sensitivity." },
      { id: "sap-q5-14", question: "Why check email forwarding rules after compromise?", options: ["Storage", "Attackers set rules to maintain access after password reset", "Compliance", "Performance"], correctAnswer: 1, explanation: "Forwarding rules let attackers keep receiving emails even after password change." },
      { id: "sap-q5-15", question: "Purpose of certificate transparency logs?", options: ["Verify SSL", "Find related domains using same cert infrastructure", "Create certs", "Block certs"], correctAnswer: 1, explanation: "CT logs reveal all certificates for a domain, discovering related phishing infrastructure." }
    ]
  },
  {
    quizId: "sap-q6",
    courseId: "soc-analyst-path",
    title: "Incident Handling Final Exam",
    description: "Comprehensive exam on incident handling, reporting, and evidence.",
    passingScore: 80,
    timeLimit: 35,
    questions: [
      { id: "sap-q6-1", question: "Correct evidence collection order?", options: ["Network→Disk→Memory", "Backups→Disk→Memory", "Memory→Network→Processes→Disk→Backups", "Disk→Memory→Network"], correctAnswer: 2, explanation: "Most volatile to least: Memory → Network → Processes → Disk → Backups." },
      { id: "sap-q6-2", question: "Hash algorithm for evidence integrity?", options: ["SHA256", "Base64", "MD5", "CRC32"], correctAnswer: 0, explanation: "SHA256 is the standard for evidence hashing in legal proceedings." },
      { id: "sap-q6-3", question: "Blameless PIR focuses on?", options: ["Improving systems and processes", "Punishment", "Reducing headcount", "Who caused it"], correctAnswer: 0, explanation: "Focus on process improvements, not individual blame." },
      { id: "sap-q6-4", question: "Active ransomware on multiple systems is?", options: ["P1 Critical", "P4", "P2", "P3"], correctAnswer: 0, explanation: "Active ransomware encryption is Critical (P1) requiring immediate response." },
      { id: "sap-q6-5", question: "Executive summary should contain?", options: ["Tool list", "What happened, impact, containment status — non-technical", "Only IOCs", "Technical details"], correctAnswer: 1, explanation: "Executive summaries are for non-technical stakeholders." },
      { id: "sap-q6-6", question: "Why not analyze original evidence?", options: ["Modification compromises legal admissibility", "Encrypted", "Too slow", "Special tools needed"], correctAnswer: 0, explanation: "Working on copies preserves integrity for legal proceedings." },
      { id: "sap-q6-7", question: "PIRs must produce?", options: ["Evaluations", "Budget requests", "Blame report", "Specific, assigned, deadline-driven actions"], correctAnswer: 3, explanation: "Concrete action items with owners and deadlines are essential." },
      { id: "sap-q6-8", question: "Incident reports should use which timezone?", options: ["Local", "EST", "UTC", "Attacker's"], correctAnswer: 2, explanation: "UTC eliminates timezone confusion across geographic locations." },
      { id: "sap-q6-9", question: "When uncertain about severity?", options: ["Ask colleague", "Escalate UP", "Classify low", "Wait for data"], correctAnswer: 1, explanation: "Escalate UP — delays in critical incidents cause more damage than false alarms." },
      { id: "sap-q6-10", question: "Chain of custody must include?", options: ["Just hash", "Description only", "Who, when, how, storage, every handoff with timestamps", "Analyst name only"], correctAnswer: 2, explanation: "Track every interaction for legal admissibility." },
      { id: "sap-q6-11", question: "Key metric after PIR improvements?", options: ["Recurrence rate of same incident type", "Email volume", "Satisfaction", "Meetings held"], correctAnswer: 0, explanation: "Recurrence rate measures whether improvements were effective." },
      { id: "sap-q6-12", question: "IOCs in reports should be?", options: ["Live and clickable", "Encrypted", "Hidden", "Defanged"], correctAnswer: 3, explanation: "Defanged IOCs prevent accidental clicks on malicious links." },
      { id: "sap-q6-13", question: "How to balance threat and impact in classification?", options: ["Only impact", "All critical", "Matrix combining both", "Only threat"], correctAnswer: 2, explanation: "Use a matrix: High threat + High impact = P1." },
      { id: "sap-q6-14", question: "P1 incident response time?", options: ["< 4h", "< 15 min", "< 24h", "< 1h"], correctAnswer: 1, explanation: "Critical incidents require immediate response within 15 minutes." },
      { id: "sap-q6-15", question: "Most damaging PIR anti-pattern?", options: ["Blaming individuals", "Long meetings", "Scheduling conflicts", "Too many actions"], correctAnswer: 0, explanation: "Blaming individuals kills reporting culture." },
      { id: "sap-q6-16", question: "Should dead ends be documented in reports?", options: ["Always — prevents repeating same work", "Never", "Only if asked", "Internal notes only"], correctAnswer: 0, explanation: "Dead ends prevent others from repeating unsuccessful investigation steps." },
      { id: "sap-q6-17", question: "Monitor compromised accounts for how long?", options: ["72h", "1 month", "24h", "1 week"], correctAnswer: 0, explanation: "Monitor at least 72 hours for delayed unauthorized access." },
      { id: "sap-q6-18", question: "PIRs should be mandatory for?", options: ["P1 and P2 incidents", "Only when requested", "P1 only", "Never"], correctAnswer: 0, explanation: "Mandatory for all P1 and P2 incidents for systematic improvement." },
      { id: "sap-q6-19", question: "Report recommendations should include?", options: ["Short-term only", "Short-term, long-term, process, and training", "Nothing if resolved", "Tool purchases"], correctAnswer: 1, explanation: "Comprehensive recommendations cover immediate, long-term, process, and training needs." },
      { id: "sap-q6-20", question: "Ultimate goal of the IR lifecycle?", options: ["Closing tickets", "Avoiding blame", "Continuously improving detection, response, and prevention", "Reducing workload"], correctAnswer: 2, explanation: "The IR lifecycle feeds lessons learned into continuous improvement." }
    ]
  },
  {
    quizId: "sap-q7",
    courseId: "soc-analyst-path",
    title: "Cloud Security Monitoring Quiz",
    description: "Test your cloud security knowledge across AWS, Azure, and container environments.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "sap-q7-1", question: "In the shared responsibility model, who is ALWAYS responsible for data security?", options: ["Depends on SLA", "Customer", "Cloud provider", "Both equally"], correctAnswer: 1, explanation: "Customers always own their data security regardless of cloud model (IaaS/PaaS/SaaS)." },
      { id: "sap-q7-2", question: "What AWS service logs all API calls?", options: ["CloudWatch", "CloudTrail", "GuardDuty", "Inspector"], correctAnswer: 1, explanation: "CloudTrail records every API call made in an AWS account for auditing and investigation." },
      { id: "sap-q7-3", question: "What does the CloudTrail event 'StopLogging' indicate?", options: ["Normal maintenance", "Defense evasion — attacker disabling audit trail", "Account closure", "Log rotation"], correctAnswer: 1, explanation: "StopLogging is a critical indicator of defense evasion — attackers disable logging to hide activity." },
      { id: "sap-q7-4", question: "What is the #1 cloud security threat according to CSA?", options: ["Insider threat", "Zero-day exploits", "DDoS attacks", "Misconfiguration"], correctAnswer: 3, explanation: "Misconfiguration (public S3 buckets, open security groups) is the most common cloud security issue." },
      { id: "sap-q7-5", question: "What does 'impossible travel' detection identify?", options: ["Time zone changes", "Flight booking fraud", "User logging in from geographically impossible locations in short time", "VPN usage"], correctAnswer: 2, explanation: "Impossible travel flags when a user authenticates from two distant locations faster than physically possible." },
      { id: "sap-q7-6", question: "Which Azure log tracks user sign-in activity?", options: ["Diagnostic Logs", "NSG Flow Logs", "Activity Log", "Azure AD Sign-in Logs"], correctAnswer: 3, explanation: "Azure AD Sign-in Logs record all authentication attempts with location, device, and risk information." },
      { id: "sap-q7-7", question: "Why is running containers as root dangerous?", options: ["Performance impact", "Network conflicts", "Container escape gives full host access", "Logging issues"], correctAnswer: 2, explanation: "If an attacker escapes a root container, they have root access to the underlying host system." },
      { id: "sap-q7-8", question: "What tool provides open-source runtime detection for containers?", options: ["Trivy", "Falco", "Clair", "kube-bench"], correctAnswer: 1, explanation: "Falco detects runtime threats in containers like unexpected shell access, network connections, and file modifications." },
      { id: "sap-q7-9", question: "What M365 operation indicates possible email compromise persistence?", options: ["UserLoggedIn", "MailItemsAccessed", "New-InboxRule with forwarding", "FileDownloaded"], correctAnswer: 2, explanation: "Creating inbox forwarding rules allows attackers to maintain access to emails even after password reset." },
      { id: "sap-q7-10", question: "What GuardDuty finding indicates crypto mining?", options: ["Trojan:DNSExfiltration", "Recon:PortProbe", "CryptoCurrency:EC2/BitcoinTool", "UnauthorizedAccess"], correctAnswer: 2, explanation: "GuardDuty specifically detects cryptocurrency mining activity on EC2 instances." },
      { id: "sap-q7-11", question: "First response to compromised AWS access keys?", options: ["Delete the user", "Stop all EC2 instances", "Disable the access keys and revoke sessions", "Change the password"], correctAnswer: 2, explanation: "Immediately disable compromised access keys and revoke active sessions to stop unauthorized access." },
      { id: "sap-q7-12", question: "What Kubernetes resource gives full cluster access?", options: ["Service", "ConfigMap", "Pod", "ClusterRole: cluster-admin"], correctAnswer: 3, explanation: "The cluster-admin ClusterRole grants unrestricted access to all resources in the Kubernetes cluster." },
      { id: "sap-q7-13", question: "What is OAuth app consent phishing?", options: ["OAuth server attack", "Stealing OAuth tokens", "Token expiration", "Tricking users into granting malicious apps permissions"], correctAnswer: 3, explanation: "Attackers create malicious OAuth apps that request broad permissions (mail.read, files.readwrite) via consent phishing." },
      { id: "sap-q7-14", question: "Which cloud detection monitors for public storage exposure?", options: ["CPU usage alert", "DNS monitoring", "Data volume anomaly", "S3/Blob bucket policy monitoring"], correctAnswer: 3, explanation: "Monitoring bucket/container policies for public access prevents accidental data exposure." },
      { id: "sap-q7-15", question: "What does VPC Flow Logs capture?", options: ["IP traffic metadata (source, dest, ports, action)", "Application data", "File transfers", "Database queries"], correctAnswer: 0, explanation: "VPC Flow Logs capture network traffic metadata including source/destination IPs, ports, and allow/deny actions." }
    ]
  },
  {
    quizId: "sap-q8",
    courseId: "soc-analyst-path",
    title: "Threat Intelligence & Hunting Quiz",
    description: "Assess threat intel lifecycle, IOC management, and hunting methodology skills.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "sap-q8-1", question: "How many phases are in the threat intelligence lifecycle?", options: ["5", "7", "4", "6"], correctAnswer: 3, explanation: "The 6 phases: Planning & Direction, Collection, Processing, Analysis, Dissemination, Feedback." },
      { id: "sap-q8-2", question: "What is STIX?", options: ["A firewall protocol", "A SIEM platform", "A structured language for describing cyber threat intelligence", "An encryption standard"], correctAnswer: 2, explanation: "STIX (Structured Threat Information eXpression) is the standard JSON format for threat intelligence." },
      { id: "sap-q8-3", question: "What does TAXII provide?", options: ["Vulnerability scanning", "Malware sandboxing", "Automated transport/sharing of STIX intelligence", "Threat analysis"], correctAnswer: 2, explanation: "TAXII defines how STIX data is shared between organizations via REST APIs." },
      { id: "sap-q8-4", question: "Typical IOC expiration for IP addresses?", options: ["30 days", "1 year", "7 days", "Never"], correctAnswer: 0, explanation: "IP addresses change frequently — 30 days is a typical expiration before they may be reassigned to legitimate use." },
      { id: "sap-q8-5", question: "What distinguishes threat hunting from detection?", options: ["Hunting is proactive, detection is reactive", "Hunting is automated", "Detection is manual", "Hunting uses better tools"], correctAnswer: 0, explanation: "Hunting proactively searches for threats that bypass automated detections, while detection waits for alerts." },
      { id: "sap-q8-6", question: "A hunting hypothesis should be?", options: ["Vague and broad", "Testable with available data sources", "Always confirmed", "Based only on intuition"], correctAnswer: 1, explanation: "Good hypotheses are specific, testable with available data, and based on threat intelligence or ATT&CK gaps." },
      { id: "sap-q8-7", question: "What is 'stacking' in threat hunting?", options: ["Frequency analysis — counting occurrences to find rare values", "Building infrastructure", "Log aggregation", "Layering defenses"], correctAnswer: 0, explanation: "Stacking counts occurrences and sorts by frequency — rare values at the bottom often indicate threats." },
      { id: "sap-q8-8", question: "How to detect C2 beaconing?", options: ["Analyze connection interval consistency (low jitter)", "Monitor CPU usage", "Check file hashes", "Scan for open ports"], correctAnswer: 0, explanation: "C2 beaconing has regular intervals with low jitter (variation), which is detectable through statistical analysis." },
      { id: "sap-q8-9", question: "What is tactical threat intelligence?", options: ["Budget planning", "Strategic business context", "Geopolitical analysis", "IOCs and TTPs for immediate detection by SOC analysts"], correctAnswer: 3, explanation: "Tactical intelligence includes specific IOCs and TTPs that analysts can immediately use for detection." },
      { id: "sap-q8-10", question: "What should a hunt report always include?", options: ["Only findings", "Hypothesis, methodology, findings, and recommendations", "Just IOCs", "Executive summary only"], correctAnswer: 1, explanation: "Complete hunt reports document the hypothesis, data sources, methodology, findings, and operationalized detections." },
      { id: "sap-q8-11", question: "What is 'long tail analysis'?", options: ["Focusing on the rare 2% of events outside the top common items", "Tracking long-running processes", "Log retention policy", "Analyzing network latency"], correctAnswer: 0, explanation: "Long tail analysis focuses on rare events (the 2%) that fall outside common patterns — where threats often hide." },
      { id: "sap-q8-12", question: "Best source for hunting hypotheses?", options: ["Vendor marketing", "Random guessing", "Social media", "Threat intelligence reports and ATT&CK gaps"], correctAnswer: 3, explanation: "Threat intelligence and MITRE ATT&CK coverage gaps provide evidence-based starting points for hunts." },
      { id: "sap-q8-13", question: "What indicates 3+ standard deviations in data transfer?", options: ["Statistical anomaly requiring investigation", "Normal variation", "Scheduled backup", "System error"], correctAnswer: 0, explanation: "3+ standard deviations from the mean is statistically unusual and warrants investigation for data exfiltration." },
      { id: "sap-q8-14", question: "How often should baselines be rebuilt?", options: ["Never", "Yearly", "Only after incidents", "Monthly"], correctAnswer: 3, explanation: "Monthly baseline rebuilds account for organic changes while keeping detection relevant." },
      { id: "sap-q8-15", question: "What should hunting findings be converted into?", options: ["Reports only", "Deleted", "Automated detection rules for continuous monitoring", "Manual checks"], correctAnswer: 2, explanation: "Operationalizing findings into automated detection rules ensures the same technique is caught in the future." }
    ]
  },
  {
    quizId: "sap-q9",
    courseId: "soc-analyst-path",
    title: "Digital Forensics Assessment",
    description: "Evaluate disk forensics, timeline analysis, and anti-forensics detection skills.",
    passingScore: 70,
    timeLimit: 25,
    questions: [
      { id: "sap-q9-1", question: "Correct order of the forensic process?", options: ["Identification, Preservation, Collection, Analysis, Presentation", "Analysis, Preservation, Presentation", "Presentation, Collection, Analysis", "Collection, Analysis, Identification"], correctAnswer: 0, explanation: "The forensic process follows: Identification → Preservation → Collection → Analysis → Presentation." },
      { id: "sap-q9-2", question: "Most volatile evidence type?", options: ["Disk data", "Log files", "CPU registers and memory", "Backup tapes"], correctAnswer: 2, explanation: "CPU registers and memory are the most volatile — they're lost in seconds when power is removed." },
      { id: "sap-q9-3", question: "What hash algorithm is standard for evidence integrity?", options: ["Base64", "SHA-256", "CRC32", "MD5"], correctAnswer: 1, explanation: "SHA-256 is the forensic standard for evidence integrity verification in legal proceedings." },
      { id: "sap-q9-4", question: "What is the NTFS Master File Table ($MFT)?", options: ["Database containing metadata for every file on the volume", "Memory allocation table", "A disk encryption key", "Network routing table"], correctAnswer: 0, explanation: "The $MFT stores metadata (timestamps, size, location, permissions) for every file and directory on NTFS." },
      { id: "sap-q9-5", question: "How to detect timestomping?", options: ["Run antivirus", "Compare $STANDARD_INFORMATION vs $FILE_NAME timestamps", "Check file extension", "Check file size"], correctAnswer: 1, explanation: "$SI timestamps are easily modified but $FN timestamps are harder to change — discrepancy indicates timestomping." },
      { id: "sap-q9-6", question: "What Windows Event ID indicates Security log was cleared?", options: ["4624", "7045", "1102", "4688"], correctAnswer: 2, explanation: "Event ID 1102 is generated when the Windows Security audit log is cleared." },
      { id: "sap-q9-7", question: "What is a super timeline?", options: ["Real-time event stream", "A project management tool", "Timeline combining timestamps from 100+ artifact sources", "A very long timeline"], correctAnswer: 2, explanation: "A super timeline merges timestamps from file system, event logs, registry, browser, and more into one view." },
      { id: "sap-q9-8", question: "What tool creates super timelines?", options: ["Plaso/log2timeline", "Burp Suite", "Wireshark", "Nmap"], correctAnswer: 0, explanation: "Plaso (log2timeline) extracts timestamps from 100+ sources and creates comprehensive super timelines." },
      { id: "sap-q9-9", question: "What survives secure file deletion?", options: ["Nothing at all", "Only the filename", "USN Journal entries and Prefetch files", "The file data"], correctAnswer: 2, explanation: "USN Journal records the deletion event, and Prefetch records execution of the deletion tool." },
      { id: "sap-q9-10", question: "What is an Alternate Data Stream (ADS)?", options: ["Network protocol", "Backup format", "Encryption method", "Hidden data stream attached to NTFS files"], correctAnswer: 3, explanation: "NTFS ADS allows hiding data within existing files — attackers use them to conceal malicious payloads." },
      { id: "sap-q9-11", question: "What should you NEVER do with original evidence?", options: ["Document it", "Analyze it directly", "Photograph it", "Hash it"], correctAnswer: 1, explanation: "Always create working copies — analyzing original evidence risks modification that destroys legal admissibility." },
      { id: "sap-q9-12", question: "What does the $UsnJrnl artifact record?", options: ["Network connections", "File creates, deletes, renames, and modifications", "User logins", "Registry changes"], correctAnswer: 1, explanation: "The USN (Update Sequence Number) Journal records all file system changes including creates, deletes, and renames." },
      { id: "sap-q9-13", question: "Best approach for timeline analysis?", options: ["Random sampling", "Only look at the last 24 hours", "Start from the beginning of time", "Start from known events and expand outward"], correctAnswer: 3, explanation: "Pivot from known events (malware detection, alert time) and expand outward to build the full picture." },
      { id: "sap-q9-14", question: "How does fileless malware evade disk forensics?", options: ["Encrypts the disk", "Uses very small files", "Hides in system folders", "Operates entirely in memory without writing to disk"], correctAnswer: 3, explanation: "Fileless malware loads and executes in memory, leaving no traditional file-based artifacts for disk forensics." },
      { id: "sap-q9-15", question: "Key principle of anti-forensics detection?", options: ["Evidence cannot be recovered", "Only advanced tools can detect it", "Anti-forensics creates its own artifacts — the cover-up leaves traces", "Attackers always succeed"], correctAnswer: 2, explanation: "The act of destroying evidence (clearing logs, timestomping, secure deletion) creates new artifacts that analysts can find." }
    ]
  },
  {
    quizId: "sap-q10",
    courseId: "soc-analyst-path",
    title: "Security Automation & SOAR Quiz",
    description: "Test your SOAR platform knowledge, playbook design, and API integration skills.",
    passingScore: 75,
    timeLimit: 20,
    questions: [
      { id: "sap-q10-1", question: "What is the primary difference between orchestration and automation in SOAR?", options: ["They are the same thing", "Automation handles a single repetitive task; orchestration coordinates multiple automated tasks and tools into one workflow", "Orchestration only applies to cloud platforms", "Automation requires human approval, orchestration does not"], correctAnswer: 1, explanation: "Automation handles individual tasks; orchestration ties multiple automated steps and tools together into a coherent workflow." },
      { id: "sap-q10-2", question: "What does SOAR stand for?", options: ["Security Operations and Reporting", "Security Orchestration, Automation and Response", "Secure Operations Automated Recovery", "Security Oversight and Remediation"], correctAnswer: 1, explanation: "SOAR = Security Orchestration, Automation and Response." },
      { id: "sap-q10-3", question: "In a phishing response playbook, what should typically happen FIRST when a suspicious email is reported?", options: ["Automatically delete the email from all mailboxes", "Extract IOCs (sender, URLs, attachments) and enrich them via threat intel", "Notify the CEO", "Block the sender's entire domain immediately"], correctAnswer: 1, explanation: "Enrichment comes first — you need context on the IOCs before taking containment action to avoid overreacting to a false positive." },
      { id: "sap-q10-4", question: "Which HTTP method is typically used to submit a new ticket via a REST API integration?", options: ["GET", "POST", "DELETE", "HEAD"], correctAnswer: 1, explanation: "POST creates a new resource, such as a new ticket in a ticketing system." },
      { id: "sap-q10-5", question: "What is a key risk of a poorly tested automated containment playbook?", options: ["It could isolate or block legitimate users/systems based on a false positive", "It uses too much CPU", "It always requires manual approval", "It cannot integrate with a SIEM"], correctAnswer: 0, explanation: "Automated containment without proper validation can cause outages by acting on false positives." },
      { id: "sap-q10-6", question: "In Python, which library is most commonly used to make HTTP API requests for security tool integrations?", options: ["requests", "pandas", "tkinter", "os"], correctAnswer: 0, explanation: "The `requests` library is the standard tool for making HTTP calls in Python automation scripts." },
      { id: "sap-q10-7", question: "What is a 'human-in-the-loop' step in a SOAR playbook?", options: ["A manual approval/decision gate before a high-impact automated action executes", "A step that always runs automatically", "A step that removes analyst involvement entirely", "A logging-only step"], correctAnswer: 0, explanation: "Human-in-the-loop steps pause automation for analyst approval before irreversible or high-impact actions." },
      { id: "sap-q10-8", question: "Which authentication method is common for securing API integrations between SOAR platforms and third-party security tools?", options: ["API keys or OAuth tokens", "Plaintext passwords in the URL", "No authentication needed", "SMS OTP only"], correctAnswer: 0, explanation: "API keys and OAuth tokens are the standard secure method for authenticating machine-to-machine integrations." },
      { id: "sap-q10-9", question: "Which metric best measures the direct time-saving impact of automation on incident response?", options: ["MTTR (Mean Time To Respond/Remediate) reduction", "Number of open browser tabs", "CPU utilization", "Number of Slack channels"], correctAnswer: 0, explanation: "MTTR reduction directly reflects how much faster incidents are handled thanks to automation." },
      { id: "sap-q10-10", question: "What should a chatbot/notification integration NOT be used for?", options: ["Alert notifications", "Interactive approve/deny commands for playbook actions", "Making irreversible destructive changes with no audit trail or approval", "Providing status updates to the team"], correctAnswer: 2, explanation: "Irreversible actions should always go through logged, approved workflows — never triggered casually via chat with no audit trail." },
      { id: "sap-q10-11", question: "Which of these is a common use case for SOAR automated enrichment?", options: ["Automatically checking a file hash against VirusTotal or threat intel feeds", "Writing marketing copy", "Compiling application source code", "Managing payroll"], correctAnswer: 0, explanation: "Enrichment automation pulls context (reputation, IOC matches) from external intel sources to speed up triage." },
      { id: "sap-q10-12", question: "What does idempotency mean in the context of a SOAR playbook action, and why does it matter?", options: ["Running the action multiple times produces the same safe result without unintended side effects", "The playbook only runs once ever", "The playbook cannot be scheduled", "The action requires internet access"], correctAnswer: 0, explanation: "Idempotent actions can safely be retried or re-run without causing duplicate or harmful side effects — critical for reliable automation." },
      { id: "sap-q10-13", question: "When integrating with a ticketing system like Jira or ServiceNow via API, what's a best practice for handling API failures?", options: ["Retry with backoff and alert if it keeps failing", "Silently ignore all failures", "Immediately page the CEO", "Delete the incident record"], correctAnswer: 0, explanation: "Retry-with-backoff plus alerting on persistent failure keeps the integration resilient without silent data loss." },
      { id: "sap-q10-14", question: "What's the biggest advantage of using Python scripts for log parsing over manual review in a SOC?", options: ["Consistent, repeatable extraction of IOCs at a scale and speed impossible manually", "Python removes the need for logging entirely", "Python scripts don't need testing", "Python eliminates false positives permanently"], correctAnswer: 0, explanation: "Scripting provides speed and consistency at scale that manual review can't match, though it still requires validation." },
      { id: "sap-q10-15", question: "Which of these best describes measuring 'automation ROI' for a SOAR deployment?", options: ["Comparing analyst time saved and MTTR improvement against platform/maintenance cost", "Counting how many playbooks exist", "Counting lines of Python code written", "Number of vendors integrated"], correctAnswer: 0, explanation: "ROI is measured by weighing real efficiency gains (time saved, faster MTTR) against the cost of running the platform." }
    ]
  },
  {
    quizId: "sap-q11",
    courseId: "soc-analyst-path",
    title: "Vulnerability Management Quiz",
    description: "Assess vulnerability scanning, CVSS scoring, and remediation workflow knowledge.",
    passingScore: 75,
    timeLimit: 20,
    questions: [
      { id: "sap-q11-1", question: "What is the correct order of the vulnerability management lifecycle?", options: ["Assess, Remediate, Plan, Scan, Verify", "Plan, Scan, Assess, Remediate, Verify", "Scan, Plan, Verify, Assess, Remediate", "Remediate, Scan, Plan, Assess, Verify"], correctAnswer: 1, explanation: "The VM lifecycle flows: Plan → Scan → Assess/Prioritize → Remediate → Verify." },
      { id: "sap-q11-2", question: "What does CVSS stand for?", options: ["Common Vulnerability Scoring System", "Certified Vulnerability Security Standard", "Cyber Vulnerability Severity Score", "Common Virus Scanning Software"], correctAnswer: 0, explanation: "CVSS = Common Vulnerability Scoring System, the industry standard for rating vulnerability severity." },
      { id: "sap-q11-3", question: "A vulnerability has a CVSS base score of 9.8. How should it generally be prioritized?", options: ["Low priority", "Critical — remediate urgently", "Ignore since no exploit exists yet", "Only relevant to compliance audits"], correctAnswer: 1, explanation: "A 9.8 falls in the Critical range and should be remediated as a top priority." },
      { id: "sap-q11-4", question: "What does EPSS (Exploit Prediction Scoring System) estimate that CVSS alone does not?", options: ["The likelihood a vulnerability will actually be exploited in the wild in the near term", "The exact patch release date", "The vendor's stock price impact", "The number of affected servers"], correctAnswer: 0, explanation: "EPSS predicts real-world exploitation probability, complementing CVSS's severity-only score for better prioritization." },
      { id: "sap-q11-5", question: "Which of these is an advantage of an authenticated (credentialed) vulnerability scan over an unauthenticated one?", options: ["Deeper visibility into missing patches and local misconfigurations", "Faster scan completion always", "No need for scan credentials", "Works only on network devices"], correctAnswer: 0, explanation: "Credentialed scans log in to the host, revealing missing patches and local misconfigurations invisible from the network alone." },
      { id: "sap-q11-6", question: "What is a common reason organizations set different remediation SLAs for critical vs. low-severity vulnerabilities?", options: ["To prioritize limited IT resources toward the highest-risk issues first", "Because low-severity vulnerabilities never need patches", "Because critical vulnerabilities take longer to test", "SLAs are only for compliance paperwork"], correctAnswer: 0, explanation: "Tiered SLAs focus limited remediation resources on the vulnerabilities that pose the greatest actual risk first." },
      { id: "sap-q11-7", question: "What is 'attack surface management' primarily concerned with?", options: ["Discovering and monitoring all externally-facing assets, including unknown/shadow IT", "Managing internal HR policies", "Writing firewall rules only", "Measuring CPU load on servers"], correctAnswer: 0, explanation: "ASM continuously discovers and tracks external-facing assets, including forgotten or unauthorized ('shadow IT') systems." },
      { id: "sap-q11-8", question: "Which of these best describes a 'false positive' in vulnerability scanning?", options: ["The scanner reports a vulnerability that doesn't actually exist or isn't exploitable in that environment", "A vulnerability that was successfully patched", "A critical vulnerability that was missed by the scanner", "An exploit that succeeded during testing"], correctAnswer: 0, explanation: "A false positive is an incorrectly reported finding — it wastes remediation effort if not triaged out." },
      { id: "sap-q11-9", question: "What is virtual patching / a compensating control used for?", options: ["Mitigating risk from a vulnerability (e.g. via a WAF or IPS rule) when a real patch can't be applied immediately", "Permanently replacing the need for real patches", "Only used for cosmetic UI bugs", "A synonym for a software update"], correctAnswer: 0, explanation: "Virtual patching provides temporary risk mitigation until the actual vendor patch can be tested and deployed." },
      { id: "sap-q11-10", question: "When communicating vulnerability risk to non-technical executives, what is most effective?", options: ["Business impact and risk framed in terms of exposure and cost", "Raw CVSS vectors and CVE numbers only", "A list of every open port", "Full technical exploit code"], correctAnswer: 0, explanation: "Executives respond to business risk and cost framing, not raw technical scoring data." },
      { id: "sap-q11-11", question: "What does 'remediation verification' (rescanning) confirm?", options: ["That the vulnerability was actually fixed and doesn't reappear", "That the scanner itself is working", "That the firewall is enabled", "That patches were purchased"], correctAnswer: 0, explanation: "Rescanning closes the loop, confirming remediation actually worked rather than just assuming it did." },
      { id: "sap-q11-12", question: "Which scanning tool covered in this module is open-source?", options: ["OpenVAS", "Nessus", "Qualys", "Rapid7 InsightVM"], correctAnswer: 0, explanation: "OpenVAS is the open-source vulnerability scanner; Nessus, Qualys, and InsightVM are commercial." },
      { id: "sap-q11-13", question: "What's a key risk of patch management without proper change management?", options: ["Untested patches could break production systems or cause outages", "Systems become more secure instantly with no downside", "Patches always apply cleanly with zero risk", "Change management slows security to zero benefit"], correctAnswer: 0, explanation: "Deploying patches without testing/change control can cause unplanned outages — a real operational risk to weigh against security urgency." },
      { id: "sap-q11-14", question: "Why is asset inventory critical to effective vulnerability management?", options: ["You can't scan, prioritize, or patch assets you don't know exist", "Inventory is only needed for finance/audit purposes", "Scanners automatically discover 100% of assets with no inventory needed", "Asset inventory replaces the need for scanning"], correctAnswer: 0, explanation: "An accurate inventory is the foundation of VM — unknown assets are unmanaged risk." },
      { id: "sap-q11-15", question: "What does an 'exception' in vulnerability management typically represent?", options: ["A documented, risk-accepted deviation from the standard remediation SLA", "A vulnerability that doesn't need tracking at all", "A scanner bug", "A mandatory zero-day patch"], correctAnswer: 0, explanation: "Exceptions formally document why a vulnerability is temporarily accepted outside normal SLA, with an owner and review date." }
    ]
  },
  {
    quizId: "sap-q12",
    courseId: "soc-analyst-path",
    title: "SOC Analyst Final Assessment",
    description: "A scenario-driven, medium-difficulty final assessment built directly from the SOC Analyst Learning Path's lesson content and hands-on lab scenarios, covering all 12 modules.",
    passingScore: 75,
    timeLimit: 45,
    questions: [
      { id: "sap-q12-1", question: "In the SOC-CMM maturity model, which level is described as 'Standardized workflows, metrics'?", options: ["Level 2 – Managed (defined processes, basic tooling)", "Level 4 – Quantitatively Managed (data-driven, automation)", "Level 3 – Defined (standardized workflows, metrics)", "Level 5 – Optimizing (continuous improvement, analytics)"], correctAnswer: 2, explanation: "SOC-CMM Level 3 – Defined is standardized workflows with metrics tracking." },
      { id: "sap-q12-2", question: "What retention period does SOX require for security logs?", options: ["7 years (SOX)", "1 year (PCI-DSS)", "6 years (HIPAA)", "As needed / minimized (GDPR)"], correctAnswer: 0, explanation: "SOX requires 7 years of retention, versus 1 year for PCI-DSS and 6 years for HIPAA." },
      { id: "sap-q12-3", question: "During a shift handover, three alerts arrive: a medium brute-force alert, a high EDR alert of PowerShell spawned by winword.exe, and a low firewall violation from a developer. Which should be investigated first?", options: ["The brute-force alert against SRV-WEB-01", "The low-severity firewall rule violation", "All three alerts with equal priority", "The EDR alert showing PowerShell spawned by winword.exe"], correctAnswer: 3, explanation: "The EDR alert is the priority — a legitimate app spawning a command-line interpreter is the most dangerous pattern of the three." },
      { id: "sap-q12-4", question: "Port 4444 is the default port most commonly associated with which tool's reverse shell?", options: ["Port 22, commonly targeted for SSH brute force", "Port 4444, the Metasploit default reverse shell port", "Port 445, used for SMB-based lateral movement", "Port 3389, used for RDP brute force attempts"], correctAnswer: 1, explanation: "Port 4444 is the well-known Metasploit default reverse shell port." },
      { id: "sap-q12-5", question: "JA3 fingerprinting hashes together which set of TLS ClientHello parameters?", options: ["Source IP, destination IP, and port number", "Certificate issuer, subject, and validity period", "TLS version, ciphers, extensions, elliptic curves, and point formats", "HTTP headers, cookies, and user-agent string"], correctAnswer: 2, explanation: "JA3 = MD5(TLSVersion, Ciphers, Extensions, EllipticCurves, EllipticCurvePointFormats)." },
      { id: "sap-q12-6", question: "Workstation WS-DEV-12 made 1,200 DNS TXT queries with 40-60 character Base64-encoded subdomains to a domain registered 3 days ago. What does this indicate?", options: ["DNS cache poisoning of the resolver", "A fast-flux DNS network rotating IPs", "A domain generation algorithm (DGA)", "DNS tunneling via encoded TXT queries"], correctAnswer: 3, explanation: "The encoded subdomains and high query volume match a DNS tunneling pattern." },
      { id: "sap-q12-7", question: "Service account 'svc-backup' had 250 failed logons at 02:15, a successful logon at 02:22, then lateral movement to a domain controller by 02:35. How much total time elapsed from the first failed logon to DC access?", options: ["20 minutes", "10 minutes", "35 minutes", "1 hour"], correctAnswer: 0, explanation: "02:15 to 02:35 is a 20-minute window." },
      { id: "sap-q12-8", question: "What share of SOC alerts typically fall into the 'Benign True Positive' (real but expected) category?", options: ["5-15%", "20-30%", "40-60%", "80-90%"], correctAnswer: 1, explanation: "Benign True Positives typically make up 20-30% of alerts, separate from the 40-60% that are false positives." },
      { id: "sap-q12-9", question: "In a Kerberoasting SIEM detection query, which Ticket_Encryption_Type value is filtered for as suspicious?", options: ["Ticket_Encryption_Type 0x12", "Ticket_Encryption_Type 0x18", "Ticket_Encryption_Type 0x11", "Ticket_Encryption_Type 0x17 (RC4)"], correctAnswer: 3, explanation: "Detection rules filter on Ticket_Encryption_Type=\"0x17\", the weaker RC4 encryption attackers prefer." },
      { id: "sap-q12-10", question: "An encoded PowerShell command downloads a second-stage script right after WINWORD.EXE spawns cmd.exe. What evasion technique is the encoded command using?", options: ["DNS tunneling", "Alternate Data Streams", "Base64-encoded command-line obfuscation", "Timestomping the payload's file timestamps"], correctAnswer: 2, explanation: "The '-enc' flag and encoded string reveal Base64 command-line obfuscation." },
      { id: "sap-q12-11", question: "Which Volatility plugin specifically detects code injection via RWX memory protection?", options: ["malfind, which detects injection through RWX memory", "pslist, which lists active processes", "netscan, which shows network connections", "dlllist, which lists loaded DLLs"], correctAnswer: 0, explanation: "malfind is built specifically for RWX-memory injection detection." },
      { id: "sap-q12-12", question: "A PowerShell SIEM detection rule searches ScriptBlockText for 'encodedcommand' and which other term?", options: ["netstat and tracert command usage", "frombase64, downloadstring, and invoke-expression", "whoami and systeminfo command usage", "certutil and bitsadmin command usage"], correctAnswer: 1, explanation: "The regex match list is (encodedcommand|frombase64|downloadstring|invoke-expression|iex)." },
      { id: "sap-q12-13", question: "An email's Return-Path is a .xyz domain, SPF fails, and DKIM is 'none'. What is the single strongest technical indicator of spoofing?", options: ["The subject line uses urgent language", "The email was sent during business hours", "The recipient works in the HR department", "SPF fail — sender IP not authorized for the claimed domain"], correctAnswer: 3, explanation: "An SPF fail directly proves the sending IP wasn't authorized for the domain." },
      { id: "sap-q12-14", question: "Which Business Email Compromise (BEC) variant specifically involves asking HR to change direct deposit details?", options: ["Payroll Diversion", "CEO Fraud", "Vendor Impersonation", "Attorney Impersonation"], correctAnswer: 0, explanation: "Payroll Diversion is the BEC type that targets HR to update direct deposit information." },
      { id: "sap-q12-15", question: "In an SPF record (v=spf1 ... -all), what does the trailing '-all' mechanism mean?", options: ["Allow all senders unconditionally", "Soft fail — mark suspicious but still deliver", "Hard fail — reject unauthorized senders", "Neutral — apply no policy at all"], correctAnswer: 2, explanation: "-all means hard fail (reject), versus ~all for soft fail and +all for allow-all." },
      { id: "sap-q12-16", question: "What is the required response time for a Critical (P1) security incident?", options: ["Less than 1 hour", "Less than 15 minutes", "Less than 4 hours", "Less than 24 hours"], correctAnswer: 1, explanation: "Four-level severity classification sets P1 response time at under 15 minutes." },
      { id: "sap-q12-17", question: "Mimikatz runs under the SYSTEM account on a domain controller at 03:00 with no scheduled maintenance. What severity should this incident receive?", options: ["Critical — SYSTEM-level credential dumping on a DC", "Low, since no data loss was confirmed yet", "Medium, pending further investigation", "High, but not needing immediate escalation"], correctAnswer: 0, explanation: "Credential-dumping tool use on a domain controller is the highest-value, highest-risk target — Critical." },
      { id: "sap-q12-18", question: "How often should small, SOC-focused tabletop exercises run at minimum?", options: ["Weekly", "Annually", "Only after a real incident occurs", "Quarterly, at minimum"], correctAnswer: 3, explanation: "Quarterly is the minimum cadence for small SOC-focused exercises, with semi-annual and annual cadences for larger ones." },
      { id: "sap-q12-19", question: "IAM user 'dev-deploy' makes S3 API calls at 04:30 UTC from an unfamiliar Eastern European IP, though the user normally only works business hours from the corporate VPN range. What is the strongest compromise indicator?", options: ["The bucket name referenced financial data", "A source IP inconsistent with the user's normal pattern", "The request used the HTTPS protocol", "More than one API call was made in sequence"], correctAnswer: 1, explanation: "The unusual source IP is the first indicator of compromised credentials." },
      { id: "sap-q12-20", question: "Which GuardDuty finding type is associated with DNS-based data exfiltration?", options: ["UnauthorizedAccess:IAMUser/MaliciousIPCaller", "CryptoCurrency:EC2/BitcoinTool", "Trojan:EC2/DNSDataExfiltration", "Recon:EC2/PortProbeUnprotectedPort"], correctAnswer: 2, explanation: "Trojan:EC2/DNSDataExfiltration is the high-severity finding for DNS-based exfiltration." },
      { id: "sap-q12-21", question: "In a Falco rule for 'Shell Spawned in Container', what condition triggers the alert?", options: ["An image pulled from an unapproved registry", "A pod being deleted unexpectedly", "A container restarting more than three times", "A shell process (bash/sh/zsh) spawned in a container"], correctAnswer: 3, explanation: "The rule condition checks proc.name against bash, sh, zsh, dash, ksh." },
      { id: "sap-q12-22", question: "A threat-intel correlation check for 'IronLotus' finds a matching DNS query and file hash in logs, but no callback-IP connections. What does this absence suggest?", options: ["The IOCs are confirmed false positives", "Compromise is likely in an early stage, pre-callback", "The malware was never actually delivered", "The firewall has blocked traffic for months"], correctAnswer: 1, explanation: "Two of three IOCs matched, but no C2 callback yet suggests the infection hasn't progressed that far." },
      { id: "sap-q12-23", question: "How long are IP-address indicators typically set to expire in IOC lifecycle management?", options: ["30 days", "7 days", "90 days", "1 year"], correctAnswer: 0, explanation: "IPs are set to expire after 30 days, versus 90 days for domains and 1 year for file hashes." },
      { id: "sap-q12-24", question: "In a beaconing-detection query, what jitter and interval pattern flags likely C2 traffic?", options: ["High jitter with random, unpredictable intervals", "Any interval greater than 24 hours between connections", "Low jitter (stdev < 5) with intervals between 30 seconds and 1 hour", "Jitter values greater than 100 seconds"], correctAnswer: 2, explanation: "The signature is low jitter (stdev < 5) with an average interval between 30 seconds and 1 hour." },
      { id: "sap-q12-25", question: "A webshell and a fake process 'kworker_update' (running as root, listening on port 4444) are found on a compromised server. Why is that process specifically suspicious?", options: ["It consumes an unusually large amount of system memory", "It was scheduled to run via a cron job entry", "It has an unusually old file creation timestamp", "It has a kernel-like name but listens on a network port"], correctAnswer: 3, explanation: "It's a fake kernel process — real kernel workers don't listen on high network ports as root." },
      { id: "sap-q12-26", question: "Which NTFS artifact is the directory index that can include deleted file entries?", options: ["$I30, the directory index that can include deleted entries", "$MFT, the master file table", "$LogFile, the file system transaction log", "$UsnJrnl, the update sequence number journal"], correctAnswer: 0, explanation: "$I30 specifically retains deleted directory entries." },
      { id: "sap-q12-27", question: "If $STANDARD_INFORMATION shows a 2024 creation date but $FILE_NAME shows 2025 on the same file, what does that indicate?", options: ["A time zone configuration mismatch", "Timestomping — the attacker backdated the $SI timestamp", "Normal behavior after a system restore", "A routine backup-related artifact"], correctAnswer: 1, explanation: "$SI is easily modified by tools like Timestomp, while $FN is harder to forge — a mismatch reveals timestomping." },
      { id: "sap-q12-28", question: "A SOC handles 45 phishing reports daily at 25 minutes each manually. How many analyst-hours per day could full automation of that workflow save?", options: ["8 hours of manual investigation time", "25 hours of manual investigation time", "18.75 hours of manual investigation time", "45 hours of manual investigation time"], correctAnswer: 2, explanation: "45 reports × 25 minutes = 1,125 minutes, or 18.75 hours." },
      { id: "sap-q12-29", question: "Roughly what alert-volume reduction can Tier 1 automation typically achieve?", options: ["About 80%", "About 25%", "About 50%", "About 95%"], correctAnswer: 0, explanation: "Automating Tier 1 triage can reduce alert volume by about 80%." },
      { id: "sap-q12-30", question: "Going from roughly 16 analysts to 3 analysts plus a SOAR platform produced roughly what annual savings?", options: ["About $150,000", "About $405,000", "About $955,000", "About $1,360,000"], correctAnswer: 2, explanation: "$1,360,000 (before) minus $405,000 (after) is about $955,000 in annual savings." },
      { id: "sap-q12-31", question: "Vuln-A (CVSS 9.8, public payment server, actively exploited) and Vuln-D (CVSS 10.0, isolated test server, no production data) both appear on a scan. Which is patched first?", options: ["Vuln-D, since it has the highest CVSS score", "Both patched with exactly equal priority", "Neither requires any urgent action", "Vuln-A, due to exposure and active exploitation"], correctAnswer: 3, explanation: "Despite a lower CVSS than Vuln-D, Vuln-A's exposure, data sensitivity, and active exploitation make it the real priority." },
      { id: "sap-q12-32", question: "What does Qualys TruRisk scoring add on top of a plain CVSS score?", options: ["A fixed compliance checklist only", "Threat intelligence and business context layered on top of CVSS", "A faster scanning engine with no other changes", "A larger vulnerability plugin count alone"], correctAnswer: 1, explanation: "TruRisk layers threat intelligence and business context on top of CVSS, not just a faster scanner." },
      { id: "sap-q12-33", question: "In a risk-based vulnerability prioritization formula, which four factors are multiplied together?", options: ["CVSS, EPSS weight, asset criticality, and exposure factor", "CVSS, patch cost, vendor reputation, and scan frequency", "CVSS, CVE age, analyst headcount, and ticket volume", "CVSS, system uptime, bandwidth, and geography"], correctAnswer: 0, explanation: "Risk Priority = CVSS × EPSS Weight × Asset Criticality × Exposure Factor." },
      { id: "sap-q12-34", question: "'john.martinez' requests TGS tickets for 12 service accounts in 3 minutes using RC4 encryption. What encryption should the organization enforce to mitigate this?", options: ["DES encryption enforced for tickets", "RC4 encryption left as the default", "MD5 hashing applied to all tickets", "AES-256 encryption enforced for tickets"], correctAnswer: 3, explanation: "AES-256 is the standard to enforce, versus the weaker RC4 the attacker used." },
      { id: "sap-q12-35", question: "Roughly what share of organizations that pay a ransom are targeted again?", options: ["About 30%", "About 50%", "About 80%", "About 10%"], correctAnswer: 2, explanation: "Approximately 80% of organizations that pay are targeted again by ransomware actors." },
      { id: "sap-q12-36", question: "In a purple team detection scorecard, what was the overall detection coverage across the tested techniques?", options: ["60% (9 out of 15)", "73% (11 out of 15)", "50% (7.5 out of 15)", "100% (15 out of 15)"], correctAnswer: 1, explanation: "The scorecard totals 11 out of 15 detections logged/alerted/blocked, or 73% overall coverage." }
    ]
  },
  // SOC ANALYST LEARNING PATH — FINAL CERTIFICATION EXAM
  {
    quizId: "sap-q13",
    courseId: "soc-analyst-path",
    title: "SOC Analyst Certification Exam",
    description: "Comprehensive final exam covering all 12 modules. You must pass this exam with 80% or higher to earn your SOC Analyst Learning Path certificate.",
    passingScore: 80,
    timeLimit: 60,
    questions: [
      // Module 1 — SOC Foundations
      { id: "sap-q13-1", question: "In the SOC-CMM model, which level indicates processes are documented, standardized, and measured?", options: ["Level 2 – Managed", "Level 3 – Defined", "Level 4 – Quantitatively Managed", "Level 1 – Initial"], correctAnswer: 2, explanation: "Level 4 (Quantitatively Managed) means processes are measured with KPIs and managed using data-driven decisions." },
      { id: "sap-q13-2", question: "A SOC analyst discovers a breach involving EU citizen data. Under GDPR, what is the maximum notification window to the supervisory authority?", options: ["72 hours", "24 hours", "7 days", "48 hours"], correctAnswer: 0, explanation: "GDPR Article 33 requires notification within 72 hours of becoming aware of a personal data breach." },
      { id: "sap-q13-3", question: "What is the primary difference between a L1 and L2 SOC analyst?", options: ["L2 only handles compliance", "L1 writes detection rules", "L2 uses different tools", "L1 triages alerts while L2 performs deeper investigation and correlation"], correctAnswer: 3, explanation: "L1 analysts perform initial triage and escalation, while L2 analysts conduct deeper investigation, threat correlation, and containment." },
      // Module 2 — Network Traffic Analysis
      { id: "sap-q13-4", question: "During packet analysis, you observe a TCP connection with SYN, SYN-ACK, then RST. What does this indicate?", options: ["Half-open scan (port scan)", "FIN scan", "Successful connection", "Connection timeout"], correctAnswer: 0, explanation: "SYN → SYN-ACK → RST is a classic half-open (stealth) port scan — the scanner sends RST instead of completing the handshake." },
      { id: "sap-q13-5", question: "Which DNS record type is commonly abused for data exfiltration via DNS tunneling?", options: ["SOA records", "A records", "MX records", "TXT records"], correctAnswer: 3, explanation: "TXT records can carry arbitrary text data, making them ideal for DNS tunneling and data exfiltration." },
      { id: "sap-q13-6", question: "You see HTTP traffic with unusually long GET parameters containing Base64-encoded strings. What attack technique should you suspect?", options: ["SQL injection", "Cross-site scripting", "C2 beaconing via HTTP", "Directory traversal"], correctAnswer: 2, explanation: "C2 (Command and Control) beacons often embed encoded commands in HTTP GET parameters to blend with normal web traffic." },
      // Module 3 — SIEM Mastery
      { id: "sap-q13-7", question: "In Splunk SPL, what does the 'stats dc(src_ip) as unique_sources by dest_port' query calculate?", options: ["Average connection duration", "Distinct source IPs connecting to each destination port", "Total traffic per port", "Failed login attempts"], correctAnswer: 1, explanation: "dc() counts distinct values — this query finds how many unique source IPs connected to each destination port, useful for detecting port scans." },
      { id: "sap-q13-8", question: "A SIEM correlation rule triggers when 5+ failed logins from the same IP are followed by a successful login within 10 minutes. What attack does this detect?", options: ["Brute force with eventual success", "Lateral movement", "Phishing", "Privilege escalation"], correctAnswer: 0, explanation: "Multiple failures followed by success is the classic signature of a successful brute-force or password-spraying attack." },
      { id: "sap-q13-9", question: "What is the biggest risk of overly sensitive SIEM correlation rules?", options: ["Missing real attacks", "Slower search performance", "Increased storage costs", "Alert fatigue from excessive false positives"], correctAnswer: 3, explanation: "Overly sensitive rules generate excessive false positives, causing alert fatigue — analysts start ignoring or auto-closing alerts, missing real threats." },
      // Module 4 — Endpoint Investigation
      { id: "sap-q13-10", question: "Which Windows registry key is commonly used by malware for persistence via auto-start?", options: ["HKLM\\SYSTEM\\CurrentControlSet", "HKLM\\SOFTWARE\\Classes", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "HKCU\\Control Panel\\Desktop"], correctAnswer: 2, explanation: "The Run/RunOnce keys under CurrentVersion execute programs at user logon — a top persistence mechanism for malware." },
      { id: "sap-q13-11", question: "You find a suspicious process with PID 4892 spawned by PowerShell. Which Windows Event ID would log this process creation?", options: ["4688", "4624", "1102", "7045"], correctAnswer: 0, explanation: "Event ID 4688 (Process Creation) logs new process details including parent process, command line, and user context." },
      { id: "sap-q13-12", question: "On Linux, an attacker adds a cron job for persistence. Where would you find it?", options: ["/proc/meminfo", "/etc/crontab and /var/spool/cron/", "/var/log/auth.log", "/etc/passwd"], correctAnswer: 1, explanation: "Cron persistence is found in /etc/crontab, /etc/cron.d/, and user-specific files under /var/spool/cron/." },
      // Module 5 — Phishing & Email Analysis
      { id: "sap-q13-13", question: "An email passes SPF but fails DKIM. The 'From' header shows company.com but 'Return-Path' shows attacker.xyz. What is this?", options: ["SPF-aligned spoofing", "DMARC pass", "Legitimate email", "Domain impersonation with header manipulation"], correctAnswer: 3, explanation: "The attacker configured SPF for their domain (attacker.xyz) but spoofed the visible 'From' header — DKIM failure and mismatched domains confirm spoofing." },
      { id: "sap-q13-14", question: "You receive a phishing email with a .html attachment. What is the most likely attack technique?", options: ["Man-in-the-browser", "DNS poisoning", "HTML smuggling delivering a payload via JavaScript", "Macro-based malware"], correctAnswer: 2, explanation: "HTML smuggling uses JavaScript in .html attachments to reconstruct and download malicious payloads, bypassing email gateway file-type scanning." },
      // Module 6 — Incident Handling
      { id: "sap-q13-15", question: "During a ransomware incident, what is the FIRST action an analyst should take?", options: ["Isolate affected systems from the network", "Pay the ransom", "Notify the media", "Wipe affected systems"], correctAnswer: 0, explanation: "Immediate network isolation prevents lateral spread while preserving evidence for investigation." },
      { id: "sap-q13-16", question: "What is the correct order of the NIST incident response lifecycle?", options: ["Triage, Investigate, Remediate, Close", "Identify, Protect, Detect, Respond, Recover", "Detect, Contain, Eradicate, Recover", "Preparation → Detection & Analysis → Containment, Eradication & Recovery → Post-Incident Activity"], correctAnswer: 3, explanation: "NIST SP 800-61 defines four phases: Preparation → Detection & Analysis → Containment/Eradication/Recovery → Post-Incident Activity." },
      { id: "sap-q13-17", question: "Chain of custody documentation must include all EXCEPT:", options: ["Hash values of digital evidence", "The analyst's personal opinion on guilt", "Who handled the evidence", "When it was transferred"], correctAnswer: 1, explanation: "Chain of custody tracks who, when, where, and integrity (hashes) — personal opinions have no place in evidence documentation." },
      // Module 7 — Cloud Security Monitoring
      { id: "sap-q13-18", question: "An AWS CloudTrail log shows 'DeleteTrail' API call from an unfamiliar IAM user. What is the severity?", options: ["Critical — potential attacker covering tracks", "Low — routine maintenance", "Informational only", "Medium — review needed"], correctAnswer: 0, explanation: "Deleting CloudTrail is a critical indicator of an attacker attempting to disable logging and cover their tracks." },
      { id: "sap-q13-19", question: "In Azure, which log source records sign-in activity including MFA status and conditional access results?", options: ["NSG Flow Logs", "Activity Log", "Azure AD Sign-in Logs", "Resource Logs"], correctAnswer: 2, explanation: "Azure AD Sign-in Logs capture authentication events including MFA challenges, conditional access policy results, and sign-in risk." },
      { id: "sap-q13-20", question: "A Kubernetes pod is running with 'privileged: true' security context. Why is this a critical finding?", options: ["It bypasses load balancing", "It uses more memory", "It can't connect to services", "The container has full host access, enabling container escape"], correctAnswer: 3, explanation: "Privileged containers have unrestricted host access — an attacker inside can escape to the host node and compromise the cluster." },
      // Module 8 — Threat Intelligence & Hunting
      { id: "sap-q13-21", question: "What is the difference between strategic and tactical threat intelligence?", options: ["Strategic informs long-term decisions for leadership; tactical provides IOCs for defenders", "Strategic is automated, tactical is manual", "Strategic is for analysts, tactical is for executives", "They are the same thing"], correctAnswer: 0, explanation: "Strategic TI informs executive risk decisions (trends, actor motivations); tactical TI provides actionable IOCs and TTPs for SOC analysts." },
      { id: "sap-q13-22", question: "In a hypothesis-driven hunt, you hypothesize 'attackers are using living-off-the-land binaries.' Which data source is MOST relevant?", options: ["DHCP leases", "Badge access logs", "Firewall logs", "Process creation logs with command-line arguments"], correctAnswer: 3, explanation: "LOLBin hunting requires process creation logs (Sysmon Event 1 / Windows 4688) with full command-line recording to spot abuse of legitimate tools." },
      { id: "sap-q13-23", question: "What STIX object type represents an adversary group like APT29?", options: ["Course of Action", "Observed Data", "Intrusion Set", "Indicator"], correctAnswer: 2, explanation: "Intrusion Set represents a named threat actor group with associated TTPs, motivations, and attributed campaigns." },
      // Module 9 — Digital Forensics
      { id: "sap-q13-24", question: "During disk imaging, the hash of the image differs from the original. What does this mean?", options: ["Normal for large drives", "The imaging process corrupted or modified data — the image is forensically unsound", "The drive is encrypted", "The image is fine — hashes vary"], correctAnswer: 1, explanation: "Hash mismatch means the forensic image is not a bit-for-bit copy — it cannot be used as evidence and must be re-imaged." },
      { id: "sap-q13-25", question: "You find $STANDARD_INFORMATION timestamps showing 2024 but $FILE_NAME timestamps showing 2025 on the same file. What does this indicate?", options: ["Timestomping — the attacker backdated $SI timestamps", "Time zone difference", "File corruption", "Normal behavior"], correctAnswer: 0, explanation: "$SI timestamps are easily modified by tools like Timestomp, but $FN timestamps are harder to forge — discrepancy proves manipulation." },
      // Cross-Module Scenario Questions
      { id: "sap-q13-26", question: "An alert fires for outbound DNS requests to a domain with high entropy. Network logs show 500+ TXT queries in 10 minutes. Endpoint logs show powershell.exe spawning nslookup. What is happening?", options: ["DNSSEC validation", "DNS cache poisoning", "DNS-based data exfiltration via PowerShell", "Normal DNS resolution"], correctAnswer: 2, explanation: "High-entropy domains + excessive TXT queries + PowerShell launching nslookup = classic DNS tunneling exfiltration pattern." },
      { id: "sap-q13-27", question: "During an investigation, you need to prove that a specific user account accessed sensitive files at 3 AM. Which THREE evidence sources would you correlate?", options: ["Antivirus alerts + proxy logs + printer logs", "Email logs + badge access + phone records", "Firewall logs + DNS logs + DHCP", "Windows 4663 (file access) + 4624 (logon) + VPN logs"], correctAnswer: 3, explanation: "4663 proves file access, 4624 proves authentication, and VPN logs prove remote origin — together they establish who, what, when, and from where." },
      { id: "sap-q13-28", question: "A SIEM alert shows a service account making API calls to AWS S3 at 2 AM. CloudTrail shows ListBuckets followed by GetObject on sensitive data. The account has no recent legitimate usage. Your FIRST action?", options: ["Investigate the API call source, verify if the access key is compromised, and isolate", "Delete the service account", "Notify the media", "Ignore — service accounts run automated tasks"], correctAnswer: 0, explanation: "Investigate first — identify the calling IP, check for key compromise, then isolate. Don't delete (destroys evidence) or ignore (could be active breach)." },
      { id: "sap-q13-29", question: "You're writing an incident report for a phishing attack that led to credential theft and lateral movement. Which section is MOST important for preventing recurrence?", options: ["Timeline of events", "Lessons learned and recommendations", "Executive summary", "Appendix with IOCs"], correctAnswer: 1, explanation: "Lessons learned drive organizational improvement — recommending MFA, email filtering, and user training prevents future similar attacks." },
      { id: "sap-q13-30", question: "Rank the following evidence by volatility (most volatile first): (1) RAM contents, (2) Swap/pagefile, (3) Disk image, (4) Network connections", options: ["3, 2, 1, 4", "2, 3, 4, 1", "4, 1, 2, 3", "1, 4, 2, 3"], correctAnswer: 3, explanation: "Per RFC 3227 order of volatility: RAM (seconds) → Network connections (seconds) → Swap (persistent but overwritten) → Disk (most stable)." }
    ]
  },
  // NETWORK SECURITY MONITORING — FINAL CERTIFICATION EXAM
  {
    quizId: "nsm-q7",
    courseId: "network-security-monitoring",
    title: "NSM Certification Exam",
    description: "Comprehensive final exam covering all 6 modules. You must pass with 80% or higher to earn your Network Security Monitoring certificate.",
    passingScore: 80,
    timeLimit: 60,
    questions: [
      { id: "nsm-q7-1", question: "What is the primary difference between IDS and IPS?", options: ["IDS monitors and alerts, IPS actively blocks malicious traffic", "They are identical", "IPS only works on endpoints", "IDS blocks traffic, IPS monitors"], correctAnswer: 0, explanation: "IDS passively monitors and alerts; IPS sits inline and actively blocks or drops malicious traffic." },
      { id: "nsm-q7-2", question: "Which Wireshark filter shows only HTTP POST requests?", options: ["tcp.port == 80", "http contains POST", "http.method == GET", "http.request.method == POST"], correctAnswer: 3, explanation: "http.request.method == POST filters specifically for HTTP POST requests in Wireshark." },
      { id: "nsm-q7-3", question: "In a TCP three-way handshake, what flags are exchanged?", options: ["RST, SYN, ACK", "FIN, FIN-ACK, ACK", "SYN, SYN-ACK, ACK", "SYN, ACK, FIN"], correctAnswer: 2, explanation: "The three-way handshake is: Client sends SYN → Server responds SYN-ACK → Client sends ACK." },
      { id: "nsm-q7-4", question: "What does a Suricata rule with 'action: drop' do differently from 'action: alert'?", options: ["Drop logs more detail", "Alert blocks the packet", "Nothing different", "Drop silently blocks the packet inline; alert only generates a notification"], correctAnswer: 3, explanation: "In IPS mode, 'drop' blocks the packet and generates an alert; 'alert' only generates the notification without blocking." },
      { id: "nsm-q7-5", question: "Which Suricata keyword inspects the HTTP URI path?", options: ["flow", "http_uri", "pcre", "content"], correctAnswer: 1, explanation: "http_uri matches against the URI path component of HTTP requests, enabling precise URL-based detection." },
      { id: "nsm-q7-6", question: "What is the primary purpose of Zeek's conn.log?", options: ["Track user logins", "Store packet payloads", "Log DNS queries", "Record metadata for every network connection including duration, bytes, and state"], correctAnswer: 3, explanation: "conn.log records connection-level metadata: source/dest IPs, ports, protocol, duration, bytes transferred, and connection state." },
      { id: "nsm-q7-7", question: "You observe DNS queries for random 32-character subdomains of a single domain. What technique is this?", options: ["DNSSEC validation", "CDN resolution", "DNS tunneling for C2 or data exfiltration", "DNS load balancing"], correctAnswer: 2, explanation: "Random long subdomains indicate DNS tunneling — data is encoded in subdomain labels to bypass traditional security controls." },
      { id: "nsm-q7-8", question: "What BPF filter captures only traffic on port 443?", options: ["port 443", "dst port 443", "port == 443", "tcp port 443"], correctAnswer: 0, explanation: "'port 443' captures both TCP and UDP traffic to/from port 443. Use 'tcp port 443' for TCP only." },
      { id: "nsm-q7-9", question: "In Zeek's ssl.log, what does the 'validation_status' field indicate?", options: ["Whether the server certificate chain was successfully validated", "TLS version", "Handshake duration", "Cipher strength"], correctAnswer: 0, explanation: "validation_status shows if Zeek could validate the certificate chain — 'ok' means valid, failures may indicate self-signed or expired certs." },
      { id: "nsm-q7-10", question: "What network behavior indicates lateral movement via SMB?", options: ["ICMP echo requests", "Internal host connecting to port 445 on multiple internal hosts sequentially", "DNS queries to public resolvers", "HTTPS to external IPs"], correctAnswer: 1, explanation: "Sequential SMB (port 445) connections from one internal host to many others indicates lateral movement or SMB-based worm propagation." },
      { id: "nsm-q7-11", question: "What Wireshark feature reconstructs transferred files from packet captures?", options: ["Protocol preferences", "Statistics panel", "Display filters", "Export Objects (File > Export Objects)"], correctAnswer: 3, explanation: "Export Objects extracts files transferred over HTTP, SMB, TFTP, and other protocols directly from the pcap." },
      { id: "nsm-q7-12", question: "A Suricata rule uses 'threshold: type both, track by_src, count 10, seconds 60'. What does this mean?", options: ["Log every 10th packet", "Alert once and suppress for 60s after 10 matches from the same source", "Block after 10 packets", "Alert on every packet"], correctAnswer: 1, explanation: "Type 'both' combines threshold (require N matches) and limit (suppress duplicates) — alert once per 60s window after 10 matches from same source." },
      { id: "nsm-q7-13", question: "What is JA3 fingerprinting used for?", options: ["Certificate validation", "DNS query analysis", "Creating unique fingerprints of TLS client hello parameters to identify applications", "Identifying file types"], correctAnswer: 2, explanation: "JA3 hashes TLS client hello fields (version, ciphers, extensions) creating a fingerprint that identifies the client application regardless of IP." },
      { id: "nsm-q7-14", question: "You see regular outbound connections every 300 seconds to the same external IP on port 8443. What is this pattern?", options: ["C2 beaconing with a 5-minute interval", "Time synchronization", "Web browsing", "Email checking"], correctAnswer: 0, explanation: "Regular interval connections (beaconing) to a fixed external IP on a non-standard port is a strong indicator of C2 communication." },
      { id: "nsm-q7-15", question: "Which Zeek log would help identify a DNS amplification attack?", options: ["http.log", "ssl.log", "conn.log", "dns.log showing large TXT/ANY responses to spoofed source IPs"], correctAnswer: 3, explanation: "DNS amplification uses large responses (TXT/ANY) directed at spoofed victim IPs — dns.log shows query types and response sizes." },
      { id: "nsm-q7-16", question: "What is the purpose of network tap vs SPAN port?", options: ["Tap only works for wireless", "SPAN is more reliable", "Tap provides lossless full-duplex copy; SPAN may drop packets under load", "They are identical"], correctAnswer: 2, explanation: "Network taps provide passive, lossless, full-duplex copies. SPAN ports can drop packets under high load and may miss errors." },
      { id: "nsm-q7-17", question: "How do you detect ICMP tunneling in network traffic?", options: ["Monitor ICMP TTL values", "Unusually large ICMP payloads or high-frequency echo requests with varying data", "Check for ICMP type 0", "Look for ICMP type 8 only"], correctAnswer: 1, explanation: "ICMP tunneling embeds data in echo request/reply payloads — look for abnormally large payloads or high volumes of ICMP with varied data." },
      { id: "nsm-q7-18", question: "What does Zeek's 'notice.log' record?", options: ["File hashes", "DNS queries", "High-level security-relevant events and anomalies detected by Zeek's Notice framework", "All network connections"], correctAnswer: 2, explanation: "notice.log captures security-relevant findings like self-signed certs, SSL errors, scan detection, and custom notices from Zeek scripts." },
      { id: "nsm-q7-19", question: "In Wireshark, how do you follow the full conversation of a TCP stream?", options: ["Export as CSV", "Right-click a packet → Follow → TCP Stream", "Use Statistics menu", "Apply display filter"], correctAnswer: 1, explanation: "Follow TCP Stream reconstructs the entire conversation between client and server, showing data in both directions." },
      { id: "nsm-q7-20", question: "What makes encrypted traffic analysis challenging for NSM?", options: ["It uses different ports", "It's faster than unencrypted", "It's impossible to analyze", "Content is opaque, requiring metadata analysis (JA3, certificate, timing, volume) instead of payload inspection"], correctAnswer: 3, explanation: "Encrypted payloads can't be inspected, so analysts rely on metadata: JA3 fingerprints, certificate details, connection timing, and data volumes." },
      { id: "nsm-q7-21", question: "A host suddenly generates traffic to 1000+ unique destination IPs on port 445 in 2 minutes. What is this?", options: ["Backup operation", "Load balancing", "Normal file sharing", "SMB worm propagation or network scanning"], correctAnswer: 3, explanation: "Rapid connections to many IPs on port 445 indicates SMB-based worm propagation (like WannaCry) or aggressive network scanning." },
      { id: "nsm-q7-22", question: "What Suricata keyword matches on file content extracted from network streams?", options: ["filedata", "http_uri", "flow", "content"], correctAnswer: 0, explanation: "filedata matches on reassembled file content from HTTP, SMTP, and other protocols — used for detecting malicious file transfers." },
      { id: "nsm-q7-23", question: "How does TLS certificate pinning affect network security monitoring?", options: ["Has no effect", "Improves log quality", "Makes monitoring easier", "Prevents MITM inspection proxies from decrypting traffic, creating visibility gaps"], correctAnswer: 3, explanation: "Certificate pinning rejects certificates not matching the expected pin, preventing TLS inspection proxies from intercepting — creating blind spots." },
      { id: "nsm-q7-24", question: "What is the significance of TTL values in network forensics?", options: ["They measure latency", "They indicate bandwidth", "TTL reveals hop count and can detect spoofed packets or traceroute activity", "They indicate encryption strength"], correctAnswer: 2, explanation: "TTL decrements per hop — unusual TTL values can reveal spoofed source IPs, traceroute scanning, or MITM positioning." },
      { id: "nsm-q7-25", question: "You capture traffic showing HTTP requests with 'User-Agent: Mozilla/4.0 (compatible; MSIE 6.0)' from a Windows 11 machine. What does this suggest?", options: ["Browser downgrade", "Legacy application", "Malware using a hardcoded outdated User-Agent string for C2", "Normal browsing"], correctAnswer: 2, explanation: "IE6 User-Agent from Windows 11 is impossible legitimately — malware often uses hardcoded outdated User-Agent strings in C2 communication." },
      { id: "nsm-q7-26", question: "What is the advantage of full packet capture (PCAP) over flow data (NetFlow)?", options: ["Easier to store long-term", "PCAP preserves complete payload content for deep inspection and evidence", "Faster to process", "Uses less storage"], correctAnswer: 1, explanation: "PCAP captures entire packets including payloads, enabling content inspection, file extraction, and forensic evidence — NetFlow only records metadata." },
      { id: "nsm-q7-27", question: "How would you detect DNS over HTTPS (DoH) being used to bypass DNS monitoring?", options: ["Identify connections to known DoH resolver IPs (e.g., 1.1.1.1:443, 8.8.8.8:443) or JA3 fingerprints", "Block all HTTPS", "Check DNS logs", "Monitor port 53"], correctAnswer: 0, explanation: "DoH encrypts DNS in HTTPS — detect by monitoring connections to known DoH providers or identifying DoH-specific JA3 fingerprints." },
      { id: "nsm-q7-28", question: "What network evidence would indicate a successful SQL injection attack?", options: ["ICMP errors", "High DNS query volume", "Normal web traffic", "HTTP responses containing database error messages or bulk data dumps"], correctAnswer: 3, explanation: "Successful SQLi shows in HTTP responses — database errors, unexpected data structures, or unusually large response bodies containing exfiltrated data." },
      { id: "nsm-q7-29", question: "In a SOC workflow, when should you escalate a network alert to an incident?", options: ["Only if the SIEM says so", "Immediately on any alert", "When corroborated by multiple data sources confirming malicious activity with business impact", "Never"], correctAnswer: 2, explanation: "Escalate when investigation confirms the alert with additional evidence (endpoint, identity, threat intel) and there's actual or potential business impact." },
      { id: "nsm-q7-30", question: "What is the best practice for sensor placement in a segmented network?", options: ["One sensor per floor", "One sensor at the perimeter only", "Sensors only on servers", "Sensors at each trust boundary — perimeter, DMZ, between VLANs, and critical segments"], correctAnswer: 3, explanation: "Sensors at each trust boundary provide visibility into north-south (perimeter) and east-west (lateral) traffic across all network segments." }
    ]
  },
  // INCIDENT RESPONSE FUNDAMENTALS — FINAL CERTIFICATION EXAM
  {
    quizId: "ir-q7",
    courseId: "incident-response",
    title: "IR Certification Exam",
    description: "Comprehensive final exam covering all 6 modules. You must pass with 80% or higher to earn your Incident Response Fundamentals certificate.",
    passingScore: 80,
    timeLimit: 60,
    questions: [
      { id: "ir-q7-1", question: "What are the four phases of the NIST SP 800-61 incident response lifecycle?", options: ["Plan, Do, Check, Act", "Triage, Investigate, Remediate, Close", "Preparation; Detection & Analysis; Containment, Eradication & Recovery; Post-Incident Activity", "Identify, Protect, Detect, Respond"], correctAnswer: 2, explanation: "NIST SP 800-61 defines: Preparation → Detection & Analysis → Containment/Eradication/Recovery → Post-Incident Activity." },
      { id: "ir-q7-2", question: "What is the SANS six-step IR process?", options: ["Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned", "Alert, Triage, Investigate, Fix, Test, Document", "Detect, Analyze, Contain, Remove, Restore, Report", "Plan, Execute, Review, Close, Report, Archive"], correctAnswer: 0, explanation: "SANS PICERL: Preparation → Identification → Containment → Eradication → Recovery → Lessons Learned." },
      { id: "ir-q7-3", question: "During preparation, what is the primary purpose of a tabletop exercise?", options: ["Audit compliance", "Walk through incident scenarios to identify gaps in plans and communication", "Test network bandwidth", "Train new employees"], correctAnswer: 1, explanation: "Tabletop exercises simulate incidents to test response procedures, identify weaknesses, and improve team coordination without real impact." },
      { id: "ir-q7-4", question: "An analyst receives an alert for a potential ransomware infection. What should they do FIRST?", options: ["Verify the alert and assess scope before taking containment action", "Format the machine", "Pay the ransom", "Notify the CEO"], correctAnswer: 0, explanation: "Always verify and assess first — determine if the alert is a true positive, identify affected systems, and understand scope before acting." },
      { id: "ir-q7-5", question: "What is the difference between short-term and long-term containment?", options: ["Short-term stops immediate spread (isolate host); long-term applies durable controls (patch, harden) while maintaining operations", "They are the same", "Short-term is for minor incidents only", "Long-term means ignoring the incident"], correctAnswer: 0, explanation: "Short-term containment is immediate (network isolation, disable accounts). Long-term containment applies sustained fixes while keeping business running." },
      { id: "ir-q7-6", question: "What evidence should be collected FIRST based on order of volatility?", options: ["Hard drive image", "System logs", "Registry hives", "Memory (RAM) dump"], correctAnswer: 3, explanation: "RAM is the most volatile — it's lost on reboot. Always collect memory first, then move to less volatile sources per RFC 3227." },
      { id: "ir-q7-7", question: "During eradication, what must you do after removing malware from a compromised system?", options: ["Delete all user data", "Verify removal, patch the vulnerability exploited, and validate no persistence mechanisms remain", "Immediately reconnect to network", "Reinstall the operating system only"], correctAnswer: 1, explanation: "After removal: verify clean state, patch the entry point, check for backdoors/persistence, and validate before returning to production." },
      { id: "ir-q7-8", question: "What is the primary purpose of an incident severity classification matrix?", options: ["Prioritize response efforts based on business impact, scope, and data sensitivity", "Assign blame", "Track employee performance", "Calculate insurance claims"], correctAnswer: 0, explanation: "Severity matrices ensure consistent prioritization — critical incidents (data breach, ransomware) get immediate resources; low-severity get scheduled response." },
      { id: "ir-q7-9", question: "When communicating during a major incident, who should serve as the single point of contact for external parties?", options: ["The IT help desk", "The designated incident commander or communications lead", "Any available analyst", "The CEO directly"], correctAnswer: 1, explanation: "A designated communications lead ensures consistent messaging, prevents conflicting statements, and manages stakeholder expectations." },
      { id: "ir-q7-10", question: "What legal consideration is critical when collecting evidence from a cloud environment?", options: ["Only local laws apply", "Just download everything", "Data jurisdiction — evidence may span multiple legal jurisdictions with different privacy laws", "Cloud evidence doesn't matter"], correctAnswer: 2, explanation: "Cloud data may reside in multiple countries with different privacy laws (GDPR, CCPA) — understand jurisdictional requirements before collection." },
      { id: "ir-q7-11", question: "What makes a forensic image 'forensically sound'?", options: ["It's created by law enforcement", "It's stored on the cloud", "It's compressed", "Hash verification proves it's a bit-for-bit copy of the original with documented chain of custody"], correctAnswer: 3, explanation: "Forensic soundness requires verified hash match (SHA-256), write-blocking during acquisition, and documented chain of custody." },
      { id: "ir-q7-12", question: "During a BEC (Business Email Compromise) incident, what is the FIRST containment action?", options: ["Reset compromised credentials and revoke active sessions immediately", "Shut down the mail server", "Delete all emails", "Notify all employees"], correctAnswer: 0, explanation: "Immediately reset passwords and revoke OAuth tokens/sessions to prevent further unauthorized access before the attacker can pivot." },
      { id: "ir-q7-13", question: "What is the purpose of IOC (Indicator of Compromise) sharing during incident response?", options: ["Required by law", "Show off findings", "Enable other organizations to detect the same threat and improve collective defense", "Only for internal use"], correctAnswer: 2, explanation: "Sharing IOCs (hashes, IPs, domains) via ISACs, STIX/TAXII enables peer organizations to proactively detect and block the same threat." },
      { id: "ir-q7-14", question: "What should a post-incident review (lessons learned) meeting focus on?", options: ["Assigning blame to individuals", "Process improvements, timeline accuracy, communication gaps, and detection enhancements", "Celebrating the team", "Compliance checkbox"], correctAnswer: 1, explanation: "Blameless post-incident reviews focus on what happened, what worked, what didn't, and actionable improvements to prevent recurrence." },
      { id: "ir-q7-15", question: "An attacker uses stolen credentials to access a VPN. What log sources confirm this?", options: ["Physical access logs only", "Only firewall logs", "Email logs only", "VPN authentication logs + AD/LDAP logs + endpoint logs showing the source machine"], correctAnswer: 3, explanation: "Correlate VPN auth logs (login time, IP), AD logs (credential validation), and endpoint logs (source machine activity) to confirm credential abuse." },
      { id: "ir-q7-16", question: "What is 'scope creep' in incident response and how do you prevent it?", options: ["Investigation expanding beyond the actual incident boundary — prevent with clear scoping and regular reassessment", "It's a good thing", "You can't prevent it", "It means the incident is growing"], correctAnswer: 0, explanation: "Scope creep wastes resources investigating unrelated issues. Define incident boundaries early and regularly reassess to stay focused." },
      { id: "ir-q7-17", question: "When is it appropriate to involve law enforcement in an incident?", options: ["Never", "When criminal activity is suspected, data breach notification laws require it, or for evidence preservation orders", "Always, for every incident", "Only for nation-state attacks"], correctAnswer: 1, explanation: "Involve law enforcement for criminal activity, when legally required (breach notification), or when you need legal authority (subpoenas, preservation orders)." },
      { id: "ir-q7-18", question: "What metric measures the average time from detection to containment?", options: ["MTTD", "MTTF", "MTTC (Mean Time to Contain)", "MTTR"], correctAnswer: 2, explanation: "MTTC measures the average time from detecting an incident to successfully containing it — a key IR efficiency metric." },
      { id: "ir-q7-19", question: "During recovery, what must be verified before bringing systems back to production?", options: ["Only that the system boots", "Backup completed", "User passwords changed", "Clean bill of health: malware removed, vulnerability patched, no persistence, monitoring in place"], correctAnswer: 3, explanation: "Before production return: confirm eradication complete, patch applied, persistence removed, enhanced monitoring active, and baseline restored." },
      { id: "ir-q7-20", question: "What is the role of threat intelligence in incident response?", options: ["It's not relevant to IR", "Provides context on attacker TTPs, helps predict next moves, and accelerates investigation through known IOCs", "Only useful for prevention", "Replaces investigation"], correctAnswer: 1, explanation: "TI maps incidents to known threat actors/campaigns, predicts attacker behavior, provides additional IOCs, and helps determine incident severity." },
      { id: "ir-q7-21", question: "A phishing email delivered a trojan that established persistence. Order the IR actions correctly:", options: ["Eradicate, then contain, then detect", "Ignore and monitor", "Detect → Contain (isolate host) → Eradicate (remove malware + persistence) → Recover (patch + monitor)", "Recover first, then investigate"], correctAnswer: 2, explanation: "Follow the lifecycle: detect the compromise, contain by isolating, eradicate malware and persistence mechanisms, then recover with hardening." },
      { id: "ir-q7-22", question: "What is a 'jump bag' in IR preparation?", options: ["A travel bag", "An emergency contact list", "A software toolkit", "A pre-packed kit with forensic tools, documentation, cables, and storage media for rapid deployment"], correctAnswer: 3, explanation: "Jump bags contain physical and digital tools (write blockers, forensic drives, documentation templates) for rapid on-site response." },
      { id: "ir-q7-23", question: "How should you handle conflicting indicators during analysis — some pointing to true positive, others to false positive?", options: ["Close as false positive", "Gather additional evidence from multiple sources to reach a confident determination", "Escalate immediately", "Flip a coin"], correctAnswer: 1, explanation: "When indicators conflict, expand your data sources — check additional logs, threat intel, and endpoint telemetry to build confidence before deciding." },
      { id: "ir-q7-24", question: "What Windows artifacts prove an executable ran on a system?", options: ["File existence alone", "Only antivirus logs", "Prefetch files, Shimcache, Amcache, UserAssist, and BAM/DAM", "Registry Run keys only"], correctAnswer: 2, explanation: "Multiple artifacts independently prove execution: Prefetch (run count/timestamps), Shimcache, Amcache (SHA1 hash), and UserAssist (GUI programs)." },
      { id: "ir-q7-25", question: "What is the biggest risk of not conducting lessons learned after an incident?", options: ["Wasting time", "No risk at all", "Losing certifications", "Repeating the same mistakes — failing to improve processes, close detection gaps, and strengthen defenses"], correctAnswer: 3, explanation: "Without lessons learned, organizations repeat failures — the same attack vectors succeed again, detection gaps persist, and response doesn't improve." },
      { id: "ir-q7-26", question: "During a supply chain compromise, what makes containment uniquely challenging?", options: ["Supply chain attacks are rare", "The malicious code is in trusted, legitimately signed software — you can't just block the vendor", "Only affects one system", "It's the same as any incident"], correctAnswer: 1, explanation: "Supply chain compromises embed in trusted software with valid signatures, making detection and containment complex — blocking the vendor disrupts operations." },
      { id: "ir-q7-27", question: "What information MUST an incident report's executive summary contain?", options: ["Full technical details", "Employee names", "Every IOC found", "Business impact, scope, timeline summary, and key recommendations in non-technical language"], correctAnswer: 3, explanation: "Executive summaries communicate business impact, affected scope, high-level timeline, and actionable recommendations for leadership decision-making." },
      { id: "ir-q7-28", question: "How do you determine if an incident is a data breach requiring notification?", options: ["Every incident is a breach", "Only if data was sold", "Assess if regulated data (PII, PHI, financial) was accessed or exfiltrated, per applicable laws", "Ask the attacker"], correctAnswer: 2, explanation: "A breach requiring notification depends on data type (PII/PHI), access vs exfiltration evidence, and applicable regulations (GDPR, HIPAA, state laws)." },
      { id: "ir-q7-29", question: "What is the purpose of creating an incident timeline?", options: ["Reconstruct the sequence of events to understand attack progression and identify gaps in detection", "Fill out paperwork", "Track analyst hours", "Satisfy auditors"], correctAnswer: 0, explanation: "Timelines reveal attack progression, dwell time, detection delays, and response effectiveness — essential for root cause analysis and improvement." },
      { id: "ir-q7-30", question: "An incident involves a compromised service account with access to 50+ systems. What containment strategy is appropriate?", options: ["Disable all 50 systems", "Ignore it — service accounts aren't important", "Only reset the password", "Rotate the service account credentials, audit all systems it accessed, and implement enhanced monitoring"], correctAnswer: 3, explanation: "Rotate credentials immediately, audit all accessed systems for signs of compromise, and add monitoring — don't just reset password (attacker may have installed backdoors)." }
    ]
  },
  // THREAT HUNTING FUNDAMENTALS — FINAL CERTIFICATION EXAM
  {
    quizId: "th-q7",
    courseId: "threat-hunting",
    title: "Threat Hunting Certification Exam",
    description: "Comprehensive final exam covering all 6 modules. You must pass with 80% or higher to earn your Threat Hunting Fundamentals certificate.",
    passingScore: 80,
    timeLimit: 60,
    questions: [
      { id: "th-q7-1", question: "What fundamentally distinguishes threat hunting from traditional detection?", options: ["Hunting is proactive and hypothesis-driven; detection is reactive and alert-driven", "Hunting uses more tools", "There's no difference", "Hunting only uses automated tools"], correctAnswer: 0, explanation: "Hunting proactively searches for threats without alerts, using hypotheses. Detection relies on pre-built rules to generate alerts reactively." },
      { id: "th-q7-2", question: "In the Hunting Maturity Model (HMM), what characterizes Level 3 (Innovative)?", options: ["No hunting capability", "Following vendor playbooks only", "Only using threat intel feeds", "Hunters create custom data analysis techniques and automate hunt procedures"], correctAnswer: 3, explanation: "HMM Level 3 organizations develop original analytical methods, automate repetitive hunts, and contribute to community knowledge." },
      { id: "th-q7-3", question: "What is the Pyramid of Pain and why is it important for hunting?", options: ["A compliance framework", "A vulnerability scoring system", "Ranks indicator types by adversary cost to change — hunting TTPs forces highest adversary cost", "A training tool"], correctAnswer: 2, explanation: "The Pyramid of Pain shows that hunting for TTPs (top) is far more impactful than IOC matching (bottom) — attackers easily change hashes/IPs but struggle to change tactics." },
      { id: "th-q7-4", question: "You hypothesize APT actors are using scheduled tasks for persistence. What data do you hunt?", options: ["Email logs", "DNS queries", "Firewall logs", "Windows Event ID 4698 (scheduled task created) and schtasks.exe process creation logs"], correctAnswer: 3, explanation: "Event ID 4698 logs scheduled task creation details. Also hunt for schtasks.exe in process creation logs with suspicious command-line arguments." },
      { id: "th-q7-5", question: "What is a LOLBin and why are they challenging to detect?", options: ["A network protocol", "Legitimate OS binaries abused for malicious purposes — they blend with normal system activity", "A type of malware", "A vulnerability"], correctAnswer: 1, explanation: "Living-off-the-Land Binaries (LOLBins) like powershell, certutil, mshta are legitimate tools abused by attackers — hard to detect because they're expected on systems." },
      { id: "th-q7-6", question: "How do you build a hunt hypothesis from MITRE ATT&CK?", options: ["Only use the most popular techniques", "Use every technique", "Select a technique relevant to your threat model, identify expected data sources, and define what anomalous usage looks like", "Random selection"], correctAnswer: 2, explanation: "Map your threat model to ATT&CK techniques, identify relevant data sources (process, network, file), and define baseline vs anomalous behavior." },
      { id: "th-q7-7", question: "What is the 'noise reduction' technique in threat hunting?", options: ["Reducing log volume", "Ignoring false positives", "Turning off alerts", "Filtering out known-good activity to surface anomalies — whitelist legitimate baselines"], correctAnswer: 3, explanation: "Stack known-good patterns (legitimate processes, normal users, expected schedules) and filter them out to surface anomalous behavior for investigation." },
      { id: "th-q7-8", question: "You discover that certutil.exe downloaded a file from an external URL. Is this malicious?", options: ["Suspicious — certutil is a LOLBin commonly abused for file downloads; investigate context (user, URL, downloaded file)", "Always legitimate", "Always malicious", "Only if from the internet"], correctAnswer: 0, explanation: "certutil -urlcache -f is a known LOLBin technique (T1105). Investigate who ran it, what URL, what was downloaded, and the broader context." },
      { id: "th-q7-9", question: "What statistical technique helps identify C2 beaconing in network data?", options: ["Checking packet size only", "Analyzing inter-connection time intervals for low jitter (regularity) across multiple sessions", "Looking at port numbers", "Simple counting"], correctAnswer: 1, explanation: "C2 beacons have regular timing intervals. Calculate the standard deviation of connection intervals — low jitter indicates automated beaconing." },
      { id: "th-q7-10", question: "How does threat intelligence enhance hunt hypotheses?", options: ["It replaces hypotheses", "It's not useful for hunting", "Provides adversary TTPs, known IOCs, and campaign context to focus hunts on relevant threats", "Only adds IOCs to blocklists"], correctAnswer: 2, explanation: "TI provides context on active threat actors targeting your sector, their preferred TTPs, and specific IOCs to prioritize and focus hunt activities." },
      { id: "th-q7-11", question: "What is 'stacking' in hunt analysis?", options: ["Layering filters", "Aggregating values and sorting by frequency to identify rare outliers (least common analysis)", "Building a tech stack", "Combining tools"], correctAnswer: 1, explanation: "Stacking groups values (process names, parent-child relationships, DNS queries) by frequency — rare items (bottom of the stack) deserve investigation." },
      { id: "th-q7-12", question: "You're hunting for credential dumping. Which data sources are MOST relevant?", options: ["Email logs", "Physical access logs", "Process access to lsass.exe (Sysmon Event 10), NTDS.dit access, and suspicious registry queries", "Web proxy logs"], correctAnswer: 2, explanation: "Credential dumping targets lsass.exe memory (Mimikatz), NTDS.dit (domain), and SAM registry hives. Sysmon Event 10 logs process access to these." },
      { id: "th-q7-13", question: "What makes a good hunt hypothesis?", options: ["Based on gut feeling", "Focus only on known IOCs", "Be as broad as possible", "Testable, specific, tied to a technique/threat actor, and based on available data sources"], correctAnswer: 3, explanation: "Good hypotheses are specific (one technique), testable (data sources exist), threat-informed (relevant to your environment), and falsifiable." },
      { id: "th-q7-14", question: "How do you hunt for DLL sideloading?", options: ["Look for legitimate executables loading DLLs from unexpected paths or unsigned DLLs in trusted directories", "Monitor network traffic", "Check user permissions", "Scan for malware signatures"], correctAnswer: 0, explanation: "DLL sideloading abuses DLL search order — hunt for signed EXEs loading unsigned DLLs, or DLLs loading from non-standard directories." },
      { id: "th-q7-15", question: "What is the difference between IOC-based and TTP-based hunting?", options: ["IOC-based is more effective", "IOC-based matches specific artifacts (hashes, IPs); TTP-based hunts behavioral patterns regardless of specific indicators", "TTP-based is easier", "They're identical"], correctAnswer: 1, explanation: "IOC hunting is narrow and easily evaded (change hash = evade). TTP hunting finds behavioral patterns that persist across campaigns regardless of specific IOCs." },
      { id: "th-q7-16", question: "You find PowerShell executing encoded commands (-enc) at 3 AM from a service account. What is your assessment?", options: ["Block PowerShell entirely", "Ignore it", "Normal automation", "Highly suspicious — investigate the encoded command content, service account usage patterns, and triggering mechanism"], correctAnswer: 3, explanation: "Encoded PowerShell from a service account at unusual hours is a strong indicator. Decode the command, investigate the account, and check for lateral movement." },
      { id: "th-q7-17", question: "What is the purpose of documenting hunt findings even when no threats are found?", options: ["Required by regulations only", "Proves coverage, identifies data gaps, refines future hypotheses, and demonstrates security posture", "Only document positive findings", "Waste of time if nothing found"], correctAnswer: 1, explanation: "Negative results are valuable — they prove you checked, identify logging gaps, improve baselines, and help prioritize future hunts." },
      { id: "th-q7-18", question: "How do you detect process injection techniques during a hunt?", options: ["Monitor for processes accessing other processes' memory space (Sysmon Event 8/10, CreateRemoteThread)", "Check user logins", "Look at network logs", "Check file sizes"], correctAnswer: 0, explanation: "Process injection involves writing to and executing in another process — Sysmon Event 8 (CreateRemoteThread) and Event 10 (ProcessAccess) capture these." },
      { id: "th-q7-19", question: "What is the value of hunting in cloud environments (AWS/Azure/GCP)?", options: ["Same as on-premise", "Not possible to hunt in cloud", "Cloud APIs create rich audit trails (CloudTrail, Activity Logs) that can reveal unauthorized access and misconfigurations", "Cloud is secure by default"], correctAnswer: 2, explanation: "Cloud environments generate detailed API logs, enabling hunts for unusual API calls, privilege escalation, unauthorized access patterns, and misconfigurations." },
      { id: "th-q7-20", question: "What converts a successful hunt finding into an ongoing detection?", options: ["Adding to a report", "Nothing — hunts are one-time", "Emailing the team", "Translating the hunt query into a SIEM correlation rule or SIGMA detection with tuning and testing"], correctAnswer: 3, explanation: "Successful hunts should be operationalized — convert the search logic into SIGMA/SIEM rules, test against historical data, tune for false positives, and deploy." },
      { id: "th-q7-21", question: "You're hunting in network metadata and find a host making HTTPS connections to an IP with a self-signed certificate every 30 minutes. Assessment?", options: ["Likely C2 beaconing — self-signed cert + regular interval + IP-based (no domain) are strong indicators", "CDN behavior", "Normal HTTPS", "Certificate misconfiguration"], correctAnswer: 0, explanation: "Regular interval + self-signed cert + direct IP (no SNI/domain) is classic C2. Investigate the host, check process making connections, and analyze timing patterns." },
      { id: "th-q7-22", question: "What is 'threat-informed defense' and how does it relate to hunting?", options: ["Compliance requirement", "Using any threat data", "Prioritizing defenses based on real adversary behavior relevant to your organization — hunts validate these defenses", "A vendor product"], correctAnswer: 2, explanation: "Threat-informed defense uses real adversary intelligence to prioritize security. Hunts validate that defenses actually detect the prioritized TTPs." },
      { id: "th-q7-23", question: "How do you hunt for data exfiltration via cloud storage services?", options: ["Impossible to detect", "Monitor for unusual uploads to cloud storage APIs, large data transfers to cloud IPs, and cloud sync tool abuse", "Check email only", "Block all cloud"], correctAnswer: 1, explanation: "Hunt for unusual cloud storage API usage, large file uploads, cloud sync tools running from unexpected users/machines, and outbound data volume anomalies." },
      { id: "th-q7-24", question: "What is the role of automation in mature threat hunting programs?", options: ["Automate data collection, baseline enrichment, and routine hunts — freeing humans for creative hypothesis development", "Replace human hunters", "Only for alerts", "Automation isn't useful"], correctAnswer: 0, explanation: "Automation handles repetitive tasks (data gathering, enrichment, scheduled hunts) while humans focus on creative hypothesis development and complex analysis." },
      { id: "th-q7-25", question: "You discover WMI event subscriptions created on 5 servers at the same time. What does this indicate?", options: ["WMI error", "Normal administration", "Likely persistence mechanism deployed across multiple systems — investigate for compromise", "Monitoring tool deployment"], correctAnswer: 2, explanation: "Simultaneous WMI event subscription creation across multiple servers suggests automated persistence deployment — a strong indicator of coordinated compromise." },
      { id: "th-q7-26", question: "What metrics should a hunt team track?", options: ["Hours worked", "Only threats found", "Hunts completed, findings (true/false positives), detections created, data gaps identified, and coverage mapped", "Tools purchased"], correctAnswer: 2, explanation: "Track hunt volume, finding rates, detection conversions, gaps discovered, ATT&CK coverage improvements — these demonstrate program value and guide priorities." },
      { id: "th-q7-27", question: "How does YARA complement threat hunting?", options: ["Network monitoring tool", "Enables pattern-based scanning of files and memory for malware characteristics during endpoint hunts", "Only for email scanning", "Replaces hunting"], correctAnswer: 1, explanation: "YARA rules define pattern-based signatures (strings, hex, conditions) to scan files, memory, and processes during endpoint hunts for known malware families." },
      { id: "th-q7-28", question: "What challenge does 'living off the cloud' present compared to traditional LOLBins?", options: ["Easier to detect", "Only affects cloud environments", "No challenge", "Attackers abuse legitimate cloud services (OneDrive, GitHub, Slack) for C2 — traffic blends with legitimate business usage"], correctAnswer: 3, explanation: "Living off the cloud uses legitimate SaaS platforms for C2/exfiltration — traffic to these domains is expected, making detection extremely challenging." },
      { id: "th-q7-29", question: "When should hunt results be shared with the broader security team?", options: ["When asked", "Immediately for active threats; regularly for findings, new baselines, and detection recommendations", "Only in annual reports", "Never"], correctAnswer: 1, explanation: "Share active threats immediately for response. Regular sharing of findings, baselines, and detection recommendations improves the entire security program." },
      { id: "th-q7-30", question: "What is the ideal relationship between threat hunting and detection engineering?", options: ["A continuous loop — hunts discover threats that become detections; detection gaps inspire new hunts", "Hunting replaces detection", "They're separate functions", "Detection replaces hunting"], correctAnswer: 0, explanation: "Hunting and detection engineering form a virtuous cycle — hunt findings become new detections, and detection blind spots generate new hunt hypotheses." }
    ]
  },
  // DETECTION ENGINEERING BASICS — FINAL CERTIFICATION EXAM
 {
    quizId: "de-q7",
    courseId: "detection-engineering",
    title: "Detection Engineering Certification Exam",
    description: "Comprehensive final exam covering all 6 modules. You must pass with 80% or higher to earn your Detection Engineering Basics certificate.",
    passingScore: 80,
    timeLimit: 60,
    questions: [
      { id: "de-q7-1", question: "What is the primary goal of detection engineering?", options: ["Block all threats", "Replace SOC analysts", "Create high-fidelity, maintainable detection rules that reliably identify malicious activity with minimal false positives", "Automate all security"], correctAnswer: 2, explanation: "Detection engineering creates quality rules that analysts trust — balancing detection coverage with actionable, low-noise alerts." },
      { id: "de-q7-2", question: "What is a SIGMA rule?", options: ["A vendor-agnostic detection rule format that can be converted to multiple SIEM query languages", "A firewall rule", "An encryption algorithm", "A network protocol"], correctAnswer: 0, explanation: "SIGMA rules are written in YAML and define detections that can be automatically converted to Splunk SPL, Elastic KQL, Microsoft KQL, and more." },
      { id: "de-q7-3", question: "In a SIGMA rule, what does the 'logsource' section define?", options: ["The output format", "The SIEM vendor", "The alert severity", "The category, product, and service that generates the events the rule detects"], correctAnswer: 3, explanation: "logsource specifies where events come from (e.g., category: process_creation, product: windows) enabling correct backend conversion." },
      { id: "de-q7-4", question: "What SIGMA detection modifier matches any item in a list?", options: ["all", "The default OR logic when listing multiple values", "regex", "contains"], correctAnswer: 1, explanation: "By default, multiple values under a field use OR logic — any match triggers. Use 'all' modifier to require every value matches." },
      { id: "de-q7-5", question: "What is YARA primarily used for?", options: ["Log analysis", "User authentication", "Network monitoring", "Pattern-based file and memory scanning to identify and classify malware families"], correctAnswer: 3, explanation: "YARA defines rules with string patterns, hex sequences, and conditions to identify malware families in files, memory dumps, and process memory." },
      { id: "de-q7-6", question: "In a YARA rule, what does the 'condition' section do?", options: ["Defines the boolean logic that determines when a rule matches based on defined strings and metadata", "Lists file names", "Specifies the target OS", "Sets alert severity"], correctAnswer: 0, explanation: "The condition section combines string identifiers, counts, file size checks, and boolean logic to determine if a file matches the rule." },
      { id: "de-q7-7", question: "What is the difference between Sysmon Event ID 1 and Windows Event ID 4688?", options: ["4688 has more data", "Sysmon 1 is for network events", "Sysmon 1 provides richer data (hashes, parent command line, current directory); 4688 is native but less detailed", "They're identical"], correctAnswer: 2, explanation: "Sysmon Event 1 captures file hash, parent process command line, current directory, and more. 4688 is native but requires audit policy and provides less detail." },
      { id: "de-q7-8", question: "What log source would detect credential dumping from LSASS?", options: ["Web proxy logs", "DNS logs", "Firewall logs", "Sysmon Event 10 (ProcessAccess) targeting lsass.exe with suspicious access masks"], correctAnswer: 3, explanation: "Sysmon Event 10 logs when a process accesses another's memory — detecting tools like Mimikatz accessing lsass.exe for credential extraction." },
      { id: "de-q7-9", question: "What is 'Detection as Code'?", options: ["Coding a SIEM from scratch", "Managing detection rules with software engineering practices: version control, testing, CI/CD, and peer review", "Using AI for detection", "Writing detections in Python"], correctAnswer: 1, explanation: "Detection as Code applies DevOps practices to detection management — Git versioning, automated testing, CI/CD deployment, and code review for quality." },
      { id: "de-q7-10", question: "Why is unit testing important for detection rules?", options: ["Slows development", "Only for compliance", "Validates rules detect true positives and don't trigger on benign activity before production deployment", "It's not important"], correctAnswer: 2, explanation: "Unit tests verify detection logic against known-good and known-bad samples — catching false positives/negatives before rules impact production SOC." },
      { id: "de-q7-11", question: "What is the purpose of a detection coverage matrix mapped to MITRE ATT&CK?", options: ["Track analyst performance", "Visualize which techniques have detections and identify coverage gaps to prioritize development", "Compliance documentation", "List all SIEM rules"], correctAnswer: 1, explanation: "Coverage matrices show detection presence/absence per ATT&CK technique, revealing gaps that detection engineers should prioritize filling." },
      { id: "de-q7-12", question: "How do you measure detection rule quality?", options: ["True positive rate, false positive rate, mean time to detect, and analyst feedback on actionability", "Rule complexity", "Count of rules only", "Number of log sources"], correctAnswer: 0, explanation: "Quality metrics include TP/FP rates, detection latency, analyst satisfaction, and actionability — a high-TP, low-FP rule that analysts trust is high quality." },
      { id: "de-q7-13", question: "What is 'detection drift' and how do you prevent it?", options: ["Moving detections between SIEMs", "Normal behavior", "Detections improving over time", "Rules becoming ineffective as environments change — prevent with regular validation, testing, and coverage reviews"], correctAnswer: 3, explanation: "Detection drift occurs when environment changes (new tools, infrastructure) invalidate existing rules. Regular validation and automated testing prevent drift." },
      { id: "de-q7-14", question: "What is the 'base rate fallacy' in detection engineering?", options: ["A detection methodology", "A SIGMA feature", "A math error", "When a rare event detector generates more false positives than true positives due to the low prevalence of real attacks"], correctAnswer: 3, explanation: "Even a 99% accurate detector for a 1-in-million event will generate far more false positives than true positives — understanding this guides rule tuning." },
      { id: "de-q7-15", question: "How should you handle a detection rule with a 90% false positive rate?", options: ["Analyze FP patterns, add exclusions for known-good behavior, narrow scope, or restructure the detection logic", "Delete it immediately", "Lower the severity", "Ignore the FPs"], correctAnswer: 0, explanation: "Analyze FP patterns to identify what's triggering falsely, add targeted exclusions, narrow the rule scope, or redesign the detection approach entirely." },
      { id: "de-q7-16", question: "What is a SIGMA 'pipeline' in the context of rule conversion?", options: ["A network pipeline", "A CI/CD pipeline", "A transformation configuration that maps SIGMA field names and log sources to a specific SIEM's schema", "A data pipeline"], correctAnswer: 2, explanation: "SIGMA pipelines define field name mappings and log source translations for specific SIEM backends — ensuring rules convert correctly to target query languages." },
      { id: "de-q7-17", question: "When writing a detection for PowerShell abuse, what makes '-enc' or '-encodedcommand' detection insufficient?", options: ["It catches too many things", "Attackers can use partial parameter names (-e, -en, -enco) due to PowerShell's parameter abbreviation feature", "PowerShell doesn't support encoding", "It's a perfect detection"], correctAnswer: 1, explanation: "PowerShell accepts abbreviated parameters — detect all variations: -e, -en, -enc, -enco, -encod, etc., or use regex for robust matching." },
      { id: "de-q7-18", question: "What is the difference between a 'detection' and an 'analytic'?", options: ["Analytics replace detections", "Detections are automated, analytics are manual", "They're identical", "A detection generates alerts; an analytic provides data insights that may inform detections or hunts"], correctAnswer: 3, explanation: "Detections are alert-generating rules. Analytics are broader queries that surface patterns, trends, or anomalies — analytics may feed into detection development." },
      { id: "de-q7-19", question: "How do you detect 'parent-child process anomalies'?", options: ["Define expected parent-child relationships and alert on deviations (e.g., Excel spawning PowerShell)", "Monitor memory usage", "Check file names", "Check network connections"], correctAnswer: 0, explanation: "Baseline normal parent-child trees (explorer→chrome, services→svchost) and detect anomalies like winword.exe→powershell.exe or outlook.exe→cmd.exe." },
      { id: "de-q7-20", question: "What role does threat intelligence play in detection engineering prioritization?", options: ["TI identifies which ATT&CK techniques are actively used against your sector, focusing development on real threats", "No role", "Replaces detection engineering", "Only provides IOCs"], correctAnswer: 0, explanation: "TI informs which threat actors target your sector and their preferred techniques — enabling prioritized detection development for the most relevant threats." },
      { id: "de-q7-21", question: "What is a 'canary token' and how does it relate to detection?", options: ["A type of SIGMA rule", "A SIEM feature", "A tripwire — fake credentials, files, or DNS entries that generate alerts when accessed by attackers", "A monitoring agent"], correctAnswer: 2, explanation: "Canary tokens are decoy resources (fake admin creds, honeypot files, DNS canaries) that generate high-confidence alerts when touched — zero false positive detection." },
      { id: "de-q7-22", question: "What YARA feature enables hunting for packed or encrypted malware?", options: ["Math module for entropy calculation and file size conditions to identify suspicious sections", "Rule inheritance", "String matching", "Hex patterns only"], correctAnswer: 0, explanation: "The math module's entropy function identifies high-entropy sections (packed/encrypted data), combined with file size conditions to find suspicious binaries." },
      { id: "de-q7-23", question: "How should detection rules be versioned?", options: ["Email notifications", "Git with semantic versioning, changelogs documenting modifications, and tagged releases for production deployments", "Manual spreadsheet tracking", "No versioning needed"], correctAnswer: 1, explanation: "Git versioning with semantic versioning (major.minor.patch), detailed changelogs, and tagged releases enables rollback, audit trail, and collaboration." },
      { id: "de-q7-24", question: "What is the 'alert funnel' concept in detection engineering?", options: ["A SIEM feature", "A marketing term", "A visualization tool", "Progressively filtering events through correlation, enrichment, and scoring to surface only high-confidence alerts"], correctAnswer: 3, explanation: "The alert funnel reduces noise through layers: raw events → correlated alerts → enriched alerts → scored/prioritized alerts for analyst review." },
      { id: "de-q7-25", question: "How do you write a SIGMA rule to detect Mimikatz execution?", options: ["Block the hash", "Detect behavioral indicators: process accessing lsass.exe, specific command-line arguments, or known PE metadata", "Monitor port 445", "Match the filename 'mimikatz.exe'"], correctAnswer: 1, explanation: "Filename matching is trivially evaded. Detect behavior: lsass access patterns, known command-line arguments (sekurlsa, kerberos), or PE metadata indicators." },
      { id: "de-q7-26", question: "What is the purpose of detection rule deprecation?", options: ["Archive for compliance", "Formally retire rules that are no longer relevant, documented with rationale, to prevent rule bloat", "Delete old rules", "Upgrade rules automatically"], correctAnswer: 1, explanation: "Deprecation formally marks rules as retired with documented reasoning — preventing rule bloat while maintaining historical record for auditing." },
      { id: "de-q7-27", question: "How do you handle detection for techniques with many legitimate uses (e.g., PowerShell)?", options: ["Only detect known signatures", "Block the tool entirely", "Don't detect them", "Layer multiple behavioral indicators, use allowlists for known-good usage, and correlate with additional context"], correctAnswer: 3, explanation: "For dual-use tools: combine behavioral signals (unusual parent, encoded commands, network activity) with context (user, time, machine) and known-good exclusions." },
      { id: "de-q7-28", question: "What is the value of community-shared detection rules (e.g., SIGMA rules repository)?", options: ["Only for small teams", "Use them without modification", "Leverage collective expertise, accelerate coverage, and adapt proven rules to your environment", "No value — use only custom rules"], correctAnswer: 2, explanation: "Community rules provide broad coverage quickly. Adapt them to your environment's log sources, field names, and false positive patterns for maximum value." },
      { id: "de-q7-29", question: "What should a detection engineering program's maturity assessment include?", options: ["Coverage breadth, rule quality metrics, CI/CD maturity, testing practices, and ATT&CK mapping completeness", "Only rule count", "Team size", "Tool inventory"], correctAnswer: 0, explanation: "Maturity spans coverage (ATT&CK mapping), quality (TP/FP rates), engineering practices (CI/CD, testing), documentation, and continuous improvement processes." },
      { id: "de-q7-30", question: "You need to detect a new zero-day technique with no known signatures. What approach do you take?", options: ["Block everything", "Ignore until patches exist", "Develop behavioral detection based on the technique's observable actions rather than specific IOCs", "Wait for vendor signatures"], correctAnswer: 2, explanation: "Zero-days lack signatures. Detect the behavior — what the exploit does (process creation, file drops, network callbacks) rather than what the exploit looks like." }
    ]
  },
  // MALWARE ANALYSIS FUNDAMENTALS — FINAL CERTIFICATION EXAM
  {
    quizId: "ma-q7",
    courseId: "malware-analysis",
    title: "Malware Analysis Certification Exam",
    description: "Comprehensive final exam covering all 6 modules. You must pass with 80% or higher to earn your Malware Analysis Fundamentals certificate.",
    passingScore: 80,
    timeLimit: 60,
    questions: [{ id: "ma-q7-1", question: "What is the difference between a virus and a worm?", options: ["Viruses only affect documents", "Worms are less dangerous", "A virus requires a host file to propagate; a worm self-propagates independently across networks", "They're identical"], correctAnswer: 2, explanation: "Viruses attach to and modify host files to spread. Worms are standalone programs that self-replicate across networks without needing a host file." },
{ id: "ma-q7-2", question: "Why is FlareVM preferred over a standard Windows VM for malware analysis?", options: ["Pre-configured with analysis tools (debuggers, disassemblers, PE tools) and security settings optimized for safe analysis", "Official Microsoft product", "It's free", "Better performance"], correctAnswer: 0, explanation: "FlareVM comes pre-installed with tools like x64dbg, Ghidra, PEStudio, YARA, and is configured with analysis-friendly settings and disabled security features." },
{ id: "ma-q7-3", question: "What is the FIRST step when you receive a malware sample for analysis?", options: ["Execute it immediately", "Disassemble it", "Delete it", "Hash the sample (MD5, SHA-256) and check against threat intel databases like VirusTotal"], correctAnswer: 3, explanation: "Always hash first — if the sample is known, existing analysis saves time. Check VirusTotal, MalwareBazaar, and internal threat intel before spending analysis effort." },
{ id: "ma-q7-4", question: "What does the 'strings' command reveal during static analysis?", options: ["File structure", "Human-readable text embedded in the binary: URLs, IPs, registry keys, error messages, and API names", "Encryption keys", "File metadata only"], correctAnswer: 1, explanation: "Strings extraction reveals embedded text indicators: C2 URLs, file paths, registry keys, API names, error strings, and sometimes hardcoded credentials." },
{ id: "ma-q7-5", question: "What is a PE file's Import Address Table (IAT) and why is it important for analysis?", options: ["A memory allocation table", "A debugging feature", "Lists external DLL functions the binary calls — reveals capabilities like file I/O, networking, and crypto usage", "A compression table"], correctAnswer: 2, explanation: "The IAT shows which API functions the binary imports — CreateFile, InternetOpenUrl, CryptEncrypt reveal file access, network, and encryption capabilities." },
{ id: "ma-q7-6", question: "What is 'packing' in the context of malware?", options: ["Compressing and/or encrypting the binary to hide its true code and evade static analysis", "Bundling multiple files", "File compression for email", "Adding metadata"], correctAnswer: 0, explanation: "Packers compress/encrypt the executable code. At runtime, a stub unpacks the original code into memory — this defeats static string and import analysis." },
{ id: "ma-q7-7", question: "How do you identify if a PE file is packed?", options: ["Run it and observe", "Check file size only", "Check the filename", "High entropy in sections, few imports, small IAT, UPX/custom packer signatures, and section name anomalies"], correctAnswer: 3, explanation: "Packed indicators: high section entropy (>7.0), very few imports (just LoadLibrary/GetProcAddress), unusual section names (.upx, .packed), and small code sections." },
{ id: "ma-q7-8", question: "During dynamic analysis, what does ProcMon capture?", options: ["DNS queries only", "Network traffic", "Real-time file system, registry, process, and thread activity with full stack traces", "Memory dumps"], correctAnswer: 2, explanation: "Process Monitor captures granular system activity: file creates/reads/writes, registry modifications, process/thread creation, and network connections with stack traces." },
{ id: "ma-q7-9", question: "What is API hooking in dynamic analysis?", options: ["Calling APIs directly", "Intercepting API calls to monitor what functions malware invokes and with what parameters", "A programming technique", "Disabling APIs"], correctAnswer: 1, explanation: "API hooking intercepts function calls (CreateFile, WriteProcessMemory, InternetConnect) to log parameters and behavior without modifying the malware." },
{ id: "ma-q7-10", question: "A malware sample checks for 'vmtoolsd.exe' and 'VBoxService.exe' processes. What is it doing?", options: ["VM detection — anti-analysis technique to detect virtual machine environments and alter behavior", "Looking for dependencies", "Process injection", "Checking for updates"], correctAnswer: 0, explanation: "Checking for VM-specific processes is a common anti-analysis technique. If detected, malware may exit, sleep, or behave benignly to evade sandbox analysis." },
{ id: "ma-q7-11", question: "What is the purpose of a sandbox in malware analysis?", options: ["Store malware samples", "Network isolation only", "A coding environment", "Automated dynamic execution environment that monitors behavior and generates analysis reports"], correctAnswer: 3, explanation: "Sandboxes (Cuckoo, ANY.RUN, Joe Sandbox) automatically execute malware in isolated environments, monitoring all activity and generating behavioral reports." },
{ id: "ma-q7-12", question: "How do VBA macros typically deliver malware payloads?", options: ["Through email headers", "Direct execution", "Auto_Open/Document_Open macros use PowerShell, WScript, or certutil to download and execute payloads from remote servers", "Via DNS"], correctAnswer: 2, explanation: "Malicious macros trigger on document open, then use shell commands (PowerShell, WScript) to download second-stage payloads from attacker-controlled servers." },
{ id: "ma-q7-13", question: "What is 'code injection' and name two common techniques?", options: ["Inserting code into another process's memory space — DLL injection and process hollowing are common methods", "HTML injection", "SQL injection", "Writing code in an IDE"], correctAnswer: 0, explanation: "Code injection inserts malicious code into legitimate processes. DLL injection loads a malicious DLL; process hollowing replaces a suspended process's code." },
{ id: "ma-q7-14", question: "In x86 assembly, what does 'CALL' instruction do?", options: ["Compares values", "Exits the program", "Allocates memory", "Pushes the return address onto the stack and transfers execution to the target function"], correctAnswer: 3, explanation: "CALL pushes EIP (next instruction address) onto the stack as return address, then jumps to the target function. RET pops the address to return." },
{ id: "ma-q7-15", question: "What is Ghidra's decompiler useful for?", options: ["Compiling code", "Converting assembly instructions back to approximate C/C++ source code for easier analysis", "Network analysis", "Debugging"], correctAnswer: 1, explanation: "Ghidra's decompiler translates disassembly into pseudo-C code, making it much easier to understand program logic without reading raw assembly." },
{ id: "ma-q7-16", question: "What is the purpose of setting breakpoints in a debugger during malware analysis?", options: ["Add code to the binary", "Monitor network traffic", "Pause execution at specific addresses to inspect memory, registers, and variable values at that point", "Stop the malware permanently"], correctAnswer: 2, explanation: "Breakpoints pause execution so you can examine the current state — register values, memory contents, stack — crucial for understanding malware behavior." },
{ id: "ma-q7-17", question: "How does ransomware typically encrypt files?", options: ["Hybrid encryption: symmetric key (AES) encrypts files, asymmetric key (RSA) encrypts the symmetric key", "Simple XOR only", "Base64 encoding", "ROT13 cipher"], correctAnswer: 0, explanation: "Ransomware uses hybrid encryption for speed: AES encrypts each file quickly, then RSA encrypts the AES key — only the attacker's RSA private key can decrypt." },
{ id: "ma-q7-18", question: "What is a YARA rule's 'meta' section used for?", options: ["List file paths", "Define matching logic", "Configure scanning options", "Store descriptive information: author, date, description, threat level, and reference URLs"], correctAnswer: 3, explanation: "The meta section stores rule metadata for documentation — author, creation date, malware family, description, references, and severity classification." },
{ id: "ma-q7-19", question: "What is 'process hollowing'?", options: ["Process termination", "Creating a suspended legitimate process, unmapping its code, and injecting malicious code in its place", "Memory leak", "Deleting a process"], correctAnswer: 1, explanation: "Process hollowing creates a suspended legitimate process (e.g., svchost.exe), hollows out its code section, writes malicious code, and resumes — masquerading as legitimate." },
{ id: "ma-q7-20", question: "How do you safely extract IOCs from a malware sample?", options: ["Use VirusTotal only", "Run it on production", "Use static analysis tools in an isolated environment to extract strings, hashes, embedded URLs, and C2 infrastructure", "Ask the attacker"], correctAnswer: 2, explanation: "In an isolated analysis VM: extract strings, decode encoded data, parse PE resources, and collect hashes, IPs, domains, URLs, mutexes, and registry keys." },
{ id: "ma-q7-21", question: "What is the significance of the PE file's timestamp?", options: ["Compilation timestamp — can indicate when the malware was built, though it's easily forged", "When it was downloaded", "File creation time", "When it was first seen"], correctAnswer: 0, explanation: "The PE timestamp shows compilation time, helping estimate creation date and correlate with campaigns. However, sophisticated actors routinely forge this value." },
{ id: "ma-q7-22", question: "What technique do malware authors use to make reverse engineering harder?", options: ["Open-source release", "Adding comments", "Good documentation", "Code obfuscation: dead code insertion, control flow flattening, string encryption, and anti-debugging tricks"], correctAnswer: 3, explanation: "Obfuscation techniques include junk code insertion, opaque predicates, string encryption, API hashing, and anti-debug checks to slow reverse engineering." },
{ id: "ma-q7-23", question: "What is a mutex in malware behavior and why do analysts care about it?", options: ["A file type", "A named synchronization object — malware creates unique mutexes to prevent multiple instances, serving as IOCs", "An encryption algorithm", "A network protocol"], correctAnswer: 1, explanation: "Malware creates named mutexes to ensure single execution. These unique names serve as reliable IOCs for detection and can identify malware families." },
{ id: "ma-q7-24", question: "How does a rootkit differ from a standard trojan?", options: ["They're identical", "Rootkits are less dangerous", "Rootkits operate at kernel level or below, actively hiding their presence from the OS and security tools", "Rootkits only affect Linux"], correctAnswer: 2, explanation: "Rootkits modify the OS kernel or boot process to actively conceal malware presence — hiding processes, files, network connections from standard tools." },
{ id: "ma-q7-25", question: "What is the MITRE ATT&CK technique ID for 'Command and Scripting Interpreter: PowerShell'?", options: ["T1059.001", "T1055.012", "T1547.001", "T1053.005"], correctAnswer: 0, explanation: "T1059.001 is the sub-technique for PowerShell under Command and Scripting Interpreter — one of the most commonly observed execution techniques." },
{ id: "ma-q7-26", question: "During analysis, you find the malware creates a service named 'WindowsUpdateSvc'. What technique is this?", options: ["Process injection", "Legitimate update", "Service discovery", "Persistence via Windows Service creation (T1543.003) using a name mimicking legitimate services"], correctAnswer: 3, explanation: "Creating services with names mimicking legitimate Windows services is a common persistence technique (T1543.003) — provides automatic startup and SYSTEM privileges." },
{ id: "ma-q7-27", question: "What is the best approach for analyzing a multi-stage malware dropper?", options: ["Only analyze the dropper", "Skip to the final payload", "Analyze each stage: initial dropper → downloaded payload → final payload, capturing IOCs and behavior at each stage", "Run it once and collect all data"], correctAnswer: 2, explanation: "Multi-stage malware requires analyzing each stage independently — each may have different C2s, techniques, and IOCs that are crucial for complete understanding." },
{ id: "ma-q7-28", question: "What does 'behavioral analysis' reveal that static analysis cannot?", options: ["Runtime behavior: actual C2 communication, decrypted strings, unpacked code, and real-time system modifications", "Import tables", "File size", "File metadata"], correctAnswer: 0, explanation: "Dynamic/behavioral analysis reveals what actually happens at runtime — decrypted configurations, real C2 traffic, dropped files, and evasion technique triggers." },
{ id: "ma-q7-29", question: "How should a malware analysis report be structured for maximum SOC value?", options: ["Technical details only", "Screenshots only", "Just list the IOCs", "Executive summary, IOCs (hashes, IPs, domains), behavioral indicators, MITRE ATT&CK mapping, and detection recommendations"], correctAnswer: 3, explanation: "Effective reports include: summary for leadership, actionable IOCs for blocking, behavioral indicators for detection, ATT&CK mapping for context, and recommendations." },
{ id: "ma-q7-30", question: "You analyze a sample that checks the system language and exits if it's Russian, Ukrainian, or Kazakh. What does this indicate?", options: ["Translation error", "Likely Eastern European cybercrime group avoiding prosecution by not targeting CIS countries", "Localization feature", "Random behavior"], correctAnswer: 1, explanation: "Many Eastern European cybercrime groups avoid targeting CIS nations to reduce law enforcement attention — language/locale checks are a common geofencing technique." }
          ]
  },
  // ==========================================
  // NETWORK FUNDAMENTALS QUIZZES
  // ==========================================
  {
    quizId: "nf-q1",
    courseId: "network-fundamentals",
    title: "Computer Networks Basics Quiz",
    description: "Test your knowledge of network types, topologies, and architecture.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "nf-q1-1", question: "What is the primary purpose of a computer network?", options: ["To protect against malware", "To enable communication and resource sharing between devices", "To increase CPU speed", "To store files locally"], correctAnswer: 1, explanation: "A computer network connects devices to enable communication, data sharing, and resource sharing such as printers and internet access." },
      { id: "nf-q1-2", question: "Which type of network typically covers a single building or campus?", options: ["LAN", "WAN", "PAN", "MAN"], correctAnswer: 0, explanation: "A LAN (Local Area Network) covers a limited area such as a building, office, or campus." },
      { id: "nf-q1-3", question: "What does WAN stand for?", options: ["Wireless Access Network", "Web Application Node", "Wired Automated Network", "Wide Area Network"], correctAnswer: 3, explanation: "WAN stands for Wide Area Network — it spans large geographical areas, connecting multiple LANs across cities, countries, or continents." },
      { id: "nf-q1-4", question: "In a star topology, what happens if the central device fails?", options: ["The network automatically switches to mesh", "Only one node is affected", "The entire network goes down", "Nothing — nodes communicate directly"], correctAnswer: 2, explanation: "In a star topology, all nodes connect through a central hub/switch. If it fails, the entire network loses connectivity." },
      { id: "nf-q1-5", question: "Which topology provides the highest redundancy?", options: ["Bus", "Full Mesh", "Star", "Ring"], correctAnswer: 1, explanation: "Full mesh topology connects every node to every other node, providing maximum redundancy — if one link fails, data can route through alternative paths." },
      { id: "nf-q1-6", question: "What is a PAN (Personal Area Network)?", options: ["A citywide network", "A private WAN", "A public access network", "A network within a few meters, like Bluetooth devices"], correctAnswer: 3, explanation: "A PAN operates within a very short range (typically a few meters) and connects personal devices like phones, headphones, and smartwatches via Bluetooth or USB." },
      { id: "nf-q1-7", question: "In a client-server architecture, what role does the server play?", options: ["It only sends data, never receives", "It only stores backups", "It acts as a simple relay", "It provides resources and services to client devices"], correctAnswer: 3, explanation: "In client-server architecture, the server centralizes resources (files, apps, databases) and provides services upon client requests." },
      { id: "nf-q1-8", question: "What is the main disadvantage of a bus topology?", options: ["It only supports two devices", "If the backbone cable fails, the entire network goes down", "High cost", "It requires too many cables"], correctAnswer: 1, explanation: "A bus topology uses a single backbone cable. If this cable fails or is damaged, all devices on the network lose connectivity." },
      { id: "nf-q1-9", question: "Which network type covers a metropolitan area, such as a city?", options: ["LAN", "MAN", "SAN", "PAN"], correctAnswer: 1, explanation: "A MAN (Metropolitan Area Network) covers a city or large campus, typically larger than a LAN but smaller than a WAN." },
      { id: "nf-q1-10", question: "What is the key advantage of peer-to-peer networking?", options: ["Better performance for large networks", "No need for a dedicated server — every device acts as both client and server", "Easier to scale to thousands of users", "Centralized security management"], correctAnswer: 1, explanation: "In P2P, each device can share and access resources directly without requiring a dedicated server, making it simpler and cheaper for small networks." },
      { id: "nf-q1-11", question: "Which device connects different networks together and routes traffic between them?", options: ["Repeater", "Router", "Hub", "Switch"], correctAnswer: 1, explanation: "A router connects different networks (e.g., your LAN to the internet) and routes packets between them using IP addresses." },
      { id: "nf-q1-12", question: "What is a CAN (Campus Area Network)?", options: ["A network spanning multiple buildings in a university or corporate campus", "A cloud-based network", "A cable television network", "A wireless network in a car"], correctAnswer: 0, explanation: "A CAN interconnects multiple LANs across buildings within a limited geographical area like a university campus or business park." },
      { id: "nf-q1-13", question: "In a ring topology, how does data travel?", options: ["In one direction (or both in dual-ring) from node to node", "Broadcast to all nodes simultaneously", "Only from the central hub", "Randomly to any node"], correctAnswer: 0, explanation: "In a ring topology, data travels sequentially from node to node in one direction (unidirectional) or both directions in a dual-ring configuration." },
      { id: "nf-q1-14", question: "What type of network is the Internet classified as?", options: ["LAN", "PAN", "WAN", "MAN"], correctAnswer: 2, explanation: "The Internet is the world's largest WAN — a global network of interconnected networks spanning the entire planet." },
      { id: "nf-q1-15", question: "What is a hybrid topology?", options: ["A network using only wireless connections", "A topology with no central device", "A combination of two or more different topologies", "A topology that only works in the cloud"], correctAnswer: 2, explanation: "A hybrid topology combines multiple topologies (e.g., star-bus or star-ring) to leverage the advantages of each for complex network designs." }
    ]
  },
  {
    quizId: "nf-q2",
    courseId: "network-fundamentals",
    title: "OSI Model Quiz",
    description: "Assess your understanding of the 7-layer OSI model and data encapsulation.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "nf-q2-1", question: "How many layers does the OSI model have?", options: ["7", "5", "6", "4"], correctAnswer: 0, explanation: "The OSI (Open Systems Interconnection) model has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application." },
      { id: "nf-q2-2", question: "Which OSI layer is responsible for routing packets between networks?", options: ["Layer 4 — Transport", "Layer 1 — Physical", "Layer 3 — Network", "Layer 2 — Data Link"], correctAnswer: 2, explanation: "Layer 3 (Network) handles logical addressing (IP) and routing packets between different networks." },
      { id: "nf-q2-3", question: "What is the PDU (Protocol Data Unit) at the Transport layer?", options: ["Bit", "Segment", "Frame", "Packet"], correctAnswer: 1, explanation: "At Layer 4 (Transport), data is encapsulated into segments (TCP) or datagrams (UDP)." },
      { id: "nf-q2-4", question: "Which layer converts data into electrical signals, light pulses, or radio waves?", options: ["Application", "Network", "Physical", "Data Link"], correctAnswer: 2, explanation: "Layer 1 (Physical) deals with the actual transmission of raw bits over a medium — electrical, optical, or wireless signals." },
      { id: "nf-q2-5", question: "At which OSI layer do switches primarily operate?", options: ["Layer 1", "Layer 4", "Layer 2", "Layer 3"], correctAnswer: 2, explanation: "Switches operate primarily at Layer 2 (Data Link), using MAC addresses to forward frames within a network." },
      { id: "nf-q2-6", question: "Which layer handles data encryption, compression, and format translation?", options: ["Session", "Transport", "Application", "Presentation"], correctAnswer: 3, explanation: "Layer 6 (Presentation) handles data formatting, encryption/decryption, compression, and character encoding translation." },
      { id: "nf-q2-7", question: "What is the purpose of the Session layer?", options: ["Routing packets", "Providing user interface", "Managing communication sessions between applications", "Physical transmission"], correctAnswer: 2, explanation: "Layer 5 (Session) establishes, manages, and terminates communication sessions between applications, handling dialog control and synchronization." },
      { id: "nf-q2-8", question: "What is data encapsulation in networking?", options: ["Compressing data for storage", "Splitting data into equal chunks", "Encrypting data for security", "Wrapping data with protocol headers at each layer as it moves down the OSI stack"], correctAnswer: 3, explanation: "Encapsulation adds protocol-specific headers (and sometimes trailers) at each OSI layer as data moves from Application to Physical." },
      { id: "nf-q2-9", question: "Which layer provides end-to-end communication and error recovery?", options: ["Transport", "Session", "Data Link", "Network"], correctAnswer: 0, explanation: "Layer 4 (Transport) provides end-to-end reliable communication with features like error detection, flow control, and retransmission (TCP)." },
      { id: "nf-q2-10", question: "The PDU at Layer 2 is called a:", options: ["Segment", "Packet", "Frame", "Bit"], correctAnswer: 2, explanation: "At the Data Link layer (Layer 2), data is encapsulated into frames, which include MAC addresses and error-checking (FCS)." },
      { id: "nf-q2-11", question: "HTTP, FTP, and SMTP operate at which OSI layer?", options: ["Application", "Presentation", "Session", "Transport"], correctAnswer: 0, explanation: "HTTP, FTP, SMTP, DNS, and other user-facing protocols operate at Layer 7 (Application)." },
      { id: "nf-q2-12", question: "What mnemonic helps remember the OSI layers from bottom to top?", options: ["All People Seem To Need Data Processing", "Do People Always Talk So Nice Politely", "Please Do Not Throw Sausage Pizza Away", "Never Say Anything To People During Parties"], correctAnswer: 2, explanation: "'Please Do Not Throw Sausage Pizza Away' represents Physical, Data Link, Network, Transport, Session, Presentation, Application." },
      { id: "nf-q2-13", question: "Which two layers are combined in the TCP/IP model's Network Access layer?", options: ["Network and Transport", "Application and Session", "Physical and Data Link", "Session and Presentation"], correctAnswer: 2, explanation: "The TCP/IP model combines OSI Layers 1 (Physical) and 2 (Data Link) into a single Network Access (or Link) layer." },
      { id: "nf-q2-14", question: "What does de-encapsulation refer to?", options: ["Removing headers at each layer as data moves up the stack at the receiving end", "Adding headers at each layer", "Compressing data packets", "Converting digital to analog"], correctAnswer: 0, explanation: "De-encapsulation is the reverse process — stripping away protocol headers/trailers at each layer as data moves up the OSI stack at the receiving host." },
      { id: "nf-q2-15", question: "Which OSI layer adds a trailer containing the FCS (Frame Check Sequence)?", options: ["Data Link", "Physical", "Network", "Transport"], correctAnswer: 0, explanation: "The Data Link layer (Layer 2) adds both a header (with MAC addresses) and a trailer containing the FCS for error detection." }
    ]
  },
  {
    quizId: "nf-q3",
    courseId: "network-fundamentals",
    title: "TCP/IP Protocol Suite Quiz",
    description: "Test your knowledge of TCP, UDP, ICMP, ARP, and port numbers.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "nf-q3-1", question: "How many layers does the TCP/IP model have?", options: ["7", "3", "4", "5"], correctAnswer: 2, explanation: "The TCP/IP model has 4 layers: Network Access, Internet, Transport, and Application." },
      { id: "nf-q3-2", question: "What is the first step of the TCP three-way handshake?", options: ["SYN-ACK", "ACK", "FIN", "SYN"], correctAnswer: 3, explanation: "The three-way handshake begins with the client sending a SYN (synchronize) packet to the server." },
      { id: "nf-q3-3", question: "Which protocol is connectionless and does not guarantee delivery?", options: ["TCP", "ICMP", "ARP", "UDP"], correctAnswer: 3, explanation: "UDP (User Datagram Protocol) is connectionless — it sends data without establishing a connection or guaranteeing delivery, providing lower latency." },
      { id: "nf-q3-4", question: "What port number does HTTP use by default?", options: ["443", "80", "21", "22"], correctAnswer: 1, explanation: "HTTP uses port 80 by default, while HTTPS uses port 443." },
      { id: "nf-q3-5", question: "What protocol does the `ping` command use?", options: ["TCP", "ICMP", "UDP", "ARP"], correctAnswer: 1, explanation: "Ping uses ICMP (Internet Control Message Protocol) Echo Request and Echo Reply messages to test connectivity." },
      { id: "nf-q3-6", question: "What does ARP resolve?", options: ["URLs to IP addresses", "IP addresses to MAC addresses", "Domain names to IP addresses", "Port numbers to services"], correctAnswer: 1, explanation: "ARP (Address Resolution Protocol) maps a known IP address to its corresponding MAC address on the local network." },
      { id: "nf-q3-7", question: "Which port range is designated as 'well-known' ports?", options: ["49152-65535", "0-1023", "1024-49151", "0-65535"], correctAnswer: 1, explanation: "Well-known ports range from 0-1023 and are assigned to commonly used protocols like HTTP (80), HTTPS (443), SSH (22), and DNS (53)." },
      { id: "nf-q3-8", question: "What happens during the second step of the TCP three-way handshake?", options: ["Client sends ACK", "Client sends FIN", "Server responds with SYN-ACK", "Connection is closed"], correctAnswer: 2, explanation: "In step 2, the server acknowledges the client's SYN and sends back a SYN-ACK (synchronize-acknowledge) packet." },
      { id: "nf-q3-9", question: "TCP provides flow control using which mechanism?", options: ["MAC filtering", "Sliding window", "DNS lookup", "ARP cache"], correctAnswer: 1, explanation: "TCP uses a sliding window mechanism to manage flow control — the receiver advertises a window size indicating how much data it can accept." },
      { id: "nf-q3-10", question: "Which protocol would you use for real-time video streaming?", options: ["ICMP", "ARP", "UDP", "TCP"], correctAnswer: 2, explanation: "UDP is preferred for real-time streaming (video, VoIP, gaming) because its lower overhead and lack of retransmission provide better performance." },
      { id: "nf-q3-11", question: "What is the default port for SSH?", options: ["23", "25", "20", "22"], correctAnswer: 3, explanation: "SSH (Secure Shell) uses port 22 by default for encrypted remote access." },
      { id: "nf-q3-12", question: "What is a socket in networking?", options: ["The combination of an IP address and a port number", "A physical connector", "A type of cable", "A network topology"], correctAnswer: 0, explanation: "A socket is the combination of an IP address and port number (e.g., 192.168.1.1:443), uniquely identifying a communication endpoint." },
      { id: "nf-q3-13", question: "What ICMP message type is used by traceroute?", options: ["Echo Request", "Redirect", "Destination Unreachable", "Time Exceeded"], correctAnswer: 3, explanation: "Traceroute works by sending packets with incrementing TTL values and receiving ICMP Time Exceeded messages from each hop along the path." },
      { id: "nf-q3-14", question: "Which TCP flag initiates connection termination?", options: ["FIN", "ACK", "RST", "SYN"], correctAnswer: 0, explanation: "The FIN (Finish) flag initiates a graceful connection termination in TCP's four-way teardown process." },
      { id: "nf-q3-15", question: "Ephemeral ports are in which range?", options: ["0-1023", "49152-65535", "80-443", "1024-49151"], correctAnswer: 1, explanation: "Ephemeral (dynamic/private) ports range from 49152-65535 and are temporarily assigned by the OS for client-side connections." }
    ]
  },
  {
    quizId: "nf-q4",
    courseId: "network-fundamentals",
    title: "IP Addressing & Subnetting Quiz",
    description: "Validate your subnetting skills and IPv4/IPv6 knowledge.",
    passingScore: 70,
    timeLimit: 25,
    questions: [
      { id: "nf-q4-1", question: "How many bits are in an IPv4 address?", options: ["64", "16", "32", "128"], correctAnswer: 2, explanation: "An IPv4 address is 32 bits long, divided into 4 octets of 8 bits each (e.g., 192.168.1.1)." },
      { id: "nf-q4-2", question: "What is the subnet mask for a /24 network?", options: ["255.255.255.128", "255.255.0.0", "255.255.255.252", "255.255.255.0"], correctAnswer: 3, explanation: "/24 means 24 bits are set to 1 in the mask, giving 255.255.255.0 — the most common subnet mask for small networks." },
      { id: "nf-q4-3", question: "Which IP address class has a default subnet mask of 255.0.0.0?", options: ["Class D", "Class A", "Class C", "Class B"], correctAnswer: 1, explanation: "Class A networks (1.0.0.0 – 126.255.255.255) use a default /8 subnet mask: 255.0.0.0." },
      { id: "nf-q4-4", question: "How many usable host addresses are in a /28 subnet?", options: ["32", "30", "16", "14"], correctAnswer: 3, explanation: "/28 provides 2^4 = 16 addresses, minus 2 (network and broadcast) = 14 usable host addresses." },
      { id: "nf-q4-5", question: "Which of the following is a private IP address range?", options: ["104.0.0.0/8", "8.8.8.0/24", "200.1.1.0/24", "172.16.0.0/12"], correctAnswer: 3, explanation: "172.16.0.0/12 (172.16.0.0 – 172.31.255.255) is one of three RFC 1918 private address ranges, along with 10.0.0.0/8 and 192.168.0.0/16." },
      { id: "nf-q4-6", question: "What does NAT stand for?", options: ["New Address Table", "Node Authentication Token", "Network Address Translation", "Network Access Terminal"], correctAnswer: 2, explanation: "NAT (Network Address Translation) translates private IP addresses to public IPs, allowing multiple devices to share a single public address." },
      { id: "nf-q4-7", question: "What is the broadcast address for the network 192.168.10.0/24?", options: ["192.168.10.255", "192.168.10.0", "192.168.10.1", "192.168.10.254"], correctAnswer: 0, explanation: "For a /24 network, the broadcast address is the last address in the range: 192.168.10.255." },
      { id: "nf-q4-8", question: "How many bits are in an IPv6 address?", options: ["32", "128", "64", "96"], correctAnswer: 1, explanation: "IPv6 addresses are 128 bits long, represented as 8 groups of 4 hexadecimal digits (e.g., 2001:0db8::1)." },
      { id: "nf-q4-9", question: "What is CIDR notation?", options: ["A way to express the subnet mask as a prefix length (e.g., /24)", "A cable standard", "A routing protocol", "A type of DNS record"], correctAnswer: 0, explanation: "CIDR (Classless Inter-Domain Routing) notation uses a slash followed by the number of network bits (e.g., 10.0.0.0/8) instead of writing full subnet masks." },
      { id: "nf-q4-10", question: "Which IP address is a loopback address?", options: ["127.0.0.1", "255.255.255.255", "0.0.0.0", "192.168.0.1"], correctAnswer: 0, explanation: "127.0.0.1 is the IPv4 loopback address — traffic sent here never leaves the host and is used for local testing." },
      { id: "nf-q4-11", question: "What does PAT (Port Address Translation) add to NAT?", options: ["DNS resolution", "Uses port numbers to map multiple internal hosts to a single public IP", "Encryption", "VLAN tagging"], correctAnswer: 1, explanation: "PAT extends NAT by using unique port numbers to distinguish traffic from multiple internal devices sharing one public IP address." },
      { id: "nf-q4-12", question: "Given the network 10.0.0.0/16, how many subnets can you create with a /24 mask?", options: ["512", "256", "64", "16"], correctAnswer: 1, explanation: "Borrowing 8 bits from the host portion (24 - 16 = 8) creates 2^8 = 256 subnets." },
      { id: "nf-q4-13", question: "Which IPv6 address type is equivalent to IPv4's private addressing?", options: ["Unique Local (ULA)", "Global Unicast", "Multicast", "Link-local"], correctAnswer: 0, explanation: "Unique Local Addresses (fc00::/7) are IPv6's equivalent of RFC 1918 private addresses — routable within an organization but not on the internet." },
      { id: "nf-q4-14", question: "What is the purpose of the network ID in an IP address?", options: ["Identifies the network or subnet the host belongs to", "Specifies the gateway", "Identifies the specific host", "Determines the port number"], correctAnswer: 0, explanation: "The network ID (determined by the subnet mask) identifies which network a host belongs to, enabling routers to make forwarding decisions." },
      { id: "nf-q4-15", question: "The address 169.254.x.x indicates what?", options: ["A multicast address", "A public IP address", "An IPv6 transition address", "An APIPA (Automatic Private IP Addressing) — DHCP failed to assign an address"], correctAnswer: 3, explanation: "169.254.0.0/16 is the APIPA range — Windows/macOS self-assign addresses here when a DHCP server is unreachable." }
    ]
  },
  {
    quizId: "nf-q5",
    courseId: "network-fundamentals",
    title: "Network Devices Quiz",
    description: "Test your understanding of switches, routers, firewalls, and VLANs.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "nf-q5-1", question: "What is the primary function of a network switch?", options: ["Forward frames based on MAC addresses within a LAN", "Route packets between networks", "Filter web traffic", "Assign IP addresses"], correctAnswer: 0, explanation: "A switch operates at Layer 2 and forwards Ethernet frames based on destination MAC addresses within a local network." },
      { id: "nf-q5-2", question: "How does a switch learn MAC addresses?", options: ["Through DNS queries", "By broadcasting ARP requests", "By examining the source MAC address of incoming frames", "Manual configuration only"], correctAnswer: 2, explanation: "Switches build their MAC address table dynamically by recording the source MAC address and ingress port of each received frame." },
      { id: "nf-q5-3", question: "What does a router use to make forwarding decisions?", options: ["DNS names", "Port numbers", "MAC addresses", "IP addresses and routing table"], correctAnswer: 3, explanation: "Routers operate at Layer 3 and use destination IP addresses combined with their routing table to determine where to forward packets." },
      { id: "nf-q5-4", question: "What is the difference between a hub and a switch?", options: ["A hub is faster", "A hub broadcasts to all ports; a switch forwards only to the correct port", "There is no difference", "A switch broadcasts; a hub is selective"], correctAnswer: 1, explanation: "A hub is a simple repeater that sends frames out all ports. A switch intelligently forwards frames only to the port where the destination device is connected." },
      { id: "nf-q5-5", question: "What is a VLAN?", options: ["A type of VPN", "A virus protection system", "A wireless network standard", "A virtual LAN that logically segments a physical network"], correctAnswer: 3, explanation: "A VLAN (Virtual LAN) logically divides a physical switch into separate broadcast domains, improving security and performance." },
      { id: "nf-q5-6", question: "What protocol is used for VLAN trunking between switches?", options: ["OSPF", "802.1Q", "STP", "ARP"], correctAnswer: 1, explanation: "IEEE 802.1Q adds a VLAN tag to Ethernet frames, allowing trunk links to carry traffic for multiple VLANs between switches." },
      { id: "nf-q5-7", question: "What is a stateful firewall?", options: ["A firewall that tracks the state of active connections and makes decisions based on context", "A firewall that only checks headers", "A firewall that blocks all traffic", "A software-only firewall"], correctAnswer: 0, explanation: "Stateful firewalls maintain a connection state table, tracking ongoing sessions and allowing return traffic for established connections." },
      { id: "nf-q5-8", question: "What is the purpose of a load balancer?", options: ["To block malicious traffic", "To encrypt data", "To translate IP addresses", "To distribute incoming traffic across multiple servers for performance and availability"], correctAnswer: 3, explanation: "Load balancers distribute client requests across multiple backend servers to optimize performance, ensure availability, and prevent overload." },
      { id: "nf-q5-9", question: "What is a reverse proxy?", options: ["A proxy that reverses encryption", "A client-side proxy", "A protocol analyzer", "A server that sits in front of backend servers and forwards client requests to them"], correctAnswer: 3, explanation: "A reverse proxy accepts client requests and forwards them to appropriate backend servers — providing load balancing, caching, and security." },
      { id: "nf-q5-10", question: "Which routing type requires manual configuration of routes?", options: ["Default routing", "Static routing", "Policy routing", "Dynamic routing"], correctAnswer: 1, explanation: "Static routing requires an administrator to manually configure each route in the routing table — suitable for small, stable networks." },
      { id: "nf-q5-11", question: "What is the default gateway?", options: ["The router interface that forwards traffic destined for other networks", "The DNS server address", "The broadcast address", "The DHCP server"], correctAnswer: 0, explanation: "The default gateway is typically a router's IP address on the local subnet — it forwards packets when the destination is outside the local network." },
      { id: "nf-q5-12", question: "Why is network segmentation important for security?", options: ["It makes the network faster", "It reduces cable costs", "It eliminates the need for firewalls", "It limits the blast radius of breaches by isolating network zones"], correctAnswer: 3, explanation: "Segmentation isolates network zones so a breach in one segment doesn't spread to others — containing lateral movement and reducing risk." },
      { id: "nf-q5-13", question: "What is a Layer 3 switch?", options: ["A firewall appliance", "A wireless access point", "A switch that can also perform routing functions using IP addresses", "A hub with extra ports"], correctAnswer: 2, explanation: "A Layer 3 switch combines traditional Layer 2 switching with Layer 3 routing capabilities, enabling inter-VLAN routing at wire speed." },
      { id: "nf-q5-14", question: "What does a WLAN controller manage?", options: ["Multiple wireless access points centrally", "Email servers", "Wired switches", "Database servers"], correctAnswer: 0, explanation: "A WLAN controller centrally manages and configures multiple wireless access points — handling roaming, security policies, and channel assignments." },
      { id: "nf-q5-15", question: "What is an access port vs a trunk port on a switch?", options: ["They are identical", "Access ports connect to routers only", "An access port carries one VLAN; a trunk port carries multiple VLANs with 802.1Q tagging", "Trunk ports are faster"], correctAnswer: 2, explanation: "Access ports are assigned to a single VLAN (for end devices), while trunk ports carry tagged traffic from multiple VLANs between switches." }
    ]
  },
  {
    quizId: "nf-q6",
    courseId: "network-fundamentals",
    title: "Application Protocols Quiz",
    description: "Assess your knowledge of DNS, DHCP, HTTP, email, and file transfer protocols.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "nf-q6-1", question: "What does DNS resolve?", options: ["IP addresses to MAC addresses", "Domain names to IP addresses", "MAC addresses to IP addresses", "Port numbers to services"], correctAnswer: 1, explanation: "DNS (Domain Name System) translates human-readable domain names (e.g., google.com) into IP addresses (e.g., 142.250.190.46)." },
      { id: "nf-q6-2", question: "What is the DORA process in DHCP?", options: ["A backup method", "Discover, Offer, Request, Acknowledge — the four steps of DHCP IP assignment", "A routing algorithm", "A DNS query process"], correctAnswer: 1, explanation: "DORA: Client broadcasts Discover → Server sends Offer → Client sends Request → Server sends Acknowledge, completing IP address assignment." },
      { id: "nf-q6-3", question: "Which DNS record type maps a domain to an IPv4 address?", options: ["CNAME", "AAAA", "A", "MX"], correctAnswer: 2, explanation: "An A record (Address record) maps a domain name to an IPv4 address (e.g., example.com → 93.184.216.34)." },
      { id: "nf-q6-4", question: "What port does DNS use by default?", options: ["80", "25", "22", "53"], correctAnswer: 3, explanation: "DNS uses port 53 — UDP for standard queries and TCP for zone transfers and large responses." },
      { id: "nf-q6-5", question: "What does HTTPS add to HTTP?", options: ["Multi-language support", "Better compression", "TLS/SSL encryption for secure communication", "Faster loading"], correctAnswer: 2, explanation: "HTTPS wraps HTTP in TLS/SSL encryption, ensuring data confidentiality, integrity, and server authentication." },
      { id: "nf-q6-6", question: "Which HTTP status code indicates 'Not Found'?", options: ["403", "301", "200", "404"], correctAnswer: 3, explanation: "HTTP 404 means the requested resource was not found on the server." },
      { id: "nf-q6-7", question: "What protocol is used for sending email?", options: ["IMAP", "POP3", "SMTP", "FTP"], correctAnswer: 2, explanation: "SMTP (Simple Mail Transfer Protocol) is used for sending/relaying email between mail servers, using port 25 (or 587 for submission)." },
      { id: "nf-q6-8", question: "What is the difference between POP3 and IMAP?", options: ["IMAP is faster", "POP3 is more secure", "POP3 downloads and typically deletes mail from server; IMAP syncs and keeps mail on server", "They are identical"], correctAnswer: 2, explanation: "POP3 downloads email locally (often deleting from server), while IMAP keeps messages on the server and syncs across multiple devices." },
      { id: "nf-q6-9", question: "What DNS record type specifies the mail server for a domain?", options: ["A", "MX", "TXT", "CNAME"], correctAnswer: 1, explanation: "MX (Mail Exchanger) records specify which mail servers are responsible for receiving email for a domain, with priority values." },
      { id: "nf-q6-10", question: "FTP uses which two ports?", options: ["25 and 110", "20 and 21", "22 and 23", "80 and 443"], correctAnswer: 1, explanation: "FTP uses port 21 for control/command and port 20 for data transfer in active mode." },
      { id: "nf-q6-11", question: "What is a DHCP lease?", options: ["A VLAN configuration", "A permanent IP assignment", "A DNS record type", "A temporary IP address assignment with an expiration time"], correctAnswer: 3, explanation: "A DHCP lease is a temporary IP address assignment — the client must renew it before expiration or release it when no longer needed." },
      { id: "nf-q6-12", question: "What is a DNS CNAME record?", options: ["A text verification record", "An alias that points one domain name to another domain name", "An IP address mapping", "A mail server record"], correctAnswer: 1, explanation: "A CNAME (Canonical Name) record creates an alias — e.g., www.example.com → example.com — pointing one domain to another." },
      { id: "nf-q6-13", question: "Which protocol replaced Telnet for secure remote access?", options: ["SMTP", "SSH", "FTP", "HTTP"], correctAnswer: 1, explanation: "SSH (Secure Shell) replaced Telnet by providing encrypted remote access — Telnet transmits everything (including passwords) in plaintext." },
      { id: "nf-q6-14", question: "What is a DHCP relay agent used for?", options: ["Email routing", "Forwarding DHCP broadcasts across different subnets to a central DHCP server", "Firewall filtering", "DNS resolution"], correctAnswer: 1, explanation: "A DHCP relay agent forwards DHCP broadcast messages across subnet boundaries to a centralized DHCP server on another network." },
      { id: "nf-q6-15", question: "What does the AAAA DNS record type do?", options: ["Creates a mail exchange record", "Defines a text record", "Maps a domain to an IPv4 address", "Maps a domain to an IPv6 address"], correctAnswer: 3, explanation: "An AAAA (quad-A) record maps a domain name to an IPv6 address (e.g., example.com → 2606:2800:220:1:248:1893:25c8:1946)." }
    ]
  },
  {
    quizId: "nf-q7",
    courseId: "network-fundamentals",
    title: "Ethernet & Data Link Quiz",
    description: "Test Ethernet standards, MAC addressing, switching, and ARP concepts.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "nf-q7-1", question: "How many bits are in a MAC address?", options: ["48", "32", "64", "128"], correctAnswer: 0, explanation: "A MAC address is 48 bits (6 bytes), typically written as six pairs of hexadecimal digits (e.g., AA:BB:CC:DD:EE:FF)." },
      { id: "nf-q7-2", question: "What does the OUI in a MAC address identify?", options: ["The VLAN number", "The manufacturer/vendor of the network interface", "The IP subnet", "The operating system"], correctAnswer: 1, explanation: "The first 3 bytes (24 bits) of a MAC address form the OUI (Organizationally Unique Identifier), identifying the hardware manufacturer." },
      { id: "nf-q7-3", question: "Which Ethernet standard supports speeds up to 1 Gbps over Cat5e cabling?", options: ["100BASE-TX", "1000BASE-T", "10BASE-T", "10GBASE-T"], correctAnswer: 1, explanation: "1000BASE-T (Gigabit Ethernet) supports 1 Gbps over Cat5e or Cat6 copper cabling up to 100 meters." },
      { id: "nf-q7-4", question: "What is the purpose of the FCS (Frame Check Sequence) in an Ethernet frame?", options: ["VLAN identification", "Encryption", "Error detection using CRC", "Routing"], correctAnswer: 2, explanation: "The FCS uses a CRC (Cyclic Redundancy Check) calculation to detect errors in the received frame — if the CRC doesn't match, the frame is discarded." },
      { id: "nf-q7-5", question: "What is STP (Spanning Tree Protocol) used for?", options: ["Wireless authentication", "DNS resolution", "IP routing", "Preventing switching loops in redundant network topologies"], correctAnswer: 3, explanation: "STP prevents broadcast storms and loops by logically blocking redundant paths in switched networks while maintaining backup paths for failover." },
      { id: "nf-q7-6", question: "What is the broadcast MAC address?", options: ["AA:AA:AA:AA:AA:AA", "00:00:00:00:00:00", "FF:FF:FF:FF:FF:FF", "01:00:00:00:00:00"], correctAnswer: 2, explanation: "FF:FF:FF:FF:FF:FF is the Layer 2 broadcast address — frames sent to this address are delivered to all devices on the LAN." },
      { id: "nf-q7-7", question: "What happens when a switch receives a frame for an unknown MAC address?", options: ["Encrypts it", "Sends it to the router", "Drops it", "Floods it out all ports except the source port"], correctAnswer: 3, explanation: "When a switch doesn't have the destination MAC in its table, it floods the frame out all ports except the one it was received on — this is called unknown unicast flooding." },
      { id: "nf-q7-8", question: "What is ARP spoofing?", options: ["A method of DNS resolution", "A legitimate ARP process", "A type of encryption", "An attack where a malicious device sends fake ARP replies to associate its MAC with another device's IP"], correctAnswer: 3, explanation: "ARP spoofing (or poisoning) sends forged ARP replies to map the attacker's MAC to a victim's IP, enabling man-in-the-middle attacks." },
      { id: "nf-q7-9", question: "What type of cable connects two similar devices directly?", options: ["Crossover", "Straight-through", "Rollover/Console", "Fiber optic"], correctAnswer: 0, explanation: "A crossover cable swaps TX/RX pairs to connect similar devices (switch-to-switch, PC-to-PC) directly — though modern devices with Auto-MDIX handle this automatically." },
      { id: "nf-q7-10", question: "What is MAC flooding?", options: ["A legitimate switch operation", "A network monitoring technique", "A VLAN configuration method", "An attack that overwhelms a switch's MAC table, causing it to act like a hub"], correctAnswer: 3, explanation: "MAC flooding sends thousands of fake MAC addresses to fill the switch's CAM table, forcing it to flood all traffic — enabling sniffing of network data." },
      { id: "nf-q7-11", question: "Which cable type supports the longest distance runs?", options: ["Coaxial", "Cat6", "Fiber optic", "Cat5e"], correctAnswer: 2, explanation: "Fiber optic cables support much longer distances (up to 80+ km for single-mode) compared to copper (max 100m), with no electromagnetic interference." },
      { id: "nf-q7-12", question: "What is the maximum cable length for Cat6 Ethernet?", options: ["100 meters", "1000 meters", "200 meters", "50 meters"], correctAnswer: 0, explanation: "Cat6 copper Ethernet cables have a maximum segment length of 100 meters (328 feet) for reliable data transmission." },
      { id: "nf-q7-13", question: "What is the difference between single-mode and multi-mode fiber?", options: ["Multi-mode is always faster", "They carry the same signals", "Single-mode is cheaper", "Single-mode uses a smaller core for longer distances; multi-mode uses a larger core for shorter distances"], correctAnswer: 3, explanation: "Single-mode fiber has a small core (~9μm), allowing one light path for long distances. Multi-mode has a larger core (~50-62.5μm) for shorter distances." },
      { id: "nf-q7-14", question: "What switching method examines the entire frame before forwarding?", options: ["Cut-through", "Adaptive", "Store-and-forward", "Fragment-free"], correctAnswer: 2, explanation: "Store-and-forward switching receives the entire frame, checks the FCS for errors, then forwards it — providing the highest error checking at slightly higher latency." },
      { id: "nf-q7-15", question: "What is port security on a switch?", options: ["A firewall feature", "A routing protocol", "A DNS security feature", "A feature that limits the number of MAC addresses allowed on a port, preventing unauthorized access"], correctAnswer: 3, explanation: "Port security restricts the number of valid MAC addresses on a switch port, helping prevent MAC flooding attacks and unauthorized device connections." }
    ]
  },
  {
    quizId: "nf-q8",
    courseId: "network-fundamentals",
    title: "Wireless Networking Quiz",
    description: "Validate wireless standards, security protocols, and threat knowledge.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "nf-q8-1", question: "Which wireless standard is known as Wi-Fi 6?", options: ["802.11ac", "802.11n", "802.11g", "802.11ax"], correctAnswer: 3, explanation: "802.11ax is Wi-Fi 6 — it provides improved performance in dense environments with features like OFDMA, MU-MIMO, and target wake time." },
      { id: "nf-q8-2", question: "What are the two common Wi-Fi frequency bands?", options: ["900 MHz and 1800 MHz", "3.5 GHz and 7 GHz", "1 GHz and 3 GHz", "2.4 GHz and 5 GHz"], correctAnswer: 3, explanation: "Wi-Fi primarily uses 2.4 GHz (longer range, more interference) and 5 GHz (shorter range, faster speeds, less interference)." },
      { id: "nf-q8-3", question: "Which wireless security protocol should NOT be used due to known vulnerabilities?", options: ["WEP", "WPA2-Enterprise", "WPA3", "WPA2-PSK with AES"], correctAnswer: 0, explanation: "WEP (Wired Equivalent Privacy) has critical vulnerabilities — its RC4 encryption can be cracked in minutes. Always use WPA2 or WPA3." },
      { id: "nf-q8-4", question: "What is the main improvement of WPA3 over WPA2?", options: ["More channels", "Better range", "Faster speeds", "SAE (Simultaneous Authentication of Equals) replacing PSK, providing forward secrecy"], correctAnswer: 3, explanation: "WPA3 introduces SAE (dragonfly handshake) replacing the PSK 4-way handshake, providing forward secrecy and resistance to offline dictionary attacks." },
      { id: "nf-q8-5", question: "What is an evil twin attack?", options: ["A firmware update attack", "A rogue access point mimicking a legitimate network's SSID to capture user traffic", "A dual-band router setup", "A VLAN misconfiguration"], correctAnswer: 1, explanation: "An evil twin is a malicious AP with the same SSID as a legitimate network — victims connect to it unknowingly, allowing the attacker to intercept all traffic." },
      { id: "nf-q8-6", question: "What does 802.1X provide in wireless networking?", options: ["Better encryption", "Longer range", "Port-based network access control with RADIUS authentication", "Faster speeds"], correctAnswer: 2, explanation: "802.1X provides enterprise authentication — requiring users to authenticate through a RADIUS server before gaining network access." },
      { id: "nf-q8-7", question: "What is SSID?", options: ["A security protocol", "The name that identifies a wireless network", "A type of encryption", "A frequency band"], correctAnswer: 1, explanation: "SSID (Service Set Identifier) is the human-readable name of a wireless network that devices see when scanning for available networks." },
      { id: "nf-q8-8", question: "What is a deauthentication attack?", options: ["A firewall feature", "A legitimate logout process", "Sending forged deauth frames to disconnect clients from an AP, often as a precursor to other attacks", "An encryption standard"], correctAnswer: 2, explanation: "Deauth attacks send spoofed deauthentication frames to force clients off the network — often used before evil twin attacks or to capture WPA handshakes." },
      { id: "nf-q8-9", question: "What is the advantage of 5 GHz over 2.4 GHz?", options: ["Longer range", "Lower power consumption", "Better wall penetration", "More available channels and less interference, providing faster speeds"], correctAnswer: 3, explanation: "5 GHz offers more non-overlapping channels and less interference (fewer devices use it), enabling faster speeds — though with shorter range." },
      { id: "nf-q8-10", question: "What is a rogue access point?", options: ["A mesh network node", "A backup AP", "An unauthorized AP connected to the network, creating a security vulnerability", "A guest network AP"], correctAnswer: 2, explanation: "A rogue AP is an unauthorized access point connected to the corporate network — it bypasses security controls and can provide backdoor access." },
      { id: "nf-q8-11", question: "What encryption algorithm does WPA2 use?", options: ["RC4", "3DES", "DES", "AES-CCMP"], correctAnswer: 3, explanation: "WPA2 uses AES-CCMP (Advanced Encryption Standard with Counter Mode CBC-MAC Protocol) for robust encryption." },
      { id: "nf-q8-12", question: "What is MU-MIMO?", options: ["An antenna type", "A frequency band", "Multi-User Multiple-Input Multiple-Output — allows simultaneous communication with multiple devices", "A security protocol"], correctAnswer: 2, explanation: "MU-MIMO enables an AP to communicate with multiple devices simultaneously rather than sequentially, improving throughput in dense environments." },
      { id: "nf-q8-13", question: "What is war driving?", options: ["Driving around to discover and map wireless networks using scanning tools", "A routing protocol", "A type of DDoS attack", "A network speed test"], correctAnswer: 0, explanation: "War driving involves physically moving through an area with wireless scanning tools to discover, map, and potentially exploit wireless networks." },
      { id: "nf-q8-14", question: "What does WPA stand for?", options: ["Wireless Public Access", "Wireless Protocol Access", "Wi-Fi Protected Access", "Wired Protocol Authentication"], correctAnswer: 2, explanation: "WPA stands for Wi-Fi Protected Access — the security standard developed by the Wi-Fi Alliance to replace the insecure WEP protocol." },
      { id: "nf-q8-15", question: "What is the purpose of a wireless IDS/IPS?", options: ["Detecting and preventing wireless attacks like rogue APs, deauth attacks, and unauthorized clients", "SSID broadcast", "Channel management", "Speed optimization"], correctAnswer: 0, explanation: "Wireless IDS/IPS monitors the RF spectrum for malicious activity — detecting rogue APs, evil twins, deauth attacks, and policy violations." }
    ]
  },
  {
    quizId: "nf-q9",
    courseId: "network-fundamentals",
    title: "Network Troubleshooting Quiz",
    description: "Assess your ability to use network diagnostic tools and methodologies.",
    passingScore: 70,
    timeLimit: 20,
    questions: [
      { id: "nf-q9-1", question: "What is the first step in a structured troubleshooting methodology?", options: ["Implement a solution", "Identify the problem and gather information", "Document findings", "Test a theory"], correctAnswer: 1, explanation: "The first step is always identifying the problem — gathering symptoms, affected users, recent changes, and scope before forming theories." },
      { id: "nf-q9-2", question: "What does the `ping` command test?", options: ["Basic connectivity and round-trip time to a destination using ICMP", "Bandwidth speed", "Port availability", "DNS resolution only"], correctAnswer: 0, explanation: "Ping sends ICMP echo requests and measures reply times, testing basic IP connectivity, latency, and packet loss to a target host." },
      { id: "nf-q9-3", question: "What does `traceroute` (or `tracert` on Windows) show?", options: ["DNS records", "The path packets take through the network, showing each hop and latency", "Open ports on a host", "MAC addresses"], correctAnswer: 1, explanation: "Traceroute maps the network path by sending packets with incrementing TTL values, revealing each router hop and its response time." },
      { id: "nf-q9-4", question: "Which command displays active network connections and listening ports?", options: ["nslookup", "traceroute", "ping", "netstat / ss"], correctAnswer: 3, explanation: "Netstat (or ss on modern Linux) shows active TCP/UDP connections, listening ports, and associated process IDs." },
      { id: "nf-q9-5", question: "What tool is used for deep packet analysis and capture?", options: ["Wireshark", "ipconfig", "ping", "nslookup"], correctAnswer: 0, explanation: "Wireshark is a packet analyzer that captures and inspects network traffic in real-time, allowing detailed protocol analysis." },
      { id: "nf-q9-6", question: "If you can ping an IP address but not a hostname, what is likely the issue?", options: ["IP address conflict", "Firewall blocking ICMP", "Network cable problem", "DNS resolution failure"], correctAnswer: 3, explanation: "If IP connectivity works but name resolution fails, the issue is with DNS — check DNS server settings, DNS service availability, and records." },
      { id: "nf-q9-7", question: "What does `nslookup` do?", options: ["Shows routing table", "Queries DNS servers to resolve domain names or look up DNS records", "Tests connectivity", "Displays ARP cache"], correctAnswer: 1, explanation: "Nslookup queries DNS servers to resolve hostnames to IPs, look up specific record types (MX, CNAME), and troubleshoot DNS issues." },
      { id: "nf-q9-8", question: "What Wireshark display filter shows only HTTP traffic?", options: ["tcp.port == 80", "filter http", "ip.proto == http", "http"], correctAnswer: 3, explanation: "The display filter 'http' shows only HTTP protocol traffic. You can also use 'tcp.port == 80' but 'http' is more precise for parsed HTTP data." },
      { id: "nf-q9-9", question: "What does `arp -a` show?", options: ["The ARP cache — mappings of IP addresses to MAC addresses", "Routing table", "DNS cache", "Open ports"], correctAnswer: 0, explanation: "The `arp -a` command displays the ARP cache — showing known IP-to-MAC address mappings for devices on the local network." },
      { id: "nf-q9-10", question: "You notice high latency on hop 3 of a traceroute but normal latency on hop 4. What does this suggest?", options: ["Hop 3's router deprioritizes ICMP responses — this is likely normal", "Your DNS is failing", "Hop 3 has a problem", "The network is overloaded"], correctAnswer: 0, explanation: "Many routers deprioritize ICMP responses. If subsequent hops show normal latency, hop 3 is likely rate-limiting ICMP, not actually congested." },
      { id: "nf-q9-11", question: "What command shows the IP configuration on Windows?", options: ["ip addr", "ipconfig", "ifconfig", "netstat"], correctAnswer: 1, explanation: "On Windows, `ipconfig` (or `ipconfig /all` for detailed info) shows IP address, subnet mask, default gateway, and DNS settings." },
      { id: "nf-q9-12", question: "What is the purpose of `ipconfig /flushdns`?", options: ["Reset network adapter", "Release the IP address", "Display routing table", "Clear the local DNS resolver cache to force fresh DNS lookups"], correctAnswer: 3, explanation: "Flushing DNS clears cached DNS records — useful when a domain's IP has changed and your system is still using the old cached record." },
      { id: "nf-q9-13", question: "What does the `pathping` command combine?", options: ["Netstat and route", "The functionality of ping and traceroute, showing path and packet loss statistics", "ping and ARP", "DNS and DHCP queries"], correctAnswer: 1, explanation: "Pathping combines traceroute (path discovery) with extended ping statistics, showing packet loss and latency at each hop over time." },
      { id: "nf-q9-14", question: "If a user has a 169.254.x.x IP address, what should you check?", options: ["Proxy settings", "DNS settings", "DHCP server availability — the client failed to obtain an IP address", "Firewall rules"], correctAnswer: 2, explanation: "169.254.x.x (APIPA) means the DHCP client couldn't reach a DHCP server — check DHCP service, network connectivity, and DHCP scope availability." },
      { id: "nf-q9-15", question: "What is the bottom-up troubleshooting approach?", options: ["Start by rebooting everything", "Start with DNS", "Start at the physical layer and work up through the OSI model", "Start at the application layer"], correctAnswer: 2, explanation: "Bottom-up starts at Layer 1 (Physical) — check cables, link lights, then Layer 2 (MAC/switching), Layer 3 (IP), and so on up the stack." }
    ]
  },
  {
    quizId: "nf-q10",
    courseId: "network-fundamentals",
    title: "Network Fundamentals Certification Exam",
    description: "Comprehensive final exam covering all 10 modules. Pass with 80% to earn your certificate.",
    passingScore: 80,
    timeLimit: 60,
    questions: [
      { id: "nf-q10-1", question: "Which OSI layer is responsible for logical addressing and routing?", options: ["Layer 4 — Transport", "Layer 2 — Data Link", "Layer 5 — Session", "Layer 3 — Network"], correctAnswer: 3, explanation: "Layer 3 (Network) handles logical addressing (IP addresses) and routing packets between different networks." },
      { id: "nf-q10-2", question: "What is the three-way handshake sequence in TCP?", options: ["ACK, SYN, FIN", "SYN, SYN-ACK, ACK", "SYN, ACK, FIN", "FIN, ACK, RST"], correctAnswer: 1, explanation: "TCP connection establishment: Client sends SYN → Server responds SYN-ACK → Client sends ACK. Connection is now established." },
      { id: "nf-q10-3", question: "How many usable host addresses exist in a /26 subnet?", options: ["62", "126", "64", "30"], correctAnswer: 0, explanation: "/26 = 6 host bits = 2^6 = 64 addresses. Minus network and broadcast = 62 usable host addresses." },
      { id: "nf-q10-4", question: "What protocol resolves IP addresses to MAC addresses?", options: ["ARP", "DHCP", "DNS", "ICMP"], correctAnswer: 0, explanation: "ARP (Address Resolution Protocol) resolves a known IP address to its corresponding MAC address on the local network segment." },
      { id: "nf-q10-5", question: "A switch floods a frame when:", options: ["The destination MAC is unknown (not in the MAC address table)", "The VLAN is misconfigured", "The frame has errors", "The destination MAC is in its CAM table"], correctAnswer: 0, explanation: "When a switch receives a frame with a destination MAC not in its table, it floods the frame out all ports except the source — this is unknown unicast flooding." },
      { id: "nf-q10-6", question: "Which wireless security protocol provides SAE (Simultaneous Authentication of Equals)?", options: ["WPA", "WPA3", "WEP", "WPA2"], correctAnswer: 1, explanation: "WPA3 introduces SAE, which replaces PSK with a more secure dragonfly handshake, providing forward secrecy and resistance to offline attacks." },
      { id: "nf-q10-7", question: "What is the default port for HTTPS?", options: ["8443", "80", "8080", "443"], correctAnswer: 3, explanation: "HTTPS uses port 443 by default for encrypted web communication over TLS/SSL." },
      { id: "nf-q10-8", question: "In the DHCP DORA process, what does the 'O' stand for?", options: ["Open", "Obtain", "Offer", "Operate"], correctAnswer: 2, explanation: "DORA: Discover, Offer, Request, Acknowledge. The DHCP server sends an Offer containing an available IP address to the requesting client." },
      { id: "nf-q10-9", question: "What is the purpose of Spanning Tree Protocol (STP)?", options: ["DNS resolution", "VLAN creation", "Preventing Layer 2 loops in redundant switch topologies", "IP address assignment"], correctAnswer: 2, explanation: "STP prevents broadcast storms by logically disabling redundant switch paths while maintaining them as backup for failover." },
      { id: "nf-q10-10", question: "Which command would you use to view the routing table on a Linux system?", options: ["nslookup", "arp -a", "ip route / route -n", "ipconfig /all"], correctAnswer: 2, explanation: "On Linux, `ip route` (or the older `route -n`) displays the kernel routing table showing destination networks, gateways, and interfaces." },
      { id: "nf-q10-11", question: "What is the broadcast address for 172.16.50.0/23?", options: ["172.16.50.1", "172.16.52.0", "172.16.51.255", "172.16.50.255"], correctAnswer: 2, explanation: "/23 means the network spans 172.16.50.0 – 172.16.51.255. The broadcast address is the last address: 172.16.51.255." },
      { id: "nf-q10-12", question: "What makes UDP suitable for real-time applications like VoIP?", options: ["Built-in encryption", "Better security", "Guaranteed delivery", "No connection overhead and no retransmission delays, providing lower latency"], correctAnswer: 3, explanation: "UDP's connectionless nature means no handshake delay and no retransmission — slightly lost packets are preferable to delayed audio/video." },
      { id: "nf-q10-13", question: "Which DNS record type creates an alias for another domain name?", options: ["CNAME", "MX", "A", "AAAA"], correctAnswer: 0, explanation: "CNAME (Canonical Name) creates an alias that points one domain to another — e.g., www.example.com → example.com." },
      { id: "nf-q10-14", question: "What is 802.1Q used for?", options: ["VLAN tagging on trunk links between switches", "Port security", "Wireless authentication", "Spanning tree"], correctAnswer: 0, explanation: "IEEE 802.1Q inserts a 4-byte VLAN tag into Ethernet frames, allowing trunk links to carry traffic for multiple VLANs." },
      { id: "nf-q10-15", question: "What is the difference between static and dynamic routing?", options: ["They are identical", "Dynamic is less reliable", "Static requires manual configuration; dynamic uses protocols (OSPF, BGP) to automatically learn routes", "Static is always faster"], correctAnswer: 2, explanation: "Static routes are manually configured by admins. Dynamic routing uses protocols like OSPF and BGP to automatically discover and adapt routes." },
      { id: "nf-q10-16", question: "An evil twin attack targets which technology?", options: ["Wired Ethernet", "Wireless networks by creating a fake AP with the same SSID", "DNS servers", "DHCP servers"], correctAnswer: 1, explanation: "Evil twin attacks create a rogue AP mimicking a legitimate wireless network's SSID to trick users into connecting and intercepting their traffic." },
      { id: "nf-q10-17", question: "What does NAT (Network Address Translation) do?", options: ["Encrypts data", "Translates private IP addresses to public IP addresses for internet access", "Assigns DHCP leases", "Resolves DNS names"], correctAnswer: 1, explanation: "NAT translates private RFC 1918 addresses to public IPs, allowing multiple internal devices to share one or more public IP addresses." },
      { id: "nf-q10-18", question: "What is the maximum segment length for Cat6 Ethernet cable?", options: ["50 meters", "200 meters", "500 meters", "100 meters"], correctAnswer: 3, explanation: "All standard Ethernet copper cables (Cat5e, Cat6, Cat6a) have a maximum segment length of 100 meters (328 feet)." },
      { id: "nf-q10-19", question: "Which tool shows the path packets take through a network?", options: ["traceroute / tracert", "netstat", "ping", "nslookup"], correctAnswer: 0, explanation: "Traceroute (tracert on Windows) shows each hop along the path to a destination, revealing routers and their response times." },
      { id: "nf-q10-20", question: "What is a VLAN's primary security benefit?", options: ["Firewall replacement", "Network segmentation — isolating broadcast domains to limit attack scope", "Encryption", "Authentication"], correctAnswer: 1, explanation: "VLANs segment the network into isolated broadcast domains, limiting the scope of broadcasts and containing lateral movement during attacks." },
      { id: "nf-q10-21", question: "IPv6 addresses are how many bits long?", options: ["96", "128", "32", "64"], correctAnswer: 1, explanation: "IPv6 addresses are 128 bits, providing approximately 3.4 × 10^38 unique addresses — solving IPv4 address exhaustion." },
      { id: "nf-q10-22", question: "What is the purpose of a default gateway?", options: ["DNS resolution", "Forwards traffic to destinations outside the local subnet", "MAC learning", "DHCP assignment"], correctAnswer: 1, explanation: "The default gateway (typically a router) forwards packets when the destination IP is not on the local subnet — it's the exit point for the LAN." },
      { id: "nf-q10-23", question: "Which Wireshark feature lets you follow an entire TCP conversation?", options: ["Follow TCP Stream", "Display filter", "Capture filter", "Protocol hierarchy"], correctAnswer: 0, explanation: "Follow TCP Stream reconstructs and displays the complete data exchange of a TCP session, making it easy to read application-layer conversations." },
      { id: "nf-q10-24", question: "What is MAC flooding?", options: ["A firmware update", "An attack that overwhelms a switch's MAC table, causing it to broadcast all traffic like a hub", "A VLAN configuration method", "A legitimate switch feature"], correctAnswer: 1, explanation: "MAC flooding fills the switch's CAM table with fake entries, causing the switch to fail-open and flood all frames to all ports — enabling traffic sniffing." },
      { id: "nf-q10-25", question: "What is the difference between single-mode and multi-mode fiber?", options: ["Multi-mode is always faster", "Same technology, different colors", "Single-mode is only for LANs", "Single-mode: smaller core, longer distance, laser; Multi-mode: larger core, shorter distance, LED"], correctAnswer: 3, explanation: "Single-mode (~9μm core) uses laser for long distances (up to 80+ km). Multi-mode (~50-62.5μm) uses LED for shorter distances (up to ~2 km)." },
      { id: "nf-q10-26", question: "What port does SSH use by default?", options: ["23", "22", "20", "25"], correctAnswer: 1, explanation: "SSH uses port 22 for secure, encrypted remote access — replacing insecure Telnet (port 23)." },
      { id: "nf-q10-27", question: "What is CIDR notation /16 equivalent to in dotted decimal?", options: ["255.255.0.0", "255.255.255.128", "255.255.255.0", "255.0.0.0"], correctAnswer: 0, explanation: "/16 means 16 network bits are set to 1: 11111111.11111111.00000000.00000000 = 255.255.0.0." },
      { id: "nf-q10-28", question: "Which protocol provides encrypted remote file transfer?", options: ["TFTP", "Telnet", "FTP", "SFTP/SCP"], correctAnswer: 3, explanation: "SFTP (SSH File Transfer Protocol) and SCP (Secure Copy) provide encrypted file transfer over SSH, unlike FTP which sends data in cleartext." },
      { id: "nf-q10-29", question: "What is Zero Trust networking?", options: ["An outdated security model", "No security at all", "A wireless-only concept", "A model where no user or device is trusted by default — every access request must be verified"], correctAnswer: 3, explanation: "Zero Trust assumes no implicit trust — every user, device, and connection must be continuously verified regardless of location (internal or external)." },
      { id: "nf-q10-30", question: "A user can ping their default gateway but cannot access external websites. What should you check next?", options: ["Change the MAC address", "DNS resolution and upstream routing — the local network works but internet access or name resolution may be failing", "Replace the Ethernet cable", "Reinstall the OS"], correctAnswer: 1, explanation: "Since local connectivity works (gateway is reachable), check DNS settings (try pinging 8.8.8.8 by IP), upstream router connectivity, and ISP status." }
    ]
  }
];

export const getQuizById = (courseId: string, quizId: string): QuizData | undefined => {
  return quizzes.find(q => q.courseId === courseId && q.quizId === quizId);
};

export const getCourseQuizzes = (courseId: string): QuizData[] => {
  return quizzes.filter(q => q.courseId === courseId);
};
