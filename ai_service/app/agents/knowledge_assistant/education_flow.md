# Educational Workflow Loop

The Knowledge Assistant operates on a specific pedagogical loop designed to maximize retention and engagement.

## 1. Profile Extraction
Every request extracts or utilizes the `LearnerProfile` to determine the explanation depth (e.g., `ELI5`, `Beginner`, `Intermediate`, `Advanced`, `Expert`) and preferred learning styles.

## 2. Concept Deconstruction
Complex topics are broken down into:
- A high-level summary
- A detailed explanation matching the requested depth
- A real-world example
- A visual analogy

## 3. Cognitive Mapping
Before presenting isolated facts, the agent identifies prerequisite knowledge and structurally maps related concepts.

## 4. Assessment & Validation
The learning loop always ends with a verification step—typically a generated multiple-choice question testing the core concept just taught.

## 5. Forward Momentum
The agent doesn't leave the user at a dead end. It calculates a structured `LearningPath` detailing the immediate next steps and provides ranked `ResourceRecommendations` (labs, articles) with rationales.
