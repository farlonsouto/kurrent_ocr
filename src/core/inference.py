import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel


class KurrentInference:
    def __init__(self):
        # Portable device detection
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_id = "dh-unibe/trocr-kurrent-XVI-XVII"

        print(f"Loading model to {self.device}...")
        self.processor = TrOCRProcessor.from_pretrained(self.model_id)
        self.model = VisionEncoderDecoderModel.from_pretrained(self.model_id).to(self.device)

    def predict(self, line_images: list):
        """Processes a list of PIL image strips"""
        if not line_images:
            return []

        # Batch processing for efficiency (especially on your Quadro T2000)
        pixel_values = self.processor(images=line_images, return_tensors="pt").pixel_values.to(self.device)

        generated_ids = self.model.generate(pixel_values)
        transcriptions = self.processor.batch_decode(generated_ids, skip_special_tokens=True)

        return transcriptions
