
/**
 * AIPNode.js
 * Compliant reference implementation of an Abstract Intent Protocol Node
 * Implements node types, structured intent routing, and response types
 */

class AIPNode {
  constructor(id, type = 'Worker', capabilities = []) {
    this.id = id;
    this.type = type;
    this.capabilities = capabilities;
    this.intentHandlers = {};
    this.connectedNodes = new Set();
  }

  // Announce node (simulation of node.announce intent)
  announce() {
    return {
      type: 'ack',
      intent: 'node.announce',
      node: {
        id: this.id,
        type: this.type,
        capabilities: this.capabilities
      }
    };
  }

  // Register an intent pattern and handler
  registerIntent(pattern, handler) {
    this.intentHandlers[pattern] = handler;
  }

  // Connect to another node
  connect(node) {
    this.connectedNodes.add(node);
    node.connectedNodes.add(this); // bidirectional
  }

  // Process a single intent
  processIntent(intentString) {
    const { action, params } = this.parseIntent(intentString);
    const handler = this.intentHandlers[action];

    if (handler) {
      try {
        const result = handler(params);
        return { type: 'fulfill', data: result };
      } catch (error) {
        return { type: 'error', message: error.message };
      }
    }

    // Defer to connected nodes
    for (const node of this.connectedNodes) {
      const result = node.processIntent(intentString);
      if (result && result.type === 'fulfill') {
        return { type: 'defer', node: node.id, result };
      }
    }

    return { type: 'reject', reason: 'No handler found' };
  }

  // Basic intent parser
  parseIntent(intent) {
    const clean = intent.replace(/^intent:\s*/, '');
    const match = clean.match(/([\w\.]+)\((.*)\)/);
    if (!match) throw new Error('Invalid intent syntax');
    const [_, action, paramStr] = match;
    const params = {};

    paramStr.split(',').forEach(pair => {
      const [k, v] = pair.split(':').map(s => s.trim().replace(/['"]/g, ''));
      if (k && v) params[k] = v;
    });

    return { action, params };
  }
}

// Example
const nodeA = new AIPNode('NodeA', 'Genesis', ['orchestrate', 'log']);
const nodeMail = new AIPNode('NodeMail', 'Worker', ['fetch']);
const nodeNotify = new AIPNode('NodeNotify', 'Worker', ['create']);

nodeA.connect(nodeMail);
nodeMail.connect(nodeNotify);

nodeA.registerIntent('node.announce', () => nodeA.announce());
nodeMail.registerIntent('fetch.email', (params) => {
  return [{ id: 1, subject: 'Test Email' }];
});
nodeNotify.registerIntent('create.label', (params) => {
  return { created: true, label: params.name };
});

module.exports = { AIPNode, nodeA, nodeMail, nodeNotify };
