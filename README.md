# Ortho4XP
A scenery generator for the X-Plane flight simulator

**Forked repository**: there is now an official git repository, https://github.com/oscarpilote/Ortho4XP is the current version from actual developer

Original links:
* http://forums.x-plane.org/index.php?/forums/topic/90469-ortho4xp/ (English forum thread)
* http://www.x-plane.fr/showthread.php?t=55404 (French forum thread)
* https://www.dropbox.com/sh/cjjwu92mausoh04/AACt-QzgMRwKDL392K_Ux3cPa (Dropbox download link)

This repository is a personal fork with some local changes and existing PRs merged

To rebuild the Triangle4xp utility:
```shell
gcc -O2 Utils/Triangle4XP.c -lm -o Utils/Triangle4XP
```

Needed packages for Gentoo (USE=tk should be set):

numpy tkinter pillow Rtree Shapely p7zip nvidia-texture-tools

If you are interested in my previous old tweaked version, checkout the master branch
