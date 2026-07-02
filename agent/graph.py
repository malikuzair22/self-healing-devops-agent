from langgraph.graph import StateGraph
from agent.state import AgentState
from agent.nodes import observe_node, diagnose_node, decide_node, act_node, verify_node, log_node

graph = StateGraph(AgentState)
graph.add_node('observe', observe_node)
graph.add_node('diagnose', diagnose_node)
graph.add_node('decide', decide_node)
graph.add_node('act', act_node)
graph.add_node('verify', verify_node)
graph.add_node('log', log_node)

graph.add_edge('observe', 'diagnose')
graph.add_edge('diagnose', 'decide')
graph.add_edge('decide', 'act')     
graph.add_edge('act', 'verify')
graph.add_edge('verify', 'log')

graph.set_entry_point('observe')

app = graph.compile()


if __name__ == "__main__":
    result = app.invoke({
        "logs": "Some random unknown error occurred",
        "metrics": "cpu_usage: 45%, memory: 60%",
        "pod_name": "target-app-867d9c8996-7jt74"
    })
    print(result)