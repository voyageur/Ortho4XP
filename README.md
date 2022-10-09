# Ortho4XP
A scenery generator for the X-Plane flight simulator

**Forked repository**: the official git repository of this great X-Plane tool can be found at https://github.com/oscarpilote/Ortho4XP, maintained by the actual developer. This repository predates the official one so does not show as a fork, but it is one

Included in this personal fork are fixes from existing PRs that were not merged at the time, and some additional changes:
* Option to enable basic transparency roads overlay (based on Transparency4Ortho)
* Zoomable world map
* Updates to providers (mostly Europe/France)
* Small UI changes (layout, some config optiosn)
* Code cleanup and python3 changes

To rebuild the Triangle4xp utility:
```shell
gcc -O2 Utils/Triangle4XP.c -lm -o Utils/Triangle4XP
```

Needed packages for Gentoo (USE=tk should be set, nvidia-texture-tools can be found in my overlay):
```
numpy tkinter pillow Rtree Shapely p7zip nvidia-texture-tools
```

Original links (dating back to this repository creation):
* http://forums.x-plane.org/index.php?/forums/topic/90469-ortho4xp/ (English forum thread)
* http://www.x-plane.fr/showthread.php?t=55404 (French forum thread)
* https://www.dropbox.com/sh/cjjwu92mausoh04/AACt-QzgMRwKDL392K_Ux3cPa (Dropbox download link)
