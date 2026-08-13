import type { Course } from "@/data/types";

export const courses: Course[] = [
  {
    id: "soc-fundamentals",
    title: "Blue Team & SOC Fundamentals",
    shortTitle: "SOC Level 1",
    description: "Build your foundation as a Level 1 SOC analyst and step into the world of cybersecurity defense. This course covers the essential skills, tools, and workflows you need to detect and respond to threats effectively.",
    difficulty: "easy",
    duration: "12 hours",
    bgImage: "soc-course-bg.jpg",
    modules: [
      {
        id: "1",
        title: "Introduction to Security Operations",
        quizId: "q1",
        lessons: [
          { 
            id: "1.1", 
            title: "Welcome to the SOC", 
            description: "Understand what a Security Operations Center is, its mission, and how it fits into an organization's security posture.",
            duration: "15 min",
            status: "completed" 
          },
          { 
            id: "1.2", 
            title: "SOC Team Roles & Responsibilities", 
            description: "Learn about different SOC roles from L1 Analyst to SOC Manager and their daily responsibilities.",
            duration: "20 min",
            status: "unlocked" 
          },
          { 
            id: "1.3", 
            title: "SOC Tools & Technologies Overview", 
            description: "Introduction to SIEM, EDR, IDS/IPS, and other essential SOC tools.",
            duration: "25 min",
            status: "locked" 
          },
          { 
            id: "1.4", 
            title: "SOC Workflows & Shift Handover", 
            description: "Understanding ticketing systems, escalation procedures, and shift management.",
            duration: "20 min",
            status: "locked" 
          },
          { 
            id: "1.5", 
            title: "Module 1 Quiz: SOC Fundamentals", 
            description: "Assess your understanding of SOC basics, roles, tools, and workflows before moving on.",
            duration: "15 min",
            status: "locked" 
          },
        ],
      },
      {
        id: "2",
        title: "Cyber Threat Landscape",
        quizId: "q2",
        lessons: [
          { 
            id: "2.1", 
            title: "Understanding Threat Actors", 
            description: "Learn about different threat actors: nation-states, cybercriminals, hacktivists, and insiders.",
            duration: "25 min",
            status: "locked" 
          },
          { 
            id: "2.2", 
            title: "Common Attack Vectors", 
            description: "Explore phishing, malware delivery, exploitation, and social engineering techniques.",
            duration: "30 min",
            status: "locked" 
          },
          { 
            id: "2.3", 
            title: "Malware Categories & Behavior", 
            description: "Overview of viruses, worms, trojans, ransomware, rootkits, and their characteristics.",
            duration: "35 min",
            status: "locked" 
          },
          { 
            id: "2.4", 
            title: "Introduction to MITRE ATT&CK", 
            description: "Understanding the ATT&CK framework and how it maps adversary behavior.",
            duration: "30 min",
            status: "locked" 
          },
          { 
            id: "2.5", 
            title: "Module 2 Quiz: Cyber Threat Landscape", 
            description: "Test your knowledge of threat actors, attack vectors, malware types, and MITRE ATT&CK.",
            duration: "15 min",
            status: "locked" 
          },
        ],
      },
      {
        id: "3",
        title: "Log Analysis Fundamentals",
        quizId: "q3",
        lessons: [
          { 
            id: "3.1", 
            title: "Why Logs Matter in Security", 
            description: "The importance of logging for detection, investigation, and compliance.",
            duration: "15 min",
            status: "locked" 
          },
          { 
            id: "3.2", 
            title: "Windows Event Log Essentials", 
            description: "Key Windows Event IDs: 4624, 4625, 4688, 4720, 4732, and their significance.",
            duration: "40 min",
            status: "locked" 
          },
          { 
            id: "3.3", 
            title: "Linux Log Analysis Basics", 
            description: "Understanding auth.log, syslog, and secure logs for threat detection.",
            duration: "35 min",
            status: "locked" 
          },
          { 
            id: "3.4", 
            title: "Network Device Logs", 
            description: "Analyzing firewall, proxy, and DNS logs for suspicious activity.",
            duration: "30 min",
            status: "locked" 
          },
          { 
            id: "3.5", 
            title: "Hands-On: Log Analysis Challenge", 
            description: "Practice identifying malicious activity in sample log files.",
            duration: "45 min",
            status: "locked" 
          },
          { 
            id: "3.6", 
            title: "Module 3 Quiz: Log Analysis Fundamentals", 
            description: "Test your knowledge of Windows, Linux, and network log analysis concepts.",
            duration: "30 min",
            status: "locked" 
          },
        ],
      },
      {
        id: "4",
        title: "SIEM Fundamentals",
        quizId: "q4",
        lessons: [
          { 
            id: "4.1", 
            title: "What is a SIEM?", 
            description: "Understanding SIEM architecture, data flow, and core capabilities.",
            duration: "20 min",
            status: "locked" 
          },
          { 
            id: "4.2", 
            title: "SIEM Navigation & Interface", 
            description: "Learning to navigate dashboards, search interfaces, and alert queues.",
            duration: "25 min",
            status: "locked" 
          },
          { 
            id: "4.3", 
            title: "Basic Search Queries", 
            description: "Writing simple queries to find specific events and patterns.",
            duration: "35 min",
            status: "locked" 
          },
          { 
            id: "4.4", 
            title: "Correlation Rules & Alerts", 
            description: "How SIEM correlates events and generates security alerts.",
            duration: "30 min",
            status: "locked" 
          },
          { 
            id: "4.5", 
            title: "Hands-On: SIEM Investigation Lab", 
            description: "Practice investigating alerts using a SIEM platform.",
            duration: "50 min",
            status: "locked" 
          },
          {
            id: "4.6",
            title: "Module 4 Quiz: SIEM Fundamentals",
            description: "Test your SIEM knowledge including navigation, queries, correlation rules, and alerts.",
            duration: "25 min",
            status: "locked"
          },
        ],
      },
      {
        id: "5",
        title: "Alert Triage & Analysis",
        quizId: "q4",
        lessons: [
          { 
            id: "5.1", 
            title: "Understanding Security Alerts", 
            description: "Alert anatomy, severity levels, and initial assessment techniques.",
            duration: "25 min",
            status: "locked" 
          },
          { 
            id: "5.2", 
            title: "The Triage Process", 
            description: "Step-by-step methodology for efficient alert triage.",
            duration: "30 min",
            status: "locked" 
          },
          { 
            id: "5.3", 
            title: "True Positive vs False Positive", 
            description: "Techniques to distinguish real threats from noise.",
            duration: "35 min",
            status: "locked" 
          },
          { 
            id: "5.4", 
            title: "Enrichment & Context Gathering", 
            description: "Using threat intel, reputation services, and context to validate alerts.",
            duration: "30 min",
            status: "locked" 
          },
          { 
            id: "5.5", 
            title: "Documentation & Escalation", 
            description: "Proper alert documentation and when/how to escalate.",
            duration: "25 min",
            status: "locked" 
          },
          {
            id: "5.6",
            title: "Module 5 Quiz: Alert Triage & Analysis",
            description: "Test your understanding of alert triage, true/false positive analysis, and escalation procedures.",
            duration: "20 min",
            status: "locked"
          },
        ],
      },
      {
        id: "6",
        title: "Threat Intelligence Basics",
        quizId: "q5",
        lessons: [
          { 
            id: "6.1", 
            title: "Introduction to Threat Intelligence", 
            description: "What is threat intel and how SOC analysts use it.",
            duration: "20 min",
            status: "locked" 
          },
          { 
            id: "6.2", 
            title: "IOC Types & Usage", 
            description: "Understanding IPs, domains, hashes, URLs, and how to leverage them.",
            duration: "25 min",
            status: "locked" 
          },
          { 
            id: "6.3", 
            title: "OSINT for SOC Analysts", 
            description: "Free tools and techniques for threat research.",
            duration: "30 min",
            status: "locked" 
          },
          { 
            id: "6.4", 
            title: "Threat Intel Platforms", 
            description: "Overview of VirusTotal, AbuseIPDB, Shodan, and other resources.",
            duration: "25 min",
            status: "locked" 
          },
          { 
            id: "6.5", 
            title: "Hands-On: Threat Intelligence Challenge", 
            description: "Apply your threat intelligence knowledge in a practical scenario.",
            duration: "40 min",
            status: "locked" 
          },
          { 
            id: "6.6", 
            title: "Module 6 Quiz: Threat Intelligence", 
            description: "Test your understanding of threat intelligence concepts, IOCs, OSINT, and intel platforms.",
            duration: "15 min",
            status: "locked" 
          },
        ],
      },
      {
        id: "7",
        title: "Incident Response Introduction",
        quizId: "q6",
        lessons: [
          {
            id: "7.1",
            title: "Incident Response Lifecycle",
            description: "NIST framework: Preparation, Detection, Containment, Eradication, Recovery, Lessons Learned.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "7.2",
            title: "Incident Classification & Severity",
            description: "How to classify incidents and determine priority.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "7.3",
            title: "Initial Containment Actions",
            description: "First response actions for common incident types.",
            duration: "35 min",
            status: "locked"
          },
          {
            id: "7.4",
            title: "Incident Documentation",
            description: "Creating effective incident tickets and reports.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "7.5",
            title: "Hands-On: Phishing Incident Response",
            description: "Walk through a complete phishing incident from detection to resolution.",
            duration: "45 min",
            status: "locked"
          },
          {
            id: "7.6",
            title: "Module 7 Quiz: Incident Response",
            description: "Test your understanding of the incident response lifecycle, classification, containment, and documentation.",
            duration: "20 min",
            status: "locked"
          },
        ],
      },
      {
        id: "8",
        title: "Endpoint Detection & Response",
        quizId: "q7",
        lessons: [
          { 
            id: "8.1", 
            title: "What is EDR?", 
            description: "Understanding endpoint detection and response technology.",
            duration: "20 min",
            status: "locked" 
          },
          { 
            id: "8.2", 
            title: "EDR Alerts & Telemetry", 
            description: "Types of EDR alerts and endpoint telemetry data.",
            duration: "30 min",
            status: "locked" 
          },
          { 
            id: "8.3", 
            title: "Process Analysis Basics", 
            description: "Understanding process trees, parent-child relationships, and suspicious behavior.",
            duration: "35 min",
            status: "locked" 
          },
          { 
            id: "8.4", 
            title: "Hands-On: EDR Investigation", 
            description: "Practice investigating EDR alerts in a simulated environment.",
            duration: "45 min",
            status: "locked" 
          },
          { 
            id: "8.5", 
            title: "Module 8 Quiz: Endpoint Detection & Response", 
            description: "Assess your knowledge of EDR concepts, telemetry, and investigation workflows.",
            duration: "15 min",
            status: "locked" 
          },
        ],
      },
      {
        id: "9",
        title: "Network Security Monitoring",
        quizId: "q8",
        lessons: [
          { 
            id: "9.1", 
            title: "Network Security Fundamentals", 
            description: "OSI model, TCP/IP, and network security concepts for SOC analysts.",
            duration: "30 min",
            status: "locked" 
          },
          { 
            id: "9.2", 
            title: "IDS/IPS Basics", 
            description: "Understanding intrusion detection and prevention systems.",
            duration: "25 min",
            status: "locked" 
          },
          { 
            id: "9.3", 
            title: "Network Traffic Analysis", 
            description: "Basics of analyzing network flows and packet captures.",
            duration: "35 min",
            status: "locked" 
          },
          { 
            id: "9.4", 
            title: "Common Network Attacks", 
            description: "Recognizing port scans, C2 traffic, data exfiltration, and lateral movement.",
            duration: "30 min",
            status: "locked" 
          },
          { 
            id: "9.5", 
            title: "Module 9 Quiz: Network Security Monitoring", 
            description: "Evaluate your understanding of network monitoring fundamentals and common attack patterns.",
            duration: "15 min",
            status: "locked" 
          },
        ],
      },
      {
        id: "10",
        title: "SOC Analyst Best Practices",
        quizId: "q9",
        lessons: [
          { 
            id: "10.1", 
            title: "Building Investigation Skills", 
            description: "Developing critical thinking and analytical mindset.",
            duration: "20 min",
            status: "locked" 
          },
          { 
            id: "10.2", 
            title: "Avoiding Analyst Burnout", 
            description: "Mental health, work-life balance, and career sustainability.",
            duration: "15 min",
            status: "locked" 
          },
          { 
            id: "10.3", 
            title: "Continuous Learning Path", 
            description: "Certifications, communities, and resources for career growth.",
            duration: "20 min",
            status: "locked" 
          },
          { 
            id: "10.4",
            title: "Final Quiz: SOC Analyst Certification", 
            description: "Comprehensive final assessment covering all SOC Level 1 modules before certification.",
            duration: "60 min",
            status: "locked" 
          },
          
          { 
            id: "10.5", 
            title: "Course Summary & Next Steps", 
            description: "Review key concepts and prepare for advanced training.",
            duration: "15 min",
            status: "locked" 
          },
        ],
      },
    ],
    quizzes: [
      {
        id: "q1",
        title: "SOC Fundamentals Quiz",
        description: "Test your understanding of SOC operations, team roles, and basic workflows.",
        questionCount: 15,
        passingScore: 70,
        duration: "20 min",
        status: "unlocked",
      },
      {
        id: "q2",
        title: "Threat Landscape Assessment",
        description: "Evaluate your knowledge of threat actors, attack vectors, and MITRE ATT&CK.",
        questionCount: 20,
        passingScore: 75,
        duration: "25 min",
        status: "locked",
      },
      {
        id: "q3",
        title: "Log Analysis Challenge",
        description: "Practical quiz on Windows, Linux, and network log analysis.",
        questionCount: 15,
        passingScore: 70,
        duration: "30 min",
        status: "locked",
      },
      {
        id: "q4",
        title: "SIEM & Alert Triage Quiz",
        description: "Test your SIEM knowledge and alert triage methodology.",
        questionCount: 20,
        passingScore: 75,
        duration: "25 min",
        status: "locked",
      },
      {
        id: "q5",
        title: "Incident Response Basics",
        description: "Assess your understanding of the IR lifecycle and containment procedures.",
        questionCount: 15,
        passingScore: 70,
        duration: "20 min",
        status: "locked",
      },
      {
        id: "q6",
        title: "Final Certification Exam",
        description: "Comprehensive exam covering all course modules. Required for certification.",
        questionCount: 50,
        passingScore: 80,
        duration: "60 min",
        status: "locked",
      },
    ],
    resources: [
      {
        id: "r1",
        title: "SOC Analyst Cheat Sheet",
        description: "Quick reference guide for common SOC tasks, commands, and procedures.",
        type: "cheatsheet",
      },
      {
        id: "r2",
        title: "Windows Event ID Reference",
        description: "Comprehensive list of critical Windows Security Event IDs for threat detection.",
        type: "pdf",
      },
      {
        id: "r3",
        title: "Linux Log Analysis Guide",
        description: "Reference guide for analyzing Linux system and authentication logs.",
        type: "pdf",
      },
      {
        id: "r4",
        title: "Alert Triage Workflow Template",
        description: "Step-by-step template for consistent alert triage and documentation.",
        type: "template",
      },
      {
        id: "r5",
        title: "Incident Response Runbook",
        description: "Playbook template for common incident types including phishing and malware.",
        type: "template",
      },
      {
        id: "r6",
        title: "MITRE ATT&CK Navigator",
        description: "Interactive tool for exploring and mapping adversary techniques.",
        type: "link",
        url: "https://mitre-attack.github.io/attack-navigator/",
      },
      {
        id: "r7",
        title: "VirusTotal",
        description: "Free service for analyzing files, URLs, and IP addresses for threats.",
        type: "link",
        url: "https://www.virustotal.com/",
      },
      {
        id: "r8",
        title: "AbuseIPDB",
        description: "IP address threat intelligence and reputation checking.",
        type: "link",
        url: "https://www.abuseipdb.com/",
      },
      {
        id: "r9",
        title: "Threat Intel Tools List",
        description: "Curated list of free OSINT and threat intelligence tools for analysts.",
        type: "pdf",
      },
      {
        id: "r10",
        title: "SOC Metrics & KPIs Guide",
        description: "Understanding MTTD, MTTR, and other key SOC performance metrics.",
        type: "pdf",
      },
    ],
  },
];