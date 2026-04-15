# Smart Finance Agent
## DeepAgents-based Multi-Agent Team for Personalized Budget Analysis

### GitHub Repository
- Project URL: https://github.com/kimiyeon/smart-finance-agent

---

## 1. Project Overview

This project implements a **special-purpose multi-agent team** using **DeepAgents** to solve a personalized finance problem.

The goal of the system is to analyze a user’s spending records and generate a smart financial report through collaboration among multiple specialized agents.

Instead of using one general agent, this project builds an **agent team** in which each sub-agent is responsible for a different reasoning stage:
- transaction classification
- spending analysis
- budget comparison
- final report generation

This project was designed to satisfy the assignment requirement of building a **multi-agent system with at least three sub-agents** and a **multi-step reasoning process** for a user-specific goal.

---

## 2. Problem Definition

Many household finance applications still require users to manually read, categorize, and interpret their transactions.  
This causes two main problems:

1. **Manual burden**: Users must classify transactions themselves.
2. **Weak interpretation**: Even if transaction data exists, extracting useful insights and actionable recommendations is difficult.

A single AI agent can answer general questions, but for a structured finance task, it is often better to divide the work across specialized agents.  
Therefore, this project uses a multi-agent architecture to automate financial reasoning step by step.

---

## 3. Project Goal

The system aims to achieve the following objectives:

- Automatically classify raw transaction text
- Calculate category-wise spending
- Compare actual spending to predefined budget limits
- Detect possible overspending
- Generate personalized financial recommendations
- Produce a final easy-to-read finance report

---

## 4. Why DeepAgents?

This project uses **DeepAgents**, a Python library designed for building agent systems with:
- a supervisor-based control structure
- sub-agent delegation
- tool usage
- planning-oriented execution

DeepAgents is suitable for this project because the finance task is not a one-step question-answering problem.  
The system must perform several connected reasoning stages before generating the final answer.

This makes it a good example of **multi-step logical reasoning**.

---

## 5. Why This Is a Multi-Agent Problem

This project is not a simple script that calculates totals.  
It is designed as an **agent team**, where each sub-agent has a specific professional role.

### Agent Roles

#### 1) Classifier Agent
- Reads raw spending text
- Determines the category of each transaction
- Example categories: food, transport, shopping, other

#### 2) Analyst Agent
- Calculates category-level totals
- Identifies major spending patterns
- Determines which types of spending are dominant

#### 3) Budget Planner Agent
- Compares category totals with monthly budget limits
- Detects whether spending is within budget or over budget
- Produces savings-oriented suggestions

#### 4) Report Writer Agent
- Collects outputs from previous agents
- Synthesizes them into one final report
- Presents the result in a user-friendly format

#### 5) Supervisor Agent
- Orchestrates the full workflow
- Delegates tasks to the correct sub-agent
- Combines intermediate results into the final answer

---

## 6. Multi-Step Reasoning Process

The final financial report cannot be generated directly from raw transaction strings.  
The system must follow a sequence of reasoning steps:

### Step 1. Transaction Understanding
The system receives raw user transaction text such as:
- 스타벅스 5000원
- 지하철 1250원
- 쿠팡 쇼핑 32000원
- 배달의민족 18000원

### Step 2. Category Classification
The Classifier Agent determines what each transaction means and maps it into a semantic category.

### Step 3. Category Aggregation
The Analyst Agent computes total spending per category.

### Step 4. Budget Evaluation
The Budget Planner Agent compares actual spending with a predefined budget table.

### Step 5. Recommendation Generation
The system derives actionable advice, such as reducing shopping or food delivery expenses.

### Step 6. Report Synthesis
The Report Writer Agent generates the final report for the user.

This sequential decision-making process demonstrates **multi-stage logical reasoning** rather than a single direct response.

---

## 7. System Architecture

```text
User Input
   ↓
Supervisor Agent
   ├── Classifier Agent
   ├── Analyst Agent
   ├── Budget Planner Agent
   └── Report Writer Agent
   ↓
Final Personalized Finance Report