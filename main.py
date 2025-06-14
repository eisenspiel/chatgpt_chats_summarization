import step_0_normalize
import step_1_preprocess
import step_2_segment
import step_3_extract
import step_4_emotion
import step_5_summary

if __name__ == "__main__":
    print("\n🚀 Running Step 0: Normalizing Raw Data...")
    step_0_normalize.run()

    #print("\n🚀 Running Step 1: Preprocessing Messages...")
    step_1_preprocess.run()

    #print("\n🚀 Running Step 2: Segmenting Messages into Topics...")
    step_2_segment.run()

    #print("\n🚀 Running Step 3: Extracting Key Sentences...")
    step_3_extract.run()

    #print("\n🚀 Running Step 4: Detecting Emotional Tone...")
    #step_4_emotion.run()

    #print("\n🚀 Running Step 5: Generating Final Summary...")
    #step_5_summary.run()

    print("\n✅ Chat summarization process completed!")
