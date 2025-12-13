from langgraph.graph import StateGraph, START, END
from src.models.state import WordState
from src.nodes.parse_word import parse_word
from src.nodes.build_back import build_back
from src.nodes.send_to_anki import send_to_anki
from src.nodes.extract_root import extract_root
from src.nodes.check_duplicate import check_duplicate
from src.nodes.build_tags import build_tags

def build_graph():
    graph = StateGraph(WordState)

    # 1. nodes
    graph.add_node("check_duplicate", check_duplicate)
    graph.add_node("fanout", lambda _: {})      # 只做分流，不改 state
    graph.add_node("parse_word", parse_word)
    graph.add_node("extract_root", extract_root)
    graph.add_node("build_tags", build_tags)
    graph.add_node("build_back", build_back)
    graph.add_node("send_to_anki", send_to_anki)

    # 2. 開始
    graph.add_edge(START, "check_duplicate")

    # 3. 判斷要不要繼續
    # check_duplicate 內部已經把 exists 算好了：
    # - note 存在 & force=False  -> exists=True
    # - 其餘情況（新字或強制更新） -> exists=False
    graph.add_conditional_edges(
        "check_duplicate",
        lambda s: "continue" if s.get("exists") is False else "skip",
        {
            "skip": END,          # 有舊卡且不強制更新 → 直接結束
            "continue": "fanout", # 需要處理 → 進 fanout
        },
    )

    # 4. fanout：在「需要處理」的情況下，同時跑兩個 node
    graph.add_edge("fanout", "parse_word")
    graph.add_edge("fanout", "extract_root")

    # 5. 平行完成後匯流到 build_tags
    graph.add_edge("parse_word", "build_tags")
    graph.add_edge("extract_root", "build_tags")

    # 6. 後續流程
    graph.add_edge("build_tags", "build_back")
    graph.add_edge("build_back", "send_to_anki")
    graph.add_edge("send_to_anki", END)

    return graph.compile()

def get_graph_app():
    return build_graph()