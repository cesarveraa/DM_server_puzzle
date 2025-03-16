# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from solve_puzzle import solve_puzzle, find_blank_position
import model
import ai

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PuzzleRequest(BaseModel):
    matrix: List[List[int]]

@app.on_event("startup")
def initialize_pattern_db():
    """Inicializar la base de datos de patrones al iniciar el servidor"""
    ai.init(4)  # Cargar patrones para puzzle 4x4

@app.post("/solve")
async def solve_endpoint(request: PuzzleRequest):
    # Validar formato de la matriz
    matrix = request.matrix
    if len(matrix) != 4 or any(len(row) != 4 for row in matrix):
        raise HTTPException(400, "La matriz debe ser de 4x4")

    # Validar contenido de la matriz
    numbers = [num for row in matrix for num in row]
    if sorted(numbers) != list(range(16)):
        raise HTTPException(400, "La matriz debe contener números del 0 al 15")

    # Verificar si ya está resuelto
    puzzle = model.Puzzle(boardSize=4, shuffle=False)
    puzzle.board = [row.copy() for row in matrix]
    puzzle.blankPos = find_blank_position(matrix)

    if puzzle.checkWin():
        return {"solution": []}

    try:
        solution_steps = solve_puzzle(matrix)
    except Exception as e:
        raise HTTPException(500, f"Error al resolver: {str(e)}")

    if not solution_steps:
        raise HTTPException(400, "El puzzle no tiene solución")

    return {"solution": solution_steps, "error": None}
