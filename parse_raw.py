import re
import os
from collections import defaultdict


def parse_raw_questions(text):
    """Parse questions from raw PDF text extraction"""
    questions = []
    lines = text.split("\n")

    current_question = None
    current_year = None
    current_question_number = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Detect year marker
        year_match = re.match(r"^(\d{4})\s+JAMB\s+(\w+)\s+QUESTIONS", line)
        if year_match:
            current_year = year_match.group(1)
            i += 1
            continue

        # Detect question number at start of line
        q_match = re.match(r"^(\d+)\.\s*(.*)", line)
        if q_match:
            # Save previous question
            if current_question and len(current_question["text"]) > 5:
                questions.append(current_question)

            q_num = q_match.group(1)
            q_text = q_match.group(2).strip() if q_match.group(2) else ""

            # Check if this is just a number with no text (continuation reference)
            if not q_text:
                current_question = {
                    "number": q_num,
                    "year": current_year,
                    "text": "",
                    "options": {"A": None, "B": None, "C": None, "D": None},
                }
                i += 1
                continue

            current_question = {
                "number": q_num,
                "year": current_year,
                "text": q_text,
                "options": {"A": None, "B": None, "C": None, "D": None},
            }
            i += 1
            continue

        # Check for diagram reference (just a number that references a diagram)
        if current_question and line.isdigit():
            # This might be a diagram reference, skip
            i += 1
            continue

        # Add to current question
        if current_question:
            # Check for options
            opt_match = re.match(r"^([A-D])\.\s*(.+)", line)
            if opt_match:
                opt = opt_match.group(1)
                opt_text = opt_match.group(2).strip()
                current_question["options"][opt] = opt_text
            elif line:
                # Add continuation to question text
                if current_question["text"]:
                    current_question["text"] += " " + line
                else:
                    current_question["text"] = line

        i += 1

    # Add last question
    if current_question and len(current_question["text"]) > 5:
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
            "undulating",
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
        if len(q["text"]) > 10:  # Only include questions with meaningful text
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
    raw_path = "/tmp/physics-raw.txt"
    base_path = "/home/ozaveshe-abdul/Documents/jamb-past-questions/Categorized-Questions/Physics"

    # Read raw text
    with open(raw_path, "r") as f:
        text = f.read()

    # Parse questions
    questions = parse_raw_questions(text)
    print(f"Parsed {len(questions)} questions from raw text")

    # Print some sample questions
    print("\nSample questions:")
    for i, q in enumerate(questions[:10]):
        category = categorize_question(q)
        print(f"  Q{q['number']} ({q['year']}): {category[:50]}...")
        if i < 3:
            print(f"    Text: {q['text'][:80]}...")

    # Write to markdown files
    write_questions_to_markdown(questions, base_path, overwrite=True)


if __name__ == "__main__":
    main()
