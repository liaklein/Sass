image  = ToExpression[$ScriptCommandLine[[2]]];

stmp = OpenWrite["tmp.txt"]
Write[stmp,a,b,c]

dir = CreateDirectory["tempdir"]
i = Import[image];
faces = FindFaces[i];
display = ImageTrim[i,#]&/@faces
SetDirectory["tempdir"]
f = 0
{name = ToString[f]~~".jpg",
Export[name,#],
f++}&/@display
ResetRirectory[]
