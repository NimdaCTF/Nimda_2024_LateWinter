using System;
using System.Security.Cryptography;
using System.Text;

namespace TokenGenerator
{
    public static class TokenGenerator
    {
        public static string GetToken()
        {
            using (SHA512 sha512 = SHA512.Create())
            {
                var timestamp = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
                var token = $"{timestamp}";

                byte[] hashBytes = sha512.ComputeHash(Encoding.UTF8.GetBytes(token));

                StringBuilder hashStringBuilder = new StringBuilder();
                foreach (byte b in hashBytes)
                {
                    hashStringBuilder.Append(b.ToString("x2"));
                }

                return hashStringBuilder.ToString();
            }
        }
    }
}
