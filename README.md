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
## How It Works
1. *Upload / Connect:* the user provides files or a data source.
2. *Scan:* the detection engine analyzes content for PII.
3. *Classify:* each finding is tagged by PII type and sensitivity.
4. *Score:* the risk module assigns a risk level.
5. *Log:* results and actions are saved as audit evidence.
6. *Report:* the user views findings and exports the report.
## Screenshots
## Installation & Setup
## Usage
1. Open the application in your browser / terminal.
2. Upload a file or select a data source.
3. Click *Scan* to start PII discovery.
4. Review findings, risk scores and the audit log.
5. Export the report if needed.
## Sample Results
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
Prerna Sharma	Team Member
Pranav Arora	Team Member
Sachin Sir	Mentor
## Team Name
Infoshield
## Acknowledgements
We would like to thank AIORI Hackathon 3 for providing the opportunity to work on this cybersecurity problem.
We are grateful to our mentor, Sachin Sir, for his guidance and support.
We also acknowledge the data-protection framework resources published by the Ministry of Electronics and Information Technology (MeitY), Government of India, which provide useful background for understanding data protection and privacy.
