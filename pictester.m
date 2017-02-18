stmp = OpenWrite["tmp.txt"]
Write[stmp,a,b,c]

dir = CreateDirectory["tempdir"]
i = Import["http://tinyurl.com/cq5uow"];
faces = FindFaces[i];
display = ImageTrim[i,#]&/@faces
SetDirectory["tempdir"]
f = 0
{name = ToString[f]~~".jpg",
Export[name,#],
f++}&/@display
ResetRirectory[]

