# Pro Analytics 01: Setup and Workflow Guide

This repository provides a clear, concise guide to help set up a machine for Python projects, 
initialize a new Python project, and follow a repeatable project workflow 
when developing professional Python projects. 

The instructions are divided into three parts.

## Part 1: Set Up Machine & Sign up for GitHub
Go to [🟢 Machine Setup](01-machine-setup/MACHINE-SETUP.md) to prepare for Python projects.
Start here to set up a machine for the first time (or to upgrade or verify professional tools).

This section contains **one-time tasks** including:
1. View file extensions and hidden files and folders.
2. Optional: Install (or verify) a package manager for your operating system.
3. Install Python, Git, and Visual Studio (VS) Code for your operating system.
4. Configure Git
5. Install common VS Code extensions.
6. Create a folder on your machine to hold your GitHub projects. 
7. Create a GitHub account (join 100 Million Developers!)

---

## Part 2: Initialize a Project
Go to [🟠 Project Initialization](02-project-initialization/PROJECT-INITIALIZATION.md)  when **starting a new project**.

This section walks you through the steps to either:
1. Copy an existing project OR start a new project from scratch.
2. Clone your new GitHub repo to your machine. 
3. Add common files such as .gitignore and requirements.txt.
4. Git add-commit-push the changes to GitHub.
5. Create a local project virtual environment for Python.

---

## Part 3: Work on the Project Over Time
Go to [🔵 Repeatable Workflow](03-repeatable-workflow/REPEATABLE-WORKFLOW.md) for ongoing project development.

This section provides the **repeatable steps** for working on Python projects. 
These steps are typically followed whenever we make changes to a project. The workflow includes:
1. Pull any recent changes from GitHub.
2. Activate the virtual environment.
3. Install dependencies.
4. Run scripts and/or Jupyter notebooks.
5. Make updates, verify the code still runs, and git add-commit-push to GitHub. 

---

## Important

- Follow the instructions carefully.
- Follow the instructions in the recommended order.
- Verify each step before proceeding. 

## Celebrate
Follow each step carefully. 
We have helped hundreds of new analysts get started with professional Python. 
Verify you can run both a script and a notebook successfully. 
Then, celebrate - that's a big iceberg needed to get started with Professional Python.

## Follow The Proven Path Provided
Hopefully, each step is not too bad and things go well. 
When they don't - that's to be expected. 
Part of the reason we get hired is to "figure things out" and we are here to help you do that. 
Learn to do a web search, and experiment with free AI assistants to help explain and provide any additional details needed. 
Remember, YOU are in charge. 
This is the process we support and these instructions work. 
Do NOT deviate unless you agree to invest time and energy to ensure any of the many alternate paths work for you throughout the program. 

## Explore

AFTER that is where the power and joy of working with Python begins. 
Keep good notes. 
Save the working versions and then, change things. For example:

- Rename a variable. 
- Add a new statement. 
- Comment things out.
- Rename a function. 
- View the logs. Log something new (e.g., every function when called and before returning a value).

Working with code is a fun, safe, rewarding way to learn. 
If you enjoy puzzles, getting value from Python is a great way to earn a living. 

## CheatSheet: Commands to Manage Virtual Environment

For Windows PowerShell (change if using Mac/Linux). 
Keep these notes in every project README.md.

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel
py -m pip install --upgrade -r requirements.txt
```

## CheatSheet: Commands to Run Python Scripts

Remember to activate your .venv (and install packages if they haven't been installed yet) before running files.
Verify that all external packages imported into a file are included in requirements.txt (and have NOT been commented out).

```shell
py demo_script.py
py do_stats.py
py draw_chart.py
py greet_user.py
```

## CheatSheet: Commands to Git add-commit-push

```shell
git add .
git commit -m "custom message"
git push -u origin main
```

## OPTIONAL: Listen to the Audio Guides

If you prefer listening **while following the written steps above**, optional [**Audio Guides**](https://denisecase.github.io/pro-analytics-01-audio-guides/) are available. These are **AI-generated two-person podcasts**.

The audio is **supplementary** and **not a replacement for the written instructions**.
The guides are not necessarily recommended. They may be distracting, and the speakers mispronounce key files and commands.
They are mostly interesting from a state-of-the-art perspective.

## OPTIONAL: Share Feedback

Feel free to ask questions in the [GitHub Discussions](https://github.com/denisecase/pro-analytics-01/discussions) or raise a [GitHub Issue](https://github.com/denisecase/pro-analytics-01/issues) if you have suggestions or need additional clarification. 

# Sales Insights Dashboard – README

## SQL Queries
- `Top Customers`: Shows total sales per customer using `sale` and `customer` tables.
- `Sales Trend`: Aggregates sales by `sale_date` to track trends over time.

## Dashboard Design
- Used a bar chart for Top Customers to highlight biggest spenders.
- Used a line chart for Sales Trend to display time-based performance.
- Added a category slicer to allow interactive filtering of visuals.

## Screenshots

### 1. Power BI Model View
![Model View](images/table_relationships.png)

### 2. Query Results
![Query Results](images/final_dashboard.png)

### 3. Final Dashboard
![Dashboard](images/final_dashboard.png)

## OLAP Sales Analysis

This script connects to `smart_sales.db` and performs:
- Revenue comparison by product category (bar chart)
- Monthly sales trend (line chart)
- Sales by product and region (pivot table)

### To Run:
1. Activate virtual environment
2. Install dependencies: `pip install pandas matplotlib`
3. Run: `python olap_analysis.py`
# 📊 OLAP Analysis of Smart Sales Data

## 🎯 Section 1: The Business Goal

**Goal**: Identify the **average sale amount** for **electronic products** sold in the **month of May**.

This goal helps the business understand seasonal performance for high-value product categories and optimize marketing, inventory, and pricing strategies accordingly.

---

## 📁 Section 2: Data Source

The analysis uses a structured **data warehouse** in the form of a SQLite database file named `smart_sales.db`, located in the `/Data/dw/` directory. The key tables and columns used were:

- **`sale` table**  
  - `sale_date`: used to extract monthly trends  
  - `sale_amount`: used for revenue calculations  
  - `product_id`: used to join with product data

- **`product` table**  
  - `product_id`: primary key for joining  
  - `category`: used to filter by `'Electronics'`

---

## 🛠️ Section 3: Tools

- **Python** with:
  - `pandas` for data manipulation and pivot tables
  - `matplotlib` for visualizations (bar and line charts)
- **SQLite** as the data storage backend
- **Visual Studio Code (VS Code)** for development and script execution

These tools were selected for their efficiency, reproducibility, and suitability for OLAP-style exploration in a script-based environment.

---

## 🔄 Section 4: Workflow & Logic

- **Descriptive Dimensions**: `category`, `product_id`, `sale_date (month)`
- **Numeric Metric**: `sale_amount`
- **Aggregations**:
  - `SUM(sale_amount)` to calculate total revenue
  - `AVG(sale_amount)` for average sales by filter
- **Slicing**: Focused on `'Electronics'` category
- **Dicing**: By product and region (via pivot table)
- **Drilldown**: From year ➡️ month (using `sale_date`)

> _Note: If using a graphical tool like Power BI or Tableau, include screenshots below._

---

## 📈 Section 5: Results

### 💡 Key Insights:
- **Bar Chart**: Total revenue by product category
- **Line Chart**: Monthly sales trends
- **Pivot Table**: Sales aggregated by product and region

The results indicate that **electronics performed exceptionally well in May**, with a high average sale amount reflecting strong demand for higher-value products.

---

## 🚀 Section 6: Suggested Business Action

- Boost marketing efforts for electronics during Q2, especially May.
- Investigate regions with below-average performance using the pivot breakdown.
- Optimize inventory levels around seasonal peaks identified in the sales trend.

---

## 🧩 Section 7: Challenges

| Issue | Resolution |
|-------|------------|
| ❌ `no such table: sales` | Verified correct table names using `sqlite_master`, changed `sales` to `sale` |
| ❌ Charts not displaying | Added `plt.show()` and confirmed output through VS Code |
| ❌ DB connection path error | Updated path to: `C:/Repos/smart-store-michaelcarter/Data/dw/smart_sales.db` |

---

📌 _For running instructions, refer to the main section of this repo or the script header in `scripts/olap_analysis.py`._
