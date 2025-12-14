from langgraph.graph import StateGraph, START, END
from src.models.listening_state import ListeningState
from src.nodes.listening import (
    check_duplicate,
    translate_sentence,
    generate_tts,
    store_audio,
    build_card,
    send_to_anki,
)


def build_listening_graph():
    graph = StateGraph(ListeningState)

    # 1. nodes（ensure_listening_model 已移至 API 啟動時執行）
    graph.add_node("check_duplicate", check_duplicate)
    graph.add_node("translate_sentence", translate_sentence)
    graph.add_node("generate_tts", generate_tts)
    graph.add_node("store_audio", store_audio)
    graph.add_node("build_card", build_card)
    graph.add_node("send_to_anki", send_to_anki)

    # 2. 開始
    graph.add_edge(START, "check_duplicate")

    # 3. 判斷要不要繼續
    graph.add_conditional_edges(
        "check_duplicate",
        lambda s: "continue" if s.get("exists") is False else "skip",
        {
            "skip": END,
            "continue": "translate_sentence",
        },
    )

    # 4. 線性流程
    graph.add_edge("translate_sentence", "generate_tts")
    graph.add_edge("generate_tts", "store_audio")
    graph.add_edge("store_audio", "build_card")
    graph.add_edge("build_card", "send_to_anki")
    graph.add_edge("send_to_anki", END)

    return graph.compile()


def get_listening_graph_app():
    return build_listening_graph()
