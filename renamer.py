import os
import eyed3
import re
import json
import os
import sys

from eyed3.id3.tag import Tag

author = "Thomas777"
book = "Reinterpreting a Century of Leftism"
publisher = "The Pete Quinones Show"

chapters = [
    ("713", "Introduction"),
    ("720", "The Rise of the National Socialists in the Weimar Republic"),
    ("728", "The Invasion of Poland and the U.S. Enters the War"),
    ("731", "FDR and The New Dealers Push For War"),
    ("734", "Winston Churchill (1 of 4) - Origins"),
    ("737", "Winston Churchill (2 of 4) - 1930s"),
    ("740", "Winston Churchill (3 of 4) - 1936-1939"),
    ("743", "Winston Churchill (4 of 4) - Becoming a Warlord"),
    ("745", "Operation Barbarossa (1 of 2) - Dispelling Myths and Introduction"),
    ("748", "Operation Barbarossa (2 of 2) - In Detail"),
    ("751", "The Conscience of the War - Wagers and Planners"),
    ("755", "The Nuremberg Regime (1 of 6) - Background (1 of 2)"),
    ("761", "The Nuremberg Regime (2 of 6) - Background (2 of 2)"),
    ("763", "The Nuremberg Regime (3 of 6) - Rudolf Hess (1 of 4)"),
    ("766", "The Nuremberg Regime (4 of 6) - Rudolf Hess (2 of 4)"),
    ("770", "The Nuremberg Regime (5 of 6) - Rudolf Hess (3 of 4)"),
    ("773", "The Nuremberg Regime (6 of 6) - Rudolf Hess (4 of 4)"),
    ("777", "The Nuremberg Proceedings (1 of 3)"),
    ("780", "The Nuremberg Proceedings (2 of 3)"),
    ("783", "The Nuremberg Proceedings (3 of 3) - The Defendants"),
    ("788", "The Trial of Hermann Göring (1 of 2)"),
    ("794", "The Trial of Hermann Göring (2 of 2) - The Cross-Examination"),
    ("797", "The Verdicts at Nuremberg"),
    ("801", "Conclusion and Q&A"),
]


for old_filename in os.listdir():
    for i, (episode, name) in enumerate(chapters, start=1):
        title = f"Chapter {str(i).zfill(2)} - {name}"

        if title in old_filename:
            audiofile = eyed3.load(old_filename)

            tag = Tag()
            tag.track_num = i
            tag.title = title
            tag.artist = author
            tag.album = book
            tag.publisher = publisher
            audiofile.tag = tag
            audiofile.tag.save()

            if old_filename != title + ".mp3":
                audiofile.rename(title)
