/* Example 1 */
likes(huy, lan).
likes(mi, tuan).
likes(tuan, mi).
likes(lan, tuan).

date(X, Y) :- likes(X, Y), likes(Y, X).

jealous(X, Y):- likes(X, Z), likes(Y, Z).

/*  Example 2   */
/*  last  */
/*  last(X, List) -> "X is the last element in List"  */
last(X,[X]).
last(X,[_|Y]) :- last(X,Y).

/*  nextto  */
/*  nextto(X,Y,List) -> "X and Y are consecutive elements in List"  */
nextto(X,Y,[X,Y|_]).
nextto(X,Y,[_|Z]) :- nextto(X,Y,Z).

/*  reverse  */
/*  reverse(List1, List2) -> "List2 is the reversing order of List1" */
/*reverse([],[]).
reverse([H|T],List) :- reverse(T,Z), append(Z,[H],List).*/

/*  sublist  */
/*  sublist(S,List) -> "S is a sublist of List which appears consecutively,  */
/*                      and in the same order"                               */
sublist([X|L],[X|M]) :- prefix(L,M).
sublist(L,[_|M]) :- sublist(L,M).

/*  prefix  */
/*  prefix(X, List) -> "X is prefix of List"    */
prefix([],_).
prefix([X|L],[X|M]) :- prefix(L,M).

/*  Example 3 */
sel(X, [X|Y], Y).
sel(U, [X|Y], [X|V]) :- sel(U,Y,V).

safe([ ]).
safe([X|Y]) :- check(X,Y), safe(Y).

check(_,[ ]).
check(P, [Q|R]) :- 
	not_on_diag(P,Q), check(P,R).

not_on_diag(p(X1,Y1),p(X2,Y2)) :-
	DX is X1-X2, DY is Y1-Y2, 
	MDY is Y2-Y1, DX=\=DY, DX=\=MDY.

queens(Rows, [Col|RestCols], Points):-
	sel(Row,Rows,RestRows),
	safe([p(Row,Col) | Points]),
	queens(RestRows,RestCols,
		[p(Row,Col) | Points]).

queens( [ ], [ ], Points) :-
	print('Solution: '),print(Points),nl.



/* Example 4 */
fact(0,1).
fact(N,R):- fact(N1,R1),N is N1 + 1,R is R1 * N.

location(city_hall).
location(vacant_lot).
location(old_mill).
location(field).
location(barber_shop).

flat(city_hall).
flat(vacant_lot).
flat(field).

grassy(city_hall).
grassy(vacant_lot).

possibly_park(X) :-
	location(X),
	flat(X),
	grassy(X).

/* Exmaple 5 */
edge(1,2).
edge(1,4).
edge(1,3).
edge(2,3).
edge(2,5).
edge(3,4).
edge(3,5).
edge(4,5).

connected(X,Y) :- edge(X,Y) ; edge(Y,X).
path(A,B,Path) :-
       travel(A,B,[A],Q), 
       reverse(Q,Path).

travel(A,B,P,[B|P]) :- 
       connected(A,B).
travel(A,B,Visited,Path) :-
       connected(A,C),           
       C \== B,
       \+member(C,Visited),
       travel(C,B,[C|Visited],Path).  

