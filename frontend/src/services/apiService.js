import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    // You can add auth token here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response || error);
    return Promise.reject(error);
  }
);

// =========== Agent API ===========

export const fetchAgents = async (projectId, region, filters = {}) => {
  try {
    const params = { projectId, region, ...filters };
    const response = await api.get('/agents', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching agents:', error);
    throw error;
  }
};

export const fetchAgentDetails = async (projectId, region, agentId) => {
  try {
    const params = { projectId, region };
    const response = await api.get(`/agents/${agentId}`, { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching agent details:', error);
    throw error;
  }
};

export const createAgent = async (projectId, region, agentData) => {
  try {
    const params = { projectId, region };
    const response = await api.post('/agents', agentData, { params });
    return response.data;
  } catch (error) {
    console.error('Error creating agent:', error);
    throw error;
  }
};

export const updateAgent = async (projectId, region, agentId, agentData) => {
  try {
    const params = { projectId, region };
    const response = await api.put(`/agents/${agentId}`, agentData, { params });
    return response.data;
  } catch (error) {
    console.error('Error updating agent:', error);
    throw error;
  }
};

export const deleteAgent = async (projectId, region, agentId) => {
  try {
    const params = { projectId, region };
    const response = await api.delete(`/agents/${agentId}`, { params });
    return response.data;
  } catch (error) {
    console.error('Error deleting agent:', error);
    throw error;
  }
};

export const testAgent = async (projectId, region, testData) => {
  try {
    const params = { projectId, region };
    const response = await api.post('/playground/test', testData, { params });
    return response.data;
  } catch (error) {
    console.error('Error testing agent:', error);
    throw error;
  }
};

export const deployAgent = async (projectId, region, agentId, deploymentData) => {
  try {
    const params = { projectId, region };
    const response = await api.post(`/agents/${agentId}/deploy`, deploymentData, { params });
    return response.data;
  } catch (error) {
    console.error('Error deploying agent:', error);
    throw error;
  }
};

// =========== Deployment API ===========

export const fetchDeployments = async (projectId, region, filters = {}) => {
  try {
    const params = { projectId, region, ...filters };
    const response = await api.get('/deployments', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching deployments:', error);
    throw error;
  }
};

export const updateDeploymentStatus = async (projectId, region, deploymentId, status) => {
  try {
    const params = { projectId, region };
    const response = await api.put(`/deployments/${deploymentId}/status`, { status }, { params });
    return response.data;
  } catch (error) {
    console.error('Error updating deployment status:', error);
    throw error;
  }
};

// =========== Template API ===========

export const fetchTemplates = async (filters = {}) => {
  try {
    const response = await api.get('/templates', { params: filters });
    return response.data;
  } catch (error) {
    console.error('Error fetching templates:', error);
    throw error;
  }
};

export const fetchTemplateDetails = async (templateId) => {
  try {
    const response = await api.get(`/templates/${templateId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching template details:', error);
    throw error;
  }
};

export const initializeFromTemplate = async (templateId, initData) => {
  try {
    const response = await api.post(`/templates/${templateId}/initialize`, initData);
    return response.data;
  } catch (error) {
    console.error('Error initializing from template:', error);
    throw error;
  }
};

// =========== File API ===========

export const uploadFiles = async (files, sessionId = null) => {
  try {
    const formData = new FormData();
    
    // Add files to form data
    for (const file of files) {
      formData.append('files', file);
    }
    
    // Add session ID if provided
    if (sessionId) {
      formData.append('session_id', sessionId);
    }
    
    const response = await api.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error uploading files:', error);
    throw error;
  }
};

export const fetchSessionFiles = async (sessionId) => {
  try {
    const response = await api.get(`/files/sessions/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching session files:', error);
    throw error;
  }
};

export const deleteSessionFiles = async (sessionId) => {
  try {
    const response = await api.delete(`/files/sessions/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting session files:', error);
    throw error;
  }
};

export default {
  fetchAgents,
  fetchAgentDetails,
  createAgent,
  updateAgent,
  deleteAgent,
  testAgent,
  deployAgent,
  fetchDeployments,
  updateDeploymentStatus,
  fetchTemplates,
  fetchTemplateDetails,
  initializeFromTemplate,
  uploadFiles,
  fetchSessionFiles,
  deleteSessionFiles
};
