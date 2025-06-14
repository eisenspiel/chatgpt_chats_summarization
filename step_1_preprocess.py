import json

def load_normalized_data(input_file: str) -> list:
    """Loads the normalized chat data from Step 0."""
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

def preprocess_messages(chats: list) -> list:
    """Cleans and standardizes messages in each chat."""
    processed_chats = []

    for chat in chats:
        title = chat["title"]
        create_time = chat["create_time"]
        update_time = chat["update_time"]
        messages = chat["messages"]

        cleaned_messages = []
        for msg in messages:
            role = msg["role"].strip().lower()  # Ensure role is consistent
            text = msg["message"].strip()  # Trim unnecessary whitespace

            if text:  # Ignore empty messages
                cleaned_messages.append({"role": role, "message": text})

        processed_chats.append({
            "title": title,
            "create_time": create_time,
            "update_time": update_time,
            "messages": cleaned_messages
        })

    return processed_chats

def save_preprocessed_data(output_file: str, processed_data: list):
    """Saves the preprocessed chat data to a JSON file."""
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(processed_data, file, indent=2, ensure_ascii=False)
        print(f"\n✅ Preprocessed data saved to {output_file}")
    except Exception as e:
        print(f"⚠️ Error saving file: {e}")

def run():
    """Executes Step 1: Preprocessing messages."""
    input_file = "output\\output_step_0.json"
    output_file = "output\\output_step_1.json"

    raw_chats = load_normalized_data(input_file)
    processed_chats = preprocess_messages(raw_chats)

    save_preprocessed_data(output_file, processed_chats)
