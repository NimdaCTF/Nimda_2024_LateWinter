using System.Net.Sockets;
using System.Text;
using Core.Models;
using NetCoreServer;

namespace API.Misc;

class ChatSession : TcpSession
{
    private Game? _game;
    private Timer? _timeoutTimer;

    public ChatSession(TcpServer server) : base(server)
    {
        server.OptionTcpKeepAliveTime = 10000;
    }

    protected override void OnConnected()
    {
        Console.WriteLine($"Chat TCP session with Id {Id} connected!");

        var message = @"Welcome to Tac in Tick.
Try to win me 100 times in 100 seconds.
Press enter to start.";
        
        // TODO: Add UserId input
        SendAsync(message);
    }

    protected override void OnDisconnected()
    {
        Console.WriteLine($"Chat TCP session with Id {Id} disconnected!");
        _timeoutTimer?.Dispose();
        Dispose();
    }

    protected override void OnReceived(byte[] buffer, long offset, long size)
    {
        string message = Encoding.UTF8.GetString(buffer, (int)offset, (int)size);
        Console.WriteLine("Incoming: " + message);

        if (message == "\n")
        {
            if (_game is null)
            {
                _timeoutTimer = new Timer(Disconnect, null, TimeSpan.FromSeconds(100), Timeout.InfiniteTimeSpan);
                _game = new Game();
                _game.Initialize();
            }

            _game!.AiStep();
            SendAsync("\nTimer started. AI Step:\n");
            SendAsync(_game.DrawBoard());

            SendAsync("\n> ");

            return;
        }

        int x, y;

        try
        {
            x = int.Parse(message.Split()[0]);
            y = int.Parse(message.Split()[1]);
        }
        catch
        {
            SendAsync("\n{X} {Y} format needed, not your garbage");
            return;
        }

        var playerStep = _game!.PlayerStep(x, y);
        if (playerStep.Message is not null)
        {
            SendAsync("\n");
            SendAsync(playerStep.Message);
        }

        if (playerStep.Status)
        {
            SendAsync("\n");
            SendAsync(_game.DrawBoard());
        }
        else
        {
            SendAsync("\n> ");
            return;
        }

        if (_game.IsEnd)
        {
            Disconnect();
            Dispose();
        }

        var aiStep = _game!.AiStep();

        SendAsync("\nAI Step:\n");

        if (aiStep.Message is not null)
            SendAsync(aiStep.Message);

        SendAsync(_game.DrawBoard());

        if (_game.IsEnd)
        {
            Disconnect();
            Dispose();
        }

        SendAsync("\n> ");
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