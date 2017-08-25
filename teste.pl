homem(socrates).
mal_estar(lisa).
mal_estar(joão).
febre(lisa).
febre(joão).
dor_de_garganta(lisa).
dor_de_garganta(josé).
dor_de_garganta(marco).
mae(marta,tony).
mae(lisa,abe).
mae(lisa,sara).
mae(nancy,john).
mae(sara,susan).
mae(mary,jill).
mae(susan,phil).
pai(dino,tony).
pai(tony,abe).
pai(tony,sara).
pai(abe,john).
pai(bill,susan).
pai(john,jill).
pai(rob,phil).

bisavo(X,Z):- avo(X,Y),avo(Y,Z).
irmao(X,Y):- parente(Z,Y),parente(Z,X).
avo(X,Z):- parente(X,Y),parente(Y,Z).
mortal(PESSOA):- homem(PESSOA).
gripe(X):- dor_de_garganta(X),febre(X),mal_estar(X).
parente(X,Y):- pai(X,Y).
