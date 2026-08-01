using System.Net.Http.Json;

namespace HalstuchLernApp.Services;

public class ContentService
{
    private readonly HttpClient _httpClient;
    private ContentModel? _content;

    public ContentService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<ContentModel> GetContentAsync()
    {
        if (_content == null)
        {
            _content = await _httpClient.GetFromJsonAsync<ContentModel>("data/content.json")
                ?? new ContentModel();
        }
        return _content;
    }
}

public class ContentModel
{
    public List<LearningCategory> Categories { get; set; } = new();
}

public class LearningCategory
{
    public string Id { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string Icon { get; set; } = string.Empty;
    public List<LearningTopic> Topics { get; set; } = new();
}

public class LearningTopic
{
    public string Id { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string? Subtitle { get; set; }
    public string? Intro { get; set; }
    public string? Content { get; set; }
    public List<string>? Items { get; set; }
    public List<LearningSection>? Sections { get; set; }
    public List<string>? Verses { get; set; }
    public List<SongStanza>? Stanzas { get; set; }
    public string? Image { get; set; }
    public string? ImageAlt { get; set; }
}

public class LearningSection
{
    public string Title { get; set; } = string.Empty;
    public string Text { get; set; } = string.Empty;
}

public class SongStanza
{
    public string Label { get; set; } = string.Empty;
    public List<string> Lines { get; set; } = new();
}
