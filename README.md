# ipy2tex

A simple package to generate a .tex file from a jupyter notebook.

## Installation
Install the package using the following command:
```
pip install https://github.com/nikhil-ravi/ipy2tex/archive/refs/heads/main.zip
```

## Usage
The package can be used to generate a LaTeX text from the jupyter notebook as follows:
```python
import ipy2tex

tex = ipy2tex.IPY2TEX("./path_to_ipynb_file")
print(tex.tex)
# Prints the .tex text.
```

To save a .tex file, use the following method:
```python
tex.write("./path_to_tex_file.tex")
```

