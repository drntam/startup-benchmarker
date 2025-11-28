# 🚀 Startup Performance Simulator  
### *Visualizing How Business Assumptions Shape Financial Outcomes*

The **Startup Performance Simulator** is an interactive data-driven dashboard that helps users explore how a startup’s financial trajectory changes when core business assumptions shift. Instead of relying on static spreadsheets, this project turns key startup drivers—CAC, churn, ARPU, cost structure, user growth—into adjustable parameters. As users tweak these inputs, the dashboard instantly updates to show the impact on revenue, profit, and cash flow over time.

This project combines **Altair**, **D3.js**, and **Tableau** to create an explorable visual environment that makes complex financial dynamics intuitive for founders, students, and early-stage investors.  
  

---

## 📊 Dataset  
**Source:** *SaaS Financial Market Dataset* (Kaggle)
**Size:** 2,500 rows (500 SaaS companies × 5 years)  

**Attributes include:**  
- Company name, segment, region, country
- Annual revenue, expenses, profit  
- Churn rate, ARPU, active customers  
- Market share and founding year  

All data is synthetic and programmatically generated, making it realistic and safe for open use.

---

## 🧰 Tech Stack  
- **Altair** — interactive line, bar, and scatter charts  
- **D3.js** — interactive industry distribution visualization  
- **Tableau** — geographical startup location map  
- **Python (NumPy, Pandas)** — data preprocessing  
- **HTML/CSS/JS** — for the final website  

---

## 📈 Visualizations Included  

### 1. **Startup Location Map** *(Tableau)*  
- **Interaction:** Region selection + hover  
- **Insight:** Shows global distribution of startup activity  

### 2. **Financial Trend Line Chart** *(Altair)*  
- **Interaction:** Dropdown filters + hover tooltips  
- **Insight:** Reveals how revenue, expenses, and profit evolve over time  

### 3. **Cost Structure Grouped Bar Chart** *(Altair)*  
- **Interaction:** Hover reveal  
- **Insight:** Compares fixed vs. variable costs  

### 4. **Industry Distribution Bar Chart** *(D3.js)*  
- **Interaction:** Sorting + click highlight + tooltips  
- **Insight:** Displays how many startups fall into each industry category  

### 5. **Profit Margin vs Revenue Growth Scatter Plot** *(Altair)*  
- **Interaction:** Brushing or click highlight  
- **Insight:** Shows how profitability relates to growth strategies  

---

## 🔍 Project Goals  
- Make startup financial modeling *interactive and approachable*  
- Help users understand how small assumption changes ripple through results  
- Provide scenario-based insights, not just static summaries  
- Demonstrate the power of combining visualization tools  

---

## 🌐 Project Website  

> https://drntam.github.io/startup-benchmarker/

---
