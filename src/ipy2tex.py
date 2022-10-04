import codecs
import json
import base64
import os


class IPY2TEX:
    def __init__(self, ipynb: str):
        self.ipynb = ipynb
        self.preamble = """\\documentclass[11pt]{exam}
\\usepackage{xcolor}
\\usepackage[most]{tcolorbox}
\\usepackage{listings}
\\definecolor{white}{rgb}{1,1,1}
\\definecolor{mygreen}{rgb}{0,0.4,0}
\\definecolor{light_gray}{rgb}{0.97,0.97,0.97}
\\definecolor{mykey}{rgb}{0.117,0.403,0.713}
\\definecolor{codegreen}{rgb}{0,0.6,0}
\\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\\definecolor{codepurple}{rgb}{0.58,0,0.82}
\\definecolor{backcolour}{rgb}{0.95,0.95,0.92}
\\tcbuselibrary{listings}
\\newlength\\inwd
\\setlength\\inwd{1.3cm}
\\newcounter{ipythcntr}
\\renewcommand{\\theipythcntr}{\\texttt{[\\arabic{ipythcntr}]}}
\\newtcblisting{pyin}[1][]{%
  sharp corners,
  enlarge left by=\\inwd,
  width=\\linewidth-\\inwd,
  enhanced,
  boxrule=0pt,
  colback=light_gray,
  listing only,
  top=0pt,
  bottom=0pt,
  overlay={
    \\node[
      anchor=north east,
      text width=\\inwd,
      font=\\footnotesize\\ttfamily\\color{mykey},
      inner ysep=2mm,
      inner xsep=0pt,
      outer sep=0pt
      ] 
      at (frame.north west)
      {\\refstepcounter{ipythcntr}\\label{#1}In \\theipythcntr:};
  }
  listing engine=listing,
  listing options={
    aboveskip=1pt,
    belowskip=1pt,
    basicstyle=\\footnotesize\\ttfamily,
    language=Python,
    keywordstyle=\\color{mykey},
    showstringspaces=false,
    stringstyle=\\color{mygreen}
  },
}
\\newtcblisting{pyprint}{
  sharp corners,
  enlarge left by=\\inwd,
  width=\\linewidth-\\inwd,
  enhanced,
  boxrule=0pt,
  colback=white,
  listing only,
  top=0pt,
  bottom=0pt,
  overlay={
    \\node[
      anchor=north east,
      text width=\\inwd,
      font=\\footnotesize\\ttfamily\\color{mykey},
      inner ysep=2mm,
      inner xsep=0pt,
      outer sep=0pt
      ] 
      at (frame.north west)
      {};
  }
  listing engine=listing,
}
\\newtcblisting{pyout}[1][\\theipythcntr]{
  sharp corners,
  enlarge left by=\\inwd,
  width=\\linewidth-\\inwd,
  enhanced,
  boxrule=0pt,
  colback=white,
  listing only,
  top=0pt,
  bottom=0pt,
  overlay={
    \\node[
      anchor=north east,
      text width=\\inwd,
      font=\\footnotesize\\ttfamily\\color{mykey},
      inner ysep=2mm,
      inner xsep=0pt,
      outer sep=0pt
      ] 
      at (frame.north west)
      {\\setcounter{ipythcntr}{\\value{ipythcntr}}Out#1:};
  }
}
\\lstdefinestyle{mystyle}{
    backgroundcolor=\\color{backcolour},   
    commentstyle=\\color{codegreen},
    keywordstyle=\\color{magenta},
    numberstyle=\\tiny\\color{codegray},
    stringstyle=\\color{codepurple},
    basicstyle=\\ttfamily\\footnotesize,
    breakatwhitespace=false,         
    breaklines=true,                 
    captionpos=b,                    
    keepspaces=true,                 
    numbers=left,                    
    numbersep=5pt,                  
    showspaces=false,                
    showstringspaces=false,
    showtabs=false,                  
    tabsize=2
}
\\lstset{style=mystyle}
"""
        self.tex = self.preamble + "\\begin{document}\n"
        self._read_source()
        self.get_tex()

    def _read_source(self):
        self.source = json.loads(codecs.open(self.ipynb, "r").read())

    def get_tex(self):
        image_cnt = 0
        for cell in self.source["cells"]:
            if cell["cell_type"] == "code":
                self.tex += "\\begin{pyin}\n"
                # Code cell
                for code_line in cell["source"]:
                    self.tex += code_line
                    if code_line[-1] != "\n":
                        self.tex += "\n"
                self.tex += "\\end{pyin}\n"
                # Output Cell
                for output_text in cell["outputs"]:
                    # Text outputs
                    if "name" in output_text and output_text["name"] == "stdout":
                        self.tex += "\\begin{pyout}\n"
                        for output_text_line in output_text["text"]:
                            self.tex = self.tex + output_text_line
                            if output_text_line[-1] != "\n":
                                self.tex = self.tex + "\n"
                        self.tex += "\\end{pyout}\n"
                    # Image output
                    if "data" in output_text and "image/png" in output_text["data"]:
                        os.makedirs(os.path.dirname("./ipy2texfigs/"), exist_ok=True)
                        with open(f"./ipy2texfigs/{image_cnt}.png", "wb") as fh:
                            fh.write(
                                base64.decodebytes(
                                    str.encode(output_text["data"]["image/png"])
                                )
                            )
                        self.tex += f"""
\\begin{{figure}}[!htbp]
\\centering
\\includegraphics[width=\\textwidth]{{./ipy2texfigs/{image_cnt}.png}}
\\caption{{Figure {image_cnt}}}
\\label{{fig:{image_cnt}}}
\\end{{figure}}
"""
                        image_cnt += 1

            self.tex += "% ================================================\n"
        self.tex += "\\end{document}\n"

    def write(self, filename):
        with open(filename, "w") as f:
            f.write(self.tex)
