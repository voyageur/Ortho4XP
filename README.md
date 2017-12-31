# Ortho4XP
A base mesh creation tool for the X-Plane 10 flight simulator

The main project can be found at :
* http://forums.x-plane.org/index.php?/forums/topic/90469-ortho4xp/ (English forum thread)
* http://www.x-plane.fr/showthread.php?t=55404 (French forum thread)
* https://www.dropbox.com/sh/cjjwu92mausoh04/AACt-QzgMRwKDL392K_Ux3cPa (Dropbox download link)

This repository is a personal fork where I work on some patches (Linux-only for the provided binaries).

To test it, I recommend grabbing Ortho4XP.py file and copy it in an existing Ortho4XP directory

To use this repository directly, after cloning build the Triangle4xp utility:
```shell
gcc -O2 Utils/Triangle4XP.c -lm -o Utils/Triangle4XP
```

List of python modules needed:

| Python module | Gentoo configuration | Fedora package |
|-|-|-|
| numpy | dev-python/numpy | python3-numpy |
| tkinter | dev-lang/python:3[tk] | python3-tk |
| pillow (PIL) with Tk | dev-python/pillow[tk] | python3-pillow-tk |


If you want to build the manual (and if you have a working latex installation):
```shell
cd Manual && latexmk -pdflatex="pdflatex -interactive=nonstopmode" -pdf *tex

```
