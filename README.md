# Tic_Tac_Toe

Environment: 
n generalized tic-tac-toe is a zero-sum adversarial game. The environment of this game is deterministic, discreted, sequential and 1-agent. 	

Search Space:
The number of branches of each node is b and the depth of the whole tree is m:
The Minmax search without pruning: O(b^m). 
The Minmax search with alpha-beta pruning：between O(b^(m/2)) and O(b^m)
The Minmax search with alpha-beta pruning and depth limitation s: O(b^(s/2)) and O(b^s)

Evaluation function:
1.	 heuristic is the sum of the utility for each row, each column and each diagonal that length is larger than target. 
2.	Score function receives a list  and return the utility of the list. If there is any possible solution in the list, it returns the utility based on the number of the nodes, otherwise the utility is 0.

Common functions:
	checkstatus(board,n): after each move, check the current state is win, lose, draw, or still progressing.
	minimax(board,n,depth,ismax,a,b): return the best utility for both players.
	findmax(board,n): find the best move for player ‘X’.
  findmin(board,n): find the best move for player ‘O’.
