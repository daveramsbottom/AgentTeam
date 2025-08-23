import requests
import os
from typing import Optional, Dict, Any, List

class TaigaClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.auth_token = None
        
    def authenticate(self) -> bool:
        """Authenticate with Taiga and get auth token"""
        auth_url = f"{self.base_url}/auth"
        
        payload = {
            "username": self.username,
            "password": self.password,
            "type": "normal"
        }
        
        try:
            response = requests.post(auth_url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            self.auth_token = data.get("auth_token")
            
            if self.auth_token:
                print(f"✅ Successfully authenticated as {self.username}")
                return True
            else:
                print("❌ Authentication failed: No token received")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers with authorization token"""
        if not self.auth_token:
            raise ValueError("Not authenticated. Call authenticate() first.")
        
        return {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the connection and return basic info"""
        if not self.auth_token:
            if not self.authenticate():
                return {"error": "Authentication failed"}
        
        try:
            projects = self.get_projects()
            if projects is None:
                return {"error": "Could not fetch projects"}
            
            return {
                "success": True,
                "projects_count": len(projects),
                "authenticated_user": self.username
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_projects(self) -> Optional[list]:
        """Get all projects for authenticated user"""
        if not self.auth_token:
            if not self.authenticate():
                return None
        
        try:
            response = requests.get(
                f"{self.base_url}/projects",
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching projects: {e}")
            return None
    
    def get_project_details(self, project_id: int) -> Optional[Dict]:
        """Get detailed information about a specific project including statuses"""
        if not self.auth_token:
            if not self.authenticate():
                return None
        
        try:
            response = requests.get(
                f"{self.base_url}/projects/{project_id}",
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching project details: {e}")
            return None
    
    def get_project_members(self, project_id: int) -> Optional[List[Dict]]:
        """Get project members"""
        if not self.auth_token:
            if not self.authenticate():
                return None
        
        try:
            response = requests.get(
                f"{self.base_url}/memberships",
                headers=self.get_headers(),
                params={"project": project_id}
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching project members: {e}")
            return None
    
    def get_user_story_statuses(self, project_id: int) -> Optional[List[Dict]]:
        """Get available user story statuses for a project"""
        if not self.auth_token:
            if not self.authenticate():
                return None
        
        try:
            response = requests.get(
                f"{self.base_url}/userstory-statuses",
                headers=self.get_headers(),
                params={"project": project_id}
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching user story statuses: {e}")
            return None
    
    def create_user_story(self, story_data: Dict[str, Any]) -> Optional[Dict]:
        """Create a new user story"""
        if not self.auth_token:
            if not self.authenticate():
                return None
        
        try:
            print(f"📄 Creating user story: {story_data.get('subject', 'Unknown')}")
            response = requests.post(
                f"{self.base_url}/userstories",
                headers=self.get_headers(),
                json=story_data
            )
            response.raise_for_status()
            
            created_story = response.json()
            print(f"✅ Successfully created user story ID: {created_story.get('id')}")
            return created_story
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating user story: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response details: {e.response.text}")
            return None
    
    def get_user_stories(self, project_id: int) -> Optional[list]:
        """Get user stories for a project"""
        if not self.auth_token:
            if not self.authenticate():
                return None
        
        try:
            response = requests.get(
                f"{self.base_url}/userstories",
                headers=self.get_headers(),
                params={"project": project_id}
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching user stories: {e}")
            return None
    
    def update_user_story(self, story_id: int, update_data: Dict[str, Any]) -> Optional[Dict]:
        """Update an existing user story"""
        if not self.auth_token:
            if not self.authenticate():
                return None
        
        try:
            print(f"📄 Updating user story ID: {story_id}")
            response = requests.patch(
                f"{self.base_url}/userstories/{story_id}",
                headers=self.get_headers(),
                json=update_data
            )
            response.raise_for_status()
            
            updated_story = response.json()
            print(f"✅ Successfully updated user story ID: {story_id}")
            return updated_story
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error updating user story: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response details: {e.response.text}")
            return None
    
    def add_comment_to_story(self, story_id: int, comment: str) -> bool:
        """Add a comment to a user story"""
        if not self.auth_token:
            if not self.authenticate():
                return False
        
        try:
            # Get the story first to get its current version
            story_response = requests.get(
                f"{self.base_url}/userstories/{story_id}",
                headers=self.get_headers()
            )
            story_response.raise_for_status()
            story_data = story_response.json()
            
            # Add comment using PATCH with comment field
            comment_payload = {
                "comment": comment,
                "version": story_data.get("version", 1)
            }
            
            response = requests.patch(
                f"{self.base_url}/userstories/{story_id}",
                headers=self.get_headers(),
                json=comment_payload
            )
            response.raise_for_status()
            
            print(f"✅ Comment added to story {story_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding comment: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            
            # Fallback: Update description instead
            print("📄 Trying fallback: updating description...")
            try:
                story_response = requests.get(
                    f"{self.base_url}/userstories/{story_id}",
                    headers=self.get_headers()
                )
                story_response.raise_for_status()
                story_data = story_response.json()
                
                current_description = story_data.get("description", "")
                new_description = f"{current_description}\n\n---\n**Agent Comment ({story_data.get('version', 1)}):**\n{comment}"
                
                update_payload = {
                    "version": story_data.get("version", 1),
                    "description": new_description
                }
                
                response = requests.patch(
                    f"{self.base_url}/userstories/{story_id}",
                    headers=self.get_headers(),
                    json=update_payload
                )
                response.raise_for_status()
                
                print(f"✅ Comment added to story description instead")
                return True
                
            except requests.exceptions.RequestException as fallback_error:
                print(f"❌ Fallback also failed: {fallback_error}")
                return False

    def debug_project_structure(self, project_id: int) -> Dict[str, Any]:
        """Debug method to inspect project structure and available fields"""
        print(f"🔍 Debugging project structure for project ID: {project_id}")
        
        debug_info = {
            "project_details": None,
            "user_stories": None,
            "story_statuses": None,
            "errors": []
        }
        
        try:
            # Get project details
            project_details = self.get_project_details(project_id)
            debug_info["project_details"] = project_details
            
            if project_details:
                print(f"📋 Project: {project_details.get('name')}")
                print(f"🆔 Project ID: {project_details.get('id')}")
                print(f"📝 Description: {project_details.get('description', 'No description')}")
            
            # Get user story statuses
            statuses = self.get_user_story_statuses(project_id)
            debug_info["story_statuses"] = statuses
            
            if statuses:
                print(f"📊 Available user story statuses:")
                for status in statuses:
                    print(f"   - {status.get('name')} (ID: {status.get('id')})")
            
            # Get existing user stories
            stories = self.get_user_stories(project_id)
            debug_info["user_stories"] = stories
            
            if stories:
                print(f"📚 Found {len(stories)} existing user stories:")
                for story in stories:
                    status_name = story.get('status_extra_info', {}).get('name', 'Unknown')
                    print(f"   - {story.get('subject')} (ID: {story.get('id')}, Status: {status_name})")
            else:
                print("📚 No user stories found")
            
        except Exception as e:
            error_msg = f"Debug error: {e}"
            debug_info["errors"].append(error_msg)
            print(f"❌ {error_msg}")
        
        return debug_info