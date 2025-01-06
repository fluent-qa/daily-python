import os

from jupyter_notebook_parser import JupyterNotebookParser as Parser

PY_MD_CODE_TEMPLATE = """
```python
{CODE}
```
"""


def compose_md_files(parsed_content):
    cells = parsed_content.get_all_cells()
    md_content = []
    for cell in cells:
        if cell["cell_type"] == "code":
            md_content.append(
                PY_MD_CODE_TEMPLATE.format(CODE="".join(cell["source"]))
            )
        if cell["cell_type"] == "markdown":
            md_content.append("".join(cell["source"]))
    return md_content


class JupyterNotesComposer:

    def to_md_file(self, note_file_path: str, md_file_path: str) -> "JupyterNotesComposer":
        parsed = Parser(note_file_path)
        md_content = compose_md_files(parsed)
        with open(md_file_path, "w") as md_file:
            md_file.writelines(md_content)
        return self


def covert_all_notes_to_md(notes_dir: str, md_dir: str):
    notes = os.listdir(notes_dir)
    for note in notes:
        p = JupyterNotesComposer()
        if os.listdir(note):
            covert_all_notes_to_md()
        md_path = "/".join([md_dir, note.replace(".ipynb", ".md")])
        p.to_md_file(md_path)
