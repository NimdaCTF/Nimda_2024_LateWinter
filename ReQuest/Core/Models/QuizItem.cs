using Shared;

namespace Core.Models;

public class QuizItem
{
    public string Question { get; init; } = null!;
    public string Answer { get; init; } = null!;
    public List<string> FakeAnswers { get; init; } = null!;
    private List<string>? _shuffledAnswers;

    public List<string> ShuffledAnswers
    {
        get
        {
            if (_shuffledAnswers is null)
            {
                _shuffledAnswers = FakeAnswers;
                _shuffledAnswers.Add(Answer);
                RandomUtils.Shuffle(_shuffledAnswers);
            }

            return _shuffledAnswers;
        }
    }

    public int GetCorrectAnswerIndex()
    {
        for (var i = 0; i < ShuffledAnswers.Count; ++i)
        {
            if (ShuffledAnswers[i] == Answer)
                return i;
        }

        return -1;
    }

    public string Formatted()
    {
        return String.Format(@"ReQuest says: {0}
1. {1}
2. {2}
3. {3}
4. {4}
You says: ", Question, ShuffledAnswers[0], ShuffledAnswers[1], ShuffledAnswers[2], ShuffledAnswers[3]);
    }
}