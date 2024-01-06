using System.Net;
using API.Misc;
using Infrastructure.Io;

namespace API;

public class Worker : BackgroundService
{
    private readonly ILogger<Worker> _logger;
    private readonly IConfiguration _configuration;
    private readonly QuizLoader _quizLoader;

    public Worker(ILogger<Worker> logger, IConfiguration configuration, QuizLoader quizLoader)
    {
        _logger = logger;
        _configuration = configuration;
        _quizLoader = quizLoader;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var server = new ChatServer(IPAddress.Parse(_configuration["Host"]!), int.Parse(_configuration["Port"]!),
            _configuration, _quizLoader);

        Console.Write("Server starting...");
        server.Start();
        Console.WriteLine("Done!");
    }
}