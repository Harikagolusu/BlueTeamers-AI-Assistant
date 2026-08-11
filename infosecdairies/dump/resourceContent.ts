export interface ResourceDocument {
  id: string;
  courseId: string;
  title: string;
  type: string;
  content: string; // markdown
}

export const resourceDocuments: ResourceDocument[] = [
  // ==========================================
  // SOC FUNDAMENTALS RESOURCES
  // ==========================================
  {
    id: "r1",
    courseId: "soc-fundamentals",
    title: "SOC Analyst Cheat Sheet",
    type: "cheatsheet",
    content: `
## SOC Analyst Quick Reference

### Alert Triage Workflow
1. **Receive Alert** — Review SIEM notification, note severity and source
2. **Initial Assessment** — Check alert context: source IP, destination, user, timestamp
3. **Enrich** — Query threat intel (VirusTotal, AbuseIPDB), check reputation
4. **Correlate** — Search for related events ±15 minutes from the alert
5. **Classify** — True Positive, False Positive, or Benign True Positive
6. **Document** — Record findings in ticketing system
7. **Escalate** — If TP, escalate per severity matrix

### Common Investigation Commands

| Task | Windows | Linux |
|------|---------|-------|
| List processes | \`tasklist /v\` | \`ps aux\` |
| Network connections | \`netstat -ano\` | \`ss -tulnp\` |
| DNS cache | \`ipconfig /displaydns\` | \`cat /etc/resolv.conf\` |
| Logged-in users | \`query user\` | \`who\` |
| Scheduled tasks | \`schtasks /query\` | \`crontab -l\` |
| Running services | \`sc query\` | \`systemctl list-units\` |
| File hashes | \`certutil -hashfile <file> SHA256\` | \`sha256sum <file>\` |

### Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| **Critical** | Active data breach, ransomware, APT | Immediate (< 15 min) |
| **High** | Confirmed malware, lateral movement | < 1 hour |
| **Medium** | Suspicious behavior, policy violation | < 4 hours |
| **Low** | Informational, minor policy deviation | < 24 hours |

### Key Acronyms
- **SIEM** — Security Information & Event Management
- **EDR** — Endpoint Detection & Response
- **IOC** — Indicator of Compromise
- **TTP** — Tactics, Techniques & Procedures
- **MTTD** — Mean Time to Detect
- **MTTR** — Mean Time to Respond
- **C2/C&C** — Command and Control
- **FP** — False Positive
- **TP** — True Positive
- **BTP** — Benign True Positive

### Escalation Matrix
| Scenario | Escalate To |
|----------|-------------|
| Confirmed malware execution | L2 Analyst / IR Team |
| Data exfiltration suspected | IR Lead + Management |
| Insider threat indicators | IR Lead + HR + Legal |
| Ransomware detected | IR Lead + CISO + Legal |
| Nation-state TTPs observed | IR Lead + CISO + Threat Intel |
`,
  },
  {
    id: "r2",
    courseId: "soc-fundamentals",
    title: "Windows Event ID Reference",
    type: "pdf",
    content: `
## Windows Security Event ID Reference

### Authentication Events

| Event ID | Description | Significance |
|----------|-------------|-------------|
| **4624** | Successful logon | Track all successful authentications |
| **4625** | Failed logon | Brute force detection (threshold: 5+ in 10 min) |
| **4634** | Logoff | Session duration analysis |
| **4648** | Explicit credential logon | Credential theft / lateral movement |
| **4672** | Special privileges assigned | Admin logon monitoring |
| **4768** | Kerberos TGT requested | Domain authentication tracking |
| **4769** | Kerberos service ticket | Service access / Kerberoasting detection |
| **4771** | Kerberos pre-auth failed | Password spraying detection |
| **4776** | NTLM authentication | Legacy auth monitoring |

### Logon Types

| Type | Name | Description |
|------|------|-------------|
| 2 | Interactive | Physical keyboard logon |
| 3 | Network | SMB, named pipes, net use |
| 4 | Batch | Scheduled task execution |
| 5 | Service | Service startup |
| 7 | Unlock | Workstation unlock |
| 8 | NetworkCleartext | IIS basic auth (cleartext!) |
| 9 | NewCredentials | RunAs /netonly |
| 10 | RemoteInteractive | RDP / Terminal Services |
| 11 | CachedInteractive | Offline domain logon |

### Account Management

| Event ID | Description | Alert On |
|----------|-------------|----------|
| **4720** | User account created | Unexpected account creation |
| **4722** | User account enabled | Re-enabled accounts |
| **4724** | Password reset attempt | Unauthorized resets |
| **4725** | User account disabled | Potential denial of service |
| **4726** | User account deleted | Account cleanup or covering tracks |
| **4728** | Member added to security group | Privilege escalation |
| **4732** | Member added to local group | Local admin additions |
| **4756** | Member added to universal group | Domain-wide privilege changes |

### Process & Execution

| Event ID | Description | Use Case |
|----------|-------------|----------|
| **4688** | Process creation | Command-line auditing |
| **4689** | Process exit | Process lifetime tracking |
| **1** (Sysmon) | Process create | Parent-child process trees |
| **3** (Sysmon) | Network connection | Process network activity |
| **7** (Sysmon) | Image loaded | DLL loading monitoring |
| **11** (Sysmon) | File create | File drop detection |

### Detection Rules

**Brute Force Detection:**
\`\`\`
Event ID 4625 | count > 5 within 10 minutes | same target account
\`\`\`

**Lateral Movement (Pass-the-Hash):**
\`\`\`
Event ID 4624 | Logon Type 3 | Source ≠ known admin workstation
\`\`\`

**Privilege Escalation:**
\`\`\`
Event ID 4728 OR 4732 | Target Group = "Administrators" or "Domain Admins"
\`\`\`

**Suspicious Service Installation:**
\`\`\`
Event ID 7045 | Service name not in baseline | ImagePath contains temp/suspicious paths
\`\`\`
`,
  },
  {
    id: "r3",
    courseId: "soc-fundamentals",
    title: "Linux Log Analysis Guide",
    type: "pdf",
    content: `
## Linux Log Analysis Reference Guide

### Key Log File Locations

| Log File | Purpose | Key Events |
|----------|---------|------------|
| \`/var/log/auth.log\` | Authentication (Debian) | SSH, sudo, PAM events |
| \`/var/log/secure\` | Authentication (RHEL) | SSH, sudo, PAM events |
| \`/var/log/syslog\` | System messages | Service starts/stops, errors |
| \`/var/log/kern.log\` | Kernel messages | Hardware, driver, security |
| \`/var/log/cron\` | Cron job execution | Scheduled task monitoring |
| \`/var/log/faillog\` | Failed login attempts | Brute force detection |
| \`/var/log/lastlog\` | Last login records | User access patterns |
| \`/var/log/wtmp\` | Login/logout history | Session tracking |
| \`/var/log/btmp\` | Bad login attempts | Failed authentication |
| \`/var/log/apache2/\` | Web server logs | HTTP requests, errors |

### Essential CLI Commands

**Search for failed SSH logins:**
\`\`\`bash
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -20
\`\`\`

**Find successful logins from unusual IPs:**
\`\`\`bash
grep "Accepted" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn
\`\`\`

**Monitor sudo usage:**
\`\`\`bash
grep "sudo:" /var/log/auth.log | grep "COMMAND" | tail -50
\`\`\`

**Detect new user creation:**
\`\`\`bash
grep "useradd\\|adduser" /var/log/auth.log
\`\`\`

**Check for cron job modifications:**
\`\`\`bash
grep -i "crontab" /var/log/auth.log
\`\`\`

**Find large file transfers (potential exfil):**
\`\`\`bash
grep -E "scp|rsync|curl|wget" /var/log/auth.log
\`\`\`

### Common Attack Patterns in Linux Logs

#### SSH Brute Force
\`\`\`
Jan 15 03:22:01 server sshd[12345]: Failed password for root from 192.168.1.100 port 54321 ssh2
Jan 15 03:22:03 server sshd[12345]: Failed password for root from 192.168.1.100 port 54322 ssh2
Jan 15 03:22:05 server sshd[12345]: Failed password for root from 192.168.1.100 port 54323 ssh2
\`\`\`
**Indicator:** Multiple failed attempts for same user from same IP in short timeframe.

#### Privilege Escalation
\`\`\`
Jan 15 04:15:22 server sudo: attacker : TTY=pts/0 ; PWD=/tmp ; USER=root ; COMMAND=/bin/bash
\`\`\`
**Indicator:** Unexpected sudo commands, especially from non-admin users.

#### Persistence via Cron
\`\`\`
Jan 15 05:00:01 server crontab[9876]: (www-data) REPLACE (www-data)
\`\`\`
**Indicator:** Crontab modifications by service accounts or unexpected users.

### Log Rotation & Retention
- Logs rotate via \`logrotate\` (config: \`/etc/logrotate.conf\`)
- Default retention: 4 weeks
- **Recommendation:** Forward to centralized SIEM before rotation
- **Critical:** Preserve original logs for forensic integrity
`,
  },
  {
    id: "r4",
    courseId: "soc-fundamentals",
    title: "Alert Triage Workflow Template",
    type: "template",
    content: `
## Alert Triage Workflow Template

### Step 1: Alert Receipt & Initial Review

| Field | Details |
|-------|---------|
| **Alert ID** | _[Auto-generated]_ |
| **Date/Time** | _[Timestamp]_ |
| **SIEM Rule** | _[Rule name that triggered]_ |
| **Severity** | ☐ Critical  ☐ High  ☐ Medium  ☐ Low |
| **Source IP** | _[IP address]_ |
| **Destination IP** | _[IP address]_ |
| **Affected User** | _[Username]_ |
| **Affected Host** | _[Hostname]_ |

### Step 2: Context Gathering

- [ ] Review full alert details in SIEM
- [ ] Check source IP reputation (VirusTotal, AbuseIPDB)
- [ ] Check destination IP/domain reputation
- [ ] Review user's normal activity baseline
- [ ] Search for related alerts ±30 minutes
- [ ] Check if source/destination is an internal asset

### Step 3: Enrichment

| Enrichment Source | Result |
|-------------------|--------|
| **VirusTotal** | _[Clean / Malicious / Suspicious]_ |
| **AbuseIPDB** | _[Confidence score]_ |
| **Threat Intel Feed** | _[Match / No match]_ |
| **GeoIP** | _[Country / ASN]_ |
| **WHOIS** | _[Registration details]_ |
| **Historical Alerts** | _[Previous incidents]_ |

### Step 4: Classification

| Classification | Selected |
|---------------|----------|
| ☐ **True Positive** | Confirmed malicious activity |
| ☐ **Benign True Positive** | Expected behavior, correctly detected |
| ☐ **False Positive** | Non-malicious, rule needs tuning |
| ☐ **Requires Escalation** | Cannot determine, needs L2 review |

### Step 5: Response Actions

- [ ] Block source IP at firewall
- [ ] Isolate affected endpoint
- [ ] Reset user credentials
- [ ] Escalate to Incident Response team
- [ ] Update threat intel with new IOCs
- [ ] Submit false positive tuning request

### Step 6: Documentation

| Field | Details |
|-------|---------|
| **Analysis Summary** | _[Brief description of findings]_ |
| **Actions Taken** | _[List of response actions]_ |
| **Time Spent** | _[Duration of investigation]_ |
| **Analyst** | _[Your name]_ |
| **Escalated To** | _[Name/Team if escalated]_ |
`,
  },
  {
    id: "r5",
    courseId: "soc-fundamentals",
    title: "Incident Response Runbook",
    type: "template",
    content: `
## Incident Response Runbook

### Phishing Incident Playbook

#### Phase 1: Detection
- [ ] Alert received from email gateway / user report / SIEM
- [ ] Capture original email headers and body
- [ ] Identify sender address, reply-to, and return-path
- [ ] Extract all URLs and attachments

#### Phase 2: Analysis
- [ ] Analyze URLs with urlscan.io and VirusTotal
- [ ] Submit attachments to sandbox (Any.Run, Hybrid Analysis)
- [ ] Check sender domain age and reputation
- [ ] Identify all recipients who received the email
- [ ] Determine if any user clicked links or opened attachments

#### Phase 3: Containment
- [ ] Block sender domain/IP at email gateway
- [ ] Block malicious URLs at proxy/firewall
- [ ] Purge email from all mailboxes
- [ ] If credentials compromised: force password reset + revoke sessions
- [ ] If malware delivered: isolate affected endpoints

#### Phase 4: Recovery
- [ ] Scan affected endpoints with EDR
- [ ] Verify no persistence mechanisms installed
- [ ] Monitor affected accounts for 72 hours
- [ ] Re-enable access after clearance

#### Phase 5: Post-Incident
- [ ] Document timeline and findings
- [ ] Update email filtering rules
- [ ] Add IOCs to threat intel platform
- [ ] Conduct user awareness follow-up

---

### Malware Incident Playbook

#### Phase 1: Detection
- [ ] Alert from EDR / AV / SIEM
- [ ] Identify affected host(s) and user(s)
- [ ] Capture malware hash (SHA256)

#### Phase 2: Analysis
- [ ] Check hash on VirusTotal and MalwareBazaar
- [ ] Determine malware family and capabilities
- [ ] Identify C2 infrastructure
- [ ] Check for lateral movement indicators

#### Phase 3: Containment
- [ ] Isolate affected endpoint from network
- [ ] Block C2 domains/IPs at firewall
- [ ] Disable compromised user accounts
- [ ] Preserve memory dump and disk image

#### Phase 4: Eradication
- [ ] Remove malware and persistence mechanisms
- [ ] Patch exploited vulnerabilities
- [ ] Reset all credentials used on affected systems
- [ ] Verify removal with full endpoint scan

#### Phase 5: Recovery & Lessons Learned
- [ ] Restore from clean backup if necessary
- [ ] Monitor for reinfection (30 days)
- [ ] Update detection rules
- [ ] Conduct post-incident review
`,
  },
  {
    id: "r9",
    courseId: "soc-fundamentals",
    title: "Threat Intel Tools List",
    type: "pdf",
    content: `
## Threat Intelligence Tools Reference

### IOC Lookup & Reputation

| Tool | URL | Purpose |
|------|-----|---------|
| **VirusTotal** | virustotal.com | File, URL, IP, domain analysis |
| **AbuseIPDB** | abuseipdb.com | IP reputation and abuse reports |
| **URLScan.io** | urlscan.io | URL scanning and screenshot |
| **Shodan** | shodan.io | Internet-connected device search |
| **Censys** | censys.io | Internet-wide scanning data |
| **GreyNoise** | greynoise.io | Internet noise vs targeted attacks |
| **OTX AlienVault** | otx.alienvault.com | Open threat exchange |
| **ThreatFox** | threatfox.abuse.ch | IOC sharing platform |

### Malware Analysis

| Tool | URL | Purpose |
|------|-----|---------|
| **Any.Run** | any.run | Interactive malware sandbox |
| **Hybrid Analysis** | hybrid-analysis.com | Free malware analysis |
| **MalwareBazaar** | bazaar.abuse.ch | Malware sample sharing |
| **Joe Sandbox** | joesandbox.com | Deep malware analysis |
| **Triage** | tria.ge | Automated malware analysis |

### OSINT & Reconnaissance

| Tool | URL | Purpose |
|------|-----|---------|
| **Maltego** | maltego.com | Link analysis and data mining |
| **SpiderFoot** | spiderfoot.net | OSINT automation |
| **theHarvester** | (GitHub) | Email/subdomain enumeration |
| **WHOIS Lookup** | whois.domaintools.com | Domain registration data |
| **DNSDumpster** | dnsdumpster.com | DNS reconnaissance |
| **crt.sh** | crt.sh | Certificate transparency logs |

### Vulnerability Intelligence

| Tool | URL | Purpose |
|------|-----|---------|
| **NVD** | nvd.nist.gov | National Vulnerability Database |
| **CVE Details** | cvedetails.com | CVE browsing and statistics |
| **Exploit-DB** | exploit-db.com | Public exploit database |
| **VulnDB** | vulndb.cyberriskanalytics.com | Commercial vuln intelligence |

### Threat Intelligence Platforms

| Tool | URL | Purpose |
|------|-----|---------|
| **MISP** | misp-project.org | Open-source TI sharing |
| **OpenCTI** | opencti.io | Cyber threat intelligence platform |
| **ThreatConnect** | threatconnect.com | TI operations platform |
| **Recorded Future** | recordedfuture.com | Real-time threat intelligence |
`,
  },
  {
    id: "r10",
    courseId: "soc-fundamentals",
    title: "SOC Metrics & KPIs Guide",
    type: "pdf",
    content: `
## SOC Metrics & KPIs Reference Guide

### Core Performance Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **MTTD** (Mean Time to Detect) | Avg time from compromise to detection | < 24 hours |
| **MTTR** (Mean Time to Respond) | Avg time from detection to containment | < 4 hours |
| **MTTA** (Mean Time to Acknowledge) | Avg time from alert to analyst pickup | < 15 minutes |
| **Dwell Time** | Time attacker is in environment undetected | < 30 days |

### Alert Metrics

| Metric | Description | Healthy Range |
|--------|-------------|---------------|
| **Alert Volume** | Total alerts per day/week | Trending down |
| **False Positive Rate** | % of alerts that are FP | < 30% |
| **True Positive Rate** | % of alerts confirmed malicious | > 20% |
| **Escalation Rate** | % of alerts escalated to L2/IR | 5-15% |
| **Alert Closure Time** | Avg time to close an alert | < 30 min (L1) |
| **Alerts per Analyst** | Workload distribution | < 50/shift |

### Incident Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Incidents per Month** | Total confirmed incidents | Track trend |
| **Severity Distribution** | Breakdown by severity level | Monitor shifts |
| **Repeat Incidents** | Same type recurring | Decreasing |
| **Containment Success Rate** | % contained before impact | > 90% |
| **Post-Incident Actions** | Improvements implemented | 100% tracked |

### Analyst Performance

| Metric | Description | Use |
|--------|-------------|-----|
| **Alerts Handled** | Volume per analyst per shift | Workload balance |
| **Accuracy Rate** | Correct classifications | Quality measure |
| **Avg Investigation Time** | Time spent per alert | Efficiency |
| **Escalation Accuracy** | % of escalations confirmed | Decision quality |
| **Training Hours** | Continuous learning time | Growth tracking |

### Dashboard Recommendations
- Display MTTD/MTTR trends over 30/90 days
- Show alert volume with severity breakdown
- Track false positive rate weekly
- Monitor analyst workload distribution
- Compare current metrics to baseline/SLA targets
`,
  },

  // ==========================================
  // LOG ANALYSIS RESOURCES
  // ==========================================
  {
    id: "la-r1",
    courseId: "log-analysis",
    title: "Windows Event ID Cheat Sheet",
    type: "cheatsheet",
    content: `
## Windows Event ID Quick Reference

### Authentication & Logon

| ID | Event | Priority |
|----|-------|----------|
| 4624 | Successful logon | Monitor Type 3, 10 |
| 4625 | Failed logon | Alert on >5 in 10min |
| 4634 | Logoff | Session tracking |
| 4648 | Explicit credentials | Lateral movement |
| 4672 | Special privileges | Admin monitoring |
| 4768 | Kerberos TGT request | Auth baseline |
| 4769 | Kerberos ST request | Kerberoasting |
| 4771 | Kerberos pre-auth fail | Password spray |

### Account Management

| ID | Event | Priority |
|----|-------|----------|
| 4720 | Account created | Always alert |
| 4722 | Account enabled | Monitor |
| 4724 | Password reset | Monitor |
| 4726 | Account deleted | Always alert |
| 4728 | Added to global group | Priv escalation |
| 4732 | Added to local group | Priv escalation |
| 4756 | Added to universal group | Domain-wide |

### Process & Execution

| ID | Event | Priority |
|----|-------|----------|
| 4688 | Process created | Command-line audit |
| 4689 | Process exited | Lifetime tracking |
| 7045 | Service installed | Persistence |
| 1102 | Audit log cleared | Anti-forensics! |

### Sysmon Events

| ID | Event | Priority |
|----|-------|----------|
| 1 | Process create | Process tree |
| 3 | Network connection | C2 detection |
| 7 | Image loaded | DLL hijacking |
| 8 | CreateRemoteThread | Injection |
| 11 | File create | Dropper activity |
| 12-14 | Registry events | Persistence |
| 22 | DNS query | C2 domains |
`,
  },
  {
    id: "la-r2",
    courseId: "log-analysis",
    title: "Linux Log Files Reference",
    type: "pdf",
    content: `
## Linux Log Files Comprehensive Reference

### System Logs

| File | Description | Key Events |
|------|-------------|------------|
| \`/var/log/syslog\` | General system activity | Service start/stop, errors |
| \`/var/log/messages\` | General messages (RHEL) | System-wide events |
| \`/var/log/kern.log\` | Kernel messages | Hardware, modules, security |
| \`/var/log/dmesg\` | Boot messages | Hardware detection |
| \`/var/log/boot.log\` | Boot process | Service startup sequence |

### Authentication Logs

| File | Description | Key Events |
|------|-------------|------------|
| \`/var/log/auth.log\` | Auth events (Debian) | SSH, sudo, PAM |
| \`/var/log/secure\` | Auth events (RHEL) | SSH, sudo, PAM |
| \`/var/log/faillog\` | Failed login counter | Brute force tracking |
| \`/var/log/lastlog\` | Last login per user | Access monitoring |
| \`/var/log/wtmp\` | Login/logout history | \`last\` command source |
| \`/var/log/btmp\` | Bad login attempts | \`lastb\` command source |

### Application Logs

| File | Description | Key Events |
|------|-------------|------------|
| \`/var/log/apache2/access.log\` | Apache requests | Web traffic analysis |
| \`/var/log/apache2/error.log\` | Apache errors | Attack indicators |
| \`/var/log/nginx/access.log\` | Nginx requests | Web traffic analysis |
| \`/var/log/mysql/error.log\` | MySQL errors | SQLi indicators |
| \`/var/log/cron\` | Cron execution | Persistence detection |
| \`/var/log/mail.log\` | Mail server | Spam/phishing |

### Useful Commands

\`\`\`bash
# Real-time log monitoring
tail -f /var/log/auth.log

# Search compressed rotated logs
zgrep "Failed password" /var/log/auth.log.*.gz

# Count events by source IP
grep "Failed password" /var/log/auth.log | \\
  awk '{print $(NF-3)}' | sort | uniq -c | sort -rn

# Timeline of sudo commands
grep "COMMAND" /var/log/auth.log | \\
  awk '{print $1, $2, $3, $6, $NF}'

# Find all login activity for a user
grep "username" /var/log/auth.log | grep -E "session opened|Accepted"
\`\`\`
`,
  },
  {
    id: "la-r3",
    courseId: "log-analysis",
    title: "Log Analysis CLI Commands",
    type: "cheatsheet",
    content: `
## Log Analysis CLI Command Reference

### grep — Pattern Search

\`\`\`bash
# Basic search
grep "error" /var/log/syslog

# Case-insensitive
grep -i "failed" /var/log/auth.log

# Invert match (exclude)
grep -v "INFO" /var/log/app.log

# Show line numbers
grep -n "unauthorized" /var/log/auth.log

# Count matches
grep -c "404" /var/log/apache2/access.log

# Context (3 lines before/after)
grep -B3 -A3 "segfault" /var/log/kern.log

# Extended regex
grep -E "(error|warning|critical)" /var/log/syslog

# Recursive search
grep -r "password" /var/log/
\`\`\`

### awk — Field Processing

\`\`\`bash
# Print specific columns
awk '{print $1, $4}' access.log

# Filter by field value
awk '$9 == 404' access.log

# Count by field
awk '{print $1}' access.log | sort | uniq -c | sort -rn

# Sum a column
awk '{sum += $10} END {print sum}' access.log

# Custom field separator
awk -F',' '{print $2}' data.csv
\`\`\`

### sed — Stream Editor

\`\`\`bash
# Replace text
sed 's/old/new/g' file.log

# Delete lines matching pattern
sed '/DEBUG/d' app.log

# Print specific line range
sed -n '100,200p' large.log

# Remove blank lines
sed '/^$/d' file.log
\`\`\`

### sort & uniq — Aggregation

\`\`\`bash
# Top 10 source IPs
cut -d' ' -f1 access.log | sort | uniq -c | sort -rn | head -10

# Unique values
sort -u field_output.txt

# Sort by numeric column
sort -t',' -k3 -n data.csv
\`\`\`

### cut — Column Extraction

\`\`\`bash
# Extract by delimiter
cut -d':' -f1 /etc/passwd

# Extract by character position
cut -c1-15 access.log

# Multiple fields
cut -d',' -f1,3,5 data.csv
\`\`\`

### Combining Commands (Pipelines)

\`\`\`bash
# Top 10 failed SSH sources
grep "Failed password" /var/log/auth.log | \\
  awk '{print $(NF-3)}' | \\
  sort | uniq -c | sort -rn | head -10

# HTTP 500 errors by URL
grep " 500 " access.log | \\
  awk '{print $7}' | \\
  sort | uniq -c | sort -rn

# Hourly event distribution
awk '{print substr($4,2,14)}' access.log | \\
  cut -d: -f1,2 | sort | uniq -c
\`\`\`
`,
  },
  {
    id: "la-r4",
    courseId: "log-analysis",
    title: "Common Attack Patterns in Logs",
    type: "pdf",
    content: `
## Common Attack Patterns in Logs

### 1. Brute Force Attack

**Windows Event Logs:**
\`\`\`
Multiple Event ID 4625 (Failed logon)
Same TargetUserName, different/same SourceNetworkAddress
Rapid succession (< 1 second intervals)
Eventually followed by Event ID 4624 (Success)
\`\`\`

**Linux auth.log:**
\`\`\`
Failed password for root from 10.0.0.5 port 22 ssh2
Failed password for root from 10.0.0.5 port 22 ssh2
Accepted password for root from 10.0.0.5 port 22 ssh2
\`\`\`

**Detection:** >5 failed logins in 10 minutes from same source

---

### 2. Lateral Movement (Pass-the-Hash)

**Windows Event Logs:**
\`\`\`
Event ID 4624, Logon Type 3 (Network)
Auth Package: NTLM (not Kerberos)
Source from internal workstation
Target: multiple servers in sequence
\`\`\`

**Detection:** NTLM Type 3 logons from non-server sources to multiple targets

---

### 3. Data Exfiltration

**Firewall/Proxy Logs:**
\`\`\`
Large outbound transfers (>100MB) to external IPs
Connections to cloud storage (Mega, Dropbox) from servers
DNS queries with unusually long subdomain strings (DNS tunneling)
Outbound connections on non-standard ports
\`\`\`

**Detection:** Baseline normal transfer volumes, alert on anomalies

---

### 4. Web Application Attacks

**Apache/Nginx Access Logs:**
\`\`\`
SQL Injection: GET /page?id=1' OR '1'='1 HTTP/1.1
XSS: GET /search?q=<script>alert(1)</script> HTTP/1.1
Directory Traversal: GET /../../etc/passwd HTTP/1.1
Command Injection: GET /ping?ip=;cat+/etc/passwd HTTP/1.1
\`\`\`

**Detection:** Pattern match on special characters in query parameters

---

### 5. Privilege Escalation

**Linux Logs:**
\`\`\`
sudo: user NOT in sudoers; TTY=pts/0
su: FAILED su for root by attacker
User added to sudo/wheel group unexpectedly
\`\`\`

**Windows Logs:**
\`\`\`
Event ID 4672 — Special privileges assigned to unexpected user
Event ID 4728/4732 — Added to Administrators group
\`\`\`

---

### 6. Persistence Mechanisms

**Indicators in logs:**
- New scheduled tasks/cron jobs
- New services installed (Event ID 7045)
- Registry run key modifications (Sysmon 12/13)
- New user accounts created (Event ID 4720)
- SSH authorized_keys modifications
`,
  },
  {
    id: "la-r5",
    courseId: "log-analysis",
    title: "Sysmon Configuration Guide",
    type: "template",
    content: `
## Sysmon Configuration Best Practices

### Recommended Sysmon Config Structure

\`\`\`xml
<Sysmon schemaversion="4.90">
  <HashAlgorithms>SHA256,IMPHASH</HashAlgorithms>
  <EventFiltering>

    <!-- Process Creation (Event ID 1) -->
    <RuleGroup name="ProcessCreate" groupRelation="or">
      <ProcessCreate onmatch="include">
        <ParentImage condition="end with">cmd.exe</ParentImage>
        <ParentImage condition="end with">powershell.exe</ParentImage>
        <ParentImage condition="end with">wscript.exe</ParentImage>
        <ParentImage condition="end with">cscript.exe</ParentImage>
        <ParentImage condition="end with">mshta.exe</ParentImage>
        <Image condition="end with">rundll32.exe</Image>
        <Image condition="end with">regsvr32.exe</Image>
        <Image condition="end with">certutil.exe</Image>
        <Image condition="end with">bitsadmin.exe</Image>
      </ProcessCreate>
    </RuleGroup>

    <!-- Network Connection (Event ID 3) -->
    <RuleGroup name="NetworkConnect" groupRelation="or">
      <NetworkConnect onmatch="include">
        <Image condition="end with">powershell.exe</Image>
        <Image condition="end with">cmd.exe</Image>
        <Image condition="end with">rundll32.exe</Image>
        <DestinationPort condition="is">4444</DestinationPort>
        <DestinationPort condition="is">5555</DestinationPort>
        <DestinationPort condition="is">8888</DestinationPort>
      </NetworkConnect>
    </RuleGroup>

    <!-- File Creation (Event ID 11) -->
    <RuleGroup name="FileCreate" groupRelation="or">
      <FileCreate onmatch="include">
        <TargetFilename condition="contains">\\Startup\\</TargetFilename>
        <TargetFilename condition="contains">\\Temp\\</TargetFilename>
        <TargetFilename condition="end with">.exe</TargetFilename>
        <TargetFilename condition="end with">.dll</TargetFilename>
        <TargetFilename condition="end with">.ps1</TargetFilename>
        <TargetFilename condition="end with">.bat</TargetFilename>
        <TargetFilename condition="end with">.hta</TargetFilename>
      </FileCreate>
    </RuleGroup>

    <!-- Registry (Event ID 12, 13, 14) -->
    <RuleGroup name="RegistryEvent" groupRelation="or">
      <RegistryEvent onmatch="include">
        <TargetObject condition="contains">\\Run\\</TargetObject>
        <TargetObject condition="contains">\\RunOnce\\</TargetObject>
        <TargetObject condition="contains">\\Services\\</TargetObject>
        <TargetObject condition="contains">\\Image File Execution</TargetObject>
      </RegistryEvent>
    </RuleGroup>

  </EventFiltering>
</Sysmon>
\`\`\`

### Installation Commands
\`\`\`powershell
# Install Sysmon
sysmon64.exe -accepteula -i sysmonconfig.xml

# Update configuration
sysmon64.exe -c sysmonconfig.xml

# Check current status
sysmon64.exe -s
\`\`\`

### Key Sysmon Events to Monitor
| Event ID | Name | Security Value |
|----------|------|---------------|
| 1 | Process Create | Execution tracking |
| 3 | Network Connect | C2 detection |
| 7 | Image Loaded | DLL side-loading |
| 8 | CreateRemoteThread | Process injection |
| 10 | Process Access | Credential dumping |
| 11 | File Create | Dropper detection |
| 12-14 | Registry | Persistence |
| 22 | DNS Query | Domain resolution |
`,
  },
  {
    id: "la-r6",
    courseId: "log-analysis",
    title: "Log Parsing Regex Patterns",
    type: "cheatsheet",
    content: `
## Log Parsing Regular Expressions

### Common Log Format (Apache/Nginx)
\`\`\`regex
^(\\S+) \\S+ \\S+ \\[([^\\]]+)\\] "(\\S+) (\\S+) \\S+" (\\d{3}) (\\d+|-)
\`\`\`
**Captures:** IP, timestamp, method, URL, status, bytes

### Syslog Format
\`\`\`regex
^(\\w{3}\\s+\\d{1,2}\\s+\\d{2}:\\d{2}:\\d{2}) (\\S+) (\\S+?)(?:\\[(\\d+)\\])?: (.+)$
\`\`\`
**Captures:** timestamp, hostname, service, PID, message

### IP Address Extraction
\`\`\`regex
\\b(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})\\b
\`\`\`

### IPv6 Address
\`\`\`regex
([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
\`\`\`

### Email Address
\`\`\`regex
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}
\`\`\`

### URL Extraction
\`\`\`regex
https?://[\\w\\-]+(\\.[\\w\\-]+)+[/\\w\\-._~:?#@!$&'()*+,;=%]*
\`\`\`

### MD5 Hash
\`\`\`regex
\\b[a-fA-F0-9]{32}\\b
\`\`\`

### SHA256 Hash
\`\`\`regex
\\b[a-fA-F0-9]{64}\\b
\`\`\`

### Windows Event ID
\`\`\`regex
EventID[=:\\s]*(\\d{4,5})
\`\`\`

### Timestamp Patterns
\`\`\`regex
# ISO 8601
\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}

# Apache/CLF
\\d{2}/\\w{3}/\\d{4}:\\d{2}:\\d{2}:\\d{2}

# Syslog
\\w{3}\\s+\\d{1,2}\\s+\\d{2}:\\d{2}:\\d{2}

# Windows
\\d{1,2}/\\d{1,2}/\\d{4}\\s+\\d{1,2}:\\d{2}:\\d{2}\\s+(AM|PM)
\`\`\`

### Suspicious Patterns
\`\`\`regex
# SQL Injection
('|--|;|UNION|SELECT|INSERT|DROP|UPDATE|DELETE|EXEC)

# XSS
(<script|javascript:|onerror=|onload=|eval\\()

# Directory Traversal
(\\.\\./|\\.\\.\\\\)

# Command Injection
(;|\\||&&|\\$\\(|\\x60)
\`\`\`
`,
  },

  // ==========================================
  // SIEM FUNDAMENTALS RESOURCES
  // ==========================================
  {
    id: "siem-r1",
    courseId: "siem-fundamentals",
    title: "SIEM Query Cheat Sheet",
    type: "cheatsheet",
    content: `
## SIEM Query Quick Reference

### Splunk (SPL)

\`\`\`spl
# Basic search
index=main sourcetype=WinEventLog EventCode=4625

# Time range
index=main earliest=-24h latest=now

# Statistics
index=main | stats count by src_ip | sort -count

# Top values
index=main | top limit=10 src_ip

# Table output
index=main | table _time, src_ip, dest_ip, action

# Where clause
index=main | where status>=400

# Timechart
index=main | timechart span=1h count by sourcetype

# Transaction grouping
index=main | transaction src_ip maxspan=5m

# Subsearch
index=main [search index=threat_intel | fields ioc_ip | rename ioc_ip as src_ip]

# Lookup enrichment
index=main | lookup geo_ip ip as src_ip OUTPUT country, city
\`\`\`

### Microsoft Sentinel (KQL)

\`\`\`kql
// Basic query
SecurityEvent | where EventID == 4625

// Time filter
SecurityEvent | where TimeGenerated > ago(24h)

// Aggregation
SecurityEvent | summarize count() by SourceIP | top 10 by count_

// Table output
SecurityEvent | project TimeGenerated, SourceIP, TargetAccount

// Where clause
CommonSecurityLog | where DeviceAction == "Deny"

// Timechart equivalent
SecurityEvent | summarize count() by bin(TimeGenerated, 1h)

// Join
SecurityEvent
| join kind=inner (ThreatIntelIndicators) on $left.SourceIP == $right.IP

// Let variable
let threshold = 5;
SecurityEvent
| where EventID == 4625
| summarize FailCount=count() by TargetAccount
| where FailCount > threshold
\`\`\`

### Elastic (EQL/KQL)

\`\`\`
# KQL (Kibana)
event.code: "4625" and source.ip: "10.0.0.*"

# Lucene
event.code:"4625" AND NOT source.ip:"127.0.0.1"

# Date range
@timestamp:[now-24h TO now]
\`\`\`
`,
  },
  {
    id: "siem-r2",
    courseId: "siem-fundamentals",
    title: "SPL (Splunk) Quick Reference",
    type: "cheatsheet",
    content: `
## Splunk Processing Language (SPL) Reference

### Search Commands

| Command | Purpose | Example |
|---------|---------|---------|
| \`search\` | Filter events | \`search error OR failed\` |
| \`where\` | Filter with expressions | \`where count > 10\` |
| \`dedup\` | Remove duplicates | \`dedup src_ip\` |
| \`sort\` | Order results | \`sort -count\` |
| \`head\` / \`tail\` | First/last N | \`head 20\` |
| \`fields\` | Select/remove fields | \`fields src_ip, dest_ip\` |
| \`rename\` | Rename fields | \`rename src as source\` |
| \`eval\` | Compute fields | \`eval mb=bytes/1024/1024\` |

### Aggregation Commands

| Command | Purpose | Example |
|---------|---------|---------|
| \`stats\` | Aggregate values | \`stats count by src_ip\` |
| \`timechart\` | Time-based stats | \`timechart span=1h count\` |
| \`chart\` | Pivot table | \`chart count over src by dest\` |
| \`top\` | Top N values | \`top 10 src_ip\` |
| \`rare\` | Least common | \`rare process_name\` |
| \`eventstats\` | Stats without reducing | \`eventstats avg(bytes) as avg_bytes\` |

### Stats Functions

| Function | Description |
|----------|-------------|
| \`count\` | Number of events |
| \`dc(field)\` | Distinct count |
| \`sum(field)\` | Sum of values |
| \`avg(field)\` | Average |
| \`min(field)\` / \`max(field)\` | Minimum / Maximum |
| \`values(field)\` | All unique values |
| \`list(field)\` | All values (with dupes) |
| \`earliest(field)\` | First chronological |
| \`latest(field)\` | Last chronological |

### Eval Functions

\`\`\`spl
| eval severity=case(count>100, "critical", count>50, "high", count>10, "medium", true(), "low")
| eval domain=replace(url, "https?://([^/]+).*", "\\1")
| eval is_internal=if(cidrmatch("10.0.0.0/8", src_ip), "yes", "no")
| eval hour=strftime(_time, "%H")
\`\`\`

### Security-Specific Searches

\`\`\`spl
# Brute force detection
index=wineventlog EventCode=4625
| stats count by src_ip, Account_Name
| where count > 5

# Suspicious process execution
index=sysmon EventCode=1
| search ParentImage="*\\\\cmd.exe" OR ParentImage="*\\\\powershell.exe"
| stats count by Image, CommandLine

# Outbound traffic anomalies
index=firewall action=allowed direction=outbound
| stats sum(bytes_out) as total_bytes by dest_ip
| where total_bytes > 1073741824
| sort -total_bytes
\`\`\`
`,
  },
  {
    id: "siem-r3",
    courseId: "siem-fundamentals",
    title: "KQL (Sentinel) Quick Reference",
    type: "cheatsheet",
    content: `
## Kusto Query Language (KQL) for Microsoft Sentinel

### Basic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| \`where\` | Filter rows | \`| where EventID == 4625\` |
| \`project\` | Select columns | \`| project TimeGenerated, SourceIP\` |
| \`extend\` | Add computed column | \`| extend Hour = datetime_part("hour", TimeGenerated)\` |
| \`summarize\` | Aggregate | \`| summarize count() by SourceIP\` |
| \`order by\` | Sort | \`| order by count_ desc\` |
| \`top\` | Top N rows | \`| top 10 by count_\` |
| \`take\` | Sample N rows | \`| take 100\` |
| \`distinct\` | Unique values | \`| distinct SourceIP\` |
| \`join\` | Combine tables | \`| join kind=inner (Table2) on Key\` |
| \`union\` | Combine rows | \`Table1 | union Table2\` |

### String Operators

| Operator | Case-Sensitive | Example |
|----------|---------------|---------|
| \`==\` | Yes | \`where Name == "Admin"\` |
| \`=~\` | No | \`where Name =~ "admin"\` |
| \`contains\` | No | \`where URL contains "login"\` |
| \`has\` | No (word match) | \`where Message has "error"\` |
| \`startswith\` | No | \`where Path startswith "/api"\` |
| \`matches regex\` | Yes | \`where IP matches regex "10\\\\.0\\\\..*"\` |

### Time Functions

\`\`\`kql
// Relative time
| where TimeGenerated > ago(24h)
| where TimeGenerated between (ago(7d) .. ago(1d))

// Time bins
| summarize count() by bin(TimeGenerated, 1h)

// Extract parts
| extend DayOfWeek = dayofweek(TimeGenerated)
| extend Hour = datetime_part("hour", TimeGenerated)
\`\`\`

### Security Hunting Queries

\`\`\`kql
// Failed logins by source
SecurityEvent
| where EventID == 4625
| where TimeGenerated > ago(24h)
| summarize FailedAttempts=count() by SourceIP=IpAddress, TargetAccount=TargetUserName
| where FailedAttempts > 5
| order by FailedAttempts desc

// Rare processes
DeviceProcessEvents
| where TimeGenerated > ago(7d)
| summarize ExecutionCount=count() by FileName
| where ExecutionCount < 3
| order by ExecutionCount

// Outbound connections by process
DeviceNetworkEvents
| where RemoteIPType == "Public"
| summarize ConnectionCount=count(), UniqueIPs=dcount(RemoteIP) by InitiatingProcessFileName
| where ConnectionCount > 100
| order by ConnectionCount desc
\`\`\`
`,
  },
  {
    id: "siem-r4",
    courseId: "siem-fundamentals",
    title: "SIEM Dashboard Templates",
    type: "template",
    content: `
## SIEM Dashboard Template Guide

### Dashboard 1: SOC Overview

**Purpose:** High-level security posture for SOC managers

| Panel | Visualization | Query Focus |
|-------|--------------|-------------|
| Total Alerts (24h) | Single Value | Count of all alerts |
| Alert Trend | Line Chart | Alerts over time (hourly) |
| Severity Breakdown | Pie/Donut | Count by severity |
| Top Alert Rules | Bar Chart | Most triggered rules |
| Top Source IPs | Table | Highest alert sources |
| MTTR Trend | Line Chart | Response time over days |
| Open Incidents | Single Value | Unresolved count |
| Analyst Workload | Bar Chart | Alerts per analyst |

---

### Dashboard 2: Authentication Monitoring

**Purpose:** Track login activity and detect anomalies

| Panel | Visualization | Query Focus |
|-------|--------------|-------------|
| Failed Logins (24h) | Single Value | Event ID 4625 count |
| Failed vs Success Trend | Dual Line | 4625 vs 4624 over time |
| Top Failed Accounts | Table | Accounts with most failures |
| Failed by Source IP | Bar Chart | IPs generating failures |
| Logon Type Distribution | Pie Chart | Type 2, 3, 10, etc. |
| Geographic Login Map | Geo Map | Login locations |
| After-Hours Logins | Table | Logins outside business hours |
| New Account Creations | Table | Event ID 4720 |

---

### Dashboard 3: Network Security

**Purpose:** Monitor network traffic and detect threats

| Panel | Visualization | Query Focus |
|-------|--------------|-------------|
| Firewall Denies (24h) | Single Value | Blocked connection count |
| Traffic Volume | Area Chart | Bytes in/out over time |
| Top Blocked IPs | Table | Most denied sources |
| Top Destinations | Bar Chart | Most accessed external IPs |
| Port Distribution | Pie Chart | Destination port breakdown |
| DNS Query Volume | Line Chart | DNS queries over time |
| Suspicious DNS | Table | Long/unusual domain queries |
| IDS Alert Summary | Table | Suricata/Snort alerts |

---

### Dashboard 4: Endpoint Security

**Purpose:** EDR and endpoint health monitoring

| Panel | Visualization | Query Focus |
|-------|--------------|-------------|
| EDR Alerts (24h) | Single Value | Endpoint detection count |
| Malware Detections | Table | AV/EDR malware finds |
| Suspicious Processes | Table | Unusual process execution |
| PowerShell Activity | Line Chart | PS execution over time |
| USB Device Connections | Table | Removable media events |
| Endpoint Health | Gauge | % endpoints reporting |
| Patch Compliance | Bar Chart | Missing patches by severity |
`,
  },
  {
    id: "siem-r5",
    courseId: "siem-fundamentals",
    title: "Alert Tuning Guide",
    type: "pdf",
    content: `
## Alert Tuning Best Practices

### The Alert Tuning Process

1. **Identify High-Volume Alerts** — Sort by frequency, find top noise generators
2. **Analyze False Positives** — Sample 20+ alerts, determine FP root cause
3. **Categorize FP Causes:**
   - Overly broad rule logic
   - Legitimate business activity not whitelisted
   - Misconfigured data sources
   - Outdated threat intelligence
4. **Apply Tuning** — Modify rule, add exceptions, adjust thresholds
5. **Validate** — Monitor for 7 days, confirm FP reduction without losing TPs
6. **Document** — Record changes, rationale, and validation results

### Tuning Techniques

#### Whitelisting
\`\`\`
# Before: Alerts on ALL PowerShell network activity
process_name="powershell.exe" AND network_connection=true

# After: Exclude known admin workstations
process_name="powershell.exe" AND network_connection=true
AND NOT src_ip IN ("10.0.1.50", "10.0.1.51", "10.0.1.52")
\`\`\`

#### Threshold Adjustment
\`\`\`
# Before: Alert on any failed login
EventCode=4625

# After: Alert on 5+ failures in 10 minutes
EventCode=4625 | stats count by src_ip, target_user | where count >= 5
\`\`\`

#### Time-Based Filtering
\`\`\`
# Exclude scheduled backup jobs (run 2-4 AM)
NOT (hour >= 2 AND hour <= 4 AND process_name="backup.exe")
\`\`\`

#### Severity Re-Classification
| Original Severity | Tuned Severity | Reason |
|-------------------|----------------|--------|
| High | Medium | Known scanner activity |
| Medium | Low | Informational only |
| Critical | High | Noisy but still relevant |

### Tuning Documentation Template

| Field | Value |
|-------|-------|
| Rule Name | _[Alert rule name]_ |
| Current FP Rate | _[% false positives]_ |
| Tuning Applied | _[Description of change]_ |
| Justification | _[Why this is safe]_ |
| Validation Period | _[7/14/30 days]_ |
| Post-Tuning FP Rate | _[New % false positives]_ |
| Approved By | _[Analyst/Manager name]_ |
| Date | _[Date applied]_ |

### Golden Rules of Tuning
1. Never suppress without investigation — always understand the root cause
2. Document every tuning decision
3. Re-validate tuned rules quarterly
4. Track tuning metrics (FP rate before/after)
5. Never tune away true positives to reduce noise
`,
  },
  {
    id: "siem-r6",
    courseId: "siem-fundamentals",
    title: "SIEM Platform Comparison",
    type: "pdf",
    content: `
## SIEM Platform Comparison

### Feature Matrix

| Feature | Splunk | Microsoft Sentinel | Elastic SIEM | IBM QRadar |
|---------|--------|-------------------|-------------|------------|
| **Deployment** | On-prem / Cloud | Cloud-native | On-prem / Cloud | On-prem / Cloud |
| **Query Language** | SPL | KQL | EQL / KQL | AQL |
| **Learning Curve** | Moderate | Moderate | Steep | Moderate |
| **Pricing Model** | Data volume (GB/day) | Pay-as-you-go | Open source + paid | EPS-based |
| **Built-in SOAR** | Via Splunk SOAR | Logic Apps | No (3rd party) | IBM Resilient |
| **Threat Intel** | Enterprise Security | Built-in TI | Elastic TI module | X-Force |
| **ML/Analytics** | MLTK | Built-in UEBA | ML jobs | UBA |
| **Community** | Very large | Growing | Large | Moderate |

### Query Language Comparison

| Task | Splunk SPL | Sentinel KQL | Elastic |
|------|-----------|-------------|---------|
| Filter | \`search error\` | \`where Message has "error"\` | \`message: "error"\` |
| Count | \`stats count\` | \`summarize count()\` | Aggregation |
| Group by | \`by field\` | \`by field\` | \`terms\` agg |
| Time chart | \`timechart span=1h\` | \`bin(TimeGenerated, 1h)\` | \`date_histogram\` |
| Top N | \`top 10 field\` | \`top 10 by count_\` | \`terms size:10\` |
| Join | \`join\` | \`join kind=inner\` | Not native |

### Strengths & Weaknesses

**Splunk**
- ✅ Most mature, largest app ecosystem
- ✅ Powerful SPL query language
- ❌ Expensive at scale
- ❌ Complex licensing model

**Microsoft Sentinel**
- ✅ Native Azure/M365 integration
- ✅ Pay-per-query pricing
- ✅ Built-in SOAR (Logic Apps)
- ❌ Azure lock-in
- ❌ Learning KQL

**Elastic SIEM**
- ✅ Open-source core
- ✅ Flexible data model
- ❌ Steep learning curve
- ❌ Requires more manual setup

**IBM QRadar**
- ✅ Strong out-of-box rules
- ✅ Network flow analysis
- ❌ Aging interface
- ❌ Limited cloud-native features
`,
  },

  // ==========================================
  // NETWORK SECURITY MONITORING RESOURCES
  // ==========================================
  {
    id: "nsm-r1",
    courseId: "network-security-monitoring",
    title: "Wireshark Display Filter Cheat Sheet",
    type: "cheatsheet",
    content: `
## Wireshark Display Filter Quick Reference

### Protocol Filters

| Filter | Description |
|--------|-------------|
| \`tcp\` | All TCP traffic |
| \`udp\` | All UDP traffic |
| \`dns\` | DNS queries/responses |
| \`http\` | HTTP traffic |
| \`tls\` | TLS/SSL traffic |
| \`icmp\` | ICMP (ping) traffic |
| \`arp\` | ARP requests/replies |
| \`smb\` or \`smb2\` | SMB file sharing |
| \`dcerpc\` | RPC calls |
| \`kerberos\` | Kerberos auth |

### IP Address Filters

| Filter | Description |
|--------|-------------|
| \`ip.addr == 10.0.0.1\` | Source or destination IP |
| \`ip.src == 10.0.0.1\` | Source IP only |
| \`ip.dst == 10.0.0.1\` | Destination IP only |
| \`ip.addr == 10.0.0.0/24\` | Subnet filter |
| \`!(ip.addr == 10.0.0.1)\` | Exclude IP |

### Port Filters

| Filter | Description |
|--------|-------------|
| \`tcp.port == 443\` | Source or dest port |
| \`tcp.dstport == 80\` | Destination port |
| \`tcp.srcport == 4444\` | Source port |
| \`udp.port == 53\` | UDP port |

### HTTP Filters

| Filter | Description |
|--------|-------------|
| \`http.request.method == "POST"\` | POST requests |
| \`http.response.code == 200\` | HTTP 200 responses |
| \`http.response.code >= 400\` | HTTP errors |
| \`http.host contains "evil"\` | Host header match |
| \`http.request.uri contains "admin"\` | URL path match |
| \`http.user_agent contains "curl"\` | User agent match |

### DNS Filters

| Filter | Description |
|--------|-------------|
| \`dns.qry.name contains "evil"\` | Query name match |
| \`dns.qry.type == 1\` | A record queries |
| \`dns.qry.type == 28\` | AAAA record queries |
| \`dns.qry.type == 16\` | TXT record queries |
| \`dns.flags.response == 1\` | DNS responses only |
| \`dns.resp.len > 512\` | Large DNS responses |

### TLS Filters

| Filter | Description |
|--------|-------------|
| \`tls.handshake.type == 1\` | Client Hello |
| \`tls.handshake.extensions.server_name\` | SNI hostname |
| \`tls.handshake.ciphersuite\` | Cipher suites offered |

### Security-Focused Filters

\`\`\`
# Potential C2 beaconing (regular intervals)
tcp && !tcp.analysis.retransmission && tcp.len > 0

# DNS tunneling (long queries)
dns.qry.name.len > 50

# Suspicious outbound connections
ip.dst != 10.0.0.0/8 && ip.dst != 172.16.0.0/12 && ip.dst != 192.168.0.0/16 && tcp.flags.syn == 1

# SMB lateral movement
smb2.cmd == 5 || smb2.cmd == 3

# Cleartext credentials
http.authbasic || ftp.request.command == "PASS"
\`\`\`
`,
  },
  {
    id: "nsm-r2",
    courseId: "network-security-monitoring",
    title: "Suricata Rule Writing Guide",
    type: "pdf",
    content: `
## Suricata Rule Writing Reference

### Rule Syntax Structure
\`\`\`
action protocol src_ip src_port -> dest_ip dest_port (rule options)
\`\`\`

### Actions
| Action | Description |
|--------|-------------|
| \`alert\` | Generate alert |
| \`pass\` | Ignore packet |
| \`drop\` | Drop & alert (IPS) |
| \`reject\` | Drop & send RST |

### Rule Header Examples
\`\`\`
alert tcp $HOME_NET any -> $EXTERNAL_NET 443 (...)
alert dns any any -> any any (...)
alert http $HOME_NET any -> $EXTERNAL_NET any (...)
\`\`\`

### Content Matching

| Keyword | Description | Example |
|---------|-------------|---------|
| \`content\` | Byte/string match | \`content:"GET /admin";\` |
| \`nocase\` | Case-insensitive | \`content:"cmd.exe"; nocase;\` |
| \`depth\` | Search first N bytes | \`depth:50;\` |
| \`offset\` | Start after N bytes | \`offset:4;\` |
| \`distance\` | Bytes after last match | \`distance:0;\` |
| \`within\` | Max bytes for next match | \`within:100;\` |
| \`pcre\` | Regex matching | \`pcre:"/admin\\.(php|asp)/i";\` |
| \`startswith\` | Content at start | \`content:"GET"; startswith;\` |
| \`endswith\` | Content at end | \`content:".exe"; endswith;\` |

### Flow Keywords

| Keyword | Description |
|---------|-------------|
| \`flow:to_server,established\` | Client → Server, session active |
| \`flow:to_client,established\` | Server → Client, session active |
| \`flow:from_server\` | Any from server |
| \`flow:stateless\` | No flow tracking |

### Example Rules

\`\`\`
# Detect PowerShell download
alert http $HOME_NET any -> $EXTERNAL_NET any (
  msg:"Possible PowerShell Download Cradle";
  flow:to_server,established;
  content:"powershell"; nocase;
  content:"downloadstring"; nocase; distance:0;
  classtype:trojan-activity;
  sid:1000001; rev:1;)

# Detect DNS tunneling (long queries)
alert dns any any -> any any (
  msg:"Possible DNS Tunneling - Long Query";
  dns.query;
  content:"."; offset:50;
  classtype:bad-unknown;
  sid:1000002; rev:1;)

# Detect outbound connection to known bad port
alert tcp $HOME_NET any -> $EXTERNAL_NET 4444 (
  msg:"Outbound Connection on Meterpreter Default Port";
  flow:to_server,established;
  classtype:trojan-activity;
  sid:1000003; rev:1;)

# Detect EXE download over HTTP
alert http any any -> any any (
  msg:"EXE File Downloaded via HTTP";
  flow:to_client,established;
  content:"MZ"; startswith;
  content:"This program";
  classtype:policy-violation;
  sid:1000004; rev:1;)
\`\`\`

### Testing Rules
\`\`\`bash
# Validate syntax
suricata -T -c /etc/suricata/suricata.yaml -S custom.rules

# Test against PCAP
suricata -r capture.pcap -S custom.rules -l /tmp/output/

# Check alerts
cat /tmp/output/fast.log
\`\`\`
`,
  },
  {
    id: "nsm-r3",
    courseId: "network-security-monitoring",
    title: "Zeek Log Field Reference",
    type: "cheatsheet",
    content: `
## Zeek Log Field Reference

### conn.log (Connection Log)

| Field | Description |
|-------|-------------|
| \`ts\` | Timestamp |
| \`uid\` | Unique connection ID |
| \`id.orig_h\` | Source IP |
| \`id.orig_p\` | Source port |
| \`id.resp_h\` | Destination IP |
| \`id.resp_p\` | Destination port |
| \`proto\` | Protocol (tcp/udp/icmp) |
| \`service\` | Detected service |
| \`duration\` | Connection duration |
| \`orig_bytes\` | Bytes sent by source |
| \`resp_bytes\` | Bytes sent by dest |
| \`conn_state\` | Connection state |
| \`history\` | Connection history flags |

### Connection States
| State | Meaning |
|-------|---------|
| \`S0\` | SYN sent, no reply |
| \`S1\` | SYN-ACK seen |
| \`SF\` | Normal established/closed |
| \`REJ\` | Connection rejected |
| \`RSTO\` | Reset by originator |
| \`RSTR\` | Reset by responder |
| \`OTH\` | No SYN, midstream |

### dns.log

| Field | Description |
|-------|-------------|
| \`query\` | DNS query domain |
| \`qtype_name\` | Query type (A, AAAA, TXT) |
| \`rcode_name\` | Response code (NOERROR, NXDOMAIN) |
| \`answers\` | Resolved addresses |
| \`TTLs\` | Time-to-live values |

### http.log

| Field | Description |
|-------|-------------|
| \`method\` | HTTP method (GET, POST) |
| \`host\` | Requested host |
| \`uri\` | Request URI |
| \`user_agent\` | Browser/tool UA string |
| \`status_code\` | HTTP response code |
| \`resp_mime_types\` | Response content type |
| \`request_body_len\` | Upload size |
| \`response_body_len\` | Download size |

### ssl.log

| Field | Description |
|-------|-------------|
| \`server_name\` | SNI hostname |
| \`subject\` | Certificate subject |
| \`issuer\` | Certificate issuer |
| \`ja3\` | JA3 client fingerprint |
| \`ja3s\` | JA3S server fingerprint |
| \`validation_status\` | Cert validation result |

### files.log

| Field | Description |
|-------|-------------|
| \`mime_type\` | File MIME type |
| \`filename\` | Original filename |
| \`md5\` / \`sha1\` / \`sha256\` | File hashes |
| \`total_bytes\` | File size |
| \`source\` | Protocol it was seen in |

### Useful Zeek CLI Commands
\`\`\`bash
# Process PCAP with Zeek
zeek -r capture.pcap

# Top DNS queries
cat dns.log | zeek-cut query | sort | uniq -c | sort -rn | head 20

# Large file transfers
cat conn.log | zeek-cut id.orig_h id.resp_h orig_bytes | awk '$3 > 10000000'

# Connections to non-standard ports
cat conn.log | zeek-cut id.resp_h id.resp_p service | awk '$3 == "-"'
\`\`\`
`,
  },
  {
    id: "nsm-r4",
    courseId: "network-security-monitoring",
    title: "Network Attack Signatures",
    type: "pdf",
    content: `
## Network Attack Traffic Signatures

### Port Scanning

**SYN Scan (Stealth):**
- TCP SYN packets to many ports
- No completed handshakes (RST sent after SYN-ACK)
- Zeek: Many \`S0\` or \`REJ\` connection states from same source

**Connect Scan:**
- Full TCP handshakes followed by immediate RST
- Zeek: \`SF\` connections with 0 bytes transferred

**Detection:**
\`\`\`
conn.log: Same orig_h → many resp_p | duration < 1s | conn_state in (S0, REJ)
\`\`\`

---

### Command & Control (C2) Beaconing

**Characteristics:**
- Regular intervals between connections (±5% jitter)
- Consistent packet sizes
- Often HTTPS to obscure domains
- Low data volume per connection

**Detection:**
\`\`\`
conn.log: Group by (orig_h, resp_h)
Calculate time deltas between connections
Standard deviation of deltas < 10% of mean = beaconing
\`\`\`

---

### DNS Tunneling

**Indicators:**
- Unusually long subdomain strings (>50 chars)
- High volume of TXT record queries
- Base64/hex-encoded subdomains
- Many unique subdomains to same domain

**Example:**
\`\`\`
aGVsbG8gd29ybGQ.evil-tunnel.com (Base64 data in subdomain)
\`\`\`

---

### Data Exfiltration

**Network indicators:**
- Large outbound transfers to unusual destinations
- Uploads via DNS TXT records
- ICMP packets with large payloads
- Connections to cloud storage APIs

---

### Lateral Movement

**SMB-based:**
- SMB connections from workstations to workstations
- PsExec: SMB → named pipe creation → service installation
- Zeek: \`smb_files.log\` showing executable transfers

**RDP:**
- RDP connections between internal hosts
- Multiple RDP sessions from same source
- Zeek: \`conn.log\` with \`resp_p=3389\`

---

### Man-in-the-Middle

**ARP Spoofing:**
- Duplicate IP-MAC mappings
- ARP replies without requests
- Wireshark: \`arp.duplicate-address-detected\`

**SSL Stripping:**
- HTTP redirect to HTTPS missing
- Certificate mismatches
- Unexpected self-signed certificates
`,
  },
  {
    id: "nsm-r5",
    courseId: "network-security-monitoring",
    title: "PCAP Analysis Workflow Template",
    type: "template",
    content: `
## PCAP Analysis Workflow

### Phase 1: Initial Triage

- [ ] Open PCAP in Wireshark, review capture info (Statistics → Capture File Properties)
- [ ] Check capture duration and packet count
- [ ] Review Protocol Hierarchy (Statistics → Protocol Hierarchy)
- [ ] Note unusual protocols or high percentages
- [ ] Check Conversations (Statistics → Conversations) for top talkers

### Phase 2: Network Overview

| Finding | Details |
|---------|---------|
| **Capture Duration** | _[Start - End time]_ |
| **Total Packets** | _[Count]_ |
| **Unique Source IPs** | _[Count and list]_ |
| **Unique Dest IPs** | _[Count and list]_ |
| **Top Protocol** | _[Protocol and %]_ |
| **Unusual Ports** | _[Non-standard ports observed]_ |

### Phase 3: Targeted Analysis

- [ ] Filter for DNS: Check for suspicious domains, tunneling
- [ ] Filter for HTTP: Review requests, downloads, POST data
- [ ] Filter for TLS: Check SNI hostnames, certificate subjects
- [ ] Filter for SMB: Look for file transfers, lateral movement
- [ ] Check for cleartext credentials (FTP, Telnet, HTTP Basic)
- [ ] Look for encoded/obfuscated payloads

### Phase 4: IOC Extraction

| IOC Type | Value | Context |
|----------|-------|---------|
| IP Address | _[IP]_ | _[Why suspicious]_ |
| Domain | _[Domain]_ | _[Queried by host X]_ |
| URL | _[Full URL]_ | _[Downloaded payload]_ |
| File Hash | _[SHA256]_ | _[Extracted from stream]_ |
| User Agent | _[UA string]_ | _[Associated with malware]_ |
| JA3 Hash | _[JA3]_ | _[Known malware fingerprint]_ |

### Phase 5: Timeline

| Timestamp | Source | Destination | Activity |
|-----------|--------|-------------|----------|
| _[Time]_ | _[IP]_ | _[IP:Port]_ | _[Description]_ |

### Phase 6: Findings Summary

- **Attack Type:** _[Classification]_
- **Initial Vector:** _[How the attack started]_
- **Affected Hosts:** _[List of compromised systems]_
- **Data Impact:** _[What data was accessed/exfiltrated]_
- **Recommendations:** _[Containment and remediation steps]_
`,
  },
  {
    id: "nsm-r6",
    courseId: "network-security-monitoring",
    title: "BPF Filter Reference",
    type: "cheatsheet",
    content: `
## Berkeley Packet Filter (BPF) Reference

### Basic Syntax

| Filter | Description |
|--------|-------------|
| \`host 10.0.0.1\` | Traffic to/from host |
| \`src host 10.0.0.1\` | Traffic from host |
| \`dst host 10.0.0.1\` | Traffic to host |
| \`net 10.0.0.0/24\` | Traffic in subnet |
| \`port 80\` | Traffic on port |
| \`src port 443\` | Source port |
| \`dst port 22\` | Destination port |
| \`portrange 8000-9000\` | Port range |

### Protocol Filters

| Filter | Description |
|--------|-------------|
| \`tcp\` | TCP only |
| \`udp\` | UDP only |
| \`icmp\` | ICMP only |
| \`arp\` | ARP only |
| \`ip\` | IPv4 only |
| \`ip6\` | IPv6 only |

### Logical Operators

| Operator | Aliases | Example |
|----------|---------|---------|
| AND | \`and\`, \`&&\` | \`host 10.0.0.1 and port 80\` |
| OR | \`or\`, \`\\|\\|\` | \`port 80 or port 443\` |
| NOT | \`not\`, \`!\` | \`not port 22\` |
| Grouping | \`()\` | \`(port 80 or port 443) and host 10.0.0.1\` |

### TCP Flags

| Filter | Description |
|--------|-------------|
| \`tcp[tcpflags] & tcp-syn != 0\` | SYN flag set |
| \`tcp[tcpflags] & tcp-rst != 0\` | RST flag set |
| \`tcp[tcpflags] & tcp-fin != 0\` | FIN flag set |
| \`tcp[tcpflags] & tcp-ack != 0\` | ACK flag set |
| \`tcp[tcpflags] == tcp-syn\` | SYN only (no ACK) |

### Common Security Filters

\`\`\`bash
# Capture only SYN packets (port scan detection)
tcpdump -i eth0 'tcp[tcpflags] == tcp-syn'

# Outbound traffic to non-standard ports
tcpdump -i eth0 'dst net not 10.0.0.0/8 and dst port not 80 and dst port not 443 and dst port not 53'

# DNS traffic only
tcpdump -i eth0 'port 53'

# Large packets (potential exfiltration)
tcpdump -i eth0 'ip[2:2] > 1000'

# ICMP (potential tunneling)
tcpdump -i eth0 'icmp and ip[2:2] > 100'

# Capture to file
tcpdump -i eth0 -w capture.pcap 'host 10.0.0.1'

# Read from file with filter
tcpdump -r capture.pcap 'tcp port 4444'
\`\`\`
`,
  },

  // ==========================================
  // INCIDENT RESPONSE RESOURCES
  // ==========================================
  {
    id: "ir-r1",
    courseId: "incident-response",
    title: "IR Playbook Template",
    type: "template",
    content: `
## Incident Response Playbook Template

### Playbook Metadata

| Field | Value |
|-------|-------|
| **Playbook Name** | _[e.g., Ransomware Response]_ |
| **Version** | _[1.0]_ |
| **Last Updated** | _[Date]_ |
| **Owner** | _[IR Team Lead]_ |
| **Severity Scope** | _[Critical / High]_ |
| **MITRE Techniques** | _[T1486, T1059, etc.]_ |

---

### Phase 1: Detection & Identification

**Trigger Conditions:**
- [ ] _[Specific alert or indicator that activates this playbook]_
- [ ] _[Secondary confirmation criteria]_

**Initial Data Collection:**
- [ ] Alert source and timestamp
- [ ] Affected systems (hostname, IP, OS)
- [ ] Affected users and accounts
- [ ] Initial scope estimate

**Severity Assessment:**
| Factor | Low | Medium | High | Critical |
|--------|-----|--------|------|----------|
| Data sensitivity | Public | Internal | Confidential | Regulated/PII |
| Systems affected | 1 | 2-10 | 10-50 | >50 or critical infra |
| Business impact | None | Minor | Significant | Severe |

---

### Phase 2: Containment

**Immediate Actions (< 1 hour):**
- [ ] _[Action 1 — e.g., Isolate affected endpoint via EDR]_
- [ ] _[Action 2 — e.g., Block C2 IPs at firewall]_
- [ ] _[Action 3 — e.g., Disable compromised accounts]_

**Evidence Preservation:**
- [ ] Capture memory dump before isolation
- [ ] Preserve relevant log files
- [ ] Document all actions with timestamps

---

### Phase 3: Eradication

- [ ] _[Remove malware/persistence mechanisms]_
- [ ] _[Patch exploited vulnerability]_
- [ ] _[Reset all potentially compromised credentials]_
- [ ] _[Verify removal with full scan]_

---

### Phase 4: Recovery

- [ ] _[Restore from clean backup]_
- [ ] _[Apply security hardening]_
- [ ] _[Monitor for reinfection — duration: ___]_
- [ ] _[Validate system functionality]_
- [ ] _[Communicate restoration to stakeholders]_

---

### Phase 5: Post-Incident

- [ ] Conduct lessons learned meeting (within 5 business days)
- [ ] Write incident report
- [ ] Update detection rules
- [ ] Update this playbook if needed
- [ ] Track all improvement actions
`,
  },
  {
    id: "ir-r2",
    courseId: "incident-response",
    title: "NIST SP 800-61 Summary",
    type: "pdf",
    content: `
## NIST SP 800-61 Rev.2 — Summary

### Overview
The NIST Computer Security Incident Handling Guide provides a framework for preparing for, detecting, analyzing, containing, eradicating, and recovering from computer security incidents.

### The Four Phases

#### Phase 1: Preparation
- Establish incident response capability
- Define policies, plans, and procedures
- Build and train the IR team
- Acquire tools and resources
- Establish communication channels
- Conduct exercises and training

**Key Activities:**
- Create IR policy and plan documents
- Set up incident tracking system
- Prepare jump bags with forensic tools
- Establish relationships with external parties (law enforcement, ISACs)

#### Phase 2: Detection & Analysis
- Monitor security events from multiple sources
- Analyze alerts and correlate indicators
- Determine incident scope and impact
- Document findings and timeline

**Detection Sources:**
- SIEM alerts and correlation rules
- IDS/IPS notifications
- Antivirus/EDR detections
- User reports and help desk tickets
- Threat intelligence feeds
- Network flow anomalies

**Analysis Steps:**
1. Profile networks and systems (baseline)
2. Understand normal behaviors
3. Create log retention policy
4. Correlate events from multiple sources
5. Keep all clocks synchronized (NTP)

#### Phase 3: Containment, Eradication & Recovery
- **Containment:** Stop the incident from spreading
  - Short-term: Isolate, block, disable
  - Long-term: Patch, rebuild, harden
- **Eradication:** Remove threat components
  - Delete malware, remove persistence
  - Identify and patch root cause
- **Recovery:** Restore normal operations
  - Rebuild from clean media
  - Restore from backups
  - Validate system integrity
  - Monitor for recurrence

#### Phase 4: Post-Incident Activity
- Conduct lessons learned meetings
- Create detailed incident reports
- Track metrics (MTTD, MTTR, dwell time)
- Update policies and procedures
- Retain evidence per policy

### Incident Severity Categories (NIST)

| Category | Description | Examples |
|----------|-------------|---------|
| **CAT 1** | Unauthorized access | Root compromise, data breach |
| **CAT 2** | Denial of service | DDoS, resource exhaustion |
| **CAT 3** | Malicious code | Virus, worm, trojan |
| **CAT 4** | Improper usage | Policy violation |
| **CAT 5** | Scans/probes | Reconnaissance |
| **CAT 6** | Investigation | Unconfirmed incidents |
`,
  },
  {
    id: "ir-r3",
    courseId: "incident-response",
    title: "Evidence Collection Checklist",
    type: "cheatsheet",
    content: `
## Digital Evidence Collection Checklist

### Order of Volatility (Collect First → Last)

1. **CPU registers, cache** — Lost immediately
2. **Memory (RAM)** — Lost on power off
3. **Network connections** — Active state changes
4. **Running processes** — Change constantly
5. **Disk contents** — Persistent but modifiable
6. **Remote logging** — External copies
7. **Physical evidence** — Hardware, notes

### Memory Acquisition

- [ ] Record system time and timezone
- [ ] Capture full memory dump
  - **Windows:** \`winpmem_mini.exe output.raw\`
  - **Linux:** \`sudo dd if=/dev/mem of=memory.raw\`
  - **LiME:** \`insmod lime.ko "path=memory.lime format=lime"\`
- [ ] Record hash of memory dump
- [ ] Note acquisition tool and version

### Live System Data

\`\`\`bash
# Windows
date /t & time /t          # System time
hostname                    # Computer name
whoami /all                 # Current user context
tasklist /v                 # Running processes
netstat -anob              # Network connections
ipconfig /all              # Network config
arp -a                     # ARP cache
route print                # Routing table
net session                # Active sessions
net use                    # Mapped drives
schtasks /query /fo LIST   # Scheduled tasks
wmic startup get          # Startup programs

# Linux
date                       # System time
hostname                   # Computer name
whoami; id                 # Current user
ps auxf                    # Process tree
ss -tulnp                  # Network connections
ip addr                    # Network config
arp -n                     # ARP cache
route -n                   # Routing table
last -a                    # Login history
crontab -l                 # Scheduled tasks
\`\`\`

### Disk Imaging

- [ ] Use write blocker (hardware or software)
- [ ] Create forensic image (\`dd\`, FTK Imager, \`dc3dd\`)
- [ ] Hash original and image (MD5 + SHA256)
- [ ] Verify hashes match
- [ ] Store image on separate, clean media

### Chain of Custody Form

| Field | Value |
|-------|-------|
| **Evidence ID** | _[Unique identifier]_ |
| **Description** | _[What was collected]_ |
| **Source System** | _[Hostname/IP]_ |
| **Collected By** | _[Name and role]_ |
| **Date/Time** | _[When collected]_ |
| **Tool Used** | _[Collection tool]_ |
| **Hash (SHA256)** | _[Hash value]_ |
| **Storage Location** | _[Where stored]_ |
| **Transferred To** | _[Name, date, reason]_ |
`,
  },
  {
    id: "ir-r4",
    courseId: "incident-response",
    title: "Incident Severity Matrix",
    type: "template",
    content: `
## Incident Severity Classification Matrix

### Severity Levels

| Level | Name | Response Time | Examples |
|-------|------|---------------|---------|
| **S1** | Critical | Immediate (< 15 min) | Active ransomware, data breach, APT |
| **S2** | High | < 1 hour | Confirmed malware, lateral movement |
| **S3** | Medium | < 4 hours | Suspicious activity, policy violations |
| **S4** | Low | < 24 hours | Informational, minor deviations |

### Impact Assessment Matrix

|  | **Confidentiality** | **Integrity** | **Availability** |
|--|--------------------|--------------|-----------------| 
| **None** | No data exposed | No data modified | No service impact |
| **Low** | Internal data | Non-critical data | Minor degradation |
| **Medium** | Confidential data | Business data | Significant outage |
| **High** | PII / Regulated | Critical systems | Full outage |

### Severity Calculation

| Impact Score | Urgency | Final Severity |
|-------------|---------|----------------|
| High + High | Spreading actively | **S1 — Critical** |
| High + Medium | Contained but active | **S2 — High** |
| Medium + Medium | Moderate risk | **S3 — Medium** |
| Low + Low | Minimal risk | **S4 — Low** |

### Escalation Path

| Severity | Notify | Approve Actions | Update Frequency |
|----------|--------|----------------|-----------------|
| **S1** | CISO, Legal, Exec | CISO | Every 30 minutes |
| **S2** | IR Lead, SOC Mgr | IR Lead | Every 2 hours |
| **S3** | SOC Manager | SOC Manager | Every 8 hours |
| **S4** | Team Lead | Analyst | Daily |

### Communication Template

**Subject:** [SEVERITY] Security Incident — [Brief Description]

**Body:**
- **Incident ID:** [ID]
- **Severity:** [S1-S4]
- **Status:** [Investigating / Contained / Resolved]
- **Impact:** [Systems/users/data affected]
- **Current Actions:** [What's being done]
- **Next Update:** [When]
- **Contact:** [IR Lead name and phone]
`,
  },
  {
    id: "ir-r5",
    courseId: "incident-response",
    title: "Post-Incident Report Template",
    type: "template",
    content: `
## Post-Incident Report Template

### Executive Summary

| Field | Details |
|-------|---------|
| **Incident ID** | _[IR-2024-XXX]_ |
| **Date Detected** | _[Date/Time]_ |
| **Date Contained** | _[Date/Time]_ |
| **Date Resolved** | _[Date/Time]_ |
| **Severity** | _[S1/S2/S3/S4]_ |
| **Classification** | _[Malware/Phishing/Breach/etc.]_ |
| **Impact Summary** | _[1-2 sentence business impact]_ |

---

### Incident Timeline

| Date/Time | Event | Source |
|-----------|-------|--------|
| _[Timestamp]_ | _[Initial compromise]_ | _[How detected]_ |
| _[Timestamp]_ | _[Alert triggered]_ | _[SIEM/EDR]_ |
| _[Timestamp]_ | _[Investigation started]_ | _[Analyst]_ |
| _[Timestamp]_ | _[Containment actions]_ | _[Actions taken]_ |
| _[Timestamp]_ | _[Eradication complete]_ | _[Verified by]_ |
| _[Timestamp]_ | _[Recovery complete]_ | _[Systems restored]_ |

---

### Technical Analysis

**Attack Vector:**
_[How the attacker gained initial access]_

**MITRE ATT&CK Mapping:**

| Tactic | Technique | Details |
|--------|-----------|---------|
| Initial Access | _[T-ID]_ | _[Description]_ |
| Execution | _[T-ID]_ | _[Description]_ |
| Persistence | _[T-ID]_ | _[Description]_ |
| Lateral Movement | _[T-ID]_ | _[Description]_ |

**Indicators of Compromise:**

| IOC Type | Value | Context |
|----------|-------|---------|
| IP | _[IP address]_ | _[C2 server]_ |
| Domain | _[Domain]_ | _[Phishing domain]_ |
| Hash (SHA256) | _[Hash]_ | _[Malware sample]_ |
| Email | _[Address]_ | _[Sender]_ |

---

### Impact Assessment

| Category | Impact | Details |
|----------|--------|---------|
| Systems | _[Count]_ | _[List of affected systems]_ |
| Users | _[Count]_ | _[Affected user accounts]_ |
| Data | _[Classification]_ | _[Type of data exposed]_ |
| Business | _[Duration]_ | _[Operational impact]_ |
| Financial | _[Estimate]_ | _[Cost of incident]_ |

---

### Lessons Learned & Recommendations

| # | Finding | Recommendation | Priority | Owner |
|---|---------|---------------|----------|-------|
| 1 | _[What went wrong]_ | _[How to prevent]_ | _[H/M/L]_ | _[Team]_ |
| 2 | _[Gap identified]_ | _[Improvement needed]_ | _[H/M/L]_ | _[Team]_ |
| 3 | _[What went well]_ | _[Continue/expand]_ | _[—]_ | _[Team]_ |

---

**Report Author:** _[Name]_
**Reviewed By:** _[IR Lead]_
**Distribution:** _[List of recipients]_
`,
  },
  {
    id: "ir-r6",
    courseId: "incident-response",
    title: "Containment Decision Tree",
    type: "pdf",
    content: `
## Containment Decision Framework

### Decision Factors

Before choosing a containment strategy, evaluate:

1. **Is the threat actively spreading?** → Immediate isolation
2. **Is data being exfiltrated?** → Block outbound immediately
3. **Is the system business-critical?** → Balance isolation vs availability
4. **Do we have good backups?** → Determines recovery options
5. **Is evidence preservation needed?** → Memory capture before isolation

### Containment Options

#### Option 1: Full Network Isolation
**When:** Active ransomware, confirmed APT, active exfiltration
- Disconnect from network (EDR isolation preferred)
- Maintain power for memory preservation
- No remote access until cleared

#### Option 2: Partial Network Isolation
**When:** Suspected compromise, investigation needed
- Block internet access, allow internal for monitoring
- Restrict to specific VLANs
- Allow IR team remote access only

#### Option 3: Account-Level Containment
**When:** Credential compromise, insider threat
- Disable compromised accounts
- Force password reset
- Revoke all active sessions and tokens
- Enable enhanced monitoring on account

#### Option 4: Application-Level Containment
**When:** Web app compromise, API abuse
- Block malicious IPs at WAF/proxy
- Disable compromised API keys
- Put application in maintenance mode
- Increase logging verbosity

#### Option 5: DNS Sinkholing
**When:** Malware with known C2 domains
- Redirect C2 domains to sinkhole
- Monitor which hosts attempt C2 contact
- Identifies scope without alerting attacker

### Containment Checklist

| Action | Completed | Notes |
|--------|-----------|-------|
| Memory captured | ☐ | Before isolation |
| Network isolated | ☐ | Method used |
| Accounts disabled | ☐ | Which accounts |
| C2 blocked | ☐ | IPs/domains blocked |
| Evidence preserved | ☐ | Logs, images, captures |
| Stakeholders notified | ☐ | Who was informed |
| Monitoring enhanced | ☐ | Additional logging |

### Common Mistakes to Avoid
1. ❌ Shutting down systems (destroys volatile evidence)
2. ❌ Running antivirus before preserving evidence
3. ❌ Alerting the attacker by visible actions
4. ❌ Not documenting containment actions
5. ❌ Incomplete containment (missing lateral access)
6. ❌ Forgetting to contain cloud/SaaS access
`,
  },

  // ==========================================
  // THREAT HUNTING RESOURCES
  // ==========================================
  {
    id: "th-r1",
    courseId: "threat-hunting",
    title: "Threat Hunting Hypothesis Templates",
    type: "template",
    content: `
## Threat Hunting Hypothesis Templates

### Template Structure

**Hypothesis:** _[Statement about what you expect to find]_
**ATT&CK Technique:** _[T-ID and name]_
**Data Sources:** _[Logs/telemetry needed]_
**Analytics:** _[Queries/logic to test hypothesis]_
**Expected Evidence:** _[What a positive finding looks like]_

---

### Hypothesis 1: Credential Dumping via LSASS Access

**Hypothesis:** An attacker has accessed the LSASS process to dump credentials.
**ATT&CK:** T1003.001 — OS Credential Dumping: LSASS Memory
**Data Sources:** Sysmon Event ID 10 (ProcessAccess), EDR telemetry
**Analytics:**
\`\`\`
ProcessAccess events where:
  TargetImage = "*\\\\lsass.exe"
  AND SourceImage NOT IN (known legitimate tools)
  AND GrantedAccess includes 0x1010 or 0x1FFFFF
\`\`\`
**Expected Evidence:** Non-system processes accessing LSASS with suspicious access rights.

---

### Hypothesis 2: Living Off the Land — Certutil Abuse

**Hypothesis:** An attacker is using certutil.exe to download files.
**ATT&CK:** T1105 — Ingress Tool Transfer
**Data Sources:** Sysmon Event ID 1, Windows Event ID 4688
**Analytics:**
\`\`\`
Process creation where:
  Image = "*\\\\certutil.exe"
  AND CommandLine contains ("-urlcache" OR "-split" OR "http")
\`\`\`
**Expected Evidence:** Certutil executions with URL parameters downloading remote files.

---

### Hypothesis 3: Scheduled Task Persistence

**Hypothesis:** An attacker has created scheduled tasks for persistence.
**ATT&CK:** T1053.005 — Scheduled Task/Job
**Data Sources:** Windows Event ID 4698, Sysmon Event ID 1
**Analytics:**
\`\`\`
Event ID 4698 (Task Created) where:
  TaskContent contains suspicious paths (Temp, AppData, ProgramData)
  OR Creator is not a known admin account
  OR Action executable is script-based (.ps1, .bat, .vbs)
\`\`\`
**Expected Evidence:** New tasks created by non-admin users pointing to suspicious locations.

---

### Hypothesis 4: DNS Beaconing to C2

**Hypothesis:** A compromised host is beaconing to a C2 server via DNS.
**ATT&CK:** T1071.004 — Application Layer Protocol: DNS
**Data Sources:** DNS query logs, Zeek dns.log, passive DNS
**Analytics:**
\`\`\`
DNS queries where:
  Query frequency to same domain is regular (±10% jitter)
  AND Domain is not in top 1M Alexa/Umbrella
  AND Query volume from same host > 100/day to same domain
\`\`\`
**Expected Evidence:** Regular-interval DNS queries to low-reputation domains.

---

### Hypothesis 5: Lateral Movement via RDP

**Hypothesis:** An attacker is pivoting through the network using RDP.
**ATT&CK:** T1021.001 — Remote Services: RDP
**Data Sources:** Windows Event ID 4624 (Type 10), firewall logs
**Analytics:**
\`\`\`
Event ID 4624, Logon Type 10 where:
  Source is a workstation (not admin jump box)
  AND Destination is another workstation
  OR Source has active malware alert
\`\`\`
**Expected Evidence:** Workstation-to-workstation RDP sessions, especially from flagged hosts.

---

### Blank Template

**Hypothesis:** _____
**ATT&CK:** T____ — _____
**Data Sources:** _____
**Analytics:**
\`\`\`
[Query logic]
\`\`\`
**Expected Evidence:** _____
**Outcome:** ☐ Confirmed  ☐ Not Found  ☐ Inconclusive
**Follow-up:** _____
`,
  },
  {
    id: "th-r2",
    courseId: "threat-hunting",
    title: "Pyramid of Pain Reference",
    type: "cheatsheet",
    content: `
## Pyramid of Pain — Quick Reference

### The Pyramid (Bottom to Top)

| Level | Indicator Type | Adversary Pain | Analyst Value |
|-------|---------------|---------------|---------------|
| 🔵 **1** | Hash Values (MD5/SHA) | Trivial | Low — easily changed |
| 🔵 **2** | IP Addresses | Easy | Low — infrastructure rotates |
| 🟢 **3** | Domain Names | Simple | Moderate — requires new registration |
| 🟡 **4** | Network/Host Artifacts | Annoying | Good — requires tool changes |
| 🟠 **5** | Tools | Challenging | High — requires new tooling |
| 🔴 **6** | TTPs (Tactics, Techniques, Procedures) | Tough! | Highest — requires new tradecraft |

### Detection Strategy by Level

**Level 1 — Hash Values:**
- Block known-bad file hashes
- Easy to bypass: recompile, add null byte
- Use for: Immediate blocking, not long-term detection

**Level 2 — IP Addresses:**
- Block C2 IPs at firewall
- Easy to bypass: new VPS, Tor, CDN
- Use for: Short-term blocking during active incidents

**Level 3 — Domain Names:**
- Block C2 domains at DNS/proxy
- Moderate effort to bypass: new domain registration
- Use for: Campaign tracking, DNS sinkholing

**Level 4 — Artifacts:**
- Detect specific registry keys, file paths, mutexes, user-agents
- Annoying to change: requires tool reconfiguration
- Use for: Behavioral signatures, Sysmon rules

**Level 5 — Tools:**
- Detect tool-specific behaviors (Cobalt Strike, Mimikatz patterns)
- Hard to bypass: requires developing new tools
- Use for: YARA rules, behavioral detection

**Level 6 — TTPs:**
- Detect the technique regardless of tool
- Hardest to bypass: requires entirely new attack methodology
- Use for: MITRE ATT&CK-based detection rules

### Hunting Priority
Focus hunting efforts on Levels 4-6 for maximum impact. Lower levels are useful for immediate response but provide diminishing returns for proactive hunting.
`,
  },
  {
    id: "th-r3",
    courseId: "threat-hunting",
    title: "LOLBins & LOLScripts Reference",
    type: "cheatsheet",
    content: `
## Living Off the Land Binaries & Scripts

### Common LOLBins (Windows)

| Binary | Malicious Use | Detection |
|--------|--------------|-----------|
| \`certutil.exe\` | File download, Base64 decode | CommandLine contains \`-urlcache\` or \`-decode\` |
| \`mshta.exe\` | Execute HTA/VBScript | Any execution from non-standard path |
| \`rundll32.exe\` | Execute DLL exports | Unusual DLL paths, network activity |
| \`regsvr32.exe\` | Execute COM scriptlets | \`/s /n /u /i:http\` flags |
| \`wmic.exe\` | Remote execution, recon | \`process call create\`, \`/node:\` |
| \`powershell.exe\` | Script execution | \`-enc\`, \`-nop\`, \`IEX\`, \`downloadstring\` |
| \`cscript/wscript\` | Script execution | Executing from Temp/Downloads |
| \`msiexec.exe\` | Install remote MSI | \`/i http://\` URLs |
| \`bitsadmin.exe\` | File download | \`/transfer\` with external URLs |
| \`schtasks.exe\` | Persistence | \`/create\` with suspicious commands |
| \`sc.exe\` | Service manipulation | \`create\` or \`config\` with binpath |
| \`net.exe\` | Recon, account manipulation | \`user /add\`, \`localgroup administrators /add\` |

### Common LOLBins (Linux)

| Binary | Malicious Use | Detection |
|--------|--------------|-----------|
| \`curl\` / \`wget\` | File download | Download to /tmp, pipe to bash |
| \`python\` | Reverse shell, script exec | \`-c 'import socket\` |
| \`perl\` | Reverse shell | \`-e 'use Socket'\` |
| \`nc\` / \`ncat\` | Reverse shell, data exfil | \`-e /bin/bash\` |
| \`socat\` | Reverse shell | \`exec:/bin/bash\` |
| \`crontab\` | Persistence | Unexpected cron modifications |
| \`at\` | Persistence | Scheduled commands |
| \`ssh\` | Tunneling, pivoting | \`-D\`, \`-L\`, \`-R\` flags |

### Detection Strategies

**Parent-Child Process Anomalies:**
- Word/Excel → cmd.exe → powershell.exe
- Explorer → mshta.exe
- svchost.exe → cmd.exe (unusual parent)

**Command-Line Red Flags:**
- Base64-encoded strings (> 50 chars)
- URL parameters in system binaries
- \`-nop -w hidden -enc\` PowerShell flags
- Pipes to \`bash\` or \`sh\`
- \`/dev/tcp\` in bash commands
`,
  },
  {
    id: "th-r4",
    courseId: "threat-hunting",
    title: "Hunt Report Template",
    type: "template",
    content: `
## Threat Hunt Report Template

### Hunt Metadata

| Field | Value |
|-------|-------|
| **Hunt ID** | _[TH-2024-XXX]_ |
| **Hunt Name** | _[Descriptive name]_ |
| **Hunter** | _[Analyst name]_ |
| **Date Range** | _[Start — End]_ |
| **Data Sources** | _[Logs/telemetry queried]_ |
| **ATT&CK Techniques** | _[T-IDs targeted]_ |
| **Status** | ☐ Complete ☐ Requires Follow-up |

### Hypothesis

_[Clear, testable statement about what threat behavior you expect to find]_

### Methodology

1. _[Step 1: Data collection approach]_
2. _[Step 2: Query/analysis technique]_
3. _[Step 3: Validation steps]_

### Queries Used

\`\`\`
[Include actual queries run with annotations]
\`\`\`

### Findings

| # | Finding | Severity | Hosts Affected |
|---|---------|----------|----------------|
| 1 | _[Description]_ | _[H/M/L]_ | _[Count/List]_ |
| 2 | _[Description]_ | _[H/M/L]_ | _[Count/List]_ |

### IOCs Discovered

| Type | Value | Context |
|------|-------|---------|
| _[IP/Domain/Hash]_ | _[Value]_ | _[Where found]_ |

### Recommendations

| # | Recommendation | Type | Priority |
|---|---------------|------|----------|
| 1 | _[Action item]_ | Detection Rule | _[H/M/L]_ |
| 2 | _[Action item]_ | Configuration | _[H/M/L]_ |
| 3 | _[Action item]_ | Process | _[H/M/L]_ |

### Detection Engineering Output

_[New SIGMA/Splunk/KQL rules to be created based on findings]_

### Conclusion

_[Summary: hypothesis confirmed/denied, key takeaways, follow-up hunts needed]_
`,
  },
  {
    id: "th-r5",
    courseId: "threat-hunting",
    title: "JA3/JA3S Fingerprint Database",
    type: "pdf",
    content: `
## JA3/JA3S TLS Fingerprint Reference

### What is JA3?
JA3 is a method for creating SSL/TLS client fingerprints based on the Client Hello packet. It captures: TLS version, ciphers, extensions, elliptic curves, and EC point formats.

### What is JA3S?
JA3S fingerprints the server's response (Server Hello) to create a server-side TLS fingerprint.

### Known Malicious JA3 Hashes

| JA3 Hash | Associated Tool/Malware |
|----------|------------------------|
| \`a0e9f5d64349fb13191bc781f81f42e1\` | Cobalt Strike |
| \`72a589da586844d7f0818ce684948eea\` | Cobalt Strike (variants) |
| \`e7d705a3286e19ea42f587b344ee6865\` | Metasploit Meterpreter |
| \`6734f37431670b3ab4292b8f60f29984\` | Trickbot |
| \`c12f54a3f91dc7bafd92cb59fe009a35\` | IcedID |
| \`51c64c77e60f3980eea90869b68c58a8\` | QakBot |
| \`3b5074b1b5d032e5620f69f9f700ff0e\` | Emotet |
| \`b386946a5a44d1ddcc843bc75336dfce\` | Dridex |

### Common Legitimate JA3 Hashes

| JA3 Hash | Client |
|----------|--------|
| \`b32309a26951912be7dba376398abc3b\` | Chrome (Windows) |
| \`473cd7cb9faa642487833865d516e578\` | Firefox |
| \`2d1eb5817199e4d95574b3e3c7cd5cf4\` | Safari |
| \`d529025a4f02501a92e8da2b1c56ea37\` | curl |
| \`1138de370e523e824bbfc608cc3c4471\` | Python requests |

### Using JA3 for Threat Hunting

**Zeek (conn.log + ssl.log):**
\`\`\`bash
# Find Cobalt Strike JA3
cat ssl.log | zeek-cut ja3 server_name | grep "a0e9f5d64349fb13191bc781f81f42e1"
\`\`\`

**Splunk:**
\`\`\`spl
index=zeek sourcetype=zeek:ssl ja3="a0e9f5d64349fb13191bc781f81f42e1"
| stats count by src_ip, dest_ip, server_name
\`\`\`

**Sentinel (KQL):**
\`\`\`kql
CommonSecurityLog
| where DeviceCustomString1 == "a0e9f5d64349fb13191bc781f81f42e1"
| summarize count() by SourceIP, DestinationIP
\`\`\`

### Hunting Strategies
1. **Baseline legitimate JA3s** in your environment
2. **Alert on new/rare JA3s** not seen before
3. **Cross-reference** with known-bad JA3 database
4. **Combine JA3 + JA3S** for unique client-server fingerprints
5. **Track JA3 changes** for same client application (may indicate tampering)
`,
  },
  {
    id: "th-r6",
    courseId: "threat-hunting",
    title: "Threat Hunting Query Library",
    type: "cheatsheet",
    content: `
## Threat Hunting Query Library

### Discovery & Reconnaissance

**Unusual Recon Commands (Splunk):**
\`\`\`spl
index=sysmon EventCode=1
(CommandLine="*whoami*" OR CommandLine="*ipconfig*" OR CommandLine="*net user*"
 OR CommandLine="*net group*" OR CommandLine="*systeminfo*" OR CommandLine="*nltest*")
| stats count values(CommandLine) by Computer, User
| where count > 3
\`\`\`

**Unusual Recon Commands (KQL):**
\`\`\`kql
DeviceProcessEvents
| where ProcessCommandLine has_any ("whoami", "ipconfig", "net user", "net group", "systeminfo")
| summarize CommandCount=count(), Commands=make_set(ProcessCommandLine) by DeviceName, AccountName
| where CommandCount > 3
\`\`\`

### Persistence

**New Scheduled Tasks (Splunk):**
\`\`\`spl
index=wineventlog EventCode=4698
| rex field=TaskContent "<Command>(?<task_command>[^<]+)</Command>"
| where NOT match(task_command, "(?i)(windows|microsoft|google|adobe)")
| table _time, Computer, SubjectUserName, TaskName, task_command
\`\`\`

### Execution

**Suspicious PowerShell (Splunk):**
\`\`\`spl
index=sysmon EventCode=1 Image="*powershell.exe"
(CommandLine="*-enc*" OR CommandLine="*-nop*" OR CommandLine="*hidden*"
 OR CommandLine="*bypass*" OR CommandLine="*IEX*" OR CommandLine="*downloadstring*")
| table _time, Computer, User, ParentImage, CommandLine
\`\`\`

### Lateral Movement

**RDP from Non-Admin Sources (Splunk):**
\`\`\`spl
index=wineventlog EventCode=4624 Logon_Type=10
| where NOT match(Source_Network_Address, "(10\\.0\\.1\\.(50|51|52))")
| stats count by Source_Network_Address, Account_Name, Workstation_Name
| sort -count
\`\`\`

### Credential Access

**LSASS Access (Splunk):**
\`\`\`spl
index=sysmon EventCode=10 TargetImage="*\\\\lsass.exe"
| where NOT match(SourceImage, "(?i)(csrss|lsass|svchost|MsMpEng|CrowdStrike)")
| table _time, Computer, SourceImage, GrantedAccess
\`\`\`

### Exfiltration

**Large Outbound Transfers (Splunk):**
\`\`\`spl
index=firewall action=allowed direction=outbound
| stats sum(bytes_out) as total_bytes by src_ip, dest_ip
| where total_bytes > 104857600
| eval mb=round(total_bytes/1048576, 2)
| sort -total_bytes
\`\`\`

### DNS Anomalies

**Long DNS Queries — Potential Tunneling (Splunk):**
\`\`\`spl
index=dns
| eval query_len=len(query)
| where query_len > 50
| stats count avg(query_len) by query, src_ip
| sort -count
\`\`\`
`,
  },

  // ==========================================
  // DETECTION ENGINEERING RESOURCES
  // ==========================================
  {
    id: "de-r1",
    courseId: "detection-engineering",
    title: "SIGMA Rule Syntax Cheat Sheet",
    type: "cheatsheet",
    content: `
## SIGMA Rule Syntax Quick Reference

### Rule Structure

\`\`\`yaml
title: Rule Title
id: UUID
status: experimental | test | stable
description: What this rule detects
author: Your Name
date: 2024/01/15
modified: 2024/06/01
references:
  - https://example.com/threat-report
tags:
  - attack.execution
  - attack.t1059.001
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    field_name: value
  condition: selection
falsepositives:
  - Legitimate admin usage
level: high
\`\`\`

### Log Source Categories

| Category | Description |
|----------|-------------|
| \`process_creation\` | New process started |
| \`file_event\` | File created/modified |
| \`network_connection\` | Network activity |
| \`registry_event\` | Registry changes |
| \`dns_query\` | DNS lookups |
| \`image_load\` | DLL/module loaded |
| \`ps_script\` | PowerShell script blocks |

### Detection Modifiers

| Modifier | Description | Example |
|----------|-------------|---------|
| (none) | Exact match | \`CommandLine: whoami\` |
| \`contains\` | Substring | \`CommandLine|contains: '-enc'\` |
| \`startswith\` | Starts with | \`Image|startswith: 'C:\\\\Temp'\` |
| \`endswith\` | Ends with | \`Image|endswith: '\\\\cmd.exe'\` |
| \`re\` | Regex | \`CommandLine|re: '.*base64.*'\` |
| \`all\` | All values must match | \`CommandLine|contains|all:\` |
| \`base64\` | Base64-encoded match | \`CommandLine|base64: 'payload'\` |

### Condition Logic

\`\`\`yaml
# AND (both must match)
condition: selection1 AND selection2

# OR (either matches)
condition: selection1 OR selection2

# NOT (exclude)
condition: selection AND NOT filter

# Count-based
condition: selection | count(src_ip) > 10

# Temporal
condition: selection | near(selection2, 5m)
\`\`\`

### Wildcards

\`\`\`yaml
# Asterisk for any characters
CommandLine: '*certutil* -urlcache*'

# Question mark for single character
EventID: 462?
\`\`\`

### Conversion Targets
\`\`\`bash
# Convert to Splunk
sigma convert -t splunk rule.yml

# Convert to Sentinel KQL
sigma convert -t microsoft365defender rule.yml

# Convert to Elastic
sigma convert -t elasticsearch rule.yml

# Convert to QRadar
sigma convert -t qradar rule.yml
\`\`\`
`,
  },
  {
    id: "de-r2",
    courseId: "detection-engineering",
    title: "YARA Rule Writing Guide",
    type: "pdf",
    content: `
## YARA Rule Writing Reference

### Basic Rule Structure

\`\`\`yara
rule RuleName {
    meta:
        author = "Your Name"
        description = "What this detects"
        date = "2024-01-15"
        reference = "https://example.com"
        hash = "abc123..."
        
    strings:
        $s1 = "suspicious string"
        $s2 = { 4D 5A 90 00 }  // hex pattern
        $s3 = /regex[0-9]+pattern/i  // regex
        
    condition:
        uint16(0) == 0x5A4D and  // PE file check
        2 of ($s*)
}
\`\`\`

### String Types

| Type | Syntax | Example |
|------|--------|---------|
| Text | \`"string"\` | \`$a = "CreateRemoteThread"\` |
| Hex | \`{ XX XX }\` | \`$b = { 4D 5A 90 00 }\` |
| Regex | \`/pattern/\` | \`$c = /cmd\\.exe.*/i\` |

### String Modifiers

| Modifier | Description |
|----------|-------------|
| \`nocase\` | Case-insensitive |
| \`wide\` | Unicode (UTF-16LE) |
| \`ascii\` | ASCII encoding |
| \`fullword\` | Whole word match |
| \`xor\` | XOR-encoded variants |
| \`base64\` | Base64-encoded |

### Condition Operators

\`\`\`yara
// Count-based
condition: 2 of ($s*)           // Any 2 strings
condition: all of ($s*)          // All strings
condition: any of ($api*)        // Any from group

// Size-based
condition: filesize < 1MB
condition: filesize > 100KB

// PE-specific
condition: pe.imports("kernel32.dll", "VirtualAlloc")
condition: pe.number_of_sections > 5
condition: pe.entry_point == 0x1000

// Math module
condition: math.entropy(0, filesize) > 7.0

// Position-based
condition: $mz at 0             // At specific offset
condition: $s1 in (0..1024)     // Within range
\`\`\`

### Example Detection Rules

\`\`\`yara
rule Suspicious_PowerShell_Download {
    meta:
        description = "Detects PowerShell download cradles"
    strings:
        $a1 = "DownloadString" nocase
        $a2 = "DownloadFile" nocase
        $a3 = "Invoke-WebRequest" nocase
        $a4 = "wget" nocase
        $a5 = "curl" nocase
        $b1 = "IEX" nocase
        $b2 = "Invoke-Expression" nocase
    condition:
        any of ($a*) and any of ($b*)
}

rule Packed_Executable {
    meta:
        description = "Detects potentially packed PE files"
    condition:
        uint16(0) == 0x5A4D and
        math.entropy(0, filesize) > 7.0 and
        filesize < 5MB
}
\`\`\`

### Testing
\`\`\`bash
# Scan single file
yara rule.yar suspect.exe

# Scan directory
yara -r rule.yar /path/to/scan/

# Show matching strings
yara -s rule.yar suspect.exe

# Multiple rule files
yara rules/ suspect.exe
\`\`\`
`,
  },
  {
    id: "de-r3",
    courseId: "detection-engineering",
    title: "Detection-as-Code Pipeline Template",
    type: "template",
    content: `
## Detection-as-Code CI/CD Pipeline Template

### Repository Structure

\`\`\`
detection-rules/
├── rules/
│   ├── sigma/
│   │   ├── windows/
│   │   │   ├── process_creation/
│   │   │   ├── registry_event/
│   │   │   └── network_connection/
│   │   └── linux/
│   ├── yara/
│   │   ├── malware/
│   │   └── webshells/
│   └── custom/
│       ├── splunk/
│       └── sentinel/
├── tests/
│   ├── unit/
│   └── integration/
├── lib/
│   └── helpers/
├── .github/
│   └── workflows/
│       └── detection-pipeline.yml
├── config/
│   └── sigma-config.yml
└── README.md
\`\`\`

### CI/CD Pipeline Stages

#### Stage 1: Validate
- [ ] SIGMA YAML syntax validation
- [ ] YARA rule compilation check
- [ ] Required metadata fields present (author, date, description, level)
- [ ] ATT&CK tag format validation

#### Stage 2: Test
- [ ] Unit tests with sample log data
- [ ] False positive rate estimation
- [ ] Backend conversion test (SIGMA → SPL/KQL)
- [ ] YARA rule performance benchmark

#### Stage 3: Review
- [ ] Automated PR creation
- [ ] Peer review required (1+ approver)
- [ ] Detection coverage report generated
- [ ] Change log updated

#### Stage 4: Deploy
- [ ] Convert to target SIEM format
- [ ] Deploy to staging environment
- [ ] 24-hour monitoring period
- [ ] Promote to production

### GitHub Actions Workflow

\`\`\`yaml
name: Detection Pipeline
on:
  push:
    paths: ['rules/**']
  pull_request:
    paths: ['rules/**']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate SIGMA rules
        run: sigma check rules/sigma/
      - name: Compile YARA rules
        run: yara -w rules/yara/*.yar /dev/null

  test:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - name: Run unit tests
        run: python -m pytest tests/unit/
      - name: Convert SIGMA rules
        run: sigma convert -t splunk rules/sigma/ > output/splunk/

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to SIEM
        run: ./scripts/deploy.sh
\`\`\`

### Rule Naming Convention
\`\`\`
[product]_[category]_[technique]_[description].yml

Examples:
windows_process_creation_certutil_download.yml
linux_network_connection_reverse_shell.yml
cloud_aws_iam_user_creation.yml
\`\`\`
`,
  },
  {
    id: "de-r4",
    courseId: "detection-engineering",
    title: "ATT&CK Coverage Mapping Template",
    type: "template",
    content: `
## ATT&CK Detection Coverage Mapping

### Coverage Levels

| Level | Description | Color Code |
|-------|-------------|------------|
| **0 — None** | No detection capability | ⬜ White |
| **1 — Minimal** | Basic IOC matching only | 🟦 Light Blue |
| **2 — Partial** | Some behavioral detection | 🟨 Yellow |
| **3 — Good** | Reliable detection with low FP | 🟧 Orange |
| **4 — Excellent** | Multiple detection methods, tested | 🟥 Red |

### Coverage Tracker

| Tactic | Technique | ID | Detection Level | Rule ID | Notes |
|--------|-----------|-----|-----------------|---------|-------|
| Initial Access | Phishing | T1566 | 3 | _[ID]_ | Email gateway + SIEM |
| Execution | PowerShell | T1059.001 | 4 | _[ID]_ | ScriptBlock + Sysmon |
| Execution | Command Shell | T1059.003 | 3 | _[ID]_ | Process creation |
| Persistence | Scheduled Task | T1053.005 | 3 | _[ID]_ | Event ID 4698 |
| Persistence | Registry Run Keys | T1547.001 | 2 | _[ID]_ | Sysmon 12/13 |
| Priv Escalation | Token Manipulation | T1134 | 1 | _[ID]_ | Limited visibility |
| Defense Evasion | Masquerading | T1036 | 2 | _[ID]_ | Path anomalies |
| Credential Access | LSASS Memory | T1003.001 | 4 | _[ID]_ | Sysmon 10 + EDR |
| Discovery | System Info | T1082 | 2 | _[ID]_ | Command monitoring |
| Lateral Movement | RDP | T1021.001 | 3 | _[ID]_ | 4624 Type 10 |
| Collection | Data Staging | T1074 | 1 | _[ID]_ | File monitoring |
| Exfiltration | Over C2 | T1041 | 2 | _[ID]_ | Network anomalies |
| Impact | Data Encrypted | T1486 | 3 | _[ID]_ | Ransomware behavior |

### Coverage Summary

| Tactic | Techniques Mapped | Avg Coverage | Gap Count |
|--------|-------------------|-------------|-----------|
| Initial Access | _[X/Y]_ | _[0-4]_ | _[Count]_ |
| Execution | _[X/Y]_ | _[0-4]_ | _[Count]_ |
| Persistence | _[X/Y]_ | _[0-4]_ | _[Count]_ |
| Privilege Escalation | _[X/Y]_ | _[0-4]_ | _[Count]_ |
| Defense Evasion | _[X/Y]_ | _[0-4]_ | _[Count]_ |
| Credential Access | _[X/Y]_ | _[0-4]_ | _[Count]_ |
| Discovery | _[X/Y]_ | _[0-4]_ | _[Count]_ |
| Lateral Movement | _[X/Y]_ | _[0-4]_ | _[Count]_ |
| Collection | _[X/Y]_ | _[0-4]_ | _[Count]_ |
| Exfiltration | _[X/Y]_ | _[0-4]_ | _[Count]_ |
| Impact | _[X/Y]_ | _[0-4]_ | _[Count]_ |

### Priority Gaps (Improve First)
1. _[Technique with lowest coverage + highest risk]_
2. _[Next priority gap]_
3. _[Next priority gap]_
`,
  },
  {
    id: "de-r5",
    courseId: "detection-engineering",
    title: "Detection Tuning Workflow",
    type: "pdf",
    content: `
## Detection Tuning Workflow

### When to Tune a Detection

- False positive rate > 30%
- Alert volume unsustainable for analysts
- Rule consistently requires analyst override
- Business context changed (new tools, processes)

### Tuning Process

#### Step 1: Data Collection
- Sample minimum 50 alert instances
- Classify each as TP, FP, or BTP
- Document the FP cause for each false positive
- Calculate current FP rate

#### Step 2: Root Cause Analysis

| FP Cause | Frequency | Solution |
|----------|-----------|----------|
| Legitimate admin tool | _[Count]_ | Whitelist by user/host |
| Scheduled job | _[Count]_ | Time-based exception |
| Misconfigured source | _[Count]_ | Fix data source |
| Overly broad logic | _[Count]_ | Refine matching criteria |

#### Step 3: Apply Tuning

**Whitelist approach:**
\`\`\`yaml
# SIGMA example
detection:
  selection:
    CommandLine|contains: 'certutil'
  filter:
    User|endswith: '-admin'
    ComputerName|startswith: 'ADMIN-'
  condition: selection and not filter
\`\`\`

**Threshold approach:**
\`\`\`yaml
detection:
  selection:
    EventID: 4625
  condition: selection | count(TargetUserName) by SourceIP > 10
  timeframe: 10m
\`\`\`

#### Step 4: Validation
- Deploy tuned rule to staging
- Monitor for 7 days minimum
- Compare FP rate before vs after
- Verify no true positives were lost
- Document results

#### Step 5: Document & Review

| Field | Value |
|-------|-------|
| Rule ID | _[ID]_ |
| Original FP Rate | _[%]_ |
| Tuning Applied | _[Description]_ |
| New FP Rate | _[%]_ |
| TP Impact | _[None / Reduced coverage for X]_ |
| Review Date | _[Next scheduled review]_ |

### Tuning Metrics Dashboard
- Track total rules tuned per month
- Monitor aggregate FP rate trend
- Alert on rules exceeding FP threshold
- Schedule quarterly rule reviews
`,
  },
  {
    id: "de-r6",
    courseId: "detection-engineering",
    title: "Log Source Onboarding Checklist",
    type: "cheatsheet",
    content: `
## Log Source Onboarding Checklist

### Pre-Onboarding

- [ ] Identify log source type and purpose
- [ ] Determine log format (Syslog, CEF, JSON, XML)
- [ ] Estimate daily log volume (events/day, GB/day)
- [ ] Identify data classification (PII, sensitive, public)
- [ ] Get approval for data collection and retention
- [ ] Assign index/data stream name

### Collection Setup

- [ ] Choose collection method:
  - [ ] Agent-based (Splunk UF, Elastic Agent, etc.)
  - [ ] Syslog forwarding
  - [ ] API polling
  - [ ] File monitoring
- [ ] Configure source system to forward logs
- [ ] Verify network connectivity (ports, firewalls)
- [ ] Test log flow end-to-end
- [ ] Confirm timestamps are correct and timezone-aware

### Parsing & Normalization

- [ ] Create/assign source type or parser
- [ ] Validate field extraction accuracy
- [ ] Map fields to common data model (CIM/ECS)
- [ ] Verify key fields are extracted:
  - [ ] Timestamp
  - [ ] Source IP / User
  - [ ] Action / Event type
  - [ ] Status / Result
- [ ] Handle multi-line events if applicable

### Quality Assurance

- [ ] Verify sample events parse correctly
- [ ] Check for data gaps or delays
- [ ] Validate event count matches source
- [ ] Test search queries return expected results
- [ ] Confirm data retention policy applied

### Detection Integration

- [ ] Identify applicable detection rules
- [ ] Test existing SIGMA rules against new source
- [ ] Create source-specific detections if needed
- [ ] Add to ATT&CK coverage map
- [ ] Update dashboard panels if applicable

### Documentation

- [ ] Document source in log source inventory
- [ ] Record collection method and configuration
- [ ] Note any known limitations or gaps
- [ ] Add to data source catalog
- [ ] Update team on new data availability

### Log Source Inventory Entry

| Field | Value |
|-------|-------|
| Source Name | _[Name]_ |
| Source Type | _[OS/App/Network/Cloud]_ |
| Log Format | _[Syslog/CEF/JSON]_ |
| Collection Method | _[Agent/Syslog/API]_ |
| Daily Volume | _[Events/day]_ |
| Index/Stream | _[Name]_ |
| Retention | _[Days]_ |
| Owner | _[Team/Person]_ |
| Onboarded Date | _[Date]_ |
`,
  },

  // ==========================================
  // MALWARE ANALYSIS RESOURCES
  // ==========================================
  {
    id: "ma-r1",
    courseId: "malware-analysis",
    title: "Malware Analysis Lab Setup Guide",
    type: "pdf",
    content: `
## Malware Analysis Lab Setup Guide

### Lab Architecture

\`\`\`
┌─────────────────────────────────────┐
│           Host System               │
│  (Clean OS, no sensitive data)      │
│                                     │
│  ┌──────────┐    ┌──────────┐      │
│  │ Analysis │    │ Analysis │      │
│  │ VM #1    │    │ VM #2    │      │
│  │ (FlareVM)│    │ (REMnux) │      │
│  └────┬─────┘    └────┬─────┘      │
│       │    Isolated    │            │
│       │   Network      │            │
│       └──────┬─────────┘            │
│              │                      │
│       ┌──────┴──────┐              │
│       │  INetSim /  │              │
│       │  FakeNet    │              │
│       └─────────────┘              │
└─────────────────────────────────────┘
\`\`\`

### VM 1: Windows Analysis (FlareVM)

**Base:** Windows 10/11 Pro (licensed)

**Setup Steps:**
1. Install clean Windows in VMware/VirtualBox
2. Disable Windows Update and Defender
3. Install FlareVM: \`(New-Object net.webclient).DownloadString('https://boxstarter.org/bootstrapper.ps1') | iex; Install-BoxstarterPackage -PackageName https://raw.githubusercontent.com/mandiant/flare-vm/main/flarevm_malware.lst\`
4. Take clean snapshot

**Key Tools Included:**
| Tool | Purpose |
|------|---------|
| x64dbg / x32dbg | Debugger |
| Ghidra | Disassembler / Decompiler |
| PEStudio | PE file analysis |
| Process Monitor | Runtime monitoring |
| Process Hacker | Process inspection |
| Wireshark | Network capture |
| HxD | Hex editor |
| YARA | Pattern matching |
| CyberChef | Data decoding |
| Detect It Easy | Packer detection |

### VM 2: Linux Analysis (REMnux)

**Base:** REMnux OVA (pre-built)

**Key Tools Included:**
| Tool | Purpose |
|------|---------|
| oletools | Office macro analysis |
| pdfid / pdf-parser | PDF analysis |
| Cutter (Rizin) | Disassembler |
| Volatility 3 | Memory forensics |
| FLOSS | String deobfuscation |
| Yara | Pattern matching |
| INetSim | Network simulation |

### Network Isolation

**Critical:** The analysis network must be completely isolated.

- Set VM network to "Host-Only" or custom isolated network
- Run INetSim/FakeNet to simulate internet services
- **Never** connect analysis VMs to real internet
- Use REMnux as the network gateway/DNS

### Snapshot Strategy

| Snapshot Name | When | Purpose |
|--------------|------|---------|
| Clean Install | After setup | Baseline |
| Pre-Analysis | Before each sample | Restore point |
| Post-Execution | After dynamic analysis | Evidence |

### Safety Rules
1. ❌ Never analyze malware on your host OS
2. ❌ Never share clipboard between host and VM
3. ❌ Never connect analysis VMs to production network
4. ✅ Always take snapshots before execution
5. ✅ Always revert to clean snapshot after analysis
6. ✅ Use dedicated hardware if possible
`,
  },
  {
    id: "ma-r2",
    courseId: "malware-analysis",
    title: "PE File Format Reference",
    type: "cheatsheet",
    content: `
## Portable Executable (PE) File Format Reference

### PE Structure Overview

\`\`\`
┌──────────────────────┐
│    DOS Header        │  MZ signature (0x5A4D)
│    (64 bytes)        │  e_lfanew → PE header offset
├──────────────────────┤
│    DOS Stub          │  "This program cannot be run in DOS mode"
├──────────────────────┤
│    PE Signature      │  "PE\\0\\0" (0x00004550)
├──────────────────────┤
│    COFF Header       │  Machine, NumberOfSections, TimeDateStamp
│    (20 bytes)        │  
├──────────────────────┤
│    Optional Header   │  AddressOfEntryPoint, ImageBase
│    (varies)          │  Subsystem, DataDirectories
├──────────────────────┤
│    Section Headers   │  .text, .data, .rdata, .rsrc
├──────────────────────┤
│    Sections          │  Actual code and data
│    .text             │  Executable code
│    .rdata            │  Read-only data, imports
│    .data             │  Read-write data
│    .rsrc             │  Resources (icons, strings)
│    .reloc            │  Relocation data
└──────────────────────┘
\`\`\`

### Key Fields for Analysis

| Field | Location | Security Significance |
|-------|----------|----------------------|
| TimeDateStamp | COFF Header | Compilation time (can be faked) |
| AddressOfEntryPoint | Optional Header | Where execution begins |
| NumberOfSections | COFF Header | Unusual count = suspicious |
| Subsystem | Optional Header | GUI (2) vs Console (3) |
| DllCharacteristics | Optional Header | ASLR, DEP settings |
| Import Table | Data Directory | APIs used by malware |
| Export Table | Data Directory | Functions exported (DLLs) |
| Resource Directory | Data Directory | Embedded files, configs |

### Suspicious Indicators

| Indicator | Why Suspicious |
|-----------|---------------|
| High entropy sections | Likely packed/encrypted |
| Few imports | May resolve dynamically |
| Section name anomalies | Custom packers |
| TimeDateStamp = 0 or future | Timestamp manipulation |
| Entry point outside .text | Possible packing |
| Large .rsrc section | Embedded payloads |
| Import: VirtualAlloc + WriteProcessMemory | Process injection |
| Import: CreateRemoteThread | Code injection |

### Common Suspicious Imports

| API | Potential Use |
|-----|--------------|
| VirtualAlloc/VirtualProtect | Memory manipulation |
| WriteProcessMemory | Process injection |
| CreateRemoteThread | Remote code execution |
| LoadLibrary/GetProcAddress | Dynamic API resolution |
| WinExec/ShellExecute | Command execution |
| InternetOpen/HttpSendRequest | Network communication |
| CryptEncrypt/CryptDecrypt | Encryption (ransomware) |
| RegSetValueEx | Registry persistence |
| CreateService | Service persistence |
`,
  },
  {
    id: "ma-r3",
    courseId: "malware-analysis",
    title: "x86 Assembly Quick Reference",
    type: "cheatsheet",
    content: `
## x86 Assembly Quick Reference for Malware Analysis

### Registers

| Register | Purpose | Notes |
|----------|---------|-------|
| EAX / RAX | Accumulator | Return values, arithmetic |
| EBX / RBX | Base | General purpose, preserved |
| ECX / RCX | Counter | Loop counter, 1st arg (x64) |
| EDX / RDX | Data | I/O, multiplication, 2nd arg (x64) |
| ESI / RSI | Source Index | String operations source |
| EDI / RDI | Destination | String operations dest, 1st arg (x64) |
| ESP / RSP | Stack Pointer | Top of stack |
| EBP / RBP | Base Pointer | Stack frame base |
| EIP / RIP | Instruction Pointer | Next instruction |

### Common Instructions

| Instruction | Description | Example |
|-------------|-------------|---------|
| MOV | Copy data | \`mov eax, 5\` |
| PUSH | Push to stack | \`push eax\` |
| POP | Pop from stack | \`pop ebx\` |
| ADD | Add | \`add eax, 10\` |
| SUB | Subtract | \`sub ecx, 1\` |
| XOR | Exclusive OR | \`xor eax, eax\` (zero out) |
| CMP | Compare | \`cmp eax, 0\` |
| TEST | Bitwise AND test | \`test eax, eax\` (check zero) |
| JMP | Unconditional jump | \`jmp 0x401000\` |
| JE / JZ | Jump if equal/zero | \`je target\` |
| JNE / JNZ | Jump if not equal | \`jne target\` |
| CALL | Call function | \`call 0x401050\` |
| RET | Return from function | \`ret\` |
| LEA | Load effective address | \`lea eax, [ebx+4]\` |
| NOP | No operation | \`nop\` (padding/sled) |

### Function Call Conventions

**x86 (32-bit) — cdecl:**
\`\`\`
push arg3    ; Arguments pushed right-to-left
push arg2
push arg1
call function
add esp, 12  ; Caller cleans stack
; Return value in EAX
\`\`\`

**x64 (64-bit) — Windows:**
\`\`\`
; First 4 args: RCX, RDX, R8, R9
; Additional args on stack
; Return value in RAX
mov rcx, arg1
mov rdx, arg2
call function
\`\`\`

### Malware-Relevant Patterns

**XOR Decryption Loop:**
\`\`\`asm
mov ecx, buffer_length
mov esi, encrypted_buffer
mov al, xor_key
decrypt_loop:
  xor byte [esi], al
  inc esi
  dec ecx
  jnz decrypt_loop
\`\`\`

**Dynamic API Resolution:**
\`\`\`asm
push hash_of_api_name   ; Custom hash
call resolve_api         ; Custom resolver
call eax                 ; Call resolved API
\`\`\`

**Stack String Construction:**
\`\`\`asm
mov dword [esp], 'cmd.'   ; Building "cmd.exe" on stack
mov dword [esp+4], 'exe'  ; To avoid string detection
\`\`\`

### Debugger Tips (x64dbg)
- **F7** — Step into
- **F8** — Step over
- **F9** — Run
- **F2** — Set breakpoint
- **Ctrl+G** — Go to address
- Set breakpoints on suspicious API calls
`,
  },
  {
    id: "ma-r4",
    courseId: "malware-analysis",
    title: "YARA Rule Templates for Malware",
    type: "template",
    content: `
## YARA Rule Templates for Malware Detection

### Template 1: Generic Packed Executable

\`\`\`yara
rule Packed_Executable {
    meta:
        author = "InfoSec Diaries"
        description = "Detects potentially packed executables"
        severity = "medium"
    condition:
        uint16(0) == 0x5A4D and
        math.entropy(0, filesize) > 7.0 and
        filesize < 5MB
}
\`\`\`

### Template 2: Suspicious PowerShell Script

\`\`\`yara
rule Suspicious_PowerShell {
    meta:
        author = "InfoSec Diaries"
        description = "Detects obfuscated PowerShell downloaders"
    strings:
        $enc1 = "FromBase64String" nocase
        $enc2 = "-EncodedCommand" nocase
        $dl1 = "DownloadString" nocase
        $dl2 = "DownloadFile" nocase
        $dl3 = "Invoke-WebRequest" nocase
        $exec1 = "Invoke-Expression" nocase
        $exec2 = "IEX" nocase
        $obf1 = "replace" nocase
        $obf2 = "-join" nocase
        $obf3 = "[char]" nocase
    condition:
        (any of ($enc*) or any of ($dl*)) and
        (any of ($exec*) or any of ($obf*))
}
\`\`\`

### Template 3: Ransomware Indicators

\`\`\`yara
rule Ransomware_Indicators {
    meta:
        author = "InfoSec Diaries"
        description = "Detects common ransomware behavior indicators"
    strings:
        $ransom1 = "Your files have been encrypted" nocase
        $ransom2 = "bitcoin" nocase
        $ransom3 = "decrypt" nocase
        $ransom4 = ".onion" nocase
        $crypto1 = "CryptEncrypt" 
        $crypto2 = "CryptGenKey"
        $crypto3 = "BCryptEncrypt"
        $shadow1 = "vssadmin" nocase
        $shadow2 = "shadowcopy" nocase
        $shadow3 = "wmic" nocase
    condition:
        uint16(0) == 0x5A4D and
        (2 of ($ransom*)) or
        (any of ($crypto*) and any of ($shadow*))
}
\`\`\`

### Template 4: Webshell Detection

\`\`\`yara
rule WebShell_Generic {
    meta:
        author = "InfoSec Diaries"
        description = "Detects common webshell patterns"
    strings:
        $php1 = "<?php" nocase
        $asp1 = "<%@ " nocase
        $exec1 = "exec(" nocase
        $exec2 = "system(" nocase
        $exec3 = "passthru(" nocase
        $exec4 = "shell_exec(" nocase
        $exec5 = "eval(" nocase
        $exec6 = "assert(" nocase
        $cmd1 = "cmd" nocase
        $cmd2 = "/bin/sh" nocase
        $upload = "move_uploaded_file" nocase
        $b64 = "base64_decode" nocase
    condition:
        (any of ($php*, $asp*)) and
        (2 of ($exec*) or ($upload and $b64))
}
\`\`\`

### Template 5: Process Injection

\`\`\`yara
rule Process_Injection_APIs {
    meta:
        author = "InfoSec Diaries"
        description = "Detects PE files with process injection API imports"
    strings:
        $api1 = "VirtualAllocEx"
        $api2 = "WriteProcessMemory"
        $api3 = "CreateRemoteThread"
        $api4 = "NtCreateThreadEx"
        $api5 = "QueueUserAPC"
        $api6 = "SetThreadContext"
        $api7 = "NtUnmapViewOfSection"
    condition:
        uint16(0) == 0x5A4D and 3 of ($api*)
}
\`\`\`
`,
  },
  {
    id: "ma-r5",
    courseId: "malware-analysis",
    title: "Dynamic Analysis Checklist",
    type: "cheatsheet",
    content: `
## Dynamic Analysis Checklist

### Pre-Execution Setup

- [ ] Revert VM to clean snapshot
- [ ] Start network simulation (INetSim / FakeNet-NG)
- [ ] Start Process Monitor (set filter for sample)
- [ ] Start Process Hacker / Process Explorer
- [ ] Start Wireshark (capture on isolated interface)
- [ ] Start Regshot (take 1st snapshot)
- [ ] Start API Monitor (optional, for API tracing)
- [ ] Disable sleep/idle in VM settings
- [ ] Record system time

### During Execution

Monitor and note:
- [ ] New processes created (parent-child tree)
- [ ] Files created, modified, or deleted
- [ ] Registry keys created or modified
- [ ] Network connections attempted
- [ ] DNS queries made
- [ ] DLLs loaded
- [ ] Mutex/named objects created
- [ ] Services installed
- [ ] Scheduled tasks created
- [ ] User account changes

### Post-Execution Collection

- [ ] Take Regshot 2nd snapshot and compare
- [ ] Save Process Monitor log (PML format)
- [ ] Export Wireshark capture (PCAP)
- [ ] Screenshot any visible indicators (ransom notes, etc.)
- [ ] Dump memory if needed (for further analysis)
- [ ] Note all observed behaviors

### Behavior Documentation

| Category | Observation |
|----------|------------|
| **Processes** | _[New processes spawned]_ |
| **Files Created** | _[Paths and names]_ |
| **Files Modified** | _[What was changed]_ |
| **Files Deleted** | _[What was removed]_ |
| **Registry Changes** | _[Keys added/modified]_ |
| **Network — DNS** | _[Domains queried]_ |
| **Network — HTTP** | _[URLs contacted]_ |
| **Network — Other** | _[Raw IP connections, ports]_ |
| **Persistence** | _[Method used]_ |
| **Evasion** | _[Anti-analysis techniques observed]_ |

### Common Anti-Analysis Checks

| Technique | How Malware Checks | Bypass |
|-----------|-------------------|--------|
| VM detection | Registry keys, MAC prefix | Modify VM settings |
| Debugger detection | IsDebuggerPresent API | Patch/hook API |
| Sandbox detection | Check mouse movement | Move mouse in VM |
| Sleep acceleration | Long Sleep() calls | Patch Sleep to return |
| Time checks | GetTickCount comparison | Adjust system time |
| Environment checks | Username, filename | Use realistic names |
`,
  },
  {
    id: "ma-r6",
    courseId: "malware-analysis",
    title: "Malware Report Template",
    type: "template",
    content: `
## Malware Analysis Report Template

### Executive Summary

| Field | Value |
|-------|-------|
| **Sample Name** | _[Original filename]_ |
| **SHA256** | _[Hash]_ |
| **File Type** | _[PE32/PE64/Script/Document]_ |
| **File Size** | _[Bytes]_ |
| **First Seen** | _[Date]_ |
| **Malware Family** | _[Family name if known]_ |
| **Verdict** | _[Malicious / Suspicious / Clean]_ |
| **Severity** | _[Critical / High / Medium / Low]_ |

**Summary:** _[2-3 sentence overview of what the malware does]_

---

### Static Analysis Findings

| Property | Value |
|----------|-------|
| MD5 | _[Hash]_ |
| SHA1 | _[Hash]_ |
| SHA256 | _[Hash]_ |
| Imphash | _[Import hash]_ |
| Compile Time | _[Timestamp]_ |
| Packer | _[None / UPX / Custom]_ |
| Entropy | _[Value]_ |

**Notable Imports:**
- _[Suspicious API 1 — Purpose]_
- _[Suspicious API 2 — Purpose]_

**Strings of Interest:**
- _[URL/domain found]_
- _[Command/path found]_
- _[Registry key found]_

---

### Dynamic Analysis Findings

**Execution Behavior:**
_[Description of what happens when executed]_

**Process Activity:**
| Process | Parent | Description |
|---------|--------|-------------|
| _[Process]_ | _[Parent]_ | _[What it does]_ |

**File System Activity:**
| Action | Path | Purpose |
|--------|------|---------|
| Created | _[Path]_ | _[Dropped payload / config]_ |
| Modified | _[Path]_ | _[Persistence / data]_ |
| Deleted | _[Path]_ | _[Anti-forensics]_ |

**Network Activity:**
| Protocol | Destination | Purpose |
|----------|-------------|---------|
| DNS | _[Domain]_ | _[C2 resolution]_ |
| HTTP | _[URL]_ | _[Payload download / beacon]_ |
| TCP | _[IP:Port]_ | _[C2 communication]_ |

**Persistence Mechanisms:**
- _[Registry run key / scheduled task / service]_

---

### MITRE ATT&CK Mapping

| Tactic | Technique | ID | Details |
|--------|-----------|-----|---------|
| _[Tactic]_ | _[Technique]_ | _[T-ID]_ | _[Specifics]_ |

---

### Indicators of Compromise (IOCs)

| Type | Value | Context |
|------|-------|---------|
| SHA256 | _[Hash]_ | Main sample |
| SHA256 | _[Hash]_ | Dropped file |
| Domain | _[Domain]_ | C2 server |
| IP | _[IP]_ | C2 infrastructure |
| URL | _[URL]_ | Payload URL |
| Mutex | _[Mutex]_ | Unique identifier |
| Registry | _[Key]_ | Persistence |

---

### Recommendations

1. _[Block IOCs at network boundary]_
2. _[Deploy YARA rule for detection]_
3. _[Update EDR with behavioral indicators]_
4. _[Scan environment for related activity]_

---

**Analyst:** _[Name]_
**Date:** _[Date]_
**Classification:** _[TLP:WHITE / GREEN / AMBER / RED]_
`,
  },
  // SOC ANALYST LEARNING PATH RESOURCES
  {
    id: "sap-r1",
    courseId: "soc-analyst-path",
    title: "SOC Analyst Investigation Playbook",
    type: "template",
    content: `
## SOC Analyst Investigation Playbook

### Phishing Alert
1. Review alert (sender, subject, recipients)
2. Extract headers, check SPF/DKIM/DMARC
3. Defang and scan URLs (URLScan, VT)
4. Hash and sandbox attachments
5. Check proxy logs for clicks
6. Block sender/URLs, purge emails
7. Reset credentials if compromised
8. Monitor affected accounts 72h

### Malware Alert
1. Review EDR/AV alert details
2. Hash file, check VT
3. Determine malware family and C2
4. Isolate endpoint
5. Block C2 at firewall
6. Remove malware and persistence
7. Monitor for reinfection 30 days

### Suspicious Login
1. Review login details and source IP
2. Check GeoIP for impossible travel
3. Review failed attempts before success
4. Contact user to verify
5. If unauthorized: reset, revoke, enable MFA
6. Monitor 72 hours
`,
  },
  {
    id: "sap-r2",
    courseId: "soc-analyst-path",
    title: "Network Protocol Cheat Sheet",
    type: "cheatsheet",
    content: `
## Network Protocol Quick Reference

### Common Ports
| Port | Service | Security Notes |
|------|---------|----------------|
| 22 | SSH | Brute force target |
| 25 | SMTP | Email relay/spoofing |
| 53 | DNS | Tunneling, DGA |
| 80/443 | HTTP/S | Web attacks, C2 |
| 445 | SMB | Lateral movement |
| 3389 | RDP | Brute force, lateral |

### TCP Flags
| Flag | Hex | Description |
|------|-----|-------------|
| SYN | 0x02 | Initiate connection |
| ACK | 0x10 | Confirm receipt |
| FIN | 0x01 | Graceful close |
| RST | 0x04 | Abort connection |
| PSH | 0x08 | Immediate delivery |

### DNS Record Types
| Type | Purpose | Abuse |
|------|---------|-------|
| A/AAAA | IP address | Malicious resolution |
| TXT | Text data | Tunneling, C2 |
| MX | Mail server | Phishing infra |
| NS | Nameserver | DNS hijacking |

### HTTP Status Codes
| Code | Meaning | Security Context |
|------|---------|------------------|
| 200 | OK | Successful request |
| 301/302 | Redirect | Open redirect abuse |
| 403 | Forbidden | Access control working |
| 404 | Not Found | Directory brute force |
| 500 | Server Error | Possible injection |
`,
  },
  {
    id: "sap-r3",
    courseId: "soc-analyst-path",
    title: "SIEM Query Reference Guide",
    type: "cheatsheet",
    content: `
## SIEM Query Reference

### Basic Patterns
\`\`\`
source_ip="10.0.0.5" AND action="blocked"
process_name="cmd*"
NOT source_ip IN ("10.0.0.0/8")
\`\`\`

### Detection Queries

**Brute Force:**
\`\`\`
event_type="failed_login" | stats count by user, source_ip | where count > 5
\`\`\`

**Lateral Movement (RDP):**
\`\`\`
event_id=4624 logon_type=10 | stats dc(dest_host) as targets by source_ip | where targets > 3
\`\`\`

**Data Exfiltration:**
\`\`\`
event_type="proxy" | stats sum(bytes_out) as upload by source_ip, dest | where upload > 100MB
\`\`\`

**Suspicious Process:**
\`\`\`
parent IN ("winword.exe","excel.exe") AND process IN ("cmd.exe","powershell.exe")
\`\`\`

**DNS Tunneling:**
\`\`\`
dns | eval len=len(subdomain) | where len > 30 | stats count by domain | where count > 100
\`\`\`
`,
  },
  {
    id: "sap-r4",
    courseId: "soc-analyst-path",
    title: "Windows Forensics Quick Reference",
    type: "cheatsheet",
    content: `
## Windows Forensics Quick Reference

### Critical Event IDs
| ID | Description | Alert On |
|----|-------------|----------|
| 4624 | Successful logon | Type 10 from unusual source |
| 4625 | Failed logon | > 5 in 10 min |
| 4688 | Process creation | Suspicious parent-child |
| 4720 | Account created | Unexpected accounts |
| 4728/4732 | Group change | Privilege escalation |
| 7045 | Service installed | Persistence/malware |
| 1102 | Audit log cleared | Evidence destruction |

### Persistence Locations
- Run keys: HKLM/HKCU\\...\\CurrentVersion\\Run
- Scheduled tasks: C:\\Windows\\System32\\Tasks\\
- Services: HKLM\\SYSTEM\\CurrentControlSet\\Services\\
- Startup folders
- WMI subscriptions: root/subscription

### LOLBins to Monitor
| Binary | Suspicious Usage |
|--------|-----------------|
| certutil | -urlcache -split -f (download) |
| mshta | Execution from email/temp |
| powershell | -enc (encoded command) |
| wmic | process call create |
| bitsadmin | /transfer (download) |

### Investigation Commands
\`\`\`powershell
Get-Process | Select Name, Id, Path
Get-NetTCPConnection | Where {$_.State -eq "Established"}
Get-AuthenticodeSignature "path\\to\\file.exe"
Get-FileHash "path\\to\\file.exe" -Algorithm SHA256
\`\`\`
`,
  },
  {
    id: "sap-r5",
    courseId: "soc-analyst-path",
    title: "Email Analysis Toolkit Guide",
    type: "pdf",
    content: `
## Email Analysis Toolkit

### Header Analysis Tools
| Tool | Purpose |
|------|---------|
| MXToolbox | Parse and analyze headers |
| Google Admin Toolbox | Gmail header analysis |

### Authentication Checks
\`\`\`bash
dig TXT example.com | grep spf      # SPF
dig TXT _dmarc.example.com          # DMARC
dig TXT selector._domainkey.example.com  # DKIM
\`\`\`

### URL Investigation
1. Defang URL
2. Parse components
3. Check reputation (URLScan, VT, PhishTank)
4. Domain investigation (WHOIS, crt.sh, PassiveDNS)
5. Expand shortened URLs

### Attachment Analysis
\`\`\`bash
file suspicious_attachment           # Identify type
sha256sum suspicious_attachment      # Hash
olevba suspicious.docm              # Extract macros
pdfid suspicious.pdf                # PDF structure
\`\`\`

### IOC Extraction Template
| Type | Value | Context |
|------|-------|---------|
| Sender Email | | From address |
| Sender IP | | X-Originating-IP |
| Domain | | Phishing domain |
| URL | | Defanged link |
| SHA256 | | Attachment hash |
`,
  },
  {
    id: "sap-r6",
    courseId: "soc-analyst-path",
    title: "Incident Report Template",
    type: "template",
    content: `
## Incident Report Template

### 1. Executive Summary
**ID:** INC-YYYY-### | **Status:** ☐ Active ☐ Contained ☐ Resolved
**Severity:** ☐ P1 ☐ P2 ☐ P3 ☐ P4

_[What happened? Impact? Contained? Current status?]_

### 2. Timeline
| Date/Time (UTC) | Event | Source |
|-----------------|-------|--------|
| | | |

### 3. Technical Analysis
- **Attack Vector:** _[How attacker gained access]_
- **Affected Systems:** _[Hostnames, IPs, roles]_
- **MITRE Mapping:** _[Tactics and techniques]_

### 4. Indicators of Compromise
| Type | Value (Defanged) | Context |
|------|-----------------|---------|
| | | |

### 5. Impact Assessment
- Data exposure scope
- Systems affected
- Business impact
- Regulatory implications

### 6. Response Actions
- Containment: _[Actions with timestamps]_
- Eradication: _[Actions with timestamps]_
- Recovery: _[Actions with timestamps]_

### 7. Recommendations
- **Immediate (0-7 days):**
- **Short-term (7-30 days):**
- **Long-term (30-90 days):**

**Author:** _[Name]_ | **Classification:** _[TLP]_
`,
  },
  // ==========================================
  // NETWORK FUNDAMENTALS RESOURCES
  // ==========================================
  {
    id: "nf-r1",
    courseId: "network-fundamentals",
    title: "Network Protocols Cheat Sheet",
    type: "cheatsheet",
    content: `
## Network Protocols Quick Reference

### Common Protocols & Port Numbers

| Protocol | Port(s) | Transport | Description |
|----------|---------|-----------|-------------|
| **FTP** | 20 (data), 21 (control) | TCP | File Transfer Protocol |
| **SSH** | 22 | TCP | Secure Shell — encrypted remote access |
| **Telnet** | 23 | TCP | Unencrypted remote access (deprecated) |
| **SMTP** | 25 / 587 | TCP | Simple Mail Transfer Protocol |
| **DNS** | 53 | UDP/TCP | Domain Name System |
| **DHCP** | 67 (server), 68 (client) | UDP | Dynamic Host Configuration Protocol |
| **TFTP** | 69 | UDP | Trivial File Transfer Protocol |
| **HTTP** | 80 | TCP | Hypertext Transfer Protocol |
| **POP3** | 110 | TCP | Post Office Protocol v3 |
| **NTP** | 123 | UDP | Network Time Protocol |
| **IMAP** | 143 | TCP | Internet Message Access Protocol |
| **SNMP** | 161/162 | UDP | Simple Network Management Protocol |
| **LDAP** | 389 | TCP/UDP | Lightweight Directory Access Protocol |
| **HTTPS** | 443 | TCP | HTTP Secure (TLS/SSL) |
| **SMB** | 445 | TCP | Server Message Block |
| **Syslog** | 514 | UDP | System Logging |
| **LDAPS** | 636 | TCP | LDAP over SSL |
| **IMAPS** | 993 | TCP | IMAP over SSL |
| **POP3S** | 995 | TCP | POP3 over SSL |
| **RDP** | 3389 | TCP/UDP | Remote Desktop Protocol |

### OSI Model Quick Reference

| Layer | Name | PDU | Devices | Key Protocols |
|-------|------|-----|---------|---------------|
| **7** | Application | Data | Gateways | HTTP, DNS, SMTP, FTP |
| **6** | Presentation | Data | — | SSL/TLS, JPEG, ASCII |
| **5** | Session | Data | — | NetBIOS, RPC |
| **4** | Transport | Segment | — | TCP, UDP |
| **3** | Network | Packet | Router | IP, ICMP, ARP, OSPF |
| **2** | Data Link | Frame | Switch, Bridge | Ethernet, 802.1Q, STP |
| **1** | Physical | Bit | Hub, Repeater | Cables, Wi-Fi signals |

### TCP vs UDP Comparison

| Feature | TCP | UDP |
|---------|-----|-----|
| **Connection** | Connection-oriented (3-way handshake) | Connectionless |
| **Reliability** | Guaranteed delivery, ordering | No guarantee |
| **Speed** | Slower (overhead) | Faster (no overhead) |
| **Header Size** | 20-60 bytes | 8 bytes |
| **Use Cases** | HTTP, FTP, SSH, Email | DNS, VoIP, Streaming, Gaming |
| **Flow Control** | Sliding window | None |
| **Error Recovery** | Retransmission | None |

### TCP Three-Way Handshake

1. **SYN** → Client sends SYN (seq=x)
2. **SYN-ACK** → Server responds SYN-ACK (seq=y, ack=x+1)
3. **ACK** → Client sends ACK (ack=y+1)

### TCP Four-Way Teardown

1. **FIN** → Initiator sends FIN
2. **ACK** → Receiver acknowledges
3. **FIN** → Receiver sends FIN
4. **ACK** → Initiator acknowledges

### ICMP Message Types

| Type | Code | Description |
|------|------|-------------|
| 0 | 0 | Echo Reply (ping response) |
| 3 | 0 | Destination Network Unreachable |
| 3 | 1 | Destination Host Unreachable |
| 3 | 3 | Destination Port Unreachable |
| 8 | 0 | Echo Request (ping) |
| 11 | 0 | TTL Exceeded (traceroute) |

### Port Ranges

- **Well-Known:** 0 – 1023 (assigned to standard services)
- **Registered:** 1024 – 49151 (used by applications)
- **Dynamic/Ephemeral:** 49152 – 65535 (temporary client ports)
`,
  },
  {
    id: "nf-r2",
    courseId: "network-fundamentals",
    title: "Subnetting Quick Reference",
    type: "cheatsheet",
    content: `
## Subnetting Quick Reference

### Subnet Mask Table

| CIDR | Subnet Mask | # Hosts | # Usable | Block Size |
|------|-------------|---------|----------|------------|
| /32 | 255.255.255.255 | 1 | 1 | 1 |
| /31 | 255.255.255.254 | 2 | 2* | 2 |
| /30 | 255.255.255.252 | 4 | 2 | 4 |
| /29 | 255.255.255.248 | 8 | 6 | 8 |
| /28 | 255.255.255.240 | 16 | 14 | 16 |
| /27 | 255.255.255.224 | 32 | 30 | 32 |
| /26 | 255.255.255.192 | 64 | 62 | 64 |
| /25 | 255.255.255.128 | 128 | 126 | 128 |
| /24 | 255.255.255.0 | 256 | 254 | 256 |
| /23 | 255.255.254.0 | 512 | 510 | 512 |
| /22 | 255.255.252.0 | 1,024 | 1,022 | 1,024 |
| /21 | 255.255.248.0 | 2,048 | 2,046 | 2,048 |
| /20 | 255.255.240.0 | 4,096 | 4,094 | 4,096 |
| /16 | 255.255.0.0 | 65,536 | 65,534 | 65,536 |
| /8 | 255.0.0.0 | 16,777,216 | 16,777,214 | 16,777,216 |

**/31 is used for point-to-point links (RFC 3021)*

### Powers of 2 (Essential for Subnetting)

| 2^n | Value | | 2^n | Value |
|-----|-------|-|-----|-------|
| 2^0 | 1 | | 2^8 | 256 |
| 2^1 | 2 | | 2^9 | 512 |
| 2^2 | 4 | | 2^10 | 1,024 |
| 2^3 | 8 | | 2^11 | 2,048 |
| 2^4 | 16 | | 2^12 | 4,096 |
| 2^5 | 32 | | 2^13 | 8,192 |
| 2^6 | 64 | | 2^14 | 16,384 |
| 2^7 | 128 | | 2^16 | 65,536 |

### Subnetting Steps

1. **Convert** the subnet mask to binary
2. **Count** the host bits (zeros in the mask)
3. **Calculate** total addresses: 2^(host bits)
4. **Subtract 2** for network ID and broadcast: usable = total - 2
5. **Find block size**: 256 - last non-zero octet of mask
6. **List networks**: Start at 0, increment by block size

### Example: Subnet 192.168.1.0/26

- **Mask:** 255.255.255.192
- **Block size:** 256 - 192 = 64
- **Subnets:**
  - 192.168.1.0 – 192.168.1.63 (broadcast: .63)
  - 192.168.1.64 – 192.168.1.127 (broadcast: .127)
  - 192.168.1.128 – 192.168.1.191 (broadcast: .191)
  - 192.168.1.192 – 192.168.1.255 (broadcast: .255)
- **Usable hosts per subnet:** 62

### Private IP Address Ranges (RFC 1918)

| Class | Range | CIDR | # Addresses |
|-------|-------|------|-------------|
| A | 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 | 16,777,216 |
| B | 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 | 1,048,576 |
| C | 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 | 65,536 |

### Special Addresses

| Address | Purpose |
|---------|---------|
| 0.0.0.0 | Default route / unspecified |
| 127.0.0.1 | Loopback (localhost) |
| 169.254.x.x | APIPA (DHCP failure) |
| 224.0.0.0/4 | Multicast |
| 255.255.255.255 | Limited broadcast |
`,
  },
  {
    id: "nf-r3",
    courseId: "network-fundamentals",
    title: "Wireshark Display Filters Guide",
    type: "cheatsheet",
    content: `
## Wireshark Display Filters Quick Reference

### Basic Protocol Filters

| Filter | Description |
|--------|-------------|
| \`http\` | Show HTTP traffic |
| \`dns\` | Show DNS queries and responses |
| \`tcp\` | Show all TCP traffic |
| \`udp\` | Show all UDP traffic |
| \`icmp\` | Show ICMP (ping/traceroute) |
| \`arp\` | Show ARP requests/replies |
| \`dhcp\` | Show DHCP transactions |
| \`tls\` | Show TLS/SSL traffic |
| \`ssh\` | Show SSH traffic |
| \`ftp\` | Show FTP control traffic |
| \`smtp\` | Show SMTP email traffic |

### IP Address Filters

| Filter | Description |
|--------|-------------|
| \`ip.addr == 192.168.1.1\` | Traffic to/from specific IP |
| \`ip.src == 10.0.0.5\` | Traffic from source IP |
| \`ip.dst == 8.8.8.8\` | Traffic to destination IP |
| \`ip.addr == 192.168.1.0/24\` | Traffic to/from a subnet |
| \`!ip.addr == 10.0.0.1\` | Exclude specific IP |

### Port Filters

| Filter | Description |
|--------|-------------|
| \`tcp.port == 80\` | TCP port 80 (src or dst) |
| \`tcp.dstport == 443\` | Destination port 443 |
| \`tcp.srcport == 22\` | Source port 22 |
| \`udp.port == 53\` | UDP port 53 (DNS) |
| \`tcp.port in {80, 443, 8080}\` | Multiple ports |

### TCP Analysis Filters

| Filter | Description |
|--------|-------------|
| \`tcp.flags.syn == 1\` | SYN packets (connection attempts) |
| \`tcp.flags.syn == 1 && tcp.flags.ack == 0\` | Initial SYN only |
| \`tcp.flags.rst == 1\` | RST packets (connection resets) |
| \`tcp.flags.fin == 1\` | FIN packets (connection teardown) |
| \`tcp.analysis.retransmission\` | Retransmitted packets |
| \`tcp.analysis.duplicate_ack\` | Duplicate ACKs |
| \`tcp.analysis.zero_window\` | Zero window (flow control) |
| \`tcp.stream eq 5\` | Follow specific TCP stream |

### HTTP Filters

| Filter | Description |
|--------|-------------|
| \`http.request\` | HTTP requests only |
| \`http.response\` | HTTP responses only |
| \`http.request.method == "POST"\` | POST requests |
| \`http.request.method == "GET"\` | GET requests |
| \`http.response.code == 404\` | 404 Not Found responses |
| \`http.response.code >= 400\` | All error responses |
| \`http.host contains "example"\` | Requests to specific host |
| \`http.request.uri contains "login"\` | URLs containing "login" |

### DNS Filters

| Filter | Description |
|--------|-------------|
| \`dns.qry.name == "example.com"\` | Queries for specific domain |
| \`dns.qry.type == 1\` | A record queries |
| \`dns.qry.type == 28\` | AAAA record queries |
| \`dns.flags.response == 1\` | DNS responses only |
| \`dns.flags.rcode == 3\` | NXDOMAIN (name not found) |

### Combining Filters

| Operator | Example |
|----------|---------|
| **AND** (\`&&\`) | \`ip.addr == 10.0.0.1 && tcp.port == 80\` |
| **OR** (\`||\`) | \`dns || http\` |
| **NOT** (\`!\`) | \`!arp && !dns\` |
| **Grouping** | \`(http || dns) && ip.addr == 10.0.0.1\` |

### Useful Compound Filters

- **All web traffic:** \`http || tls\`
- **Failed connections:** \`tcp.flags.rst == 1 || icmp.type == 3\`
- **Suspicious DNS:** \`dns.qry.name contains ".ru" || dns.qry.name contains ".cn"\`
- **Large packets:** \`frame.len > 1500\`
- **Slow responses:** \`tcp.time_delta > 1\`
- **Non-standard ports:** \`tcp.port > 1024 && tcp.port < 49152\`

### Capture Filter vs Display Filter

| Feature | Capture Filter | Display Filter |
|---------|---------------|----------------|
| **When** | During capture | After capture |
| **Syntax** | BPF (Berkeley Packet Filter) | Wireshark-specific |
| **Example** | \`host 10.0.0.1\` | \`ip.addr == 10.0.0.1\` |
| **Performance** | Reduces file size | Searches full capture |
`,
  },
  {
    id: "nf-r4",
    courseId: "network-fundamentals",
    title: "OSI Model Reference Poster",
    type: "pdf",
    content: `
## OSI Model — Complete Reference

### Layer 7: Application

- **Function:** Provides network services directly to user applications
- **Protocols:** HTTP, HTTPS, FTP, SMTP, POP3, IMAP, DNS, DHCP, SNMP, SSH, Telnet
- **Devices:** Application gateways, proxy servers
- **PDU:** Data
- **Key Concepts:** User authentication, network services, API communication

### Layer 6: Presentation

- **Function:** Data formatting, encryption, compression, character encoding
- **Protocols/Standards:** SSL/TLS, JPEG, PNG, GIF, MPEG, ASCII, Unicode, MIME
- **Devices:** —
- **PDU:** Data
- **Key Concepts:** Data translation between formats, encryption/decryption

### Layer 5: Session

- **Function:** Manages communication sessions (establish, maintain, terminate)
- **Protocols:** NetBIOS, RPC, PPTP, SIP
- **Devices:** —
- **PDU:** Data
- **Key Concepts:** Dialog control (simplex, half-duplex, full-duplex), synchronization

### Layer 4: Transport

- **Function:** End-to-end communication, segmentation, flow control, error recovery
- **Protocols:** TCP, UDP
- **Devices:** —
- **PDU:** Segment (TCP) / Datagram (UDP)
- **Key Concepts:** Port numbers, 3-way handshake, windowing, multiplexing

### Layer 3: Network

- **Function:** Logical addressing, routing, path determination
- **Protocols:** IP (IPv4/IPv6), ICMP, ARP, OSPF, BGP, EIGRP, RIP
- **Devices:** Router, Layer 3 Switch
- **PDU:** Packet
- **Key Concepts:** IP addressing, subnetting, routing tables, NAT

### Layer 2: Data Link

- **Function:** Physical addressing, framing, error detection, media access control
- **Sub-layers:** LLC (Logical Link Control) + MAC (Media Access Control)
- **Protocols:** Ethernet (802.3), Wi-Fi (802.11), 802.1Q (VLANs), STP, PPP
- **Devices:** Switch, Bridge, NIC
- **PDU:** Frame
- **Key Concepts:** MAC addresses, switching, VLANs, STP, ARP

### Layer 1: Physical

- **Function:** Bit transmission over physical medium (electrical, optical, radio)
- **Standards:** Ethernet (10BASE-T, 100BASE-TX, 1000BASE-T), 802.11, RS-232
- **Devices:** Hub, Repeater, Modem, Cables, Connectors
- **PDU:** Bit
- **Key Concepts:** Cabling (Cat5e/6/6a, Fiber), connectors (RJ-45, LC, SC), signaling

---

### Data Encapsulation Flow

\`\`\`
Application  → [ Data                                    ]
Transport    → [ TCP/UDP Header | Data                   ]  = Segment
Network      → [ IP Header | TCP Header | Data           ]  = Packet
Data Link    → [ Frame Header | IP | TCP | Data | FCS    ]  = Frame
Physical     → [ 10110010101001011010... ]                   = Bits
\`\`\`

### Common Mnemonics

- **Top → Bottom:** All People Seem To Need Data Processing
- **Bottom → Top:** Please Do Not Throw Sausage Pizza Away
`,
  },
  {
    id: "nf-r5",
    courseId: "network-fundamentals",
    title: "Network Command-Line Tools Guide",
    type: "template",
    content: `
## Network Command-Line Tools — Complete Reference

### 1. ping — Test Connectivity

**Purpose:** Test basic IP connectivity and measure round-trip time

| OS | Command |
|----|---------|
| Windows | \`ping 8.8.8.8\` |
| Linux/Mac | \`ping -c 4 8.8.8.8\` |

**Useful Flags:**
- \`-t\` (Windows) — Continuous ping
- \`-c N\` (Linux) — Send N packets
- \`-s SIZE\` (Linux) — Set packet size
- \`-i INTERVAL\` (Linux) — Set interval between pings

**Reading Results:**
- **Reply from:** Successful connectivity
- **Request timed out:** No response (host down or ICMP blocked)
- **TTL:** Hops remaining (indicates distance)
- **time:** Round-trip latency in ms

---

### 2. traceroute / tracert — Path Discovery

**Purpose:** Show the path packets take to a destination

| OS | Command |
|----|---------|
| Windows | \`tracert 8.8.8.8\` |
| Linux | \`traceroute 8.8.8.8\` |

**Reading Results:**
- Each line = one hop (router)
- Three time values per hop
- \`* * *\` = No response (ICMP blocked)
- Increasing latency at a specific hop = potential bottleneck

---

### 3. nslookup / dig — DNS Queries

**Purpose:** Query DNS servers for name resolution

| Task | Command |
|------|---------|
| Basic lookup | \`nslookup example.com\` |
| Specific record | \`nslookup -type=MX example.com\` |
| Specific DNS server | \`nslookup example.com 8.8.8.8\` |
| dig (Linux, more detail) | \`dig example.com A\` |
| dig reverse lookup | \`dig -x 8.8.8.8\` |
| dig short output | \`dig +short example.com\` |

---

### 4. ipconfig / ifconfig / ip — Interface Configuration

| Task | Windows | Linux |
|------|---------|-------|
| View config | \`ipconfig\` | \`ip addr show\` |
| Detailed view | \`ipconfig /all\` | \`ip addr\` |
| Release DHCP | \`ipconfig /release\` | \`dhclient -r\` |
| Renew DHCP | \`ipconfig /renew\` | \`dhclient\` |
| Flush DNS | \`ipconfig /flushdns\` | \`systemd-resolve --flush-caches\` |

---

### 5. netstat / ss — Network Connections

| Task | netstat | ss (modern) |
|------|---------|-------------|
| All connections | \`netstat -an\` | \`ss -an\` |
| Listening ports | \`netstat -tlnp\` | \`ss -tlnp\` |
| With process IDs | \`netstat -anp\` | \`ss -anp\` |
| TCP only | \`netstat -at\` | \`ss -at\` |
| UDP only | \`netstat -au\` | \`ss -au\` |
| Routing table | \`netstat -rn\` | \`ip route\` |

---

### 6. arp — ARP Cache

| Task | Command |
|------|---------|
| View ARP cache | \`arp -a\` |
| Delete entry | \`arp -d IP_ADDRESS\` |
| Add static entry | \`arp -s IP_ADDRESS MAC_ADDRESS\` |

---

### 7. route — Routing Table

| Task | Windows | Linux |
|------|---------|-------|
| View table | \`route print\` | \`ip route show\` |
| Add route | \`route add DEST mask MASK GW\` | \`ip route add DEST/CIDR via GW\` |
| Delete route | \`route delete DEST\` | \`ip route del DEST/CIDR\` |
| Default route | \`route add 0.0.0.0 mask 0.0.0.0 GW\` | \`ip route add default via GW\` |

---

### 8. Wireshark Quick Commands

| Task | Filter/Command |
|------|---------------|
| Capture on interface | \`wireshark -i eth0\` |
| Capture with filter | \`wireshark -i eth0 -f "port 80"\` |
| Command-line capture | \`tshark -i eth0 -w output.pcap\` |
| Read capture file | \`tshark -r capture.pcap\` |
| Apply display filter | \`tshark -r file.pcap -Y "http"\` |

---

### Troubleshooting Checklist

- [ ] \`ping 127.0.0.1\` — Test TCP/IP stack
- [ ] \`ping DEFAULT_GATEWAY\` — Test local network
- [ ] \`ping 8.8.8.8\` — Test internet connectivity
- [ ] \`ping google.com\` — Test DNS resolution
- [ ] \`ipconfig /all\` — Verify IP configuration
- [ ] \`nslookup example.com\` — Test DNS
- [ ] \`tracert destination\` — Identify routing issues
- [ ] \`netstat -an\` — Check active connections
- [ ] \`arp -a\` — Verify ARP entries
`,
  },
];

export const getResourceContent = (courseId: string, resourceId: string): ResourceDocument | undefined => {
  return resourceDocuments.find(doc => doc.courseId === courseId && doc.id === resourceId);
};
