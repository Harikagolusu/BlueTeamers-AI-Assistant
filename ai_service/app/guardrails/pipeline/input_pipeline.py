from app.guardrails.pipeline.base_pipeline import BasePipeline

class InputPipeline(BasePipeline):
    def __init__(self):
        super().__init__(name="InputGuardrails")
