# 🔐 Automated Entra ID Posture Auditor & ChatOps Alerter

A lightweight, read-only security automation tool that assesses Microsoft Entra ID identity posture using Microsoft Graph, identifies potential security risks, assigns risk severity, generates security reports, and sends actionable alerts through ChatOps.

The project is designed to demonstrate practical identity-security automation using Python, Microsoft Graph, security analysis, risk scoring, testing, containerization, and CI.

---

## 🎯 Project Objective

Organizations can accumulate large numbers of user accounts, privileged roles, authentication events, and identity configurations.

The challenge is not simply having identity-security features available. Security teams also need a practical way to **continuously examine identity data, identify concerning patterns, prioritize findings, and communicate actionable results**.

This project addresses that operational problem by providing a lightweight identity posture auditing workflow.

The auditor:

- Collects relevant identity-security data
- Analyzes the data against defined security rules
- Identifies potential posture issues
- Assigns severity and risk scores
- Generates an assessment report
- Sends alerts for important findings
- Provides remediation recommendations

The project is intentionally **not a replacement for Microsoft Entra ID Governance, CIEM, ISPM, Microsoft Defender, or other enterprise security platforms**.

Instead, it demonstrates how a focused security-automation layer can consume identity data and turn it into actionable security information.

---

# 🛡️ Why This Project Matters

## Real Industry Problem

Identity security teams need visibility into issues such as:

- Privileged users without MFA registration
- Stale or inactive accounts
- Excessive privileged access
- Privileged role exposure
- Repeated authentication failures
- High-risk identity findings

Manually reviewing these conditions does not scale well.

This project automates the initial assessment and prioritization process.

---

## 💻 Professional Development Skills

The project demonstrates practical experience with:

- Python application development
- Modular software architecture
- Microsoft Graph API
- Microsoft Entra ID
- Identity and access security
- Security rule development
- Risk scoring
- Automated reporting
- ChatOps
- Docker
- GitHub Actions
- Automated testing
- Python security scanning

The goal is to demonstrate more than point-and-click administration by building an actual security automation workflow.

---

# 🏗️ Architecture

```text
                         Microsoft Entra ID
                                │
                                │
                        Microsoft Graph API
                                │
                                ▼
                       ┌─────────────────┐
                       │     Fetcher     │
                       │                 │
                       │ Retrieve data   │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    Analyzer     │
                       │                 │
                       │ MFA posture     │
                       │ Stale accounts  │
                       │ Role exposure   │
                       │ Sign-in risks   │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Risk Scorer   │
                       │                 │
                       │ Severity        │
                       │ Risk score      │
                       └────────┬────────┘
                                │
                     ┌──────────┴──────────┐
                     │                     │
                     ▼                     ▼
              Security Report        ChatOps Alert
              Markdown / HTML        Teams / Slack
```

### 🔄 Core Security Workflow

The auditor follows a simple security workflow:
```
Detect
  ↓
Assess
  ↓
Score
  ↓
Report
  ↓
Alert
  ↓
Recommend Remediation
```
The system focuses on identifying and communicating security risks rather than automatically changing the tenant.


### 🧪 Mock Mode

The project includes a mock-data mode that allows the complete security-analysis pipeline to run without access to a real Microsoft Entra ID tenant.

This is useful for:

Development
Testing
Demonstrations
Portfolio reviews
CI testing
Recruiters evaluating the project locally

The mock workflow is:
```
mock_data.json
      │
      ▼
   Fetcher
      │
      ▼
   Analyzer
      │
      ▼
 Risk Scorer
      │
      ▼
   Reporter
      │
      ▼
   Alerter
```
The mock dataset simulates identity information such as:

Users
Account status
Last sign-in activity
MFA registration
Privileged role assignments
Sign-in events

This allows the security engine to be developed and tested before connecting it to a live tenant.


### ☁️ Live Mode

The project can also operate against a real Microsoft Entra ID environment through Microsoft Graph.

The live workflow is:
```
Microsoft Entra ID
       │
       ▼
Microsoft Graph API
       │
       ▼
    Fetcher
       │
       ▼
    Analyzer
       │
       ▼
   Risk Scorer
       │
       ├───────────────┐
       ▼               ▼
Security Report    ChatOps Alert
```
The analysis engine remains independent from the data source.

This means the application can use:
```
Mock Data
    OR
Microsoft Graph
```
without requiring a completely different security-analysis implementation.


### 🔐 Security Boundary

The auditor is intentionally read-only.

It does not automatically:

Disable user accounts
Remove directory roles
Change MFA settings
Modify Conditional Access policies
Change tenant configuration

Instead, it:
```
Detects
   ↓
Analyzes
   ↓
Prioritizes
   ↓
Reports
   ↓
Alerts
   ↓
Recommends Remediation
```
This design reduces the risk of automated actions disrupting legitimate business processes.

It also keeps the project focused on security visibility, analysis, and decision support.


### 🔎 Planned Security Checks

The initial security-analysis engine focuses on:

### 1. Privileged Users Without MFA Registration

Identify privileged users whose available registration data indicates that MFA has not been registered.

MFA registration is treated as an identity-security signal. The project does not claim that registration data alone proves whether MFA enforcement is configured.

### 2. Stale or Inactive Accounts

Identify accounts that have not shown recent sign-in activity.

Potential findings can help security teams investigate:

Abandoned accounts
Dormant accounts
Former employee accounts
Unused identities

### 3. Excessive Privileged Access

Identify users with privileged roles that may warrant review.

The purpose is to highlight potentially unnecessary privilege rather than automatically remove access.

### 4. Privileged Role Exposure

Analyze privileged directory-role assignments and highlight potentially excessive concentration of administrative privileges.

### 5. Repeated Authentication Failures

Analyze sign-in activity for repeated failed authentication attempts that may warrant investigation.

### 6. Risk Prioritization

Findings are assigned severity and risk scores so that security teams can focus on the most important issues first.

Example:

🔴 Critical
🟠 High
🟡 Medium
🟢 Low


### 📊 Risk Scoring

The risk-scoring component converts individual security findings into prioritized results.

Conceptually:
```
Security Finding
       ↓
Severity
       ↓
Risk Factors
       ↓
Risk Score
       ↓
Priority
```
The scoring system is designed to make findings easier to understand and act upon.

The exact scoring rules will be documented alongside the implementation so that the assessment remains explainable rather than becoming a mysterious number produced by a computer because apparently computers enjoy secrecy.


### 📄 Automated Reporting

The reporter component will generate structured security-assessment reports.

Reports are intended to contain:

Assessment summary
Total findings
Findings by severity
Affected identities
Evidence
Risk scores
Security recommendations
Overall posture summary

Example:
```
Entra ID Security Assessment
────────────────────────────

Critical Findings:  1
High Findings:      2
Medium Findings:    3
Low Findings:       1

Top Finding:
Privileged user without MFA registration

Risk:
HIGH

Recommendation:
Review the user's authentication-method registration
and verify that appropriate MFA controls are enforced.
```


### 🚨 ChatOps Alerting

Important findings can be forwarded to a ChatOps platform such as:

Microsoft Teams
Slack

The purpose is to reduce the time between:
```
Security Finding
      ↓
Detection
      ↓
Notification
      ↓
Investigation
```
Alerts will be severity-aware so that every minor finding does not become a digital fire alarm.


### 🔑 Microsoft Graph Authentication

The live implementation will use Microsoft Graph with appropriately scoped permissions.

The project follows the principle of least privilege.

For scenarios involving user registration and audit data, permissions will be restricted to the minimum access required by the corresponding Graph operations.

The project will not request broad administrative permissions simply because they are convenient.

No client secrets, passwords, tokens, certificates, or other sensitive credentials will be committed to GitHub.


### ⚙️ Engineering Principles

### Least Privilege

Only the minimum Microsoft Graph permissions required by each operation should be requested.

### Read-Only by Design

The initial auditor identifies and reports risks without making changes to the tenant.

### Separation of Concerns

The application is divided into independent components for:

Authentication
Data collection
Security analysis
Risk scoring
Reporting
Alerting

### Reproducibility

Mock data allows the application to run without access to an organization's tenant.

### Testability

Security rules should be independently testable using predictable datasets.

### Automation

GitHub Actions will automate:
Testing
Linting
Formatting checks
Security scanning
Containerization

Docker will provide a consistent runtime environment for the application.


### 🧰 Technology Stack

Technology	                      Purpose
Python	                          Core application and security analysis
Microsoft Entra ID	              Identity and access data source
Microsoft Graph API	              Programmatic access to Entra data
JSON	                            Mock security dataset
Pytest	                          Automated testing
Black	                            Python code formatting
Flake8	                          Python linting
Bandit	                          Python security scanning
Docker	                          Containerized execution
GitHub Actions	                  Continuous Integration
Microsoft Teams / Slack	          ChatOps alerting


## 📂 Project Structure
```
entra-identity-posture-auditor/
│
├── src/
│   ├── auth.py
│   ├── fetcher.py
│   ├── analyzer.py
│   ├── scorer.py
│   ├── reporter.py
│   └── alerter.py
│
├── mock/
│   └── mock_data.json
│
├── tests/
│
├── reports/
│
├── docs/
│   ├── architecture/
│   ├── security/
│   └── screenshots/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```


## 🧩 Application Components

### auth.py

Responsible for authentication and acquiring access to Microsoft Graph.

### fetcher.py

Responsible for retrieving identity and security data.

The fetcher provides a common interface for obtaining data from:

Mock datasets
Microsoft Graph

### analyzer.py

Contains the security-analysis rules.

This component evaluates collected data and identifies potential security findings.

### scorer.py

Calculates risk and severity for identified findings.

### reporter.py

Converts findings into human-readable security reports.

### alerter.py

Handles ChatOps notifications for important findings.


### 📈 Project Development Flow

```
Real Industry Problem
        ↓
Security Requirements
        ↓
Architecture
        ↓
Mock Dataset
        ↓
Detection Engine
        ↓
Risk Scoring
        ↓
Automated Reports
        ↓
Testing
        ↓
Microsoft Graph Integration
        ↓
ChatOps Alerts
        ↓
Docker
        ↓
GitHub Actions
        ↓
Documentation & Evidence
```
The project is intentionally developed in stages so that every major component can be tested independently before additional complexity is introduced.



### ⏱️ Development Scope

The project is designed as a focused, portfolio-ready MVP that can be developed and demonstrated within approximately 8 hours of focused development.

The objective is to build a complete and demonstrable security-automation workflow rather than attempting to reproduce the functionality of a large enterprise security platform.


### MVP Development Plan

Stage	    Approx. Time	            Focus	Outcome
1	        30 min	                  Project Foundation	Repository structure and mock dataset
2	        75 min	                  Security Analysis	Identity-risk detection engine
3	        45 min	                  Risk Scoring	Severity and risk prioritization
4	        60 min	                  Reporting	Automated security report
5	        45 min	                  Testing	Automated tests for security rules
6	        60 min	                  Microsoft Graph	Live Entra ID integration
7        	30 min	                  Authentication	Secure Graph API access
8	        30 min	                  Mock / Live Mode	Local and real-tenant execution
9	        30 min	                  ChatOps	Security alerts
10	      30 min	                  Docker	Containerized execution
11	      30 min	                  CI	GitHub Actions security pipeline
12	      15 min	                  Documentation	Final README, evidence and cleanup

The schedule is a development target rather than a requirement. Security and correctness take priority over completing a feature simply to satisfy a clock.


### 🧪 Testing Strategy

Testing will cover the security-analysis pipeline using controlled datasets.

Tests will verify that the auditor correctly identifies scenarios such as:
```
Privileged user + MFA not registered
                ↓
             Finding
Inactive account
       ↓
    Finding
Repeated failed sign-ins
       ↓
    Finding
Normal user + normal activity
       ↓
 No unnecessary finding
```
The mock dataset provides deterministic inputs for these tests.


### 🐳 Containerization

A Docker image will package the application and its runtime dependencies.

Conceptually:
```
Source Code
     ↓
Dockerfile
     ↓
Docker Image
     ↓
Docker Container
     ↓
Auditor
```
This provides a consistent execution environment and demonstrates basic cloud-native application practices.


### 🔄 Continuous Integration

GitHub Actions will provide automated checks whenever changes are pushed to the repository.

The intended pipeline is:
```
Git Push
   ↓
GitHub Actions
   ├── Install Dependencies
   ├── Run Tests
   ├── Run Flake8
   ├── Check Black Formatting
   └── Run Bandit
   ↓
Build / Validation Result
```
This helps prevent security and quality regressions from being introduced unnoticed.


### 🛠️ Development Approach

The project follows a practical engineering methodology:
```
Problem
  ↓
Understand Existing Solutions
  ↓
Identify Operational Gap
  ↓
Define Security Requirements
  ↓
Design
  ↓
Build
  ↓
Test
  ↓
Measure
  ↓
Document
```
The purpose is not to create another security product for the sake of having a security product.

The goal is to demonstrate how a developer can identify a practical security problem and build a focused automation solution around it.


## 📚 What This Project Demonstrates

### Microsoft Entra ID

Identity management concepts
Authentication-method visibility
Directory roles
Privileged identity considerations
Identity posture assessment

### Microsoft Graph

API-based identity data retrieval
Permission scoping
Programmatic security analysis

### Python

Modular application design
API integration
Data processing
Security-rule implementation
Risk scoring
Report generation

### Cybersecurity

Least privilege
Identity security
Privileged access monitoring
Security posture assessment
Risk prioritization
Defensive automation

### DevSecOps

Automated testing
Code quality checks
Static security scanning
GitHub Actions
Docker


### 🎯 Portfolio Goal

The project demonstrates the ability to move beyond manually configuring security services and instead build automation around identity-security operations.

It combines:

```
Python
   +
Microsoft Entra ID
   +
Microsoft Graph
   +
Identity Security
   +
Risk Analysis
   +
Security Automation
   +
DevSecOps
   +
Cloud-Native Practices
```

The final result should demonstrate practical security-engineering skills through:
```
Problem
   ↓
Architecture
   ↓
Implementation
   ↓
Security Decisions
   ↓
Testing
   ↓
Findings
   ↓
Reports
   ↓
Automation
```

### 🚀 Future Improvements

Potential future improvements include:

Additional Entra ID posture checks
More advanced risk-scoring rules
Historical posture tracking
Scheduled assessments
Additional ChatOps integrations
Expanded automated testing
Dashboard-based visualization
Additional Microsoft security data sources
Expanded reporting formats

These improvements are intentionally outside the initial MVP scope so that the core security workflow remains focused and maintainable.


### ⚠️ Security & Privacy

This project is intended for authorized environments only.

When using Live Mode:

Use a dedicated test environment where possible
Request only necessary Microsoft Graph permissions
Never commit credentials or access tokens
Store secrets using environment variables or secure secret stores
Do not expose real tenant data in screenshots or reports
Review generated findings before taking administrative action

The auditor itself is designed to remain read-only.


## 👨‍💻 Author

### Faizan Khan Khaleel

BCA | Cloud Architecture & Cybersecurity

This project is part of my hands-on development journey in:

☁️ Cloud Engineering
🔐 Cybersecurity
🐍 Python
🪪 Identity & Access Management
⚙️ Security Automation
🛠️ DevSecOps


### 📌 Project Status

### 🚧 In Development

The project is being developed incrementally, beginning with mock-data analysis before introducing Microsoft Graph integration, testing, reporting, ChatOps, Docker, and GitHub Actions.

The repository will document the implementation, security decisions, testing results, and evidence as development progresses.


**This is the single complete `README.md`**, including the problem, architecture, mock mode, live mode, security boundary, checks, scoring, reporting, ChatOps, Graph permissions, testing, Docker, CI, 8-hour development scope, project structure, portfolio positioning, and future improvements.

I would use this as the **initial master README**, then update the `Project Status`, screenshots, actual commands, test results, and implementation details as we build.
