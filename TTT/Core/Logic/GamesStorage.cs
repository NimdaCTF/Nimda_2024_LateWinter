using System.Collections;
using Core.Models;

namespace Core.Logic;

public class GamesStorage : IList<Game>
{
    private readonly List<Game> _games;

    public GamesStorage()
    {
        _games = new List<Game>();
    }

    public IEnumerator<Game> GetEnumerator()
    {
        return _games.GetEnumerator();
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        return GetEnumerator();
    }

    public void Add(Game item)
    {
        if (_games.Any(x => x.Uid == item.Uid) || _games.Any(x => x.UserId == item.UserId && !x.IsEnd))
        {
            throw new Exception("Game with this uid or with this userid is already on air.");
        }

        _games.Add(item);
    }

    public void Clear()
    {
        _games.Clear();
    }

    public bool Contains(Game item)
    {
        return _games.Contains(item);
    }

    public void CopyTo(Game[] array, int arrayIndex)
    {
        _games.CopyTo(array, arrayIndex);
    }

    public bool Remove(Game item)
    {
        return _games.Remove(item);
    }

    public int Count => _games.Count;
    public bool IsReadOnly => false;

    public int IndexOf(Game item)
    {
        return _games.IndexOf(item);
    }

    public void Insert(int index, Game item)
    {
        throw new NotImplementedException();
    }

    public void RemoveAt(int index)
    {
        _games.RemoveAt(index);
    }

    public Game this[int index]
    {
        get => _games[index];
        set => _games[index] = value;
    }
}