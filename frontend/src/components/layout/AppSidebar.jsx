import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Cpu, 
  PlayCircle, 
  Database, 
  BarChart3,
  Settings,
  LayoutTemplate,
  Github,
  HelpCircle
} from 'lucide-react';

const AppSidebar = () => {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(`${path}/`);
  };

  const navigationItems = [
    { name: 'Dashboard', icon: LayoutDashboard, path: '/' },
    { name: 'Agents', icon: Cpu, path: '/agents' },
    { name: 'Deployments', icon: Database, path: '/deployments' },
    { name: 'Playground', icon: PlayCircle, path: '/playground' },
    { name: 'Templates', icon: LayoutTemplate, path: '/templates' },
    { name: 'Analytics', icon: BarChart3, path: '/analytics' }
  ];

  const resourceItems = [
    { 
      name: 'Documentation', 
      icon: HelpCircle, 
      path: 'https://github.com/sudsk/agent-fleet/blob/main/README.md',
      external: true
    },
    { 
      name: 'Agent Starter Pack', 
      icon: Github, 
      path: 'https://github.com/GoogleCloudPlatform/agent-starter-pack',
      external: true 
    },
    { 
      name: 'GitHub Repository', 
      icon: Github, 
      path: 'https://github.com/sudsk/agent-fleet',
      external: true 
    }
  ];

  return (
    <div className="w-64 bg-white border-r border-gray-200 hidden md:block">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center">
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
          <h1 className="text-xl font-semibold text-gray-800">AgentFleet.io</h1>
        </div>
        <p className="text-sm text-gray-500 mt-1">Agent Management Plane</p>
      </div>
      
      <nav className="p-4">
        <ul className="space-y-1">
          {navigationItems.map((item) => (
            <li key={item.name}>
              <Link 
                to={item.path} 
                className={`flex items-center py-2 px-4 rounded-md ${
                  isActive(item.path)
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <item.icon className="h-5 w-5 mr-3" />
                <span>{item.name}</span>
              </Link>
            </li>
          ))}
        </ul>
        
        <div className="border-t border-gray-200 my-4 pt-4">
          <h3 className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">Resources</h3>
          <ul className="space-y-1">
            {resourceItems.map((item) => (
              <li key={item.name}>
                {item.external ? (
                  <a 
                    href={item.path} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center py-2 px-4 rounded-md text-gray-700 hover:bg-gray-100"
                  >
                    <item.icon className="h-5 w-5 mr-3" />
                    <span>{item.name}</span>
                  </a>
                ) : (
                  <Link 
                    to={item.path} 
                    className={`flex items-center py-2 px-4 rounded-md ${
                      isActive(item.path)
                        ? 'bg-blue-50 text-blue-600'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <item.icon className="h-5 w-5 mr-3" />
                    <span>{item.name}</span>
                  </Link>
                )}
              </li>
            ))}
          </ul>
        </div>
      </nav>
      
      <div className="absolute bottom-0 w-64 p-4 border-t border-gray-200">
        <Link 
          to="/settings" 
          className="flex items-center py-2 px-4 rounded-md text-gray-700 hover:bg-gray-100"
        >
          <Settings className="h-5 w-5 mr-3" />
          <span>Settings</span>
        </Link>
        <div className="mt-4 text-xs text-gray-500 text-center">
          AgentFleet.io v0.1.0
        </div>
      </div>
    </div>
  );
};

export default AppSidebar;
