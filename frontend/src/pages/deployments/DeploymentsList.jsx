import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Database, Search, Info, ExternalLink, AlertTriangle } from 'lucide-react';
import StatusBadge from '../../components/common/StatusBadge';

const DeploymentsList = ({ projectId, region }) => {
  const [deployments, setDeployments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  
  useEffect(() => {
    const fetchDeployments = async () => {
      if (!projectId) {
        setIsLoading(false);
        return;
      }
      
      setIsLoading(true);
      
      try {
        // In a real implementation, this would be an API call
        // Simulate API response
        setTimeout(() => {
          const mockDeployments = [
            {
              id: 'deploy-1',
              agentId: 'agent-1',
              agentName: 'Customer Service Bot',
              deploymentType: 'AGENT_ENGINE',
              version: '1.0.0',
              environment: 'DEVELOPMENT',
              projectId: projectId,
              region: region,
              resourceName: `projects/${projectId}/locations/${region}/reasoningEngines/agent-1`,
              status: 'SUCCESSFUL',
              endpointUrl: `https://${region}-aiplatform.googleapis.com/v1/projects/${projectId}/locations/${region}/reasoningEngines/agent-1`,
              deployedAt: '2025-04-10T12:00:00Z',
              deployedBy: 'user@example.com'
            },
            {
              id: 'deploy-2',
              agentId: 'agent-4',
              agentName: 'Product Recommendation',
              deploymentType: 'CLOUD_RUN',
              version: '1.0.0',
              environment: 'DEVELOPMENT',
              projectId: projectId,
              region: region,
              resourceName: `projects/${projectId}/locations/${region}/services/agent-4`,
              status: 'FAILED',
              deployedAt: '2025-04-09T14:20:00Z',
              deployedBy: 'user@example.com'
            },
            {
              id: 'deploy-3',
              agentId: 'agent-2',
              agentName: 'Document Retrieval Agent',
              deploymentType: 'AGENT_ENGINE',
              version: '1.1.0',
              environment: 'DEVELOPMENT',
              projectId: projectId,
              region: region,
              resourceName: `projects/${projectId}/locations/${region}/reasoningEngines/agent-2`,
              status: 'IN_PROGRESS',
              deployedAt: '2025-04-11T09:45:00Z',
              deployedBy: 'user@example.com'
            }
          ];
          
          setDeployments(mockDeployments);
          setIsLoading(false);
        }, 1000);
      } catch (error) {
        console.error('Error fetching deployments:', error);
        setIsLoading(false);
      }
    };
    
    fetchDeployments();
  }, [projectId, region]);
  
  const filteredDeployments = deployments.filter(deployment => 
    deployment.agentName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    deployment.deploymentType.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  if (!projectId) {
    return (
      <div className="w-full h-full flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-200 max-w-lg">
          <AlertTriangle className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-4 text-center">No Google Cloud Project selected</h2>
          <p className="mb-4 text-gray-600 text-center">
            Please set your Google Cloud Project ID in the top navigation to get started.
          </p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Deployments</h1>
        <div className="flex gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search deployments..."
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        {isLoading ? (
          <div className="p-8 text-center">
            <svg className="animate-spin h-8 w-8 text-blue-600 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="text-gray-500">Loading deployments...</p>
          </div>
        ) : filteredDeployments.length === 0 ? (
          <div className="p-8 text-center">
            {searchTerm ? (
              <p className="text-gray-500">No deployments found matching "{searchTerm}"</p>
            ) : (
              <>
                <Info className="h-12 w-12 text-blue-500 mx-auto mb-4" />
                <p className="mb-4 text-gray-600">No deployments found in this project.</p>
                <Link
                  to="/agents"
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Deploy an agent
                </Link>
              </>
            )}
          </div>
        ) : (
          <>
            <div className="grid grid-cols-12 py-3 px-4 border-b border-gray-200 bg-gray-50 text-sm font-medium text-gray-600">
              <div className="col-span-3">Agent</div>
              <div className="col-span-2">Type</div>
              <div className="col-span-2">Version</div>
              <div className="col-span-2">Status</div>
              <div className="col-span-2">Deployment Date</div>
              <div className="col-span-1">Actions</div>
            </div>
            
            {filteredDeployments.map((deployment) => (
              <div 
                key={deployment.id} 
                className="grid grid-cols-12 py-4 px-4 border-b border-gray-200 hover:bg-gray-50"
              >
                <div className="col-span-3 flex items-center">
                  <div className="h-8 w-8 rounded-full bg-green-100 flex items-center justify-center text-green-600 mr-3">
                    <Database size={16} />
                  </div>
                  <div>
                    <Link to={`/agents/${deployment.agentId}`} className="font-medium text-gray-900 hover:text-blue-600">
                      {deployment.agentName}
                    </Link>
                    <p className="text-xs text-gray-500">
                      {deployment.environment}
                    </p>
                  </div>
                </div>
                <div className="col-span-2 flex items-center">
                  <span className="px-2 py-1 bg-gray-100 rounded text-xs">
                    {deployment.deploymentType}
                  </span>
                </div>
                <div className="col-span-2 flex items-center text-sm">
                  {deployment.version}
                </div>
                <div className="col-span-2 flex items-center">
                  <StatusBadge status={deployment.status} />
                </div>
                <div className="col-span-2 flex items-center text-sm text-gray-600">
                  {new Date(deployment.deployedAt).toLocaleDateString()}
                </div>
                <div className="col-span-1 flex items-center">
                  {deployment.status === 'SUCCESSFUL' && deployment.endpointUrl && (
                    <a
                      href={deployment.endpointUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-1 text-gray-500 hover:text-blue-600 rounded-full hover:bg-gray-100"
                      title="View Endpoint"
                    >
                      <ExternalLink size={18} />
                    </a>
                  )}
                </div>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
};

export default DeploymentsList;
