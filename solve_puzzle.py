import model
import ai

def solve_puzzle(initial_board):
    """
    Función principal que resuelve el puzzle.
    
    :param initial_board: Matriz 2D que representa el estado inicial del puzzle
    :return: Lista de matrices que representan los pasos para resolver el puzzle
    """
    board_size = len(initial_board)
    puzzle = model.Puzzle(boardSize=board_size, shuffle=False)
    puzzle.board = [row[:] for row in initial_board]  # Copia manual del tablero
    puzzle.blankPos = find_blank_position(initial_board)

    ai.init(board_size)

    if puzzle.checkWin():
        return []

    # Ejecuta el algoritmo idaStar para obtener los movimientos
    solution_moves = ai.idaStar(puzzle)

    # Generar los estados (matrices) en cada paso de la solución
    solution_boards = []
    if solution_moves is not None:
        for move in solution_moves:
            puzzle.move(move)
            solution_boards.append([row[:] for row in puzzle.board])  # Copia manual del tablero
        return solution_boards
    else:
        return []

def find_blank_position(board):
    """
    Encuentra la posición del espacio en blanco (0) en el puzzle.
    
    :param board: Matriz 2D que representa el puzzle
    :return: Una tupla (fila, columna) con la posición del espacio en blanco
    """
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == 0:
                return (i, j)
