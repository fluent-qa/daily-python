from pydantic import BaseModel


class RemoteDocPrompt(BaseModel):
    docs_url: str
    role: str = "请为一个初学者总结"
    prompt: str
    output_type: str = "markdown"

    def to_prompt(self):
        return f"文档地址为:{self.docs_url},{self.role}: {self.prompt},并用{self.output_type} 返回"


def generate_remote_prompts(doc_url: str, prompt: str, role: str = None) -> str:
    if role is None:
        prompt = RemoteDocPrompt(
            docs_url=doc_url,
            prompt=prompt,
        )
    else:
        prompt = RemoteDocPrompt(docs_url=doc_url, prompt=prompt, role=role)
    return prompt.to_prompt()
