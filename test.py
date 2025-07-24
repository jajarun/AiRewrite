from src.prompts.template import apply_prompt_template
from src.graph.types import workerState
from newspaper import Article

article = Article("https://blog.respon.ai/zh/docs/difference-between-whatspp-messenger-business-and-api")
article.download()
article.parse()

result = apply_prompt_template("rewrite", workerState(
    platform="facebook",
    article_title=article.title,
    article_content=article.text,
    change_style="Casual",
))
print(result)