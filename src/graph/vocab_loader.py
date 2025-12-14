from langgraph.graph import StateGraph, START, END
from src.models.vocab_state import VocabState
from src.nodes.vocab import (
    parse_word,
    send_to_anki,
    extract_root,
    check_duplicate,
    build_tags,
    build_examples,
    generate_tts,
    store_audio,
)


def build_vocab_graph():
    graph = StateGraph(VocabState)

    graph.add_node("check_duplicate", check_duplicate)
    graph.add_node("fanout", lambda _: {})
    graph.add_node("parse_word", parse_word)
    graph.add_node("extract_root", extract_root)
    graph.add_node("build_tags", build_tags)
    graph.add_node("build_examples", build_examples)
    graph.add_node("generate_tts", generate_tts)
    graph.add_node("store_audio", store_audio)
    graph.add_node("send_to_anki", send_to_anki)

    graph.add_edge(START, "check_duplicate")

    # 判斷要不要建立新的卡片
    # check_duplicate：
    # - note 存在 & force=False  -> exists=True
    # - 其餘情況（新字或強制更新） -> exists=False
    graph.add_conditional_edges(
        "check_duplicate",
        lambda s: "continue" if s.get("exists") is False else "skip",
        {
            "skip": END,  # 有舊卡且不強制更新 -> 直接結束
            "continue": "fanout",  # 需要處理 -> fanout
        },
    )

    # fanout：在「需要處理」的情況下，同時跑兩個 node
    graph.add_edge("fanout", "parse_word")
    graph.add_edge("fanout", "extract_root")

    # 平行完成後匯流到 build_tags
    graph.add_edge("parse_word", "build_tags")
    graph.add_edge("extract_root", "build_tags")

    # 後續流程：build_examples -> TTS -> store_audio -> send_to_anki
    graph.add_edge("build_tags", "build_examples")
    graph.add_edge("build_examples", "generate_tts")
    graph.add_edge("generate_tts", "store_audio")
    graph.add_edge("store_audio", "send_to_anki")
    graph.add_edge("send_to_anki", END)

    return graph.compile()


def get_vocab_graph_app():
    return build_vocab_graph()
