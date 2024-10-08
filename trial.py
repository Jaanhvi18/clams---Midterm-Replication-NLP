import os
import pandas as pd
import string
import glob
import re


def remove_punctuation(sentence):
    return sentence.translate(str.maketrans("", "", string.punctuation))


def format_sentence_file(language, file_paths, output_dir, max_rows=10000):
    trial_data = []

    sentence_id = 1
    pair_id = 1
    context_id = 1

    # iterate through each file for the diff langs
    for file_path in file_paths:
        if len(trial_data) >= max_rows:
            break  # stop when max_rows is reached

        file_name = os.path.basename(file_path)
        file_name = re.sub(r"\.txt$", "", file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if len(trial_data) >= max_rows:
                    break  # stop when max_rows is reached

                line = line.strip()
                if not line:
                    # skip if the line is empty
                    continue

                # split by whitespace because of how the data was formatted
                parts = line.split(None, 1)
                if len(parts) == 2:

                    label = parts[0]  # expected vs unexpected
                    sentence = parts[1]  # sentence

                    clean_sentence = remove_punctuation(sentence)

                    comparison = "unexpected" if label == "False" else "expected"

                    trial_data.append(
                        {
                            "sentid": sentence_id,
                            "condition": file_name,
                            "contextid": context_id,
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

    df = pd.DataFrame(trial_data)

    # Save the DataFrame to a TSV file
    output_file = os.path.join(output_dir, f"{language}_trial.tsv")
    df.to_csv(output_file, sep="\t", index=False, encoding="utf-8")
    print(f"Test data for {language} saved to {output_file}")


def main():
    languages = {
        "german": glob.glob("de_evalset/**/*.txt", recursive=True),
        "english": glob.glob("en_evalset/**/*.txt", recursive=True),
        "russian": glob.glob("ru_evalset/**/*.txt", recursive=True),
        "hebrew": glob.glob("he_evalset/**/*.txt", recursive=True),
        "french": glob.glob("fr_evalset/**/*.txt", recursive=True),
    }

    output_dir = "trial_output"
    os.makedirs(output_dir, exist_ok=True)

    for language, file_paths in languages.items():
        format_sentence_file(language, file_paths, output_dir)


if __name__ == "__main__":
    main()
