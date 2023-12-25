using System.Text;

namespace Core.Models;

/// <summary>
/// False - player, True - AI
/// </summary>
public class Game
{
    public Guid Uid { get; init; }
    public string UserId { get; init; } = null!;
    public List<List<bool?>>? Board { get; set; } = null!;
    public bool IsInitialized => Board is not null;
    public bool IsPlayerWonOrTie { get; set; } = false;
    public bool IsEnd { get; set; } = false;
    public bool IsPlayerStep { get; set; } = false;
    public DateTime? LastStepDate = null;
    public DateTime CreateDate = DateTime.UtcNow;

    public void Initialize()
    {
        if (IsInitialized)
        {
            throw new Exception("Game is already initialized");
        }

        Board = new List<List<bool?>>
        {
            new List<bool?> { null, null, null, null, null, null, null, null, null, null },
            new List<bool?> { null, null, null, null, null, null, null, null, null, null },
            new List<bool?> { null, null, null, null, null, null, null, null, null, null },
            new List<bool?> { null, null, null, null, null, null, null, null, null, null },
            new List<bool?> { null, null, null, null, null, null, null, null, null, null },
            new List<bool?> { null, null, null, null, null, null, null, null, null, null },
            new List<bool?> { null, null, null, null, null, null, null, null, null, null },
            new List<bool?> { null, null, null, null, null, null, null, null, null, null },
            new List<bool?> { null, null, null, null, null, null, null, null, null, null },
            new List<bool?> { null, null, null, null, null, null, null, null, null, null }
        };
    }

    public string DrawBoard()
    {
        if (!IsInitialized)
        {
            throw new Exception("Game is not initialized");
        }

        var board = new StringBuilder();

        for (int i = 0; i < 10; i++)
        {
            for (int j = 0; j < 10; j++)
            {
                if (Board![i][j] == true)
                {
                    board.Append("O");
                }
                else if (Board![i][j] == false)
                {
                    board.Append("X");
                }
                else
                {
                    board.Append("-");
                }

                board.Append(" | ");
            }

            board.AppendLine();
            board.AppendLine("-----------------------------------------");
        }

        return board.ToString();
    }

    public StepResult PlayerStep(int x, int y)
    {
        if (!IsInitialized)
            throw new Exception("Not initialized");

        if (x < 0 || x >= 10 || y < 0 || y >= 10)
        {
            return new StepResult
            {
                Status = false,
                Message = "Invalid coordinates. X and Y must be between 0 and 9."
            };
        }

        if (Board![x][y] is true)
        {
            return new StepResult
            {
                Status = false,
                Message = "This cell is already occupied by AI"
            };
        }

        if (Board![x][y] is false)
        {
            return new StepResult
            {
                Status = false,
                Message = "This cell is already occupied by you"
            };
        }

        Board![x][y] = false; // Player move (X)
        IsPlayerStep = false;

        if (IsWin())
        {
            IsPlayerWonOrTie = true;
            IsEnd = true;

            return new StepResult
            {
                Status = true,
                Message = "You won"
            };
        }

        if (IsTie())
        {
            IsPlayerWonOrTie = true;
            IsEnd = true;

            return new StepResult
            {
                Status = true,
                Message = "Tie"
            };
        }

        return new StepResult
        {
            Status = true
        };
    }

    public StepResult AiStep()
    {
        if (!IsInitialized)
            throw new Exception("Not initialized");

        var stepDone = false;

        if (TryWin(out var winMove))
        {
            ApplyMove(winMove.X, winMove.Y, true); // AI move (O)
            stepDone = true;
        }

        if (TryBlock(out var blockMove) && !stepDone)
        {
            ApplyMove(blockMove.X, blockMove.Y, true); // AI move (O)
            stepDone = true;
        }

        if (!stepDone)
            MakeRandomMove();

        if (IsWin())
        {
            IsPlayerWonOrTie = false;
            IsEnd = true;
            return new StepResult
            {
                Status = true,
                Message = "AI won"
            };
        }

        if (IsTie())
        {
            IsPlayerWonOrTie = true;
            IsEnd = true;
            return new StepResult
            {
                Status = true,
                Message = "Tie"
            };
        }

        IsPlayerStep = true;

        return new StepResult
        {
            Status = true
        };
    }

    private void ApplyMove(int x, int y, bool isPlayer)
    {
        if (Board![x][y] != null)
        {
            throw new Exception("This cell is already occupied");
        }

        Board![x][y] = isPlayer;

        if (!isPlayer)
        {
            IsPlayerStep = false;
        }
    }

    private bool TryWin(out (int X, int Y) winMove)
    {
        winMove = default;

        for (int i = 0; i < 10; i++)
        {
            if (TryWinningMoveInRow(i, out winMove))
            {
                return true;
            }

            if (TryWinningMoveInColumn(i, out winMove))
            {
                return true;
            }
        }

        if (TryWinningMoveInDiagonals(out winMove))
        {
            return true;
        }

        return false;
    }

    private bool TryWinningMoveInRow(int row, out (int X, int Y) winMove)
    {
        winMove = default;

        for (int j = 0; j < 10; j++)
        {
            if (Board![row][j] == null)
            {
                winMove = (row, j);
                return true;
            }
        }

        return false;
    }

    private bool TryWinningMoveInColumn(int col, out (int X, int Y) winMove)
    {
        winMove = default;

        for (int i = 0; i < 10; i++)
        {
            if (Board![i][col] == null)
            {
                winMove = (i, col);
                return true;
            }
        }

        return false;
    }

    private bool TryWinningMoveInDiagonals(out (int X, int Y) winMove)
    {
        winMove = default;

        // Check main diagonal
        for (int i = 0; i < 10; i++)
        {
            if (Board![i][i] == null)
            {
                winMove = (i, i);
                return true;
            }
        }

        // Check other diagonal
        for (int i = 0; i < 10; i++)
        {
            if (Board![i][9 - i] == null)
            {
                winMove = (i, 9 - i);
                return true;
            }
        }

        return false;
    }

    private bool TryBlock(out (int X, int Y) blockMove)
    {
        blockMove = default;

        // Check for a blocking move in rows, columns, or diagonals
        for (int i = 0; i < 10; i++)
        {
            // Check rows
            if (TryBlockingMoveInRow(i, out blockMove))
            {
                return true;
            }

            // Check columns
            if (TryBlockingMoveInColumn(i, out blockMove))
            {
                return true;
            }
        }

        // Check diagonals
        if (TryBlockingMoveInDiagonals(out blockMove))
        {
            return true;
        }

        return false;
    }

    private bool TryBlockingMoveInRow(int row, out (int X, int Y) blockMove)
    {
        blockMove = default;

        for (int j = 0; j < 10; j++)
        {
            if (Board![row][j] == null)
            {
                blockMove = (row, j);
                return true;
            }
        }

        return false;
    }

    private bool TryBlockingMoveInColumn(int col, out (int X, int Y) blockMove)
    {
        blockMove = default;

        for (int i = 0; i < 10; i++)
        {
            if (Board![i][col] == null)
            {
                blockMove = (i, col);
                return true;
            }
        }

        return false;
    }

    private bool TryBlockingMoveInDiagonals(out (int X, int Y) blockMove)
    {
        blockMove = default;

        // Check main diagonal
        for (int i = 0; i < 10; i++)
        {
            if (Board![i][i] == null)
            {
                blockMove = (i, i);
                return true;
            }
        }

        // Check other diagonal
        for (int i = 0; i < 10; i++)
        {
            if (Board![i][9 - i] == null)
            {
                blockMove = (i, 9 - i);
                return true;
            }
        }

        return false;
    }

    private void MakeRandomMove()
    {
        // Find an empty cell and make a random move
        var emptyCells = new List<(int X, int Y)>();

        for (int i = 0; i < 10; i++)
        {
            for (int j = 0; j < 10; j++)
            {
                if (Board![i][j] == null)
                {
                    emptyCells.Add((i, j));
                }
            }
        }

        if (emptyCells.Count > 0)
        {
            // Make a random move
            var randomMove = emptyCells[new Random().Next(emptyCells.Count)];
            ApplyMove(randomMove.X, randomMove.Y, true); // AI move (O)
        }
    }

    public bool IsWin()
    {
        // Check for a win in rows, columns, or diagonals
        for (int i = 0; i < 10; i++)
        {
            if (CheckRowForWin(i) || CheckColumnForWin(i))
            {
                return true;
            }
        }

        return CheckDiagonalsForWin();
    }

    private bool CheckRowForWin(int row)
    {
        for (int col = 0; col < 10; col++)
        {
            if (Board![row][col] == null || Board![row][col] != Board![row][0])
            {
                return false;
            }
        }

        return true;
    }

    private bool CheckColumnForWin(int col)
    {
        for (int row = 0; row < 10; row++)
        {
            if (Board![row][col] == null || Board![row][col] != Board![0][col])
            {
                return false;
            }
        }

        return true;
    }

    private bool CheckDiagonalsForWin()
    {
        // Check main diagonal (top-left to bottom-right)
        for (int i = 0; i < 10 - 2; i++)
        {
            for (int j = 0; j < 10 - 2; j++)
            {
                if (Board![i][j] != null &&
                    Board![i][j] == Board![i + 1][j + 1] &&
                    Board![i + 1][j + 1] == Board![i + 2][j + 2])
                {
                    return true;
                }
            }
        }

        // Check other diagonal (top-right to bottom-left)
        for (int i = 0; i < 10 - 2; i++)
        {
            for (int j = 2; j < 10; j++)
            {
                if (Board![i][j] != null &&
                    Board![i][j] == Board![i + 1][j - 1] &&
                    Board![i + 1][j - 1] == Board![i + 2][j - 2])
                {
                    return true;
                }
            }
        }

        return false;
    }


    public bool IsTie()
    {
        for (int i = 0; i < 10; i++)
        {
            for (int j = 0; j < 10; j++)
            {
                if (Board![i][j] == null)
                {
                    return false;
                }
            }
        }

        return true;
    }
}