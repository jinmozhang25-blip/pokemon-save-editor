# v.0.1.3

A python script which reads a Pokemon Gen 1's save file and returns the player's:

- Name
- Rival's name
- Amount of money
- List of badges
- List of pokemon in your party with their species and level
- List of items in your bag
- List of items in your pc

Support save files from Pokemon Red/Blue(US/EU)

Script supports a normal 32 KiB file, a 8KiB bank-1-only file, a 64 KiB padded dump, and a file with an mGBA/RTC footer.

```
========================================
CONSULT SAVE FILE
========================================
1. Player
2. Rival
3. Money
4. Badges
5. Party Pokémon
6. Bag items
7. PC items
8. Exit
----------------------------------------
Enter your choice (1-8):
```

Credits:

Bulbapedia

- (Save data structure Generation I) - https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_I)#Party_Data
- (List of Pokémon by index number in Generation I) - https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_index_number_in_Generation_I
- (List of Item by index number in Generation I) - https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_in_Generation_I
