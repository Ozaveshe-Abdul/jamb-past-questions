import re


def parse_interleaved_questions(text):
    questions = []
    lines = text.split("\n")

    # Track two streams for left and right columns
    left_stream = []
    right_stream = []
    current_year = None

    for line in lines:
        line = line.strip()

        # Detect year marker
        year_match = re.match(r"^(\d{4})\s+JAMB\s+(\w+)\s+QUESTIONS", line)
        if year_match:
            current_year = year_match.group(1)
            continue

        # Detect question number (indicates new question)
        q_match = re.match(r"^(\d+)\.\s*(.*)", line)
        if q_match:
            # Save any complete questions
            if left_stream:
                questions.append(process_stream(left_stream, current_year))
                left_stream = []
            if right_stream:
                questions.append(process_stream(right_stream, current_year))
                right_stream = []

            q_num = q_match.group(1)
            q_text = q_match.group(2).strip()

            # Determine which column (alternating pattern based on what we've seen)
            # This is a heuristic - we alternate between left and right
            if len(questions) % 2 == 0:
                left_stream = [(q_num, q_text)]
            else:
                right_stream = [(q_num, q_text)]
            continue

        # Detect options
        opt_match = re.match(r"^([A-D])\.\s*(.*)", line)
        if opt_match:
            opt = opt_match.group(1)
            opt_text = opt_match.group(2).strip()
            if len(questions) % 2 == 0 and left_stream:
                add_option(left_stream, opt, opt_text)
            elif right_stream:
                add_option(right_stream, opt, opt_text)
            continue

    # Process remaining streams
    if left_stream:
        questions.append(process_stream(left_stream, current_year))
    if right_stream:
        questions.append(process_stream(right_stream, current_year))

    return questions


def process_stream(stream, year):
    if not stream:
        return None

    num, text = stream[0]
    options = {"A": None, "B": None, "C": None, "D": None}

    for item in stream[1:]:
        if len(item) == 2 and item[0] in ["A", "B", "C", "D"]:
            options[item[0]] = item[1]

    return {
        "number": num,
        "year": year,
        "text": text,
        "options": options,
        "diagram_ref": None,
    }


def add_option(stream, opt, text):
    stream.append((opt, text))


def simple_parse(text):
    """Simpler parser that just extracts numbered questions sequentially"""
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

        # Detect question number (only if it looks like a new question start)
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
            # Check for options
            opt_match = re.match(r"^([A-D])\.\s*(.+)", line)
            if opt_match:
                opt = opt_match.group(1)
                opt_text = opt_match.group(2).strip()
                current_question["options"][opt] = opt_text
            elif line and not line.startswith(str(current_question["number"])):
                # Add to question text
                current_question["text"] += " " + line

        i += 1

    # Add last question
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
        ],
        "Equilibrium-of-Forces": [
            "equilibrium",
            "moment",
            "couple",
            "force",
            "resultant",
            "parallel",
            "perpendicular",
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
        "Vapours": ["vapour", "saturated", "relative humidity", "dew point", "droplet"],
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


def main():
    with open("/tmp/physics-pastq-nolayout.txt", "r") as f:
        text = f.read()

    questions = simple_parse(text)

    print(f"Found {len(questions)} questions\n")

    # Print first 20 questions with their categories
    for q in questions[:20]:
        category = categorize_question(q)
        print(f"Q{q['number']} ({q['year']}): {category}")
        print(f"Text: {q['text'][:80]}...")
        print(
            f"Options: A={q['options']['A'][:20] if q['options']['A'] else 'None'}..."
            if q["options"]["A"]
            else "Options: Incomplete"
        )
        print()


if __name__ == "__main__":
    main()
