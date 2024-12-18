from transformers import PegasusTokenizer, PegasusForConditionalGeneration


class FinSummary:
    def __init__(self):
        self.model_name = "human-centered-summarization/financial-summarization-pegasus"
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
        self.model = PegasusForConditionalGeneration.from_pretrained(self.model_name)

    def summarize(self, text):
        input_ids = self.tokenizer(text, return_tensors="pt").input_ids
        output = self.model.generate(
            input_ids, max_length=32, num_beams=5, early_stopping=True
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
