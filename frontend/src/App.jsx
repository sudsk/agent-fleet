import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AppHeader from './components/layout/AppHeader';
import AppSidebar from './components/layout/AppSidebar';
import Dashboard from './pages/Dashboard';
import AgentsList from './pages/agents/AgentsList';
// import AgentDetails from './pages/agents/AgentDetails';
import DeploymentsList from './pages/deployments/DeploymentsList';
import Playground from './pages/playground/Playground';
import TemplateGallery from './pages/templates/TemplateGallery';
import TemplateDetails from './pages/templates/TemplateDetails';
import NotFoundPage from './pages/NotFoundPage';

function App() {
  const [projectId, setProjectId] = useState(localStorage.getItem('projectId') || '');
  const [region, setRegion] = useState(localStorage.getItem('region') || 'us-central1');

  useEffect(() => {
    // Initialize from localStorage
    const storedProjectId = localStorage.getItem('projectId');
    const storedRegion = localStorage.getItem('region');
    
    if (storedProjectId) setProjectId(storedProjectId);
    if (storedRegion) setRegion(storedRegion);
  }, []);

  const updateProjectSettings = (newProjectId, newRegion) => {
    setProjectId(newProjectId);
    setRegion(newRegion);
    
    // Store in localStorage for persistence
    localStorage.setItem('projectId', newProjectId);
    localStorage.setItem('region', newRegion);
  };

  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        <AppSidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          <AppHeader 
            projectId={projectId} 
            region={region} 
            updateProjectSettings={updateProjectSettings} 
          />
          <main className="flex-1 overflow-auto bg-gray-50 p-4">
            <Routes>
              <Route path="/" element={<Dashboard projectId={projectId} region={region} />} />
              
              {/* Agent Routes */}
              <Route path="/agents" element={<AgentsList projectId={projectId} region={region} />} />
              <Route path="/agents/:agentId" element={<AgentDetails projectId={projectId} region={region} />} />
              
              {/* Deployment Routes */}
              <Route path="/deployments" element={<DeploymentsList projectId={projectId} region={region} />} />
              
              {/* Playground Route */}
              <Route path="/playground" element={<Playground projectId={projectId} region={region} />} />
              <Route path="/playground/:agentId" element={<Playground projectId={projectId} region={region} />} />
              
              {/* Template Routes */}
              <Route path="/templates" element={<TemplateGallery projectId={projectId} region={region} />} />
              <Route path="/templates/:templateId" element={<TemplateDetails projectId={projectId} region={region} />} />
              
              {/* 404 Page */}
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
