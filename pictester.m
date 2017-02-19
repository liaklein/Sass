#!/usr/local/bin/wolframscript
dir = CreateDirectory["tempdir"]
i = Import[".tmp-image-file"];
faces = FindFaces[i];
display = ImageTrim[i,#]&/@faces
SetDirectory["tempdir"]
f = 0
{name = ToString[f]~~".jpg",
Export[name,#],
f++}&/@display
ResetRirectory[]
