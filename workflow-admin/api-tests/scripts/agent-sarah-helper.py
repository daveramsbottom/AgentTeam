#!/usr/bin/env python3
"""
AgentSarah Helper Script for API Test Management
Provides utilities for AI agents to interact with Newman collections
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class NewmanTestManager:
    """Helper class for AgentSarah to manage API tests"""
    
    def __init__(self, base_path: str = "/tests"):
        self.base_path = Path(base_path)
        self.collections_path = self.base_path / "collections"
        self.environments_path = self.base_path / "environments"
        self.data_path = self.base_path / "data"
        self.results_path = self.base_path / "results"
        
        # Ensure directories exist
        for path in [self.collections_path, self.environments_path, self.data_path, self.results_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def create_test_collection(self, name: str, description: str, tests: List[Dict]) -> str:
        """Create a new Postman collection file"""
        collection = {
            "info": {
                "name": f"Workflow Admin - {name}",
                "description": description,
                "version": "1.0.0",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "auth": {"type": "noauth"},
            "event": self._get_global_events(),
            "variable": [{"key": "collection_version", "value": "1.0.0"}],
            "item": tests
        }
        
        file_path = self.collections_path / f"{name.lower().replace(' ', '-')}.postman.json"
        with open(file_path, 'w') as f:
            json.dump(collection, f, indent=2)
        
        return str(file_path)
    
    def add_test_to_collection(self, collection_name: str, test_item: Dict) -> bool:
        """Add a new test to an existing collection"""
        file_path = self.collections_path / f"{collection_name}.postman.json"
        
        if not file_path.exists():
            return False
        
        with open(file_path, 'r') as f:
            collection = json.load(f)
        
        collection["item"].append(test_item)
        
        with open(file_path, 'w') as f:
            json.dump(collection, f, indent=2)
        
        return True
    
    def create_test_item(self, name: str, method: str, url: str, 
                        tests: List[str], description: str = "", 
                        body: Optional[Dict] = None) -> Dict:
        """Create a test item for a collection"""
        item = {
            "name": name,
            "event": [
                {
                    "listen": "test",
                    "script": {"exec": tests}
                }
            ],
            "request": {
                "method": method.upper(),
                "header": [],
                "url": {
                    "raw": url,
                    "host": ["{{base_url}}"],
                    "path": url.replace("{{base_url}}/", "").split("/")
                },
                "description": description
            },
            "response": []
        }
        
        if body and method.upper() in ["POST", "PUT", "PATCH"]:
            item["request"]["body"] = {
                "mode": "raw",
                "raw": json.dumps(body, indent=2),
                "options": {
                    "raw": {"language": "json"}
                }
            }
        
        return item
    
    def run_tests(self, collection: str, environment: str = "docker") -> Dict:
        """Execute tests using Newman and return results"""
        cmd = [
            "newman", "run", 
            f"collections/{collection}.postman.json",
            "--environment", f"environments/{environment}.json",
            "--reporters", "json",
            "--reporter-json-export", f"results/temp-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        ]
        
        try:
            result = subprocess.run(cmd, cwd=self.base_path, capture_output=True, text=True)
            
            # Parse results if available
            if result.returncode == 0:
                # Find the most recent results file
                results_files = list(self.results_path.glob("temp-*.json"))
                if results_files:
                    latest_result = max(results_files, key=os.path.getctime)
                    with open(latest_result, 'r') as f:
                        return json.load(f)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_test_results(self, results: Dict) -> Dict:
        """Analyze test results and provide insights for AI agents"""
        if not results.get("run"):
            return {"error": "No valid test results found"}
        
        run_data = results["run"]
        stats = run_data.get("stats", {})
        
        analysis = {
            "summary": {
                "total_tests": stats.get("tests", {}).get("total", 0),
                "passed_tests": stats.get("tests", {}).get("passed", 0),
                "failed_tests": stats.get("tests", {}).get("failed", 0),
                "total_requests": stats.get("requests", {}).get("total", 0),
                "failed_requests": stats.get("requests", {}).get("failed", 0),
                "avg_response_time": stats.get("requests", {}).get("average", 0)
            },
            "pass_rate": 0,
            "recommendations": [],
            "failed_tests": []
        }
        
        # Calculate pass rate
        total_tests = analysis["summary"]["total_tests"]
        if total_tests > 0:
            analysis["pass_rate"] = (analysis["summary"]["passed_tests"] / total_tests) * 100
        
        # Extract failed test details
        for execution in run_data.get("executions", []):
            for assertion in execution.get("assertions", []):
                if assertion.get("error"):
                    analysis["failed_tests"].append({
                        "test_name": assertion.get("assertion"),
                        "error": assertion.get("error", {}).get("message"),
                        "request": execution.get("item", {}).get("name")
                    })
        
        # Generate recommendations
        if analysis["pass_rate"] < 100:
            analysis["recommendations"].append("Some tests are failing - review failed test details")
        if analysis["summary"]["avg_response_time"] > 2000:
            analysis["recommendations"].append("Response times are high - consider performance optimization")
        if analysis["summary"]["failed_requests"] > 0:
            analysis["recommendations"].append("Request failures detected - check API availability")
        
        return analysis
    
    def _get_global_events(self) -> List[Dict]:
        """Get global event scripts for collections"""
        return [
            {
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "pm.request.headers.add({key: 'Content-Type', value: pm.environment.get('content_type')});"
                    ]
                }
            },
            {
                "listen": "test", 
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "pm.test('Response time is acceptable', function () {",
                        "    const timeout = parseInt(pm.environment.get('timeout')) || 5000;",
                        "    pm.expect(pm.response.responseTime).to.be.below(timeout);",
                        "});"
                    ]
                }
            }
        ]

if __name__ == "__main__":
    # Example usage for AgentSarah
    manager = NewmanTestManager()
    
    # Create a simple test
    test_item = manager.create_test_item(
        name="Test Agent Creation",
        method="POST",
        url="{{base_url}}/api/{{api_version}}/agents",
        tests=[
            "pm.test('Agent created successfully', function () {",
            "    pm.response.to.have.status(201);",
            "});"
        ],
        body={"name": "TestAgent", "agent_type": "Developer"}
    )
    
    print("✅ Newman Test Manager ready for AgentSarah!")
    print(f"📁 Collections: {manager.collections_path}")
    print(f"🌍 Environments: {manager.environments_path}")
    print(f"📊 Results: {manager.results_path}")