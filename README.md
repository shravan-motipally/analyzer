# analyzer

## Issues faced in sentiment analysis
1. Sentiment analysis using finbert seems to be really wacky
2. The distilled Roberta model seems to be a better option - but is still not entirely good by itself,
so using finbert along with the distilled Roberta model works better

## Issues faced in summarization
1. The pegasus model requires some training before it can be used directly

## Issues faced in similarity match
1. Levenstein distance is a poor indicator of matching company names
2. Fuzzy wuzzy which uses levenstein distance is also a poor indicator of matching company names
3. Cosine similarity is unfortunately also a bad indicator
4. Jaccard similarity is also a bad indicator
