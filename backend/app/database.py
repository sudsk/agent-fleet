from sqlalchemy import create_engine, Column, String, Float, Integer, Text, JSON, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uuid, os
from datetime import datetime
import enum

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/agentfleet")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Enums for status tracking
class AgentStatus(enum.Enum):
    DRAFT = "DRAFT"
    TESTED = "TESTED"
    DEPLOYED = "DEPLOYED"
    ARCHIVED = "ARCHIVED"
    
class EnvironmentType(enum.Enum):
    DEV = "DEVELOPMENT"
    UAT = "UAT"
    PROD = "PRODUCTION"
    
class DeploymentStatus(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"

# Core Models
class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    agent_family_id = Column(String, nullable=False, index=True)  # Grouping for lineage tracking
    framework = Column(String, nullable=False)
    repository_url = Column(String, nullable=True)  # Git repository URL
    source_hash = Column(String, nullable=True)  # Git commit hash or source identifier
    template_id = Column(String, nullable=True)  # Reference to template if created from one
    status = Column(String, nullable=False, default=AgentStatus.DRAFT.value)
    environment = Column(String, nullable=False, default=EnvironmentType.DEV.value)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String, nullable=True)
    
    # Model configuration
    model_id = Column(String, nullable=True)
    temperature = Column(Float, nullable=True)
    max_output_tokens = Column(Integer, nullable=True)
    
    # System instruction/prompt
    system_instruction = Column(Text, nullable=True)
    
    # Additional configuration
    configuration = Column(JSON, nullable=True)  # Flexible configuration storage
    
    # Relationships
    deployments = relationship("Deployment", back_populates="agent")
    metrics = relationship("AgentMetrics", back_populates="agent")
    tests = relationship("AgentTest", back_populates="agent")

class Deployment(Base):
    __tablename__ = "deployments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    deployment_type = Column(String, nullable=False)  # AGENT_ENGINE, CLOUD_RUN, etc.
    version = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    project_id = Column(String, nullable=False)
    region = Column(String, nullable=False)
    resource_name = Column(String, nullable=True)  # Vertex AI resource name
    status = Column(String, nullable=False)
    endpoint_url = Column(String, nullable=True)
    deployed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    deployed_by = Column(String, nullable=True)
    
    # Deployment configuration
    configuration = Column(JSON, nullable=True)  # Deployment-specific configuration
    
    # Relationships
    agent = relationship("Agent", back_populates="deployments")
    
class Template(Base):
    __tablename__ = "templates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    framework = Column(String, nullable=False)
    category = Column(String, nullable=True)  # RAG, Chatbot, Multi-agent, etc.
    repository_url = Column(String, nullable=True)
    configuration = Column(JSON, nullable=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class AgentMetrics(Base):
    __tablename__ = "agent_metrics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    request_count = Column(Integer, default=0)
    avg_response_time_ms = Column(Float, default=0)
    token_count_input = Column(Integer, default=0)
    token_count_output = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    estimated_cost = Column(Float, default=0)
    
    # Relationships
    agent = relationship("Agent", back_populates="metrics")

class AgentTest(Base):
    __tablename__ = "agent_tests"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    metrics = Column(JSON, nullable=True)
    success = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column(String, nullable=True)
    
    # Relationships
    agent = relationship("Agent", back_populates="tests")

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)
