# Enhanced AgentIan Testing Guide

## Quick Verification Steps

### 1. **Test the Enhanced Architecture Components**
```bash
python3 langgraph/test_enhanced_workflow.py
```

This will verify:
- ✅ Context analyzer detects project types correctly
- ✅ State machine transitions work
- ✅ Story filtering prevents duplicates
- ✅ Enhanced story generation uses context

### 2. **Test Enhanced AgentIan (Architecture Test)**
```bash
python3 langgraph/main.py --enhanced
```

Look for these differences from old AgentIan:
- 📊 Shows "State Machine: MONITORING" 
- 🔍 Shows "Monitoring System: 2 monitors, 3 handlers"
- 🤖 Shows "Enhanced Capabilities Preview"
- 💬 Sends message about "flexible state machine + event monitoring"

### 3. **Test Continuous Monitoring (The Big Test)**
```bash
python3 langgraph/main.py --enhanced-monitoring
```

This starts the enhanced agent in continuous mode:
- 🔍 Monitors Slack every 30 seconds
- 📊 Monitors Jira every 60 seconds  
- 🧠 Uses intelligent context analysis
- 💬 Responds to messages with context awareness

### 4. **Test Different Project Types**

Send these messages in Slack to test context awareness:

#### Basic App Test:
```
"Create a simple calculator app"
```
**Expected:** Should detect "basic_application", ask minimal questions, avoid authentication stories

#### E-commerce Test:
```
"Build an online store for selling books"
```
**Expected:** Should detect "e-commerce_web_app", ask about products/payments, suggest cart/catalog stories

#### Existing Stories Test:
```
"Add new features to my project" (when stories already exist)
```
**Expected:** Should analyze existing backlog, avoid duplicates, suggest complementary stories

### 5. **Verify Duplicate Prevention**

1. Create some stories in Jira manually
2. Send same project request again
3. **Expected:** Should say "All necessary stories already exist" or create only non-duplicate stories

## Key Differences to Look For

### ❌ Old Hardcoded Behavior:
- Always asks same 3-4 questions
- Always creates "User Registration" + "Dashboard" stories
- Ignores existing backlog
- Same behavior regardless of project type

### ✅ New Intelligent Behavior:
- Analyzes existing stories first
- Detects project type (basic, e-commerce, API, etc.)
- Asks context-specific questions
- Creates relevant stories for project type
- Skips duplicate stories
- Provides reasoning for decisions

## Verification Checklist

### Context Analysis Working:
- [ ] Different questions for "basic app" vs "e-commerce app"
- [ ] Fewer questions when stories already exist
- [ ] Project type detection in messages ("Project Type Detected: basic_application")

### Story Generation Working:
- [ ] Basic app: Gets simple functionality stories (no authentication)
- [ ] E-commerce app: Gets product/cart/payment stories
- [ ] API service: Gets endpoint/authentication stories
- [ ] No duplicate stories created when they already exist

### Event Monitoring Working:
- [ ] Responds to Slack messages within 30 seconds
- [ ] Detects Jira story status changes
- [ ] Sends periodic health checks
- [ ] Shows current agent state in responses

### Human-like Behavior:
- [ ] Provides reasoning for decisions
- [ ] Acknowledges existing work
- [ ] Suggests next actions based on project phase
- [ ] Idles appropriately when no work needed

## Debugging Tips

### If Still Getting Same Stories:
1. Check logs for "Using intelligent story generation" vs "Using fallback"
2. Verify enhanced agent is being used (look for state machine messages)
3. Check that context analyzer is running (should see project type detection)

### If Questions Are Still Generic:
1. Verify intelligent context analyzer is loaded
2. Check that existing stories are being analyzed
3. Look for "context-aware questions" in logs

### If Duplicates Are Created:
1. Check story filtering logs ("Skipping duplicate story")
2. Verify Jira connection is working
3. Test similarity detection manually

## Success Indicators

When everything is working, you should see:

1. **Context Awareness**: "Project Type Detected: basic_application"
2. **Intelligent Questions**: Different questions for different project types
3. **Duplicate Prevention**: "All necessary stories already exist" or "2 skipped to avoid duplicates"
4. **Reasoning**: Clear explanations for decisions
5. **State Awareness**: Messages about current agent state and next actions

The key test is: **Try the same project request twice - the second time should be handled differently!**