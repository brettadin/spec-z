"""
Provenance tracking system for reproducibility
"""
from datetime import datetime
from typing import List, Dict, Any
import yaml
import json


class ProvenanceTracker:
    """
    Track operations and transformations for reproducibility.
    """
    
    def __init__(self):
        """Initialize provenance tracker."""
        self.records: List[Dict[str, Any]] = []
    
    def add_record(self, operation: str, details: Dict[str, Any]):
        """
        Add a provenance record.
        
        Args:
            operation: Name of the operation
            details: Dictionary with operation details
        """
        record = {
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.records.append(record)
    
    def export_yaml(self, filename: str):
        """Export provenance to YAML file."""
        with open(filename, 'w') as f:
            yaml.dump({"provenance": self.records}, f, default_flow_style=False)
    
    def export_json(self, filename: str):
        """Export provenance to JSON file."""
        with open(filename, 'w') as f:
            json.dump({"provenance": self.records}, f, indent=2)
    
    def get_summary(self) -> str:
        """Get a text summary of provenance."""
        lines = ["Provenance History:", "=" * 50]
        for i, record in enumerate(self.records, 1):
            lines.append(f"\n{i}. {record['operation']} at {record['timestamp']}")
            for key, value in record['details'].items():
                lines.append(f"   - {key}: {value}")
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        return f"ProvenanceTracker(n_records={len(self.records)})"
