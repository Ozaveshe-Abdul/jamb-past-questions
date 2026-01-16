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
4. Then within each main topic md file, let every subheading  be written and its questions written under it.

NOTE: this means categorization is (Main topic -> sub topic -> questions

### Step 3: Extract and Categorize Questions
1. Dont use automated script, read the question manually and categorize it. 
2. read the question text to identify:
   - Question numbers
   - Year markers (e.g., "2010 JAMB PHYSICS QUESTIONS")
   - Question text
   - Options (A, B, C, D), Make sure to write options on seperate lines
   - Diagram references (if any)
3. Match each question to its corresponding topic based on:
   - Content analysis (subject matter)
   - Keywords related to topics
4. Append categorized questions to the appropriate topic's `questions.md` file
5. Finish each topic before moving to the next.
6. Dont try to finish everything in one go, do 2 topics or more and take a break, dont overwhelm yourself by attempting to do everything once.
NOTE: dont use script read and write manually, disregard the time it will take.

### Step 4: Format Questions in Markdown
Each question should be formatted as:
```markdown
# [Topic Name]

# [Sub-topic Name]
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
1. Dont use scripts
2. Extract manually for maximum accuracy

### For Physics Syllabus
**Pending**

### For Chemistry Syllabus
**PENDING**: Chemistry syllabus PDF must be provided by user before topics can be extracted.

## Status Tracking

### Physics
- [x] Syllabus topics fully extracted (39 topics identified)
- [x] All topic folders created
- [ ] All questions categorized and written to markdown (59 questions categorized so far - 9/39 topics completed)
  - [x] Measurements and Units (7 questions)
  - [x] Scalars and Vectors (3 questions)
  - [x] Motion (19 questions)
  - [x] Gravitational Field (3 questions)
  - [x] Equilibrium of Forces (5 questions)
  - [x] Work, Energy and Power (9 questions)
  - [x] Friction (3 questions)
  - [x] Simple Machines (1 question)
  - [x] Elasticity: Hooke's Law and Young's Modulus (3 questions)
  - [ ] Pressure (0 questions)
  - [ ] Liquids At Rest (0 questions)
  - [ ] Temperature and Its Measurement (0 questions)
  - [ ] Thermal Expansion (0 questions)
  - [ ] Gas Laws (0 questions)
  - [ ] Quantity of Heat (0 questions)
  - [ ] Change of State (0 questions)
  - [ ] Vapours (0 questions)
  - [ ] Structure of Matter and Kinetic Theory (0 questions)
  - [ ] Heat Transfer (0 questions)
  - [ ] Waves (0 questions)
  - [ ] Propagation of Sound Waves (0 questions)
  - [ ] Characteristics of Sound Waves (0 questions)
  - [ ] Light Energy (0 questions)
  - [ ] Reflection of Light at Plane and Curved Surfaces (0 questions)
  - [ ] Refraction of Light Through at Plane and Curved Surfaces (0 questions)
  - [ ] Optical Instruments (0 questions)
  - [ ] Dispersion of light and colours (0 questions)
  - [ ] Electrostatics (0 questions)
  - [ ] Capacitors (0 questions)
  - [ ] Electric Cells (0 questions)
  - [ ] Current Electricity (0 questions)
  - [ ] Electrical Energy and Power (0 questions)
  - [ ] Magnets and Magnetic Fields (0 questions)
  - [ ] Force on a Current-Carrying Conductor in a Magnetic Field (0 questions)
  - [ ] Electromagnetic Induction (0 questions)
  - [ ] Simple A.C. Circuits (0 questions)
  - [ ] Conduction of Electricity Through Liquids (0 questions)
  - [ ] Elementary Modern Physics-Bohr's Theory (0 questions)
  - [ ] Introductory Electronics (0 questions)
- [ ] Diagrams handled appropriately (pending - using references only)
- [ ] Clean up garbled text (some questions have minor text issues due to PDF formatting)
- [ ] Review uncategorized questions and manually assign to topics
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
7. don't use script or any form of automation, read and write manually. Disregard the time it will take.
8. Dont't try to accoomplish everything in one go to maintain maximum accuraccy.
9. After each successful section/milestone document progress, so you or another agent instance can continue where you left
