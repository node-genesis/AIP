
#!/usr/bin/env python3
"""
AIPNode_Compliant.py
Reference implementation of an Abstract Intent Protocol (AIP) node in Python.
"""

import re
import json
from typing import Dict, Set, Callable, Optional, Any


class AIPNode:
    def __init__(self, node_id: str, node_type: str = 'Worker', capabilities: Optional[list[str]] = None):
        self.node_id = node_id
        self.node_type = node_type
        self.capabilities = capabilities or []
        self.intent_handlers: Dict[str, Callable] = {}
        self.connected_nodes: Set['AIPNode'] = set()
        print(f"AIP Node {node_id} ({node_type}) initialized")

    def announce(self) -> dict:
        return {
            'type': 'ack',
            'intent': 'node.announce',
            'node': {
                'id': self.node_id,
                'type': self.node_type,
                'capabilities': self.capabilities
            }
        }

    def register_intent(self, intent_pattern: str, handler: Callable) -> 'AIPNode':
        self.intent_handlers[intent_pattern] = handler
        return self

    def connect(self, node: 'AIPNode') -> 'AIPNode':
        self.connected_nodes.add(node)
        node.connected_nodes.add(self)
        return self

    def process_intent(self, intent: str) -> dict:
        action, params = self.parse_intent(intent)
        if action in self.intent_handlers:
            try:
                result = self.intent_handlers[action](params)
                return {'type': 'fulfill', 'from': self.node_id, 'data': result}
            except Exception as e:
                return {'type': 'error', 'from': self.node_id, 'message': str(e)}

        for node in self.connected_nodes:
            if node is not self:
                result = node.process_intent(intent)
                if result.get('type') == 'fulfill':
                    return {'type': 'defer', 'from': self.node_id, 'to': node.node_id, 'result': result}

        return {'type': 'reject', 'from': self.node_id, 'reason': 'No handler found'}

    def parse_intent(self, intent_string: str) -> tuple[str, Dict[str, str]]:
        clean = intent_string[8:] if intent_string.startswith('intent: ') else intent_string
        match = re.match(r'([\w\.]+)\((.*)\)', clean)
        if not match:
            raise ValueError(f"Invalid intent format: {intent_string}")

        action = match.group(1)
        param_string = match.group(2)
        params = {}

        if param_string:
            pairs = re.findall(r'(\w+)\s*:\s*['"](.*?)['"](?:,|$)', param_string)
            for key, value in pairs:
                params[key] = value

        return action, params


# Example Genesis node test
def example():
    node_gen = AIPNode("genesis", "Genesis", ["orchestrate", "log"])
    node_mail = AIPNode("mail", "Worker", ["fetch"])
    node_notify = AIPNode("notify", "Worker", ["create"])

    node_gen.connect(node_mail).connect(node_notify)

    node_gen.register_intent("node.announce", lambda _: node_gen.announce())
    node_mail.register_intent("fetch.email", lambda p: [{"id": 1, "subject": "Hello"}])
    node_notify.register_intent("create.label", lambda p: {"success": True, "label": p.get("name")})

    intents = [
        "intent: node.announce()",
        "intent: fetch.email(filter: \"unread\")",
        "intent: create.label(name: \"Important\")",
        "intent: unknown.command()"
    ]

    for i in intents:
        print(json.dumps(node_gen.process_intent(i), indent=2))


if __name__ == "__main__":
    example()
