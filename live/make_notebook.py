"""Writes train_kaggle.ipynb from train_kaggle.py ('# %%' cells), with a first cell that writes chessvision.py,
so the notebook runs the server's own code. Run it again after changing either file."""
import json
import pathlib

HERE = pathlib.Path(__file__).parent


def cell(kind, text):
    lines = text.strip('\n').splitlines(keepends=True)
    c = {'cell_type': kind, 'metadata': {}, 'source': lines}
    if kind == 'code':
        c.update(execution_count=None, outputs=[])
    return c


cells = []
for chunk in (HERE / 'train_kaggle.py').read_text(encoding='utf-8').split('# %%')[1:]:
    head, _, body = chunk.partition('\n')
    if head.strip() == '[markdown]':
        cells.append(cell('markdown', '\n'.join(l[2:] if l.startswith('# ') else l.lstrip('#') for l in body.splitlines())))
    else:
        cells.append(cell('code', body))
vision = '%%writefile chessvision.py\n' + (HERE / 'chessvision.py').read_text(encoding='utf-8')
cells.insert(1, cell('code', vision))
nb = {'cells': cells, 'metadata': {'kernelspec': {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'},
                                   'language_info': {'name': 'python'},
                                   'kaggle': {'accelerator': 'nvidiaTeslaT4', 'isInternetEnabled': True}},
      'nbformat': 4, 'nbformat_minor': 5}
(HERE / 'train_kaggle.ipynb').write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
print(len(cells), 'cells ->', HERE / 'train_kaggle.ipynb')
