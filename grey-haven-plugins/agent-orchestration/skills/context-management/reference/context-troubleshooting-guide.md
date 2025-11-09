# Context Management Troubleshooting Guide

Comprehensive solutions for common context management issues.

**Quick Navigation:**
- [Save Failures](#save-failures)
- [Restore Failures](#restore-failures)
- [Performance Issues](#performance-issues)
- [Size Issues](#size-issues)
- [Corruption Issues](#corruption-issues)
- [Version Compatibility](#version-compatibility)

---

## Save Failures

### Issue: "Context too large" error

**Symptoms:**
- Error: "Context exceeds maximum size (500KB)"
- Save operation fails or hangs
- Performance degradation

**Root Causes:**
1. Conversation history not pruned (>100 messages)
2. Large file contents embedded in context
3. Excessive checkpoints without cleanup
4. Redundant data in decisions/actions

**Solutions:**

**Solution 1: Prune Conversation History**
```javascript
function pruneConversationHistory(history, maxMessages = 50) {
  if (history.length <= maxMessages) return history;

  // Strategy: Keep first 5, last 20, and decision points
  const start = history.slice(0, 5);
  const end = history.slice(-20);

  // Extract decision points from middle
  const middle = history.slice(5, -20);
  const decisions = middle.filter(msg =>
    msg.content.includes('DECISION:') ||
    msg.content.includes('ERROR:') ||
    msg.content.includes('MILESTONE:')
  );

  return [...start, ...decisions, ...end];
}

// Usage
context.conversation_history = pruneConversationHistory(
  context.conversation_history,
  50
);
```

**Solution 2: Externalize Large Files**
```python
import os
import hashlib

def externalize_large_files(context, size_threshold_kb=10):
    """Move large file contents to external storage."""
    externalized = {}

    for file_path in context.get('files_modified', []):
        file_size = os.path.getsize(file_path) / 1024  # KB

        if file_size > size_threshold_kb:
            # Calculate hash for deduplication
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            # Store in external location
            external_path = f".claude/context/files/{file_hash}.txt"
            os.makedirs(os.path.dirname(external_path), exist_ok=True)

            with open(file_path) as src, open(external_path, 'w') as dst:
                dst.write(src.read())

            externalized[file_path] = {
                'size': int(file_size),
                'hash': file_hash,
                'storage': external_path
            }

    context['large_file_refs'] = externalized
    return context
```

**Solution 3: Compress Checkpoints**
```javascript
const zlib = require('zlib');

function compressCheckpoints(checkpoints) {
  return checkpoints.map(checkpoint => {
    const json = JSON.stringify(checkpoint);
    const compressed = zlib.gzipSync(json);
    return {
      id: checkpoint.id,
      timestamp: checkpoint.timestamp,
      data: compressed.toString('base64'),
      compressed: true
    };
  });
}

function decompressCheckpoint(checkpoint) {
  if (!checkpoint.compressed) return checkpoint;

  const compressed = Buffer.from(checkpoint.data, 'base64');
  const json = zlib.gunzipSync(compressed).toString();
  return JSON.parse(json);
}
```

**Verification:**
```bash
# Check context size before/after
du -h .claude/context/workflow-id.json

# Should see 60-80% reduction after optimization
# Before: 850 KB → After: 120 KB
```

---

### Issue: Permission denied when saving

**Symptoms:**
- Error: "EACCES: permission denied"
- Save fails silently
- Context file not updated

**Root Causes:**
1. Incorrect file permissions
2. Directory doesn't exist
3. File locked by another process
4. Insufficient disk space

**Solutions:**

**Solution 1: Check and Fix Permissions**
```bash
# Check current permissions
ls -la .claude/context/

# Fix permissions
chmod 755 .claude/context/
chmod 644 .claude/context/*.json

# Verify
ls -la .claude/context/
```

**Solution 2: Ensure Directory Exists**
```python
import os
import json

def safe_save_context(workflow_id, context):
    """Save context with directory creation."""
    context_dir = '.claude/context'
    os.makedirs(context_dir, exist_ok=True)

    context_path = os.path.join(context_dir, f'{workflow_id}.json')
    temp_path = f'{context_path}.tmp'

    try:
        # Write to temp file first
        with open(temp_path, 'w') as f:
            json.dump(context, f, indent=2)

        # Atomic rename
        os.replace(temp_path, context_path)

        return True

    except Exception as e:
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise e
```

**Solution 3: Handle File Locks**
```javascript
const fs = require('fs');
const lockfile = require('proper-lockfile');

async function saveContextWithLock(workflowId, context) {
  const contextPath = `.claude/context/${workflowId}.json`;

  // Acquire lock
  const release = await lockfile.lock(contextPath, {
    retries: {
      retries: 5,
      minTimeout: 100,
      maxTimeout: 1000
    }
  });

  try {
    // Save context
    fs.writeFileSync(contextPath, JSON.stringify(context, null, 2));
  } finally {
    // Always release lock
    await release();
  }
}
```

---

## Restore Failures

### Issue: "Invalid JSON" error

**Symptoms:**
- Error: "Unexpected token < in JSON at position 0"
- JSON.parse() fails
- Context file appears empty or corrupted

**Root Causes:**
1. Incomplete write (process killed during save)
2. Disk full during save
3. File corruption
4. Wrong file format

**Solutions:**

**Solution 1: Validate Before Parse**
```javascript
function safeLoadContext(contextPath) {
  try {
    const content = fs.readFileSync(contextPath, 'utf-8');

    // Check if empty
    if (!content || content.trim().length === 0) {
      throw new Error('Context file is empty');
    }

    // Check if valid JSON structure
    if (!content.trim().startsWith('{')) {
      throw new Error('Context file does not contain valid JSON');
    }

    // Parse
    const context = JSON.parse(content);

    // Validate required fields
    const required = ['version', 'workflow_id', 'timestamp'];
    for (const field of required) {
      if (!(field in context)) {
        throw new Error(`Missing required field: ${field}`);
      }
    }

    return context;

  } catch (error) {
    console.error(`Failed to load context: ${error.message}`);

    // Try to load backup
    const backupPath = `${contextPath}.backup`;
    if (fs.existsSync(backupPath)) {
      console.log('Attempting to restore from backup...');
      return safeLoadContext(backupPath);
    }

    throw error;
  }
}
```

**Solution 2: Implement Backup Strategy**
```python
import shutil
import json

def save_context_with_backup(workflow_id, context):
    """Save context with automatic backup."""
    context_path = f'.claude/context/{workflow_id}.json'
    backup_path = f'{context_path}.backup'

    # If context exists, backup before overwriting
    if os.path.exists(context_path):
        shutil.copy2(context_path, backup_path)

    # Save new context
    temp_path = f'{context_path}.tmp'
    with open(temp_path, 'w') as f:
        json.dump(context, f, indent=2)

    # Verify new file is valid JSON
    with open(temp_path) as f:
        json.load(f)  # Will raise if invalid

    # Atomic replace
    os.replace(temp_path, context_path)

    return context_path
```

**Solution 3: Repair Corrupted JSON**
```javascript
const fs = require('fs');

function repairCorruptedContext(contextPath) {
  const content = fs.readFileSync(contextPath, 'utf-8');

  // Common repairs
  let repaired = content;

  // Remove trailing commas
  repaired = repaired.replace(/,(\s*[}\]])/g, '$1');

  // Fix unclosed strings (basic attempt)
  const stringMatches = repaired.match(/"[^"]*$/);
  if (stringMatches) {
    repaired += '"';
  }

  // Fix unclosed objects/arrays
  const openBraces = (repaired.match(/{/g) || []).length;
  const closeBraces = (repaired.match(/}/g) || []).length;
  repaired += '}'.repeat(Math.max(0, openBraces - closeBraces));

  // Try to parse
  try {
    return JSON.parse(repaired);
  } catch (error) {
    throw new Error(`Unable to repair JSON: ${error.message}`);
  }
}
```

---

### Issue: Version incompatibility

**Symptoms:**
- Error: "Context version 1.0 not compatible with current version 2.0"
- Missing fields after restore
- Unexpected behavior after restore

**Root Cause:**
- Context saved with older schema version
- Breaking changes in newer version
- Missing migration path

**Solutions:**

**Solution 1: Implement Version Migration**
```javascript
const MIGRATIONS = {
  '1.0': migrateFrom1_0to1_1,
  '1.1': migrateFrom1_1to2_0,
  '2.0': migrateFrom2_0to2_1
};

function migrateContext(context, targetVersion = CURRENT_VERSION) {
  let current = { ...context };
  const currentVersion = current.version;

  console.log(`Migrating context from v${currentVersion} to v${targetVersion}`);

  // Apply migrations in order
  const versions = Object.keys(MIGRATIONS).sort(compareVersions);

  for (const version of versions) {
    if (compareVersions(current.version, version) < 0) {
      console.log(`  Applying migration: v${version}`);
      current = MIGRATIONS[version](current);
      current.version = version;
    }
  }

  return current;
}

// Example migration: v1.0 → v1.1
function migrateFrom1_0to1_1(context) {
  return {
    ...context,
    version: '1.1',
    // New field in v1.1
    constraints: context.constraints || [],
    // Rename field
    files_changed: context.files_modified || []
  };
}

// Example migration: v1.1 → v2.0 (breaking changes)
function migrateFrom1_1to2_0(context) {
  return {
    version: '2.0',
    workflow_id: context.workflow_id,
    timestamp: context.timestamp,
    current_agent: context.current_agent,

    // Restructured in v2.0
    state: {
      phase: context.phase,
      files: context.files_changed,
      decisions: context.decisions,
      actions: context.pending_actions
    },

    // New required field
    metadata: {
      created_at: context.created_at || context.timestamp,
      updated_at: context.timestamp,
      creator: 'migration-from-v1.1'
    }
  };
}
```

**Solution 2: Version Compatibility Check**
```python
from packaging import version as pkg_version

CURRENT_VERSION = "2.1"
MIN_SUPPORTED_VERSION = "1.0"

def check_version_compatibility(context):
    """Check if context version is supported."""
    context_version = context.get('version', '1.0')

    # Parse versions
    current = pkg_version.parse(CURRENT_VERSION)
    minimum = pkg_version.parse(MIN_SUPPORTED_VERSION)
    ctx_ver = pkg_version.parse(context_version)

    # Check if too old
    if ctx_ver < minimum:
        raise ValueError(
            f"Context version {context_version} is too old. "
            f"Minimum supported: {MIN_SUPPORTED_VERSION}"
        )

    # Check if too new
    if ctx_ver > current:
        raise ValueError(
            f"Context version {context_version} is newer than "
            f"current version {CURRENT_VERSION}. Please update."
        )

    # Check if migration needed
    if ctx_ver < current:
        print(f"Migration required: {context_version} → {CURRENT_VERSION}")
        return False  # Needs migration

    return True  # Compatible
```

---

## Performance Issues

### Issue: Slow save/restore operations

**Symptoms:**
- Save takes >5 seconds
- Restore takes >10 seconds
- UI freezes during operations
- High CPU usage

**Root Causes:**
1. Large context size (>500KB)
2. Synchronous I/O blocking main thread
3. No caching of frequently loaded contexts
4. Expensive validation operations

**Solutions:**

**Solution 1: Async Operations**
```javascript
async function saveContextAsync(workflowId, context) {
  const contextPath = `.claude/context/${workflowId}.json`;
  const tempPath = `${contextPath}.tmp`;

  // Serialize in background
  const jsonString = await new Promise((resolve, reject) => {
    setImmediate(() => {
      try {
        resolve(JSON.stringify(context, null, 2));
      } catch (error) {
        reject(error);
      }
    });
  });

  // Write asynchronously
  await fs.promises.writeFile(tempPath, jsonString);
  await fs.promises.rename(tempPath, contextPath);

  console.log(`Context saved: ${contextPath} (${jsonString.length} bytes)`);
}

async function loadContextAsync(workflowId) {
  const contextPath = `.claude/context/${workflowId}.json`;

  // Read asynchronously
  const jsonString = await fs.promises.readFile(contextPath, 'utf-8');

  // Parse in background
  return await new Promise((resolve, reject) => {
    setImmediate(() => {
      try {
        resolve(JSON.parse(jsonString));
      } catch (error) {
        reject(error);
      }
    });
  });
}
```

**Solution 2: Implement Caching**
```python
from functools import lru_cache
import time

class ContextCache:
    def __init__(self, max_size=10, ttl_seconds=300):
        self.cache = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds

    def get(self, workflow_id):
        """Get context from cache if valid."""
        if workflow_id in self.cache:
            context, timestamp = self.cache[workflow_id]

            # Check TTL
            if time.time() - timestamp < self.ttl_seconds:
                print(f"Cache hit: {workflow_id}")
                return context
            else:
                del self.cache[workflow_id]

        return None

    def set(self, workflow_id, context):
        """Store context in cache."""
        # Evict oldest if at capacity
        if len(self.cache) >= self.max_size:
            oldest = min(self.cache.items(), key=lambda x: x[1][1])
            del self.cache[oldest[0]]

        self.cache[workflow_id] = (context, time.time())

# Usage
cache = ContextCache(max_size=10, ttl_seconds=300)

def load_context_with_cache(workflow_id):
    # Check cache first
    cached = cache.get(workflow_id)
    if cached:
        return cached

    # Load from disk
    with open(f'.claude/context/{workflow_id}.json') as f:
        context = json.load(f)

    # Store in cache
    cache.set(workflow_id, context)

    return context
```

**Solution 3: Lazy Validation**
```javascript
class LazyContext {
  constructor(contextPath) {
    this.contextPath = contextPath;
    this._metadata = null;
    this._fullContext = null;
  }

  // Load only metadata initially
  get metadata() {
    if (!this._metadata) {
      const json = fs.readFileSync(this.contextPath, 'utf-8');
      const context = JSON.parse(json);

      this._metadata = {
        version: context.version,
        workflow_id: context.workflow_id,
        phase: context.phase,
        timestamp: context.timestamp
      };
    }
    return this._metadata;
  }

  // Load full context only when needed
  get fullContext() {
    if (!this._fullContext) {
      const json = fs.readFileSync(this.contextPath, 'utf-8');
      this._fullContext = JSON.parse(json);
    }
    return this._fullContext;
  }

  // Validate only when accessed
  validate() {
    const required = ['version', 'workflow_id', 'timestamp'];
    for (const field of required) {
      if (!(field in this.metadata)) {
        throw new Error(`Missing required field: ${field}`);
      }
    }
    return true;
  }
}

// Usage
const context = new LazyContext('.claude/context/workflow-id.json');
console.log(context.metadata.phase);  // Fast - only loads metadata
// context.fullContext.conversation_history  // Slower - loads everything
```

---

## Size Issues

### Issue: Context exceeds recommended size

**Symptoms:**
- Context file >500KB
- Slow save/restore operations
- High memory usage
- Git repository bloat

**Root Cause:**
- Excessive conversation history (>100 messages)
- Large file snapshots embedded
- Uncompressed data
- Redundant information

**Solutions:**

**Solution 1: Aggressive Pruning**
```javascript
function aggressiveOptimization(context) {
  const optimized = { ...context };

  // 1. Prune conversation history (keep only 30)
  if (optimized.conversation_history?.length > 30) {
    optimized.conversation_history = [
      ...optimized.conversation_history.slice(0, 5),   // First 5
      ...optimized.conversation_history.slice(-25)     // Last 25
    ];
  }

  // 2. Remove completed pending actions
  optimized.pending_actions = optimized.pending_actions?.filter(
    action => action.status !== 'completed'
  ) || [];

  // 3. Deduplicate decisions
  optimized.decisions = [...new Set(optimized.decisions || [])];

  // 4. Remove redundant error log entries
  if (optimized.error_log?.length > 20) {
    // Keep only unique errors
    const uniqueErrors = new Map();
    optimized.error_log.forEach(error => {
      const key = `${error.type}-${error.message}`;
      if (!uniqueErrors.has(key)) {
        uniqueErrors.set(key, error);
      }
    });
    optimized.error_log = Array.from(uniqueErrors.values());
  }

  // 5. Compress old checkpoints
  if (optimized.checkpoints?.length > 5) {
    optimized.checkpoints = optimized.checkpoints.slice(-5);
  }

  return optimized;
}

// Measure size reduction
const before = JSON.stringify(context).length;
const optimized = aggressiveOptimization(context);
const after = JSON.stringify(optimized).length;
const reduction = ((before - after) / before * 100).toFixed(1);

console.log(`Size reduced: ${before} → ${after} bytes (${reduction}% reduction)`);
```

**Solution 2: Context Splitting**
```python
def split_large_context(context, max_size_kb=100):
    """Split large context into main + archive."""
    import json

    # Serialize to check size
    json_str = json.dumps(context, indent=2)
    size_kb = len(json_str) / 1024

    if size_kb <= max_size_kb:
        return context  # No split needed

    # Create main context (essential fields only)
    main_context = {
        'version': context['version'],
        'workflow_id': context['workflow_id'],
        'timestamp': context['timestamp'],
        'current_agent': context['current_agent'],
        'phase': context['phase'],
        'next_agent': context.get('next_agent'),

        'files_modified': context.get('files_modified', []),
        'decisions': context.get('decisions', [])[-20:],  # Last 20
        'pending_actions': context.get('pending_actions', []),

        'archive_ref': f".claude/context/archive/{context['workflow_id']}-full.json"
    }

    # Save full context to archive
    archive_path = main_context['archive_ref']
    os.makedirs(os.path.dirname(archive_path), exist_ok=True)

    with open(archive_path, 'w') as f:
        json.dump(context, f, indent=2)

    print(f"Context split: main={len(json.dumps(main_context))/1024:.1f}KB, archive={size_kb:.1f}KB")

    return main_context
```

---

## Corruption Issues

### Issue: Context file corrupted

**Symptoms:**
- Invalid JSON errors
- Missing data after restore
- Unexpected null values
- Truncated file

**Root Causes:**
1. Process killed during write
2. Disk full
3. Hardware failure
4. Concurrent writes

**Solutions:**

**Solution 1: Atomic Writes**
```javascript
const fs = require('fs');
const path = require('path');

function atomicSaveContext(workflowId, context) {
  const contextDir = '.claude/context';
  const contextPath = path.join(contextDir, `${workflowId}.json`);
  const tempPath = `${contextPath}.${process.pid}.tmp`;

  try {
    // 1. Write to temp file
    fs.writeFileSync(tempPath, JSON.stringify(context, null, 2));

    // 2. Verify temp file is valid
    const verification = JSON.parse(fs.readFileSync(tempPath, 'utf-8'));
    if (!verification.workflow_id) {
      throw new Error('Verification failed: missing workflow_id');
    }

    // 3. Backup existing context
    if (fs.existsSync(contextPath)) {
      const backupPath = `${contextPath}.backup`;
      fs.copyFileSync(contextPath, backupPath);
    }

    // 4. Atomic rename (replaces existing)
    fs.renameSync(tempPath, contextPath);

    // 5. Verify final file
    JSON.parse(fs.readFileSync(contextPath, 'utf-8'));

    return contextPath;

  } catch (error) {
    // Cleanup temp file on error
    if (fs.existsSync(tempPath)) {
      fs.unlinkSync(tempPath);
    }
    throw error;
  }
}
```

**Solution 2: Corruption Detection**
```python
import hashlib
import json

def save_context_with_checksum(workflow_id, context):
    """Save context with integrity checksum."""
    context_path = f'.claude/context/{workflow_id}.json'

    # Serialize context
    json_str = json.dumps(context, indent=2)

    # Calculate checksum
    checksum = hashlib.sha256(json_str.encode()).hexdigest()

    # Add checksum to context
    context_with_checksum = {
        **context,
        '_checksum': checksum
    }

    # Save
    with open(context_path, 'w') as f:
        json.dump(context_with_checksum, f, indent=2)

    return checksum

def verify_context_integrity(context_path):
    """Verify context hasn't been corrupted."""
    with open(context_path) as f:
        context = json.load(f)

    # Extract stored checksum
    stored_checksum = context.pop('_checksum', None)

    if not stored_checksum:
        raise ValueError('No checksum found - cannot verify')

    # Recalculate checksum
    json_str = json.dumps(context, indent=2)
    calculated_checksum = hashlib.sha256(json_str.encode()).hexdigest()

    if stored_checksum != calculated_checksum:
        raise ValueError(
            f'Checksum mismatch: file may be corrupted\n'
            f'  Stored: {stored_checksum}\n'
            f'  Calculated: {calculated_checksum}'
        )

    return context  # Without checksum field
```

---

## Version Compatibility

### Issue: Cannot load context from different version

**Symptoms:**
- Missing fields after migration
- TypeError: undefined property
- Workflow cannot resume

**Solutions:**

**Solution 1: Backward Compatibility**
```javascript
function loadContextWithFallbacks(contextPath) {
  const context = JSON.parse(fs.readFileSync(contextPath, 'utf-8'));

  // Provide defaults for fields added in newer versions
  return {
    version: context.version || '1.0',
    workflow_id: context.workflow_id,
    timestamp: context.timestamp,

    // v1.1+ field
    constraints: context.constraints || [],

    // v2.0+ field
    metadata: context.metadata || {
      created_at: context.timestamp,
      updated_at: context.timestamp
    },

    // v2.1+ field
    tags: context.tags || [],

    ...context
  };
}
```

**Solution 2: Forward Compatibility**
```python
def save_context_forward_compatible(context):
    """Save context that older versions can still read."""

    # Always include required fields for oldest supported version
    essential = {
        'version': context['version'],
        'workflow_id': context['workflow_id'],
        'timestamp': context['timestamp'],
        'current_agent': context['current_agent'],
        'phase': context['phase']
    }

    # Add all other fields (new versions can have extra)
    full_context = {
        **essential,
        **{k: v for k, v in context.items() if k not in essential}
    }

    return full_context
```

---

## Quick Diagnostic Commands

```bash
# Check context file exists
test -f .claude/context/workflow-id.json && echo "✅ Exists" || echo "❌ Missing"

# Validate JSON syntax
jq empty .claude/context/workflow-id.json && echo "✅ Valid JSON" || echo "❌ Invalid JSON"

# Check context size
du -h .claude/context/workflow-id.json

# View required fields only
jq '{version, workflow_id, timestamp, phase}' .claude/context/workflow-id.json

# Count conversation messages
jq '.conversation_history | length' .claude/context/workflow-id.json

# List all workflow contexts
ls -lh .claude/context/*.json

# Find large contexts (>100KB)
find .claude/context -name "*.json" -size +100k -exec du -h {} \;

# Verify all contexts are valid JSON
for f in .claude/context/*.json; do
  jq empty "$f" 2>/dev/null && echo "✅ $f" || echo "❌ $f"
done
```

---

**Troubleshooting Guide Version**: 1.0
**Last Updated**: 2025-01-15
