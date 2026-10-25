using System.Collections.Generic;
using Microsoft.Extensions.Configuration;
using Visionary.Core.Entities;
using Visionary.Core.Enums;
using Visionary.Infrastructure.Services;
using Xunit;

namespace Visionary.Tests
{
    public class AuthTests
    {
        [Fact]
        public void PasswordHasher_ShouldHashAndVerifyCorrectly()
        {
            var hasher = new PasswordHasher();
            var rawPassword = "TestPassword@123";

            var hash = hasher.HashPassword(rawPassword);

            Assert.NotNull(hash);
            Assert.True(hasher.VerifyPassword(rawPassword, hash));
            Assert.False(hasher.VerifyPassword("WrongPassword", hash));
        }

        [Fact]
        public void JwtService_ShouldGenerateAndValidateToken()
        {
            var configData = new Dictionary<string, string?>
            {
                { "Jwt:Key", "SuperSecretTestingSecurityKeyForVisionaryPlatform2026" },
                { "Jwt:Issuer", "VisionaryTestApi" },
                { "Jwt:Audience", "VisionaryTestAudience" },
                { "Jwt:ExpiryMinutes", "60" }
            };

            var configuration = new ConfigurationBuilder()
                .AddInMemoryCollection(configData)
                .Build();

            var jwtService = new JwtService(configuration);
            var user = new User
            {
                Email = "student@visionary.dntu.edu.vn",
                FullName = "Nguyễn Văn A"
            };
            var roles = new List<string> { AppRoles.Student, AppRoles.ClubMember };

            var token = jwtService.GenerateToken(user, roles);

            Assert.False(string.IsNullOrWhiteSpace(token));
            Assert.True(jwtService.ValidateToken(token));
        }
    }
}
