#!/usr/bin/env python3
# Copyright 2025 Vantage Compute Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Generate API documentation from Python SDK docstrings.

This script generates markdown documentation from the cudo_compute_sdk module
for use in the Docusaurus documentation site.
"""

import ast
import inspect
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent directory to path to import SDK
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from cudo_compute_sdk import CudoComputeSDK
    from cudo_compute_sdk import schema
except ImportError as e:
    print(f"Error importing SDK: {e}")
    print("Make sure the SDK is installed or the path is correct")
    sys.exit(1)


def get_method_signature(method) -> str:
    """Get formatted method signature."""
    try:
        sig = inspect.signature(method)
        return str(sig)
    except (ValueError, TypeError):
        return "()"


def extract_docstring_parts(docstring: Optional[str]) -> Dict[str, Any]:
    """Extract parts from a docstring (summary, args, returns, examples)."""
    if not docstring:
        return {"summary": "", "args": [], "returns": "", "examples": []}
    
    lines = docstring.strip().split("\n")
    summary = []
    args = []
    returns = []
    examples = []
    current_section = "summary"
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("Args:"):
            current_section = "args"
            continue
        elif line.startswith("Returns:"):
            current_section = "returns"
            continue
        elif line.startswith("Example:") or line.startswith("Examples:"):
            current_section = "examples"
            continue
        elif line.startswith("Raises:"):
            current_section = "raises"
            continue
        
        if current_section == "summary" and line:
            summary.append(line)
        elif current_section == "args" and line:
            args.append(line)
        elif current_section == "returns" and line:
            returns.append(line)
        elif current_section == "examples" and line:
            examples.append(line)
    
    return {
        "summary": " ".join(summary),
        "args": args,
        "returns": " ".join(returns),
        "examples": examples,
    }


def generate_sdk_class_docs() -> str:
    """Generate documentation for the main CudoComputeSDK class."""
    output = []
    
    output.append("---")
    output.append("title: SDK API Documentation")
    output.append("description: Auto-generated API documentation from SDK docstrings")
    output.append("---")
    output.append("")
    output.append("# SDK API Documentation")
    output.append("")
    output.append("This documentation is auto-generated from the SDK source code docstrings.")
    output.append("")
    output.append("## CudoComputeSDK")
    output.append("")
    
    # Add class docstring
    if CudoComputeSDK.__doc__:
        output.append(CudoComputeSDK.__doc__.strip())
        output.append("")
    
    # Get all public methods
    methods = [
        (name, method)
        for name, method in inspect.getmembers(CudoComputeSDK, predicate=inspect.isfunction)
        if not name.startswith("_") and name != "close"
    ]
    
    # Group methods by category
    categories = {
        "Projects": ["list_projects", "get_project", "create_project", "delete_project"],
        "Virtual Machines": [
            "list_vms", "get_vm", "create_vm", "start_vm", "stop_vm", 
            "restart_vm", "terminate_vm"
        ],
        "Data Centers": [
            "list_data_centers", "get_data_center", 
            "list_machine_types_for_data_center"
        ],
        "Images": ["list_images"],
        "Networks": ["list_networks", "create_network", "delete_network"],
        "Security Groups": [
            "list_security_groups", "create_security_group",
            "create_security_group_rule", "delete_security_group"
        ],
        "SSH Keys": ["list_ssh_keys", "create_ssh_key", "delete_ssh_key"],
        "Storage": [
            "list_disks", "create_disk", "attach_disk_to_vm",
            "detach_disk_from_vm", "delete_disk"
        ],
    }
    
    for category, method_names in categories.items():
        output.append(f"### {category}")
        output.append("")
        
        for method_name in method_names:
            # Find the method in the list
            method_obj = next((m for n, m in methods if n == method_name), None)
            if not method_obj:
                continue
            
            # Get signature and docstring
            sig = get_method_signature(method_obj)
            docstring = inspect.getdoc(method_obj)
            parts = extract_docstring_parts(docstring)
            
            # Method header
            output.append(f"#### `{method_name}{sig}`")
            output.append("")
            
            # Summary
            if parts["summary"]:
                output.append(parts["summary"])
                output.append("")
            
            # Args
            if parts["args"]:
                output.append("**Parameters:**")
                output.append("")
                for arg in parts["args"]:
                    output.append(f"- {arg}")
                output.append("")
            
            # Returns
            if parts["returns"]:
                output.append("**Returns:**")
                output.append("")
                output.append(parts["returns"])
                output.append("")
            
            # Examples
            if parts["examples"]:
                output.append("**Example:**")
                output.append("")
                output.append("```python")
                for example in parts["examples"]:
                    output.append(example)
                output.append("```")
                output.append("")
            
            output.append("---")
            output.append("")
    
    return "\n".join(output)


def generate_schema_docs() -> str:
    """Generate documentation for schema/data models."""
    output = []
    
    output.append("---")
    output.append("title: Data Models")
    output.append("description: Schema and data model documentation")
    output.append("---")
    output.append("")
    output.append("# Data Models")
    output.append("")
    output.append("Pydantic models used for API requests and responses.")
    output.append("")
    
    # Get all classes from schema module that are defined in the schema module
    models = [
        (name, obj)
        for name, obj in inspect.getmembers(schema, predicate=inspect.isclass)
        if not name.startswith("_") and obj.__module__ == "cudo_compute_sdk.schema"
    ]
    
    # Sort by name
    models.sort(key=lambda x: x[0])
    
    for name, model in models:
        output.append(f"## {name}")
        output.append("")
        
        # Add docstring if available, clean up internal markdown links
        if model.__doc__:
            docstring = model.__doc__.strip()
            # Remove lines with internal pydantic documentation links
            lines = docstring.split("\n")
            cleaned_lines = []
            for line in lines:
                # Skip lines with markdown links to non-existent paths
                if "[" in line and "](" in line and ("../concepts/" in line or "../api/" in line):
                    continue
                # Skip lines with !!! admonitions
                if line.strip().startswith("!!!"):
                    continue
                cleaned_lines.append(line)
            docstring = "\n".join(cleaned_lines).strip()
            if docstring:
                output.append(docstring)
                output.append("")
        
        # Try to get fields from Pydantic model
        try:
            if hasattr(model, "model_fields"):
                fields = model.model_fields
                if fields:
                    output.append("**Fields:**")
                    output.append("")
                    for field_name, field_info in fields.items():
                        field_type = field_info.annotation if hasattr(field_info, 'annotation') else 'Any'
                        output.append(f"- `{field_name}`: {field_type}")
                    output.append("")
        except:
            pass
        
        output.append("---")
        output.append("")
    
    return "\n".join(output)


def main():
    """Generate all API documentation."""
    docs_dir = Path(__file__).parent.parent / "docs" / "api"
    docs_dir.mkdir(exist_ok=True)
    
    # Generate SDK class docs
    print("Generating SDK class documentation...")
    sdk_docs = generate_sdk_class_docs()
    sdk_docs_path = docs_dir / "sdk-methods.md"
    sdk_docs_path.write_text(sdk_docs)
    print(f"✓ Written to {sdk_docs_path}")
    
    # Generate schema docs
    print("Generating schema documentation...")
    schema_docs = generate_schema_docs()
    schema_docs_path = docs_dir / "data-models.md"
    schema_docs_path.write_text(schema_docs)
    print(f"✓ Written to {schema_docs_path}")
    
    print("\n✓ API documentation generated successfully!")


if __name__ == "__main__":
    main()
