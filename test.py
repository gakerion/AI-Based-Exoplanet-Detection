# test_astrosage.py

from transformers import pipeline, BitsAndBytesConfig
import torch


# ==========================================
# 1. Load AstroSage
# ==========================================

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

model_name = "AstroMLab/AstroSage-8B"
context = "Return all the datapoints of the given star id in a python dictionary. make sure the keys are the datapoints and the values are values. dont question me , just give the values you know ."

generator = pipeline(
    "text-generation",
    model=model_name,
    model_kwargs={
        "quantization_config": quant_config
    },
    device_map="auto"
)


# ==========================================
# 2. Ask AstroSage
# ==========================================

def ask_astrosage(query):

    prompt = f"""
You are AstroSage, an astronomy AI assistant.

Answer the following astronomy question clearly and scientifically.

User:
{context}
{query}

AstroSage:
"""

    result = generator(
        prompt,
        max_new_tokens=1000,
        temperature=0.7,
        do_sample=True
    )

    return result[0]["generated_text"]


# ==========================================
# 3. Interactive testing
# ==========================================

print("=" * 60)
print("             AstroSage Test Console")
print("=" * 60)
print("Type your astronomy question.")
print("Type 'exit' to quit.")
print("=" * 60)

while True:

    query = input("\nYou: ")

    if query.lower() == "exit":
        print("Exiting AstroSage...")
        break

    answer = ask_astrosage(query)

    print("\nAstroSage:")
    print(answer)