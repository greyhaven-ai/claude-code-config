---
allowed-tools: Bash, Read
description: List knowledge base entries with filtering options
argument-hint: [type] [--recent] [--orphaned]
---
List knowledge entries: $ARGUMENTS

<context>
Display knowledge base entries with filtering, sorting, and summary statistics.
</context>

<actions>
```bash
# Parse arguments
TYPE=""
FILTER=""

if [[ "$ARGUMENTS" =~ --recent ]]; then
    FILTER="-mtime -7"
fi

if [[ "$ARGUMENTS" =~ --orphaned ]]; then
    # Show entries with no ontological relations
    echo "🔍 Finding orphaned entries..."
    for file in .claude/kb/*/*.md; do
        relations=$(grep -c "\[\[.*\]\]" "$file" 2>/dev/null || echo 0)
        if [ "$relations" -eq 0 ]; then
            title=$(grep "^title:" "$file" | cut -d'"' -f2)
            echo "  📄 $title"
            echo "     Path: $file"
        fi
    done
    exit 0
fi

# Extract type filter
if [[ "$ARGUMENTS" =~ (metadata|debug_history|qa|code_index|patterns|plans|cheatsheets|memory_anchors|other) ]]; then
    TYPE="${BASH_REMATCH[1]}"
fi

# List entries
if [ -n "$TYPE" ]; then
    echo "📚 Knowledge Base: $TYPE"
    find .claude/kb/$TYPE -name "*.md" $FILTER -type f | while read file; do
        title=$(grep "^title:" "$file" | cut -d'"' -f2)
        updated=$(grep "^updated_at:" "$file" | cut -d'"' -f2 | cut -d'T' -f1)
        tags=$(grep "tags:" "$file" -A 5 | grep "  - " | head -3 | sed 's/  - //' | tr '\n' ', ' | sed 's/,$//')
        echo "  📄 $title"
        echo "     Updated: $updated | Tags: $tags"
    done
else
    echo "📚 Knowledge Base Overview"
    for type_dir in .claude/kb/*; do
        type=$(basename "$type_dir")
        count=$(find "$type_dir" -name "*.md" -type f | wc -l)
        echo "  📁 $type: $count entries"
    done
    echo ""
    echo "💡 Usage: /kb-list [type] [--recent] [--orphaned]"
    echo "   Types: metadata, debug_history, qa, code_index, patterns, plans, cheatsheets, memory_anchors, other"
fi
```
</actions>
