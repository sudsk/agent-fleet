from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from datetime import datetime
import uuid

from app.database import get_db, Template
from app.services.agent_starter_pack import AgentStarterPackService

router = APIRouter()
agent_starter_pack = AgentStarterPackService()

@router.get("/templates")
async def list_templates(
    framework: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Lists available agent templates with optional filtering."""
    try:
        # Base query
        query = db.query(Template)
        
        # Apply filters
        if framework:
            query = query.filter(Template.framework == framework)
            
        if category:
            query = query.filter(Template.category == category)
            
        # Get templates
        templates = query.all()
        
        return [
            {
                "id": template.id,
                "name": template.name,
                "description": template.description,
                "framework": template.framework,
                "category": template.category,
                "repositoryUrl": template.repository_url,
                "configuration": template.configuration,
                "usageCount": template.usage_count,
                "createdAt": template.created_at,
                "updatedAt": template.updated_at
            }
            for template in templates
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing templates: {str(e)}")

@router.get("/templates/{template_id}")
async def get_template(
    template_id: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Gets a specific template by ID."""
    try:
        template = db.query(Template).filter(Template.id == template_id).first()
        
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
            
        return {
            "id": template.id,
            "name": template.name,
            "description": template.description,
            "framework": template.framework,
            "category": template.category,
            "repositoryUrl": template.repository_url,
            "configuration": template.configuration,
            "usageCount": template.usage_count,
            "createdAt": template.created_at,
            "updatedAt": template.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting template: {str(e)}")

@router.post("/templates")
async def create_template(
    template_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict:
    """Creates a new template."""
    try:
        # Extract template data
        name = template_data.get("name")
        if not name:
            raise HTTPException(status_code=400, detail="Template name is required")
            
        # Create template
        template = Template(
            id=str(uuid.uuid4()),
            name=name,
            description=template_data.get("description"),
            framework=template_data.get("framework", "CUSTOM"),
            category=template_data.get("category"),
            repository_url=template_data.get("repositoryUrl"),
            configuration=template_data.get("configuration"),
            usage_count=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(template)
        db.commit()
        db.refresh(template)
        
        return {
            "id": template.id,
            "name": template.name,
            "description": template.description,
            "framework": template.framework,
            "category": template.category,
            "repositoryUrl": template.repository_url,
            "configuration": template.configuration,
            "usageCount": template.usage_count,
            "createdAt": template.created_at,
            "updatedAt": template.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating template: {str(e)}")

@router.put("/templates/{template_id}")
async def update_template(
    template_id: str,
    template_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict:
    """Updates an existing template."""
    try:
        template = db.query(Template).filter(Template.id == template_id).first()
        
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
            
        # Update fields if provided
        if "name" in template_data:
            template.name = template_data["name"]
            
        if "description" in template_data:
            template.description = template_data["description"]
            
        if "framework" in template_data:
            template.framework = template_data["framework"]
            
        if "category" in template_data:
            template.category = template_data["category"]
            
        if "repositoryUrl" in template_data:
            template.repository_url = template_data["repositoryUrl"]
            
        if "configuration" in template_data:
            template.configuration = template_data["configuration"]
            
        template.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(template)
        
        return {
            "id": template.id,
            "name": template.name,
            "description": template.description,
            "framework": template.framework,
            "category": template.category,
            "repositoryUrl": template.repository_url,
            "configuration": template.configuration,
            "usageCount": template.usage_count,
            "createdAt": template.created_at,
            "updatedAt": template.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating template: {str(e)}")

@router.delete("/templates/{template_id}")
async def delete_template(
    template_id: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Deletes a template."""
    try:
        template = db.query(Template).filter(Template.id == template_id).first()
        
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
            
        db.delete(template)
        db.commit()
        
        return {"message": "Template deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting template: {str(e)}")

@router.post("/templates/{template_id}/initialize")
async def initialize_from_template(
    template_id: str,
    initialization_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Initializes a new agent project from a template.
    This endpoint interacts with the Agent Starter Pack to create a new project.
    """
    try:
        template = db.query(Template).filter(Template.id == template_id).first()
        
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
            
        # Extract initialization parameters
        project_name = initialization_data.get("projectName")
        repository_url = initialization_data.get("repositoryUrl")
        
        if not project_name:
            raise HTTPException(status_code=400, detail="Project name is required")
            
        # Update usage count
        template.usage_count += 1
        db.commit()
        
        # Initialize project using Agent Starter Pack service
        try:
            # This would be implemented to interact with Agent Starter Pack CLI
            result = await agent_starter_pack.initialize_project(
                template_id=template_id,
                project_name=project_name,
                repository_url=repository_url,
                configuration=initialization_data.get("configuration", {})
            )
            
            return {
                "templateId": template.id,
                "projectName": project_name,
                "repositoryUrl": result.get("repositoryUrl"),
                "message": "Project initialized successfully",
                "nextSteps": result.get("nextSteps", [])
            }
            
        except Exception as init_error:
            raise HTTPException(status_code=500, detail=f"Error initializing project: {str(init_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error initializing from template: {str(e)}")

@router.get("/templates/synchronize")
async def synchronize_templates(
    db: Session = Depends(get_db)
) -> Dict:
    """
    Synchronizes templates with the Agent Starter Pack repository.
    This refreshes the template catalog from upstream sources.
    """
    try:
        # Call service to synchronize templates
        result = await agent_starter_pack.synchronize_templates()
        
        # Process templates from Agent Starter Pack
        templates_added = 0
        templates_updated = 0
        
        for template_data in result.get("templates", []):
            # Check if template already exists
            template_name = template_data.get("name")
            existing_template = db.query(Template).filter(Template.name == template_name).first()
            
            if existing_template:
                # Update existing template
                existing_template.description = template_data.get("description", existing_template.description)
                existing_template.framework = template_data.get("framework", existing_template.framework)
                existing_template.category = template_data.get("category", existing_template.category)
                existing_template.repository_url = template_data.get("repositoryUrl", existing_template.repository_url)
                existing_template.configuration = template_data.get("configuration", existing_template.configuration)
                existing_template.updated_at = datetime.utcnow()
                templates_updated += 1
            else:
                # Create new template
                template = Template(
                    id=str(uuid.uuid4()),
                    name=template_name,
                    description=template_data.get("description"),
                    framework=template_data.get("framework", "CUSTOM"),
                    category=template_data.get("category"),
                    repository_url=template_data.get("repositoryUrl"),
                    configuration=template_data.get("configuration"),
                    usage_count=0,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(template)
                templates_added += 1
                
        db.commit()
        
        return {
            "status": "success",
            "templatesAdded": templates_added,
            "templatesUpdated": templates_updated,
            "lastSynchronized": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error synchronizing templates: {str(e)}")
