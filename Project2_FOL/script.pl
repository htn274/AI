likes(huy, lan).
likes(mi, tuan).
likes(tuan, mi).
likes(lan, tuan).

date(X, Y) :- likes(X, Y), likes(Y, X).

jealous(X, Y):- likes(X, Z), likes(Y, Z).

