using API;
using Infrastructure.Io;

IHost host = Host.CreateDefaultBuilder(args)
    .ConfigureServices(services =>
    {
        services.AddSingleton<QuizLoader>();
        services.AddHostedService<Worker>();
    })
    .Build();

host.Run();
