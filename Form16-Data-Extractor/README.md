# 📄 Form 16 PDF Data Extractor to JSON

A lightweight and efficient Python automation tool designed to process **Form 16 (TDS Certificate) PDF** files. It intelligently extracts critical tax, salary, and identification data, transforming it into a clean, structured JSON format.

Instead of relying on unstable, hardcoded index matching (e.g., `lines[4]`), this project utilizes **Regex (Regular Expressions)** and **Keyword-Based Parsing**. This ensures high reliability—even if the PDF layout or line spacing shifts slightly, the data extraction remains accurate.

---

## ✨ Key Features

* **Robust Text Extraction:** Utilizes `pdfplumber` instead of older libraries like `PyPDF4` or `PyPDF2`, ensuring clean text extraction without breaking or merging words awkwardly.
* **Smart Regex Matching:** Dynamically identifies and extracts the PAN and TAN card numbers of both the employer and employee based on their strict standard patterns.
* **Dynamic Year Parsing:** Auto-detects and extracts the specific Assessment Year (AY) directly from the text flow.
* **Financial Data Capture:** Accurately parses the employee's Gross Salary and the Total TDS Deducted from the internal tables.
* **Clean JSON Output:** Delivers the extracted data in a neat, well-structured JSON format, ready to be pushed to any database or web API endpoint.

---
