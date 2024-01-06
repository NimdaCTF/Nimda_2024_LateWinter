using System.Net;
using System.Net.Sockets;
using Infrastructure.Io;
using NetCoreServer;

namespace API.Misc;

class ChatServer : TcpServer
{
    private readonly IConfiguration _configuration;
    private readonly QuizLoader _quizLoader;

    public ChatServer(IPAddress address, int port, IConfiguration configuration, QuizLoader quizLoader) : base(address, port)
    {
        _configuration = configuration;
        _quizLoader = quizLoader;
    }

    protected override TcpSession CreateSession()
    {
        return new ChatSession(this, _configuration, _quizLoader);
    }

    protected override void OnError(SocketError error)
    {
        Console.WriteLine($"Chat TCP server caught an error with code {error}");
    }
}