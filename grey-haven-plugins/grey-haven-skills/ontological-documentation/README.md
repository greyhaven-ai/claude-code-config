# Ontological Documentation Skill

This skill provides comprehensive tools and templates for creating ontological documentation of software systems.

## Directory Structure

```
ontological-documentation/
├── SKILL.md                    # Main skill definition
├── README.md                   # This file
├── references/                 # Reference guides
│   ├── concept_extraction_guide.md
│   ├── documentation_templates.md
│   └── ontology_patterns.md
├── scripts/                    # Utility scripts
│   ├── extract_concepts.py
│   └── generate_ontology_diagram.py
└── assets/                     # Examples and templates
    ├── examples/
    │   └── ecommerce-ontology.md
    └── ontology-templates/
        └── domain-ontology.md
```

## What's Included

### Reference Guides

- **concept_extraction_guide.md**: Methodologies for extracting domain concepts from codebases
- **documentation_templates.md**: Standardized templates for documenting concepts and relationships
- **ontology_patterns.md**: Common patterns and best practices for ontological documentation

### Scripts

- **extract_concepts.py**: Automated concept extraction from Python and JavaScript/TypeScript code
- **generate_ontology_diagram.py**: Generate Mermaid, PlantUML, GraphViz, and JSON-LD diagrams

### Examples & Templates

- **ecommerce-ontology.md**: Complete example of e-commerce domain ontology
- **domain-ontology.md**: Template for documenting new domain ontologies

## Usage

This skill activates automatically when working on:
- Domain modeling and architecture documentation
- Creating conceptual frameworks
- Extracting and documenting business concepts from code
- Building knowledge graphs and semantic models

## Quick Start

1. Read [SKILL.md](SKILL.md) for the full skill definition
2. Review the [concept extraction guide](references/concept_extraction_guide.md)
3. Use the [templates](references/documentation_templates.md) for your documentation
4. Check the [e-commerce example](assets/examples/ecommerce-ontology.md) for inspiration

## Scripts Usage

### Extract Concepts
```bash
python scripts/extract_concepts.py /path/to/codebase
```

### Generate Diagrams
```bash
python scripts/generate_ontology_diagram.py ontology.json --format mermaid
```
