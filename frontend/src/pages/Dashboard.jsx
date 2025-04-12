import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Cpu, PlayCircle, LayoutTemplate, Database, ArrowRight, AlertTriangle } from 'lucide-react';
import StatusBadge from '../components/common/StatusBadge';

const Dashboard = ({ projectId, region }) => {
  const [agentStats, setAgentStats] = useState({
    total: 0,
    deployed: 0,
    tested: 0,
    draft: 0
  });
  
  const [recentAgents, setRecentAgents] = useState([]);
  const [recentDeployments, setRecentDeployments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    // Simulated API calls for demo purposes
    const fetchDashboardData = async () => {
      if (!projectId) {
        setIsLoading(false);
        return;
      }
      
      setIsLoading(true);
      
      try {
        // In a real implementation, this would be API calls
        
        // Simulate agent stats
        setAgentStats({
          total: 12,
          deployed: 5,
          tested: 3,
          draft: 4
        });
        
        // Simulate recent agents
        setRecentAgents([
          {
            id: 'agent-1',
            name: 'Customer Service Bot',
            status: 'DEPLOYED',
            framework: 'LANGGRAPH',
            updatedAt: '2025-04-10T12:00:00Z'
          },
          {
            id: 'agent-2',
            name: 'Document Retrieval Agent',
            status: 'TESTED',
            framework: 'LANGCHAIN',
            updatedAt: '2025-04-09T15:30:00Z'
          },
          {
            id: 'agent-3',
            name: 'Sales Assistant',
            status: 'DRAFT',
            framework: 'CREWAI',
            updatedAt: '2025-04-08T09:15:00Z'
          }
        ]);
        
        // Simulate recent deployments
        setRecentDeployments([
          {
            id: 'deploy-1',
            agentId: 'agent-1',
            agentName: 'Customer Service Bot',
            status: 'SUCCESSFUL',
            deploymentType: 'AGENT_ENGINE',
            deployedAt: '2025-04-10T12:00:00Z'
          },
          {
            id: 'deploy-2',
            agentId: 'agent-4',
            agentName: 'Product Recommendation',
            status: 'FAILED',
            deploymentType: 'CLOUD_RUN',
            deployedAt: '2025-04-09T14:20:00Z'
          }
        ]);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchDashboardData();
  }, [projectId, region]);

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
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm text-gray-500">Total Agents</p>
              <h3 className="text-2xl font-semibold mt-1">{isLoading ? '...' : agentStats.total}</h3>
            </div>
            <div className="p-3 bg-blue-100 rounded-full">
              <Cpu className="h-6 w-6 text-blue-600" />
            </div>
          </div>
          <div className="mt-4">
            <Link to="/agents" className="text-blue-600 text-sm font-medium hover:text-blue-800 inline-flex items-center">
              View all agents
              <ArrowRight className="h-4 w-4 ml-1" />
            </Link>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm text-gray-500">Deployed</p>
              <h3 className="text-2xl font-semibold mt-1">{isLoading ? '...' : agentStats.deployed}</h3>
            </div>
            <div className="p-3 bg-green-100 rounded-full">
              <Database className="h-6 w-6 text-green-600" />
            </div>
          </div>
          <div className="mt-4">
            <Link to="/deployments" className="text-green-600 text-sm font-medium hover:text-green-800 inline-flex items-center">
              View deployments
              <ArrowRight className="h-4 w-4 ml-1" />
            </Link>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm text-gray-500">Testing</p>
              <h3 className="text-2xl font-semibold mt-1">{isLoading ? '...' : agentStats.tested}</h3>
            </div>
            <div className="p-3 bg-purple-100 rounded-full">
              <PlayCircle className="h-6 w-6 text-purple-600" />
            </div>
          </div>
          <div className="mt-4">
            <Link to="/playground" className="text-purple-600 text-sm font-medium hover:text-purple-800 inline-flex items-center">
              Open playground
              <ArrowRight className="h-4 w-4 ml-1" />
            </Link>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm text-gray-500">Templates</p>
              <h3 className="text-2xl font-semibold mt-1">{isLoading ? '...' : 5}</h3>
            </div>
            <div className="p-3 bg-yellow-100 rounded-full">
              <LayoutTemplate className="h-6 w-6 text-yellow-600" />
            </div>
          </div>
          <div className="mt-4">
            <Link to="/templates" className="text-yellow-600 text-sm font-medium hover:text-yellow-800 inline-flex items-center">
              Browse templates
              <ArrowRight className="h-4 w-4 ml-1" />
            </Link>
          </div>
        </div>
      </div>
      
      {/* Recent Agents and Deployments */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Recent Agents */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="border-b border-gray-200 px-6 py-4 flex justify-between items-center">
            <h2 className="text-lg font-semibold">Recent Agents</h2>
            <Link to="/agents" className="text-sm text-blue-600 hover:text-blue-800">View all</Link>
          </div>
          <div className="p-6">
            {isLoading ? (
              <div className="py-4 text-center text-gray-500">Loading...</div>
            ) : recentAgents.length === 0 ? (
              <div className="py-8 text-center text-gray-500">
                <p className="mb-4">No agents found in this project.</p>
                <Link to="/agents/create" className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                  Create your first agent
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {recentAgents.map((agent) => (
                  <div key={agent.id} className="flex items-center justify-between">
                    <div>
                      <Link to={`/agents/${agent.id}`} className="font-medium text-blue-600 hover:text-blue-800">
                        {agent.name}
                      </Link>
                      <p className="text-xs text-gray-500">
                        <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs mr-2">
                          {agent.framework}
                        </span>
                        {new Date(agent.updatedAt).toLocaleDateString()}
                      </p>
                    </div>
                    <StatusBadge status={agent.status} />
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        
        {/* Recent Deployments */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="border-b border-gray-200 px-6 py-4 flex justify-between items-center">
            <h2 className="text-lg font-semibold">Recent Deployments</h2>
            <Link to="/deployments" className="text-sm text-blue-600 hover:text-blue-800">View all</Link>
          </div>
          <div className="p-6">
            {isLoading ? (
              <div className="py-4 text-center text-gray-500">Loading...</div>
            ) : recentDeployments.length === 0 ? (
              <div className="py-8 text-center text-gray-500">
                <p>No deployments found in this project.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {recentDeployments.map((deployment) => (
                  <div key={deployment.id} className="flex items-center justify-between">
                    <div>
                      <Link to={`/agents/${deployment.agentId}`} className="font-medium text-blue-600 hover:text-blue-800">
                        {deployment.agentName}
                      </Link>
                      <p className="text-xs text-gray-500">
                        <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs mr-2">
                          {deployment.deploymentType}
                        </span>
                        {new Date(deployment.deployedAt).toLocaleDateString()}
                      </p>
                    </div>
                    <StatusBadge status={deployment.status} />
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Getting Started Guide */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <h2 className="text-lg font-semibold mb-4">Getting Started with AgentFleet</h2>
        <div className="space-y-4">
          <div className="flex">
            <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mr-4">
              1
            </div>
            <div>
              <h3 className="text-md font-medium">Connect to Agent Starter Pack</h3>
              <p className="text-sm text-gray-600 mt-1">
                Use AgentFleet to manage agents created with the Agent Starter Pack
              </p>
            </div>
          </div>
          
          <div className="flex">
            <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mr-4">
              2
            </div>
            <div>
              <h3 className="text-md font-medium">Browse Template Gallery</h3>
              <p className="text-sm text-gray-600 mt-1">
                Choose from pre-built agent templates to get started quickly
              </p>
            </div>
          </div>
          
          <div className="flex">
            <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mr-4">
              3
            </div>
            <div>
              <h3 className="text-md font-medium">Test in Local Playground</h3>
              <p className="text-sm text-gray-600 mt-1">
                Try your agent in the playground before deployment
              </p>
            </div>
          </div>
          
          <div className="flex">
            <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mr-4">
              4
            </div>
            <div>
              <h3 className="text-md font-medium">Deploy and Monitor</h3>
              <p className="text-sm text-gray-600 mt-1">
                Deploy your agents to production and monitor their performance
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
