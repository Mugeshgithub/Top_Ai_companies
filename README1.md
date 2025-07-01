
# 🚀 AI 100 Firmographics Dashboard

An end-to-end data analytics project built in **Snowflake** using **Streamlit**, delivering real-time insights on the top 100 AI companies worldwide. This repo covers everything from Snowflake Marketplace data collection to dashboard deployment — all version-controlled in GitHub.

---

## 📌 Overview

This project explores:
- Business models (SaaS, B2B, etc.)
- Funding stages (Angel to Series H)
- Company ages
- Sector trends and geography

Built as a full-stack solution using:
- **Snowflake** (Data Warehouse + Semantic Modeling)
- **Streamlit** (In-Snowflake dashboarding)
- **GitHub** (CI + Code versioning)

---

## 🔁 Project Workflow

### 1️⃣ Data Collection (Snowflake Marketplace)
- Data sourced directly from **Snowflake Marketplace**
- Dataset: Firmographic data on 100 top AI companies
- Loaded and queried using Snowflake Worksheets
- Fields included: `Company Name`, `Business Model`, `Startup Stage`, `Founding Year`, `Headquarters`, etc.

### 2️⃣ Data Cleaning & Preprocessing
- Handled missing/null values
- Created calculated fields:
  - `company_age` = current year − founding year
  - Aggregated company counts by category
- Standardized category labels:
  - e.g., `"Usage-based"` → `"Usage Based"`
- Removed duplicates and harmonized startup stages

### 3️⃣ Semantic Modeling
- Created semantic YAML models to:
  - Enable **natural language querying**
  - Standardize business terms (e.g., company count, startup stage)
- Example:
  ```yaml
  semantic_model:
    name: firmographics_ai
    dimensions:
      - name: stage
        type: categorical
  ```

### 4️⃣ Streamlit App Development
- Built an **interactive dashboard** directly in Snowflake via Streamlit
- Key tabs:
  - `Valuation Insights`
  - `Geographic Trends`
  - `Business Models`
  - `Company Age Analysis`
- Charts built with **Altair** (can integrate Plotly for more interactivity)
- Responsive layout with real-time database connection

### 5️⃣ GitHub Integration
- Repository: [Top_AI_Companies](https://github.com/Mugeshgithub/Top_Ai_companies)
- Configured **Snowflake Git Integration** using PAT
- Pushed `streamlit_app.py` and `environment.yml`
- Enables tracking changes, deploying updates, and collaborating

---

## 📊 Sample Insights

| Insight | Observation |
|--------|-------------|
| **Top business model** | SaaS dominates across funding stages |
| **Seed stage companies** | Lean toward B2C and Usage Based models |
| **Age cluster** | Most firms are 3–7 years old |
| **Funding stages** | Series B stage has the highest company count |

---

## 📂 Project Structure

```
├── streamlit_app.py          # Main dashboard script
├── environment.yml           # Required packages
├── semantic_models/          # Cortex YAML files (optional)
└── README.md                 # Project walkthrough
```

---

## ✅ How to Run (In Snowflake)

1. Clone this repo using Snowflake Streamlit
2. Ensure `GIT_API_INTEGRATION` is set correctly
3. Click **Run** on `streamlit_app.py` inside Snowflake
4. Explore dashboard tabs: valuation, trends, models, company age

---

## 🔐 Git Integration Notes

- Use a GitHub **Personal Access Token (PAT)** to authenticate
- Push changes with commit messages from within Snowflake’s Streamlit editor
- Set branch permissions properly to avoid conflicts

---

## 👨‍💻 Author

**Mugesh Murugaiyan**  
[LinkedIn](https://www.linkedin.com/in/mugeshmurugaiyan) • `snazzy.mugi@gmail.com`  
Data Analyst | AI Tools Explorer | Design + Insight Driven

---

## 🤝 Contributions

Open to feedback and contributions. PRs welcome!

---
