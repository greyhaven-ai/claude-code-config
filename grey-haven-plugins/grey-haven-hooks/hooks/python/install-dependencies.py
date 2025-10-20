#!/usr/bin/env python3
"""
Dependency installer for Claude Config Python hooks
Installs only the dependencies needed for the hooks you're using
"""

import subprocess
import sys
import importlib.util
from pathlib import Path

# Define hook dependencies
HOOK_DEPENDENCIES = {
    'test-data-generator.py': {
        'modules': ['faker'],
        'packages': ['faker>=20.0.0'],
        'description': 'Test data generation'
    },
    'db-query-performance-analyzer.py': {
        'modules': ['sqlparse'],
        'packages': ['sqlparse>=0.4.0'],
        'description': 'SQL query analysis'
    },
    '../scripts/claude_repo_optimizer.py': {
        'modules': ['yaml'],
        'packages': ['PyYAML>=6.0'],
        'description': 'Repository optimization'
    }
}

def check_module(module_name):
    """Check if a Python module is installed"""
    spec = importlib.util.find_spec(module_name)
    return spec is not None

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    hooks_dir = Path(__file__).parent
    python_hooks_dir = hooks_dir / 'python'
    scripts_dir = hooks_dir.parent / 'scripts'
    
    print("🔍 Checking Python hook dependencies...\n")
    
    missing_deps = {}
    installed_deps = []
    
    # Check each hook
    for hook_file, info in HOOK_DEPENDENCIES.items():
        # Determine full path
        if hook_file.startswith('../'):
            hook_path = hooks_dir.parent / hook_file[3:]
        else:
            hook_path = python_hooks_dir / hook_file
            
        # Only check if hook file exists
        if hook_path.exists():
            for module in info['modules']:
                if not check_module(module):
                    if hook_file not in missing_deps:
                        missing_deps[hook_file] = info
                else:
                    installed_deps.append(f"✅ {module} (for {info['description']})")
    
    # Show status
    if installed_deps:
        print("Already installed:")
        for dep in installed_deps:
            print(f"  {dep}")
        print()
    
    if not missing_deps:
        print("✨ All dependencies are already installed!")
        return
    
    # Show missing dependencies
    print("Missing dependencies detected:")
    for hook, info in missing_deps.items():
        print(f"  ❌ {hook}: {info['description']}")
        print(f"     Requires: {', '.join(info['modules'])}")
    
    print("\n" + "="*50)
    response = input("Install missing dependencies? (y/n): ").lower().strip()
    
    if response != 'y':
        print("\n⚠️  Some hooks may not work without their dependencies")
        print("You can run this script again later to install them")
        return
    
    # Install missing dependencies
    print("\n📦 Installing dependencies...")
    for hook, info in missing_deps.items():
        for package in info['packages']:
            print(f"  Installing {package}...")
            if install_package(package):
                print(f"  ✅ Installed {package}")
            else:
                print(f"  ❌ Failed to install {package}")
    
    print("\n✨ Dependency installation complete!")
    print("\nNote: These dependencies are optional. The core Claude Config")
    print("functionality works without them. Only specific hooks require them.")

if __name__ == '__main__':
    main()