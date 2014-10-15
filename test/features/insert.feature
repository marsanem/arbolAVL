Feature: As a user I want to insert elments to a list and get it sorted.

Scenario: just ask
  Given: The list: "platano, pepino, manzana, kiwi, sandia, melon, fresa, mango, pera, guayaba, piña"
  When: What do you like "platano" or "pepino"
  And: I anwser: "pepino"
  Then: sorted list should look: "pepino, platano"

Scenario: sort just 3 elements
  Given: The previous list
  When: I press next
  And: I should see: "Que prefieres 'manzana' o 'platano'?"
  And: I choose "chicken tai"
  Then: sorted list should look: "manzana, pepino, platano"

Scenario: sort just 3 elements
  Given: The previous list
  When: next question is between "kiwi" and "pepino" I choose "kiwi"
  And: next question is between "kiwi" and "manzana" I choose "kiwi"
  Then: sorted list should look: "kiwi, manzana, pepino, platano"

Scenario: sort just 3 elements
  Given: The previous list
  When: next question is between "sandia" and "pepino" I choose "sandia"
  And: next question is between  "sandia" and "manzana" I choose "sandia"
  And: next question is between  "sandia" and "kiwi" I choose "sandia"
  Then: sorted list should look: "sandia, kiwi, manzana, pepino, platano"

Scenario: sort just 3 elements
  Given: The previous list
  When: next question is between "melon" and "pepino" I choose "melon"
  And: next question is between  "melon" and "kiwi" I choose "melon"
  And: next question is between  "melon" and "sandia" I choose "melon"
  Then: sorted list should look: "melon, sandia, kiwi, manzana, pepino, platano"

Scenario: sort just 3 elements
  Given: The previous list
  When: next question is between "fresa" and "kiwi" I choose "fresa"
  And: next question is between  "fresa" and "sandia" I choose "fresa"
  And: next question is between  "fresa" and "melon" I choose "fresa"
  Then: sorted list should look: "fresa, melon, sandia, kiwi, manzana, pepino, platano"

Scenario: sort just 3 elements
  Given: The previous list
  When: next question is between "mango" and "kiwi" I choose "mango"
  And: next question is between  "mango" and "melon" I choose "mango"
  And: next question is between  "mango" and "fresa" I choose "mango"
  Then: sorted list should look: "mango, fresa, melon, sandia, kiwi, manzana, pepino, platano"

Scenario: sort just 3 elements
  Given: The previous list
  When: next question is between "pera" and "kiwi" I choose "pera"
  And: next question is between  "pera" and "melon" I choose "pera"
  And: next question is between  "pera" and "fresa" I choose "pera"
  And: next question is between  "pera" and "mango" I choose "pera"
  Then: sorted list should look: "pera, mango, fresa, melon, sandia, kiwi, manzana, pepino, platano"

Scenario: sort just 3 elements
  Given: The previous list
  When: next question is between "guayaba" and "kiwi" I choose "guayaba"
  And: next question is between  "guayaba" and "melon" I choose "guayaba"
  And: next question is between  "guayaba" and "mango" I choose "guayaba"
  And: next question is between  "guayaba" and "pera" I choose "guayaba"
  Then: sorted list should look: "guayaba, pera, mango, fresa, melon, sandia, kiwi, manzana, pepino, platano"


Scenario: sort just 3 elements
  Given: The previous list
  When: next question is between "piña" and "kiwi" I choose "piña"
  And: next question is between  "piña" and "mango" I choose "piña"
  And: next question is between  "piña" and "pera" I choose "piña"
  And: next question is between  "piña" and "guayaba" I choose "piña"
  Then: sorted list should look: "piña, guayaba, pera, mango, fresa, melon, sandia, kiwi, manzana, pepino, platano"
