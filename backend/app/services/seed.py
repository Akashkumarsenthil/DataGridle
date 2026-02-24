"""Seed the database with domain categories, topics, roadmap items, YouTube resources, and sample questions."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.category import Category
from app.models.topic import Topic
from app.models.company import CompanyTag
from app.models.user import User, UserRole
from app.models.roadmap import RoadmapItem
from app.models.learning import LearningResource
from app.models.question import Question
from app.core.security import hash_password


# ──────────────────────────────────────────────
# 1. CATEGORIES (10 data domains)
# ──────────────────────────────────────────────

CATEGORIES = [
    {
        "name": "Data Engineering",
        "slug": "data-engineering",
        "description": "SQL, ETL, data modeling, Spark, Airflow, and pipeline design",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/2172/2172891.png",
    },
    {
        "name": "Data Science",
        "slug": "data-science",
        "description": "Statistics, pandas, hypothesis testing, A/B tests, and EDA",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
    },
    {
        "name": "Machine Learning",
        "slug": "machine-learning",
        "description": "Model training, evaluation, feature engineering, NLP, and deep learning",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/2103/2103658.png",
    },
    {
        "name": "Data Analytics",
        "slug": "data-analytics",
        "description": "Business metrics, dashboards, product analytics, Excel and SQL",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/1828/1828791.png",
    },
    {
        "name": "MLOps",
        "slug": "mlops",
        "description": "ML pipelines, model serving, monitoring, CI/CD for ML, and experiment tracking",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/4616/4616734.png",
    },
    {
        "name": "DevOps / DataOps",
        "slug": "devops-dataops",
        "description": "Infrastructure as code, CI/CD, Docker, Kubernetes, and data orchestration",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/919/919853.png",
    },
    {
        "name": "Generative AI / LLM Engineering",
        "slug": "generative-ai",
        "description": "Prompt engineering, RAG, fine-tuning, LangChain, vector databases, and LLM deployment",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
    },
    {
        "name": "Business Intelligence",
        "slug": "business-intelligence",
        "description": "Data visualization, Tableau, Power BI, KPIs, reporting, and storytelling",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/3281/3281289.png",
    },
    {
        "name": "Data Architecture",
        "slug": "data-architecture",
        "description": "Data lakes, warehouses, mesh, governance, catalog, and schema design",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/2570/2570576.png",
    },
    {
        "name": "NLP / Computer Vision",
        "slug": "nlp-computer-vision",
        "description": "Text processing, transformers, image classification, object detection, and multimodal AI",
        "icon_url": "https://cdn-icons-png.flaticon.com/512/4712/4712035.png",
    },
]

# ──────────────────────────────────────────────
# 2. TOPICS per category  (8-12 each)
# ──────────────────────────────────────────────

TOPICS = {
    "data-engineering": [
        {"name": "SQL Basics", "difficulty_level": "easy", "order_index": 1},
        {"name": "SQL Joins", "difficulty_level": "easy", "order_index": 2},
        {"name": "Aggregations & GROUP BY", "difficulty_level": "easy", "order_index": 3},
        {"name": "Subqueries", "difficulty_level": "medium", "order_index": 4},
        {"name": "Window Functions", "difficulty_level": "medium", "order_index": 5},
        {"name": "CTEs & Recursive Queries", "difficulty_level": "medium", "order_index": 6},
        {"name": "Data Modeling", "difficulty_level": "hard", "order_index": 7},
        {"name": "ETL Pipelines", "difficulty_level": "hard", "order_index": 8},
        {"name": "Apache Spark", "difficulty_level": "hard", "order_index": 9},
        {"name": "Airflow Orchestration", "difficulty_level": "hard", "order_index": 10},
        {"name": "Performance Optimization", "difficulty_level": "hard", "order_index": 11},
        {"name": "System Design", "difficulty_level": "very_hard", "order_index": 12},
    ],
    "data-science": [
        {"name": "Python for Data Science", "difficulty_level": "easy", "order_index": 1},
        {"name": "Pandas & NumPy", "difficulty_level": "easy", "order_index": 2},
        {"name": "Descriptive Statistics", "difficulty_level": "easy", "order_index": 3},
        {"name": "Probability Distributions", "difficulty_level": "medium", "order_index": 4},
        {"name": "Hypothesis Testing", "difficulty_level": "medium", "order_index": 5},
        {"name": "A/B Testing", "difficulty_level": "medium", "order_index": 6},
        {"name": "Exploratory Data Analysis", "difficulty_level": "medium", "order_index": 7},
        {"name": "Feature Engineering", "difficulty_level": "hard", "order_index": 8},
        {"name": "Regression Models", "difficulty_level": "hard", "order_index": 9},
        {"name": "Classification Models", "difficulty_level": "hard", "order_index": 10},
    ],
    "machine-learning": [
        {"name": "Supervised Learning Basics", "difficulty_level": "easy", "order_index": 1},
        {"name": "Linear & Logistic Regression", "difficulty_level": "easy", "order_index": 2},
        {"name": "Decision Trees & Random Forests", "difficulty_level": "medium", "order_index": 3},
        {"name": "Ensemble Methods", "difficulty_level": "medium", "order_index": 4},
        {"name": "SVM & Kernel Methods", "difficulty_level": "medium", "order_index": 5},
        {"name": "Unsupervised Learning", "difficulty_level": "medium", "order_index": 6},
        {"name": "Neural Networks Fundamentals", "difficulty_level": "hard", "order_index": 7},
        {"name": "Deep Learning with PyTorch/TF", "difficulty_level": "hard", "order_index": 8},
        {"name": "Model Evaluation & Tuning", "difficulty_level": "hard", "order_index": 9},
        {"name": "ML System Design", "difficulty_level": "very_hard", "order_index": 10},
    ],
    "data-analytics": [
        {"name": "SQL for Analytics", "difficulty_level": "easy", "order_index": 1},
        {"name": "Excel & Spreadsheets", "difficulty_level": "easy", "order_index": 2},
        {"name": "Data Cleaning", "difficulty_level": "easy", "order_index": 3},
        {"name": "Metrics & KPIs", "difficulty_level": "medium", "order_index": 4},
        {"name": "Product Analytics", "difficulty_level": "medium", "order_index": 5},
        {"name": "Cohort & Funnel Analysis", "difficulty_level": "medium", "order_index": 6},
        {"name": "Dashboard Design", "difficulty_level": "medium", "order_index": 7},
        {"name": "Statistical Analysis", "difficulty_level": "hard", "order_index": 8},
        {"name": "Stakeholder Communication", "difficulty_level": "hard", "order_index": 9},
    ],
    "mlops": [
        {"name": "ML Lifecycle Overview", "difficulty_level": "easy", "order_index": 1},
        {"name": "Experiment Tracking (MLflow)", "difficulty_level": "easy", "order_index": 2},
        {"name": "Model Versioning & Registry", "difficulty_level": "medium", "order_index": 3},
        {"name": "Feature Stores", "difficulty_level": "medium", "order_index": 4},
        {"name": "ML Pipelines (Kubeflow/Vertex)", "difficulty_level": "medium", "order_index": 5},
        {"name": "Model Serving & APIs", "difficulty_level": "hard", "order_index": 6},
        {"name": "Monitoring & Drift Detection", "difficulty_level": "hard", "order_index": 7},
        {"name": "CI/CD for ML", "difficulty_level": "hard", "order_index": 8},
        {"name": "Infrastructure & Scaling", "difficulty_level": "very_hard", "order_index": 9},
    ],
    "devops-dataops": [
        {"name": "Linux & Shell Basics", "difficulty_level": "easy", "order_index": 1},
        {"name": "Git & Version Control", "difficulty_level": "easy", "order_index": 2},
        {"name": "Docker Containers", "difficulty_level": "easy", "order_index": 3},
        {"name": "CI/CD Pipelines", "difficulty_level": "medium", "order_index": 4},
        {"name": "Kubernetes", "difficulty_level": "medium", "order_index": 5},
        {"name": "Infrastructure as Code (Terraform)", "difficulty_level": "medium", "order_index": 6},
        {"name": "Cloud Services (AWS/GCP/Azure)", "difficulty_level": "hard", "order_index": 7},
        {"name": "Monitoring & Observability", "difficulty_level": "hard", "order_index": 8},
        {"name": "Data Orchestration", "difficulty_level": "hard", "order_index": 9},
        {"name": "Security & Networking", "difficulty_level": "very_hard", "order_index": 10},
    ],
    "generative-ai": [
        {"name": "LLM Fundamentals", "difficulty_level": "easy", "order_index": 1},
        {"name": "Prompt Engineering", "difficulty_level": "easy", "order_index": 2},
        {"name": "OpenAI & Hugging Face APIs", "difficulty_level": "easy", "order_index": 3},
        {"name": "LangChain & Orchestration", "difficulty_level": "medium", "order_index": 4},
        {"name": "Retrieval Augmented Generation (RAG)", "difficulty_level": "medium", "order_index": 5},
        {"name": "Vector Databases", "difficulty_level": "medium", "order_index": 6},
        {"name": "Fine-Tuning LLMs", "difficulty_level": "hard", "order_index": 7},
        {"name": "Evaluation & Safety", "difficulty_level": "hard", "order_index": 8},
        {"name": "Agents & Tool Use", "difficulty_level": "hard", "order_index": 9},
        {"name": "Production LLM Deployment", "difficulty_level": "very_hard", "order_index": 10},
    ],
    "business-intelligence": [
        {"name": "BI Concepts & Data Literacy", "difficulty_level": "easy", "order_index": 1},
        {"name": "SQL for BI", "difficulty_level": "easy", "order_index": 2},
        {"name": "Tableau Fundamentals", "difficulty_level": "easy", "order_index": 3},
        {"name": "Power BI Fundamentals", "difficulty_level": "easy", "order_index": 4},
        {"name": "Data Visualization Best Practices", "difficulty_level": "medium", "order_index": 5},
        {"name": "DAX & Calculated Fields", "difficulty_level": "medium", "order_index": 6},
        {"name": "KPI Design & Reporting", "difficulty_level": "medium", "order_index": 7},
        {"name": "Data Storytelling", "difficulty_level": "hard", "order_index": 8},
        {"name": "Advanced Analytics in BI", "difficulty_level": "hard", "order_index": 9},
    ],
    "data-architecture": [
        {"name": "Relational Database Design", "difficulty_level": "easy", "order_index": 1},
        {"name": "Normalization & Denormalization", "difficulty_level": "easy", "order_index": 2},
        {"name": "Data Warehouse Concepts", "difficulty_level": "medium", "order_index": 3},
        {"name": "Dimensional Modeling (Star/Snowflake)", "difficulty_level": "medium", "order_index": 4},
        {"name": "Data Lakes & Lakehouses", "difficulty_level": "medium", "order_index": 5},
        {"name": "Data Mesh", "difficulty_level": "hard", "order_index": 6},
        {"name": "Data Governance & Cataloging", "difficulty_level": "hard", "order_index": 7},
        {"name": "Streaming Architecture (Kafka)", "difficulty_level": "hard", "order_index": 8},
        {"name": "Cloud Data Platforms", "difficulty_level": "hard", "order_index": 9},
        {"name": "System Design for Data", "difficulty_level": "very_hard", "order_index": 10},
    ],
    "nlp-computer-vision": [
        {"name": "Text Preprocessing", "difficulty_level": "easy", "order_index": 1},
        {"name": "Word Embeddings (Word2Vec, GloVe)", "difficulty_level": "easy", "order_index": 2},
        {"name": "Sequence Models (RNN, LSTM)", "difficulty_level": "medium", "order_index": 3},
        {"name": "Transformers & Attention", "difficulty_level": "medium", "order_index": 4},
        {"name": "BERT, GPT & Pre-trained Models", "difficulty_level": "medium", "order_index": 5},
        {"name": "Image Classification (CNNs)", "difficulty_level": "medium", "order_index": 6},
        {"name": "Object Detection (YOLO, RCNN)", "difficulty_level": "hard", "order_index": 7},
        {"name": "Image Segmentation", "difficulty_level": "hard", "order_index": 8},
        {"name": "Multimodal Models", "difficulty_level": "hard", "order_index": 9},
        {"name": "Deployment & Optimization", "difficulty_level": "very_hard", "order_index": 10},
    ],
}

# ──────────────────────────────────────────────
# 3. ROADMAP ITEMS per category (week-by-week)
# ──────────────────────────────────────────────

ROADMAPS = {
    "data-engineering": [
        {"title": "SQL Fundamentals", "description": "SELECT, WHERE, ORDER BY, LIMIT, and basic filtering", "week_number": 1, "estimated_hours": 8, "order_index": 1},
        {"title": "Joins & Set Operations", "description": "INNER, LEFT, RIGHT, FULL joins, UNION, INTERSECT", "week_number": 2, "estimated_hours": 8, "order_index": 2},
        {"title": "Aggregations & Grouping", "description": "GROUP BY, HAVING, aggregate functions, ROLLUP", "week_number": 3, "estimated_hours": 6, "order_index": 3},
        {"title": "Subqueries & CTEs", "description": "Correlated subqueries, WITH clauses, recursive CTEs", "week_number": 4, "estimated_hours": 8, "order_index": 4},
        {"title": "Window Functions", "description": "ROW_NUMBER, RANK, LAG, LEAD, running totals, partitions", "week_number": 5, "estimated_hours": 10, "order_index": 5},
        {"title": "Data Modeling & Schema Design", "description": "Star schema, snowflake, normalization, slowly changing dimensions", "week_number": 6, "estimated_hours": 10, "order_index": 6},
        {"title": "ETL/ELT Pipelines", "description": "Extract-Transform-Load patterns, batch vs streaming, idempotency", "week_number": 7, "estimated_hours": 10, "order_index": 7},
        {"title": "Apache Spark Essentials", "description": "RDDs, DataFrames, transformations, actions, Spark SQL", "week_number": 8, "estimated_hours": 12, "order_index": 8},
        {"title": "Airflow & Orchestration", "description": "DAGs, operators, sensors, scheduling, monitoring", "week_number": 9, "estimated_hours": 8, "order_index": 9},
        {"title": "Performance Tuning & System Design", "description": "Indexing, partitioning, query optimization, data pipeline architecture", "week_number": 10, "estimated_hours": 12, "order_index": 10},
    ],
    "data-science": [
        {"title": "Python for Data Science", "description": "Python basics, data types, functions, list comprehensions", "week_number": 1, "estimated_hours": 8, "order_index": 1},
        {"title": "Pandas & NumPy Deep Dive", "description": "DataFrames, Series, indexing, vectorized operations", "week_number": 2, "estimated_hours": 10, "order_index": 2},
        {"title": "Descriptive Statistics", "description": "Mean, median, mode, variance, standard deviation, percentiles", "week_number": 3, "estimated_hours": 6, "order_index": 3},
        {"title": "Probability & Distributions", "description": "Bayes theorem, normal, binomial, Poisson distributions", "week_number": 4, "estimated_hours": 8, "order_index": 4},
        {"title": "Hypothesis Testing", "description": "t-tests, chi-squared, p-values, confidence intervals, power analysis", "week_number": 5, "estimated_hours": 8, "order_index": 5},
        {"title": "A/B Testing", "description": "Experiment design, sample size, significance, practical significance", "week_number": 6, "estimated_hours": 8, "order_index": 6},
        {"title": "Exploratory Data Analysis", "description": "Visualization, correlation, outlier detection, storytelling with data", "week_number": 7, "estimated_hours": 8, "order_index": 7},
        {"title": "Feature Engineering", "description": "Encoding, scaling, binning, interaction features, domain-driven features", "week_number": 8, "estimated_hours": 10, "order_index": 8},
        {"title": "Regression & Classification", "description": "Linear/logistic regression, evaluation metrics, cross-validation", "week_number": 9, "estimated_hours": 10, "order_index": 9},
        {"title": "Capstone: End-to-End DS Project", "description": "Full project: data collection, EDA, modeling, presentation", "week_number": 10, "estimated_hours": 12, "order_index": 10},
    ],
    "machine-learning": [
        {"title": "ML Landscape & Types", "description": "Supervised, unsupervised, reinforcement learning overview", "week_number": 1, "estimated_hours": 6, "order_index": 1},
        {"title": "Linear Models", "description": "Linear regression, logistic regression, regularization (L1/L2)", "week_number": 2, "estimated_hours": 8, "order_index": 2},
        {"title": "Tree-Based Models", "description": "Decision trees, random forests, gradient boosting (XGBoost, LightGBM)", "week_number": 3, "estimated_hours": 10, "order_index": 3},
        {"title": "SVM & Kernel Methods", "description": "Support vector machines, kernel trick, margin optimization", "week_number": 4, "estimated_hours": 8, "order_index": 4},
        {"title": "Unsupervised Learning", "description": "K-means, DBSCAN, hierarchical clustering, PCA, t-SNE", "week_number": 5, "estimated_hours": 8, "order_index": 5},
        {"title": "Neural Networks Foundations", "description": "Perceptrons, backpropagation, activation functions, optimizers", "week_number": 6, "estimated_hours": 10, "order_index": 6},
        {"title": "Deep Learning with PyTorch", "description": "Tensors, autograd, building CNNs and RNNs", "week_number": 7, "estimated_hours": 12, "order_index": 7},
        {"title": "Model Evaluation & Tuning", "description": "Cross-validation, hyperparameter tuning, bias-variance tradeoff", "week_number": 8, "estimated_hours": 8, "order_index": 8},
        {"title": "Feature Engineering for ML", "description": "Feature selection, importance, dimensionality reduction", "week_number": 9, "estimated_hours": 8, "order_index": 9},
        {"title": "ML System Design", "description": "End-to-end ML systems, serving, scaling, real-world challenges", "week_number": 10, "estimated_hours": 12, "order_index": 10},
    ],
    "data-analytics": [
        {"title": "SQL Essentials for Analysts", "description": "SELECT, JOINs, aggregations, subqueries for analytics", "week_number": 1, "estimated_hours": 8, "order_index": 1},
        {"title": "Excel & Spreadsheet Mastery", "description": "Pivot tables, VLOOKUP, conditional formatting, charts", "week_number": 2, "estimated_hours": 6, "order_index": 2},
        {"title": "Data Cleaning & Wrangling", "description": "Handling nulls, duplicates, formatting, data validation", "week_number": 3, "estimated_hours": 6, "order_index": 3},
        {"title": "Metrics & KPI Design", "description": "North star metrics, leading/lagging indicators, OKRs", "week_number": 4, "estimated_hours": 6, "order_index": 4},
        {"title": "Product Analytics", "description": "Funnels, retention, engagement, user segmentation, DAU/MAU", "week_number": 5, "estimated_hours": 8, "order_index": 5},
        {"title": "Cohort & Funnel Analysis", "description": "Building cohorts, conversion funnels, drop-off analysis", "week_number": 6, "estimated_hours": 8, "order_index": 6},
        {"title": "Dashboard Design & Visualization", "description": "Principles of good dashboards, chart selection, storytelling", "week_number": 7, "estimated_hours": 8, "order_index": 7},
        {"title": "Statistical Thinking for Analysts", "description": "Distributions, significance, correlation vs causation", "week_number": 8, "estimated_hours": 8, "order_index": 8},
    ],
    "mlops": [
        {"title": "ML Lifecycle Overview", "description": "From research to production, MLOps maturity levels", "week_number": 1, "estimated_hours": 6, "order_index": 1},
        {"title": "Experiment Tracking with MLflow", "description": "Logging parameters, metrics, artifacts, comparing runs", "week_number": 2, "estimated_hours": 8, "order_index": 2},
        {"title": "Model Versioning & Registry", "description": "Model versioning, staging, production promotion", "week_number": 3, "estimated_hours": 8, "order_index": 3},
        {"title": "Feature Stores", "description": "Feast, Tecton; online/offline features, point-in-time correctness", "week_number": 4, "estimated_hours": 8, "order_index": 4},
        {"title": "ML Pipelines", "description": "Kubeflow, Vertex AI Pipelines, orchestrating training workflows", "week_number": 5, "estimated_hours": 10, "order_index": 5},
        {"title": "Model Serving", "description": "REST/gRPC APIs, TensorFlow Serving, Triton, BentoML", "week_number": 6, "estimated_hours": 10, "order_index": 6},
        {"title": "Monitoring & Drift Detection", "description": "Data drift, model drift, performance monitoring, alerting", "week_number": 7, "estimated_hours": 10, "order_index": 7},
        {"title": "CI/CD for ML", "description": "Automated testing, model validation, deployment pipelines", "week_number": 8, "estimated_hours": 10, "order_index": 8},
    ],
    "devops-dataops": [
        {"title": "Linux & Shell Scripting", "description": "File system, permissions, bash scripting, cron", "week_number": 1, "estimated_hours": 8, "order_index": 1},
        {"title": "Git & Version Control", "description": "Branching, merging, rebasing, pull requests, Git flow", "week_number": 2, "estimated_hours": 6, "order_index": 2},
        {"title": "Docker Fundamentals", "description": "Images, containers, Dockerfile, docker-compose, networking", "week_number": 3, "estimated_hours": 8, "order_index": 3},
        {"title": "CI/CD Pipelines", "description": "GitHub Actions, Jenkins, GitLab CI, automated testing", "week_number": 4, "estimated_hours": 8, "order_index": 4},
        {"title": "Kubernetes Essentials", "description": "Pods, services, deployments, config maps, Helm charts", "week_number": 5, "estimated_hours": 12, "order_index": 5},
        {"title": "Infrastructure as Code", "description": "Terraform, CloudFormation, Pulumi, state management", "week_number": 6, "estimated_hours": 10, "order_index": 6},
        {"title": "Cloud Platforms (AWS/GCP/Azure)", "description": "Core services, IAM, networking, storage, compute", "week_number": 7, "estimated_hours": 12, "order_index": 7},
        {"title": "Monitoring & Observability", "description": "Prometheus, Grafana, ELK stack, distributed tracing", "week_number": 8, "estimated_hours": 8, "order_index": 8},
        {"title": "Data Orchestration & DataOps", "description": "Airflow, Prefect, dbt, data quality checks", "week_number": 9, "estimated_hours": 10, "order_index": 9},
    ],
    "generative-ai": [
        {"title": "LLM Fundamentals", "description": "Transformer architecture, attention mechanism, tokenization", "week_number": 1, "estimated_hours": 8, "order_index": 1},
        {"title": "Prompt Engineering", "description": "Zero-shot, few-shot, chain-of-thought, prompt templates", "week_number": 2, "estimated_hours": 6, "order_index": 2},
        {"title": "API Integration (OpenAI, HF)", "description": "Chat completions, embeddings, streaming, function calling", "week_number": 3, "estimated_hours": 8, "order_index": 3},
        {"title": "LangChain & Orchestration", "description": "Chains, agents, tools, memory, output parsers", "week_number": 4, "estimated_hours": 10, "order_index": 4},
        {"title": "RAG Pipeline", "description": "Document loading, chunking, embedding, retrieval, reranking", "week_number": 5, "estimated_hours": 10, "order_index": 5},
        {"title": "Vector Databases", "description": "Pinecone, Weaviate, ChromaDB, FAISS, similarity search", "week_number": 6, "estimated_hours": 8, "order_index": 6},
        {"title": "Fine-Tuning LLMs", "description": "LoRA, QLoRA, PEFT, training data preparation", "week_number": 7, "estimated_hours": 12, "order_index": 7},
        {"title": "Evaluation & Safety", "description": "LLM evaluation frameworks, hallucination detection, guardrails", "week_number": 8, "estimated_hours": 8, "order_index": 8},
        {"title": "Agents & Tool Use", "description": "Building autonomous agents, function calling, multi-step reasoning", "week_number": 9, "estimated_hours": 10, "order_index": 9},
        {"title": "Production Deployment", "description": "Scaling, caching, cost optimization, monitoring", "week_number": 10, "estimated_hours": 10, "order_index": 10},
    ],
    "business-intelligence": [
        {"title": "BI Concepts & Data Literacy", "description": "What is BI, data-driven decision making, BI stack", "week_number": 1, "estimated_hours": 4, "order_index": 1},
        {"title": "SQL for BI Analysts", "description": "Analytical queries, window functions, CTEs for reporting", "week_number": 2, "estimated_hours": 8, "order_index": 2},
        {"title": "Tableau Deep Dive", "description": "Worksheets, dashboards, calculated fields, LOD expressions", "week_number": 3, "estimated_hours": 10, "order_index": 3},
        {"title": "Power BI Essentials", "description": "Data modeling, DAX, Power Query, report design", "week_number": 4, "estimated_hours": 10, "order_index": 4},
        {"title": "Data Visualization Principles", "description": "Chart types, color theory, Gestalt principles, storytelling", "week_number": 5, "estimated_hours": 6, "order_index": 5},
        {"title": "KPI & Reporting Frameworks", "description": "OKRs, balanced scorecards, executive dashboards", "week_number": 6, "estimated_hours": 8, "order_index": 6},
        {"title": "Data Storytelling", "description": "Narrative structure, audience analysis, presenting insights", "week_number": 7, "estimated_hours": 6, "order_index": 7},
        {"title": "Advanced Analytics in BI", "description": "Forecasting, clustering in Tableau, R/Python integration", "week_number": 8, "estimated_hours": 10, "order_index": 8},
    ],
    "data-architecture": [
        {"title": "Relational Database Design", "description": "ER diagrams, tables, constraints, relationships", "week_number": 1, "estimated_hours": 8, "order_index": 1},
        {"title": "Normalization & Denormalization", "description": "1NF-3NF, BCNF, when to denormalize for performance", "week_number": 2, "estimated_hours": 6, "order_index": 2},
        {"title": "Data Warehouse Concepts", "description": "Kimball vs Inmon, ETL/ELT, staging areas", "week_number": 3, "estimated_hours": 8, "order_index": 3},
        {"title": "Dimensional Modeling", "description": "Star schema, snowflake schema, fact/dimension tables, SCDs", "week_number": 4, "estimated_hours": 10, "order_index": 4},
        {"title": "Data Lakes & Lakehouses", "description": "Delta Lake, Iceberg, Hudi, storage layers, metadata management", "week_number": 5, "estimated_hours": 10, "order_index": 5},
        {"title": "Data Mesh Principles", "description": "Domain ownership, self-serve platform, data products", "week_number": 6, "estimated_hours": 8, "order_index": 6},
        {"title": "Data Governance", "description": "Catalogs, lineage, quality, privacy, compliance", "week_number": 7, "estimated_hours": 8, "order_index": 7},
        {"title": "Streaming Architecture", "description": "Kafka, Kinesis, event sourcing, CQRS patterns", "week_number": 8, "estimated_hours": 10, "order_index": 8},
        {"title": "Cloud Data Platforms", "description": "Snowflake, BigQuery, Redshift architecture deep dives", "week_number": 9, "estimated_hours": 10, "order_index": 9},
    ],
    "nlp-computer-vision": [
        {"title": "Text Preprocessing", "description": "Tokenization, stemming, lemmatization, stop words, TF-IDF", "week_number": 1, "estimated_hours": 6, "order_index": 1},
        {"title": "Word Embeddings", "description": "Word2Vec, GloVe, FastText, embedding visualization", "week_number": 2, "estimated_hours": 8, "order_index": 2},
        {"title": "Sequence Models", "description": "RNNs, LSTMs, GRUs, sequence-to-sequence", "week_number": 3, "estimated_hours": 10, "order_index": 3},
        {"title": "Transformers & Attention", "description": "Self-attention, multi-head attention, positional encoding", "week_number": 4, "estimated_hours": 10, "order_index": 4},
        {"title": "Pre-trained Language Models", "description": "BERT, GPT, T5, transfer learning for NLP", "week_number": 5, "estimated_hours": 10, "order_index": 5},
        {"title": "CNN for Images", "description": "Convolutional layers, pooling, ResNet, VGG architectures", "week_number": 6, "estimated_hours": 10, "order_index": 6},
        {"title": "Object Detection", "description": "YOLO, Faster RCNN, SSD, anchor boxes, NMS", "week_number": 7, "estimated_hours": 12, "order_index": 7},
        {"title": "Segmentation & Generation", "description": "U-Net, Mask RCNN, GANs, diffusion models", "week_number": 8, "estimated_hours": 12, "order_index": 8},
        {"title": "Multimodal & Deployment", "description": "CLIP, vision-language models, ONNX, TensorRT optimization", "week_number": 9, "estimated_hours": 10, "order_index": 9},
    ],
}

# ──────────────────────────────────────────────
# 4. YOUTUBE RESOURCES per category
# ──────────────────────────────────────────────

RESOURCES = {
    "data-engineering": [
        {"title": "SQL Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY", "resource_type": "video", "estimated_duration_minutes": 260, "order_in_playlist": 1},
        {"title": "SQL Joins Explained - TechWithTim", "url": "https://www.youtube.com/watch?v=9yeOJ0ZMUYw", "resource_type": "video", "estimated_duration_minutes": 15, "order_in_playlist": 2},
        {"title": "Window Functions in SQL - DataWithZach", "url": "https://www.youtube.com/watch?v=Ww71knvhQ-s", "resource_type": "video", "estimated_duration_minutes": 45, "order_in_playlist": 3},
        {"title": "Data Modeling Explained", "url": "https://www.youtube.com/watch?v=--pKmQGODqM", "resource_type": "video", "estimated_duration_minutes": 20, "order_in_playlist": 4},
        {"title": "Apache Spark Full Course - Simplilearn", "url": "https://www.youtube.com/watch?v=GFC2gOL1p9k", "resource_type": "video", "estimated_duration_minutes": 330, "order_in_playlist": 5},
        {"title": "Apache Airflow Tutorial - DataEngineering", "url": "https://www.youtube.com/watch?v=K9AnJ9_ZAXE", "resource_type": "video", "estimated_duration_minutes": 60, "order_in_playlist": 6},
        {"title": "ETL vs ELT Explained", "url": "https://www.youtube.com/watch?v=oF_2J1YSQ3k", "resource_type": "video", "estimated_duration_minutes": 12, "order_in_playlist": 7},
    ],
    "data-science": [
        {"title": "Python for Data Science - freeCodeCamp", "url": "https://www.youtube.com/watch?v=LHBE6Q9XlzI", "resource_type": "video", "estimated_duration_minutes": 720, "order_in_playlist": 1},
        {"title": "Pandas Complete Tutorial - Corey Schafer", "url": "https://www.youtube.com/watch?v=ZyhVh-qRZPA", "resource_type": "video", "estimated_duration_minutes": 60, "order_in_playlist": 2},
        {"title": "Statistics for Data Science - Krish Naik", "url": "https://www.youtube.com/watch?v=LZzq1zSL1bs", "resource_type": "video", "estimated_duration_minutes": 120, "order_in_playlist": 3},
        {"title": "Hypothesis Testing Explained", "url": "https://www.youtube.com/watch?v=0oc49DyA3hU", "resource_type": "video", "estimated_duration_minutes": 20, "order_in_playlist": 4},
        {"title": "A/B Testing Tutorial - DataCamp", "url": "https://www.youtube.com/watch?v=sNMCAy2NS8o", "resource_type": "video", "estimated_duration_minutes": 30, "order_in_playlist": 5},
        {"title": "Feature Engineering - Kaggle", "url": "https://www.youtube.com/watch?v=68ABAU_V8qI", "resource_type": "video", "estimated_duration_minutes": 45, "order_in_playlist": 6},
    ],
    "machine-learning": [
        {"title": "Machine Learning Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=NWONeJKn6kc", "resource_type": "video", "estimated_duration_minutes": 540, "order_in_playlist": 1},
        {"title": "Linear Regression Explained - StatQuest", "url": "https://www.youtube.com/watch?v=nk2CQITm_eo", "resource_type": "video", "estimated_duration_minutes": 27, "order_in_playlist": 2},
        {"title": "Random Forest - StatQuest", "url": "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ", "resource_type": "video", "estimated_duration_minutes": 10, "order_in_playlist": 3},
        {"title": "XGBoost Tutorial - Krish Naik", "url": "https://www.youtube.com/watch?v=OtD8wVaFm6E", "resource_type": "video", "estimated_duration_minutes": 30, "order_in_playlist": 4},
        {"title": "Neural Networks from Scratch - 3Blue1Brown", "url": "https://www.youtube.com/watch?v=aircAruvnKk", "resource_type": "video", "estimated_duration_minutes": 19, "order_in_playlist": 5},
        {"title": "Deep Learning with PyTorch - Full Course", "url": "https://www.youtube.com/watch?v=c36lUUr864M", "resource_type": "video", "estimated_duration_minutes": 600, "order_in_playlist": 6},
    ],
    "data-analytics": [
        {"title": "SQL for Data Analysts - Alex The Analyst", "url": "https://www.youtube.com/watch?v=7mz73uXD9DA", "resource_type": "video", "estimated_duration_minutes": 60, "order_in_playlist": 1},
        {"title": "Excel Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=Vl0H-qTclOg", "resource_type": "video", "estimated_duration_minutes": 240, "order_in_playlist": 2},
        {"title": "Product Analytics Explained", "url": "https://www.youtube.com/watch?v=oeY3jK8dYqY", "resource_type": "video", "estimated_duration_minutes": 18, "order_in_playlist": 3},
        {"title": "Cohort Analysis Tutorial", "url": "https://www.youtube.com/watch?v=JZcYeaLZmCQ", "resource_type": "video", "estimated_duration_minutes": 20, "order_in_playlist": 4},
        {"title": "Dashboard Design Best Practices", "url": "https://www.youtube.com/watch?v=cDMFiYL26xI", "resource_type": "video", "estimated_duration_minutes": 15, "order_in_playlist": 5},
    ],
    "mlops": [
        {"title": "MLOps Explained - DataTalksClub", "url": "https://www.youtube.com/watch?v=s0uaFZSzwfI", "resource_type": "video", "estimated_duration_minutes": 15, "order_in_playlist": 1},
        {"title": "MLflow Tutorial - Full Course", "url": "https://www.youtube.com/watch?v=qdcHHrsXA48", "resource_type": "video", "estimated_duration_minutes": 90, "order_in_playlist": 2},
        {"title": "Feature Stores Explained", "url": "https://www.youtube.com/watch?v=DESBDwqoBUo", "resource_type": "video", "estimated_duration_minutes": 20, "order_in_playlist": 3},
        {"title": "Kubeflow Pipelines Tutorial", "url": "https://www.youtube.com/watch?v=6wWdNg0GMV4", "resource_type": "video", "estimated_duration_minutes": 45, "order_in_playlist": 4},
        {"title": "Model Serving with BentoML", "url": "https://www.youtube.com/watch?v=bIjS6kgpfpg", "resource_type": "video", "estimated_duration_minutes": 30, "order_in_playlist": 5},
        {"title": "ML Monitoring - Evidently AI", "url": "https://www.youtube.com/watch?v=IjNPyJmtcOo", "resource_type": "video", "estimated_duration_minutes": 25, "order_in_playlist": 6},
    ],
    "devops-dataops": [
        {"title": "Linux Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=sWbUDq4S6Y8", "resource_type": "video", "estimated_duration_minutes": 300, "order_in_playlist": 1},
        {"title": "Git & GitHub Crash Course", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "resource_type": "video", "estimated_duration_minutes": 60, "order_in_playlist": 2},
        {"title": "Docker Tutorial - TechWorld with Nana", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "resource_type": "video", "estimated_duration_minutes": 180, "order_in_playlist": 3},
        {"title": "Kubernetes Tutorial - TechWorld with Nana", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "resource_type": "video", "estimated_duration_minutes": 240, "order_in_playlist": 4},
        {"title": "Terraform Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=SLB_c_ayRMo", "resource_type": "video", "estimated_duration_minutes": 150, "order_in_playlist": 5},
        {"title": "GitHub Actions CI/CD Tutorial", "url": "https://www.youtube.com/watch?v=R8_veQiYBjI", "resource_type": "video", "estimated_duration_minutes": 60, "order_in_playlist": 6},
    ],
    "generative-ai": [
        {"title": "Transformers Explained - 3Blue1Brown", "url": "https://www.youtube.com/watch?v=wjZofJX0v4M", "resource_type": "video", "estimated_duration_minutes": 27, "order_in_playlist": 1},
        {"title": "Prompt Engineering Guide - DAIR.AI", "url": "https://www.youtube.com/watch?v=dOxUroR57xs", "resource_type": "video", "estimated_duration_minutes": 45, "order_in_playlist": 2},
        {"title": "LangChain Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=lG7Uxts9SXs", "resource_type": "video", "estimated_duration_minutes": 180, "order_in_playlist": 3},
        {"title": "RAG Tutorial - Full Implementation", "url": "https://www.youtube.com/watch?v=tcqEUSNCn8I", "resource_type": "video", "estimated_duration_minutes": 90, "order_in_playlist": 4},
        {"title": "Vector Databases Explained", "url": "https://www.youtube.com/watch?v=klTvEwg3oJ4", "resource_type": "video", "estimated_duration_minutes": 20, "order_in_playlist": 5},
        {"title": "Fine-Tuning LLMs with LoRA", "url": "https://www.youtube.com/watch?v=YVU5wAA6Txo", "resource_type": "video", "estimated_duration_minutes": 60, "order_in_playlist": 6},
        {"title": "Building AI Agents - Full Tutorial", "url": "https://www.youtube.com/watch?v=sal78ACtGTc", "resource_type": "video", "estimated_duration_minutes": 120, "order_in_playlist": 7},
    ],
    "business-intelligence": [
        {"title": "Tableau Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=aHaOIvR00So", "resource_type": "video", "estimated_duration_minutes": 360, "order_in_playlist": 1},
        {"title": "Power BI Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=3u7MQz1EyPY", "resource_type": "video", "estimated_duration_minutes": 240, "order_in_playlist": 2},
        {"title": "Data Visualization Best Practices", "url": "https://www.youtube.com/watch?v=5Zg-C8AAIGg", "resource_type": "video", "estimated_duration_minutes": 25, "order_in_playlist": 3},
        {"title": "DAX Tutorial for Power BI", "url": "https://www.youtube.com/watch?v=iW2bEhO4UPA", "resource_type": "video", "estimated_duration_minutes": 60, "order_in_playlist": 4},
        {"title": "Data Storytelling Masterclass", "url": "https://www.youtube.com/watch?v=r5_34YnCmMY", "resource_type": "video", "estimated_duration_minutes": 30, "order_in_playlist": 5},
    ],
    "data-architecture": [
        {"title": "Database Design Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=ztHopE5Wnpc", "resource_type": "video", "estimated_duration_minutes": 480, "order_in_playlist": 1},
        {"title": "Data Warehousing Explained", "url": "https://www.youtube.com/watch?v=AHR_7jFCMeY", "resource_type": "video", "estimated_duration_minutes": 30, "order_in_playlist": 2},
        {"title": "Dimensional Modeling Tutorial", "url": "https://www.youtube.com/watch?v=lWPiSZf7-uQ", "resource_type": "video", "estimated_duration_minutes": 45, "order_in_playlist": 3},
        {"title": "Data Lakehouse Architecture", "url": "https://www.youtube.com/watch?v=RJCemCDmYQE", "resource_type": "video", "estimated_duration_minutes": 25, "order_in_playlist": 4},
        {"title": "Data Mesh Explained - Zhamak Dehghani", "url": "https://www.youtube.com/watch?v=_bmYXWCxF_Q", "resource_type": "video", "estimated_duration_minutes": 60, "order_in_playlist": 5},
        {"title": "Apache Kafka Full Tutorial", "url": "https://www.youtube.com/watch?v=CU44hKLMg7k", "resource_type": "video", "estimated_duration_minutes": 90, "order_in_playlist": 6},
    ],
    "nlp-computer-vision": [
        {"title": "NLP Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=fNxaJsNG3-s", "resource_type": "video", "estimated_duration_minutes": 360, "order_in_playlist": 1},
        {"title": "Word Embeddings Explained - StatQuest", "url": "https://www.youtube.com/watch?v=viZrOnJclY0", "resource_type": "video", "estimated_duration_minutes": 15, "order_in_playlist": 2},
        {"title": "Attention Is All You Need - Explained", "url": "https://www.youtube.com/watch?v=iDulhoQ2pro", "resource_type": "video", "estimated_duration_minutes": 25, "order_in_playlist": 3},
        {"title": "BERT Explained", "url": "https://www.youtube.com/watch?v=xI0HHN5XKDo", "resource_type": "video", "estimated_duration_minutes": 20, "order_in_playlist": 4},
        {"title": "CNN for Image Classification - Sentdex", "url": "https://www.youtube.com/watch?v=WvoLTXIjBYU", "resource_type": "video", "estimated_duration_minutes": 45, "order_in_playlist": 5},
        {"title": "YOLO Object Detection Tutorial", "url": "https://www.youtube.com/watch?v=WgPbbWmnXJ8", "resource_type": "video", "estimated_duration_minutes": 30, "order_in_playlist": 6},
    ],
}

# ──────────────────────────────────────────────
# 5. SAMPLE QUESTIONS per category (5-8 each)
# ──────────────────────────────────────────────

SAMPLE_QUESTIONS = {
    "data-engineering": [
        {"title": "Find Duplicate Emails", "description": "Write a SQL query to find all duplicate email addresses in the 'users' table.", "question_type": "sql", "difficulty": "easy"},
        {"title": "Second Highest Salary", "description": "Write a SQL query to get the second highest salary from the 'employees' table.", "question_type": "sql", "difficulty": "easy"},
        {"title": "Running Total of Orders", "description": "Using window functions, calculate the running total of order amounts partitioned by customer_id, ordered by order_date.", "question_type": "sql", "difficulty": "medium"},
        {"title": "Consecutive Login Days", "description": "Find users who logged in for 3 or more consecutive days. Use the 'logins' table with columns user_id, login_date.", "question_type": "sql", "difficulty": "medium"},
        {"title": "Pivot Monthly Revenue", "description": "Transform monthly revenue data from rows into columns (Jan through Dec) for each product category.", "question_type": "sql", "difficulty": "hard"},
        {"title": "Design a Star Schema", "description": "Given an e-commerce platform, design a star schema with a fact table for orders and appropriate dimension tables. Explain your design choices.", "question_type": "case_study", "difficulty": "hard"},
    ],
    "data-science": [
        {"title": "Calculate Mean & Median", "description": "Given a list of numbers, write Python code to calculate the mean, median, and mode without using external libraries.", "question_type": "python", "difficulty": "easy"},
        {"title": "Explain P-Value", "description": "A marketing team ran an A/B test. Group A (control) had 500 users with 50 conversions. Group B (variant) had 500 users with 65 conversions. Calculate the p-value and state your conclusion at alpha=0.05.", "question_type": "case_study", "difficulty": "medium"},
        {"title": "Feature Scaling Impact", "description": "Explain when and why you would use StandardScaler vs MinMaxScaler. Give a concrete example where choosing the wrong scaler would hurt model performance.", "question_type": "mcq", "difficulty": "medium"},
        {"title": "Handle Missing Data", "description": "Write Python/pandas code to handle missing values in a dataset with a mix of numerical and categorical columns. Explain your imputation strategy.", "question_type": "python", "difficulty": "medium"},
        {"title": "Sample Size Calculation", "description": "Your product team wants to run an A/B test. The baseline conversion rate is 5%, and they want to detect a 1% increase. Calculate the required sample size per group (power=0.8, alpha=0.05).", "question_type": "case_study", "difficulty": "hard"},
    ],
    "machine-learning": [
        {"title": "Bias-Variance Tradeoff", "description": "Explain the bias-variance tradeoff. Your model has high training accuracy (99%) but low test accuracy (70%). Diagnose the problem and suggest 3 concrete solutions.", "question_type": "mcq", "difficulty": "easy"},
        {"title": "Implement K-Means", "description": "Implement the K-Means clustering algorithm from scratch in Python. Include initialization, assignment, and update steps.", "question_type": "python", "difficulty": "medium"},
        {"title": "ROC vs PR Curve", "description": "You have an imbalanced dataset (95% negative, 5% positive). Explain why Precision-Recall curve is more informative than ROC curve in this case.", "question_type": "mcq", "difficulty": "medium"},
        {"title": "Build a Gradient Boosted Model", "description": "Using scikit-learn, build a GradientBoostingClassifier for a binary classification task. Include hyperparameter tuning with GridSearchCV.", "question_type": "python", "difficulty": "medium"},
        {"title": "Design a Recommendation System", "description": "Design an ML system for recommending products to users on an e-commerce platform. Discuss collaborative filtering vs content-based approaches, cold start, and evaluation.", "question_type": "case_study", "difficulty": "hard"},
    ],
    "data-analytics": [
        {"title": "Revenue by Region", "description": "Write a SQL query to calculate total revenue, order count, and average order value by region for Q4 2024.", "question_type": "sql", "difficulty": "easy"},
        {"title": "Month-over-Month Growth", "description": "Write a SQL query to calculate the month-over-month revenue growth rate for each product category.", "question_type": "sql", "difficulty": "medium"},
        {"title": "Funnel Drop-off Analysis", "description": "Given a user funnel (visit -> signup -> add_to_cart -> purchase), write SQL to calculate the conversion rate at each step and identify the biggest drop-off.", "question_type": "sql", "difficulty": "medium"},
        {"title": "Cohort Retention Table", "description": "Build a cohort retention analysis. Group users by their signup month and calculate D7, D14, D30 retention rates.", "question_type": "sql", "difficulty": "hard"},
        {"title": "Define Success Metrics", "description": "Your company launches a new mobile feature. Define 3 success metrics (north star, leading indicator, guardrail) and explain how you would measure each.", "question_type": "case_study", "difficulty": "medium"},
    ],
    "mlops": [
        {"title": "MLflow Experiment Setup", "description": "Write Python code to set up an MLflow experiment, log hyperparameters, metrics, and a trained model artifact.", "question_type": "python", "difficulty": "easy"},
        {"title": "Docker for ML", "description": "Write a Dockerfile for a FastAPI model serving application that loads a scikit-learn model and exposes a /predict endpoint.", "question_type": "case_study", "difficulty": "medium"},
        {"title": "Data Drift Detection", "description": "Explain 3 methods for detecting data drift in production ML systems. Write Python code to implement one using the KS test.", "question_type": "python", "difficulty": "medium"},
        {"title": "CI/CD Pipeline for ML", "description": "Design a CI/CD pipeline for an ML model that includes data validation, training, evaluation, and deployment gates.", "question_type": "case_study", "difficulty": "hard"},
        {"title": "A/B Testing an ML Model", "description": "Describe how you would A/B test a new recommendation model against the current production model. Include traffic splitting, metrics, and rollback criteria.", "question_type": "case_study", "difficulty": "hard"},
    ],
    "devops-dataops": [
        {"title": "Dockerfile Optimization", "description": "Given a Dockerfile that takes 10 minutes to build, identify 5 optimization techniques to reduce build time and image size.", "question_type": "case_study", "difficulty": "easy"},
        {"title": "Shell Script for Log Analysis", "description": "Write a bash script that parses an nginx access log, counts unique IPs, and finds the top 10 most-requested URLs.", "question_type": "python", "difficulty": "medium"},
        {"title": "Kubernetes Deployment", "description": "Write a Kubernetes deployment YAML for a web app with 3 replicas, health checks, resource limits, and a horizontal pod autoscaler.", "question_type": "case_study", "difficulty": "medium"},
        {"title": "Terraform State Management", "description": "Explain Terraform state management. What problems can arise with shared state? How do you set up remote state with locking?", "question_type": "case_study", "difficulty": "hard"},
        {"title": "Incident Response", "description": "Your production database CPU is at 100%. Walk through your debugging process step by step, from alerting to resolution.", "question_type": "case_study", "difficulty": "hard"},
    ],
    "generative-ai": [
        {"title": "Prompt Engineering Techniques", "description": "Given a customer support use case, write 3 different prompt templates using zero-shot, few-shot, and chain-of-thought approaches. Compare their outputs.", "question_type": "case_study", "difficulty": "easy"},
        {"title": "Build a RAG Pipeline", "description": "Write Python code to implement a basic RAG pipeline using LangChain: load a PDF, chunk it, create embeddings, store in a vector DB, and answer questions.", "question_type": "python", "difficulty": "medium"},
        {"title": "Token Counting & Cost", "description": "Estimate the cost of processing 1000 customer support tickets with GPT-4. Average ticket length is 200 words. Include input and output tokens.", "question_type": "mcq", "difficulty": "easy"},
        {"title": "Evaluate RAG Quality", "description": "Design an evaluation framework for a RAG-based Q&A system. Include metrics for retrieval quality, answer relevance, and faithfulness.", "question_type": "case_study", "difficulty": "hard"},
        {"title": "Fine-Tune vs RAG Decision", "description": "Your team needs to build a domain-specific chatbot. Compare fine-tuning vs RAG approaches across 5 dimensions: cost, latency, accuracy, maintenance, and data requirements.", "question_type": "case_study", "difficulty": "hard"},
    ],
    "business-intelligence": [
        {"title": "SQL for Executive Dashboard", "description": "Write SQL queries to power an executive dashboard showing YTD revenue, QoQ growth, top 5 products, and regional breakdown.", "question_type": "sql", "difficulty": "medium"},
        {"title": "Choose the Right Chart", "description": "For each of these scenarios, select the most appropriate chart type and explain why: (a) revenue trend over 12 months, (b) market share of 5 competitors, (c) correlation between price and sales.", "question_type": "mcq", "difficulty": "easy"},
        {"title": "DAX Calculated Measure", "description": "Write a DAX measure that calculates the year-over-year growth rate, handling cases where the prior year had zero revenue.", "question_type": "case_study", "difficulty": "medium"},
        {"title": "Dashboard Critique", "description": "Review a dashboard with 15 charts, 3 different color schemes, and no clear hierarchy. List 5 specific improvements based on data visualization best practices.", "question_type": "case_study", "difficulty": "medium"},
        {"title": "Self-Service BI Strategy", "description": "Design a self-service BI strategy for a 500-person company. Address data governance, tool selection, training, and data modeling standards.", "question_type": "case_study", "difficulty": "hard"},
    ],
    "data-architecture": [
        {"title": "Normalize to 3NF", "description": "Given a flat table with customer orders (customer_name, address, product, price, order_date), normalize it to 3NF. Show each normal form step.", "question_type": "case_study", "difficulty": "easy"},
        {"title": "Star vs Snowflake Schema", "description": "Compare star and snowflake schemas for an online retail store. When would you choose one over the other? Provide DDL for your chosen approach.", "question_type": "sql", "difficulty": "medium"},
        {"title": "Design a Data Lake", "description": "Design a three-layer data lake (raw, cleansed, curated) for a healthcare company. Address partitioning, file formats, and access patterns.", "question_type": "case_study", "difficulty": "hard"},
        {"title": "SCD Type 2 Implementation", "description": "Write SQL to implement a Slowly Changing Dimension Type 2 for a customer dimension table. Handle inserts, updates, and the effective date range.", "question_type": "sql", "difficulty": "hard"},
        {"title": "Data Mesh Domain Design", "description": "A company has 4 business units. Design a data mesh architecture defining domain boundaries, data products, and a self-serve platform.", "question_type": "case_study", "difficulty": "hard"},
    ],
    "nlp-computer-vision": [
        {"title": "Text Preprocessing Pipeline", "description": "Write Python code for a complete NLP preprocessing pipeline: tokenization, lowercasing, stop word removal, lemmatization, and TF-IDF vectorization.", "question_type": "python", "difficulty": "easy"},
        {"title": "Sentiment Analysis with BERT", "description": "Fine-tune a pre-trained BERT model for binary sentiment classification on movie reviews. Include data loading, training loop, and evaluation.", "question_type": "python", "difficulty": "medium"},
        {"title": "Image Classification CNN", "description": "Build a CNN in PyTorch for classifying images into 10 categories. Include conv layers, pooling, dropout, and training with data augmentation.", "question_type": "python", "difficulty": "medium"},
        {"title": "Attention Mechanism", "description": "Implement a simplified self-attention mechanism from scratch in Python. Show how queries, keys, and values are computed and combined.", "question_type": "python", "difficulty": "hard"},
        {"title": "Object Detection Pipeline", "description": "Design an end-to-end object detection pipeline for a retail store that counts products on shelves. Discuss model choice, training data, and deployment.", "question_type": "case_study", "difficulty": "hard"},
    ],
}

COMPANIES = [
    {"company_name": "Google", "industry": "Technology"},
    {"company_name": "Amazon", "industry": "E-commerce / Cloud"},
    {"company_name": "Meta", "industry": "Social Media"},
    {"company_name": "Apple", "industry": "Technology"},
    {"company_name": "Netflix", "industry": "Streaming"},
    {"company_name": "Microsoft", "industry": "Technology"},
    {"company_name": "Uber", "industry": "Transportation"},
    {"company_name": "Stripe", "industry": "Fintech"},
    {"company_name": "Spotify", "industry": "Music / Streaming"},
    {"company_name": "Airbnb", "industry": "Travel / Hospitality"},
    {"company_name": "LinkedIn", "industry": "Social / Professional"},
    {"company_name": "Databricks", "industry": "Data / AI"},
    {"company_name": "Snowflake", "industry": "Data / Cloud"},
]


# ──────────────────────────────────────────────
# SEED FUNCTION
# ──────────────────────────────────────────────

async def seed_database(db: AsyncSession):
    existing = await db.execute(select(Category).limit(1))
    if existing.scalar_one_or_none():
        return

    # 1. Categories
    cat_map: dict[str, Category] = {}
    for cat_data in CATEGORIES:
        cat = Category(**cat_data)
        db.add(cat)
        cat_map[cat_data["slug"]] = cat
    await db.flush()

    # 2. Topics
    topic_first_map: dict[str, Topic] = {}
    for slug, topic_list in TOPICS.items():
        cat = cat_map[slug]
        first_topic = None
        for topic_data in topic_list:
            topic = Topic(category_id=cat.id, **topic_data)
            db.add(topic)
            if first_topic is None:
                first_topic = topic
        if first_topic:
            topic_first_map[slug] = first_topic
    await db.flush()

    # 3. Roadmap items
    roadmap_map: dict[str, list[RoadmapItem]] = {}
    for slug, roadmap_list in ROADMAPS.items():
        cat = cat_map[slug]
        items = []
        for rm_data in roadmap_list:
            rm = RoadmapItem(category_id=cat.id, **rm_data)
            db.add(rm)
            items.append(rm)
        roadmap_map[slug] = items
    await db.flush()

    # 4. Learning resources (YouTube videos)
    for slug, res_list in RESOURCES.items():
        cat = cat_map[slug]
        rm_items = roadmap_map.get(slug, [])
        for i, res_data in enumerate(res_list):
            rm_item_id = rm_items[i].id if i < len(rm_items) else None
            resource = LearningResource(
                category_id=cat.id,
                roadmap_item_id=rm_item_id,
                **res_data,
            )
            db.add(resource)

    # 5. Companies
    for company_data in COMPANIES:
        company = CompanyTag(**company_data)
        db.add(company)

    # 6. Admin user
    admin = User(
        username="admin",
        email="admin@datagridle.com",
        password_hash=hash_password("admin123"),
        role=UserRole.ADMIN,
        is_verified=True,
    )
    db.add(admin)
    await db.flush()

    # 7. Sample questions (using admin as creator)
    for slug, q_list in SAMPLE_QUESTIONS.items():
        cat = cat_map[slug]
        first_topic = topic_first_map.get(slug)
        if not first_topic:
            continue
        for q_data in q_list:
            q = Question(
                category_id=cat.id,
                topic_id=first_topic.id,
                creator_id=admin.id,
                title=q_data["title"],
                description=q_data["description"],
                question_type=q_data["question_type"],
                difficulty=q_data["difficulty"],
                status="approved",
            )
            db.add(q)

    await db.commit()
