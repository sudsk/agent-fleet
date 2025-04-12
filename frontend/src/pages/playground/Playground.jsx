import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Send, Paperclip, Bot, FileUp, AlertTriangle } from 'lucide-react';

const Playground = ({ projectId, region }) => {
  const { agentId } = useParams();
  const [agent, setAgent] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingAgent, setIsLoadingAgent] = useState(agentId ? true : false);
  const [files, setFiles] = useState([]);
  const messagesEndRef = useRef(null);
  
  // Fetch agent details if agentId is provided
  useEffect(() => {
    const fetchAgentDetails = async () => {
      if (!agentId || !projectId) return;
      
      setIsLoadingAgent(true);
      
      try {
        // In a real implementation, this would be an API call
        // Mock API response
        setTimeout(() => {
          const mockAgent = {
            id: agentId,
            name: agentId === 'agent-1' ? 'Customer Service Bot' : 
                 agentId === 'agent-2' ? 'Document Retrieval Agent' : 
                 agentId === 'agent-3' ? 'Sales Assistant' : 'Test Agent',
            description: 'Agent for testing in the playground',
            framework: agentId === 'agent-1' ? 'LANGGRAPH' : 
                      agentId === 'agent-2' ? 'LANGCHAIN' : 
                      agentId === 'agent-3' ? 'CREWAI' : 'CUSTOM',
            status: 'DEPLOYED'
          };
          
          setAgent(mockAgent);
          
          // Add a welcome message
          setMessages([
            {
              role: 'assistant',
              content: `Hi! I'm ${mockAgent.name}. How can I help you today?`
            }
          ]);
          
          setIsLoadingAgent(false);
        }, 1000);
      } catch (error) {
        console.error('Error fetching agent:', error);
        setIsLoadingAgent(false);
      }
    };
    
    fetchAgentDetails();
  }, [agentId, projectId]);
  
  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleSendMessage = async () => {
    if (!input.trim()) return;
    
    // Add user message
    setMessages([...messages, { role: 'user', content: input }]);
    
    // Clear input
    setInput('');
    
    // Simulate API request
    setIsLoading(true);
    
    try {
      // In a real implementation, this would be an API call
      // Mock API response with a delay
      setTimeout(() => {
        const mockResponse = {
          textResponse: generateAgentResponse(input, agent?.framework || 'CUSTOM', files)
        };
        
        // Add agent response
        setMessages(prev => [...prev, { role: 'assistant', content: mockResponse.textResponse }]);
        setIsLoading(false);
      }, 2000);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        role: 'system', 
        content: 'Sorry, there was an error processing your request.' 
      }]);
      setIsLoading(false);
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };
  
  const handleFileUpload = (e) => {
    const uploadedFiles = Array.from(e.target.files);
    setFiles([...files, ...uploadedFiles]);
    
    // Add system message about uploaded files
    setMessages([...messages, { 
      role: 'system', 
      content: `Uploaded ${uploadedFiles.length} file(s): ${uploadedFiles.map(f => f.name).join(', ')}` 
    }]);
  };
  
  // Helper function to generate responses based on framework
  const generateAgentResponse = (query, framework, files) => {
    let response = '';
    
    // Base response
    if (query.toLowerCase().includes('hello') || query.toLowerCase().includes('hi')) {
      response = 'Hello! How can I assist you today?';
    } else if (query.toLowerCase().includes('help')) {
      response = 'I can help you with information, answer questions, and assist with various tasks. What do you need help with?';
    } else {
      response = `I've processed your request: "${query}"\n\nIs there anything else you'd like to know?`;
    }
    
    // Framework-specific additions
    if (framework === 'LANGCHAIN') {
      response += '\n\nI used my tools to search for the most relevant information for you.';
    } else if (framework === 'LANGGRAPH') {
      response += '\n\nI processed your request through multiple steps in my reasoning graph.';
    } else if (framework === 'CREWAI') {
      response += '\n\nMy team of specialized agents collaborated to provide this answer.';
    }
    
    // Add file reference if files are present
    if (files && files.length > 0) {
      response += `\n\nI've analyzed the ${files.length} file(s) you uploaded and incorporated relevant information into my response.`;
    }
    
    return response;
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
  
  if (isLoadingAgent) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center items-center h-64">
          <svg className="animate-spin h-8 w-8 text-blue-600 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>Loading agent...</span>
        </div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Agent Playground</h1>
        {!agentId && (
          <Link
            to="/agents"
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
          >
            Select Agent
          </Link>
        )}
      </div>
      
      {agent && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <div className="flex items-center">
            <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mr-3">
              <Bot size={20} />
            </div>
            <div>
              <h2 className="font-semibold text-lg">{agent.name}</h2>
              <p className="text-sm text-gray-600">
                <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs mr-2">
                  {agent.framework}
                </span>
                {agent.description}
              </p>
            </div>
          </div>
        </div>
      )}
      
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col h-[calc(100vh-12rem)]">
        {/* Messages Area */}
        <div className="flex-1 p-4 overflow-y-auto" style={{ scrollBehavior: 'smooth' }}>
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center text-gray-400">
              <div className="text-center">
                <Bot className="h-16 w-16 mx-auto mb-4" />
                {agentId ? (
                  <p>Start chatting with this agent</p>
                ) : (
                  <p>Select an agent from the agents page or start typing</p>
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-md px-4 py-3 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-blue-100 text-blue-800'
                        : message.role === 'system'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
        
        {/* Input Area */}
        <div className="border-t border-gray-200 p-4">
          {files.length > 0 && (
            <div className="mb-2 flex flex-wrap">
              {files.map((file, index) => (
                <div key={index} className="mr-2 mb-2 bg-blue-50 text-blue-700 px-2 py-1 rounded-full text-xs flex items-center">
                  <FileUp size={12} className="mr-1" />
                  {file.name}
                  <button
                    className="ml-1 text-blue-500 hover:text-blue-700"
                    onClick={() => {
                      setFiles(files.filter((_, i) => i !== index));
                    }}
                  >
                    &times;
                  </button>
                </div>
              ))}
            </div>
          )}
          
          <div className="flex items-center">
            <label className="p-2 text-gray-500 hover:text-blue-500 rounded-md hover:bg-gray-100 cursor-pointer">
              <Paperclip size={20} />
              <input
                type="file"
                multiple
                className="hidden"
                onChange={handleFileUpload}
              />
            </label>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={!input.trim() || isLoading}
              className="ml-2 p-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {isLoading ? (
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <Send size={20} />
              )}
            </button>
          </div>
        </div>
      </div>
      
      <div className="mt-6 bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <h3 className="text-sm font-medium mb-2">Agent Playground Help</h3>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• Use the playground to test your agents before deployment</li>
          <li>• Upload files to test document processing capabilities</li>
          <li>• All interactions in the playground are ephemeral and not stored</li>
        </ul>
      </div>
    </div>
  );
};

export default Playground;
