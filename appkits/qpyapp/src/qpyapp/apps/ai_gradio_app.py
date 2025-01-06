import gradio as gr
from qpyapp import ai,conf

conf.load_dotenv()

gr.load(
    name='hyperbolic:deepseek-ai/DeepSeek-V3',
    src=ai.registry,
    title ="AI Chat/Application/Agent",
    coder=True
).launch()
