import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def load_preprocessed_data(input_file: str) -> list:
    with open(input_file, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_topic_boundaries(embeddings: list, threshold: float = 0.5) -> list:
    topic_boundaries = [0]
    for i in range(1, len(embeddings)):
        sim = cosine_similarity([embeddings[i - 1]], [embeddings[i]])[0][0]
        if sim < threshold:
            topic_boundaries.append(i)
    return topic_boundaries

def group_messages_by_topic(messages: list, boundaries: list) -> list:
    topics = []
    for i in range(len(boundaries)):
        start = boundaries[i]
        end = boundaries[i + 1] if i + 1 < len(boundaries) else len(messages)
        block = messages[start:end]
        topics.append({
            "topic": None,
            "messages": block
        })
    return topics

def post_process_merge_emoji_only(topics: list) -> list:
    merged = []
    for i, block in enumerate(topics):
        msgs = block["messages"]
        if len(msgs) == 1 and len(msgs[0]["message"].strip()) <= 3:
            if merged:
                merged[-1]["messages"].extend(msgs)
                continue
            elif i + 1 < len(topics):
                topics[i + 1]["messages"] = msgs + topics[i + 1]["messages"]
                continue
        merged.append(block)
    return merged

def post_process_merge_short_similar(topics: list, model) -> list:
    if len(topics) < 3:
        return topics

    def average_embedding(messages):
        texts = [msg["message"] for msg in messages]
        return np.mean(model.encode(texts), axis=0)

    result = []
    i = 0
    while i < len(topics):
        current = topics[i]
        if len(current["messages"]) == 1:
            prev = result[-1] if result else None
            nxt = topics[i + 1] if i + 1 < len(topics) else None

            curr_vec = average_embedding(current["messages"])

            if prev:
                prev_vec = average_embedding(prev["messages"])
                sim_prev = cosine_similarity([curr_vec], [prev_vec])[0][0]
            else:
                sim_prev = 0

            if nxt:
                nxt_vec = average_embedding(nxt["messages"])
                sim_next = cosine_similarity([curr_vec], [nxt_vec])[0][0]
            else:
                sim_next = 0

            if max(sim_prev, sim_next) > 0.9:
                if sim_prev >= sim_next and prev:
                    prev["messages"].extend(current["messages"])
                elif nxt:
                    nxt["messages"] = current["messages"] + nxt["messages"]
                i += 1
                continue

        result.append(current)
        i += 1

    return result

def segment_by_topics(chats: list, model) -> list:
    segmented_chats = []
    for chat in chats:
        messages = chat.get("messages", [])
        if not messages:
            continue

        texts = [msg["message"] for msg in messages]
        embeddings = model.encode(texts)

        boundaries = detect_topic_boundaries(embeddings)
        topics = group_messages_by_topic(messages, boundaries)
        topics = post_process_merge_emoji_only(topics)
        topics = post_process_merge_short_similar(topics, model)

        print(f"📌 Chat '{chat.get('title')}' processed: {len(topics)} topic(s) found.")

        segmented_chats.append({
            "title": chat.get("title"),
            "create_time": chat.get("create_time"),
            "update_time": chat.get("update_time"),
            "topics": topics
        })
    return segmented_chats

def save_segmented_data(output_file: str, segmented_data: list):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(segmented_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Segmented data saved to {output_file}")

def run():
    input_file = "output\\output_step_1.json"
    output_file = "output\\output_step_2.json"
    model = SentenceTransformer("all-mpnet-base-v2")

    preprocessed_chats = load_preprocessed_data(input_file)
    segmented_chats = segment_by_topics(preprocessed_chats, model)
    save_segmented_data(output_file, segmented_chats)