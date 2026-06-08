from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch

MODEL_NAME = "microsoft/Florence-2-large"

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = AutoProcessor.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
).to(device)


def detect_products(image_path):

    image = Image.open(image_path).convert("RGB")

    # prompt = "<DETAILED_CAPTION>"
    prompt = "<MORE_DETAILED_CAPTION>"
    # prompt = """
    # List every visible food item in this refrigerator.
    # Be exhaustive.
    # Include fruits, vegetables, dairy products,
    # drinks, eggs and packaged food. Also try to find out what is in f.e bottles - like ketchup.
    # And if you can - describe amount of products.
    # """

    inputs = processor(
        text=prompt,
        images=image,
        return_tensors="pt"
    )

    inputs = {
        k: v.to(device)
        for k, v in inputs.items()
    }

    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=256
    )

    caption = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    print("\nFLORENCE CAPTION:")
    print(caption)

    return caption