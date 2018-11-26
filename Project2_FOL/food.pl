person(P).
chef(P).
place(P).
source(I, P).
ingredient(I).
dish(D).
event(E).
allergy(P, I).
sweat(I).
sour(I).
salty(I).
spicy(I).
meat(I).
seafood(I).
vegetables(I).
fruit(F).
drink(D).
alcoholic(D).
cook_method(CM).
cook_method(D, CM).
vegetarian(P).
recommended_together(D1, D2).
dish_in_event(D, E).
ingredient_in_event(I, E).
ingredient_in_dish(I, D).
drink_in_event(D, E).
chef_in_event(C, E).
invited(E, P).
cant_eat(P, D):-ingredient(I), contains(D, I), allergy(P, I); vegetarian(P), contains(D, I), meat(I); vegetarian(P), contains(D, I), seafood(I).
cant_drink(P, D).
cant_join(P, E):-dish(D), dish_in_event(D, E), cant_eat(P, D).
not_fun_party(E):-person(P), invited(E, P), cant_join(P, E); person(P), invited(E, P), drink(D), alcoholic(D), drink_in_event(D, E), cant_drink(P, D).
same_ingredient_events(I, E1, E2).
same_ingredients_event(I1, I2, E).
same_ingredient_dishes(I, E1, E2).
same_ingredients_dish(I1, I2, D).
same_dish_events(D, E1, E2).
same_dishes_event(D1, D2, E).
high_grade_ingredient(I).
high_grade_dish(D).
high_grade_event(E).
high_grade_drink(D).
same_chefs_dish(C1, C2, D).
same_chef_dishes(C, D1, D2).
same_chef_events(C, E1, E2).
same_chefs_event(C1, C2, E).
same_source_ingredients(S, I1, I2).
same_source_dishes(S, D1, D2).
same_sources_dish(S1, S2, D).
same_source_events(S, E1, E2).
same_sources_event(S1, S2, E).


person(bao).
person(nu).
person(cuong).
person(duy).

ingredient(salt).
ingredient(sugar).
ingredient(pepper).
ingredient(soy_sauce).
ingredient(fish_sauce).
ingredient(cooking_oil).
ingredient(butter).
ingredient(vinegar).

ingredient(garlic).
ingredient(onion).
ingredient(chili).
ingredient(chiken).
ingredient(fish).
ingredient(pork).
ingredient(water).
ingredient(coconut).
ingredient(egg).
ingredient(ginger).
ingredient(peanut).
ingredient(tomato).
ingredient(potato).
ingredient(wine).
ingredient(flour).

dish(fried_egg).
dish(fried_fish).
dish(poached_fish).
dish(poached_pork_and_egg).
dish(cake).

event(birthday).
event(wedding).
event(family).

contains(fried_egg, egg).
contains(fried_egg, salt).
contains(fried_egg, pepper).
contains(fried_egg, butter).
contains(fried_egg, fish_sauce).
contains(fried_egg, tomato).

contains(poached_fish, fish).
contains(poached_fish, fish_sauce).
contains(poached_fish, onion).
contains(poached_fish, pepper).
contains(poached_fish, water).
contains(poached_fish, sugar).

contains(poached_pork_and_egg, pork).
contains(poached_pork_and_egg, egg).
contains(poached_pork_and_egg, water).
contains(poached_pork_and_egg, soy_sauce).
contains(poached_pork_and_egg, fish_sauce).
contains(poached_pork_and_egg, sugar).
contains(poached_pork_and_egg, pepper).
contains(poached_pork_and_egg, coconut).
contains(poached_pork_and_egg, onion).
contains(poached_pork_and_egg, ginger).
contains(poached_pork_and_egg, vinegar).
contains(poached_pork_and_egg, wine).
contains(poached_pork_and_egg, cooking_oil).

contains(fried_fish, fish).
contains(fried_fish, cooking_oil).
contains(fried_fish, garlic).
contains(fried_fish, fish_sauce).
contains(fried_fish, vinegar).
contains(fried_fish, chili).
contains(fried_fish, pepper).

contains(cake, flour).
contains(cake, egg).
contains(cake, water).
contains(cake, sugar).
contains(cacke, milk).
