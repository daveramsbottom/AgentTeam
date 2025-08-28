# How to Set Dynamic Project Goals for AgentIan

## 🎯 **Problem Solved:**
The project goal was hardcoded in `main.py` as "Build a modern web application for task management...". 

Now AgentIan **dynamically pulls project goals from Jira** so you can use the same AgentTeam for **multiple different projects**.

## 🚀 **How to Set Project Goals:**

### **Method 1: Command Line (Easiest)**
```bash
python3 main.py --set-goal "Build a mobile expense tracking app with receipt scanning"
```
*This creates/updates a "🎯 Project Goal" Epic in your Jira project*

### **Method 2: Directly in Jira (Recommended)**
1. Go to your Jira project: `https://daveramsbottom.atlassian.net/browse/SCRUM`
2. **Create New Epic** or **find existing "🎯 Project Goal" Epic**
3. **Summary**: "🎯 Project Goal" (or similar)
4. **Description**: Enter your detailed project goal
5. Save the Epic

### **Method 3: Manual Epic Creation**
1. **Create Epic** → **Summary**: "Project Goal"
2. **Description**: Your detailed project objective
3. Epic will be **visible in backlog and reports**
4. **Team can easily find and reference** project goals

### **Method 4: Via API (Advanced)**
```python
from jira.client import JiraClient

client = JiraClient(base_url, username, token)
client.update_project_goal("SCRUM", "Build a fitness tracking mobile app")
```

## 🔍 **How It Works:**

### **Goal Priority (AgentIan checks in this order):**
1. **"🎯 Project Goal" Epic Description** ← **Primary source (NEW!)**
2. **Any Epic with "Project Goal" in summary** 
3. **Jira Project Description** (legacy fallback)
4. **Project Name** (as fallback: "Work on the ProjectName project")
5. **Generic fallback** ("Manage tasks for PROJECT_KEY")

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

### **✅ Epic-Based Visibility:**
- **Highly visible** in Jira backlog and boards
- **Team accessible** - everyone can see and edit project goals
- **Rich formatting** - supports full Jira description formatting
- **Tracking friendly** - appears in reports and dashboards

### **✅ Multi-Project Support:**
- Use same AgentTeam setup for different projects
- Switch between projects by changing Jira project key
- Each project gets context-aware questions and stories

### **✅ Team Collaboration:**
- Project managers set goals in visible Epics (not hidden project settings)
- AgentIan automatically adapts to new goals
- No code changes needed for new projects
- **Easy for team members to find and reference**

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
- ✅ **Epic-based goal extraction** - NEW! Prioritizes visible Epics
- ✅ **Command-line Epic creation** - Creates "🎯 Project Goal" Epics
- ✅ **Legacy fallback support** - Still works with project descriptions
- ✅ **Dynamic goal extraction** from multiple sources working
- ✅ **Context-aware story generation** working
- ✅ **Multi-project support** enabled
- ✅ **Team-visible project goals** in backlog and reports

## 🎉 **What's New:**
- **Epic-based project goals** are now the primary method
- **Much more visible** to team members in Jira interface
- **Better team collaboration** - everyone can see and edit goals
- **Automatic Epic creation** via `--set-goal` command
- **Backward compatible** - existing project description goals still work

AgentIan is now **truly flexible and team-friendly** - project goals are visible, accessible, and easy to manage for the entire team!