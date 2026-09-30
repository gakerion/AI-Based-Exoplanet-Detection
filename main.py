import helper
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_NAME = "AstroMLab/AstroSage-8B"

# Model objects are created during FastAPI startup, not during a request.
tokenizer = None
model = None

quant_config = BitsAndBytesConfig(load_in_8bit=True)


def load_model():
    """Load AstroSage once into memory/VRAM."""
    global tokenizer, model

    if model is not None and tokenizer is not None:
        print("AstroSage is already loaded.")
        return

    print("Loading AstroSage tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Loading AstroSage-8B in 8-bit...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=quant_config,
        device_map="auto",
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    )

    model.eval()
    print("AstroSage model loaded successfully.")


def get_star_summary(kic_id, star_data=None):
    """Generate one concise AstroSage summary for a KIC ID."""
    if model is None or tokenizer is None:
        raise RuntimeError("AstroSage has not been loaded yet.")

    if star_data is None:
        star_data = helper.lookup_star(kic_id)

    star_info = (
        f"- Oxygen: {star_data['Oxygen']}\n"
        f"- Metallicity: {star_data['Metallicity']}\n"
        f"- Mass: {star_data['Mass']} solar masses\n"
        f"- Gravity: {star_data['Gravity']} m/s²\n"
        f"- Radius: {star_data['Radius']} solar radii\n"
        f"- Distance: {star_data['Distance']} light years\n"
        f"- Hydrogen: {star_data['Hydrogen']}"
    )

    prompt = f"""You are an astronomy assistant.

Analyze the following catalog data for KIC {kic_id}:

{star_info}

Write ONE concise scientific summary in a single paragraph.

Rules:
- Use ONLY the data provided.
- Do not estimate or invent values.
- If a value is Unknown, state that it is unknown.
- Do not repeat the summary.
- Do not discuss future research or observations.
- Do not add a second paragraph.
- Do not include headings or formatting.
- STOP after the first paragraph.
"""

    inputs = tokenizer(prompt, return_tensors="pt")

    # With device_map="auto", put inputs on the model's input device.
    input_device = next(model.parameters()).device
    inputs = {key: value.to(input_device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated_tokens = outputs[0, inputs["input_ids"].shape[1]:]

    return tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    ).strip()
