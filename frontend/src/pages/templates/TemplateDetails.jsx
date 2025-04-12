import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Code, Download, Send, AlertTriangle, Users, Clock, Star } from 'lucide-react';

const TemplateDetails = ({ projectId, region }) => {
  const { templateId } = useParams();
  const navigate = useNavigate();
  const [template, setTemplate] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isInitializing, setIsInitializing] = useState(false);
  const [projectName, setProjectName] = useState('');
  
  useEffect(() => {
    const fetchTemplateDetails = async () => {
      setIsLoading(true);
      
      try {
        // In a real implementation, this would be an API call
        // Simulate API response with a delay
        setTimeout(() => {
          const mockTemplate = {
            id: templateId,
            name: templateId === 'template-1' ? 'RAG Agent' :
                 templateId === 'template-2' ? 'Sequential Graph Agent' :
                 templateId === 'template-3' ? 'Research Team' :
                 templateId === 'template-4' ? 'Simple Vertex AI Agent' :
                 templateId === 'template-5' ? 'Document Q&A Agent' : 'Unknown Template',
            description: templateId === 'template-1' ? 'A Retrieval-Augmented Generation agent that can query documents.' :
                         templateId === 'template-2' ? 'A sequential conversation agent using LangGraph.' :
                         templateId === 'template-3' ? 'A multi-agent system using CrewAI for research tasks.' :
                         templateId === 'template-4' ? 'A simple agent using Vertex AI models directly.' :
                         templateId === 'template-5' ? 'A document question-answering agent using LlamaIndex.' : 'Template description',
            framework: templateId === 'template-1' ? 'LANGCHAIN' :
                      templateId === 'template-2' ? 'LANGGRAPH' :
                      templateId === 'template-3' ? 'CREWAI' :
                      templateId === 'template-4' ? 'CUSTOM' :
                      templateId === 'template-5' ? 'LLAMAINDEX' : 'CUSTOM',
            category: templateId === 'template-1' ? 'RAG' :
                     templateId === 'template-2' ? 'Conversation' :
                     templateId === 'template-3' ? 'Multi-agent' :
                     templateId === 'template-4' ? 'Basic' :
                     templateId === 'template-5' ? 'RAG' : 'Other',
            usageCount: templateId === 'template-1' ? 128 :
                       templateId === 'template-2' ? 97 :
                       templateId === 'template-3' ? 76 :
                       templateId === 'template-4' ? 205 :
                       templateId === 'template-5' ? 89 : 50,
            createdAt: '2025-01-15T10:00:00Z',
            lastUpdated: '2025-03-30T15:30:00Z',
            rating: 4.7,
            requirements: ['google-cloud-aiplatform>=1.36.0'],
            files: [
              {
                name: 'main.py',
                content: `# Main agent code\n\nimport os\nfrom vertexai.generative_models import GenerativeModel\n\ndef run_agent(query):\n    # Initialize the model\n    model = GenerativeModel("gemini-1.5-pro")\n    \n    # Generate response\n    response = model.generate_content(query)\n    \n    # Return the response text\n    return response.text\n`
              },
              {
                name: 'requirements.txt',
                content: 'google-cloud-aiplatform>=1.36.0\nvertexai>=0.0.1'
              },
              {
                name: 'config.yaml',
                content: `# Agent configuration\nmodel: gemini-1.5-pro\ntemperature: 0.2\nmax_output_tokens: 1024\n`
              }
            ]
          };
          
          setTemplate(mockTemplate);
          setIsLoading(false);
        }, 1000);
      } catch (error) {
        console.error('Error fetching template details:', error);
        setIsLoading(false);
      }
    };
    
    fetchTemplateDetails();
  }, [templateId]);
  
  const handleInitializeProject = async () => {
    if (!projectName || !projectId) return;
    
    setIsInitializing(true);
    
    try {
      // In a real implementation, this would be an API call
      // Simulate API response with a delay
      setTimeout(() => {
        // Navigate to the agents list after successful initialization
        navigate('/agents');
      }, 2000);
    } catch (error) {
      console.error('Error initializing project:', error);
      setIsInitializing(false);
    }
  };
  
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
  
  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center items-center h-64">
          <svg className="animate-spin h-8 w-8 text-blue-600 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>Loading template details...</span>
        </div>
      </div>
    );
  }
  
  if (!template) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Error: </strong>
          <span className="block sm:inline">Template not found</span>
        </div>
        <div className="mt-4">
          <Link to="/templates" className="text-blue-600 hover:text-blue-800">
            <ArrowLeft className="inline mr-2 h-4 w-4" />
            Back to Templates
          </Link>
        </div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link to="/templates" className="text-blue-600 hover:text-blue-800 inline-flex items-center">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Templates
        </Link>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Column - Template Info */}
        <div className="md:col-span-2">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <div className="flex items-center mb-2">
                    <span className={`px-2 py-1 rounded text-xs mr-2 ${
                      template.framework === 'LANGCHAIN' ? 'bg-green-100 text-green-800' :
                      template.framework === 'LANGGRAPH' ? 'bg-blue-100 text-blue-800' :
                      template.framework === 'CREWAI' ? 'bg-purple-100 text-purple-800' :
                      template.framework === 'LLAMAINDEX' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {template.framework}
                    </span>
                    <span className="px-2 py-1 rounded text-xs bg-gray-100 text-gray-800">
                      {template.category}
                    </span>
                  </div>
                  <h1 className="text-2xl font-bold">{template.name}</h1>
                </div>
                <div className="flex items-center">
                  <Star className="h-5 w-5 text-yellow-400 mr-1" />
                  <span className="font-medium">{template.rating.toFixed(1)}</span>
                </div>
              </div>
              
              <p className="text-gray-600 mb-6">{template.description}</p>
              
              <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="flex items-center">
                  <Users className="h-5 w-5 text-gray-400 mr-2" />
                  <div>
                    <p className="text-sm text-gray-500">Users</p>
                    <p className="font-medium">{template.usageCount}</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <Clock className="h-5 w-5 text-gray-400 mr-2" />
                  <div>
                    <p className="text-sm text-gray-500">Last Updated</p>
                    <p className="font-medium">{new Date(template.lastUpdated).toLocaleDateString()}</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <Code className="h-5 w-5 text-gray-400 mr-2" />
                  <div>
                    <p className="text-sm text-gray-500">Files</p>
                    <p className="font-medium">{template.files.length}</p>
                  </div>
                </div>
              </div>
              
              <div className="mb-6">
                <h2 className="text-lg font-medium mb-2">Requirements</h2>
                <div className="bg-gray-50 p-4 rounded-md">
                  <ul className="list-disc list-inside space-y-1">
                    {template.requirements.map((req, index) => (
                      <li key={index} className="text-sm text-gray-700">{req}</li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <div>
                <h2 className="text-lg font-medium mb-2">Source Files</h2>
                {template.files.map((file, index) => (
                  <div key={index} className="mb-4">
                    <div className="flex justify-between items-center mb-2">
                      <div className="font-medium">{file.name}</div>
                      <button className="text-sm text-blue-600 hover:text-blue-800 flex items-center">
                        <Download className="h-4 w-4 mr-1" />
                        Download
                      </button>
                    </div>
                    <div className="bg-gray-800 text-white p-4 rounded-md overflow-x-auto">
                      <pre className="text-sm font-mono">{file.content}</pre>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
        
        {/* Right Column - Initialize Project */}
        <div className="md:col-span-1">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 sticky top-6">
            <h2 className="text-lg font-medium mb-4">Initialize Project</h2>
            <p className="text-sm text-gray-600 mb-4">
              Create a new agent project from this template.
            </p>
            
            <form onSubmit={(e) => { e.preventDefault(); handleInitializeProject(); }}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Project Name
                </label>
                <input
                  type="text"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  placeholder="my-agent-project"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Google Cloud Project
                </label>
                <input
                  type="text"
                  value={projectId}
                  disabled
                  className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
                />
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Region
                </label>
                <input
                  type="text"
                  value={region}
                  disabled
                  className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
                />
              </div>
              
              <button
                type="submit"
                disabled={!projectName || isInitializing}
                className="w-full flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {isInitializing ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Initializing...
                  </>
                ) : (
                  <>
                    <Send className="mr-2 h-4 w-4" />
                    Initialize Project
                  </>
                )}
              </button>
            </form>
            
            <div className="mt-4 text-xs text-gray-500">
              <p>This will:</p>
              <ul className="list-disc list-inside space-y-1 mt-1">
                <li>Create a new agent from this template</li>
                <li>Set up the agent in your project</li>
                <li>Allow you to customize and deploy it</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TemplateDetails;
