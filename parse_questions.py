import re
import sys


def parse_questions(text):
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
        q_match = re.match(r"^(\d+)\.\s+(.+)", line)
        if q_match:
            # Save previous question if exists
            if current_question:
                questions.append(current_question)

            # Start new question
            q_num = q_match.group(1)
            q_text = q_match.group(2)
            current_question = {
                "number": q_num,
                "year": current_year,
                "text": q_text,
                "options": {"A": None, "B": None, "C": None, "D": None},
                "diagram_ref": None,
            }
            i += 1
            continue

        # Detect options
        if current_question:
            option_match = re.match(r"^([A-D])\.\s+(.+)", line)
            if option_match:
                opt = option_match.group(1)
                opt_text = option_match.group(2)
                current_question["options"][opt] = opt_text
                i += 1
                continue

            # Add continuation to question text
            if line and not line.startswith(
                ("A.", "B.", "C.", "D.", str(current_question["number"] + ". "))
            ):
                current_question["text"] += " " + line

        i += 1

    # Add last question
    if current_question:
        questions.append(current_question)

    return questions


def categorize_question(question):
    text = question["text"].lower()

    # Keywords for each topic
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
        ],
        "Friction": [
            "friction",
            "coefficient",
            "viscosity",
            "terminal",
            "lubricant",
            "rough",
            "smooth",
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
        ],
        "Quantity-of-Heat": [
            "heat",
            "specific heat",
            "capacity",
            "calorimeter",
            "latent",
            "joule",
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
        ],
        "Vapours": ["vapour", "saturated", "relative humidity", "dew point"],
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
        ],
        "Reflection-of-Light-at-Plane-and-Curved-Surfaces": [
            "reflection",
            "mirror",
            "plane",
            "concave",
            "convex",
            "image",
            "focal",
        ],
        "Refraction-of-Light-Through-at-Plane-and-Curved-Surfaces": [
            "refraction",
            "lens",
            "convex",
            "concave",
            "prism",
            "refractive index",
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
        ],
        "Electrostatics": [
            "charge",
            "electron",
            "proton",
            "coulomb",
            "electric field",
            "potential",
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
        ],
        "Electrical-Energy-and-Power": [
            "electrical power",
            "kilowatt",
            "kilowatt-hour",
            "energy",
            "watt",
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
        ],
        "Conduction-of-Electricity-Through-Liquids": [
            "electrolysis",
            "electrolyte",
            "ion",
            "anode",
            "cathode",
            "faraday law",
        ],
        "Elementary-Modern-Physics-Bohrs-Theory": [
            "bohr",
            "atom",
            "electron orbit",
            "quantum",
            "photoelectric",
            "x-ray",
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
    with open("/tmp/physics-pastq-layout.txt", "r") as f:
        text = f.read()

    questions = parse_questions(text)

    # Print first 10 questions for testing
    print(f"Found {len(questions)} questions\n")
    for q in questions[:10]:
        print(f"Question {q['number']} ({q['year']})")
        print(f"Text: {q['text'][:100]}...")
        print(
            f"Options: A: {q['options']['A'][:30] if q['options']['A'] else 'None'}..."
        )
        category = categorize_question(q)
        print(f"Category: {category}")
        print()


if __name__ == "__main__":
    main()
