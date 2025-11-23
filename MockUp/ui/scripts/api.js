/**
 * AvenStudio API Client - Vanilla JavaScript
 * Provides access to Python backend via Electron IPC bridge
 */

class AvenStudioAPI {
  constructor() {
    this.isElectron = typeof window !== 'undefined' &&
                      typeof window.api !== 'undefined';

    if (!this.isElectron) {
      console.warn('⚠️ Running in browser mode - using localStorage fallback');
    }
  }

  // ==================== TASKS ====================

  async getTasks(filters = {}) {
    if (this.isElectron) {
      return await window.api.tasks.list(filters);
    } else {
      // Fallback for browser development
      const saved = localStorage.getItem('tasks');
      let tasks = saved ? JSON.parse(saved) : this._getDefaultTasks();

      // Apply filters
      if (filters.status) {
        tasks = tasks.filter(t => t.status === filters.status);
      }
      if (filters.priority) {
        tasks = tasks.filter(t => t.priority === filters.priority);
      }
      if (filters.category) {
        tasks = tasks.filter(t => t.category === filters.category);
      }

      return tasks;
    }
  }

  async createTask(taskData) {
    if (this.isElectron) {
      return await window.api.tasks.create(taskData);
    } else {
      const tasks = await this.getTasks();
      const newTask = {
        id: this._generateId(),
        ...taskData,
        status: taskData.status || 'todo',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
      tasks.push(newTask);
      localStorage.setItem('tasks', JSON.stringify(tasks));
      return newTask;
    }
  }

  async updateTask(id, updates) {
    if (this.isElectron) {
      return await window.api.tasks.update(id, updates);
    } else {
      const tasks = await this.getTasks();
      const index = tasks.findIndex(t => t.id === id);
      if (index === -1) throw new Error('Task not found');

      tasks[index] = {
        ...tasks[index],
        ...updates,
        updatedAt: new Date().toISOString()
      };
      localStorage.setItem('tasks', JSON.stringify(tasks));
      return tasks[index];
    }
  }

  async deleteTask(id) {
    if (this.isElectron) {
      return await window.api.tasks.delete(id);
    } else {
      const tasks = await this.getTasks();
      const filtered = tasks.filter(t => t.id !== id);
      localStorage.setItem('tasks', JSON.stringify(filtered));
    }
  }

  // ==================== STATS ====================

  async getStats() {
    if (this.isElectron) {
      return await window.api.stats.get();
    } else {
      const tasks = await this.getTasks();

      return {
        total_tasks: tasks.length,
        by_status: {
          'todo': tasks.filter(t => t.status === 'todo').length,
          'in-progress': tasks.filter(t => t.status === 'in-progress').length,
          'review': tasks.filter(t => t.status === 'review').length,
          'blocked': tasks.filter(t => t.status === 'blocked').length,
          'done': tasks.filter(t => t.status === 'done').length
        },
        by_priority: {
          'low': tasks.filter(t => t.priority === 'low').length,
          'medium': tasks.filter(t => t.priority === 'medium').length,
          'high': tasks.filter(t => t.priority === 'high').length,
          'urgent': tasks.filter(t => t.priority === 'urgent').length
        },
        by_category: tasks.reduce((acc, task) => {
          acc[task.category] = (acc[task.category] || 0) + 1;
          return acc;
        }, {}),
        completion_rate: tasks.length > 0
          ? Math.round((tasks.filter(t => t.status === 'done').length / tasks.length) * 100)
          : 0,
        overdue: tasks.filter(t => {
          if (!t.dueDate) return false;
          return new Date(t.dueDate) < new Date() && t.status !== 'done';
        }).length
      };
    }
  }

  // ==================== CATEGORIES ====================

  async getCategories() {
    if (this.isElectron) {
      return await window.api.categories.list();
    } else {
      const saved = localStorage.getItem('categories');
      return saved ? JSON.parse(saved) : [
        'planning',
        'design',
        'finance',
        'building',
        'compliance',
        'other'
      ];
    }
  }

  async createCategory(name) {
    if (this.isElectron) {
      return await window.api.categories.create(name);
    } else {
      const categories = await this.getCategories();
      if (!categories.includes(name)) {
        categories.push(name);
        localStorage.setItem('categories', JSON.stringify(categories));
      }
    }
  }

  // ==================== AUTOMATION ====================

  async getAutomationRules() {
    if (this.isElectron) {
      return await window.api.automation.list();
    } else {
      const saved = localStorage.getItem('automation_rules');
      return saved ? JSON.parse(saved) : [];
    }
  }

  async createAutomationRule(rule) {
    if (this.isElectron) {
      return await window.api.automation.create(rule);
    } else {
      const rules = await this.getAutomationRules();
      const newRule = {
        id: this._generateId(),
        ...rule,
        createdAt: new Date().toISOString(),
        triggerCount: 0
      };
      rules.push(newRule);
      localStorage.setItem('automation_rules', JSON.stringify(rules));
      return newRule;
    }
  }

  // ==================== HELPERS ====================

  _generateId() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  _getDefaultTasks() {
    return [
      {
        id: this._generateId(),
        title: 'Submit Planning Application',
        description: 'Complete and submit planning application to local council',
        status: 'in-progress',
        priority: 'high',
        category: 'planning',
        tags: ['legal', 'urgent'],
        dueDate: '2025-12-01',
        completionPercentage: 60,
        createdAt: '2025-11-01T10:00:00Z',
        updatedAt: '2025-11-20T14:30:00Z'
      },
      {
        id: this._generateId(),
        title: 'Foundation Design Review',
        description: 'Review and approve foundation designs from structural engineer',
        status: 'todo',
        priority: 'high',
        category: 'design',
        tags: ['structural', 'engineering'],
        dueDate: '2025-11-28',
        completionPercentage: 0,
        createdAt: '2025-11-15T09:00:00Z',
        updatedAt: '2025-11-15T09:00:00Z'
      },
      {
        id: this._generateId(),
        title: 'Budget Spreadsheet Update',
        description: 'Update project budget with recent quotes',
        status: 'todo',
        priority: 'medium',
        category: 'finance',
        tags: ['budgeting'],
        dueDate: '2025-11-25',
        completionPercentage: 25,
        createdAt: '2025-11-10T11:00:00Z',
        updatedAt: '2025-11-22T16:00:00Z'
      },
      {
        id: this._generateId(),
        title: 'Site Survey Completed',
        description: 'Topographical survey of building site',
        status: 'done',
        priority: 'high',
        category: 'planning',
        tags: ['survey', 'completed'],
        dueDate: '2025-11-15',
        completionPercentage: 100,
        createdAt: '2025-10-20T08:00:00Z',
        updatedAt: '2025-11-14T17:00:00Z'
      },
      {
        id: this._generateId(),
        title: 'Material Selection - Kitchen',
        description: 'Choose tiles, countertops, and cabinetry',
        status: 'review',
        priority: 'medium',
        category: 'design',
        tags: ['interior', 'materials'],
        dueDate: '2025-12-10',
        completionPercentage: 80,
        createdAt: '2025-11-05T10:00:00Z',
        updatedAt: '2025-11-21T13:00:00Z'
      },
      {
        id: this._generateId(),
        title: 'Building Regulations Approval',
        description: 'Waiting on building control approval',
        status: 'blocked',
        priority: 'urgent',
        category: 'compliance',
        tags: ['legal', 'blocked'],
        dueDate: '2025-11-30',
        completionPercentage: 90,
        createdAt: '2025-11-01T09:00:00Z',
        updatedAt: '2025-11-23T10:00:00Z'
      }
    ];
  }
}

// Export singleton instance
window.avenAPI = new AvenStudioAPI();
