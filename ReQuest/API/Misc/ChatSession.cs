using System.Net.Sockets;
using System.Text;
using Core.Logic;
using Core.Models;
using Infrastructure.Io;
using NetCoreServer;

namespace API.Misc;

class ChatSession : TcpSession
{
    private GameSession? _gameSession;
    private List<QuizItem>? _quizItems;
    private readonly IConfiguration _configuration;
    private readonly QuizLoader _quizLoader;

    private List<QuizItem> QuizItems
    {
        get
        {
            if (_quizItems is null)
            {
                _quizItems = _quizLoader.LoadedItems;
            }

            return _quizItems;
        }
    }

    public ChatSession(TcpServer server, IConfiguration configuration, QuizLoader quizLoader) : base(server)
    {
        _configuration = configuration;
        _quizLoader = quizLoader;
        server.OptionTcpKeepAliveTime = 10000;
    }

    protected override void OnConnected()
    {
        Console.WriteLine($"Chat TCP session with Id {Id} connected!");

        var message = @"Welcome to ReQuest.
Pass my cool quiz
Give me ur userId: ";

        SendAsync(message);
    }

    protected override void OnDisconnected()
    {
        Console.WriteLine($"Chat TCP session with Id {Id} disconnected!");
        Dispose();
    }

    protected override void OnReceived(byte[] buffer, long offset, long size)
    {
        string message = Encoding.UTF8.GetString(buffer, (int)offset, (int)size);
        Console.WriteLine("Incoming: " + message);

        if (_gameSession is null)
        {
            if (String.IsNullOrEmpty(message.ReplaceLineEndings("")))
            {
                SendAsync("Invalid userId");
                Disconnect();
                return;
            }
            
            _gameSession = new GameSession(message, QuizItems);
            SendAsync($"\n{_gameSession.GetNext()!.Formatted()}");

            return;
        }

        int.TryParse(message, out var choice);
        if (!_gameSession!.Check(choice))
        {
            // SendAsync($"\nNo. Correct answer was: {_gameSession.CurrentItem.Answer}");
            SendAsync($"\nNo"); // XD
            Disconnect();
            return;
        }

        SendAsync("\nGood one.");
        var item = _gameSession.GetNext();

        if (item is null)
        {
            SendAsync(
                $"\nU won\n{_gameSession.GetFlag(_configuration["Flag:Secret"]!, _configuration["Flag:Prefix"]!, int.Parse(_configuration["Flag:SaltSize"]!))}"); // TODO
            Disconnect();
            return;
        }

        SendAsync($"\n{item.Formatted()}");
    }

    protected override void OnError(SocketError error)
    {
        Console.WriteLine($"Chat TCP session caught an error with code {error}");
    }

    private void Disconnect(object state)
    {
        Disconnect();
    }
}