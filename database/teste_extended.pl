parente(dino,tony).
parente(tony,abe).
parente(tony,sara).
parente(abe,john).
parente(bill,susan).
parente(john,jill).
parente(rob,phil).
parente(marta,tony).
parente(lisa,abe).
parente(lisa,sara).
parente(nancy,john).
parente(sara,susan).
parente(mary,jill).
parente(susan,phil).
homem(socrates).
homem(dino).
homem(tony).
homem(abe).
homem(bill).
homem(john).
homem(rob).
homem(jill).
homem(phil).
febre(lisa).
febre(joão).
dor_de_garganta(lisa).
dor_de_garganta(josé).
dor_de_garganta(marco).
mal_estar(lisa).
mal_estar(joão).
mulher(marta).
mulher(lisa).
mulher(lisa).
mulher(nancy).
mulher(sara).
mulher(mary).
mulher(susan).

bisavo(X,Z):- avo(X,Y),avo(Y,Z).
pai(X,Y):- parente(X,Y),homem(X).
irmao(X,Y):- parente(Z,Y),parente(Z,X).
avo(X,Z):- pai(X,Y),parente(Y,Z).
gripe(X):- mal_estar(X),febre(X),dor_de_garganta(X).
mortal(PESSOA):- homem(PESSOA).
mae(X,Y):- parente(X,Y),mulher(X).
