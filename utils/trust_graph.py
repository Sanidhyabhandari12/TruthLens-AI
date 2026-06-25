import networkx as nx
import matplotlib.pyplot as plt
import os


def build_trust_graph(all_docs_entities):
    graph = nx.DiGraph()

    for doc_name, entities in all_docs_entities.items():

        doc_node = f"Document: {doc_name}"
        graph.add_node(doc_node)

        for name in entities.get("names", []):
            name_node = f"Name: {name}"
            graph.add_node(name_node)
            graph.add_edge(doc_node, name_node, relation="contains")

        for pan in entities.get("pan", []):
            pan_node = f"PAN: {pan}"
            graph.add_node(pan_node)
            graph.add_edge(doc_node, pan_node, relation="contains")

        for gstin in entities.get("gstin", []):
            gst_node = f"GSTIN: {gstin}"
            graph.add_node(gst_node)
            graph.add_edge(doc_node, gst_node, relation="contains")

        for amount in entities.get("amounts", []):
            amount_node = f"Amount: {amount}"
            graph.add_node(amount_node)
            graph.add_edge(doc_node, amount_node, relation="mentions")

    return graph


def save_trust_graph_image(all_docs_entities):
    graph = build_trust_graph(all_docs_entities)

    os.makedirs("reports", exist_ok=True)

    image_path = os.path.join("reports", "trust_graph.png")

    plt.figure(figsize=(14, 8))

    pos = nx.spring_layout(
        graph,
        k=0.8,
        seed=42
    )

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=2200,
        font_size=8,
        arrows=True
    )

    edge_labels = nx.get_edge_attributes(
        graph,
        "relation"
    )

    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=edge_labels,
        font_size=7
    )

    plt.title("TruthLens Trust Graph")
    plt.tight_layout()
    plt.savefig(image_path, dpi=200)
    plt.close()

    return image_path