# community_challenge_week_05
In de community challenge van de Bit Academy van deze week moeten we een script schrijven wat controleerd of een ingevoerde Sudoku juist is ingevuld.
De uitvoering hiervan staat in een jupyter notebook.

De bonus opdracht om een Sudoku oplosser te maken heb ik in Python geschreven. Op een gegeven moment liep ik vast en heb ik op internet gezocht en zodoende de recursie/backtracking methode gevonden. 

Deze werkt heel goed, maar is eigenlijk een soort Brute Force methode, dus ik heb daarna wat nieuwe functies toegevoegd die wat 'menselijke logica' toevoegen.

Als ik een sudoku maak, kijk ik eerst naar de rijen of kolommen die het meest vol zijn. Vervolgens sluit ik getallen uit die al in de rij en kolom staan. Dit heb ik aan het script toegevoegd, waardoor het veel efficienter is.

Ik heb ook wat CSV bestanden geupload met moeilijkere sudoku's. Evil2 duurt het langst en met de originele methode zijn er 6 miljoen 'guesses' nodig om de puzzel op te lossen.
Na het toevoegen van de logica slechts 600K. 

V2:

Ik heb nu ook logica toegevoegd die controleert hoeveel en welke getallen er in een blok staan. Hierdoor wordt de moeilijkste Sudoku binnen 2 seconden opgelost en met slechts 9K guesses :)
