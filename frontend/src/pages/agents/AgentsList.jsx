import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Cpu, Search, Plus, MoreHorizontal, Play, Trash2, InfoCircle, AlertTriangle } from 'lucide-react';
import StatusBadge from '../../components/common/StatusBadge';

const AgentsList = ({ projectId, region }) => {
  const navigate = useNavigate();
  const [agents, setAgents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteConfirmation, setDeleteConfirmation] = useState(null);
  const [openMenuId, setOpenMenuId] = useState(null);
  
  useEffect(() => {
    const fetchAgents = async () => {
      if (!projectId) {
        setIsLoading(false);
        return;
      }
      
      setIsLoading(true);
      
      try {
        // In a real implementation, this would be an API call
        // Simulate API response
        setTimeout(() => {
          const mockAgents = [
            {
              id: 'agent-1',
              name: 'Customer Service Bot',
              description: 'Handles common customer inquiries and requests',
              framework: 'LANGGRAPH',
              status: 'DEPLOYED',
              environment: 'DEVELOPMENT',
              createdAt: '2025-04-01T10:00:00Z',
              updatedAt: '2025-04-10T12:00:00Z'
            },
            {
              id: 'agent-2',
              name: 'Document Retrieval Agent',
              description: 'Answers questions based on internal documentation',
              framework: 'LANGCHAIN',
              status: 'TESTED',
              environment: 'DEVELOPMENT',
              createdAt: '2025-04-02T15:30:00Z',
              updatedAt: '2025-04-09T15:30:00Z'
            },
            {
              id: 'agent-3',
              name: 'Sales Assistant',
              description: 'Helps with product recommendations',
              framework: 'CREWAI',
              status: 'DRAFT',
              environment: 'DEVELOPMENT',
              createdAt: '2025-04-05T09:15:00Z',
              updatedAt: '2025-04-08T09:15:00Z'
            },
            {
              id: 'agent-4',
              name: 'Product Recommendation',
              description: 'Provides personalized product recommendations',
              framework: 'CUSTOM',
              status: 'FAILED',
              environment: 'DEVELOPMENT',
              createdAt: '2025-04-03T11:45:00Z',
              updatedAt: '2025-04-09T14:20:00Z'
            }
          ];
          
          setAgents(mockAgents);
          setIsLoading(false);
        }, 1000);
      } catch (error) {
        console.error('Error fetching agents:', error);
        setIsLoading(false);
      }
    };
    
    fetchAgents();
  }, [projectId, region]);
  
  const handleDeleteAgent = (agentId) => {
    // In a real implementation, this would be an API call
    setAgents(agents.filter(agent => agent.id !== agentId));
    setDeleteConfirmation(null);
  };
  
  const filteredAgents = agents.filter(agent => 
    agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    agent.description.toLowerCase().includes(searchTerm.toLowerCase())
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
        <h1 className="text-2xl font-bold">Agents</h1>
        <div className="flex gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search agents..."
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button 
            onClick={() => navigate('/agents/create')}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            <Plus size={16} />
            <span>Create Agent</span>
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        {isLoading ? (
          <div className="p-8 text-center">
            <svg className="animate-spin h-8 w-8 text-blue-600 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="text-gray-500">Loading agents...</p>
          </div>
        ) : filteredAgents.length === 0 ? (
          <div className="p-8 text-center">
            {searchTerm ? (
              <p className="text-gray-500">No agents found matching "{searchTerm}"</p>
            ) : (
              <>
                <InfoCircle className="h-12 w-12 text-blue-500 mx-auto mb-4" />
                <p className="mb-4 text-gray-600">No agents found in this project.</p>
                <button
                  onClick={() => navigate('/agents/create')}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Create your first agent
                </button>
              </>
            )}
          </div>
        ) : (
          <>
            <div className="grid grid-cols-12 py-3 px-4 border-b border-gray-200 bg-gray-50 text-sm font-medium text-gray-600">
              <div className="col-span-4">Name</div>
              <div className="col-span-3">Framework</div>
              <div className="col-span-2">Status</div>
              <div className="col-span-2">Last Updated</div>
              <div className="col-span-1 text-right">Actions</div>
            </div>
            
            {filteredAgents.map((agent) => (
              <div 
                key={agent.id} 
                className="grid grid-cols-12 py-4 px-4 border-b border-gray-200 hover:bg-gray-50"
              >
                <div className="col-span-4 flex items-center">
                  <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mr-3">
                    <Cpu size={16} />
                  </div>
                  <div>
                    <Link to={`/agents/${agent.id}`} className="font-medium text-gray-900 hover:text-blue-600">
                      {agent.name}
                    </Link>
                    <p className="text-xs text-gray-500">{agent.description}</p>
                  </div>
                </div>
                <div className="col-span-3 flex items-center">
                  <span className="px-2 py-1 bg-gray-100 rounded text-xs">
                    {agent.framework}
                  </span>
                </div>
                <div className="col-span-2 flex items-center">
                  <StatusBadge status={agent.status} />
                </div>
                <div className="col-span-2 flex items-center text-sm text-gray-600">
                  {new Date(agent.updatedAt).toLocaleDateString()}
                </div>
                <div className="col-span-1 flex items-center justify-end relative">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setOpenMenuId(openMenuId === agent.id ? null : agent.id);
                    }}
                    className="p-1 text-gray-500 hover:text-gray-700 rounded-full hover:bg-gray-100"
                  >
                    <MoreHorizontal size={16} />
                  </button>
                  
                  {openMenuId === agent.id && (
                    <div className="absolute right-0 top-8 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-10">
                      <Link
                        to={`/agents/${agent.id}`}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        View Details
                      </Link>
                      <Link
                        to={`/playground/${agent.id}`}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Test in Playground
                      </Link>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setDeleteConfirmation(agent.id);
                          setOpenMenuId(null);
                        }}
                        className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                      >
                        Delete
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </>
        )}
      </div>
      
      {/* Delete Confirmation Modal */}
      {deleteConfirmation && (
        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true">
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>
            <div className="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
              <div className="sm:flex sm:items-start">
                <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                  <Trash2 className="h-6 w-6 text-red-600" />
                </div>
                <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Delete Agent</h3>
                  <div className="mt-2">
                    <p className="text-sm text-gray-500">
                      Are you sure you want to delete this agent? This action cannot be undone.
                    </p>
                  </div>
                </div>
              </div>
              <div className="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
                  onClick={() => handleDeleteAgent(deleteConfirmation)}
                >
                  Delete
                </button>
                <button
                  type="button"
                  className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:w-auto sm:text-sm"
                  onClick={() => setDeleteConfirmation(null)}
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AgentsList;
