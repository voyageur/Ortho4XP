# Ortho4XP
A base mesh creation tool for the X-Plane 10 flight simulator

The main project can be found at :
* http://forums.x-plane.org/index.php?/forums/topic/90469-ortho4xp/ (English forum thread)
* http://www.x-plane.fr/showthread.php?t=55404 (French forum thread)
* https://www.dropbox.com/sh/cjjwu92mausoh04/AACt-QzgMRwKDL392K_Ux3cPa (Dropbox download link)

This repository is a personal fork where I work on some patches (Linux-only for the provided binaries).

To test it, I recommend grabbing Ortho4XP.py file and copy it in an existing Ortho4XP directory

To use this repository directly, some useful commands:
```shell
# Build Triangle4XP binary
gcc -O2 -lm Utils/Triangle4XP.c -o Utils/Triangle4XP

# Generate manual
cd Manual && latexmk -pdflatex="pdflatex -interactive=nonstopmode" -pdf *tex

```
