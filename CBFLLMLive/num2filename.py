# %%
import json
from pathlib import Path


# %%
def num2filename(num: str, target_path: Path) -> Path:
    for file in target_path.rglob("*"):
        if file.is_file() and num in file.name:
            return Path(*file.parts[-2:]).__str__()

    return None


# %%
root_path = Path(__file__).parent
target_path = root_path / "つくよみちゃん立ち絵"

satisfied_nums = [
    "01-01b",
    "01-02b",
    "01-03ac",
    "01-03b",
    "02-01ac",
    "02-01b",
    "02-02ac",
    "02-02b",
    "02-03ac",
    "02-03b",
    "02-04a",
    "02-04b",
    "02-04c",
    "03-01b",
    "03-02ac",
    "03-02b",
    "03-04ac",
    "03-04b",
    "04-01ac",
    "04-01b",
    "04-02ac",
    "04-02b",
    "11-01b",
    "11-01d",
]
neutral_nums = [
    "01-01a",
    "01-01c",
    "01-02a",
    "01-02c",
    "03-01a",
    "03-01c",
    "03-03a",
    "03-03b",
    "03-03c",
    "05-01a",
    "05-01b",
    "05-01c",
    "06-01a",
    "06-01b",
    "06-01c",
    "06-02a",
    "06-02c",
    "06-03c",
    "07-02a",
    "07-02c",
    "07-03a",
    "07-03b",
    "07-03c",
    "07-04ac",
    "11-01a",
    "11-01c",
]
unsatisfied_nums = [
    "06-02b",
    "06-03a",
    "06-03b",
    "07-01ac",
    "07-01b",
    "07-02b",
    "07-04b",
]

satisfied_filenames = []
neutral_filenames = []
unsatisfied_filenames = []
for num in satisfied_nums:
    filename = num2filename(num, target_path)
    if filename is not None:
        satisfied_filenames.append(filename)
for num in neutral_nums:
    filename = num2filename(num, target_path)
    if filename is not None:
        neutral_filenames.append(filename)
for num in unsatisfied_nums:
    filename = num2filename(num, target_path)
    if filename is not None:
        unsatisfied_filenames.append(filename)

# %%
satisfied_filenames
# %%
json_path = root_path / "TsukuyomiExpressions.json"
with json_path.open(mode="w", encoding="utf-8") as f:
    json.dump(
        {
            "satisfied": satisfied_filenames,
            "neutral": neutral_filenames,
            "unsatisfied": unsatisfied_filenames,
        },
        f,
        indent=4,
        ensure_ascii=False,
    )
# %%
