namespace Shared;

public static class RandomUtils
{
    public static void Shuffle<T>(List<T> list)
    {
        var random = new Random();

        var n = list.Count;
        for (var i = n - 1; i > 0; i--)
        {
            var j = random.Next(0, i + 1);
            (list[i], list[j]) = (list[j], list[i]);
        }
    }
}