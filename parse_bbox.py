import re
import os
from collections import defaultdict


def parse_bbox_html(html_path):
    with open(html_path, "r") as f:
        html_content = f.read()

    words = []
    word_pattern = r'<word xMin="([^"]+)" yMin="([^"]+)" xMax="([^"]+)" yMax="([^"]+)">([^<]+)</word>'

    for match in re.finditer(word_pattern, html_content):
        x_min = float(match.group(1))
        y_min = float(match.group(2))
        x_max = float(match.group(3))
        y_max = float(match.group(4))
        text = match.group(5)
        words.append(
            {
                "x_min": x_min,
                "y_min": y_min,
                "x_max": x_max,
                "y_max": y_max,
                "text": text,
                "y_center": (y_min + y_max) / 2,
            }
        )

    return words


def separate_columns(words, page_width=595.56):
    """Separate words into left and right columns based on x-coordinate"""
    left_column = []
    right_column = []

    for word in words:
        x_center = (word["x_min"] + word["x_max"]) / 2
        if x_center < page_width / 2:
            left_column.append(word)
        else:
            right_column.append(word)

    return left_column, right_column


def reconstruct_text(column_words):
    """Reconstruct text from column words by grouping by y-coordinate"""
    # Group words by line (similar y-coordinates)
    lines = defaultdict(list)

    for word in column_words:
        # Round y to nearest integer for line grouping
        y_line = int(word["y_center"])
        lines[y_line].append(word)

    # Sort lines by y-coordinate (top to bottom)
    sorted_lines = sorted(lines.items(), key=lambda x: x[0])

    text_lines = []
    for y, words_in_line in sorted_lines:
        # Sort words in line by x-coordinate (left to right)
        words_in_line.sort(key=lambda w: w["x_min"])
        line_text = " ".join(w["text"] for w in words_in_line)
        text_lines.append(line_text)

    return "\n".join(text_lines)


def extract_year_from_page(text):
    """Extract year marker from page text"""
    year_match = re.search(r"(\d{4})\s+JAMB\s+(\w+)\s+QUESTIONS", text)
    if year_match:
        return year_match.group(1)
    return None


def parse_questions_from_text(text):
    """Parse questions from column text"""
    questions = []
    lines = text.split("\n")

    current_question = None
    current_year = extract_year_from_page(text)

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Detect year marker
        year_match = re.match(r"^(\d{4})\s+JAMB\s+(\w+)\s+QUESTIONS", line)
        if year_match:
            current_year = year_match.group(1)
            i += 1
            continue

        # Detect question number
        q_match = re.match(r"^(\d+)\.\s*(.*)", line)
        if q_match:
            # Save previous question
            if current_question and len(current_question["text"]) > 10:
                questions.append(current_question)

            q_num = q_match.group(1)
            q_text = q_match.group(2).strip()

            if len(q_text) > 5:
                current_question = {
                    "number": q_num,
                    "year": current_year,
                    "text": q_text,
                    "options": {"A": None, "B": None, "C": None, "D": None},
                }
            i += 1
            continue

        # Add to current question
        if current_question:
            opt_match = re.match(r"^([A-D])\.\s*(.+)", line)
            if opt_match:
                opt = opt_match.group(1)
                opt_text = opt_match.group(2).strip()
                current_question["options"][opt] = opt_text
            elif line and not line.startswith(str(current_question["number"])):
                # Add continuation to question text
                current_question["text"] += " " + line

        i += 1

    # Add last question
    if current_question and len(current_question["text"]) > 10:
        questions.append(current_question)

    return questions


def categorize_question(question):
    text = question["text"].lower()

    topics = {
        "Measurements-and-Units": [
            "metre",
            "vernier",
            "micrometer",
            "screw",
            "measuring cylinder",
            "mass",
            "weight",
            "balance",
            "time",
            "second",
            "unit",
            "fundamental",
            "derived",
            "weighed",
            "weighing",
        ],
        "Limitations-of-Experimental-Measurements": [
            "accuracy",
            "error",
            "significant",
            "standard form",
            "limitation",
        ],
        "Motion": [
            "velocity",
            "speed",
            "acceleration",
            "distance",
            "displacement",
            "uniform",
            "non-uniform",
            "graph",
            "velocity-time",
            "kmh",
            "ms-1",
            "ms-2",
            "car moves",
            "decelerates",
            "accelerates",
            "constant speed",
            "deceleration",
        ],
        "Gravitational-Field": [
            "gravitational",
            "gravity",
            "g",
            "escape velocity",
            "orbit",
            "weightless",
            "planet",
            "earth",
            "moon",
            "thunderstorm",
            "lightning",
        ],
        "Equilibrium-of-Forces": [
            "equilibrium",
            "moment",
            "couple",
            "force",
            "resultant",
            "parallel",
            "perpendicular",
            "stable equilibrium",
        ],
        "Work-Energy-and-Power": [
            "work",
            "energy",
            "power",
            "joule",
            "watt",
            "kinetic",
            "potential",
            "conservation",
            "machine",
            "velocity ratio",
            "effort",
            "load",
        ],
        "Friction": [
            "friction",
            "coefficient",
            "viscosity",
            "terminal",
            "lubricant",
            "rough",
            "smooth",
            "conveyor belts",
        ],
        "Elasticity-Hookes-Law-and-Youngs-Modulus": [
            "elastic",
            "hooke",
            "young",
            "modulus",
            "extension",
            "spring",
            "deformation",
            "stress",
            "strain",
            "wire extended",
            "wire of length",
        ],
        "Pressure": ["pressure", "pascal", "barometer", "manometer", "atmospheric"],
        "Liquids-At-Rest": [
            "liquid",
            "hydraulic",
            "piston",
            "u-tube",
            "density",
            "buoyancy",
            "archimedes",
            "hydrometer",
            "mercury",
            "alcohol",
            "water over mercury",
        ],
        "Temperature-and-Its-Measurement": [
            "temperature",
            "thermometer",
            "celsius",
            "kelvin",
            "fahrenheit",
            "thermocouple",
        ],
        "Thermal-Expansion": [
            "expansion",
            "linear",
            "area",
            "volume",
            "expansivity",
            "bimetallic",
            "heated through temperature",
        ],
        "Gas-Laws": [
            "boyle",
            "charles",
            "pressure",
            "volume",
            "temperature",
            "ideal gas",
            "pv=nrt",
            "gas law",
            "mole of gas",
        ],
        "Quantity-of-Heat": [
            "heat",
            "specific heat",
            "capacity",
            "calorimeter",
            "latent",
            "joule",
            "radiated",
            "calorimetric",
        ],
        "Change-of-State": [
            "melting",
            "freezing",
            "boiling",
            "evaporation",
            "condensation",
            "sublimation",
            "solid",
            "liquid",
            "gas",
            "ice",
        ],
        "Vapours": [
            "vapour",
            "saturated",
            "relative humidity",
            "dew point",
            "droplet",
            "condensation",
            "evaporation",
        ],
        "Structure-of-Matter-and-Kinetic-Theory": [
            "atom",
            "molecule",
            "kinetic theory",
            "brownian",
            "solid",
            "liquid",
            "gas structure",
        ],
        "Heat-Transfer": [
            "conduction",
            "convection",
            "radiation",
            "insulator",
            "conductor",
            "heat transfer",
        ],
        "Waves": [
            "wave",
            "transverse",
            "longitudinal",
            "wavelength",
            "frequency",
            "amplitude",
            "period",
            "wave equation",
        ],
        "Propagation-of-Sound-Waves": [
            "sound",
            "audible",
            "ultrasonic",
            "infrasonic",
            "speed of sound",
            "electric bell",
        ],
        "Characteristics-of-Sound-Waves": [
            "pitch",
            "loudness",
            "quality",
            "intensity",
            "echo",
            "reverberation",
        ],
        "Light-Energy": [
            "light",
            "ray",
            "beam",
            "velocity",
            "refraction index",
            "snell",
            "total internal reflection",
        ],
        "Reflection-of-Light-at-Plane-and-Curved-Surfaces": [
            "reflection",
            "mirror",
            "plane",
            "concave",
            "convex",
            "image",
            "focal",
            "mirror formula",
        ],
        "Refraction-of-Light-Through-at-Plane-and-Curved-Surfaces": [
            "refraction",
            "lens",
            "convex",
            "concave",
            "prism",
            "refractive index",
            "critical angle",
        ],
        "Optical-Instruments": [
            "microscope",
            "telescope",
            "camera",
            "eye",
            "magnifying",
            "projector",
        ],
        "Dispersion-of-light-and-colours": [
            "dispersion",
            "spectrum",
            "rainbow",
            "prism",
            "colour",
            "primary",
            "white light",
        ],
        "Electrostatics": [
            "charge",
            "electron",
            "proton",
            "coulomb",
            "electric field",
            "potential",
            "charged rod",
        ],
        "Capacitors": [
            "capacitor",
            "capacitance",
            "farad",
            "dielectric",
            "parallel plate",
        ],
        "Electric-Cells": [
            "cell",
            "battery",
            "emf",
            "electromotive",
            "terminal",
            "primary",
            "secondary",
            "internal resistance",
        ],
        "Current-Electricity": [
            "current",
            "ammeter",
            "voltmeter",
            "resistance",
            "ohm",
            "ohm's law",
            "series",
            "parallel",
            "circuit",
        ],
        "Electrical-Energy-and-Power": [
            "electrical power",
            "kilowatt",
            "kilowatt-hour",
            "energy",
            "watt",
            "transmitted",
        ],
        "Magnets-and-Magnetic-Fields": [
            "magnet",
            "magnetic field",
            "north",
            "south",
            "pole",
            "domain",
        ],
        "Force-on-a-Current-Carrying-Conductor-in-a-Magnetic-Field": [
            "motor",
            "moving coil",
            "magnetic force",
            "fleming",
        ],
        "Electromagnetic-Induction": [
            "induction",
            "lenz",
            "faraday",
            "transformer",
            "generator",
            "flux",
        ],
        "Simple-A-C-Circuits": [
            "alternating",
            "a.c.",
            "rms",
            "peak",
            "frequency",
            "inductor",
            "capacitor reactance",
            "a.c. circuit",
        ],
        "Conduction-of-Electricity-Through-Liquids": [
            "electrolysis",
            "electrolyte",
            "ion",
            "anode",
            "cathode",
            "faraday law",
            "discharge tube",
        ],
        "Elementary-Modern-Physics-Bohrs-Theory": [
            "bohr",
            "atom",
            "electron orbit",
            "quantum",
            "photoelectric",
            "x-ray",
            "ground state",
            "radioisotope",
            "nuclear",
        ],
        "Introductory-Electronics": [
            "transistor",
            "diode",
            "semiconductor",
            "pn junction",
            "rectifier",
            "amplifier",
        ],
    }

    best_topic = None
    best_score = 0

    for topic, keywords in topics.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_topic = topic

    return best_topic if best_topic else "Uncategorized"


def write_questions_to_markdown(questions, base_path, overwrite=True):
    """Organize and write questions to markdown files"""
    # Clear existing files if overwrite
    if overwrite:
        for topic_dir in os.listdir(base_path):
            questions_path = os.path.join(base_path, topic_dir, "questions.md")
            if os.path.exists(questions_path):
                topic_name = topic_dir.replace("-", " ")
                with open(questions_path, "w") as f:
                    f.write(f"# {topic_name}\n\n")

    # Organize questions by topic
    categorized = defaultdict(list)
    for q in questions:
        category = categorize_question(q)
        categorized[category].append(q)

    # Write questions to each topic's markdown file
    for topic, topic_questions in categorized.items():
        topic_path = os.path.join(base_path, topic, "questions.md")

        if not os.path.exists(topic_path):
            print(f"Warning: {topic_path} does not exist, skipping")
            continue

        # Read existing content to get current question count
        with open(topic_path, "r") as f:
            existing_content = f.read()

        question_num = len(
            [
                line
                for line in existing_content.split("\n")
                if line.startswith("## Question")
            ]
        )

        # Append new questions
        with open(topic_path, "a") as f:
            for q in topic_questions:
                question_num += 1
                f.write(f"## Question {question_num} ({q['year']}: Q{q['number']})\n")
                f.write(f"{q['text']}\n\n")
                f.write("Options:\n")
                for opt, opt_text in q["options"].items():
                    if opt_text:
                        f.write(f"{opt}. {opt_text}\n")
                f.write("\n---\n")

        print(f"Written {len(topic_questions)} questions to {topic}/questions.md")

    # Handle uncategorized
    if "Uncategorized" in categorized:
        print(
            f"\nNote: {len(categorized['Uncategorized'])} questions could not be categorized automatically"
        )


def main():
    html_path = "/tmp/physics-bbox.html"
    base_path = "/home/ozaveshe-abdul/Documents/jamb-past-questions/Categorized-Questions/Physics"

    # Parse bbox HTML
    words = parse_bbox_html(html_path)
    print(f"Extracted {len(words)} words from PDF")

    # Separate into columns
    left_col, right_col = separate_columns(words)
    print(f"Left column: {len(left_col)} words, Right column: {len(right_col)} words")

    # Reconstruct text for each column
    left_text = reconstruct_text(left_col)
    right_text = reconstruct_text(right_col)

    # Parse questions from each column
    left_questions = parse_questions_from_text(left_text)
    right_questions = parse_questions_from_text(right_text)

    print(f"\nParsed {len(left_questions)} questions from left column")
    print(f"Parsed {len(right_questions)} questions from right column")

    # Combine questions from both columns
    all_questions = left_questions + right_questions
    print(f"Total questions: {len(all_questions)}")

    # Print some sample questions
    print("\nSample questions:")
    for i, q in enumerate(all_questions[:5]):
        category = categorize_question(q)
        print(f"  Q{q['number']} ({q['year']}): {category[:50]}...")

    # Write to markdown files
    write_questions_to_markdown(all_questions, base_path, overwrite=True)


if __name__ == "__main__":
    main()
