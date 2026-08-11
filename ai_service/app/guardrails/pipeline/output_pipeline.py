from app.guardrails.pipeline.base_pipeline import BasePipeline

class OutputPipeline(BasePipeline):
    def __init__(self):
        super().__init__(name="OutputGuardrails")
