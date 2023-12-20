#!/usr/bin/env python3
import os
from os import listdir
from os.path import isfile, join

FILES_DIR = "./bad-data-copy"
NONE_SNORE_AVG_NAMING = "NAvgSnore"
NONE_MAX_SNORE_NAMING = "NMSnore"

onlyfiles = [f for f in listdir(FILES_DIR) if isfile(join(FILES_DIR, f))]


def process_line(line):
    parts = line.split(",")
    if len(parts) != 3:
        raise Exception("Bad Value Inner Data Layer")
    try:
        return float(parts[1]), int(parts[2])
    except ValueError:
        raise Exception("Bad Value To Parse")


def calculate_metrics(snore_points_array, noise_level_elements):
    max_snore_point = 0.0
    avg_snore_points = 0.0
    avg_noise_level = sum(noise_level_elements) / len(noise_level_elements)
    if len(snore_points_array) != 0:
        max_snore_point = max(snore_points_array)
        avg_snore_points = sum(snore_points_array) / len(snore_points_array)
    else:
        max_snore_point = NONE_MAX_SNORE_NAMING
        avg_snore_points = NONE_SNORE_AVG_NAMING
    return max_snore_point, avg_snore_points, avg_noise_level


def generate_filename(old_filename, max_snore_point, avg_snore_points, avg_noise_level):
    base_filename = old_filename.rsplit(".", 1)[0]
    placeholder_data = "07-48-35.025"
    if(old_filename.find("snore") != -1):
        base_filename = old_filename.rsplit("-", 1)[0]
        base_filename += "-" + placeholder_data
    try:
        new_values = (
            f"{max_snore_point:.2f}-{avg_snore_points:.2f}-{avg_noise_level:.2f}"
        )
    except ValueError:
        new_values = f"{max_snore_point}-{avg_snore_points}-{avg_noise_level:.2f}"

    new_filename = f"{base_filename}-{new_values}.csv"
    return new_filename


for file in onlyfiles:
    snore_points_array = []
    noise_level_elements = []
    with open(join(FILES_DIR, file), "r") as f:
        for line in f:
            db, event_type = process_line(line)
            if event_type == 7:
                snore_points_array.append(db)
            if event_type == 0:
                noise_level_elements.append(db)
    f.close()
    max_s, avg_s, noise = calculate_metrics(snore_points_array, noise_level_elements)
    new_filename = generate_filename(file, max_s, avg_s, noise)
    print(f"Renaming {file} to {new_filename}")
    old_file_path = os.path.join(FILES_DIR, file)
    new_file_path = os.path.join(FILES_DIR, new_filename)
    os.rename(old_file_path, new_file_path)
    print("Done renaming")
