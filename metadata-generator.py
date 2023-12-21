DIRNAME = "test-flight-user-mix"
NONE_SNORE_AVG_NAMING = "NAvgSnore"
NONE_MAX_SNORE_NAMING = "NMSnore"
VERSION_PLACEHOLDER = 1035
MODEL_PLACEHOLDER = "iPhone10"
CSV_PLACEHOLDER = "csv"


import os
from os import listdir
from os.path import join, isfile


def calculate_metrics(filename):
    with open(join(DIRNAME, filename), "r", encoding="utf-8") as f:
        noise_levels, snore_event_noise_levels, none_snore_event_noise_levels = (
            [],
            [],
            [],
        )
        first_snore_event_timestamp, last_line = "null", None

        for line in f:
            parts = line.split(",")
            if len(parts) != 3:
                raise Exception("Bad data")
            timestamp, noise, event = parts[0], float(parts[1]), int(parts[2])

            if noise != float("-inf"):
                noise_levels.append(noise)

                if event == 7:
                    if first_snore_event_timestamp == "null":
                        first_snore_event_timestamp = timestamp
                    snore_event_noise_levels.append(noise)
                elif event == 0:
                    none_snore_event_noise_levels.append(noise)

            last_line = line

    if last_line:
        last_event_timestamp = last_line.split(",")[0]
    avg_db, max_db = (
        (sum(noise_levels) / len(noise_levels), max(noise_levels))
        if noise_levels
        else (0, 0)
    )
    noise_level = (
        sum(none_snore_event_noise_levels) / len(none_snore_event_noise_levels)
        if none_snore_event_noise_levels
        else 0
    )

    if snore_event_noise_levels:
        peak_snore, avg_snore = max(snore_event_noise_levels), sum(
            snore_event_noise_levels
        ) / len(snore_event_noise_levels)
    else:
        peak_snore, avg_snore = NONE_MAX_SNORE_NAMING, NONE_SNORE_AVG_NAMING

    serialized_event = "snore" if snore_event_noise_levels else "none"

    return (
        last_event_timestamp,
        serialized_event,
        len(snore_event_noise_levels),
        avg_db,
        max_db,
        first_snore_event_timestamp,
        peak_snore,
        avg_snore,
        noise_level,
    )


def generate_new_filename(old_filename: str):
    splits = old_filename.split("-")
    new_filename = [CSV_PLACEHOLDER, splits[1], splits[2], splits[3]]

    (
        last_event_timestamp,
        serialized_event,
        snore_count,
        avg_db,
        max_db,
        first_snore_event_timestamp,
        peak_snore,
        avg_snore,
        noise_level,
    ) = calculate_metrics(old_filename)

    new_filename += [
        last_event_timestamp[:8],
        serialized_event,
        str(VERSION_PLACEHOLDER),
        MODEL_PLACEHOLDER,
        str(snore_count),
        f"{avg_db:.2f}",
        f"{max_db:.2f}",
        first_snore_event_timestamp,
        f"{peak_snore:.2f}" if peak_snore != NONE_MAX_SNORE_NAMING else peak_snore,
        f"{avg_snore:.2f}" if avg_snore != NONE_SNORE_AVG_NAMING else avg_snore,
        f"{noise_level:.2f}",
    ]

    return "-".join(new_filename) + ".csv"


def os_rename(old_filename, new_filename):
    print(f"Renaming {old_filename} to {new_filename}")
    old_file_path = os.path.join(DIRNAME, old_filename)
    new_file_path = os.path.join(DIRNAME, new_filename)
    os.rename(old_file_path, new_file_path)
    print("Done renaming")


files = [f for f in listdir(DIRNAME) if isfile(join(DIRNAME, f))]

for file in files:
    new_filename = generate_new_filename(file)
    os_rename(file, new_filename)
