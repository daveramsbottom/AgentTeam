# How to Set Dynamic Project Goals for AgentIan

## 🎯 **Problem Solved:**
The project goal was hardcoded in `main.py` as "Build a modern web application for task management...". 

Now AgentIan **dynamically pulls project goals from Jira** so you can use the same AgentTeam for **multiple different projects**.

## 🚀 **How to Set Project Goals:**

### **Method 1: Command Line (Easiest)**
```bash
python3 main.py --set-goal "Build a mobile expense tracking app with receipt scanning"
```

### **Method 2: Directly in Jira (Recommended)**
1. Go to your Jira project: `https://daveramsbottom.atlassian.net/browse/SCRUM`
2. Click **Project Settings** → **Details**
3. Edit the **Description** field with your project goal
4. Save changes

### **Method 3: Via API (Advanced)**
```python
from jira.client import JiraClient

client = JiraClient(base_url, username, token)
client.update_project_goal("SCRUM", "Build a fitness tracking mobile app")
```

## 🔍 **How It Works:**

### **Goal Priority (AgentIan checks in this order):**
1. **Jira Project Description** (if > 20 characters) ← **Primary source**
2. **Project Name** (as fallback: "Work on the ProjectName project")
3. **Generic fallback** ("Manage tasks for PROJECT_KEY")

### **Enhanced Workflow:**
```python
# Before (Hardcoded):
project_goal = test_goals[0]  # Always same goal

# After (Dynamic):
project_goal = agent_ian.jira_client.get_project_goal(project_key)
```

## 📋 **Example Project Goals:**

### **Mobile Apps:**
```
Build a fitness tracking mobile app with workout logging, progress charts, and social sharing features
```

### **E-commerce:**
```
Create an online marketplace for handmade crafts with seller profiles, payment processing, and review system
```

### **SaaS Applications:**
```
Develop a customer relationship management (CRM) platform with lead tracking, email automation, and reporting dashboards
```

### **APIs:**
```
Build a RESTful API for weather data aggregation with real-time updates, historical data, and location-based forecasting
```

## 🎯 **Benefits:**

### **✅ Multi-Project Support:**
- Use same AgentTeam setup for different projects
- Switch between projects by changing Jira project key
- Each project gets context-aware questions and stories

### **✅ Team Collaboration:**
- Project managers set goals in Jira (where they live)
- AgentIan automatically adapts to new goals
- No code changes needed for new projects

### **✅ Context-Aware Intelligence:**
- Different project types get different questions
- Stories generated match the actual project goal
- No more generic "user registration" for every project

## 🧪 **Testing Different Goals:**

### **Test 1: Basic App**
```bash
python3 main.py --set-goal "Create a simple calculator app for basic math operations"
```
**Expected:** Minimal questions, simple functionality stories

### **Test 2: E-commerce**
```bash
python3 main.py --set-goal "Build an online bookstore with shopping cart and payment processing"
```
**Expected:** Questions about products, payments, catalog stories

### **Test 3: API Service**
```bash
python3 main.py --set-goal "Develop a REST API for task management with user authentication"
```
**Expected:** Questions about endpoints, authentication stories

## 🔄 **Multi-Project Workflow:**

### **Project A: E-commerce**
1. Set project key to `ECOM` in `.env`
2. Set goal: "Build online electronics store"
3. Run AgentIan → Gets e-commerce specific stories

### **Project B: Mobile App**
1. Set project key to `MOBILE` in `.env`  
2. Set goal: "Create fitness tracking app"
3. Run AgentIan → Gets mobile app specific stories

### **Project C: API Service**
1. Set project key to `API` in `.env`
2. Set goal: "Build payment processing API"
3. Run AgentIan → Gets API specific stories

## 📊 **Current Status:**
- ✅ Dynamic goal extraction from Jira working
- ✅ Command-line goal setting working
- ✅ Context-aware story generation working
- ✅ Multi-project support enabled
- ✅ Fallback handling for missing goals

AgentIan is now **truly flexible** and can work with any project type by adapting to the goals you set in Jira!