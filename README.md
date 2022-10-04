# ipy2tex

A simple package to generate a .tex file from a jupyter notebook.

## Usage
---
The package can be used to generate a LaTeX text from the jupyter notebook as follows:
```
import ipy2tex

tex = ipy2tex.IPY2TEX("./path_to_ipynb_file")
print(tex.tex)
# Prints the .tex text.
```

To save a .tex file, use the following method:
```
tex.write("./path_to_tex_file.tex")
```

