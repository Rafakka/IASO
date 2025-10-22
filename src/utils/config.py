import yaml
import os
from typing import Dict, Any

class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        default_config = {
            'gateway': {
                'base_url': 'http://localhost:8080',
                'timeout': 30
            },
            'processing': {
                'batch_size': 50,
                'delay_between_messages': 0.5
            },
            'logging': {
                'level': 'INFO',
                'file': 'sms_automation.log'
            }
        }
        
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                user_config = yaml.safe_load(f) or {}
            # Merge with default config
            return self._merge_dicts(default_config, user_config)
        else:
            # Create default config file
            with open(self.config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return default_config
    
    def _merge_dicts(self, dict1: Dict, dict2: Dict) -> Dict:
        """Recursively merge two dictionaries"""
        result = dict1.copy()
        for key, value in dict2.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = self._merge_dicts(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default=None):
        """Get configuration value by key"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default