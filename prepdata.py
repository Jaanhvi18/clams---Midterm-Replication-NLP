import os
import pandas as pd
import string
import glob
import difflib
import re


def remove_punctuation(sentence):
    return sentence.translate(str.maketrans("", "", string.punctuation))


def format_sentence_file(language, file_paths, output_dir):
    formatted_data = []

    sentence_id = 0
    pair_id = 0
    context_id = 0

    previous_condition = None

    # iterate through each file for the diff langs
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        file_name = re.sub(r"\.txt$", "", file_name)
        # print(file_name)
        # print(f"Processing {file_path} for language {language}")
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    # skip if the line is empty
                    continue

                # split by whitespace bc of how the data was formatted
                parts = line.split(None, 1)
                if len(parts) == 2:

                    label = parts[0]
                    sentence = parts[1]  # snetenec

                    clean_sentence = remove_punctuation(sentence)

                    comparison = "unexpected" if label == "False" else "expected"

                    formatted_data.append(
                        {
                            "sentid": sentence_id,
                            "condition": file_name,
                            "contextid": pair_id,
                            "pairid": pair_id,
                            "comparison": comparison,
                            "lemma": "placeholder",
                            "sentence": clean_sentence,
                            "ROI": len(clean_sentence.split()),
                        }
                    )
                    sentence_id += 1
                    context_id += 1

                    if comparison == "unexpected":
                        pair_id += 1

    df = pd.DataFrame(formatted_data)

    # Take only the top 4 rows
    # df_top_4 = df.head(4)

    output_file = os.path.join(output_dir, f"{language}_formatted.tsv")
    df.to_csv(output_file, sep="\t", index=False, encoding="utf-8")

    # output_file = os.path.join(output_dir, f"{language}_formatted.tsv")
    # df.to_csv(output_file, sep="\t", index=False, encoding="utf-8")
    # print(f"Formatted data for {language} saved to {output_file}")


def main():
    languages = {
        # "english": glob.glob("clams/de_evalset/en_evalset/**/*.txt", recursive=True),
        "english": glob.glob("en_evalset/**/*.txt", recursive=True),
        # "hebrew": glob.glob("clams/de_evalset/he_evalset/**/*.txt", recursive=True),
        # "french": glob.glob("clams/de_evalset/fr_evalset/**/*.txt", recursive=True),
        # "russian": glob.glob("clams/de_evalset/ru_evalset/**/*.txt", recursive=True),
    }

    output_dir = "formatted_data"
    os.makedirs(output_dir, exist_ok=True)

    for language, file_paths in languages.items():
        format_sentence_file(language, file_paths, output_dir)


if __name__ == "__main__":
    main()

