using Core.Models;
using System.Text.Json;
using Microsoft.Extensions.Configuration;

namespace Infrastructure.Io
{
    public class QuizLoader
    {
        private readonly string _filePath;

        public List<QuizItem> LoadedItems { get; private set; }

        public QuizLoader(IConfiguration configuration)
        {
            _filePath = configuration["Quiz:FilePath"]!;
            LoadedItems = LoadQuizItems();
        }

        private List<QuizItem> LoadQuizItems()
        {
            try
            {
                var jsonContent = File.ReadAllText(_filePath);

                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };

                var quizData = JsonSerializer.Deserialize<Dictionary<string, QuizData>>(jsonContent, options)!;

                var quizItems = new List<QuizItem>();

                foreach (var kvp in quizData)
                {
                    var quizItem = new QuizItem
                    {
                        Question = kvp.Key,
                        Answer = kvp.Value.Answer.ToString(),
                        FakeAnswers = kvp.Value.Fakes.Select(x => x.ToString()).ToList()
                    };

                    quizItems.Add(quizItem);
                }

                return quizItems;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
                return new List<QuizItem>();
            }
        }

        private class QuizData
        {
            public int Answer { get; set; }
            public List<int> Fakes { get; set; }
        }
    }
}