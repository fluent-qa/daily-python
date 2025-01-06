import prompts_generator as gen


def test_generate_remote_prompts():
    docs_url = "https://pdm-project.org/latest/"
    prompt_list = [
        "PDM在项目中如何安装和删除依赖",
        "PDM如何Build和Publish",
        "PDM如何配置项目",
        "PDM如何编写脚本",
        "PDM如何管理虚拟环境",
        "PDM如何高级应用",
        "PDM生命周期和Hook管理",
    ]
    for content in prompt_list:
        result = gen.generate_remote_prompts(doc_url=docs_url, prompt=content)
        output_title = f"""
        ---
        {result}
        ---
        """
        print(output_title)
