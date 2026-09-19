from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Things from the old repositories that should be reviewed if they still
# appear inside code, markdown, notebook headings, comments, or file paths.
# ---------------------------------------------------------------------------

SEARCH_TERMS = {
    # Old chronological/generic names
    "Day1": "Old chronological name",
    "Day2": "Old chronological name",
    "Day 3": "Old chronological name",
    "Day4": "Old chronological name",
    "Day5": "Old chronological name",
    "Day6": "Old chronological name",
    "Day7": "Old chronological name",
    "Day8": "Old chronological name",
    "Day9": "Old chronological name",

    # Old descriptive filenames/headings
    "K_means": "Old filename/name",
    "K_nearest_neighbor": "Old filename/name",
    "More_on_Logistic_Regression_Model": "Old notebook name",
    "More_on_Logistic_Regression_Part2": "Old notebook name",
    "More_on_Logistic_Regression_Part3": "Old notebook name",
    "More on Logistic Regression": "Possible old notebook heading",
    "Plotting Graph": "Old notebook heading/name",
    "Introduction to PySpark": "Old notebook heading/name",
    "Filtering in Pyspark": "Old notebook heading/name",
    "Logistic Regression in Pyspark": "Old notebook heading/name",

    # Old dataset names
    "Social_Network_Ads.csv": "Dataset path/name",
    "titanic.csv": "Dataset path/name",
    "basic_data.csv": "Dataset path/name",
    "test2.csv": "Dataset path/name",
    "df_train.csv": "Dataset path/name",
    "df_test.csv": "Dataset path/name",

    # Other old file names
    "DecisionTreeRegressor.ipynb": "Old filename",
    "Decision_Tree_Analysis.ipynb": "Old filename",
    "Gini_versus_Entropy.ipynb": "Old filename",
    "KNN_Classification_Comparison.ipynb": "Old filename",
    "L1RegularizationinLogisticRegression.ipynb": "Old filename",
    "LassoRegression.ipynb": "Old filename",
    "Overfitting_Underfitting_in_Decision_Tree.ipynb": "Old filename",
    "RidgeRegression.ipynb": "Old filename",
    "RidgeRegressionFromScratch.ipynb": "Old filename",
    "SparsityinRegularization.ipynb": "Old filename",
    "SupervisedLearning.ipynb": "Old filename",
    "iris_dataset_tree_visualization.ipynb": "Old filename",
}


TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".rst",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}


# Detect obvious hardcoded Windows absolute paths such as:
# D:\Projects\something.csv
WINDOWS_ABSOLUTE_PATH = re.compile(
    r"""[A-Za-z]:[\\/][^"'`\n\r]+"""
)


# Detect obvious Unix/macOS absolute user paths.
UNIX_USER_PATH = re.compile(
    r"""(?:/home/[^/"'\s]+|/Users/[^/"'\s]+)[^"'`\n\r]*"""
)


def get_tracked_files():
    """
    Scan Git-tracked files only.

    Since git mv updates the index, this should operate on your new filenames
    rather than the old paths.
    """
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    return [
        ROOT / line
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def shorten(text, limit=180):
    text = text.replace("\n", " ").replace("\r", " ").strip()

    if len(text) <= limit:
        return text

    return text[: limit - 3] + "..."


def find_terms(text):
    matches = []

    lower_text = text.lower()

    for term, category in SEARCH_TERMS.items():
        if term.lower() in lower_text:
            matches.append((term, category))

    return matches


def report_match(path, location, term, category, excerpt):
    relative = path.relative_to(ROOT)

    print(f"\n[{category}]")
    print(f"File:     {relative}")
    print(f"Location: {location}")
    print(f"Match:    {term}")
    print(f"Text:     {shorten(excerpt)}")


def audit_text_file(path):
    count = 0

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            print(f"\n[SKIP: encoding] {path.relative_to(ROOT)}")
            return 0

    for line_number, line in enumerate(text.splitlines(), start=1):

        for term, category in find_terms(line):
            report_match(
                path,
                f"line {line_number}",
                term,
                category,
                line,
            )
            count += 1

        for match in WINDOWS_ABSOLUTE_PATH.findall(line):
            report_match(
                path,
                f"line {line_number}",
                match,
                "Hardcoded absolute path",
                line,
            )
            count += 1

        for match in UNIX_USER_PATH.findall(line):
            report_match(
                path,
                f"line {line_number}",
                match,
                "Hardcoded absolute path",
                line,
            )
            count += 1

    return count


def audit_notebook(path):
    count = 0

    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(
            f"\n[ERROR reading notebook] "
            f"{path.relative_to(ROOT)}: {exc}"
        )
        return 0

    cells = notebook.get("cells", [])

    for cell_index, cell in enumerate(cells, start=1):
        cell_type = cell.get("cell_type", "unknown")

        source = cell.get("source", [])

        if isinstance(source, list):
            text = "".join(source)
        else:
            text = str(source)

        lines = text.splitlines()

        for line_number, line in enumerate(lines, start=1):

            for term, category in find_terms(line):
                report_match(
                    path,
                    f"{cell_type} cell {cell_index}, line {line_number}",
                    term,
                    category,
                    line,
                )
                count += 1

            for match in WINDOWS_ABSOLUTE_PATH.findall(line):
                report_match(
                    path,
                    f"{cell_type} cell {cell_index}, line {line_number}",
                    match,
                    "Hardcoded absolute path",
                    line,
                )
                count += 1

            for match in UNIX_USER_PATH.findall(line):
                report_match(
                    path,
                    f"{cell_type} cell {cell_index}, line {line_number}",
                    match,
                    "Hardcoded absolute path",
                    line,
                )
                count += 1

    return count


def main():
    try:
        files = get_tracked_files()
    except subprocess.CalledProcessError:
        print("ERROR: Run this script from inside your Git repository.")
        sys.exit(1)

    total_matches = 0
    scanned = 0

    print("=" * 72)
    print(" INTERNAL REFERENCE AUDIT")
    print("=" * 72)
    print()
    print("This script does NOT modify any files.")
    print()

    for path in files:
        if not path.exists() or not path.is_file():
            continue

        suffix = path.suffix.lower()

        if suffix == ".ipynb":
            scanned += 1
            total_matches += audit_notebook(path)

        elif suffix in TEXT_EXTENSIONS:
            scanned += 1
            total_matches += audit_text_file(path)

    print()
    print("=" * 72)
    print(" SUMMARY")
    print("=" * 72)
    print()
    print(f"Files scanned: {scanned}")
    print(f"References requiring review: {total_matches}")

    if total_matches == 0:
        print()
        print("No legacy names, dataset references, or obvious absolute paths found.")
    else:
        print()
        print("Review the matches above before making replacements.")


if __name__ == "__main__":
    main()