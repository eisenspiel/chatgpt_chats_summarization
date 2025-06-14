import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def load_segmented_data(input_file: str) -> list:
    """Loads topic-segmented data from Step 2."""
    with open(input_file, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_key_sentences_from_topic(messages: list, model) -> list:
    """Extracts the most semantically central sentence(s) from a topic block."""
    if not messages:
        return []

    # Split all messages into individual sentences
    sentences = []
    for msg in messages:
        for line in msg["message"].split("\n"):
            line = line.strip()
            if len(line) > 3:
                sentences.append(line)

    if not sentences:
        return []

    # Embed all sentences
    embeddings = model.encode(sentences)
    avg_vector = np.mean(embeddings, axis=0)

    # Rank by similarity to average topic vector
    scores = cosine_similarity([avg_vector], embeddings)[0]
    ranked_indices = np.argsort(scores)[::-1]

    # Take top 1 or 2 depending on topic length
    top_n = 2 if len(sentences) > 5 else 1
    top_sentences = [sentences[i] for i in ranked_indices[:top_n]]

    return top_sentences

def extract_all_key_sentences(chats: list, model) -> list:
    """Processes each chat's topic blocks to extract key sentences."""
    output = []
    for chat in chats:
        new_chat = {
            "title": chat.get("title"),
            "create_time": chat.get("create_time"),
            "update_time": chat.get("update_time"),
            "topics": []
        }

        for topic in chat.get("topics", []):
            messages = topic.get("messages", [])
            key_sentences = extract_key_sentences_from_topic(messages, model)
            new_topic = {
                "topic": topic.get("topic"),
                "messages": messages,
                "key_sentences": key_sentences
            }
            new_chat["topics"].append(new_topic)

        print(f"📌 Chat '{chat.get('title')}' processed: {len(new_chat['topics'])} topics")
        output.append(new_chat)

    return output

def save_key_sentences(output_file: str, data: list):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Key sentences saved to {output_file}")

def run():
    input_file = "output\\output_step_2.json"
    output_file = "output\\output_step_3.json"
    model = SentenceTransformer("all-mpnet-base-v2")

    segmented_data = load_segmented_data(input_file)
    summarized = extract_all_key_sentences(segmented_data, model)
    save_key_sentences(output_file, summarized)
