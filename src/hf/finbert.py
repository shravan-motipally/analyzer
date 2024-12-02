from transformers import AutoTokenizer, AutoModelForSequenceClassification


class Finbert:
    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        logits = outputs.logits
        probabilities = logits.softmax(dim=1)
        sentiment = self.model.config.id2label[probabilities.argmax().item()]
        return sentiment


