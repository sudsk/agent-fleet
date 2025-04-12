from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class EnvironmentType(str, Enum):
    DEV = "DEVELOPMENT"
    UAT = "UAT"
    PROD = "PRODUCTION"

class AgentStatus(str, Enum):
    DRAFT = "DRAFT"
    TESTED = "TESTED"
    DEPLOYED = "DEPLOYED"
    ARCHIVED = "ARCHIVED"

class DeploymentStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"

class FrameworkType(str, Enum):
    CUSTOM = "CUSTOM"
    LANGCHAIN = "LANGCHAIN"
    LLAMAINDEX = "LLAMAINDEX"
    LANGGRAPH = "LANGGRAPH"
    CREWAI = "CREWAI"

class GenerationConfig(BaseModel):
    temperature: float = 0.2
    maxOutputTokens: int = 1024
    topP: Optional[float] = None
    topK: Optional[int] = None

class SystemInstruction(BaseModel):
    text: str

class SystemInstructionPart(BaseModel):
    text: str

class SystemInstructionRequest(BaseModel):
    parts: List[SystemInstructionPart]

# Request Models
class CreateAgentRequest(BaseModel):
    name: str
    description: Optional[str] = None
    agentFamilyId: Optional[str] = None  # If creating a new agent family
    framework: FrameworkType
    repositoryUrl: Optional[str] = None
    sourceHash: Optional[str] = None
    templateId: Optional[str] = None
    environment: EnvironmentType = EnvironmentType.DEV
    modelId: str
    temperature: float = 0.2
    maxOutputTokens: int = 1024
    systemInstruction: str
    configuration: Optional[Dict[str, Any]] = None

class UpdateAgentRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    repositoryUrl: Optional[str] = None
    sourceHash: Optional[str] = None
    status: Optional[AgentStatus] = None
    modelId: Optional[str] = None
    temperature: Optional[float] = None
    maxOutputTokens: Optional[int] = None
    systemInstruction: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None

class RegisterAgentRequest(BaseModel):
    """Used by CI/CD pipelines to register agents from Agent Starter Pack"""
    name: str
    description: Optional[str] = None
    agentFamilyId: Optional[str] = None
    framework: FrameworkType
    repositoryUrl: str
    sourceHash: str
    environment: EnvironmentType
    projectId: str
    region: str = "us-central1"
    modelId: str
    temperature: float = 0.2
    maxOutputTokens: int = 1024
    systemInstruction: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    deploymentInfo: Optional[Dict[str, Any]] = None

# Response Models
class AgentResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    agentFamilyId: str
    framework: str
    repositoryUrl: Optional[str] = None
    sourceHash: Optional[str] = None
    templateId: Optional[str] = None
    status: str
    environment: str
    modelId: Optional[str] = None
    temperature: Optional[float] = None
    maxOutputTokens: Optional[int] = None
    systemInstruction: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    createdAt: datetime
    updatedAt: datetime
    createdBy: Optional[str] = None

class DeploymentResponse(BaseModel):
    id: str
    agentId: str
    deploymentType: str
    version: str
    environment: str
    projectId: str
    region: str
    resourceName: Optional[str] = None
    status: str
    endpointUrl: Optional[str] = None
    deployedAt: datetime
    deployedBy: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None

class AgentFamilyResponse(BaseModel):
    id: str
    name: str
    agents: List[AgentResponse]

class AgentTestResponse(BaseModel):
    id: str
    agentId: str
    query: str
    response: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    success: bool
    createdAt: datetime
    createdBy: Optional[str] = None

class AgentMetricsResponse(BaseModel):
    id: str
    agentId: str
    date: datetime
    requestCount: int
    avgResponseTimeMs: float
    tokenCountInput: int
    tokenCountOutput: int
    errorCount: int
    estimatedCost: float
