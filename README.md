# 🧠 Chat Summarization Project

This project is designed to summarize long personal chats into structured summaries, preserving important details, emotional tone, and topic continuity.

---

## 📁 Project Structure

```
/chat_summarization_project
│── Dockerfile              # 🐳 Runs the project in Docker
│── main.py                 # 🧠 Core script with all processing logic
│── step_0_normalize.py     # 🔄 Step 0: Normalize raw data
│── step_1_preprocess.py    # 📝 Step 1: Preprocess Messages
│── step_2_segment.py       # 🏷️ Step 2: Segment Messages by Topics
│── step_3_extract.py       # 📌 Step 3: Extract Key Sentences
│── step_4_emotion.py       # 🎭 Step 4: Detect Emotional Tone
│── step_5_summary.py       # 📄 Step 5: Generate Final Summary
│── input.json              # 📥 Raw input data
│── output_step_0.json      # 📝 Output after data normalization
│── output_step_1.json      # 📝 Output after message preprocessing
│── output_step_2.json      # 📝 Topic segmentation result
│── output_step_3.json      # 📝 Extracted key sentences
│── output_step_4.json      # 📝 Emotion detection results
│── output_step_5.txt       # 📄 Final readable summary
│── README.md               # 📖 Documentation (to be drafted)
```

---

## ✅ Completed Steps

### Step 0: Normalize Raw Data
- Extracts structured messages from complex JSON structure.
- Result: flat list of messages per chat.

### Step 1: Preprocess Messages
- Cleans messages and keeps role and text.
- Result: list of `{role, message}` items.

---

### Step 2: Segment Messages by Topics
- Encodes each message with `all-mpnet-base-v2` (768D).
- Compares adjacent vectors with cosine similarity.
- Splits topics when similarity drops below threshold (0.5).
- Post-processing:
  - Merges emoji-only or very short segments into neighbors.
  - Attempts to merge semantically similar 1-message segments (threshold 0.9).
  - However, current post-processing may still struggle with emotionally continuous replies (future improvement needed).
- Output: `topics[]` field, each with its messages.
- Note: `topic` field is left `null` and will be filled in Step 5.

---

### Step 3: Extract Key Sentences
- For each topic block, splits messages into individual sentences.
- Uses sentence embeddings (MPNet) to rank sentences by cosine similarity to average.
- Selects top 1–2 central sentences to store as `key_sentences[]` for each topic.
- Output is written to `output_step_3.json`.

---

## 🔜 Future Steps

### Step 4: Detect Emotional Tone
- Analyze the emotional tone of each topic using a sentiment/emotion classifier.
- Assign labels like `joy`, `sadness`, `love`, `curiosity`, etc.
- Store as `emotion` key in each topic block.
- Output to `output_step_4.json`.

### Step 5: Generate Final Summary
- Use GPT or T5 model to generate a final summary based on:
  - `key_sentences`
  - `emotions`
  - `topic flow`
- Each topic receives a short paragraph summary and optional topic name.
- Final summary saved to `output_step_5.txt`.

---

## 📌 Known Issues / Future Improvements

- Multi-topic messages are not yet split; each message is treated as a unit.
- Emotional or dialog-based continuity is not yet fully captured in topic segmentation.
- Segment merging logic may miss emotionally tied short messages even with relaxed thresholds.
- Consider emotion-based merge logic or conversation-flow heuristics in future.

---