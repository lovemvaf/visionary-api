using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Visionary.Core.Entities;

namespace Visionary.Core.Interfaces
{
    public interface IJwtService
    {
        string GenerateToken(User user, IEnumerable<string> roles);
        bool ValidateToken(string token);
    }

    public interface IPasswordHasher
    {
        string HashPassword(string password);
        bool VerifyPassword(string password, string hashedPassword);
    }

    public interface ICacheService
    {
        Task<T?> GetAsync<T>(string key);
        Task SetAsync<T>(string key, T value, TimeSpan? expiration = null);
        Task RemoveAsync(string key);
    }

    public interface IDataAutomationService
    {
        Task SyncGitHubTrendingAsync();
        Task SyncHuggingFaceModelsAsync();
        Task SyncTechNewsAsync();
    }
}
