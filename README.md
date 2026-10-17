## Team Name
**Infoshield**

Presentation Video..!!

[![PrivacyShield AI - Video](https://youtube.com)](https://youtu.be/sNKK1PAr2T0)


PrivacyShield AI
AI-Powered Personal Data Discovery and Privacy Auditing
Identify sensitive personal information. Assess exposure risks. Strengthen data privacy.
PrivacyShield AI is a privacy-auditing project designed to identify Personally Identifiable Information (PII) in datasets, assess potential exposure risks, and help users understand where sensitive information may be present.
Developed as part of AIORI Hackathon — Problem Statement PS019.
## Overview
Organizations store huge amounts of data across files, databases and documents, and often don't know where personal data (PII) is hiding. This project is an AI-powered platform that automatically discovers personal data, evaluates how risky its exposure is, and keeps audit-ready evidence for compliance. It was built for *AIORI-3 Hackathon, Problem Statement PS019: Personal Data Discovery*.
## Problem Statement
- Personal data (names, emails, phone numbers, Aadhaar/PAN, bank details, etc.) is scattered across unstructured and structured sources.
- Manual discovery is slow, error-prone and does not scale.
- Without visibility, organizations cannot assess risk or prove compliance with privacy regulations (e.g., DPDP Act 2023, GDPR).
- Audit trails are often missing, incomplete or hard to verify.
## Our Solution
We built an automated privacy auditing platform that:
1. *Discovers* PII across data sources using AI and pattern-based detection.
2. *Assesses* the risk of each exposure based on data sensitivity and context.
3. *Maintains* tamper-evident audit evidence so compliance can be demonstrated at any time.
## Key Features
- 🔍 *PII Detection:* identifies personal and sensitive data in files and datasets 
- ⚠️ *Risk Assessment:* scores exposure by sensitivity and severity
- 🧾 *Audit Evidence:* logs every scan, finding and action for compliance reporting
- 📊 *Dashboard & Reports:* clear view of findings and risk levels
- 🔐 *Privacy-first Design:* sensitive values are masked in outputs
## System Architecture
*Components:*
- *Data Ingestion Layer:* accepts files / data sources for scanning
- *PII Detection Engine:* regex + NLP/ML models to find personal data
- *Risk Scoring Module:* classifies findings as Low / Medium / High / Critical
- *Audit Log Store:* records findings and actions as evidence
- *User Interface:* dashboard and reports
## Technology Stack
Frontend : app.py
Backend : database.py
github
## How It Works
1. *Upload / Connect:* the user provides files or a data source.
2. *Scan:* the detection engine analyzes content for PII.
3. *Classify:* each finding is tagged by PII type and sensitivity.
4. *Score:* the risk module assigns a risk level.
5. *Log:* results and actions are saved as audit evidence.
6. *Report:* the user views findings and exports the report.
## Screenshots
<img width="1366" height="768" alt="ss 1" src="https://github.com/user-attachments/assets/d496a47d-41de-418a-9257-b236c24d8d70" />
<img width="1366" height="768" alt="ss 2" src="https://github.com/user-attachments/assets/592688c7-1c5e-41cb-9aee-4d8b2702c644" />
<img width="1366" height="768" alt="ss 3" src="https://github.com/user-attachments/assets/f4a4d184-9a4c-4328-b47a-9f57c5a07731" />
<img width="1366" height="768" alt="ss 4" src="https://github.com/user-attachments/assets/c3d02125-0387-4de7-b859-aae2a6a993d9" />

## Usage
1. Open the application in your browser / terminal.
2. Upload a file or select a data source.
3. Click *Scan* to start PII discovery.
4. Review findings, risk scores and the audit log.
5. Export the report if needed.
## Sample Results
| Input | Detected PII | Risk Level |
| hackathon_test.csv | Name, Email, Phone | Medium |
| requirements.txt | Aadhaar, PAN, Address | High |
## Security & Privacy Considerations
- Detected PII is *masked* in dashboards and reports.
- Processing is done locally / in a controlled environment; no data is shared with third parties.
- Secrets and API keys are stored in environment variables, never committed.
- Audit logs are append-only to preserve integrity.
- Follows data-minimization: only what is needed for detection is stored.
## Limitations & Future Scope
**Limitations**
The scanner has some important limitations to consider.
**Rule dependency:** Detection quality depends on the rules configured for the scanner.
**False positives:** Some fields may be flagged even when they do not contain personal data.
**False negatives:** Some relevant fields may be missed if their patterns are not covered by the rules.
**Limited input sources:** The proposed scope covers synthetic CSV files and one supported SQL database.
**Metadata availability:** Missing or incomplete source metadata can limit the quality of mapping results.
**Evaluation coverage:** A small labelled test set may not represent all possible datasets.
**Need for human review:** Technical findings alone cannot establish the complete context or legal significance of a data field.
These limitations should be assessed during implementation and testing.
**Future Scope**
There are several ways the project could be improved in the future.
**More data sources:** Extend support to additional databases and structured file formats.
**Better detection rules:** Improve the coverage and accuracy of configurable rules.
**Detection explanations:** Show which rule triggered a finding and why it was flagged.
**Interactive reports:** Add filters and visual summaries to make findings easier to examine.
**Inventory comparison:** Compare results from different scans to identify changes in discovered fields or metadata.
**Expanded testing:** Use larger labelled datasets to evaluate precision and recall more reliably.
**Improved access control:** Add stronger controls for accessing sensitive inventories and reports.
**Review tracking:** Introduce a way to track findings that have been reviewed or require follow-up.
**Scalability:** Improve processing for larger datasets.
These improvements could make the scanner more useful for repeatable privacy reviews while keeping its findings transparent and open to human validation.
## Team Members
Prerna Sharma

Pranav Arora

Sachin Sir (Mentor)



## Acknowledgements
We would like to thank AIORI Hackathon 3 for providing the opportunity to work on this cybersecurity problem.
We are grateful to our mentor, Sachin Sir, for his guidance and support.
We also acknowledge the data-protection framework resources published by the Ministry of Electronics and Information Technology (MeitY), Government of India, which provide useful background for understanding data protection and privacy.
