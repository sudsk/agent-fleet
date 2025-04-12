from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path, File, UploadFile, Form
from datetime import datetime
import uuid

from app.database import get_db, Agent, AgentTest
from app.services.vertex_ai import VertexAIService
from app.services.agent_tester import AgentTesterService

router = APIRouter()
vertex_service = VertexAIService()
agent_tester = AgentTesterService()

@router.post("/playground/test")
async def test_agent(
    test_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Tests an agent in the local playground.
    This allows testing of agent behavior before deployment.
    """
    try:
        agent_id = test_data.get("agentId")
        if not agent_id:
            raise HTTPException(status_code=400, detail="Agent ID is required")
            
        # Get query and additional parameters
        query = test_data.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
            
        # Get file information if provided
        files = test_data.get("files", [])
        
        # Start timer for metrics
        start_time = datetime.utcnow()
        success = True
        
        # Get agent
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Test the agent
        try:
            # Call agent testing service
            response = await agent_tester.test_agent(
                agent=agent,
                query=query,
                files=files,
                additional_params=test_data.get("additionalParams", {})
            )
            
        except Exception as test_error:
            success = False
            response = {
                "textResponse": f"Error testing agent: {str(test_error)}",
                "error": str(test_error)
            }
            
        # End timer
        end_time = datetime.utcnow()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        # Record test in database
        test_record = AgentTest(
            id=str(uuid.uuid4()),
            agent_id=agent.id,
            query=query,
            response=response.get("textResponse", ""),
            metrics={
                "duration_ms": duration_ms,
                "success": success,
                "totalTokens": response.get("metrics", {}).get("totalTokens", 0),
                "inputTokens": response.get("metrics", {}).get("inputTokens", 0),
                "outputTokens": response.get("metrics", {}).get("outputTokens", 0)
            },
            success=success,
            created_at=datetime.utcnow()
        )
        
        db.add(test_record)
        db.commit()
        
        # Return the response
        return {
            "testId": test_record.id,
            "agentId": agent.id,
            "textResponse": response.get("textResponse", ""),
            "actions": response.get("actions", []),
            "files": response.get("files", []),
            "metrics": {
                "duration_ms": duration_ms,
                "success": success,
                "totalTokens": response.get("metrics", {}).get("totalTokens", 0)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing agent: {str(e)}")

@router.get("/playground/tests")
async def list_tests(
    agent_id: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Lists test history for an agent or all tests."""
    try:
        # Base query
        query = db.query(AgentTest)
        
        # Filter by agent if provided
        if agent_id:
            query = query.filter(AgentTest.agent_id == agent_id)
            
        # Get tests
        tests = query.order_by(AgentTest.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": test.id,
                "agentId": test.agent_id,
                "query": test.query,
                "response": test.response,
                "metrics": test.metrics,
                "success": test.success,
                "createdAt": test.created_at
            }
            for test in tests
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tests: {str(e)}")

@router.post("/playground/upload")
async def upload_test_files(
    files: List[UploadFile] = File(...),
    session_id: Optional[str] = Form(None)
) -> Dict:
    """
    Uploads files for testing with agents.
    These files can be referenced in agent test queries.
    """
    try:
        if not session_id:
            session_id = str(uuid.uuid4())
            
        uploaded_files = []
        
        for file in files:
            # Process the file
            file_data = await file.read()
            
            # Save file for testing session
            # In a production implementation, this would save to storage
            file_id = str(uuid.uuid4())
            filename = file.filename
            content_type = file.content_type
            
            uploaded_files.append({
                "file_id": file_id,
                "filename": filename,
                "content_type": content_type,
                "size": len(file_data)
            })
            
        return {
            "session_id": session_id,
            "files": uploaded_files,
            "message": f"Successfully uploaded {len(uploaded_files)} files"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")

@router.post("/playground/query")
async def query_deployed_agent(
    query_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Queries an agent that has already been deployed to Vertex AI.
    This is useful for testing deployed agents through AgentFleet.
    """
    try:
        agent_id = query_data.get("agentId")
        if not agent_id:
            raise HTTPException(status_code=400, detail="Agent ID is required")
            
        query = query_data.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
            
        project_id = query_data.get("projectId")
        region = query_data.get("region", "us-central1")
        
        if not project_id:
            raise HTTPException(status_code=400, detail="Project ID is required")
            
        # Get agent
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Find the latest successful deployment
        from sqlalchemy import and_
        from app.database import DeploymentStatus
        
        deployment = (
            db.query(db.Deployment)
            .filter(
                and_(
                    db.Deployment.agent_id == agent_id,
                    db.Deployment.project_id == project_id,
                    db.Deployment.region == region,
                    db.Deployment.status == DeploymentStatus.SUCCESSFUL.value
                )
            )
            .order_by(db.Deployment.deployed_at.desc())
            .first()
        )
        
        if not deployment:
            raise HTTPException(status_code=404, detail="No successful deployment found for this agent")
            
        # Start timer for metrics
        start_time = datetime.utcnow()
        
        # Query the deployed agent
        try:
            response = await vertex_service.query_agent(
                project_id=project_id,
                region=region,
                resource_name=deployment.resource_name,
                query=query
            )
            
            success = True
            
        except Exception as query_error:
            success = False
            response = {
                "textResponse": f"Error querying agent: {str(query_error)}",
                "error": str(query_error)
            }
            
        # End timer
        end_time = datetime.utcnow()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        # Record test in database
        test_record = AgentTest(
            id=str(uuid.uuid4()),
            agent_id=agent.id,
            query=query,
            response=response.get("textResponse", ""),
            metrics={
                "duration_ms": duration_ms,
                "success": success,
                "deployment_id": deployment.id,
                "project_id": project_id,
                "region": region
            },
            success=success,
            created_at=datetime.utcnow()
        )
        
        db.add(test_record)
        db.commit()
        
        # Return the response
        return {
            "testId": test_record.id,
            "agentId": agent.id,
            "textResponse": response.get("textResponse", ""),
            "actions": response.get("actions", []),
            "metrics": {
                "duration_ms": duration_ms,
                "success": success
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying deployed agent: {str(e)}")
