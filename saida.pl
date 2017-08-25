mae(lisa,abe).
mae(lisa,sara).
mae(nancy,john).
mae(sara,susan).
mae(mary,jill).
mae(susan,phil).
mal_estar(lisa).
mal_estar(joão).
dor_de_garganta(lisa).
dor_de_garganta(josé).
dor_de_garganta(marco).
febre(lisa).
febre(joão).
pai(tony,abe).
pai(tony,sara).
pai(abe,john).
pai(bill,susan).
pai(john,jill).
pai(rob,phil).
homem(socrates).
parente(X,Y):- pai(X,Y).
irmao(X,Y):- parente(Z,Y),parente(Z,X).
gripe(X):- mal_estar(X),dor_de_garganta(X),febre(X).
avo(X,Z):- parente(X,Y),parente(Y,Z).
mortal(PESSOA):- homem(PESSOA).
bisavo(X,Z):- avo(X,Y),avo(Y,Z).
