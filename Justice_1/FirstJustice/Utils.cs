using System;
using System.Security.Cryptography;
using System.Text;

namespace FirstJustice.Utils
{
    public static class Utils
    {
        public static string GetFlag(string user_id, string prefix, string secret, int saltSize)
        {
            var key = Encoding.UTF8.GetBytes(prefix);
            using (var hmac = new HMACSHA256(key))
            {
                var resultBytes = hmac.ComputeHash(Encoding.UTF8.GetBytes(user_id));
                var result = BitConverter.ToString(resultBytes).Replace("-", "").ToLower().Substring(0, saltSize);
                return prefix + result;
            }
        }
    }
}
