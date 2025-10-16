#!/usr/bin/env python3

import argparse
import csv
import glob
import os

parser = argparse.ArgumentParser(
    description="Load participant data from CSV and format as HTML."
)
parser.add_argument(
    "--input_file",
    action="store",
    type=str,
    default="data/participant.csv",
    help="Path to CSV file containing the participant data.",
)
parser.add_argument(
    "--output_file",
    action="store",
    type=str,
    default="participant.html",
    help="Path to write formatted HTML file to.",
)
args = parser.parse_args()

_PARTICIPANT_TEMPLATE = r'<li><a href="{url}" target="_blank"><img src="{image_file_path}" />{name}</a>{is_organizer}({affiliation})</li>'

html = r'<ul class="faces">' + "\n"
with open(args.input_file, "r") as f:
    reader = csv.DictReader(f)

    # Sort by last name with organizers first.
    sorted_rows = sorted(
        reader, key=lambda row: (not int(row["is_organizer"]), row["last_name"].lower())
    )

    for row in sorted_rows:
        # Normalize names to match image file names.
        normalized_first_name = (
            row["first_name"].lower().replace(" ", "-").replace("'", "-")
        )
        normalized_last_name = (
            row["last_name"].lower().replace(" ", "-").replace("'", "-")
        )

        glob_image_files = glob.glob(
            f"assets/participant/{normalized_first_name}_{normalized_last_name}.*"
        )

        if len(glob_image_files) == 0:
            image_file_path = "assets/participant/default.jpg"
            print(
                f"No image file found for {row['first_name']} {row['last_name']}. "
                f"Using default image."
            )
        else:
            image_file_path = glob_image_files[0]

        # Mark organizers.
        if int(row["is_organizer"]):
            is_organizer = "<b>Organizer</b><br />"
        else:
            is_organizer = ""

        html += (
            "\t"
            + _PARTICIPANT_TEMPLATE.format(
                url=row["url"],
                image_file_path=image_file_path,
                name=f"{row['first_name']} {row['last_name']}",
                is_organizer=is_organizer,
                affiliation=row["affiliation"],
            )
            + "\n"
        )

html += "</ul>"
html = html.expandtabs(4)

with open(args.output_file, "w") as f:
    f.write(html)
