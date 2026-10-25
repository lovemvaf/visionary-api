using System;
using System.IO;
using System.Linq;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Visionary.Infrastructure.Data;
using Xunit;

namespace Visionary.Tests
{
    public class CustomWebApplicationFactory : WebApplicationFactory<Program>
    {
        private readonly string _testDbPath = Path.Combine(Path.GetTempPath(), $"visionary_test_{Guid.NewGuid():N}.db");

        protected override void ConfigureWebHost(IWebHostBuilder builder)
        {
            builder.UseEnvironment("Development");
            builder.ConfigureServices(services =>
            {
                var descriptors = services.Where(d =>
                    d.ServiceType == typeof(DbContextOptions<AppDbContext>) ||
                    d.ServiceType == typeof(AppDbContext)).ToList();

                foreach (var descriptor in descriptors)
                {
                    services.Remove(descriptor);
                }

                services.AddDbContext<AppDbContext>(options =>
                {
                    options.UseSqlite($"Data Source={_testDbPath}");
                });

                services.AddScoped<Visionary.Core.Interfaces.IAppDbContext>(p => p.GetRequiredService<AppDbContext>());
            });
        }

        protected override void Dispose(bool disposing)
        {
            base.Dispose(disposing);
            try
            {
                if (File.Exists(_testDbPath))
                {
                    File.Delete(_testDbPath);
                }
            }
            catch
            {
                // Ignore transient file lock
            }
        }
    }

    [CollectionDefinition("IntegrationTests")]
    public class IntegrationTestCollection : ICollectionFixture<CustomWebApplicationFactory>
    {
    }
}
