import re
import os


def simple_parse(text):
    questions = []
    lines = text.split("\n")

    current_question = None
    current_year = None

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
        q_match = re.match(r"^(\d+)\.\s*(.+)", line)
        if q_match:
            # Save previous question
            if current_question and len(current_question["text"]) > 20:
                questions.append(current_question)

            q_num = q_match.group(1)
            q_text = q_match.group(2).strip()

            # Only start new question if text is substantial
            if len(q_text) > 5:
                current_question = {
                    "number": q_num,
                    "year": current_year,
                    "text": q_text,
                    "options": {"A": None, "B": None, "C": None, "D": None},
                    "diagram_ref": None,
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
                current_question["text"] += " " + line

        i += 1

    if current_question and len(current_question["text"]) > 20:
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


def write_questions_to_markdown(questions, base_path):
    # Organize questions by topic
    categorized = {}
    for q in questions:
        category = categorize_question(q)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(q)

    # Write questions to each topic's markdown file
    for topic, topic_questions in categorized.items():
        topic_path = os.path.join(base_path, topic, "questions.md")

        # Check if file exists
        if os.path.exists(topic_path):
            # Read existing content
            with open(topic_path, "r") as f:
                existing_content = f.read()

            # Append new questions
            with open(topic_path, "a") as f:
                question_num = len(
                    [
                        line
                        for line in existing_content.split("\n")
                        if line.startswith("## Question")
                    ]
                )
                for q in topic_questions:
                    question_num += 1
                    f.write(
                        f"\n## Question {question_num} ({q['year']}: Q{q['number']})\n"
                    )
                    f.write(f"{q['text']}\n\n")
                    f.write("Options:\n")
                    for opt, opt_text in q["options"].items():
                        if opt_text:
                            f.write(f"{opt}. {opt_text}\n")
                    if q["diagram_ref"]:
                        f.write(f"\n{q['diagram_ref']}\n")
                    f.write("\n---\n")
        else:
            # Create new file
            with open(topic_path, "w") as f:
                topic_name = topic.replace("-", " ")
                f.write(f"# {topic_name}\n\n")
                question_num = 0
                for q in topic_questions:
                    question_num += 1
                    f.write(
                        f"## Question {question_num} ({q['year']}: Q{q['number']})\n"
                    )
                    f.write(f"{q['text']}\n\n")
                    f.write("Options:\n")
                    for opt, opt_text in q["options"].items():
                        if opt_text:
                            f.write(f"{opt}. {opt_text}\n")
                    if q["diagram_ref"]:
                        f.write(f"\n{q['diagram_ref']}\n")
                    f.write("\n---\n")

        print(f"Written {len(topic_questions)} questions to {topic}/questions.md")

    # Handle uncategorized
    if "Uncategorized" in categorized:
        print(
            f"\nNote: {len(categorized['Uncategorized'])} questions could not be categorized automatically"
        )


def main():
    with open("/tmp/physics-pastq-nolayout.txt", "r") as f:
        text = f.read()

    questions = simple_parse(text)
    print(f"Parsed {len(questions)} questions\n")

    base_path = "/home/ozaveshe-abdul/Documents/jamb-past-questions/Categorized-Questions/Physics"
    write_questions_to_markdown(questions, base_path)


if __name__ == "__main__":
    main()
