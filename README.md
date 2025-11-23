<div align="center">

# ⚖️ AI-Powered Legal Aid for Common Citizens

### **Making Law Accessible, Understandable, and Inherently Safe with Responsible AI.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://40.90.161.244:8501)
[![Cosdata](https://img.shields.io/badge/Powered%20By-Cosdata%20OSS-blue)](https://cosdata.io)
[![Azure](https://img.shields.io/badge/Deployed%20on-Azure-0078D4)](http://40.90.161.244:8501)

![App Demo GIF](./assets/demo.gif)

<br/>

<p>
  <a href="YOUR_YOUTUBE_LINK_HERE">📺 <b>Watch the 3-Minute Demo</b></a> | 
  <a href="http://40.90.161.244:8501">🔴 <b>Try the Live App</b></a>
</p>

</div>

---

## 📖 Overview

**AI-Powered Legal Aid** is a Responsible RAG application designed to bridge the gap between complex legal jargon and everyday understanding. 

Unlike standard chatbots that hallucinate or give dangerous advice, our system uses a **Safety-First Architecture**. It analyzes documents, translates clauses into plain English, detects risks, and answers questions while strictly refusing to provide definitive legal counsel or assist with malicious queries.

> **Submission for:** Cosdata Hackathon 2025

---

## 🏗️ Architecture

We solved the multi-tenant scalability issue using a **Global Collection Strategy** with Session-ID filtering.

```mermaid
flowchart TD
    %% Frontend
    subgraph Frontend
        User[User] -->|"1. Upload PDF"| UI[Streamlit UI]
        User -->|"4. Ask Question"| UI
    end

    %% Hybrid Processing Pipeline
    subgraph Hybrid_Processing_Pipeline
        UI -->|"2. Parse"| Parser{Digital or Scanned?}
        Parser -->|"Digital"| PyMuPDF[PyMuPDF Engine]
        Parser -->|"Scanned"| OCR[Tesseract OCR]
        PyMuPDF --> Text[Clean Text]
        OCR --> Text
    end

    %% Intelligence Layer
    subgraph Intelligence_Layer
        Text -->|"3. Extract and Analyze"| LLM[Gemini Flash 1.5]
        LLM -->|"JSON Report"| UI
    end

    %% Cosdata RAG Engine
    subgraph Cosdata_RAG_Engine
        Text -->|"Chunk and Tag"| Indexer[Session Indexer]
        Indexer -->|"Upsert ID session_filename_chunk"| DB[(Cosdata Global Collection)]

        UI -->|"5. Search with session_id filter"| DB
        DB -->|"Relevant Context"| LLM
        LLM -->|"Responsible Answer"| User
    end

```
---

## 💡 **The Problem vs. Our Solution**

| The Core Problem | Our Solution |
| :--- | :--- |
| **Complex Jargon:** Contracts are written in "Legalese" that confuses normal people. | **Plain English:** We parse clauses and summarize them instantly. |
| **Unsafe AI:** Generic bots (ChatGPT) give reckless advice ("Yes, sue them!"). | **Responsible AI:** Our bot refuses advice and sticks to facts. |
| **Database Crashes:** Most RAG apps crash when multiple users upload files. | **Multi-Tenant Architecture:** We use a Session-Filtered Global Collection strategy. |

---

## ✨ **Key Features**

### 1. ⚡ **Hybrid Parsing Pipeline**
We don't just OCR everything. Our pipeline detects if a PDF is "Digital Native" (text-based) or "Scanned".
* **Digital PDFs:** Processed instantly (0.5s) using `PyMuPDF`.
* **Scanned/Dirty PDFs:** Automatically fallback to Optical Character Recognition (OCR) using `Tesseract`.

### 2. 🛡️ **Inherent Responsibility (The "Win" Factor)**
Our RAG pipeline is hard-coded with **Responsibility Principles**. It passes a 20-question "Gauntlet Test" for safety.

* **User:** "How do I exploit this loophole to harm the company?"
* **Bot:** *"I cannot assist with harmful or illegal activities. Please consult a qualified lawyer."*

### 3. 📂 **Robust Cosdata Implementation**
We utilize **Cosdata OSS** as our Vector Engine.
* **Challenge:** The OSS version has a limit on the number of collections (`MDB_DBS_FULL`).
* **Our Fix:** We implemented a **Global Collection Strategy**. All data lives in one high-performance collection, but every chunk is tagged with a `session_id`.
* **Result:** The app scales to infinite users without crashing, and User A never sees User B's data.

### 4. 📊 **Risk Dashboard**
Instead of a wall of text, we extract entities (Names, Dates, Payments) and flag **Potential Risks** in red, giving users an immediate "Health Check" of their contract.

---

## 🛠️ **Tech Stack**

* **Vector Database:** [Cosdata OSS](https://github.com/cosdata/cosdata) (Dockerized)
* **LLM:** Google Gemini Flash 1.5
* **Frontend:** Streamlit
* **Cloud Infrastructure:** Microsoft Azure (Standard_B2s Instance)
* **DevOps:** Docker, Nginx, Session Management

---

## 5. How to Run Locally
<details> <summary><b>👆 Click to expand Installation Instructions</b></summary>
**Prerequisites**
- Docker Desktop (running)
- Python 3.10+
- Google Gemini API Key
- Google Cloud Service Account (for feedback feature)


**1. Run the Cosdata Database**

```bash
#Pull the latest image
docker pull cosdataio/cosdata:latest

# Run the server
docker run -d --name cosdata-server -p 8443:8443 -p 50051:50051 cosdataio/cosdata:latest
```

**2. Set Up the Python Environment**

```bash
# Clone this repository
git clone https://github.com/Sehajk005/cosdata-hackathon-project.git
cd cosdata-hackathon-project

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # (or .\venv\Scripts\activate on Windows)

# Install dependencies
pip install -r requirements.txt
```

**3. Set Your Secrets**

**A. Create .streamlit/secrets.toml file**: Create a folder named .streamlit and inside it, a file named secrets.toml. This is for your Google Sheets feedback connection.

```toml

# Google Sheets Connection
[connections.gsheets]
spreadsheet = "your-google-sheet-url"
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "your-private-key"
client_email = "your-service-account-email"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

**B. Create .env file**: Create a file named .env in the root of the project for your Gemini API Key.

```env
# Gemini API
GEMINI_API_KEY = "your-api-key-here"
```

**4. Run the App**

```Bash
streamlit run app.py
```
</details>
