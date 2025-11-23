/**
 * Electron Preload Script
 * Bridges React UI to Python backend via IPC
 * Exposes safe API methods to window.api
 */

const { contextBridge } = require('electron');

const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Helper: Make API request
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Request failed [${endpoint}]:`, error);
    throw error;
  }
}

/**
 * Expose API to renderer process
 */
contextBridge.exposeInMainWorld('api', {
  /**
   * Tasks API
   */
  tasks: {
    list: async (filters = {}) => {
      const params = new URLSearchParams();
      if (filters.status) params.append('status', filters.status);
      if (filters.priority) params.append('priority', filters.priority);
      if (filters.category) params.append('category', filters.category);

      const query = params.toString();
      return apiRequest(`/api/tasks${query ? '?' + query : ''}`);
    },

    get: async (id) => {
      return apiRequest(`/api/tasks/${id}`);
    },

    create: async (data) => {
      return apiRequest('/api/tasks', {
        method: 'POST',
        body: JSON.stringify(data)
      });
    },

    update: async (id, data) => {
      return apiRequest(`/api/tasks/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data)
      });
    },

    delete: async (id) => {
      return apiRequest(`/api/tasks/${id}`, {
        method: 'DELETE'
      });
    }
  },

  /**
   * Stats API (for dashboard)
   */
  stats: {
    get: async () => {
      return apiRequest('/api/stats');
    }
  },

  /**
   * Categories API
   */
  categories: {
    list: async () => {
      return apiRequest('/api/categories');
    },

    create: async (name) => {
      return apiRequest('/api/categories', {
        method: 'POST',
        body: JSON.stringify({ name })
      });
    },

    update: async (oldName, newName) => {
      return apiRequest(`/api/categories/${oldName}`, {
        method: 'PUT',
        body: JSON.stringify({ name: newName })
      });
    },

    delete: async (name) => {
      return apiRequest(`/api/categories/${name}`, {
        method: 'DELETE'
      });
    }
  },

  /**
   * Automation Rules API
   */
  automation: {
    list: async () => {
      return apiRequest('/api/automation/rules');
    },

    get: async (id) => {
      return apiRequest(`/api/automation/rules/${id}`);
    },

    create: async (rule) => {
      return apiRequest('/api/automation/rules', {
        method: 'POST',
        body: JSON.stringify(rule)
      });
    },

    update: async (id, rule) => {
      return apiRequest(`/api/automation/rules/${id}`, {
        method: 'PUT',
        body: JSON.stringify(rule)
      });
    },

    delete: async (id) => {
      return apiRequest(`/api/automation/rules/${id}`, {
        method: 'DELETE'
      });
    },

    execute: async (taskId, trigger) => {
      return apiRequest('/api/automation/execute', {
        method: 'POST',
        body: JSON.stringify({ taskId, trigger })
      });
    }
  },

  /**
   * System API
   */
  system: {
    health: async () => {
      return apiRequest('/');
    },

    ping: async () => {
      try {
        await apiRequest('/');
        return true;
      } catch {
        return false;
      }
    }
  }
});

/**
 * Expose environment info
 */
contextBridge.exposeInMainWorld('env', {
  isElectron: true,
  platform: process.platform,
  apiBaseUrl: API_BASE_URL
});

console.log('✅ Preload script loaded - window.api available');
