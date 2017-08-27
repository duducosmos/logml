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
mal_estar(lisa).
mal_estar(joão).
febre(lisa).
febre(joão).
mulher(marta).
mulher(lisa).
mulher(lisa).
mulher(nancy).
mulher(sara).
mulher(mary).
mulher(susan).
homem(socrates).
homem(dino).
homem(tony).
homem(abe).
homem(bill).
homem(john).
homem(rob).
homem(jill).
homem(phil).
dor_de_garganta(lisa).
dor_de_garganta(josé).
dor_de_garganta(marco).

gripe(X):- febre(X),mal_estar(X),dor_de_garganta(X).
pai(X,Y):- homem(X),parente(X,Y).
mae(X,Y):- mulher(X),parente(X,Y).
irmao(X,Y):- parente(Z,Y),parente(Z,X).
avo(X,Z):- parente(Y,Z),pai(X,Y).
mortal(PESSOA):- homem(PESSOA).
bisavo(X,Z):- avo(X,Y),avo(Y,Z).
