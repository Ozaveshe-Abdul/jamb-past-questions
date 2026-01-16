# Agent Guidelines for JAMB Past Questions Categorization

## Critical Rules

### 1. NEVER Assume or Create Content
- **STRICTLY FORBIDDEN**: Do NOT assume, infer, or create topics, questions, or answers from external knowledge
- **ONLY USE** information explicitly stated in the provided:
  - Syllabus PDF for that subject
  - Past Questions PDF for that subject
- If information is unclear or ambiguous, leave it as-is or note the uncertainty

### 2. Check Required Files Before Starting
Before working on any subject, verify both files exist:
- `[Subject]-syllabus.pdf`
- `[Subject]pastQ.pdf` (or similar naming)

If either file is missing:
- **STOP IMMEDIATELY**
- **ASK THE USER** to provide the missing file
- Do NOT proceed with any work on that subject

### 3. Always Read plan.md First
When prompted for this task:
1. **MUST** read `plan.md` first to understand the current state and workflow
2. Follow the documented steps in order
3. Update the status tracking section as work progresses
4. Do not skip steps or deviate from the plan without user confirmation

### 4. Topic Extraction from Syllabus
- Extract ONLY what is explicitly written in the syllabus
- If a numbered section has no clear topic name (e.g., just "1." or "20."), mark it as `[Topic X - needs extraction]` and note the line number
- Do not invent topic names or content
- Preserve exact topic naming conventions (capitalization, wording)

### 5. Question Categorization
- Match questions to topics based ONLY on the content or context in the question 
- Do NOT assume context or create connections not present in the question
- If a question's topic is unclear, you may:
  - Mark it with `[Uncategorized - needs review]`
  - Ask the user for guidance
- Never assign questions to topics arbitrarily

### 6. Question Formatting Requirements
Each question MUST include:
- Sequential numbering within its topic
- Original year and question number in brackets: `(Year: Q#)`
- Full question text exactly as appears in PDF
- All options (A, B, C, D) as written. Each option should be on a seperate line
- Diagram reference if applicable

Format:
```markdown
## Question [N] ([Year]: Q[Q#])
[Question text]

Options:
A. [Option text]
B. [Option text]
C. [Option text]
D. [Option text]

[Diagram reference if needed]
```

### 7. Diagram Handling
- First attempt: Check if diagram can be extracted and embedded
  - Use appropriate tools to crop/extract images
  - Embed using markdown image syntax: `![Diagram description](path/to/image)`
- Fallback: Add reference note
  - Format: `[Diagram reference: See original PDF, [Year] [Subject] Question [Number]]`
- Never attempt to describe diagrams in text

### 8. Folder Structure
Create folders with descriptive, hyphenated names:
```
Categorized-Questions/
└── [Subject]/
    └── [Topic-Name]/
        └── questions.md
```

Examples:
- `Measurements-and-Units/`
- `Elasticity-Hookes-Law-and-Youngs-Modulus/`
- `Propagation-of-Sound-Waves/`

### 9. Workflow Order
Follow steps sequentially as outlined in plan.md:
1. Extract topic structure from syllabus
2. Create folder structure
3. Extract and categorize questions
4. Format questions in markdown
5. Handle diagrams

Do not skip ahead or reverse the order.

### 10. Status Updates
After completing each major step:
1. Update the status tracking section in `plan.md`
2. Mark completed items with `[x]`
3. Note any issues encountered
4. Provide summary to user

### 11. Error Handling
If you encounter issues:
- Syllabus parsing errors: Note the line number and issue in `plan.md`, continue if possible
- Question parsing errors: Flag the question for review, continue with others
- Missing information: Do NOT invent; ask user for clarification

### 12. Verification
Before considering work complete:
1. Verify all questions from the PDF have been categorized
2. Verify each topic has a questions.md file (even if empty)
3. Verify formatting is consistent across all files
4. Verify plan.md status is updated

## Prohibited Actions

❌ Creating topics not in the syllabus
❌ Creating questions not in the past questions PDF
❌ Using external knowledge sources for topics or questions
❌ Making assumptions about ambiguous content
❌ Skipping the plan.md read step on first prompt
❌ Proceeding without required PDFs
❌ Inventing syllabus content for missing files
❌ Describing diagrams in text (use references only)

## Required Actions

✅ Read `plan.md` on first prompt
✅ Check for required PDFs before starting
✅ Ask user for missing files
✅ Extract ONLY from provided PDFs
✅ Follow workflow order
✅ Update status tracking
✅ Format questions consistently
✅ Handle diagrams appropriately (embed or reference)
