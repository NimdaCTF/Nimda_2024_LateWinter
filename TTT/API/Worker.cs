using System.Net;
using API.Misc;

namespace API;

public class Worker : BackgroundService
{
    private readonly ILogger<Worker> _logger;

    public Worker(ILogger<Worker> logger)
    {
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        int port = 1111;

        Console.WriteLine($"TCP server port: {port}");

        Console.WriteLine();

        var server = new ChatServer(IPAddress.Loopback, port);

        Console.Write("Server starting...");
        server.Start();
        Console.WriteLine("Done!");
    }
}