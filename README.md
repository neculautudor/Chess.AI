# Chess.AI
## Project Requirements  

- [x]  Model a chess game suitable for AI  
- [x]  Develop different versions of AI with the purpose of defeating a real player  

## AI versions
### Dumb AI
* A non-deterministic approach 
* At each stage, chooses a random piece and moves it as far away from its "base" - stupidly aggressive, hence the "dumb" name

### Look Ahead v1
* A deterministic approach
* Associates each piece with a certain value, depending on its importance
* Iterates through each possible move with a customizable depth
* Adds the most valuable piece that can be captured to the move value
* Subtracts the most valuable piece that the enemy can capture afterwards
* Repeats the addition and substraction cycle depending on the depth by recursion

### Look Ahead v2
* Inherits some functionalities from Look Ahead v1
* Pursues to checkmate the enemy and avoids getting checkmated by marking a checkmate move as a value of 50 (knowing that the highest valued piece is 9)
* Can checkmate in endgame as well, by: pushing the enemy king to the edge of the board, minimizing the available moves of the enemy king, avoiding stalemating the enemy king

## Team Member Roles  
### @Neculau Tudor 
* Modelling - documentation & implementation
* Look Ahead AI v1 - research & implementation
* Look Ahead AI v2 - research & implementation
* AI vs AI simulation - implementation
### @Peiu Iulian
* Modelling - review & refactor & optimizations
* Dumb AI - implementation
* Look Ahead AI v1 - review
* Look Ahead AI v2 - research
* AI vs AI simulation - implementation


