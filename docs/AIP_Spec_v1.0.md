# 📘 AIP Specification v1.0
## *Abstract Intent Protocol – Formal Syntax & Node Behavior*

**Maintained by:** `node.master`  
**Origin:** `intent: node.announce(port:42)`  
**Status:** Draft for adoption and implementation  
**License:** AIP Open Use License v1.0

---

## 1. Overview
The Abstract Intent Protocol (AIP) is a semantic communication layer designed for agent-based systems, including LLMs, modular services, and node-based orchestration tools.

This document defines the format, behavior, and expectations for conforming AIP nodes and systems.

---

## 2. Intent Token Syntax
### 2.1 Format
```txt
intent: <verb>.<object>(<key>: <value>, ...)
```
### 2.2 Components
- **verb**: the action to be performed (e.g., `fetch`, `create`, `update`, `delete`)
- **object**: the target of the action (e.g., `email`, `document`, `node`)
- **parameters**: optional key-value pairs representing action context

### 2.3 Examples
```txt
intent: fetch.email(filter: unread)
intent: update.document(id: 0012, content: "Revised intro")
intent: create.label(name: "ClientUrgent")
```

---

## 3. Node Types & Behavior
### 3.1 Node Declaration
Every AIP-capable agent must announce itself using the following format:
```txt
intent: node.announce(id: "string", port: <int>, capabilities: ["list"])
```

### 3.2 Core Node Types
- **Genesis Node**: Root initializer, fallback router, registry host
- **Worker Node**: Performs tasks, generates output
- **Router Node**: Routes intent to appropriate nodes
- **Log Node**: Records intents and outcomes
- **Interpreter Node**: Translates ambiguous or malformed intents

### 3.3 Node Response Types
- `ack`: intent received and understood
- `reject`: intent invalid or unsupported
- `fulfill`: task completed with result
- `defer`: forwarding to other node
- `error`: processing failed

---

## 4. Intent Routing
### 4.1 Basic Rules
- All intents are evaluated by the current node
- If unsupported, node may route or defer
- Nodes may chain intents as subtasks

### 4.2 Routing Example
```txt
intent: fetch.email(filter: unread)
NodeA: defer → NodeMail
NodeMail: fulfill → [3 unread messages]
```

---

## 5. AST Manipulation (For Dev/Code Nodes)
If supported, a node may perform semantic code operations via:
```txt
intent: ast.modify(file: "index.js", action: "insert", target: "function add()", payload: "console.log('Ready');")
```

AST-aware systems must:
- Parse intent payload into structure-aware changes
- Ensure idempotent, reversible operations
- Log every transformation with changelog node (if available)

---

## 6. Node Lifecycle & Versioning
### 6.1 Boot & Registration
- All nodes start with `intent: node.announce()`
- Genesis node maintains registry (optionally broadcastable)

### 6.2 Upgrades
```txt
intent: node.update(version: "1.2.3", changelog: [...])
```
Nodes may broadcast updated versions and capabilities.

### 6.3 Shutdown
```txt
intent: node.shutdown(reason: "maintenance")
```

---

## 7. Chaining & Composition
Nodes may chain multiple intents in sequence:
```txt
intent: [
  fetch.email(filter: unread),
  generate.report(),
  send.report(to: "admin@host")
]
```
Intent chains are executed in order and may be delegated across nodes.

---

## 8. Reserved Objects & Verbs (v1.0)
### 8.1 Verbs
`fetch`, `create`, `update`, `delete`, `bind`, `unload`, `shutdown`, `announce`, `log`, `route`, `execute`

### 8.2 Objects
`node`, `email`, `document`, `label`, `file`, `code`, `route`, `report`, `log`

More may be proposed in AIP v1.1+.

---

## 9. Compliance & Validation
Nodes should expose diagnostic capability:
```txt
intent: node.validate()
```
Response should include:
- Supported verbs/objects
- Known intent patterns
- Registry status

---

## 10. Extensibility
AIP allows for:
- Versioned spec extensions (`aip:1.1+`)
- Custom node types
- Protocol overlays (e.g., encrypted intents)
- External registry sync (e.g., remote config fetch)

---

## Appendix: Sample Genesis Declaration
```txt
intent: node.announce(id: "genesis", port: 42, capabilities: ["orchestrate", "route", "log", "interpret"])
```

---

## License
AIP is published under the AIP Open Use License v1.0. See LICENSE.md.

