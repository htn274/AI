male(phillip).
male(charles).
male(mark_phillips).
male(timothy_laurence).
male(andrew).
male(edward).
male(william).
male(harry).
male(peter_phillips).
male(mike).
male(james).
male(george).

female(elizabeth).
female(diana).
female(camilla).
female(anne).
female(sarah).
female(sophie).
female(kate).
female(autumn).
female(zara).
female(beatrice).
female(eugeine).
female(louise_mountbatten).
female(charlotte).
female(savannah).
female(isla).
female(miagrace).

married(elizabeth, phillip).
married(phillip, elizabeth).
married(charles, camilla).
married(camilla, charles).
married(anne, timothy_laurence).
married(timothy_laurence, anne).
married(sophie, edward).
married(edward, sophie).
married(william, kate).
married(kate, william).
married(peter_phillips, autumn).
married(peter_phillips, autumn).
married(zara, mike).
married(mike, zara).

divorced(diana, charles).
divorced(charles, diana).
divorced(mark_phillips, anne).
divorced(anne, mark_phillips).
divorced(sarah, andrew).
divorced(andrew, sarah).

parent(elizabeth, charles).
parent(elizabeth, anne).
parent(elizabeth, andrew).
parent(elizabeth, edward).
parent(phillip, charles).
parent(phillip, anne).
parent(phillip, andrew).
parent(phillip, edward).

parent(charles, william).
parent(charles, harry).
parent(diana, william).
parent(diana, harry).

parent(mark_phillips, peter_phillips).
parent(mark_phillips, zara).
parent(anne, peter_phillips).
parent(anne, zara).

parent(sarah, beatrice).
parent(sarah, eugeine).
parent(andrew, beatrice).
parent(andrew, eugeine).

parent(sophie, james).
parent(sophie, louise_mountbatten).
parent(edward, james).
parent(edward, louise_mountbatten).

parent(william, george).
parent(william, charlotte).
parent(kate, george).
parent(kate, charlotte).

parent(autumn, savannah).
parent(autumn, isla).
parent(peter_phillips, savannah).
parent(peter_phillips, isla).

parent(zara, miagrace).
parent(mike, miagrace).

husband(Person, Wife) :-
    male(Person),
    female(Wife),
    married(Person, Wife),
    married(Wife, Person).

wife(Person, Husband) :-
    female(Person),
    male(Husband),
    married(Person, Husband),
    married(Husband, Person).

father(Parent, Child) :-
    parent(Parent, Child),
    male(Parent).

mother(Parent, Child) :-
    parent(Parent, Child),
    female(Parent).

child(Child, Parent) :-
    parent(Parent, Child).

son(Child, Parent) :-
    parent(Parent, Child),
    male(Child).

daughter(Child, Parent) :-
    parent(Parent, Child),
    female(Child).

grandparent(GrandParent, GrandChild) :-
    parent(GrandParent, Parent),
    parent(Parent, GrandChild).

grandmother(GrandMother, GrandChild) :-
    female(GrandMother),
    mother(GrandMother, Mother),
    mother(Mother, GrandChild).

grandfather(GrandFather, GrandChild) :-
    male(GrandFather),
    father(GrandFather, Father),
    father(Father, GrandChild).

grandchild(GrandChild, GrandParent):-
    grandparent(GrandParent, GrandChild).

grandson(GrandSon, GrandParent) :-
    grandparent(GrandParent, GrandSon),
    male(GrandSon).

granddaughter(GrandDaughter, GrandParent) :-
    grandparent(GrandParent, GrandDaughter),
    female(GrandDaughter).

sibling(Person1, Person2):-
    father(Father, Person1),
    father(Father, Person2),
    mother(Mother, Person1),
    mother(Mother, Person2).


brother(Person, Sibling):-
    male(Person),
    sibling(Person, Sibling).

sister(Person, Sibling):-
    female(Person),
    sibling(Person, Sibling).
    
aunt(Person, NieceNewphew):-
    parent(Parent, NieceNewphew),
    sister(Person, Parent).

aunt(Person, NieceNewphew):-
    parent(Parent, NieceNewphew),
    brother(Husband, Parent),
    husband(Husband, Person).

uncle(Person, NieceNewphew):-
    parent(Parent, NieceNewphew),
    brother(Person, Parent).

uncle(Person, NieceNewphew) :-
    parent(Parent, NieceNewphew),
    sister(Wife, Parent),
    wife(Wife, Person).

niece(Person, AuntUncle) :-
    female(Person),
    aunt(AuntUncle, Person).

niece(Person, AuntUncle) :-
    female(Person),
    uncle(AuntUncle, Person).
            
nephew(Person, AuntUncle) :-
    male(Person), 
    aunt(AuntUncle, Person).

nephew(Person, AuntUncle) :-
    male(Person), 
    uncle(AuntUncle, Person).









