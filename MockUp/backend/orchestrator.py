"""
Core Orchestrator
Routes requests to appropriate modules
"""

import os
import sys
from typing import Dict, Any

# Import data layer
from data.sqlite_layer import SQLiteDataLayer

# Import modules
from modules.tasks.handlers import TasksModule
from modules.stats.handlers import StatsModule
from modules.categories.handlers import CategoriesModule
from modules.automation.handlers import AutomationModule


class Orchestrator:
    """
    Core orchestrator for AvenStudio
    Routes all requests to appropriate modules
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize orchestrator with configuration"""
        self.config = config
        self.modules = {}

        # Initialize data layer
        if config['db_type'] == 'sqlite':
            self.data_layer = SQLiteDataLayer(config['db_path'])
            print(f"✅ SQLite data layer initialized")
        else:
            raise ValueError(f"Unsupported database type: {config['db_type']}")

        # Initialize database schema
        self.data_layer.initialize_schema()

        # Register modules
        self._register_modules()

    def _register_modules(self):
        """Discover and register all modules"""
        print("📦 Registering modules...")

        self.modules['tasks'] = TasksModule()
        print("  ✓ Tasks module")

        self.modules['stats'] = StatsModule()
        print("  ✓ Stats module")

        self.modules['categories'] = CategoriesModule()
        print("  ✓ Categories module")

        self.modules['automation'] = AutomationModule()
        print("  ✓ Automation module")

        print(f"✅ {len(self.modules)} modules registered")

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route request to appropriate module

        Args:
            request: {
                'module': str,
                'action': str,
                'id': Optional[str],
                'data': Optional[dict],
                'filters': Optional[dict]
            }

        Returns:
            {
                'success': bool,
                'data': Any,
                'error': Optional[str]
            }
        """
        module_name = request.get('module')

        # Check if module exists
        if module_name not in self.modules:
            return {
                'success': False,
                'error': f"Module '{module_name}' not found"
            }

        # Get module
        module = self.modules[module_name]

        # Handle request
        try:
            result = module.handle(request, self.data_layer)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
