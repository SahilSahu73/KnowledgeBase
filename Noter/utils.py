import hashlib
import os
import datetime


def generate_filename_id(filename: str) -> str:
    """
    Generate a SHA256-based unique ID for a file based on its filename only.
    The same filename will always return the same ID.
    """
    return hashlib.sha256(filename.encode("utf-8")).hexdigest()


def add_front_matter(folder: str):
    """
    Adds a YAML front-matter block to each Markdown file in the folder.
    Title = filename (without extension)
    unique_id = SHA256(filename)
    """
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                file_time = os.path.getctime(file_path)
                date_str = datetime.datetime.fromtimestamp(file_time).strftime("%Y-%m-%d")

                # Read file contents
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Skip if file already has front-matter
                if content.startswith("---\n"):
                    print(f"Skipping (already has front-matter): {file_path}")
                    continue

                # Extract filename without extension
                title = os.path.splitext(file)[0]
                unique_id = generate_filename_id(file)

                # YAML front-matter template
                front_matter = f"""---
title: "{title}"
unique_id: "{unique_id}"
author: "AutoMigrationScript"
tags: []
description: ""
date: "{date_str}"
---

"""

                # Write back file with front-matter prepended
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(front_matter + content)

                print(f"Front-matter added: {file_path}")


if __name__ == "__main__":
    knowledge_base_folder = "../KnowledgeBase/"
    add_front_matter(knowledge_base_folder)
