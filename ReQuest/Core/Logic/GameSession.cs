using System.Security.Cryptography;
using System.Text;
using Core.Models;

namespace Core.Logic;

public class GameSession
{
    private string _userId;
    private readonly List<QuizItem> _items;
    private int _nextItemIndex = 0;
    public QuizItem CurrentItem => _items[_nextItemIndex - 1];

    public GameSession(string userId, List<QuizItem> items)
    {
        _userId = userId;
        _items = items;
    }

    public QuizItem? GetNext()
    {
        if (_items.Count <= _nextItemIndex)
        {
            return null;
        }

        var item = _items[_nextItemIndex];
        _nextItemIndex++;
        return item;
    }

    public string GetFlag(string flagSecret, string flagPrefix, int saltSize)
    {
        var key = Encoding.UTF8.GetBytes(flagSecret);
        using (var hmac = new HMACSHA256(key))
        {
            var result = Convert.ToHexString(hmac.ComputeHash(Encoding.UTF8.GetBytes(_userId))).ToLower()
                .Take(saltSize);
            return flagPrefix + String.Join("", result);
        }
    }

    public bool Check(int choice)
    {
        return choice - 1 == CurrentItem.GetCorrectAnswerIndex();
    }
}