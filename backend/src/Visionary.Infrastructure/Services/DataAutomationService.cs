using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Visionary.Core.Entities;
using Visionary.Core.Enums;
using Visionary.Core.Interfaces;
using Visionary.Infrastructure.Data;

namespace Visionary.Infrastructure.Services
{
    public class DataAutomationService : IDataAutomationService
    {
        private readonly AppDbContext _context;
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly ILogger<DataAutomationService> _logger;

        public DataAutomationService(
            AppDbContext context,
            IHttpClientFactory httpClientFactory,
            ILogger<DataAutomationService> logger)
        {
            _context = context;
            _httpClientFactory = httpClientFactory;
            _logger = logger;
        }

        public async Task SyncGitHubTrendingAsync()
        {
            var source = await _context.ContentSources.FirstOrDefaultAsync(s => s.Type == "GitHubApi");
            if (source == null || !source.IsEnabled) return;

            var run = new ImportRun
            {
                SourceId = source.Id,
                StartTime = DateTime.UtcNow,
                Status = "Running"
            };
            _context.ImportRuns.Add(run);
            await _context.SaveChangesAsync();

            try
            {
                var client = _httpClientFactory.CreateClient();
                client.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("VisionaryPlatform", "1.0"));
                client.Timeout = TimeSpan.FromSeconds(15);

                var response = await client.GetAsync("https://api.github.com/search/repositories?q=stars:>5000+topic:machine-learning&sort=stars&per_page=10");
                if (!response.IsSuccessStatusCode)
                {
                    run.Status = "Failed";
                    run.ErrorMessage = $"GitHub API returned {response.StatusCode}";
                    run.EndTime = DateTime.UtcNow;
                    source.LastStatus = run.Status;
                    source.LastRunAt = DateTime.UtcNow;
                    await _context.SaveChangesAsync();
                    return;
                }

                var content = await response.Content.ReadAsStringAsync();
                using var doc = JsonDocument.Parse(content);
                var items = doc.RootElement.GetProperty("items");

                int fetched = 0;
                int inserted = 0;

                foreach (var item in items.EnumerateArray())
                {
                    fetched++;
                    var fullName = item.GetProperty("full_name").GetString() ?? "";
                    var desc = item.TryGetProperty("description", out var d) && d.ValueKind == JsonValueKind.String ? d.GetString() : "No description provided.";
                    var url = item.GetProperty("html_url").GetString() ?? "";
                    var lang = item.TryGetProperty("language", out var l) && l.ValueKind == JsonValueKind.String ? l.GetString() : "Unknown";
                    var stars = item.GetProperty("stargazers_count").GetInt32();
                    var forks = item.GetProperty("forks_count").GetInt32();
                    var licenseName = item.TryGetProperty("license", out var lic) && lic.ValueKind == JsonValueKind.Object && lic.TryGetProperty("spdx_id", out var spdx) ? spdx.GetString() : "Open";

                    var existing = await _context.TechResources.FirstOrDefaultAsync(t => t.Name == fullName);
                    if (existing == null)
                    {
                        var resource = new TechResource
                        {
                            Name = fullName,
                            SourceType = TechSourceType.GitHubRepository,
                            ExternalId = fullName,
                            OfficialUrl = url,
                            Description = desc ?? "",
                            PrimaryLanguage = lang,
                            License = licenseName,
                            MetricsJson = $"{{\"stars\": {stars}, \"forks\": {forks}}}",
                            LearningSuitability = stars > 20000 ? "Highly Recommended" : "Recommended",
                            LastCheckedAt = DateTime.UtcNow,
                            IsVerified = true
                        };
                        _context.TechResources.Add(resource);
                        inserted++;
                    }
                    else
                    {
                        existing.Description = desc ?? existing.Description;
                        existing.MetricsJson = $"{{\"stars\": {stars}, \"forks\": {forks}}}";
                        existing.LastCheckedAt = DateTime.UtcNow;
                    }
                }

                run.ItemsFetched = fetched;
                run.ItemsInserted = inserted;
                run.Status = "Success";
                run.EndTime = DateTime.UtcNow;
                source.LastRunAt = DateTime.UtcNow;
                source.LastStatus = "Success";
                await _context.SaveChangesAsync();
                _logger.LogInformation("Successfully synced GitHub Trending. Fetched: {Fetched}, Inserted: {Inserted}", fetched, inserted);
            }
            catch (Exception ex)
            {
                run.Status = "Failed";
                run.ErrorMessage = ex.Message;
                run.EndTime = DateTime.UtcNow;
                source.LastRunAt = DateTime.UtcNow;
                source.LastStatus = "Failed";
                await _context.SaveChangesAsync();
                _logger.LogError(ex, "Error syncing GitHub Trending");
            }
        }

        public async Task SyncHuggingFaceModelsAsync()
        {
            var source = await _context.ContentSources.FirstOrDefaultAsync(s => s.Type == "HuggingFaceApi");
            if (source == null || !source.IsEnabled) return;

            var run = new ImportRun
            {
                SourceId = source.Id,
                StartTime = DateTime.UtcNow,
                Status = "Running"
            };
            _context.ImportRuns.Add(run);
            await _context.SaveChangesAsync();

            try
            {
                var client = _httpClientFactory.CreateClient();
                client.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("VisionaryPlatform", "1.0"));
                client.Timeout = TimeSpan.FromSeconds(15);

                var response = await client.GetAsync("https://huggingface.co/api/models?sort=likes7d&direction=-1&limit=10");
                if (!response.IsSuccessStatusCode)
                {
                    run.Status = "Failed";
                    run.ErrorMessage = $"Hugging Face API returned {response.StatusCode}";
                    run.EndTime = DateTime.UtcNow;
                    source.LastStatus = run.Status;
                    source.LastRunAt = DateTime.UtcNow;
                    await _context.SaveChangesAsync();
                    return;
                }

                var content = await response.Content.ReadAsStringAsync();
                using var doc = JsonDocument.Parse(content);

                int fetched = 0;
                int inserted = 0;

                foreach (var item in doc.RootElement.EnumerateArray())
                {
                    fetched++;
                    var id = item.GetProperty("id").GetString() ?? "";
                    var pipeline = item.TryGetProperty("pipeline_tag", out var p) && p.ValueKind == JsonValueKind.String ? p.GetString() : "text-generation";
                    var downloads = item.TryGetProperty("downloads", out var d) && d.ValueKind == JsonValueKind.Number ? d.GetInt32() : 0;
                    var likes = item.TryGetProperty("likes", out var l) && l.ValueKind == JsonValueKind.Number ? l.GetInt32() : 0;

                    var existing = await _context.TechResources.FirstOrDefaultAsync(t => t.Name == id);
                    if (existing == null)
                    {
                        var resource = new TechResource
                        {
                            Name = id,
                            SourceType = TechSourceType.HuggingFaceModel,
                            ExternalId = id,
                            OfficialUrl = $"https://huggingface.co/{id}",
                            Description = $"State-of-the-art AI model for {pipeline} on Hugging Face Hub.",
                            PrimaryLanguage = "Python / PyTorch",
                            License = "Open Source / Model Weights",
                            MetricsJson = $"{{\"downloads\": {downloads}, \"likes\": {likes}}}",
                            LearningSuitability = "AI/ML Research & Practice",
                            LastCheckedAt = DateTime.UtcNow,
                            IsVerified = true
                        };
                        _context.TechResources.Add(resource);
                        inserted++;
                    }
                    else
                    {
                        existing.MetricsJson = $"{{\"downloads\": {downloads}, \"likes\": {likes}}}";
                        existing.LastCheckedAt = DateTime.UtcNow;
                    }
                }

                run.ItemsFetched = fetched;
                run.ItemsInserted = inserted;
                run.Status = "Success";
                run.EndTime = DateTime.UtcNow;
                source.LastRunAt = DateTime.UtcNow;
                source.LastStatus = "Success";
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                run.Status = "Failed";
                run.ErrorMessage = ex.Message;
                run.EndTime = DateTime.UtcNow;
                source.LastRunAt = DateTime.UtcNow;
                source.LastStatus = "Failed";
                await _context.SaveChangesAsync();
                _logger.LogError(ex, "Error syncing Hugging Face models");
            }
        }

        public async Task SyncTechNewsAsync()
        {
            var source = await _context.ContentSources.FirstOrDefaultAsync(s => s.Type == "RssFeed");
            if (source == null || !source.IsEnabled) return;

            var run = new ImportRun
            {
                SourceId = source.Id,
                StartTime = DateTime.UtcNow,
                Status = "Running"
            };
            _context.ImportRuns.Add(run);
            await _context.SaveChangesAsync();

            try
            {
                var client = _httpClientFactory.CreateClient();
                client.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("VisionaryPlatform", "1.0"));
                client.Timeout = TimeSpan.FromSeconds(15);

                var response = await client.GetAsync("https://dev.to/api/articles?tag=programming&per_page=5");
                if (response.IsSuccessStatusCode)
                {
                    var content = await response.Content.ReadAsStringAsync();
                    using var doc = JsonDocument.Parse(content);

                    var techCategory = await _context.PostCategories.FirstOrDefaultAsync(c => c.Slug == "cong-nghe-ai");
                    var adminUser = await _context.Users.FirstOrDefaultAsync(u => u.Email == "quachkhoaduc@visionary.dntu.edu.vn");

                    if (techCategory != null && adminUser != null)
                    {
                        int fetched = 0;
                        int inserted = 0;

                        foreach (var item in doc.RootElement.EnumerateArray())
                        {
                            fetched++;
                            var title = item.GetProperty("title").GetString() ?? "";
                            var desc = item.TryGetProperty("description", out var d) ? d.GetString() ?? "" : "";
                            var url = item.GetProperty("url").GetString() ?? "";
                            var slug = "news-" + (item.TryGetProperty("slug", out var s) ? s.GetString() ?? Guid.NewGuid().ToString("N")[..8] : Guid.NewGuid().ToString("N")[..8]);

                            var existing = await _context.Posts.FirstOrDefaultAsync(p => p.Slug == slug);
                            if (existing == null)
                            {
                                var post = new Post
                                {
                                    CategoryId = techCategory.Id,
                                    AuthorUserId = adminUser.Id,
                                    Title = title,
                                    Slug = slug,
                                    Summary = desc.Length > 400 ? desc[..400] + "..." : desc,
                                    ContentMarkdown = $"### {title}\n\n{desc}\n\n[Đọc bài gốc trên nguồn tin chính thống]({url})",
                                    ContentHtml = $"<h3>{title}</h3><p>{desc}</p><p><a href='{url}' target='_blank' rel='noopener noreferrer'>Đọc bài gốc trên nguồn tin chính thống</a></p>",
                                    Status = PostStatus.Published,
                                    PublishedAt = DateTime.UtcNow
                                };
                                _context.Posts.Add(post);
                                inserted++;
                            }
                        }

                        run.ItemsFetched = fetched;
                        run.ItemsInserted = inserted;
                        run.Status = "Success";
                        run.EndTime = DateTime.UtcNow;
                        source.LastRunAt = DateTime.UtcNow;
                        source.LastStatus = "Success";
                        await _context.SaveChangesAsync();
                        return;
                    }
                }

                run.Status = "Failed";
                run.ErrorMessage = $"Dev.to API returned {response.StatusCode}";
                run.EndTime = DateTime.UtcNow;
                source.LastRunAt = DateTime.UtcNow;
                source.LastStatus = "Failed";
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                run.Status = "Failed";
                run.ErrorMessage = ex.Message;
                run.EndTime = DateTime.UtcNow;
                source.LastRunAt = DateTime.UtcNow;
                source.LastStatus = "Failed";
                await _context.SaveChangesAsync();
                _logger.LogError(ex, "Error syncing tech news");
            }
        }
    }
}
