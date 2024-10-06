import pandas as pd
import difflib
import os
import glob

input_folder = "formatted_data"
output_folder = "output"
os.makedirs(
    output_folder, exist_ok=True
)  

file_paths = glob.glob(os.path.join(input_folder, "*.tsv"))


def find_first_different_word_index(sentence1, sentence2):
    words1 = sentence1.split()
    words2 = sentence2.split()

    differ = difflib.Differ()
    diff = list(differ.compare(words1, words2))

    for i, word in enumerate(diff):
        if word.startswith("- "):
            return i

    return None



for file_path in file_paths:

    language = os.path.basename(file_path).replace("_formatted.tsv", "")

    df = pd.read_csv(file_path, sep="\t")

    updated_rows = []

    # iteraing using unique pairids
    for pair_id in df["pairid"].unique():
        sentence_pair = df[df["pairid"] == pair_id]

        if len(sentence_pair) == 2:
            sentence1 = sentence_pair.iloc[0]["sentence"]
            sentence2 = sentence_pair.iloc[1]["sentence"]

            diff_index = find_first_different_word_index(sentence1, sentence2)
            updated_rows.append(
                {
                    "sentid": sentence_pair.iloc[0]["sentid"],
                    "condition": sentence_pair.iloc[0]["condition"],
                    "contextid": sentence_pair.iloc[0]["contextid"],
                    "pairid": sentence_pair.iloc[0]["pairid"],
                    "comparison": sentence_pair.iloc[0]["comparison"],
                    "sentence": sentence1,
                    "ROI": diff_index,
                }
            )

            # Add sentence 2 to updated_rows
            updated_rows.append(
                {
                    "sentid": sentence_pair.iloc[1]["sentid"],
                    "condition": sentence_pair.iloc[1]["condition"],
                    "contextid": sentence_pair.iloc[1]["contextid"],
                    "pairid": sentence_pair.iloc[1]["pairid"],
                    "comparison": sentence_pair.iloc[1]["comparison"],
                    "sentence": sentence2,
                    "ROI": diff_index,
                }
            )


    updated_df = pd.DataFrame(updated_rows)

    output_csv_path = os.path.join(output_folder, f"{language}_updated.tsv")
    updated_df.to_csv(output_csv_path, sep="\t", index=False)

    print(f"Updated TSV saved for {language} at: {output_csv_path}")
