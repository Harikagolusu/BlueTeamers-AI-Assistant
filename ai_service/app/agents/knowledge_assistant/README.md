# Knowledge Assistant Agent

The **Knowledge Assistant Agent** is a production product agent designed for educational purposes. It explains complex cybersecurity concepts, generates learning paths, assesses user knowledge, and recommends targeted resources, entirely adapting to the user's specific `LearnerProfile`.

## Core Capabilities
- **Concept Explanation**: Explains concepts using appropriate depth, real-world examples, and visual analogies.
- **Concept Mapping**: Identifies prerequisites and related learning topics.
- **Knowledge Retrieval**: Searches internal documentation and vectors for context.
- **Learning Path Generation**: Builds personalized curriculum goals based on known and weak topics.
- **Knowledge Assessment**: Generates targeted multiple-choice questions to test understanding.
- **Resource Recommendation**: Provides ranked suggestions for labs, articles, and documentation.

## Usage
The agent operates via the platform's Workflow Engine and orchestration layer. It exposes the `EDUCATION` capability.
