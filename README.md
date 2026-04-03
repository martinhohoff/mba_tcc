[EN](#machine-learning-applied-to-predicting-awards-in-cinema-metadata) | [PT](#aprendizagem-de-máquina-aplicada-à-previsão-de-premiações-em-metadados-de-cinema)

# Machine learning applied to predicting awards in cinema metadata

This repository contains the final monograph for the MBA in Data Science at ICMC/USP, authored by Martinho Hoffman, focused on applying machine learning models to predict film nominations and wins at the Academy Awards.

The project combines:

- an academic text written in LaTeX, based on the `USPSC` template;
- exploratory analysis and data preparation in Python/Jupyter;
- figures generated from the experiments and used in the final document.

## Objective

The study investigates the applicability of machine learning models to predict the probability of film nominations and awards at the Oscars, especially in the Best Picture category, using features such as revenue, production countries, original language, and other cinema metadata.

## Repository structure

- `TCC.tex`: main document entry point.
- `0-pre-textual.tex` to `6-Abstract.tex`: front matter, abstract, and supporting pre-textual sections.
- `Cap1-Introducao.tex`, `Cap2-Metodologia.tex`, `Cap3-Desenvolvimento.tex`, `Cap3-Conclusao.tex`, `Cap4-Conclusao.tex`: thesis chapters.
- `fim0-bibliografia.bib`: bibliography file.
- `USPSC.cls` and `USPSC1.cls`: USP Sao Carlos LaTeX classes.
- `notebook/oscar.ipynb`: notebook with the project analysis.
- `notebook/notebook_original.py`: Python script version of the main data-processing workflow.
- `*.png`: figures and charts used in the monograph.
- `Extras/`: auxiliary template files and reference materials.

## Data sources

The script in `notebook/notebook_original.py` references Kaggle datasets, especially:

- `the_oscar_award`
- `the_movies_dataset`

The script expects Kaggle-style paths such as `kaggle/input/...`. Those datasets are not versioned in this repository.

## How to compile the document

With a LaTeX distribution installed, compile the main file with:

```bash
pdflatex TCC.tex
bibtex TCC
pdflatex TCC.tex
pdflatex TCC.tex
```

If you prefer, use `latexmk` to automate the process:

```bash
latexmk -pdf TCC.tex
```

## Notes

- The repository includes both the monograph sources and exported graphical artifacts.
- The `notebook/` directory documents the analytical part of the project, while the `.tex` files contain the final written work.
- This English section was added to make the repository easier to navigate for non-Portuguese readers.

---

# Aprendizagem de máquina aplicada à previsão de premiações em metadados de cinema

Monografia do MBA em Ciências de Dados do ICMC/USP, de autoria de Martinho Hoffman, sobre a aplicação de modelos de aprendizagem de máquina para prever indicação e vitória de filmes no Oscar.

O trabalho combina:

- texto acadêmico em LaTeX, baseado no modelo `USPSC`;
- análise exploratória e preparação de dados em Python/Jupyter;
- figuras geradas a partir dos experimentos e utilizadas no documento final.

## Objetivo

O estudo investiga a aplicabilidade de modelos de machine learning na previsão de chances de indicação e premiação de filmes no Academy Awards, em especial na categoria de Melhor Filme, a partir de atributos como renda, países de produção, idioma original e outros metadados de cinema.

## Estrutura do repositório

- `TCC.tex`: arquivo principal do documento.
- `0-pre-textual.tex` a `6-Abstract.tex`: elementos pré-textuais, resumo e abstract.
- `Cap1-Introducao.tex`, `Cap2-Metodologia.tex`, `Cap3-Desenvolvimento.tex`, `Cap3-Conclusao.tex`, `Cap4-Conclusao.tex`: capítulos do trabalho.
- `fim0-bibliografia.bib`: referências bibliográficas.
- `USPSC.cls` e `USPSC1.cls`: classes LaTeX do modelo USP São Carlos.
- `notebook/oscar.ipynb`: notebook com a análise do projeto.
- `notebook/notebook_original.py`: versão em script Python do fluxo principal de tratamento de dados.
- `*.png`: figuras e gráficos usados na monografia.
- `Extras/`: arquivos auxiliares do modelo e materiais de referência.

## Fontes de dados

O script em `notebook/notebook_original.py` referencia datasets do Kaggle, em especial:

- `the_oscar_award`
- `the_movies_dataset`

Os caminhos esperados no script seguem o padrão de ambiente do Kaggle, como `kaggle/input/...`. Esses arquivos não estão versionados neste repositório.

## Como compilar o documento

Com uma distribuição LaTeX instalada, compile o arquivo principal:

```bash
pdflatex TCC.tex
bibtex TCC
pdflatex TCC.tex
pdflatex TCC.tex
```

Se preferir, use `latexmk` para automatizar o processo:

```bash
latexmk -pdf TCC.tex
```

## Observações

- O repositório reúne tanto os fontes da monografia quanto artefatos gráficos já exportados.
- A pasta `notebook/` documenta a parte analítica do trabalho, enquanto os arquivos `.tex` concentram a redação final.
- O arquivo `README.md` foi preenchido para facilitar navegação, manutenção e futura reprodução do projeto.
