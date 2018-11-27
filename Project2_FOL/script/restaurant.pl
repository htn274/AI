person(bao).
person(nu).
person(cuong).
person(duy).
person(theanh).
person(hy).

chef(bao).
chef(nu).
chef(hy).

place(vietnam).
place(japan).
place(china).

ingredient(salt).
ingredient(sugar).
ingredient(pepper).
ingredient(soy_sauce).
ingredient(fish_sauce).
ingredient(olive_oil).
ingredient(butter).
ingredient(vinegar).
ingredient(garlic).
ingredient(onion).
ingredient(chili).
ingredient(chicken).
ingredient(beef).
ingredient(fish).
ingredient(shrimp).
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
ingredient(lemon).

source(beef, japan).
source(fish, vietnam).
source(pork, vietnam).
source(egg, china).
source(X, china):-vegetables(X).

dish(fried_egg).
dish(fried_fish).
dish(cake).
dish(poached_fish).
dish(poached_pork_and_egg).
dish(salad).
dish(beefsteak).

event(birthday).
event(family_meeting).
event(wedding).

allergy(cuong, fish).
allergy(hy, salt).

sweat(sugar).
sweat(coconut).

sour(vinegar).
sour(lemon).
sour(tomato).

salty(salt).
salty(fish_sauce).
salty(soy_sauce).

spicy(chili).
spicy(pepper).
spicy(ginger).

meat(pork).
meat(beef).
meat(chicken).

seafood(fish).
seafood(shrimp).

vegetables(potato).
vegetables(onion).
vegetables(chili).
vegetables(garlic).
vegetables(ginger).
vegetables(peanut).

fruit(coconut).
fruit(lemon).
fruit(tomato).

drink(soda).
drink(water).
drink(beer).
drink(wine).
drink(strongbow).

alcoholic(beer).
alcoholic(wine).
alcoholic(strongbow).

vegetarian(hy).
vegetarian(theanh).

dish_in_event(cake, birthday).
dish_in_event(fried_fish, birthday).
dish_in_event(salad, birthday).
dish_in_event(fried_egg, family_meeting).
dish_in_event(fried_fish, family_meeting).
dish_in_event(poached_fish, family_meeting).
dish_in_event(poached_pork_and_egg, family_meeting).
dish_in_event(salad, family_meeting).
dish_in_event(fried_fish, wedding).
dish_in_event(salad, wedding).
dish_in_event(beefsteak, wedding).

ingredient_in_dish(egg, fried_egg).
ingredient_in_dish(salt, fried_egg).
ingredient_in_dish(pepper, fried_egg).
ingredient_in_dish(butter, fried_egg).
ingredient_in_dish(fish_sauce, fried_egg).
ingredient_in_dish(tomato, fried_egg).

ingredient_in_dish(fish, poached_fish).
ingredient_in_dish(fish_sauce, poached_fish).
ingredient_in_dish(onion, poached_fish).
ingredient_in_dish(pepper, poached_fish).
ingredient_in_dish(water, poached_fish).
ingredient_in_dish(sugar, poached_fish).

ingredient_in_dish(pork, poached_pork_and_egg).
ingredient_in_dish(egg, poached_pork_and_egg).
ingredient_in_dish(water, poached_pork_and_egg).
ingredient_in_dish(soy_sauce, poached_pork_and_egg).
ingredient_in_dish(fish_sauce, poached_pork_and_egg).
ingredient_in_dish(sugar, poached_pork_and_egg).
ingredient_in_dish(pepper, poached_pork_and_egg).
ingredient_in_dish(coconut, poached_pork_and_egg).
ingredient_in_dish(onion, poached_pork_and_egg).
ingredient_in_dish(ginger, poached_pork_and_egg).
ingredient_in_dish(wine, poached_pork_and_egg).

ingredient_in_dish(fish, fried_fish).
ingredient_in_dish(olive_oil, fried_fish).
ingredient_in_dish(garlic, fried_fish).
ingredient_in_dish(fish_sauce, fried_fish).
ingredient_in_dish(vinegar, fried_fish).
ingredient_in_dish(chili, fried_fish).
ingredient_in_dish(pepper, fried_fish).

ingredient_in_dish(flour, cake).
ingredient_in_dish(egg, cake).
ingredient_in_dish(water, cake).
ingredient_in_dish(sugar, cake).

ingredient_in_dish(beef, beefsteak).
ingredient_in_dish(olive_oil, beefsteak).
ingredient_in_dish(garlic, beefsteak).
ingredient_in_dish(potato, beefsteak).

ingredient_in_dish(beef, salad).
ingredient_in_dish(shrimp, salad).
ingredient_in_dish(chicken, salad).
ingredient_in_dish(tomato, salad).
ingredient_in_dish(peanut, salad).
ingredient_in_dish(vinegar, salad).

ingredient_in_event(I, E):-dish(D), dish_in_event(D, E), ingredient_in_dish(I, D).

drink_in_event(soda, wedding).
drink_in_event(soda, family_meeting).
drink_in_event(soda, birthday).
drink_in_event(water, wedding).
drink_in_event(water, family_meeting).
drink_in_event(water, birthday).
drink_in_event(beer, wedding).
drink_in_event(beer, birthday).
drink_in_event(wine, wedding).
drink_in_event(strongbow, family_meeting).

chef_in_event(bao, family_meeting).
chef_in_event(nu, birthday).
chef_in_event(hy, wedding).
chef_in_event(bao, wedding).
chef_in_event(nu, family_meeting).

invited(birthday, theanh).
invited(wedding, duy).
invited(family_meeting, cuong).

cant_eat(P, D):-ingredient(I), ingredient_in_dish(I, D), allergy(P, I).
cant_eat(P, D):-vegetarian(P), ingredient_in_dish(I, D), meat(I).
cant_eat(P, D):-vegetarian(P), ingredient_in_dish(I, D), seafood(I).

cant_drink(duy, wine).
cant_drink(bao, water).
cant_drink(nu, strongbow).

cant_join(P, E):-dish(D), dish_in_event(D, E), cant_eat(P, D).

not_fun_event(E):-invited(E, P), cant_join(P, E).
not_fun_event(E):-invited(E, P), drink(D), alcoholic(D), drink_in_event(D, E), cant_drink(P, D).

same_ingredient_events(I, E1, E2):-ingredient_in_event(I, E1), ingredient_in_event(I, E2).

same_ingredients_event(I1, I2, E):-ingredient_in_event(I1, E), ingredient_in_event(I2, E).

same_ingredient_dishes(I, D1, D2):-ingredient_in_dish(I, D1), ingredient_in_dish(I, D2).

same_ingredients_dish(I1, I2, D):-ingredient_in_dish(I1, D), ingredient_in_dish(I2, D).

same_dish_events(D, E1, E2):-dish_in_event(D, E1), dish_in_event(D, E2).

same_dishes_event(D1, D2, E):-dish_in_event(D1, E), dish_in_event(D2, E).

high_grade_ingredient(I):-source(I, japan).

high_grade_dish(D):-ingredient_in_dish(I, D), high_grade_ingredient(I).

high_grade_event(E):-dish_in_event(D, E), high_grade_dish(D).

same_chef_events(C, E1, E2):-chef_in_event(C, E1), chef_in_event(C, E2).

same_chefs_event(C1, C2, E):-chef_in_event(C1, E), chef_in_event(C2, E).

same_source_ingredients(S, I1, I2):-source(I1, S), source(I2, S).

source_in_dish(S, D):-ingredient(I), source(I, S), ingredient_in_dish(I, D).

same_source_dishes(S, D1, D2):-source_in_dish(S, D1), source_in_dish(S, D2).

same_sources_dish(S1, S2, D):-source_in_dish(S1, D), source_in_dish(S2, D).

source_in_event(S, E):-ingredient(I), source(I, S), ingredient_in_event(I, E).

same_source_events(S, E1, E2):-source_in_event(S, E1), source_in_event(S, E2).

same_sources_event(S1, S2, E):-source_in_event(S1, E), source_in_event(S2, E).
