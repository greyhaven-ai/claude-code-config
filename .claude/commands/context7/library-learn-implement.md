---
allowed-tools: Task, TodoWrite, Read, Write, MultiEdit, Bash
description: Learn a library with Context7 docs, then implement features with TDD agents
argument-hint: [library name and feature to implement]
---

Learn library and implement feature: $ARGUMENTS

<ultrathink>
Documentation drives understanding. Context7 provides the map, agents build the territory. Learn, implement, test.
</ultrathink>

<megaexpertise type="library-learning-orchestrator">
The assistant should use Context7 to deeply understand a library's documentation, then chain TDD agents to implement features correctly.
</megaexpertise>

<context>
Learning and implementing: $ARGUMENTS
Will fetch comprehensive docs from Context7
Chain appropriate implementation agents based on language
</context>

<requirements>
- Resolve library to Context7 ID
- Fetch comprehensive documentation
- Understand API patterns and best practices
- Implement feature with TDD
- Create example code with tests
</requirements>

<actions>
1. **Parse Request**:
   ```javascript
   // Extract library and feature from arguments
   const [libraryName, ...featureParts] = "$ARGUMENTS".split(' ');
   const feature = featureParts.join(' ');
   
   console.log(`Library: ${libraryName}`);
   console.log(`Feature to implement: ${feature}`);
   ```

2. **Resolve Library in Context7**:
   ```javascript
   // Search for library
   const libraries = await mcp__context7__resolve_library_id({
     libraryName: libraryName
   });
   
   // Select best match
   const library = libraries.find(l => 
     l.name.toLowerCase() === libraryName.toLowerCase() ||
     l.trust_score >= 8
   ) || libraries[0];
   
   console.log(`Selected: ${library.id} (Trust: ${library.trust_score}/10)`);
   console.log(`Snippets available: ${library.code_snippets}`);
   ```

3. **Fetch Comprehensive Documentation**:
   ```javascript
   // Get general documentation
   const generalDocs = await mcp__context7__get_library_docs({
     context7CompatibleLibraryID: library.id,
     tokens: 15000
   });
   
   // Get feature-specific documentation
   const featureDocs = await mcp__context7__get_library_docs({
     context7CompatibleLibraryID: library.id,
     topic: feature,
     tokens: 10000
   });
   
   // Get code examples
   const exampleDocs = await mcp__context7__get_library_docs({
     context7CompatibleLibraryID: library.id,
     topic: "examples code snippets",
     tokens: 8000
   });
   ```

4. **Analyze Documentation with Web Researcher**:
   - Invoke web-docs-researcher agent:
     ```
     Task: "Analyze library documentation for ${libraryName}:
           
           General Docs:
           ${generalDocs}
           
           Feature-Specific (${feature}):
           ${featureDocs}
           
           Extract:
           1. Core concepts and patterns
           2. API methods relevant to: ${feature}
           3. Best practices and gotchas
           4. Common implementation patterns
           5. Error handling approaches"
     ```

5. **Determine Implementation Language**:
   ```javascript
   // Detect language from examples
   const hasTypeScript = exampleDocs.includes('```typescript');
   const hasJavaScript = exampleDocs.includes('```javascript');
   const hasPython = exampleDocs.includes('```python');
   const hasReact = exampleDocs.includes('React') || exampleDocs.includes('JSX');
   
   let implementationLanguage;
   if (hasTypeScript || (hasJavaScript && library.id.includes('react'))) {
     implementationLanguage = 'typescript';
   } else if (hasPython) {
     implementationLanguage = 'python';
   } else {
     implementationLanguage = 'javascript';
   }
   ```

6. **Chain to Appropriate TDD Agent**:
   
   **For TypeScript/JavaScript Libraries**:
   - Invoke tdd-typescript agent:
     ```
     Task: "Implement ${feature} using ${libraryName}:
           
           Documentation Summary:
           ${docsSummary}
           
           API Methods Available:
           ${apiMethods}
           
           Example Pattern:
           ${exampleDocs}
           
           Requirements:
           1. Implement ${feature} following library patterns
           2. Write comprehensive tests first
           3. Handle edge cases mentioned in docs
           4. Follow library's error handling conventions
           5. Use TypeScript types if available"
     ```
   
   **For Python Libraries**:
   - Invoke tdd-python agent:
     ```
     Task: "Implement ${feature} using ${libraryName}:
           
           Documentation:
           ${docsSummary}
           
           Implement following library conventions:
           1. Use documented initialization patterns
           2. Follow error handling as shown in examples
           3. Write pytest tests first
           4. Include type hints"
     ```

7. **Create Implementation Plan**:
   ```markdown
   ## Implementation Plan: ${feature}
   
   ### Library: ${libraryName} (${library.id})
   
   ### Core Concepts from Docs:
   ${conceptsSummary}
   
   ### Required Methods/APIs:
   ${apiMethods.map(m => `- ${m.name}: ${m.description}`).join('\n')}
   
   ### Implementation Steps:
   1. Setup and initialization
   2. Core feature implementation
   3. Error handling
   4. Edge cases
   5. Performance considerations
   
   ### Test Cases:
   1. Happy path
   2. Error scenarios
   3. Edge cases
   4. Integration tests
   ```

8. **Generate Example Implementation**:
   ```typescript
   // Example: ${feature} with ${libraryName}
   
   // Based on Context7 documentation
   import { ${imports} } from '${libraryName}';
   
   /**
    * ${feature} implementation
    * Following patterns from: ${library.id}
    * Documentation: ${library.doc_coverage}% coverage
    */
   export class ${className} {
     constructor(config: ${ConfigType}) {
       // Initialization pattern from docs
       ${initCode}
     }
     
     /**
      * Main feature implementation
      * Ref: ${docReference}
      */
     async ${methodName}(params: ${ParamsType}): Promise<${ReturnType}> {
       try {
         // Implementation based on documented patterns
         ${implementation}
       } catch (error) {
         // Error handling from library docs
         ${errorHandling}
       }
     }
   }
   ```

9. **Generate Comprehensive Tests**:
   ```typescript
   // Tests for ${feature}
   import { describe, it, expect, beforeEach } from 'vitest';
   import { ${className} } from './implementation';
   
   describe('${feature} with ${libraryName}', () => {
     let instance: ${className};
     
     beforeEach(() => {
       // Setup from library docs
       instance = new ${className}(${testConfig});
     });
     
     describe('Happy Path (from docs examples)', () => {
       it('should ${expectedBehavior}', async () => {
         // Test based on documented example
         const result = await instance.${methodName}(${testParams});
         expect(result).toEqual(${expectedResult});
       });
     });
     
     describe('Error Handling (from docs)', () => {
       it('should handle ${errorCase}', async () => {
         // Error case from documentation
         await expect(instance.${methodName}(${invalidParams}))
           .rejects.toThrow(${expectedError});
       });
     });
     
     describe('Edge Cases (from docs gotchas)', () => {
       ${edgeCases.map(edge => `
       it('should handle ${edge.description}', async () => {
         ${edge.test}
       });`).join('\n')}
     });
   });
   ```

10. **Create Integration Example**:
    ```javascript
    // Real-world integration example
    // Based on Context7 documentation patterns
    
    async function realWorldExample() {
      // Initialize as shown in docs
      const client = new ${libraryName}.Client({
        ${configFromDocs}
      });
      
      // Implement feature
      const feature = new ${className}(client);
      
      // Use feature as documented
      try {
        const result = await feature.${methodName}({
          ${realWorldParams}
        });
        
        console.log('Success:', result);
      } catch (error) {
        // Handle errors as per library docs
        if (error.code === '${errorCode}') {
          console.error('Known error:', error.message);
        } else {
          throw error;
        }
      }
    }
    ```

11. **Documentation Cross-Reference**:
    ```markdown
    ## Documentation References
    
    ### Context7 Source
    - Library ID: ${library.id}
    - Version: ${library.version}
    - Trust Score: ${library.trust_score}/10
    - Coverage: ${library.doc_coverage}%
    
    ### Key Documentation Sections Used
    ${docSections.map(s => `
    #### ${s.title}
    - Topic: ${s.topic}
    - Relevance: ${s.relevance}
    - Code Snippets: ${s.snippets}
    `).join('\n')}
    
    ### API Methods Referenced
    ${apiMethods.map(m => `
    - \`${m.signature}\`
      - Docs: ${m.docLink}
      - Used for: ${m.usage}
    `).join('\n')}
    
    ### Patterns Followed
    1. ${pattern1} - [Ref: ${ref1}]
    2. ${pattern2} - [Ref: ${ref2}]
    
    ### Gotchas Avoided
    1. ${gotcha1} - Solution: ${solution1}
    2. ${gotcha2} - Solution: ${solution2}
    ```

12. **Generate Learning Report**:
    ```markdown
    # Library Learning & Implementation Report
    
    ## Library: ${libraryName}
    - Context7 ID: ${library.id}
    - Documentation Quality: ${library.trust_score}/10
    - Code Snippets Available: ${library.code_snippets}
    
    ## Feature Implemented: ${feature}
    
    ### What I Learned from Docs:
    ${learningSummary}
    
    ### Key Patterns Discovered:
    1. ${pattern1}
    2. ${pattern2}
    3. ${pattern3}
    
    ### Implementation Details:
    - Language: ${implementationLanguage}
    - Framework: ${framework}
    - Test Framework: ${testFramework}
    - Lines of Code: ${loc}
    - Test Coverage: ${coverage}%
    
    ### Challenges & Solutions:
    ${challenges.map(c => `
    **Challenge**: ${c.description}
    **Solution**: ${c.solution} (Ref: ${c.docRef})
    `).join('\n')}
    
    ### Performance Considerations:
    ${performanceNotes}
    
    ### Security Considerations:
    ${securityNotes}
    
    ### Next Steps:
    1. Deploy implementation
    2. Monitor for edge cases
    3. Contribute examples back to Context7
    4. Create tutorial for team
    ```

13. **Verify Implementation**:
    ```bash
    # Run tests
    if [ "$implementationLanguage" = "typescript" ]; then
      bun test
    elif [ "$implementationLanguage" = "python" ]; then
      uv run pytest
    fi
    
    # Check coverage
    bun test --coverage
    
    # Lint
    bun run lint
    ```
</actions>

The assistant should treat Context7 as the authoritative source for library knowledge, extracting patterns and best practices, then chain TDD agents to create production-ready implementations with comprehensive tests.