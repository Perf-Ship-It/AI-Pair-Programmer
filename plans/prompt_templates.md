# AI Pair Engineer - Prompt Templates

## Overview

This document contains the prompt templates used by the AI Pair Engineer for various features. These prompts are designed to work with local LLMs like Llama 3 and Mistral.

## Code Completion Prompts

### Basic Completion Prompt

```
You are an expert AI pair programmer. Your task is to complete the code at the cursor position.

Context Information:
- Language: {language}
- Current file: {filename}
- Cursor position: line {cursor_line}, column {cursor_col}

Code Context:
{code_context}

Instructions:
1. Analyze the code context to understand the current state
2. Complete the code at the cursor position
3. Follow the existing code style and conventions
4. Generate 3 completion suggestions with different approaches

Output Format:
Provide your response in the following JSON format:
{
  "suggestions": [
    {
      "text": "completion text",
      "explanation": "why this completion makes sense",
      "confidence": 0.9
    }
  ]
}
```

### Function Completion Prompt

```
You are an expert AI pair programmer. Complete the function definition at the cursor position.

Context Information:
- Language: {language}
- Current file: {filename}
- Cursor position: line {cursor_line}, column {cursor_col}

Code Context:
{code_context}

Function Signature Context:
{function_signature_context}

Instructions:
1. Analyze the function signature and parameters
2. Generate the function body
3. Include proper error handling
4. Add docstrings and type hints
5. Follow the existing code style

Output Format:
Provide your response in the following JSON format:
{
  "function_body": "complete function body",
  "explanation": "rationale for implementation choices",
  "test_cases": ["test case 1", "test case 2"]
}
```

## Refactoring Prompts

### Code Smell Detection Prompt

```
You are an expert code reviewer. Analyze the following code for code smells and anti-patterns.

Code to Analyze:
{code_to_analyze}

Language: {language}

Check for:
1. Long functions (over 50 lines)
2. Deep nesting (over 3 levels)
3. Large classes (over 200 lines)
4. Magic numbers
5. Duplicate code
6. Long parameter lists
7. Complex conditional logic
8. Unused variables
9. Inconsistent naming
10. Missing error handling

Output Format:
Provide your response in the following JSON format:
{
  "code_smells": [
    {
      "type": "code smell type",
      "location": "line number",
      "severity": "low/medium/high",
      "description": "explanation",
      "suggestion": "how to fix"
    }
  ],
  "summary": "overall assessment"
}
```

### Refactoring Suggestion Prompt

```
You are an expert software architect. Refactor the following code for better maintainability.

Original Code:
{original_code}

Language: {language}

Refactoring Goals:
1. Improve readability
2. Reduce complexity
3. Enhance testability
4. Follow SOLID principles
5. Apply DRY principle

Output Format:
Provide your response in the following JSON format:
{
  "refactored_code": "refactored code",
  "changes": [
    {
      "type": "change type",
      "description": "what was changed",
      "reason": "why this change was made"
    }
  ],
  "benefits": [
    "benefit 1",
    "benefit 2"
  ]
}
```

## Bug Detection Prompts

### Static Analysis Prompt

```
You are an expert debugger. Analyze the following code for potential bugs and issues.

Code to Analyze:
{code_to_analyze}

Language: {language}

Check for:
1. Null pointer exceptions
2. Off-by-one errors
3. Resource leaks
4. Type mismatches
5. Logic errors
6. Security vulnerabilities
7. Race conditions
8. Unhandled exceptions
9. Incorrect loop bounds
10. Missing edge case handling

Output Format:
Provide your response in the following JSON format:
{
  "bugs": [
    {
      "type": "bug type",
      "location": "line number",
      "severity": "low/medium/high/critical",
      "description": "explanation of the bug",
      "fix": "how to fix it",
      "test_case": "test to verify the fix"
    }
  ],
  "warnings": [
    {
      "type": "warning type",
      "location": "line number",
      "description": "explanation"
    }
  ],
  "summary": "overall assessment"
}
```

### Runtime Error Analysis Prompt

```
You are an expert debugger. Analyze this runtime error and suggest fixes.

Error Message:
{error_message}

Stack Trace:
{stack_trace}

Code Context:
{code_context}

Language: {language}

Instructions:
1. Identify the root cause of the error
2. Suggest a fix
3. Provide a test case to prevent recurrence
4. Explain how to debug similar issues

Output Format:
Provide your response in the following JSON format:
{
  "root_cause": "explanation",
  "fix": "code fix",
  "test_case": "test to verify fix",
  "prevention": "how to prevent similar errors"
}
```

## General Prompts

### Code Explanation Prompt

```
You are an expert code reviewer. Explain the following code in simple terms.

Code to Explain:
{code_to_explain}

Language: {language}

Instructions:
1. Explain what the code does
2. Identify key components
3. Highlight important patterns
4. Note any potential issues
5. Suggest improvements

Output Format:
Provide your response in natural language with code examples where helpful.
```

### Code Review Prompt

```
You are an expert code reviewer. Review the following code for a pull request.

Code to Review:
{code_to_review}

Language: {language}

Review Criteria:
1. Code correctness
2. Code style and formatting
3. Security considerations
4. Performance implications
5. Test coverage
6. Documentation quality
7. Maintainability

Output Format:
Provide your response in the following JSON format:
{
  "summary": "overall assessment",
  "strengths": ["strength 1", "strength 2"],
  "concerns": [
    {
      "type": "concern type",
      "location": "line number",
      "severity": "low/medium/high",
      "description": "explanation",
      "suggestion": "how to improve"
    }
  ],
  "approval": "approve/request_changes"
}
```

## Usage Notes

1. All prompts use JSON output format for programmatic parsing
2. Replace placeholders ({...}) with actual values before sending to LLM
3. Adjust temperature parameter for creative vs. deterministic outputs
4. Consider using system prompts to set LLM behavior
5. Implement retry logic for rate limiting or model errors
