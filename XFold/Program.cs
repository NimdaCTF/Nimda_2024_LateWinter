using System.Security.Cryptography;
using System.Text;

namespace XFold;

// For HighWay

public static class Program
{
    private static string Secret => "folder-knock-rude-justin-in-time-key";
    private static string Prefix => "nimda_h!gh3sT_W@y_Is_OuR_WaYYyyyy_";
    private static int SaltSize => 12;
    
    public static string GetFlag(string userId)
    {
        var key = Encoding.UTF8.GetBytes(Secret);
        using (var hmac = new HMACSHA256(key))
        {
            var result = Convert.ToHexString(hmac.ComputeHash(Encoding.UTF8.GetBytes(userId))).ToLower()
                .Take(SaltSize);
            return Prefix + String.Join("", result);
        }
    }

    public static void Main(string[] args)
    {
        if (args.Length != 1)
        {
            Environment.Exit(-1);
        }
        
        Console.WriteLine(GetFlag(args[0]));
    }
}