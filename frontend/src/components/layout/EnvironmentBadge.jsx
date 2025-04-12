import React, { useState, useEffect } from 'react';

const EnvironmentBadge = () => {
  const [environment, setEnvironment] = useState('DEVELOPMENT');
  
  useEffect(() => {
    // In a real implementation, this would fetch from the environment API
    // For now, use the environment variable if available
    const envFromApi = process.env.REACT_APP_ENVIRONMENT;
    if (envFromApi) {
      setEnvironment(envFromApi);
    }
  }, []);
  
  const getEnvironmentStyles = () => {
    switch (environment) {
      case 'PRODUCTION':
        return {
          bgColor: 'bg-red-100',
          textColor: 'text-red-800',
          borderColor: 'border-red-200'
        };
      case 'UAT':
        return {
          bgColor: 'bg-yellow-100',
          textColor: 'text-yellow-800',
          borderColor: 'border-yellow-200'
        };
      case 'DEVELOPMENT':
      default:
        return {
          bgColor: 'bg-green-100',
          textColor: 'text-green-800',
          borderColor: 'border-green-200'
        };
    }
  };
  
  const { bgColor, textColor, borderColor } = getEnvironmentStyles();
  
  return (
    <div className={`ml-4 px-3 py-1 rounded-md ${bgColor} ${textColor} border ${borderColor} text-xs font-medium`}>
      {environment}
    </div>
  );
};

export default EnvironmentBadge;
