# JAMB Past Questions Categorization Plan

## Objective
Categorize JAMB past questions by topics according to the subject syllabus to organize questions for better study and reference.

## Current Repository Structure
```
jamb-past-questions/
├── ChemistrypastQ.pdf
├── Physics-pastQ.pdf
├── Physics-syllabus.pdf
├── Categorized-Questions/
│   └── Physics/ (39 topic folders with questions.md files)
├── plan.md (this file)
└── AGENT.md
```

## Required Files for Each Subject
- Syllabus PDF (defines topics and subtopics)
- Past Questions PDF (contains actual questions from various years)

**Note**: Chemistry syllabus PDF is missing and must be provided by the user.

## Workflow Steps

### Step 1: Extract Topic Structure from Syllabus
1. Use `pdftotext` to convert syllabus PDF to text
2. Identify all main topics (numbered sections like "1.", "2.", "3. Motion", etc.)
3. Extract topic names, creating clean folder-safe names
4. Document each topic with its line reference in the syllabus

### Step 2: Create Folder Structure
For each subject:
1. Create a main folder in `Categorized-Questions/` for the subject (e.g., `Categorized-Questions/Physics/`)
2. For each main topic, create a subfolder (e.g., `Categorized-Questions/Physics/Measurements-and-Units/`)
3. Inside each topic folder, create a `questions.md` file with the topic name as the header

### Step 3: Extract and Categorize Questions
1. Use `pdftotext` to convert past questions PDF to text
2. Parse the extracted text to identify:
   - Question numbers
   - Year markers (e.g., "2010 JAMB PHYSICS QUESTIONS")
   - Question text
   - Options (A, B, C, D)
   - Diagram references (if any)
3. Match each question to its corresponding topic based on:
   - Content analysis (subject matter)
   - Keywords related to topics
4. Append categorized questions to the appropriate topic's `questions.md` file

### Step 4: Format Questions in Markdown
Each question should be formatted as:
```markdown
# [Topic Name]

## Question 1 (2010: Q5)
[Question text here]

Options:
A. [Option A]
B. [Option B]
C. [Option C]
D. [Option D]

[Diagram reference if applicable: *See original PDF, 2010 Physics Question 5*]
```

### Step 5: Handle Diagrams
- If possible to crop and embed: Extract diagrams and embed in markdown using image syntax
- If not possible: Add reference note: `[Diagram reference: See original PDF, [Year] [Subject] Question [Number]]`

## Topic Extraction Rules

### For Physics Syllabus
Main topics identified:
1. Measurements and Units
2. Limitations of Experimental Measurements
3. Motion
4. Gravitational Field
5. Equilibrium of Forces
6. Work, Energy and Power
7. Friction
8. Friction (continuation with viscosity)
9. Elasticity: Hooke's Law and Young's Modulus
10. Pressure
11. Liquids At Rest
12. Temperature and Its Measurement
13. Thermal Expansion
14. Gas Laws
15. Quantity of Heat
16. Change of State
17. Vapours
18. Structure of Matter and Kinetic Theory
19. Heat Transfer
20. Waves
21. Propagation of Sound Waves
22. Characteristics of Sound Waves
23. Light Energy
24. Reflection of Light at Plane and Curved Surfaces
25. Refraction of Light Through at Plane and Curved Surfaces
26. Optical Instruments
27. Dispersion of light and colours
28. Electrostatics
29. Capacitors
30. Electric Cells
31. Current Electricity
32. Electrical Energy and Power
33. Magnets and Magnetic Fields
34. Force on a Current-Carrying Conductor in a Magnetic Field
35. Electromagnetic Induction
36. Simple A.C. Circuits
37. Conduction of Electricity Through Liquids
38. Elementary Modern Physics-Bohr's Theory
39. Introductory Electronics

### For Chemistry Syllabus
**PENDING**: Chemistry syllabus PDF must be provided by user before topics can be extracted.

## Status Tracking

### Physics
- [x] Syllabus topics fully extracted (39 topics identified)
- [x] All topic folders created
- [x] All questions categorized and written to markdown (486 questions parsed using raw text extraction, significantly improved quality)
- [ ] Diagrams handled appropriately (pending - using references only)
- [ ] Clean up garbled text (some questions have minor text issues due to PDF formatting)
- [ ] Review uncategorized questions and manually assign to topics (68 questions currently in Uncategorized, many are answer keys or fragments)
- [ ] Verify all questions are correctly categorized and remove any misassigned ones

### Chemistry
- [ ] Syllabus PDF received from user (MISSING - must be provided)
- [ ] Syllabus topics extracted
- [ ] All topic folders created
- [ ] All questions categorized and written to markdown
- [ ] Diagrams handled appropriately

## Known Issues
1. PDF text extraction has mixed content from columns, causing some question text to be garbled
2. Some questions appear duplicated due to column parsing
3. 68 questions could not be automatically categorized and are in the Uncategorized folder
4. Diagrams are not embedded (only references provided)

## Next Steps for Physics
1. Review and manually categorize uncategorized questions
2. Remove duplicate questions
3. Consider manual cleanup of garbled question text
4. Attempt to extract and embed diagrams if possible

## Important Notes
1. Never infer, assume, or create topics/questions from external knowledge
2. Only use information from the provided syllabus and past question PDFs
3. Always number questions sequentially within each topic
4. Always append original question year and number in brackets after each question
5. Ask user if syllabus or past questions PDF is missing for any subject
6. Maintain clean folder structure with descriptive, hyphenated names
