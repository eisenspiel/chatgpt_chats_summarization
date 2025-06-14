import json

def load_raw_data(input_file: str) -> dict:
    """Loads the raw JSON data from the input file."""
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return {}

def find_root_message(mapping: dict) -> str:
    """Finds the first meaningful user message in the chat tree."""
    for msg_id, node in mapping.items():
        message = node.get("message", {})  # Could be None
        if not message:
            continue  # Skip if message is missing

        role = message.get("author", {}).get("role", "")
        text = message.get("content", {}).get("parts", [""])[0].strip()

        if role == "user" and text:
            return msg_id  # Found the first real message

    return None  # No valid user message found

def traverse_message_tree(mapping: dict) -> list:
    """Traverses the message tree structure to reconstruct a linear chat history."""
    messages = []
    root_id = find_root_message(mapping)

    if not root_id:
        return messages

    queue = [root_id]

    while queue:
        current_id = queue.pop(0)
        node = mapping.get(current_id)

        if not node or not node.get("message"):
            continue

        message_data = node["message"]
        role = message_data.get("author", {}).get("role", "")
        content = message_data.get("content", {})
        parts = content.get("parts", [])

        # Handle parts format variations
        if isinstance(parts, list) and parts and isinstance(parts[0], str):
            text = parts[0]
        elif isinstance(parts, dict):
            first = parts.get("0", {})
            text = first.get("text", "") if isinstance(first, dict) else ""
        else:
            text = ""

        # Only add if there's meaningful content
        if isinstance(text, str) and text.strip():
            messages.append({
                "role": role,
                "message": text.strip()
            })

        queue.extend(node.get("children", []))

    return messages

def extract_conversations(raw_data: list) -> list:
    """Extracts and normalizes conversations from the raw JSON structure."""
    conversations = []

    for chat in raw_data:
        title = chat.get("title", "Untitled Chat")
        create_time = chat.get("create_time")
        update_time = chat.get("update_time")
        mapping = chat.get("mapping", {})

        messages = traverse_message_tree(mapping)

        conversations.append({
            "title": title,
            "create_time": create_time,
            "update_time": update_time,
            "messages": messages
        })

    return conversations

def normalize_chat_structure(raw_data: list) -> list:
    """Processes raw conversations into a structured format."""
    normalized_chats = []

    for chat in raw_data:
        title = chat.get("title", "Untitled Chat")
        create_time = chat.get("create_time")
        update_time = chat.get("update_time")
        messages = chat.get("messages", [])

        # Remove empty messages
        messages = [msg for msg in messages if msg["message"].strip()]

        # Ensure consistent formatting (e.g., trimming unnecessary newlines)
        for msg in messages:
            msg["message"] = msg["message"].strip()

        normalized_chats.append({
            "title": title,
            "create_time": create_time,
            "update_time": update_time,
            "messages": messages
        })

    return normalized_chats

def save_normalized_data(output_file: str, normalized_data: list):
    """Saves the normalized chat data to a JSON file."""
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(normalized_data, file, indent=2, ensure_ascii=False)
        print(f"\n✅ Normalized data saved to {output_file}")
    except Exception as e:
        print(f"⚠️ Error saving file: {e}")

def run():
    """Executes Step 0: Normalizing raw data."""
    input_file = "input\\input_test_step2.json"
    output_file = "output\\output_step_0.json"

    raw_data = load_raw_data(input_file)
    extracted_chats = extract_conversations(raw_data)
    normalized_chats = normalize_chat_structure(extracted_chats)

    save_normalized_data(output_file, normalized_chats)
