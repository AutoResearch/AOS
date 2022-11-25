from rouge_score import rouge_scorer

with open('text_1.txt') as f:
    text_1 = f.read()
with open('text_2.txt') as f:
    text_2 = f.read()

scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

score = scorer.score(text_1, text_2)

with open('scores.txt', 'a')as f:
    f.write('Rouge score:\n')
    f.write(str(score))
