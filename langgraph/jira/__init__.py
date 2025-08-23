# jira/__init__.py
"""
Jira integration module for AgentTeam
"""

from .client import JiraClient, JiraIssue, JiraTask

__all__ = ['JiraClient', 'JiraIssue', 'JiraTask']