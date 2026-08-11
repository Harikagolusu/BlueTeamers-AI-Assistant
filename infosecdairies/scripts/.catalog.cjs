// src/data/courses/course1.ts
var courses = [
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
          }
        ]
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
          }
        ]
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
          }
        ]
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
          }
        ]
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
          }
        ]
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
          }
        ]
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
          }
        ]
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
          }
        ]
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
          }
        ]
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
          }
        ]
      }
    ],
    quizzes: [
      {
        id: "q1",
        title: "SOC Fundamentals Quiz",
        description: "Test your understanding of SOC operations, team roles, and basic workflows.",
        questionCount: 15,
        passingScore: 70,
        duration: "20 min",
        status: "unlocked"
      },
      {
        id: "q2",
        title: "Threat Landscape Assessment",
        description: "Evaluate your knowledge of threat actors, attack vectors, and MITRE ATT&CK.",
        questionCount: 20,
        passingScore: 75,
        duration: "25 min",
        status: "locked"
      },
      {
        id: "q3",
        title: "Log Analysis Challenge",
        description: "Practical quiz on Windows, Linux, and network log analysis.",
        questionCount: 15,
        passingScore: 70,
        duration: "30 min",
        status: "locked"
      },
      {
        id: "q4",
        title: "SIEM & Alert Triage Quiz",
        description: "Test your SIEM knowledge and alert triage methodology.",
        questionCount: 20,
        passingScore: 75,
        duration: "25 min",
        status: "locked"
      },
      {
        id: "q5",
        title: "Incident Response Basics",
        description: "Assess your understanding of the IR lifecycle and containment procedures.",
        questionCount: 15,
        passingScore: 70,
        duration: "20 min",
        status: "locked"
      },
      {
        id: "q6",
        title: "Final Certification Exam",
        description: "Comprehensive exam covering all course modules. Required for certification.",
        questionCount: 50,
        passingScore: 80,
        duration: "60 min",
        status: "locked"
      }
    ],
    resources: [
      {
        id: "r1",
        title: "SOC Analyst Cheat Sheet",
        description: "Quick reference guide for common SOC tasks, commands, and procedures.",
        type: "cheatsheet"
      },
      {
        id: "r2",
        title: "Windows Event ID Reference",
        description: "Comprehensive list of critical Windows Security Event IDs for threat detection.",
        type: "pdf"
      },
      {
        id: "r3",
        title: "Linux Log Analysis Guide",
        description: "Reference guide for analyzing Linux system and authentication logs.",
        type: "pdf"
      },
      {
        id: "r4",
        title: "Alert Triage Workflow Template",
        description: "Step-by-step template for consistent alert triage and documentation.",
        type: "template"
      },
      {
        id: "r5",
        title: "Incident Response Runbook",
        description: "Playbook template for common incident types including phishing and malware.",
        type: "template"
      },
      {
        id: "r6",
        title: "MITRE ATT&CK Navigator",
        description: "Interactive tool for exploring and mapping adversary techniques.",
        type: "link",
        url: "https://mitre-attack.github.io/attack-navigator/"
      },
      {
        id: "r7",
        title: "VirusTotal",
        description: "Free service for analyzing files, URLs, and IP addresses for threats.",
        type: "link",
        url: "https://www.virustotal.com/"
      },
      {
        id: "r8",
        title: "AbuseIPDB",
        description: "IP address threat intelligence and reputation checking.",
        type: "link",
        url: "https://www.abuseipdb.com/"
      },
      {
        id: "r9",
        title: "Threat Intel Tools List",
        description: "Curated list of free OSINT and threat intelligence tools for analysts.",
        type: "pdf"
      },
      {
        id: "r10",
        title: "SOC Metrics & KPIs Guide",
        description: "Understanding MTTD, MTTR, and other key SOC performance metrics.",
        type: "pdf"
      }
    ]
  }
];

// src/data/courses.ts
var courses2 = [
  ...courses,
  {
    id: "log-analysis",
    title: "Log Analysis for Beginners",
    shortTitle: "Log Analysis",
    description: "Start your journey into log analysis. Learn to read, parse, and understand security logs from various sources including Windows, Linux, and network devices.",
    difficulty: "easy",
    duration: "8 hours",
    bgImage: "courses/log-analysis-bg.jpg",
    modules: [
      {
        id: "1",
        title: "Introduction to Security Logs",
        quizId: "la-q1",
        lessons: [
          {
            id: "1.1",
            title: "What are Security Logs?",
            description: "Understanding what logs are, why they matter for security, and how they help detect threats.",
            duration: "15 min",
            status: "completed"
          },
          {
            id: "1.2",
            title: "Common Log Formats",
            description: "Learn about Syslog, CEF, JSON, CSV, and other standard log formats used in security.",
            duration: "20 min",
            status: "unlocked"
          },
          {
            id: "1.3",
            title: "Log Sources Overview",
            description: "Explore different log sources: endpoints, servers, network devices, applications, and cloud services.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "1.4",
            title: "Log Collection & Centralization",
            description: "How logs are collected, forwarded, and centralized for analysis in a SIEM.",
            duration: "20 min",
            status: "locked"
          },
          {
            id: "1.5",
            title: "Module 1 Quiz: Log Fundamentals",
            description: "Test your understanding of log basics, formats, and collection methods.",
            duration: "15 min",
            status: "locked"
          }
        ]
      },
      {
        id: "2",
        title: "Windows Event Logs",
        quizId: "la-q2",
        lessons: [
          {
            id: "2.1",
            title: "Windows Event Log Architecture",
            description: "Understanding Windows Event Log structure, channels, and the Event Viewer tool.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "2.2",
            title: "Critical Security Event IDs",
            description: "Deep dive into Event IDs 4624, 4625, 4688, 4720, 4732, 4768, 4769, and more.",
            duration: "40 min",
            status: "locked"
          },
          {
            id: "2.3",
            title: "Authentication & Logon Analysis",
            description: "Analyzing logon types, authentication protocols, and detecting suspicious login patterns.",
            duration: "35 min",
            status: "locked"
          },
          {
            id: "2.4",
            title: "Process & Command Line Logging",
            description: "Understanding Event ID 4688, Sysmon, and command-line auditing for threat detection.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "2.5",
            title: "PowerShell Logging",
            description: "Module, Script Block, and Transcription logging for detecting malicious PowerShell.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "2.6",
            title: "Hands-On: Windows Log Investigation",
            description: "Practice identifying suspicious activity in Windows event logs.",
            duration: "45 min",
            status: "locked"
          },
          {
            id: "2.7",
            title: "Module 2 Quiz: Windows Event Log Mastery",
            description: "Assess your knowledge of Windows Event IDs and log analysis.",
            duration: "25 min",
            status: "locked"
          }
        ]
      },
      {
        id: "3",
        title: "Linux System Logs",
        quizId: "la-q3",
        lessons: [
          {
            id: "3.1",
            title: "Linux Logging Architecture",
            description: "Understanding syslog, rsyslog, journald, and the /var/log directory structure.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "3.2",
            title: "Authentication Logs (auth.log/secure)",
            description: "Analyzing SSH logins, sudo usage, PAM events, and failed authentication attempts.",
            duration: "35 min",
            status: "locked"
          },
          {
            id: "3.3",
            title: "System & Application Logs",
            description: "Working with syslog, kern.log, daemon.log, and application-specific logs.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "3.4",
            title: "Web Server Logs (Apache/Nginx)",
            description: "Parsing access and error logs, detecting web attacks and suspicious requests.",
            duration: "35 min",
            status: "locked"
          },
          {
            id: "3.5",
            title: "Hands-On: Linux Log Analysis Challenge",
            description: "Investigate a simulated breach using only Linux log files.",
            duration: "45 min",
            status: "locked"
          },
          {
            id: "3.6",
            title: "Module 3 Quiz: Linux & Network Logs",
            description: "Practical quiz on Linux system, auth, and network device logs.",
            duration: "20 min",
            status: "locked"
          }
        ]
      },
      {
        id: "4",
        title: "Network Device Logs",
        quizId: "la-q4",
        lessons: [
          {
            id: "4.1",
            title: "Firewall Log Analysis",
            description: "Understanding firewall log formats, allow/deny decisions, and traffic patterns.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "4.2",
            title: "Proxy & Web Gateway Logs",
            description: "Analyzing HTTP/HTTPS traffic, user agents, and detecting C2 communications.",
            duration: "35 min",
            status: "locked"
          },
          {
            id: "4.3",
            title: "DNS Query Logs",
            description: "Detecting DNS tunneling, DGA domains, and suspicious DNS queries.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "4.4",
            title: "VPN & Remote Access Logs",
            description: "Monitoring VPN connections, geographic anomalies, and unauthorized access.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "4.5",
            title: "Module 4 Quiz: Network Log Analysis",
            description: "Test your skills on firewall, proxy, DNS, and VPN log analysis.",
            duration: "20 min",
            status: "locked"
          }
        ]
      },
      {
        id: "5",
        title: "Log Analysis Techniques",
        lessons: [
          {
            id: "5.1",
            title: "Pattern Recognition & Baseline",
            description: "Establishing normal baselines and identifying deviations.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "5.2",
            title: "Timeline Reconstruction",
            description: "Building chronological timelines from multiple log sources.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "5.3",
            title: "Correlation Across Sources",
            description: "Connecting events from different logs to see the full picture.",
            duration: "35 min",
            status: "locked"
          },
          {
            id: "5.4",
            title: "Command Line Tools for Logs",
            description: "Using grep, awk, sed, cut, and other CLI tools for log analysis.",
            duration: "40 min",
            status: "locked"
          },
          {
            id: "5.5",
            title: "Module 5 Quiz: Log Analysis Techniques",
            description: "Assess your pattern recognition, timeline, and correlation skills.",
            duration: "15 min",
            status: "locked"
          }
        ]
      },
      {
        id: "6",
        title: "Practical Log Analysis",
        quizId: "la-q5",
        lessons: [
          {
            id: "6.1",
            title: "Detecting Brute Force Attacks",
            description: "Identifying password spraying and brute force patterns in logs.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "6.2",
            title: "Detecting Lateral Movement",
            description: "Finding signs of attackers moving through the network.",
            duration: "35 min",
            status: "locked"
          },
          {
            id: "6.3",
            title: "Detecting Data Exfiltration",
            description: "Identifying unusual data transfers and potential data theft.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "6.4",
            title: "Final Practical Challenge",
            description: "Complete investigation scenario using all log analysis skills.",
            duration: "60 min",
            status: "locked"
          },
          {
            id: "6.5",
            title: "Final Certification Exam",
            description: "Comprehensive exam covering all log analysis modules.",
            duration: "45 min",
            status: "locked"
          }
        ]
      }
    ],
    quizzes: [
      {
        id: "la-q1",
        title: "Log Fundamentals Quiz",
        description: "Test your understanding of log formats, sources, and basic concepts.",
        questionCount: 15,
        passingScore: 70,
        duration: "15 min",
        status: "unlocked"
      },
      {
        id: "la-q2",
        title: "Windows Event Log Mastery",
        description: "Assess your knowledge of Windows Event IDs and log analysis.",
        questionCount: 20,
        passingScore: 75,
        duration: "25 min",
        status: "locked"
      },
      {
        id: "la-q3",
        title: "Linux Log Analysis Challenge",
        description: "Practical quiz on Linux system and authentication logs.",
        questionCount: 15,
        passingScore: 70,
        duration: "20 min",
        status: "locked"
      },
      {
        id: "la-q4",
        title: "Network Log Analysis",
        description: "Test your skills on firewall, proxy, and DNS log analysis.",
        questionCount: 15,
        passingScore: 70,
        duration: "20 min",
        status: "locked"
      },
      {
        id: "la-q5",
        title: "Final Certification Exam",
        description: "Comprehensive exam covering all log analysis modules. Required for certification.",
        questionCount: 40,
        passingScore: 80,
        duration: "45 min",
        status: "locked"
      }
    ],
    resources: [
      {
        id: "la-r1",
        title: "Windows Event ID Cheat Sheet",
        description: "Quick reference for critical Windows Security Event IDs and their meanings.",
        type: "cheatsheet"
      },
      {
        id: "la-r2",
        title: "Linux Log Files Reference",
        description: "Comprehensive guide to Linux log file locations and their purposes.",
        type: "pdf"
      },
      {
        id: "la-r3",
        title: "Log Analysis CLI Commands",
        description: "Collection of grep, awk, sed, and other CLI commands for log parsing.",
        type: "cheatsheet"
      },
      {
        id: "la-r4",
        title: "Common Attack Patterns in Logs",
        description: "Reference guide showing how different attacks appear in various log sources.",
        type: "pdf"
      },
      {
        id: "la-r5",
        title: "Sysmon Configuration Guide",
        description: "Best practices for configuring Sysmon for enhanced Windows logging.",
        type: "template"
      },
      {
        id: "la-r6",
        title: "Log Parsing Regex Patterns",
        description: "Regular expressions for extracting data from common log formats.",
        type: "cheatsheet"
      },
      {
        id: "la-r7",
        title: "CyberChef",
        description: "Web-based tool for decoding, parsing, and analyzing data from logs.",
        type: "link",
        url: "https://gchq.github.io/CyberChef/"
      },
      {
        id: "la-r8",
        title: "Windows Event Log Encyclopedia",
        description: "Ultimate Windows Security reference for all event IDs.",
        type: "link",
        url: "https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/"
      }
    ]
  },
  {
    id: "siem-fundamentals",
    title: "SIEM Fundamentals",
    shortTitle: "SIEM Basics",
    description: "Master Security Information and Event Management basics. Learn to navigate and understand modern SIEM platforms, create queries, build dashboards, and respond to alerts effectively.",
    difficulty: "easy",
    duration: "10 hours",
    bgImage: "courses/siem-fundamentals-bg.jpg",
    modules: [
      {
        id: "1",
        title: "Introduction to SIEM",
        quizId: "siem-q1",
        lessons: [
          {
            id: "1.1",
            title: "What is SIEM?",
            description: "Understanding SIEM technology, its purpose, and how it fits into modern security operations.",
            duration: "20 min",
            status: "unlocked"
          },
          {
            id: "1.2",
            title: "SIEM Architecture & Components",
            description: "Learn about data collectors, indexers, search heads, and the data flow in SIEM platforms.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "1.3",
            title: "Popular SIEM Platforms Overview",
            description: "Compare Splunk, Microsoft Sentinel, Elastic SIEM, QRadar, and other major platforms.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "1.4",
            title: "SIEM Use Cases in Security",
            description: "Real-world applications: threat detection, compliance, incident response, and forensics.",
            duration: "20 min",
            status: "locked"
          },
          {
            id: "siem-q1",
            title: "Module 1 Quiz: SIEM Fundamentals",
            description: "Test your understanding of SIEM architecture, components, and basic concepts.",
            duration: "15 min",
            status: "locked"
          }
        ]
      },
      {
        id: "2",
        title: "Data Ingestion & Management",
        quizId: "siem-q2",
        lessons: [
          {
            id: "2.1",
            title: "Log Collection Methods",
            description: "Agent-based vs agentless collection, syslog, API integrations, and forwarders.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "2.2",
            title: "Data Normalization & Parsing",
            description: "Converting raw logs into structured, searchable data with field extraction.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "2.3",
            title: "Data Sources & Indexing",
            description: "Understanding indexes, source types, and how data is organized for efficient searching.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "2.4",
            title: "Data Retention & Storage",
            description: "Managing data lifecycle, hot/warm/cold storage tiers, and compliance requirements.",
            duration: "20 min",
            status: "locked"
          },
          {
            id: "siem-q2",
            title: "Module 2 Quiz: Data Ingestion Assessment",
            description: "Evaluate your knowledge of log collection, normalization, and data management.",
            duration: "15 min",
            status: "locked"
          }
        ]
      },
      {
        id: "3",
        title: "Search & Query Fundamentals",
        lessons: [
          {
            id: "3.1",
            title: "Basic Search Syntax",
            description: "Writing your first SIEM queries, using keywords, and understanding search modes.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "3.2",
            title: "Filtering & Field Extraction",
            description: "Narrowing results with filters, boolean operators, and extracting specific fields.",
            duration: "35 min",
            status: "locked"
          },
          {
            id: "3.3",
            title: "Time Range & Wildcards",
            description: "Searching across time periods, using wildcards, and optimizing search performance.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "3.4",
            title: "Hands-On: Basic Search Lab",
            description: "Practice writing queries to find specific security events in sample data.",
            duration: "40 min",
            status: "locked"
          }
        ]
      },
      {
        id: "4",
        title: "Advanced Query Techniques",
        quizId: "siem-q3",
        lessons: [
          {
            id: "4.1",
            title: "Aggregation & Statistics",
            description: "Using stats, count, sum, avg, and other aggregation commands for analysis.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "4.2",
            title: "Joins & Lookups",
            description: "Combining data from multiple sources and enriching events with lookup tables.",
            duration: "35 min",
            status: "locked"
          },
          {
            id: "4.3",
            title: "Subsearches & Transactions",
            description: "Building complex queries with nested searches and grouping related events.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "4.4",
            title: "Hands-On: Advanced Query Lab",
            description: "Create complex queries to investigate a simulated security incident.",
            duration: "45 min",
            status: "locked"
          },
          {
            id: "siem-q3",
            title: "Module 4 Quiz: Search & Query Mastery",
            description: "Practical quiz on writing SIEM queries and search techniques.",
            duration: "25 min",
            status: "locked"
          }
        ]
      },
      {
        id: "5",
        title: "Dashboards & Visualization",
        lessons: [
          {
            id: "5.1",
            title: "Dashboard Fundamentals",
            description: "Creating effective security dashboards with charts, tables, and single value panels.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "5.2",
            title: "Visualization Types",
            description: "Choosing the right chart: line, bar, pie, heatmaps, and geographic maps.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "5.3",
            title: "Interactive Dashboards",
            description: "Adding drill-downs, filters, time pickers, and dynamic inputs to dashboards.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "5.4",
            title: "Hands-On: Build a SOC Dashboard",
            description: "Create a functional security operations dashboard from scratch.",
            duration: "50 min",
            status: "locked"
          }
        ]
      },
      {
        id: "6",
        title: "Alerts & Correlation Rules",
        quizId: "siem-q4",
        lessons: [
          {
            id: "6.1",
            title: "Understanding SIEM Alerts",
            description: "How alerts are generated, severity levels, and alert fatigue management.",
            duration: "20 min",
            status: "locked"
          },
          {
            id: "6.2",
            title: "Creating Detection Rules",
            description: "Building correlation rules to detect suspicious patterns and behaviors.",
            duration: "35 min",
            status: "locked"
          },
          {
            id: "6.3",
            title: "Alert Tuning & Optimization",
            description: "Reducing false positives and improving detection accuracy over time.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "6.4",
            title: "Alert Response Actions",
            description: "Configuring notifications, automated responses, and escalation workflows.",
            duration: "25 min",
            status: "locked"
          },
          {
            id: "siem-q4",
            title: "Module 6 Quiz: Dashboards & Alerts",
            description: "Test your skills on visualization, dashboards, and alert configuration.",
            duration: "15 min",
            status: "locked"
          }
        ]
      },
      {
        id: "7",
        title: "Practical SIEM Operations",
        quizId: "siem-q5",
        lessons: [
          {
            id: "7.1",
            title: "Alert Triage Workflow",
            description: "Step-by-step process for investigating and responding to SIEM alerts.",
            duration: "30 min",
            status: "locked"
          },
          {
            id: "7.2",
            title: "Investigation Techniques",
            description: "Using SIEM to pivot, correlate, and build investigation timelines.",
            duration: "35 min",
            status: "locked"
          },
          {
            id: "7.3",
            title: "SIEM Best Practices",
            description: "Tips for effective SIEM usage, query optimization, and daily operations.",
            duration: "20 min",
            status: "locked"
          },
          {
            id: "7.4",
            title: "Final Practical Challenge",
            description: "Complete a full investigation scenario using all learned SIEM skills.",
            duration: "60 min",
            status: "locked"
          },
          {
            id: "siem-q5",
            title: "Final Certification Exam: SIEM Fundamentals",
            description: "Comprehensive exam covering all SIEM fundamentals modules. Required for certification.",
            duration: "45 min",
            status: "locked"
          }
        ]
      }
    ],
    quizzes: [
      {
        id: "siem-q1",
        title: "SIEM Fundamentals Quiz",
        description: "Test your understanding of SIEM architecture, components, and basic concepts.",
        questionCount: 15,
        passingScore: 70,
        duration: "15 min",
        status: "unlocked"
      },
      {
        id: "siem-q2",
        title: "Data Ingestion Assessment",
        description: "Evaluate your knowledge of log collection, normalization, and data management.",
        questionCount: 15,
        passingScore: 70,
        duration: "15 min",
        status: "locked"
      },
      {
        id: "siem-q3",
        title: "Search & Query Mastery",
        description: "Practical quiz on writing SIEM queries and search techniques.",
        questionCount: 20,
        passingScore: 75,
        duration: "25 min",
        status: "locked"
      },
      {
        id: "siem-q4",
        title: "Dashboards & Alerts Quiz",
        description: "Test your skills on visualization, dashboards, and alert configuration.",
        questionCount: 15,
        passingScore: 70,
        duration: "15 min",
        status: "locked"
      },
      {
        id: "siem-q5",
        title: "Final Certification Exam",
        description: "Comprehensive exam covering all SIEM fundamentals modules. Required for certification.",
        questionCount: 40,
        passingScore: 80,
        duration: "45 min",
        status: "locked"
      }
    ],
    resources: [
      {
        id: "siem-r1",
        title: "SIEM Query Cheat Sheet",
        description: "Quick reference for common SIEM search commands and syntax patterns.",
        type: "cheatsheet"
      },
      {
        id: "siem-r2",
        title: "SPL (Splunk) Quick Reference",
        description: "Essential Splunk Processing Language commands for security analysts.",
        type: "cheatsheet"
      },
      {
        id: "siem-r3",
        title: "KQL (Sentinel) Quick Reference",
        description: "Kusto Query Language basics for Microsoft Sentinel users.",
        type: "cheatsheet"
      },
      {
        id: "siem-r4",
        title: "SIEM Dashboard Templates",
        description: "Pre-built dashboard templates for common SOC monitoring use cases.",
        type: "template"
      },
      {
        id: "siem-r5",
        title: "Alert Tuning Guide",
        description: "Best practices for reducing false positives and optimizing detection rules.",
        type: "pdf"
      },
      {
        id: "siem-r6",
        title: "SIEM Platform Comparison",
        description: "Feature comparison of major SIEM platforms for informed decision-making.",
        type: "pdf"
      },
      {
        id: "siem-r7",
        title: "Splunk Documentation",
        description: "Official Splunk documentation and training resources.",
        type: "link",
        url: "https://docs.splunk.com/"
      },
      {
        id: "siem-r8",
        title: "Microsoft Sentinel Docs",
        description: "Official Microsoft Sentinel documentation and learning paths.",
        type: "link",
        url: "https://learn.microsoft.com/en-us/azure/sentinel/"
      }
    ]
  },
  {
    id: "network-security-monitoring",
    title: "Network Security Monitoring",
    shortTitle: "NSM",
    description: "Master deep packet inspection, network-based threat detection, and traffic analysis. Learn to use tools like Zeek, Suricata, and Wireshark to identify malicious activity on the wire.",
    difficulty: "medium",
    duration: "14 hours",
    bgImage: "courses/soc-analyst-practical-bg.jpg",
    modules: [
      {
        id: "1",
        title: "NSM Foundations",
        quizId: "nsm-q1",
        lessons: [
          { id: "1.1", title: "What is Network Security Monitoring?", description: "Understanding NSM philosophy, goals, and how it complements endpoint detection.", status: "unlocked" },
          { id: "1.2", title: "Network Protocols Deep Dive", description: "TCP/IP, UDP, DNS, HTTP/S, and other protocols from a security perspective.", status: "locked" },
          { id: "1.3", title: "The OSI Model for Defenders", description: "How each OSI layer exposes different attack surfaces and detection opportunities.", status: "locked" },
          { id: "1.4", title: "NSM Architecture & Sensor Placement", description: "Designing network tap points, SPAN ports, and sensor deployment strategies.", status: "locked" },
          { id: "1.5", title: "Module 1 Quiz: NSM Foundations", description: "Test your knowledge of NSM philosophy, network protocols, OSI model, and sensor placement.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "2",
        title: "Packet Capture & Analysis",
        quizId: "nsm-q2",
        lessons: [
          { id: "2.1", title: "Introduction to Wireshark", description: "Navigating the Wireshark interface, capture filters, and display filters.", status: "locked" },
          { id: "2.2", title: "TCP Stream Analysis", description: "Following TCP conversations, identifying retransmissions, and session reconstruction.", status: "locked" },
          { id: "2.3", title: "DNS Traffic Analysis", description: "Detecting DNS tunneling, DGA domains, and suspicious query patterns.", status: "locked" },
          { id: "2.4", title: "HTTP/HTTPS Traffic Inspection", description: "Analyzing web traffic, extracting files, and identifying malicious payloads.", status: "locked" },
          { id: "2.5", title: "Hands-On: PCAP Analysis Lab", description: "Investigate real-world attack PCAPs to identify malicious activity.", status: "locked" },
          { id: "2.6", title: "Module 2 Quiz: Packet Capture & Analysis", description: "Assess your Wireshark skills, TCP stream analysis, DNS and HTTP traffic inspection.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "3",
        title: "Intrusion Detection with Suricata",
        quizId: "nsm-q3",
        lessons: [
          { id: "3.1", title: "Suricata Architecture & Setup", description: "Installing and configuring Suricata as an IDS/IPS engine.", status: "locked" },
          { id: "3.2", title: "Writing Suricata Rules", description: "Rule syntax, content matching, flow keywords, and protocol-specific options.", status: "locked" },
          { id: "3.3", title: "Alert Management & Tuning", description: "Managing alert output, suppressing false positives, and threshold configuration.", status: "locked" },
          { id: "3.4", title: "Hands-On: Custom Detection Rules", description: "Write and test Suricata rules to detect specific attack patterns.", status: "locked" },
          { id: "3.5", title: "Module 3 Quiz: Intrusion Detection with Suricata", description: "Evaluate your understanding of Suricata architecture, rule writing, and alert tuning.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "4",
        title: "Network Metadata with Zeek",
        quizId: "nsm-q4",
        lessons: [
          { id: "4.1", title: "Introduction to Zeek", description: "Understanding Zeek's role in NSM and its log-based approach to network analysis.", status: "locked" },
          { id: "4.2", title: "Zeek Log Types", description: "Exploring conn.log, dns.log, http.log, ssl.log, files.log, and other key logs.", status: "locked" },
          { id: "4.3", title: "Threat Hunting with Zeek Logs", description: "Using Zeek metadata to detect C2 beacons, lateral movement, and exfiltration.", status: "locked" },
          { id: "4.4", title: "Zeek Scripting Basics", description: "Writing simple Zeek scripts to create custom detections and log enrichments.", status: "locked" },
          { id: "4.5", title: "Module 4 Quiz: Network Metadata with Zeek", description: "Test your knowledge of Zeek logs, threat hunting with metadata, and Zeek scripting.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "5",
        title: "Network Attack Detection",
        quizId: "nsm-q5",
        lessons: [
          { id: "5.1", title: "Detecting Reconnaissance", description: "Identifying port scans, service enumeration, and network mapping attempts.", status: "locked" },
          { id: "5.2", title: "Detecting Command & Control", description: "Recognizing C2 beaconing patterns, encrypted channels, and covert communications.", status: "locked" },
          { id: "5.3", title: "Detecting Lateral Movement", description: "Spotting SMB abuse, RDP pivoting, PsExec, and pass-the-hash on the network.", status: "locked" },
          { id: "5.4", title: "Detecting Data Exfiltration", description: "Identifying large transfers, DNS exfil, steganography, and protocol tunneling.", status: "locked" },
          { id: "5.5", title: "Module 5 Quiz: Network Attack Detection", description: "Assess your ability to detect reconnaissance, C2, lateral movement, and exfiltration.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "6",
        title: "Practical NSM Operations",
        quizId: "nsm-q6",
        lessons: [
          { id: "6.1", title: "Building an NSM Workflow", description: "Integrating Zeek, Suricata, and SIEM for a complete monitoring pipeline.", status: "locked" },
          { id: "6.2", title: "Network Forensics Basics", description: "Evidence preservation, timeline construction, and reporting from network data.", status: "locked" },
          { id: "6.3", title: "NSM Best Practices", description: "Sensor maintenance, rule updates, and operational efficiency tips.", status: "locked" },
          { id: "6.4", title: "Final Practical Challenge", description: "Investigate a multi-stage network intrusion using all NSM tools and techniques.", status: "locked" },
          { id: "6.5", title: "Module 6 Quiz: Practical NSM Operations", description: "Evaluate your understanding of NSM workflows, network forensics, and best practices.", duration: "15 min", status: "locked" }
        ]
      }
    ],
    quizzes: [
      { id: "nsm-q1", title: "NSM Foundations Quiz", description: "Test your knowledge of NSM philosophy, network protocols, OSI model, and sensor placement.", questionCount: 10, passingScore: 70, duration: "15 min", status: "unlocked" },
      { id: "nsm-q2", title: "Packet Capture & Analysis Quiz", description: "Assess your Wireshark skills, TCP stream analysis, DNS and HTTP traffic inspection.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "nsm-q3", title: "Intrusion Detection with Suricata Quiz", description: "Evaluate your understanding of Suricata architecture, rule writing, and alert tuning.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "nsm-q4", title: "Network Metadata with Zeek Quiz", description: "Test your knowledge of Zeek logs, threat hunting with metadata, and Zeek scripting.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "nsm-q5", title: "Network Attack Detection Quiz", description: "Assess your ability to detect reconnaissance, C2, lateral movement, and exfiltration.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "nsm-q6", title: "Practical NSM Operations Quiz", description: "Evaluate your understanding of NSM workflows, network forensics, and best practices.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" }
    ],
    resources: [
      { id: "nsm-r1", title: "Wireshark Display Filter Cheat Sheet", description: "Quick reference for common Wireshark display filters used in threat detection.", type: "cheatsheet" },
      { id: "nsm-r2", title: "Suricata Rule Writing Guide", description: "Comprehensive guide to Suricata rule syntax, keywords, and best practices.", type: "pdf" },
      { id: "nsm-r3", title: "Zeek Log Field Reference", description: "Complete field reference for conn.log, dns.log, http.log, ssl.log, and files.log.", type: "cheatsheet" },
      { id: "nsm-r4", title: "Network Attack Signatures", description: "Reference of common network attack patterns and their corresponding traffic signatures.", type: "pdf" },
      { id: "nsm-r5", title: "PCAP Analysis Workflow Template", description: "Step-by-step template for systematic packet capture analysis during investigations.", type: "template" },
      { id: "nsm-r6", title: "BPF Filter Reference", description: "Berkeley Packet Filter syntax guide for tcpdump and Wireshark capture filters.", type: "cheatsheet" },
      { id: "nsm-r7", title: "Wireshark Official Docs", description: "Official Wireshark user guide and protocol dissector documentation.", type: "link", url: "https://www.wireshark.org/docs/" },
      { id: "nsm-r8", title: "Zeek Documentation", description: "Official Zeek documentation including scripting reference and log formats.", type: "link", url: "https://docs.zeek.org/" }
    ]
  },
  {
    id: "incident-response",
    title: "Incident Response Fundamentals",
    shortTitle: "Incident Response",
    description: "Learn the complete incident response lifecycle. Master containment, eradication, recovery, and post-incident analysis procedures used by IR professionals.",
    difficulty: "medium",
    duration: "12 hours",
    bgImage: "courses/incident-response-bg.jpg",
    modules: [
      {
        id: "1",
        title: "IR Foundations & Frameworks",
        quizId: "ir-q1",
        lessons: [
          { id: "1.1", title: "What is Incident Response?", description: "Defining incidents, events, and the role of IR in modern cybersecurity.", status: "unlocked" },
          { id: "1.2", title: "NIST IR Lifecycle", description: "Preparation, Detection & Analysis, Containment, Eradication & Recovery, Post-Incident.", status: "locked" },
          { id: "1.3", title: "SANS PICERL Framework", description: "Comparing the SANS six-phase model with NIST and understanding when to use each.", status: "locked" },
          { id: "1.4", title: "Building an IR Team", description: "Roles, responsibilities, RACI matrices, and cross-functional coordination.", status: "locked" },
          { id: "ir-q1", title: "Module 1 Quiz: IR Foundations & Frameworks", description: "Test your knowledge of incident response fundamentals, lifecycle models, and IR team structure.", status: "locked" }
        ]
      },
      {
        id: "2",
        title: "Preparation & Readiness",
        quizId: "ir-q2",
        lessons: [
          { id: "2.1", title: "IR Policy & Plan Development", description: "Crafting incident response policies, playbooks, and escalation procedures.", status: "locked" },
          { id: "2.2", title: "Communication Plans", description: "Internal notifications, external disclosure, legal obligations, and media handling.", status: "locked" },
          { id: "2.3", title: "IR Toolkit & Jump Bag", description: "Essential tools, forensic hardware, and software for rapid deployment.", status: "locked" },
          { id: "2.4", title: "Tabletop Exercises", description: "Designing and running tabletop scenarios to test IR readiness.", status: "locked" },
          { id: "ir-q2", title: "Module 2 Quiz: Preparation & Readiness", description: "Test your knowledge of IR planning, communication, toolkit preparation, and tabletop exercises.", status: "locked" }
        ]
      },
      {
        id: "3",
        title: "Detection & Analysis",
        quizId: "ir-q3",
        lessons: [
          { id: "3.1", title: "Incident Detection Sources", description: "SIEM alerts, EDR detections, user reports, threat intelligence feeds.", status: "locked" },
          { id: "3.2", title: "Incident Triage & Prioritization", description: "Severity classification, impact assessment, and resource allocation.", status: "locked" },
          { id: "3.3", title: "Indicator Analysis", description: "Analyzing IOCs, correlating events, and building attack timelines.", status: "locked" },
          { id: "3.4", title: "Root Cause Analysis Techniques", description: "The 5 Whys, fishbone diagrams, and fault tree analysis for incidents.", status: "locked" },
          { id: "ir-q3", title: "Module 3 Quiz: Detection & Analysis", description: "Test your understanding of detection sources, triage, indicator analysis, and root cause analysis.", status: "locked" }
        ]
      },
      {
        id: "4",
        title: "Containment Strategies",
        quizId: "ir-q4",
        lessons: [
          { id: "4.1", title: "Short-Term Containment", description: "Network isolation, port blocking, DNS sinkholes, and immediate threat neutralization.", status: "locked" },
          { id: "4.2", title: "Long-Term Containment", description: "System reimaging, account lockdowns, credential rotation, and segmentation.", status: "locked" },
          { id: "4.3", title: "Evidence Preservation", description: "Chain of custody, memory acquisition, disk imaging, and log preservation.", status: "locked" },
          { id: "4.4", title: "Containment Decision Framework", description: "Balancing business continuity with security\u2014when to isolate vs. monitor.", status: "locked" },
          { id: "ir-q4", title: "Module 4 Quiz: Containment Strategies", description: "Test your knowledge of containment, evidence preservation, and decision-making frameworks.", status: "locked" }
        ]
      },
      {
        id: "5",
        title: "Eradication & Recovery",
        quizId: "ir-q5",
        lessons: [
          { id: "5.1", title: "Malware Removal & Cleanup", description: "Removing persistence mechanisms, backdoors, and malicious artifacts.", status: "locked" },
          { id: "5.2", title: "System Restoration", description: "Rebuilding from clean images, patching vulnerabilities, and hardening configurations.", status: "locked" },
          { id: "5.3", title: "Validation & Monitoring", description: "Verifying eradication success and implementing enhanced monitoring post-recovery.", status: "locked" },
          { id: "5.4", title: "Business Resumption", description: "Phased recovery, user communication, and service restoration procedures.", status: "locked" },
          { id: "ir-q5", title: "Module 5 Quiz: Eradication & Recovery", description: "Test your knowledge of malware removal, system restoration, validation, and business resumption.", status: "locked" }
        ]
      },
      {
        id: "6",
        title: "Post-Incident Activities",
        quizId: "ir-q6",
        lessons: [
          { id: "6.1", title: "Lessons Learned Meetings", description: "Facilitating blameless post-mortems and extracting actionable improvements.", status: "locked" },
          { id: "6.2", title: "Incident Report Writing", description: "Executive summaries, technical findings, timeline documentation, and recommendations.", status: "locked" },
          { id: "6.3", title: "Metrics & KPIs", description: "MTTD, MTTR, dwell time, and other metrics for measuring IR effectiveness.", status: "locked" },
          { id: "6.4", title: "Continuous Improvement", description: "Updating playbooks, tuning detections, and feeding lessons into the preparation phase.", status: "locked" },
          { id: "ir-q6", title: "Module 6 Quiz: Post-Incident Activities", description: "Test your knowledge of lessons learned, report writing, metrics, and continuous improvement.", status: "locked" }
        ]
      },
      {
        id: "7",
        title: "IR Certification Exam",
        quizId: "ir-q7",
        lessons: [
          { id: "ir-q7", title: "Final Certification Exam: Incident Response", description: "Comprehensive final exam covering all modules. You must pass with 80% or higher to earn your certificate.", status: "locked" }
        ]
      }
    ],
    quizzes: [
      { id: "ir-q1", title: "IR Foundations & Frameworks Quiz", description: "Test your knowledge of IR lifecycle models, NIST and SANS frameworks, and team structure.", questionCount: 10, passingScore: 70, duration: "15 min", status: "unlocked" },
      { id: "ir-q2", title: "Preparation & Readiness Quiz", description: "Assess your understanding of IR policies, communication plans, toolkits, and tabletop exercises.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "ir-q3", title: "Detection & Analysis Quiz", description: "Evaluate your skills in incident detection, triage, indicator analysis, and root cause techniques.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "ir-q4", title: "Containment Strategies Quiz", description: "Test containment approaches including isolation, evidence preservation, and decision frameworks.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "ir-q5", title: "Eradication & Recovery Quiz", description: "Assess knowledge of malware removal, system restoration, validation, and business resumption.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "ir-q6", title: "Post-Incident Activities Quiz", description: "Evaluate understanding of lessons learned, report writing, IR metrics, and continuous improvement.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "ir-q7", title: "IR Certification Exam", description: "Comprehensive final exam covering all 6 modules. You must pass with 80% or higher to earn your Incident Response Fundamentals certificate.", questionCount: 20, passingScore: 80, duration: "25 min", status: "locked" }
    ],
    resources: [
      { id: "ir-r1", title: "IR Playbook Template", description: "Pre-built incident response playbook covering phishing, malware, and data breach scenarios.", type: "template" },
      { id: "ir-r2", title: "NIST SP 800-61 Summary", description: "Condensed reference of the NIST Computer Security Incident Handling Guide.", type: "pdf" },
      { id: "ir-r3", title: "Evidence Collection Checklist", description: "Step-by-step checklist for volatile and non-volatile evidence acquisition and chain of custody.", type: "cheatsheet" },
      { id: "ir-r4", title: "Incident Severity Matrix", description: "Template for classifying incident severity based on impact, scope, and data sensitivity.", type: "template" },
      { id: "ir-r5", title: "Post-Incident Report Template", description: "Structured template for executive summaries, timelines, findings, and recommendations.", type: "template" },
      { id: "ir-r6", title: "Containment Decision Tree", description: "Visual guide for choosing containment strategies based on incident type and business impact.", type: "pdf" },
      { id: "ir-r7", title: "NIST Incident Handling Guide", description: "Official NIST SP 800-61 Rev.2 publication for incident response.", type: "link", url: "https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final" },
      { id: "ir-r8", title: "SANS Incident Handler's Handbook", description: "SANS reading room paper covering practical incident handling procedures.", type: "link", url: "https://www.sans.org/white-papers/33901/" }
    ]
  },
  {
    id: "threat-hunting",
    title: "Threat Hunting Fundamentals",
    shortTitle: "Threat Hunting",
    description: "Proactively search for threats in your environment. Learn hypothesis-driven hunting, IOC analysis, and threat intelligence integration techniques.",
    difficulty: "hard",
    duration: "14 hours",
    bgImage: "courses/threat-hunting-bg.jpg",
    modules: [
      {
        id: "1",
        title: "Hunting Methodology & Mindset",
        quizId: "th-q1",
        lessons: [
          { id: "1.1", title: "Proactive vs Reactive Security", description: "Understanding the threat hunting mindset and why reactive detection alone is insufficient.", status: "unlocked" },
          { id: "1.2", title: "Threat Hunting Maturity Model", description: "HMM levels 0\u20134 and how to assess your organization's hunting capability.", status: "locked" },
          { id: "1.3", title: "Hypothesis-Driven Hunting", description: "Formulating testable hypotheses from threat intelligence, TTPs, and environmental context.", status: "locked" },
          { id: "1.4", title: "Data Sources for Hunting", description: "Identifying and prioritizing telemetry: endpoint, network, cloud, and identity logs.", status: "locked" },
          { id: "1.5", title: "Module 1 Quiz: Hunting Methodology & Mindset", description: "Test your understanding of proactive hunting philosophy, maturity models, and hypothesis development.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "2",
        title: "Threat Intelligence Integration",
        quizId: "th-q2",
        lessons: [
          { id: "2.1", title: "Threat Intelligence Platforms", description: "MISP, OpenCTI, ThreatConnect\u2014aggregating and operationalizing intel feeds.", status: "locked" },
          { id: "2.2", title: "IOC Types & Pyramid of Pain", description: "Hash values, IP addresses, domains, artifacts, tools, and TTPs\u2014what matters most.", status: "locked" },
          { id: "2.3", title: "MITRE ATT&CK for Hunters", description: "Mapping hunts to ATT&CK techniques, sub-techniques, and data sources.", status: "locked" },
          { id: "2.4", title: "Building Threat Profiles", description: "Creating adversary profiles and predicting likely attack paths in your environment.", status: "locked" },
          { id: "2.5", title: "Module 2 Quiz: Threat Intelligence Integration", description: "Assess your knowledge of TI platforms, IOC types, ATT&CK mapping, and threat profiling.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "3",
        title: "Hunting Techniques & Tradecraft",
        quizId: "th-q3",
        lessons: [
          { id: "3.1", title: "Behavioral Analysis Hunting", description: "Identifying anomalous behavior patterns that evade signature-based detection.", status: "locked" },
          { id: "3.2", title: "Statistical & Anomaly-Based Hunting", description: "Using frequency analysis, stacking, and outlier detection to find threats.", status: "locked" },
          { id: "3.3", title: "Living Off the Land Detection", description: "Hunting for LOLBins, PowerShell abuse, WMI persistence, and dual-use tools.", status: "locked" },
          { id: "3.4", title: "Hunting with YARA & Sigma", description: "Writing and deploying detection content during active hunts.", status: "locked" },
          { id: "3.5", title: "Module 3 Quiz: Hunting Techniques & Tradecraft", description: "Evaluate your skills in behavioral analysis, anomaly hunting, LOLBin detection, and YARA/Sigma.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "4",
        title: "Endpoint Threat Hunting",
        quizId: "th-q4",
        lessons: [
          { id: "4.1", title: "Process Tree Analysis", description: "Analyzing parent-child process relationships to detect malicious execution chains.", status: "locked" },
          { id: "4.2", title: "Persistence Mechanism Hunting", description: "Registry run keys, scheduled tasks, services, WMI subscriptions, and startup folders.", status: "locked" },
          { id: "4.3", title: "Memory & Fileless Threat Hunting", description: "Detecting process injection, reflective DLL loading, and in-memory-only payloads.", status: "locked" },
          { id: "4.4", title: "Credential Access Hunting", description: "Detecting LSASS dumps, Kerberoasting, AS-REP roasting, and token manipulation.", status: "locked" },
          { id: "4.5", title: "Module 4 Quiz: Endpoint Threat Hunting", description: "Test your knowledge of process analysis, persistence hunting, fileless threats, and credential attacks.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "5",
        title: "Network & Cloud Hunting",
        quizId: "th-q5",
        lessons: [
          { id: "5.1", title: "Network-Based Threat Hunting", description: "Hunting in Zeek logs, NetFlow, and DNS data for lateral movement and C2.", status: "locked" },
          { id: "5.2", title: "Encrypted Traffic Analysis", description: "JA3/JA3S fingerprinting, certificate anomalies, and TLS metadata hunting.", status: "locked" },
          { id: "5.3", title: "Cloud Environment Hunting", description: "Hunting in AWS CloudTrail, Azure Activity Logs, and GCP Audit Logs.", status: "locked" },
          { id: "5.4", title: "Identity-Based Hunting", description: "Detecting impossible travel, MFA fatigue attacks, and OAuth token abuse.", status: "locked" },
          { id: "5.5", title: "Module 5 Quiz: Network & Cloud Hunting", description: "Assess your ability to hunt in network metadata, encrypted traffic, cloud logs, and identity systems.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "6",
        title: "Hunt Operations & Reporting",
        quizId: "th-q6",
        lessons: [
          { id: "6.1", title: "Planning & Scoping Hunts", description: "Defining objectives, timelines, data requirements, and success criteria.", status: "locked" },
          { id: "6.2", title: "Hunt Automation & Notebooks", description: "Using Jupyter notebooks, KQL, and SPL for repeatable hunt workflows.", status: "locked" },
          { id: "6.3", title: "Documenting & Reporting Findings", description: "Writing actionable hunt reports that drive detection engineering improvements.", status: "locked" },
          { id: "6.4", title: "From Hunt to Detection", description: "Converting successful hunts into automated detections and continuous monitoring.", status: "locked" },
          { id: "6.5", title: "Module 6 Quiz: Hunt Operations & Reporting", description: "Evaluate your understanding of hunt planning, automation, reporting, and converting hunts to detections.", duration: "15 min", status: "locked" }
        ]
      }
    ],
    quizzes: [
      { id: "th-q1", title: "Hunting Methodology & Mindset Quiz", description: "Test your understanding of proactive hunting philosophy, maturity models, and hypothesis development.", questionCount: 10, passingScore: 70, duration: "15 min", status: "unlocked" },
      { id: "th-q2", title: "Threat Intelligence Integration Quiz", description: "Assess your knowledge of TI platforms, IOC types, ATT&CK mapping, and threat profiling.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "th-q3", title: "Hunting Techniques & Tradecraft Quiz", description: "Evaluate your skills in behavioral analysis, anomaly hunting, LOLBin detection, and YARA/Sigma.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "th-q4", title: "Endpoint Threat Hunting Quiz", description: "Test your knowledge of process analysis, persistence hunting, fileless threats, and credential attacks.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "th-q5", title: "Network & Cloud Hunting Quiz", description: "Assess your ability to hunt in network metadata, encrypted traffic, cloud logs, and identity systems.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "th-q6", title: "Hunt Operations & Reporting Quiz", description: "Evaluate your understanding of hunt planning, automation, reporting, and converting hunts to detections.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" }
    ],
    resources: [
      { id: "th-r1", title: "Threat Hunting Hypothesis Templates", description: "Pre-built hypothesis templates aligned to MITRE ATT&CK techniques for structured hunts.", type: "template" },
      { id: "th-r2", title: "Pyramid of Pain Reference", description: "Visual guide to indicator types ranked by adversary impact when denied.", type: "cheatsheet" },
      { id: "th-r3", title: "LOLBins & LOLScripts Reference", description: "Comprehensive list of living-off-the-land binaries and scripts with detection guidance.", type: "cheatsheet" },
      { id: "th-r4", title: "Hunt Report Template", description: "Structured template for documenting hunt scope, methodology, findings, and detection recommendations.", type: "template" },
      { id: "th-r5", title: "JA3/JA3S Fingerprint Database", description: "Reference of known JA3 fingerprints for malware families, tools, and legitimate applications.", type: "pdf" },
      { id: "th-r6", title: "Threat Hunting Query Library", description: "Collection of ready-to-use SPL and KQL queries organized by ATT&CK technique.", type: "cheatsheet" },
      { id: "th-r7", title: "MITRE ATT&CK Navigator", description: "Interactive tool for mapping and visualizing technique coverage during threat hunts.", type: "link", url: "https://mitre-attack.github.io/attack-navigator/" },
      { id: "th-r8", title: "ThreatHunter Playbook", description: "Open-source community-driven threat hunting playbook with Jupyter notebooks.", type: "link", url: "https://threathunterplaybook.com/" }
    ]
  },
  {
    id: "detection-engineering",
    title: "Detection Engineering Basics",
    shortTitle: "Detection Engineering",
    description: "Build custom detection rules and analytics. Master SIGMA rules, YARA signatures, and detection-as-code methodologies for modern SOC environments.",
    difficulty: "hard",
    duration: "16 hours",
    bgImage: "courses/detection-engineering-bg.jpg",
    quizzes: [
      { id: "de-q1", title: "Detection Fundamentals Quiz", description: "Test your understanding of detection philosophy, coverage models, and alert quality.", questionCount: 10, passingScore: 70, duration: "15 min", status: "unlocked" },
      { id: "de-q2", title: "SIGMA Rules Quiz", description: "Assess your knowledge of SIGMA syntax, modifiers, and rule conversion.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "de-q3", title: "YARA Signatures Quiz", description: "Quiz on YARA rule structure, pattern matching, and conditions.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "de-q4", title: "Log Source Mastery Quiz", description: "Test your knowledge of Windows, Linux, network, and cloud log sources.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "de-q5", title: "Detection-as-Code Quiz", description: "Assess your understanding of version control, CI/CD, and testing for detections.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "de-q6", title: "Detection Operations Quiz", description: "Quiz on tuning, metrics, coverage mapping, and detection lifecycle management.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" }
    ],
    modules: [
      {
        id: "1",
        title: "Detection Fundamentals",
        badge: "Core",
        badgeColor: "bg-primary/20 text-primary border-primary/30",
        quizId: "de-q1",
        lessons: [
          { id: "1.1", title: "Detection Philosophy & Mindset", description: "The art and science of building effective detections.", status: "unlocked" },
          { id: "1.2", title: "Detection Coverage Models", description: "Mapping and measuring your detection surface.", status: "locked" },
          { id: "1.3", title: "Alert Quality & False Positive Management", description: "Building high-fidelity alerts analysts trust.", status: "locked" },
          { id: "1.4", title: "The Detection Engineering Lifecycle", description: "From idea to production detection.", status: "locked" },
          { id: "1.5", title: "Module 1 Quiz: Detection Fundamentals", description: "Test your understanding of detection philosophy, coverage models, and alert quality.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "2",
        title: "SIGMA Rules",
        badge: "Lab",
        badgeColor: "bg-secondary/20 text-secondary border-secondary/30",
        quizId: "de-q2",
        lessons: [
          { id: "2.1", title: "SIGMA Syntax Deep Dive", description: "Master the generic detection rule format.", status: "locked" },
          { id: "2.2", title: "Writing Custom SIGMA Rules", description: "Craft rules from threat intelligence and hunt findings.", status: "locked" },
          { id: "2.3", title: "SIGMA Modifiers & Conditions", description: "Advanced logic, aggregation, and near-time correlation.", status: "locked" },
          { id: "2.4", title: "Rule Conversion & Backend Targets", description: "Convert SIGMA to Splunk SPL, Elastic KQL, and Sentinel.", status: "locked" },
          { id: "2.5", title: "Module 2 Quiz: SIGMA Rules", description: "Assess your knowledge of SIGMA syntax, modifiers, and rule conversion.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "3",
        title: "YARA Signatures",
        badge: "Lab",
        badgeColor: "bg-secondary/20 text-secondary border-secondary/30",
        quizId: "de-q3",
        lessons: [
          { id: "3.1", title: "YARA Rule Structure", description: "Meta, strings, and condition blocks.", status: "locked" },
          { id: "3.2", title: "Pattern Matching Techniques", description: "Text, hex, regex, and wildcard patterns.", status: "locked" },
          { id: "3.3", title: "Advanced YARA Conditions", description: "Modules, file size, entropy, and PE features.", status: "locked" },
          { id: "3.4", title: "YARA in Production", description: "Scanning at scale, performance, and integration.", status: "locked" },
          { id: "3.5", title: "Module 3 Quiz: YARA Signatures", description: "Quiz on YARA rule structure, pattern matching, and conditions.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "4",
        title: "Log Source Mastery",
        badge: "Core",
        badgeColor: "bg-primary/20 text-primary border-primary/30",
        quizId: "de-q4",
        lessons: [
          { id: "4.1", title: "Windows Event Log Deep Dive", description: "Critical event IDs, Sysmon, and audit policies.", status: "locked" },
          { id: "4.2", title: "Linux & Network Log Sources", description: "Auditd, syslog, Zeek, and firewall logs.", status: "locked" },
          { id: "4.3", title: "Cloud & Identity Log Sources", description: "CloudTrail, Azure AD, Okta, and SaaS logs.", status: "locked" },
          { id: "4.4", title: "Log Normalization & Enrichment", description: "CIM, ECS, and enrichment pipelines.", status: "locked" },
          { id: "4.5", title: "Module 4 Quiz: Log Source Mastery", description: "Test your knowledge of Windows, Linux, network, and cloud log sources.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "5",
        title: "Detection as Code",
        badge: "Lab",
        badgeColor: "bg-secondary/20 text-secondary border-secondary/30",
        quizId: "de-q5",
        lessons: [
          { id: "5.1", title: "Version Control for Detections", description: "Git workflows, branching, and review processes.", status: "locked" },
          { id: "5.2", title: "CI/CD Pipelines for Detection", description: "Automated testing, validation, and deployment.", status: "locked" },
          { id: "5.3", title: "Detection Testing Frameworks", description: "Unit testing, Atomic Red Team, and validation.", status: "locked" },
          { id: "5.4", title: "Infrastructure as Code for SIEM", description: "Terraform, Ansible, and repeatable deployments.", status: "locked" },
          { id: "5.5", title: "Module 5 Quiz: Detection as Code", description: "Assess your understanding of version control, CI/CD, and testing for detections.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "6",
        title: "Detection Operations",
        badge: "Quiz",
        badgeColor: "bg-orange-500/20 text-orange-400 border-orange-500/30",
        quizId: "de-q6",
        lessons: [
          { id: "6.1", title: "Detection Tuning & Optimization", description: "Reducing noise while maintaining coverage.", status: "locked" },
          { id: "6.2", title: "Detection Metrics & KPIs", description: "Measuring detection program effectiveness.", status: "locked" },
          { id: "6.3", title: "ATT&CK Coverage Mapping", description: "Visualizing and tracking detection coverage.", status: "locked" },
          { id: "6.4", title: "Detection Lifecycle Management", description: "Retirement, review cadence, and continuous improvement.", status: "locked" },
          { id: "6.5", title: "Module 6 Quiz: Detection Operations", description: "Quiz on tuning, metrics, coverage mapping, and detection lifecycle management.", duration: "15 min", status: "locked" }
        ]
      }
    ],
    resources: [
      { id: "de-r1", title: "SIGMA Rule Syntax Cheat Sheet", description: "Quick reference for SIGMA rule fields, modifiers, conditions, and log source mappings.", type: "cheatsheet" },
      { id: "de-r2", title: "YARA Rule Writing Guide", description: "Complete guide to YARA syntax including strings, conditions, modules, and performance tips.", type: "pdf" },
      { id: "de-r3", title: "Detection-as-Code Pipeline Template", description: "CI/CD pipeline configuration for automated detection testing and deployment.", type: "template" },
      { id: "de-r4", title: "ATT&CK Coverage Mapping Template", description: "Spreadsheet template for tracking detection coverage across ATT&CK techniques.", type: "template" },
      { id: "de-r5", title: "Detection Tuning Workflow", description: "Step-by-step process for tuning detections to reduce false positives while maintaining coverage.", type: "pdf" },
      { id: "de-r6", title: "Log Source Onboarding Checklist", description: "Checklist for integrating new log sources into your detection engineering pipeline.", type: "cheatsheet" },
      { id: "de-r7", title: "SigmaHQ Rule Repository", description: "Community-maintained repository of SIGMA detection rules for common threats.", type: "link", url: "https://github.com/SigmaHQ/sigma" },
      { id: "de-r8", title: "Atomic Red Team", description: "Library of small, portable detection tests mapped to MITRE ATT&CK techniques.", type: "link", url: "https://github.com/redcanaryco/atomic-red-team" }
    ]
  },
  {
    id: "malware-analysis",
    title: "Malware Analysis Fundamentals",
    shortTitle: "Malware Analysis",
    description: "Analyze malicious software safely. Learn static and dynamic analysis, sandboxing, and reverse engineering basics for security professionals.",
    difficulty: "hard",
    duration: "18 hours",
    bgImage: "courses/malware-analysis-bg.jpg",
    quizzes: [
      { id: "ma-q1", title: "Malware Landscape & Lab Setup Quiz", description: "Test your knowledge of malware categories and safe analysis environments.", questionCount: 10, passingScore: 70, duration: "15 min", status: "unlocked" },
      { id: "ma-q2", title: "Static Analysis Techniques Quiz", description: "Assess your understanding of file identification, strings, and PE analysis.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "ma-q3", title: "Dynamic & Behavioral Analysis Quiz", description: "Test your sandbox and runtime monitoring skills.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "ma-q4", title: "Document & Script Malware Quiz", description: "Evaluate your ability to analyze macro and script-based threats.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "ma-q5", title: "Reverse Engineering Fundamentals Quiz", description: "Test your knowledge of disassembly, debugging, and code analysis.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" },
      { id: "ma-q6", title: "Reporting & Threat Intel Quiz", description: "Assess your malware reporting and IOC extraction skills.", questionCount: 10, passingScore: 70, duration: "15 min", status: "locked" }
    ],
    modules: [
      {
        id: "1",
        title: "Malware Landscape & Lab Setup",
        quizId: "ma-q1",
        lessons: [
          { id: "1.1", title: "Malware Taxonomy", description: "Classify malware by behavior: viruses, worms, trojans, ransomware, rootkits, bootkits, and wipers.", duration: "20 min", status: "unlocked" },
          { id: "1.2", title: "Threat Actor Motivations", description: "Understand financially-motivated, state-sponsored, hacktivist, and insider threat malware campaigns.", duration: "15 min", status: "locked" },
          { id: "1.3", title: "Building a Safe Analysis Lab", description: "Configure isolated VMs with FlareVM, REMnux, and network segmentation for safe malware handling.", duration: "25 min", status: "locked" },
          { id: "1.4", title: "Sample Acquisition & Handling", description: "Source malware samples from MalwareBazaar, VirusTotal, and malware zoos while maintaining chain of custody.", duration: "20 min", status: "locked" },
          { id: "1.5", title: "Module 1 Quiz: Malware Landscape & Lab Setup", description: "Test your knowledge of malware categories and safe analysis environments.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "2",
        title: "Static Analysis Techniques",
        quizId: "ma-q2",
        lessons: [
          { id: "2.1", title: "File Identification & Hashing", description: "Use file, TrID, ssdeep fuzzy hashing, and imphash to identify and classify unknown binaries.", duration: "20 min", status: "locked" },
          { id: "2.2", title: "String Extraction & Analysis", description: "Extract readable strings with FLOSS, decode obfuscated strings, and identify IOCs from string output.", duration: "20 min", status: "locked" },
          { id: "2.3", title: "PE Header Deep Dive", description: "Parse PE structures with PE-bear and pefile: sections, imports, exports, timestamps, and anomalies.", duration: "25 min", status: "locked" },
          { id: "2.4", title: "Packing & Obfuscation Detection", description: "Detect UPX, Themida, and custom packers using entropy analysis, section names, and Detect It Easy.", duration: "20 min", status: "locked" },
          { id: "2.5", title: "Module 2 Quiz: Static Analysis Techniques", description: "Assess your understanding of file identification, strings, and PE analysis.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "3",
        title: "Dynamic & Behavioral Analysis",
        quizId: "ma-q3",
        lessons: [
          { id: "3.1", title: "Sandbox Fundamentals", description: "Configure and use ANY.RUN, Cuckoo Sandbox, and Joe Sandbox for automated behavioral analysis.", duration: "25 min", status: "locked" },
          { id: "3.2", title: "Process & Registry Monitoring", description: "Use Process Monitor, Process Hacker, and Regshot to capture runtime filesystem and registry changes.", duration: "20 min", status: "locked" },
          { id: "3.3", title: "Network Traffic Capture", description: "Intercept malware C2 with FakeNet-NG, INetSim, and Wireshark to decode protocols and extract payloads.", duration: "25 min", status: "locked" },
          { id: "3.4", title: "API Call Tracing", description: "Trace Win32 API calls with API Monitor and x64dbg to understand malware behavior at the system level.", duration: "20 min", status: "locked" },
          { id: "3.5", title: "Module 3 Quiz: Dynamic & Behavioral Analysis", description: "Test your sandbox and runtime monitoring skills.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "4",
        title: "Document & Script Malware",
        quizId: "ma-q4",
        lessons: [
          { id: "4.1", title: "Office Macro Analysis", description: "Extract and deobfuscate VBA macros from Office documents using olevba, oletools, and ViperMonkey.", duration: "25 min", status: "locked" },
          { id: "4.2", title: "PDF Malware Analysis", description: "Parse malicious PDFs with pdf-parser, peepdf, and identify JavaScript, launch actions, and embedded objects.", duration: "20 min", status: "locked" },
          { id: "4.3", title: "PowerShell & Script Deobfuscation", description: "Decode Base64, character substitution, and invoke-expression chains in PowerShell, VBScript, and JScript.", duration: "25 min", status: "locked" },
          { id: "4.4", title: "HTML Smuggling & LNK Files", description: "Analyze HTML smuggling payloads and malicious shortcut files used in modern phishing campaigns.", duration: "20 min", status: "locked" },
          { id: "4.5", title: "Module 4 Quiz: Document & Script Malware", description: "Evaluate your ability to analyze macro and script-based threats.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "5",
        title: "Reverse Engineering Fundamentals",
        quizId: "ma-q5",
        lessons: [
          { id: "5.1", title: "x86 Assembly Essentials", description: "Learn registers, instructions, calling conventions, and stack frames needed for binary analysis.", duration: "30 min", status: "locked" },
          { id: "5.2", title: "Ghidra for Malware Analysis", description: "Navigate Ghidra's decompiler, cross-references, function graphs, and scripting for malware RE.", duration: "25 min", status: "locked" },
          { id: "5.3", title: "Debugging with x64dbg", description: "Set breakpoints, trace execution, defeat anti-debugging tricks, and unpack samples with x64dbg.", duration: "25 min", status: "locked" },
          { id: "5.4", title: "Identifying C2 Protocols", description: "Reverse engineer custom C2 communication: XOR encryption, domain generation algorithms, and protocol parsing.", duration: "25 min", status: "locked" },
          { id: "5.5", title: "Module 5 Quiz: Reverse Engineering Fundamentals", description: "Test your knowledge of disassembly, debugging, and code analysis.", duration: "15 min", status: "locked" }
        ]
      },
      {
        id: "6",
        title: "Reporting & Threat Intelligence",
        quizId: "ma-q6",
        lessons: [
          { id: "6.1", title: "IOC Extraction & STIX/TAXII", description: "Extract indicators of compromise and format them using STIX 2.1 for automated threat intelligence sharing.", duration: "20 min", status: "locked" },
          { id: "6.2", title: "YARA Rule Creation", description: "Write effective YARA rules from malware artifacts: strings, byte patterns, PE features, and conditions.", duration: "25 min", status: "locked" },
          { id: "6.3", title: "Writing Malware Analysis Reports", description: "Structure professional reports with executive summary, technical details, IOCs, and MITRE ATT&CK mapping.", duration: "20 min", status: "locked" },
          { id: "6.4", title: "Attribution & Campaign Tracking", description: "Link samples to threat actors using infrastructure overlaps, code reuse, and TTPs for campaign tracking.", duration: "20 min", status: "locked" },
          { id: "6.5", title: "Module 6 Quiz: Reporting & Threat Intel", description: "Assess your malware reporting and IOC extraction skills.", duration: "15 min", status: "locked" }
        ]
      }
    ],
    resources: [
      { id: "ma-r1", title: "Malware Analysis Lab Setup Guide", description: "Complete guide to building isolated analysis environments with FlareVM and REMnux.", type: "pdf" },
      { id: "ma-r2", title: "PE File Format Reference", description: "Detailed reference for the Portable Executable format including headers, sections, and imports.", type: "cheatsheet" },
      { id: "ma-r3", title: "x86 Assembly Quick Reference", description: "Essential x86 instructions, registers, calling conventions, and common patterns in malware.", type: "cheatsheet" },
      { id: "ma-r4", title: "YARA Rule Templates for Malware", description: "Pre-built YARA rule templates for common malware families and behaviors.", type: "template" },
      { id: "ma-r5", title: "Dynamic Analysis Checklist", description: "Step-by-step checklist for sandbox setup, monitoring tools, and behavioral observation.", type: "cheatsheet" },
      { id: "ma-r6", title: "Malware Report Template", description: "Professional report template with IOC tables, MITRE mapping, and executive summary sections.", type: "template" },
      { id: "ma-r7", title: "MalwareBazaar", description: "Free malware sample repository for research and analysis practice.", type: "link", url: "https://bazaar.abuse.ch/" },
      { id: "ma-r8", title: "Any.Run Interactive Sandbox", description: "Interactive online malware analysis sandbox with real-time monitoring.", type: "link", url: "https://any.run/" }
    ]
  },
  {
    id: "soc-analyst-path",
    title: "SOC Analyst Learning Path",
    shortTitle: "SOC Analyst Path",
    description: "A structured career-ready program covering everything from foundational SOC skills to advanced threat analysis, incident handling, and reporting. Designed to prepare you for real-world SOC analyst roles.",
    difficulty: "medium",
    duration: "40 hours",
    bgImage: "courses/soc-analyst-path-bg.jpg",
    modules: [
      {
        id: "1",
        title: "SOC Analyst Role & Environment",
        quizId: "sap-q1",
        lessons: [
          { id: "1.1", title: "Day in the Life of a SOC Analyst", description: "Walk through a typical shift including alert triage, escalation, documentation, and shift handover.", duration: "20 min", status: "completed" },
          { id: "1.2", title: "SOC Maturity Models", description: "Understand SOC maturity levels from reactive to proactive and how organizations evolve their security operations.", duration: "25 min", status: "unlocked" },
          { id: "1.3", title: "Compliance & Regulatory Frameworks", description: "Overview of PCI-DSS, HIPAA, GDPR, and SOX requirements relevant to SOC operations.", duration: "20 min", status: "locked" },
          { id: "1.4", title: "Building Your Analyst Toolkit", description: "Set up your personal investigation toolkit with essential free and commercial tools.", duration: "30 min", status: "locked" },
          { id: "1.5", title: "SOC Communication & Stakeholder Management", description: "Learn to communicate effectively with IT teams, management, and external parties during incidents.", duration: "20 min", status: "locked" },
          { id: "1.6", title: "Metrics, KPIs & Reporting for SOC Teams", description: "Track and present SOC performance using MTTD, MTTR, alert volume, and efficiency metrics.", duration: "25 min", status: "locked" },
          { id: "1.7", title: "Module 1 Quiz: SOC Analyst Role & Environment", description: "Test your understanding of SOC operations, maturity models, and compliance frameworks.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "2",
        title: "Network Traffic Analysis",
        quizId: "sap-q2",
        lessons: [
          { id: "2.1", title: "TCP/IP Deep Dive for Analysts", description: "Master TCP flags, handshakes, sessions, and how attackers abuse protocol behavior.", duration: "30 min", status: "locked" },
          { id: "2.2", title: "DNS Analysis & Threat Detection", description: "Detect DNS tunneling, DGA domains, fast-flux networks, and DNS-based C2 channels.", duration: "25 min", status: "locked" },
          { id: "2.3", title: "HTTP/HTTPS Traffic Investigation", description: "Analyze web traffic for malicious payloads, beaconing patterns, and data exfiltration.", duration: "30 min", status: "locked" },
          { id: "2.4", title: "Wireshark for SOC Analysts", description: "Practical packet capture analysis using display filters, stream following, and expert info.", duration: "35 min", status: "locked" },
          { id: "2.5", title: "TLS/SSL Interception & Analysis", description: "Understand TLS handshakes, certificate validation, and how to analyze encrypted traffic.", duration: "25 min", status: "locked" },
          { id: "2.6", title: "Network Flow Analysis with Zeek", description: "Use Zeek (Bro) for connection logs, protocol analysis, and behavioral network monitoring.", duration: "30 min", status: "locked" },
          { id: "2.7", title: "Module 2 Quiz: Network Traffic Analysis", description: "Evaluate your skills in TCP/IP analysis, DNS threats, and packet inspection.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "3",
        title: "SIEM Mastery",
        quizId: "sap-q3",
        lessons: [
          { id: "3.1", title: "Advanced SIEM Queries", description: "Write complex search queries using regex, subsearches, lookups, and statistical functions.", duration: "35 min", status: "locked" },
          { id: "3.2", title: "Correlation Rule Development", description: "Design multi-event correlation rules to detect attack chains and reduce false positives.", duration: "30 min", status: "locked" },
          { id: "3.3", title: "Dashboard Creation & Visualization", description: "Build actionable SOC dashboards that surface critical alerts and trends.", duration: "25 min", status: "locked" },
          { id: "3.4", title: "Log Source Onboarding", description: "Integrate new data sources, normalize fields, and validate event parsing.", duration: "25 min", status: "locked" },
          { id: "3.5", title: "Alert Tuning & False Positive Reduction", description: "Systematically reduce noise by tuning thresholds, whitelisting, and enrichment-based suppression.", duration: "25 min", status: "locked" },
          { id: "3.6", title: "SIEM Use Case Development", description: "Design detection use cases from threat model to implementation and validation.", duration: "30 min", status: "locked" },
          { id: "3.7", title: "Module 3 Quiz: SIEM Mastery", description: "Test your SIEM query writing, correlation rules, and dashboard skills.", duration: "25 min", status: "locked" }
        ]
      },
      {
        id: "4",
        title: "Endpoint Investigation",
        quizId: "sap-q4",
        lessons: [
          { id: "4.1", title: "Process Forensics on Windows", description: "Analyze running processes, DLL injection, process hollowing, and living-off-the-land binaries.", duration: "30 min", status: "locked" },
          { id: "4.2", title: "Registry & Persistence Analysis", description: "Identify persistence mechanisms via Run keys, scheduled tasks, services, and WMI subscriptions.", duration: "25 min", status: "locked" },
          { id: "4.3", title: "Linux Endpoint Forensics", description: "Investigate suspicious processes, network connections, cron jobs, and shell history on Linux.", duration: "25 min", status: "locked" },
          { id: "4.4", title: "Memory Analysis Fundamentals", description: "Use Volatility to analyze memory dumps for hidden processes, injected code, and network artifacts.", duration: "35 min", status: "locked" },
          { id: "4.5", title: "Browser Forensics & Web Artifacts", description: "Extract browsing history, cached files, cookies, and download records for investigation.", duration: "25 min", status: "locked" },
          { id: "4.6", title: "PowerShell & Script Block Logging", description: "Detect malicious PowerShell usage through script block logging, transcription, and AMSI.", duration: "30 min", status: "locked" },
          { id: "4.7", title: "Module 4 Quiz: Endpoint Investigation", description: "Assess your endpoint forensics knowledge on Windows and Linux systems.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "5",
        title: "Phishing & Email Analysis",
        quizId: "sap-q5",
        lessons: [
          { id: "5.1", title: "Email Header Analysis", description: "Parse email headers to trace message origin, identify spoofing, and verify SPF/DKIM/DMARC.", duration: "25 min", status: "locked" },
          { id: "5.2", title: "Malicious Attachment Analysis", description: "Safely examine Office macros, PDFs, ISO files, and archive-based payloads.", duration: "30 min", status: "locked" },
          { id: "5.3", title: "URL & Domain Investigation", description: "Investigate suspicious links using URLScan, VirusTotal, WHOIS, and passive DNS.", duration: "25 min", status: "locked" },
          { id: "5.4", title: "Phishing Response Playbook", description: "End-to-end phishing incident handling: detection, containment, eradication, and reporting.", duration: "30 min", status: "locked" },
          { id: "5.5", title: "Business Email Compromise Detection", description: "Identify BEC patterns including CEO fraud, vendor impersonation, and invoice redirection.", duration: "25 min", status: "locked" },
          { id: "5.6", title: "Email Security Architecture", description: "Configure and evaluate SPF, DKIM, DMARC, email gateways, and sandboxing solutions.", duration: "30 min", status: "locked" },
          { id: "5.7", title: "Module 5 Quiz: Phishing & Email Analysis", description: "Validate your email header analysis and phishing response skills.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "6",
        title: "Incident Handling & Reporting",
        quizId: "sap-q6",
        lessons: [
          { id: "6.1", title: "Incident Severity Classification", description: "Apply consistent severity scoring using asset criticality, impact, and threat intelligence context.", duration: "20 min", status: "locked" },
          { id: "6.2", title: "Evidence Collection & Chain of Custody", description: "Preserve digital evidence with proper hashing, storage, and documentation for legal admissibility.", duration: "25 min", status: "locked" },
          { id: "6.3", title: "Writing Effective Incident Reports", description: "Structure professional reports with executive summary, timeline, technical findings, and recommendations.", duration: "25 min", status: "locked" },
          { id: "6.4", title: "Post-Incident Review & Lessons Learned", description: "Conduct blameless retrospectives to improve detection, response, and prevention capabilities.", duration: "20 min", status: "locked" },
          { id: "6.5", title: "Tabletop Exercises & Simulation", description: "Plan and conduct incident response tabletop exercises to test team readiness.", duration: "25 min", status: "locked" },
          { id: "6.6", title: "Building Runbooks & Automation", description: "Create standardized runbooks and automate repetitive response actions with SOAR.", duration: "30 min", status: "locked" },
          { id: "6.7", title: "Module 6 Quiz: Incident Handling & Reporting", description: "Comprehensive exam covering incident handling, reporting, and evidence management.", duration: "35 min", status: "locked" }
        ]
      },
      {
        id: "7",
        title: "Cloud Security Monitoring",
        quizId: "sap-q7",
        lessons: [
          { id: "7.1", title: "Cloud Security Fundamentals for SOC", description: "Understand shared responsibility, cloud service models, and security implications for monitoring.", duration: "25 min", status: "locked" },
          { id: "7.2", title: "AWS CloudTrail & GuardDuty Analysis", description: "Investigate AWS API activity, detect unauthorized access, and analyze GuardDuty findings.", duration: "30 min", status: "locked" },
          { id: "7.3", title: "Azure & Microsoft 365 Security Monitoring", description: "Monitor Azure AD sign-ins, Defender alerts, and Microsoft 365 audit logs.", duration: "30 min", status: "locked" },
          { id: "7.4", title: "Container & Kubernetes Security", description: "Detect threats in containerized environments including image scanning and runtime monitoring.", duration: "30 min", status: "locked" },
          { id: "7.5", title: "GCP Security Command Center & Logging", description: "Analyze Google Cloud audit logs, Security Command Center findings, and IAM anomalies.", duration: "25 min", status: "locked" },
          { id: "7.6", title: "Cloud SIEM Integration & Multi-Cloud Monitoring", description: "Centralize cloud logs into SIEM platforms and build detection rules across multi-cloud environments.", duration: "30 min", status: "locked" },
          { id: "7.7", title: "Module 7 Quiz: Cloud Security Monitoring", description: "Test your cloud security knowledge across AWS, Azure, and container environments.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "8",
        title: "Threat Intelligence & Hunting",
        quizId: "sap-q8",
        lessons: [
          { id: "8.1", title: "Threat Intelligence Lifecycle", description: "Plan, collect, process, analyze, and disseminate actionable threat intelligence.", duration: "25 min", status: "locked" },
          { id: "8.2", title: "Building IOC Feeds & STIX/TAXII", description: "Create and consume threat intelligence feeds using STIX format and TAXII protocols.", duration: "30 min", status: "locked" },
          { id: "8.3", title: "Hypothesis-Driven Threat Hunting", description: "Develop hunting hypotheses from ATT&CK techniques and execute structured hunts.", duration: "35 min", status: "locked" },
          { id: "8.4", title: "Hunting with Data Analytics", description: "Apply statistical analysis, frequency analysis, and anomaly detection to find hidden threats.", duration: "30 min", status: "locked" },
          { id: "8.5", title: "MITRE ATT&CK for Threat Hunting", description: "Map adversary techniques to ATT&CK framework and develop detection coverage matrices.", duration: "30 min", status: "locked" },
          { id: "8.6", title: "Threat Actor Profiling & Campaign Tracking", description: "Track APT groups, attribute campaigns, and build threat actor profiles using diamond model.", duration: "25 min", status: "locked" },
          { id: "8.7", title: "Module 8 Quiz: Threat Intelligence & Hunting", description: "Assess threat intel lifecycle, IOC management, and hunting methodology skills.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "9",
        title: "Digital Forensics Fundamentals",
        quizId: "sap-q9",
        lessons: [
          { id: "9.1", title: "Digital Forensics Methodology", description: "Follow forensic methodology: identification, preservation, analysis, and presentation.", duration: "25 min", status: "locked" },
          { id: "9.2", title: "Disk Imaging & File System Analysis", description: "Create forensic images and analyze NTFS, ext4, and FAT file systems for evidence.", duration: "30 min", status: "locked" },
          { id: "9.3", title: "Timeline Analysis & Super Timeline", description: "Build comprehensive timelines from multiple artifact sources using log2timeline/plaso.", duration: "35 min", status: "locked" },
          { id: "9.4", title: "Anti-Forensics & Evidence Destruction", description: "Detect timestomping, log clearing, secure deletion, and other anti-forensic techniques.", duration: "25 min", status: "locked" },
          { id: "9.5", title: "Mobile Device Forensics", description: "Extract and analyze evidence from iOS and Android devices including app data and communications.", duration: "30 min", status: "locked" },
          { id: "9.6", title: "Forensic Report Writing & Court Presentation", description: "Prepare legally admissible forensic reports and understand expert witness responsibilities.", duration: "25 min", status: "locked" },
          { id: "9.7", title: "Module 9 Quiz: Digital Forensics Fundamentals", description: "Evaluate disk forensics, timeline analysis, and anti-forensics detection skills.", duration: "25 min", status: "locked" }
        ]
      },
      {
        id: "10",
        title: "Security Automation & SOAR",
        quizId: "sap-q10",
        lessons: [
          { id: "10.1", title: "Introduction to SOAR Platforms", description: "Understand SOAR architecture, orchestration vs automation, and selecting the right platform.", duration: "25 min", status: "locked" },
          { id: "10.2", title: "Building Automated Playbooks", description: "Design and implement automated response playbooks for common alert types like phishing and malware.", duration: "30 min", status: "locked" },
          { id: "10.3", title: "API Integration for Security Tools", description: "Connect security tools via REST APIs for automated enrichment, blocking, and ticketing.", duration: "30 min", status: "locked" },
          { id: "10.4", title: "Python Scripting for SOC Analysts", description: "Write Python scripts for log parsing, IOC extraction, and automated investigation workflows.", duration: "35 min", status: "locked" },
          { id: "10.5", title: "Chatbot & Notification Automation", description: "Build Slack/Teams integrations for alert notifications and interactive response commands.", duration: "25 min", status: "locked" },
          { id: "10.6", title: "Measuring Automation ROI & Metrics", description: "Track automation effectiveness using time saved, MTTR reduction, and analyst satisfaction metrics.", duration: "20 min", status: "locked" },
          { id: "10.7", title: "Module 10 Quiz: Security Automation & SOAR", description: "Test your SOAR platform knowledge, playbook design, and API integration skills.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "11",
        title: "Vulnerability Management",
        quizId: "sap-q11",
        lessons: [
          { id: "11.1", title: "Vulnerability Management Lifecycle", description: "Plan, scan, assess, remediate, and verify \u2014 the complete VM lifecycle for SOC teams.", duration: "25 min", status: "locked" },
          { id: "11.2", title: "Scanning Tools: Nessus, Qualys & OpenVAS", description: "Configure and run vulnerability scans using industry-standard tools and interpret results.", duration: "30 min", status: "locked" },
          { id: "11.3", title: "CVSS Scoring & Risk Prioritization", description: "Calculate CVSS scores, understand exploit prediction scoring, and prioritize remediation.", duration: "25 min", status: "locked" },
          { id: "11.4", title: "Patch Management & Remediation Workflows", description: "Coordinate patching across IT teams with SLAs, exceptions, and change management.", duration: "25 min", status: "locked" },
          { id: "11.5", title: "Attack Surface Management", description: "Discover and monitor external-facing assets, shadow IT, and third-party exposure.", duration: "25 min", status: "locked" },
          { id: "11.6", title: "Vulnerability Reporting & Stakeholder Communication", description: "Create executive dashboards, trend reports, and communicate risk to non-technical stakeholders.", duration: "20 min", status: "locked" },
          { id: "11.7", title: "Module 11 Quiz: Vulnerability Management", description: "Assess vulnerability scanning, CVSS scoring, and remediation workflow knowledge.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "12",
        title: "Advanced Attack Techniques",
        quizId: "sap-q12",
        lessons: [
          { id: "12.1", title: "Active Directory Attacks & Defense", description: "Detect Kerberoasting, Pass-the-Hash, DCSync, and Golden Ticket attacks in AD environments.", duration: "35 min", status: "locked" },
          { id: "12.2", title: "Lateral Movement Detection", description: "Identify lateral movement via PsExec, WMI, RDP, and SMB using log analysis and EDR.", duration: "30 min", status: "locked" },
          { id: "12.3", title: "Ransomware Analysis & Response", description: "Understand ransomware kill chains, detect pre-encryption behavior, and execute containment.", duration: "30 min", status: "locked" },
          { id: "12.4", title: "Supply Chain Attack Detection", description: "Detect software supply chain compromises, dependency confusion, and trojanized updates.", duration: "25 min", status: "locked" },
          { id: "12.5", title: "Zero-Day & Exploit Detection", description: "Identify exploitation attempts through behavioral analysis, exploit guard alerts, and anomaly detection.", duration: "30 min", status: "locked" },
          { id: "12.6", title: "Red Team vs Blue Team Exercises", description: "Plan and participate in purple team exercises to validate detections and improve SOC capabilities.", duration: "30 min", status: "locked" },
          { id: "12.7", title: "Final Assessment Quiz: SOC Analyst Learning Path", description: "A comprehensive, medium-difficulty final assessment covering all 12 modules of the course.", duration: "45 min", status: "locked" }
        ]
      }
    ],
    quizzes: [
      { id: "sap-q1", title: "SOC Analyst Foundations Quiz", description: "Test your understanding of the SOC analyst role, maturity models, and compliance frameworks.", questionCount: 15, passingScore: 70, duration: "20 min", status: "unlocked" },
      { id: "sap-q2", title: "Network Traffic Analysis Quiz", description: "Evaluate your skills in TCP/IP analysis, DNS threats, and packet inspection.", questionCount: 15, passingScore: 75, duration: "20 min", status: "locked" },
      { id: "sap-q3", title: "SIEM Mastery Assessment", description: "Test your SIEM query writing, correlation rules, and dashboard skills.", questionCount: 15, passingScore: 75, duration: "25 min", status: "locked" },
      { id: "sap-q4", title: "Endpoint Investigation Quiz", description: "Assess your endpoint forensics knowledge on Windows and Linux systems.", questionCount: 15, passingScore: 70, duration: "20 min", status: "locked" },
      { id: "sap-q5", title: "Phishing & Email Analysis Quiz", description: "Validate your email header analysis and phishing response skills.", questionCount: 15, passingScore: 75, duration: "20 min", status: "locked" },
      { id: "sap-q6", title: "Incident Handling Final Exam", description: "Comprehensive exam covering incident handling, reporting, and evidence management.", questionCount: 25, passingScore: 80, duration: "35 min", status: "locked" },
      { id: "sap-q7", title: "Cloud Security Monitoring Quiz", description: "Test your cloud security knowledge across AWS, Azure, and container environments.", questionCount: 15, passingScore: 75, duration: "20 min", status: "locked" },
      { id: "sap-q8", title: "Threat Intelligence & Hunting Quiz", description: "Assess threat intel lifecycle, IOC management, and hunting methodology skills.", questionCount: 15, passingScore: 75, duration: "20 min", status: "locked" },
      { id: "sap-q9", title: "Digital Forensics Assessment", description: "Evaluate disk forensics, timeline analysis, and anti-forensics detection skills.", questionCount: 15, passingScore: 75, duration: "25 min", status: "locked" },
      { id: "sap-q10", title: "Security Automation & SOAR Quiz", description: "Test your SOAR platform knowledge, playbook design, and API integration skills.", questionCount: 15, passingScore: 75, duration: "20 min", status: "locked" },
      { id: "sap-q11", title: "Vulnerability Management Quiz", description: "Assess vulnerability scanning, CVSS scoring, and remediation workflow knowledge.", questionCount: 15, passingScore: 75, duration: "20 min", status: "locked" },
      { id: "sap-q12", title: "SOC Analyst Final Assessment", description: "A comprehensive, medium-difficulty final assessment covering all 12 modules of the SOC Analyst Learning Path.", questionCount: 36, passingScore: 75, duration: "45 min", status: "locked" },
      { id: "sap-q13", title: "SOC Analyst Certification Exam", description: "Comprehensive final exam covering all 12 modules. Pass with 80% or higher to earn your SOC Analyst Learning Path certificate.", questionCount: 30, passingScore: 80, duration: "60 min", status: "locked" }
    ],
    resources: [
      { id: "sap-r1", title: "SOC Analyst Investigation Playbook", description: "Step-by-step investigation guides for common alert types and scenarios.", type: "template" },
      { id: "sap-r2", title: "Network Protocol Cheat Sheet", description: "Quick reference for TCP flags, HTTP methods, DNS record types, and common ports.", type: "cheatsheet" },
      { id: "sap-r3", title: "SIEM Query Reference Guide", description: "Common search patterns, regex examples, and statistical queries for SOC investigations.", type: "cheatsheet" },
      { id: "sap-r4", title: "Windows Forensics Quick Reference", description: "Key registry paths, event IDs, persistence locations, and artifact locations.", type: "cheatsheet" },
      { id: "sap-r5", title: "Email Analysis Toolkit Guide", description: "Tools and techniques for dissecting suspicious emails and extracting IOCs.", type: "pdf" },
      { id: "sap-r6", title: "Incident Report Template", description: "Professional incident report template with sections for timeline, impact, and remediation.", type: "template" },
      { id: "sap-r7", title: "CyberChef", description: "Web-based tool for encoding, decoding, and data transformation during investigations.", type: "link", url: "https://gchq.github.io/CyberChef/" },
      { id: "sap-r8", title: "URLScan.io", description: "Free service for scanning and analyzing suspicious URLs and websites.", type: "link", url: "https://urlscan.io/" },
      { id: "sap-r9", title: "SOAR Playbook Templates", description: "Ready-to-use automation playbook templates for phishing, malware, and access violations.", type: "template" },
      { id: "sap-r10", title: "MITRE ATT&CK Navigator", description: "Interactive tool for mapping detection coverage against the ATT&CK framework.", type: "link", url: "https://mitre-attack.github.io/attack-navigator/" }
    ]
  },
  {
    id: "network-fundamentals",
    title: "Network Fundamentals",
    shortTitle: "Net Basics",
    description: "Master the foundations of computer networking \u2014 from the OSI model and TCP/IP to subnetting, routing, switching, DNS, DHCP, wireless, and network troubleshooting. Essential knowledge for any cybersecurity professional.",
    difficulty: "easy",
    duration: "16 hours",
    bgImage: "courses/network-fundamentals-bg.jpg",
    modules: [
      {
        id: "nf-1",
        title: "Introduction to Computer Networks",
        quizId: "nf-q1",
        lessons: [
          { id: "nf-1.1", title: "What is a Computer Network?", description: "Understanding networks, their purpose, and how devices communicate.", duration: "20 min", status: "unlocked" },
          { id: "nf-1.2", title: "Types of Networks: LAN, WAN, MAN & More", description: "Explore LAN, WAN, MAN, PAN, CAN, and their characteristics.", duration: "25 min", status: "locked" },
          { id: "nf-1.3", title: "Network Topologies", description: "Star, bus, ring, mesh, and hybrid topologies \u2014 advantages and use cases.", duration: "20 min", status: "locked" },
          { id: "nf-1.4", title: "Network Architecture: Client-Server vs Peer-to-Peer", description: "Comparing centralized and decentralized network models.", duration: "15 min", status: "locked" },
          { id: "nf-q1", title: "Module 1 Quiz: Computer Networks Basics", description: "Test your knowledge of network types, topologies, and architecture.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "nf-2",
        title: "The OSI Model",
        quizId: "nf-q2",
        lessons: [
          { id: "nf-2.1", title: "Understanding the OSI Reference Model", description: "The 7-layer model and why it matters for networking and security.", duration: "25 min", status: "locked" },
          { id: "nf-2.2", title: "Physical & Data Link Layers (Layers 1-2)", description: "Cables, signals, MAC addresses, switches, and Ethernet framing.", duration: "30 min", status: "locked" },
          { id: "nf-2.3", title: "Network & Transport Layers (Layers 3-4)", description: "IP addressing, routing, TCP, UDP, and port numbers.", duration: "30 min", status: "locked" },
          { id: "nf-2.4", title: "Session, Presentation & Application Layers (Layers 5-7)", description: "Session management, data formatting, encryption, and application protocols.", duration: "25 min", status: "locked" },
          { id: "nf-2.5", title: "Data Encapsulation & PDUs", description: "How data is encapsulated at each layer: bits, frames, packets, segments, and data.", duration: "20 min", status: "locked" },
          { id: "nf-q2", title: "Module 2 Quiz: OSI Model", description: "Assess your understanding of the 7-layer OSI model and data encapsulation.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "nf-3",
        title: "TCP/IP Protocol Suite",
        quizId: "nf-q3",
        lessons: [
          { id: "nf-3.1", title: "TCP/IP Model vs OSI Model", description: "The 4-layer TCP/IP model and how it maps to the OSI model.", duration: "20 min", status: "locked" },
          { id: "nf-3.2", title: "TCP: Connection-Oriented Communication", description: "Three-way handshake, sequence numbers, flow control, and reliability.", duration: "30 min", status: "locked" },
          { id: "nf-3.3", title: "UDP: Connectionless Communication", description: "When speed matters more than reliability \u2014 use cases and header format.", duration: "20 min", status: "locked" },
          { id: "nf-3.4", title: "ICMP & ARP Protocols", description: "Ping, traceroute, ARP resolution, and their role in network communication.", duration: "25 min", status: "locked" },
          { id: "nf-3.5", title: "Ports & Sockets", description: "Well-known ports, registered ports, ephemeral ports, and socket communication.", duration: "20 min", status: "locked" },
          { id: "nf-q3", title: "Module 3 Quiz: TCP/IP Protocol Suite", description: "Test your knowledge of TCP, UDP, ICMP, ARP, and port numbers.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "nf-4",
        title: "IP Addressing & Subnetting",
        quizId: "nf-q4",
        lessons: [
          { id: "nf-4.1", title: "IPv4 Addressing Fundamentals", description: "Binary conversion, address classes, and the structure of IPv4 addresses.", duration: "30 min", status: "locked" },
          { id: "nf-4.2", title: "Subnet Masks & CIDR Notation", description: "Understanding subnet masks, CIDR, and how they define network boundaries.", duration: "35 min", status: "locked" },
          { id: "nf-4.3", title: "Subnetting Practice", description: "Step-by-step subnetting calculations \u2014 network ID, broadcast, usable hosts.", duration: "40 min", status: "locked" },
          { id: "nf-4.4", title: "Private vs Public IP Addresses & NAT", description: "RFC 1918 ranges, NAT, PAT, and how private networks access the internet.", duration: "25 min", status: "locked" },
          { id: "nf-4.5", title: "IPv6 Fundamentals", description: "IPv6 address format, types, transition mechanisms, and dual-stack.", duration: "25 min", status: "locked" },
          { id: "nf-q4", title: "Module 4 Quiz: IP Addressing & Subnetting", description: "Validate your subnetting skills and IPv4/IPv6 knowledge.", duration: "25 min", status: "locked" }
        ]
      },
      {
        id: "nf-5",
        title: "Network Devices & Infrastructure",
        quizId: "nf-q5",
        lessons: [
          { id: "nf-5.1", title: "Hubs, Switches & Bridges", description: "Layer 2 devices \u2014 how switches learn MAC addresses and forward frames.", duration: "25 min", status: "locked" },
          { id: "nf-5.2", title: "Routers & Routing Basics", description: "How routers forward packets, routing tables, static vs dynamic routing.", duration: "30 min", status: "locked" },
          { id: "nf-5.3", title: "Firewalls, Proxies & Load Balancers", description: "Packet filtering, stateful inspection, reverse proxies, and traffic distribution.", duration: "25 min", status: "locked" },
          { id: "nf-5.4", title: "Access Points & Network Controllers", description: "Wireless access points, WLAN controllers, and network management.", duration: "20 min", status: "locked" },
          { id: "nf-5.5", title: "VLANs & Network Segmentation", description: "Virtual LANs, trunking (802.1Q), and why segmentation improves security.", duration: "25 min", status: "locked" },
          { id: "nf-q5", title: "Module 5 Quiz: Network Devices", description: "Test your understanding of switches, routers, firewalls, and VLANs.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "nf-6",
        title: "Application Layer Protocols",
        quizId: "nf-q6",
        lessons: [
          { id: "nf-6.1", title: "DNS: Domain Name System", description: "DNS hierarchy, record types (A, AAAA, MX, CNAME, TXT), and query process.", duration: "30 min", status: "locked" },
          { id: "nf-6.2", title: "DHCP: Dynamic Host Configuration", description: "DORA process, lease management, scopes, and DHCP relay.", duration: "25 min", status: "locked" },
          { id: "nf-6.3", title: "HTTP & HTTPS", description: "Request/response model, methods, status codes, TLS/SSL, and certificates.", duration: "30 min", status: "locked" },
          { id: "nf-6.4", title: "Email Protocols: SMTP, POP3, IMAP", description: "How email works end-to-end \u2014 sending, receiving, and storage.", duration: "25 min", status: "locked" },
          { id: "nf-6.5", title: "FTP, SSH, Telnet & Other Protocols", description: "File transfer, remote access protocols, and their security implications.", duration: "20 min", status: "locked" },
          { id: "nf-q6", title: "Module 6 Quiz: Application Protocols", description: "Assess your knowledge of DNS, DHCP, HTTP, email, and file transfer protocols.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "nf-7",
        title: "Ethernet & Data Link Technologies",
        quizId: "nf-q7",
        lessons: [
          { id: "nf-7.1", title: "Ethernet Standards & Cabling", description: "Cat5e, Cat6, fiber optics, cable types, and Ethernet standards (10/100/1G/10G).", duration: "25 min", status: "locked" },
          { id: "nf-7.2", title: "MAC Addresses & Ethernet Framing", description: "MAC address format, OUI, broadcast/multicast, and Ethernet frame structure.", duration: "25 min", status: "locked" },
          { id: "nf-7.3", title: "Switching Concepts & STP", description: "MAC address tables, switching methods, Spanning Tree Protocol, and loop prevention.", duration: "30 min", status: "locked" },
          { id: "nf-7.4", title: "ARP & Layer 2 Security Concerns", description: "ARP operation, ARP spoofing, MAC flooding, and Layer 2 attack vectors.", duration: "25 min", status: "locked" },
          { id: "nf-q7", title: "Module 7 Quiz: Ethernet & Data Link", description: "Test Ethernet standards, MAC addressing, switching, and ARP concepts.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "nf-8",
        title: "Wireless Networking",
        quizId: "nf-q8",
        lessons: [
          { id: "nf-8.1", title: "Wireless Standards (802.11a/b/g/n/ac/ax)", description: "Wi-Fi generations, frequencies (2.4 GHz vs 5 GHz), channel width, and speeds.", duration: "25 min", status: "locked" },
          { id: "nf-8.2", title: "Wireless Security: WEP, WPA, WPA2, WPA3", description: "Evolution of wireless security \u2014 vulnerabilities and best practices.", duration: "30 min", status: "locked" },
          { id: "nf-8.3", title: "Wireless Authentication & Enterprise Wi-Fi", description: "PSK vs 802.1X/RADIUS, EAP methods, and certificate-based authentication.", duration: "25 min", status: "locked" },
          { id: "nf-8.4", title: "Wireless Threats & Mitigation", description: "Evil twin, rogue AP, deauth attacks, war driving, and wireless IDS.", duration: "25 min", status: "locked" },
          { id: "nf-q8", title: "Module 8 Quiz: Wireless Networking", description: "Validate wireless standards, security protocols, and threat knowledge.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "nf-9",
        title: "Network Troubleshooting & Tools",
        quizId: "nf-q9",
        lessons: [
          { id: "nf-9.1", title: "Troubleshooting Methodology", description: "Systematic approach: identify, theory, test, plan, implement, verify, document.", duration: "20 min", status: "locked" },
          { id: "nf-9.2", title: "Command-Line Tools: ping, traceroute, nslookup", description: "Using ping, tracert/traceroute, nslookup, dig, and pathping for diagnostics.", duration: "30 min", status: "locked" },
          { id: "nf-9.3", title: "Network Analysis: netstat, ss, arp, ipconfig/ifconfig", description: "Viewing connections, routing tables, ARP caches, and interface configuration.", duration: "30 min", status: "locked" },
          { id: "nf-9.4", title: "Packet Capture with Wireshark", description: "Capturing and analyzing packets \u2014 filters, following streams, and protocol analysis.", duration: "35 min", status: "locked" },
          { id: "nf-9.5", title: "Hands-On: Network Troubleshooting Lab", description: "Diagnose and resolve common network issues in simulated scenarios.", duration: "45 min", status: "locked" },
          { id: "nf-q9", title: "Module 9 Quiz: Network Troubleshooting", description: "Assess your ability to use network diagnostic tools and methodologies.", duration: "20 min", status: "locked" }
        ]
      },
      {
        id: "nf-10",
        title: "Network Security & Modern Networking",
        quizId: "nf-q10",
        lessons: [
          { id: "nf-10.1", title: "Network Security Fundamentals", description: "Defense in depth, least privilege, segmentation, and the CIA triad in networking.", duration: "25 min", status: "locked" },
          { id: "nf-10.2", title: "VPNs: Site-to-Site & Remote Access", description: "IPSec, SSL/TLS VPNs, tunneling protocols, and split tunneling.", duration: "25 min", status: "locked" },
          { id: "nf-10.3", title: "Network Access Control (NAC) & 802.1X", description: "Port-based authentication, NAC solutions, and zero trust networking.", duration: "25 min", status: "locked" },
          { id: "nf-10.4", title: "Cloud & Virtualized Networking", description: "Virtual switches, SDN, VPC, cloud network architecture, and micro-segmentation.", duration: "25 min", status: "locked" },
          { id: "nf-10.5", title: "Course Summary & Next Steps", description: "Review all modules and prepare for advanced networking and security courses.", duration: "15 min", status: "locked" },
          { id: "nf-q10", title: "Final Certification Exam: Network Fundamentals", description: "Comprehensive final exam covering all 10 modules. Pass with 80% to earn your certificate.", duration: "60 min", status: "locked" }
        ]
      }
    ],
    quizzes: [
      { id: "nf-q1", title: "Computer Networks Basics Quiz", description: "Test your knowledge of network types, topologies, and architecture.", questionCount: 15, passingScore: 70, duration: "20 min", status: "unlocked" },
      { id: "nf-q2", title: "OSI Model Quiz", description: "Assess your understanding of the 7-layer OSI model and data encapsulation.", questionCount: 15, passingScore: 70, duration: "20 min", status: "locked" },
      { id: "nf-q3", title: "TCP/IP Protocol Suite Quiz", description: "Test your knowledge of TCP, UDP, ICMP, ARP, and port numbers.", questionCount: 15, passingScore: 75, duration: "20 min", status: "locked" },
      { id: "nf-q4", title: "IP Addressing & Subnetting Quiz", description: "Validate your subnetting skills and IPv4/IPv6 knowledge.", questionCount: 15, passingScore: 75, duration: "25 min", status: "locked" },
      { id: "nf-q5", title: "Network Devices Quiz", description: "Test your understanding of switches, routers, firewalls, and VLANs.", questionCount: 15, passingScore: 70, duration: "20 min", status: "locked" },
      { id: "nf-q6", title: "Application Protocols Quiz", description: "Assess your knowledge of DNS, DHCP, HTTP, email, and file transfer protocols.", questionCount: 15, passingScore: 70, duration: "20 min", status: "locked" },
      { id: "nf-q7", title: "Ethernet & Data Link Quiz", description: "Test Ethernet standards, MAC addressing, switching, and ARP concepts.", questionCount: 15, passingScore: 70, duration: "20 min", status: "locked" },
      { id: "nf-q8", title: "Wireless Networking Quiz", description: "Validate wireless standards, security protocols, and threat knowledge.", questionCount: 15, passingScore: 70, duration: "20 min", status: "locked" },
      { id: "nf-q9", title: "Network Troubleshooting Quiz", description: "Assess your ability to use network diagnostic tools and methodologies.", questionCount: 15, passingScore: 75, duration: "20 min", status: "locked" },
      { id: "nf-q10", title: "Network Fundamentals Certification Exam", description: "Comprehensive final exam covering all 10 modules. Pass with 80% to earn your certificate.", questionCount: 30, passingScore: 80, duration: "60 min", status: "locked" }
    ],
    resources: [
      { id: "nf-r1", title: "Network Protocols Cheat Sheet", description: "Quick reference for common protocols, ports, and their functions.", type: "cheatsheet" },
      { id: "nf-r2", title: "Subnetting Quick Reference", description: "Subnet mask table, CIDR notation guide, and calculation shortcuts.", type: "cheatsheet" },
      { id: "nf-r3", title: "Wireshark Display Filters Guide", description: "Common Wireshark filters for protocol analysis and troubleshooting.", type: "cheatsheet" },
      { id: "nf-r4", title: "OSI Model Reference Poster", description: "Visual reference of all 7 layers with protocols and devices at each layer.", type: "pdf" },
      { id: "nf-r5", title: "Network Command-Line Tools Guide", description: "Complete reference for ping, traceroute, nslookup, netstat, and more.", type: "template" },
      { id: "nf-r6", title: "Subnet Calculator", description: "Online subnet calculator for practice and real-world use.", type: "link", url: "https://www.subnet-calculator.com/" }
    ]
  }
];

// scripts/export_course_catalog.ts
var import_fs = require("fs");
var import_path = require("path");
var ID_TO_SLUG = {
  "soc-fundamentals": "blue-team-soc-fundamentals",
  "log-analysis": "log-analysis-for-beginners",
  "network-fundamentals": "network-fundamentals",
  "siem-fundamentals": "siem-fundamentals",
  "incident-response": "incident-response-fundamentals",
  "soc-analyst-path": "soc-analyst-path",
  "network-security-monitoring": "network-security-monitoring",
  "detection-engineering": "detection-engineering-basics",
  "malware-analysis": "malware-analysis-fundamentals",
  "threat-hunting": "threat-hunting-fundamentals",
  "cybersecurity-frameworks": "cybersecurity-frameworks"
};
var catalog = {};
for (const course of courses2) {
  const slug = ID_TO_SLUG[course.id] || course.id;
  catalog[slug] = {
    id: course.id,
    slug,
    title: course.title,
    shortTitle: course.shortTitle,
    description: course.description,
    difficulty: course.difficulty,
    duration: course.duration,
    modules: (course.modules || []).map((m) => ({
      id: m.id,
      title: m.title,
      lessons: (m.lessons || []).map((l) => ({
        id: l.id,
        title: l.title,
        description: l.description || ""
      }))
    }))
  };
}
var outPath = (0, import_path.resolve)(
  __dirname,
  "../../ai_service/app/knowledge/data/course_catalog.json"
);
(0, import_fs.mkdirSync)((0, import_path.dirname)(outPath), { recursive: true });
(0, import_fs.writeFileSync)(outPath, JSON.stringify(catalog, null, 2));
console.log(
  `Wrote course catalog for ${Object.keys(catalog).length} courses -> ${outPath}`
);
