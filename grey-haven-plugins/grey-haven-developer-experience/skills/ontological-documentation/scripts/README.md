# Ontological Documentation Scripts

This directory contains utility scripts for automated concept extraction and diagram generation.

## Scripts

### extract_concepts.py

Analyzes codebases to extract domain concepts, entities, and relationships for building ontological documentation.

**Features:**
- Supports Python and JavaScript/TypeScript
- Extracts classes, functions, inheritance relationships, and imports
- Builds ontological structure with relationships (is_a, part_of, depends_on, associates_with)
- Generates JSON ontology representation
- Creates Mermaid diagrams

**Usage:**
```bash
# Analyze a single file
python extract_concepts.py /path/to/file.py

# Analyze a directory
python extract_concepts.py /path/to/codebase

# Save output to file
python extract_concepts.py /path/to/codebase > ontology.json
```

**Output:**
- JSON ontology structure
- Mermaid diagram representation

### generate_ontology_diagram.py

Generates visual representations of ontologies in various formats.

**Features:**
- Supports multiple diagram formats (Mermaid, PlantUML, GraphViz DOT, JSON-LD)
- Customizable relationship symbols
- Semantic web compatibility (JSON-LD output)
- Styled diagrams with concept type differentiation

**Usage:**
```bash
# Generate all formats
python generate_ontology_diagram.py ontology.json

# Generate specific format
python generate_ontology_diagram.py ontology.json --format mermaid

# Specify output directory
python generate_ontology_diagram.py ontology.json --output ./diagrams

# Available formats: mermaid, plantuml, dot, json-ld, all
```

**Output Examples:**

Mermaid:
```bash
python generate_ontology_diagram.py ontology.json --format mermaid
# Creates: ontology_mermaid.md
```

PlantUML:
```bash
python generate_ontology_diagram.py ontology.json --format plantuml
# Creates: ontology_plantuml.puml
```

GraphViz DOT:
```bash
python generate_ontology_diagram.py ontology.json --format dot
# Creates: ontology.dot
```

JSON-LD:
```bash
python generate_ontology_diagram.py ontology.json --format json-ld
# Creates: ontology_jsonld.json
```

## Requirements

Both scripts use only Python standard library modules:
- `ast` - Python AST parsing
- `re` - Regular expressions
- `json` - JSON processing
- `pathlib` - Path handling
- `argparse` - Command-line argument parsing

No additional dependencies required!

## Example Workflow

```bash
# 1. Extract concepts from codebase
python extract_concepts.py /path/to/codebase > ontology.json

# 2. Generate diagrams
python generate_ontology_diagram.py ontology.json --output ./docs/diagrams

# 3. Review generated documentation
ls ./docs/diagrams/
# ontology_mermaid.md
# ontology_plantuml.puml
# ontology.dot
# ontology_jsonld.json
```

## Integration with Skill

These scripts support the main [SKILL.md](../SKILL.md) by providing automated tools for concept extraction and visualization. Use them to bootstrap your ontological documentation process.
