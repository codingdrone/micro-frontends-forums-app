


```json

{
  // Review behavior
  "strictness": 2,
  "commentTypes": ["logic", "syntax", "style", "info"],
  
  // Custom standards
  "customContext": {
    "rules": [
      {
        "rule": "No direct database queries in controllers",
        "scope": ["src/controllers/**/*.ts"]
      }
    ],
    "files": [
      {
        "path": "docs/architecture.md",
        "description": "System architecture guidelines"
      }
    ]
  },
  
  // Pattern repositories (cross-repo context)
  "patternRepositories": ["company/shared-standards"],
  
  // Ignore patterns (newline-separated string)
  "ignorePatterns": "*.generated.*\n**/vendor/**\n**/__snapshots__/**"
}
```



```json
{
  "strictness": 2,
  "commentTypes": ["logic", "syntax"],
  "model": "gpt-4",
  "instructions": "Focus on security and maintainability",
  "ignorePatterns": "**/*.generated.*\ndist/**\n*.md",
  "patternRepositories": ["acme/shared-utils"],
  "triggerOnUpdates": false,
  "fileChangeLimit": 100,
  "includeAuthors": [],
  "excludeAuthors": ["dependabot[bot]"],
  "includeBranches": ["main", "develop"],
  "excludeBranches": ["draft/**"],
  "customContext": {
    "rules": [
      {
        "rule": "All API endpoints must have rate limiting",
        "scope": ["src/api/**/*.ts"]
      }
    ],
    "files": [
      {
        "path": "docs/architecture.md",
        "description": "System architecture"
      }
    ]
  },
  "shouldUpdateDescription": false,
  "updateExistingSummaryComment": true,
  "statusCheck": true,
  "includeConfidenceScore": true,
  "summarySection": {
    "included": true,
    "collapsible": false,
    "defaultOpen": true
  }
}
```
