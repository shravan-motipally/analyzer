from transformers import AutoTokenizer, AutoModelForSequenceClassification


class FinNewsSentimentAnalysis:
    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
        )

    def predict(self, text):
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        outputs = self.model(**inputs)
        logits = outputs.logits
        probabilities = logits.softmax(dim=1)
        sentiment = self.model.config.id2label[probabilities.argmax().item()]
        return sentiment
