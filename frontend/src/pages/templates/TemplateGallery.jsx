import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, LayoutTemplate, Filter, ArrowRight, AlertTriangle } from 'lucide-react';

const TemplateGallery = ({ projectId, region }) => {
  const [templates, setTemplates] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFramework, setSelectedFramework] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  
  const frameworks = ['All', 'CUSTOM', 'LANGCHAIN', 'LANGGRAPH', 'CREWAI', 'LLAMAINDEX'];
  const categories = ['All', 'RAG', 'Conversation', 'Multi-agent', 'Basic'];
  
  useEffect(() => {
    const fetchTemplates = async () => {
      setIsLoading(true);
      
      try {
        // In a real implementation, this would be an API call
        // Simulate API response
        setTimeout(() => {
          const mockTemplates = [
            {
              id: 'template-1',
              name: 'RAG Agent',
              description: 'A Retrieval-Augmented Generation agent that can query documents.',
              framework: 'LANGCHAIN',
              category: 'RAG',
              usageCount: 128
            },
            {
              id: 'template-2',
              name: 'Sequential Graph Agent',
              description: 'A sequential conversation agent using LangGraph.',
              framework: 'LANGGRAPH',
              category: 'Conversation',
              usageCount: 97
            },
            {
              id: 'template-3',
              name: 'Research Team',
              description: 'A multi-agent system using CrewAI for research tasks.',
              framework: 'CREWAI',
              category: 'Multi-agent',
              usageCount: 76
            },
            {
              id: 'template-4',
              name: 'Simple Vertex AI Agent',
              description: 'A simple agent using Vertex AI models directly.',
              framework: 'CUSTOM',
              category: 'Basic',
              usageCount: 205
            },
            {
              id: 'template-5',
              name: 'Document Q&A Agent',
              description: 'A document question-answering agent using LlamaIndex.',
              framework: 'LLAMAINDEX',
              category: 'RAG',
              usageCount: 89
            }
          ];
          
          setTemplates(mockTemplates);
          setIsLoading(false);
        }, 1000);
      } catch (error) {
        console.error('Error fetching templates:', error);
        setIsLoading(false);
      }
    };
    
    fetchTemplates();
  }, []);
  
  // Filter templates based on search term and filters
  const filteredTemplates = templates.filter((template) => {
    const matchesSearch = template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         template.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFramework = selectedFramework === 'All' || selectedFramework === '' || 
                            template.framework === selectedFramework;
    
    const matchesCategory = selectedCategory === 'All' || selectedCategory === '' ||
                           template.category === selectedCategory;
    
    return matchesSearch && matchesFramework && matchesCategory;
  });
  
  const resetFilters = () => {
    setSearchTerm('');
    setSelectedFramework('');
    setSelectedCategory('');
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
  
  return (
    <div className="container mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Agent Templates</h1>
        <div className="flex items-center space-x-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search templates..."
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button
            onClick={resetFilters}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-md"
          >
            Reset Filters
          </button>
        </div>
      </div>
      
      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div className="flex items-center mb-4">
          <Filter className="h-5 w-5 text-gray-500 mr-2" />
          <h2 className="text-lg font-medium">Filters</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Framework
            </label>
            <select
              value={selectedFramework}
              onChange={(e) => setSelectedFramework(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {frameworks.map((framework) => (
                <option key={framework} value={framework}>
                  {framework}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Category
            </label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
      
      {/* Templates List */}
      {isLoading ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
          <svg className="animate-spin h-8 w-8 text-blue-600 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p className="text-gray-500">Loading templates...</p>
        </div>
      ) : filteredTemplates.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
          <p className="text-gray-500">No templates found matching your filters.</p>
          <button
            onClick={resetFilters}
            className="mt-4 px-4 py-2 text-sm text-white bg-blue-600 hover:bg-blue-700 rounded-md"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {filteredTemplates.map((template) => (
            <div
              key={template.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
            >
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <span className={`px-2 py-1 rounded text-xs ${
                    template.framework === 'LANGCHAIN' ? 'bg-green-100 text-green-800' :
                    template.framework === 'LANGGRAPH' ? 'bg-blue-100 text-blue-800' :
                    template.framework === 'CREWAI' ? 'bg-purple-100 text-purple-800' :
                    template.framework === 'LLAMAINDEX' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {template.framework}
                  </span>
                  <span className={`px-2 py-1 rounded text-xs bg-gray-100 text-gray-800`}>
                    {template.category}
                  </span>
                </div>
                
                <div className="mb-4">
                  <h3 className="text-lg font-medium mb-2">{template.name}</h3>
                  <p className="text-gray-600 text-sm">{template.description}</p>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-500">
                    {template.usageCount} users
                  </span>
                  <Link
                    to={`/templates/${template.id}`}
                    className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800"
                  >
                    View details
                    <ArrowRight className="ml-1 h-4 w-4" />
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TemplateGallery;
