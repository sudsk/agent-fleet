import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import EnvironmentBadge from './EnvironmentBadge';
import ProjectSelector from '../common/ProjectSelector';

const AppHeader = ({ projectId, region, updateProjectSettings }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  return (
    <header className="bg-white border-b border-gray-200 py-4 px-6 flex justify-between items-center">
      <div className="flex items-center">
        <Link to="/" className="flex items-center">
          <svg 
            className="h-8 w-8 text-blue-600 mr-2" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2" 
            strokeLinecap="round" 
            strokeLinejoin="round"
          >
            <path d="M12 2a10 10 0 1 0 10 10H12V2z" />
            <path d="M12 2a10 10 0 0 1 10 10H12V2z" />
            <circle cx="12" cy="12" r="4" />
          </svg>
          <h2 className="text-lg font-semibold text-gray-800 hidden md:block">AgentFleet.io</h2>
        </Link>
        <EnvironmentBadge />
        <button 
          className="md:hidden text-gray-500 hover:text-gray-700 ml-4"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>
      
      <div className="flex items-center space-x-4">
        <ProjectSelector 
          projectId={projectId}
          region={region}
          updateProjectSettings={updateProjectSettings}
        />
        <div className="hidden md:flex items-center space-x-2">
          <a 
            href="https://github.com/sudsk/agent-fleet"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-500 hover:text-gray-700"
          >
            <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
              <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.167 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.343-3.369-1.343-.454-1.155-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.272.098-2.65 0 0 .84-.269 2.75 1.025A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.025 2.747-1.025.546 1.378.203 2.397.1 2.65.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.933.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12c0-5.523-4.477-10-10-10z" />
            </svg>
          </a>
          <div className="h-6 w-px bg-gray-300"></div>
          <div className="relative">
            <button className="relative w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-700">
              <span>U</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default AppHeader;
