from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch

MODEL_NAME = "microsoft/Florence-2-base"

processor = AutoProcessor.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

image = Image.open(
    "data/uploads/lodowka.jpg"
).convert("RGB")

prompt = "<DETAILED_CAPTION>"

inputs = processor(
    text=prompt,
    images=image,
    return_tensors="pt"
)

generated_ids = model.generate(
    input_ids=inputs["input_ids"],
    pixel_values=inputs["pixel_values"],
    max_new_tokens=128
)

generated_text = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True
)[0]

print(generated_text)