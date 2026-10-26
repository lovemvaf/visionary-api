using System;
using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Builder;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using Visionary.Api.Middleware;
using Visionary.Core.Interfaces;
using Visionary.Infrastructure.Data;
using Visionary.Infrastructure.Services;

var builder = WebApplication.CreateBuilder(args);

// Dynamically bind to PORT if provided by cloud hosting (Render, Cloud Run, etc.)
var port = Environment.GetEnvironmentVariable("PORT");
if (!string.IsNullOrEmpty(port))
{
    builder.WebHost.UseUrls($"http://0.0.0.0:{port}");
}

// Add Controllers & JSON Options
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase;
        options.JsonSerializerOptions.DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull;
    });

// Configure Database: PostgreSQL is mandatory in Production. SQLite is only permitted in Development/Test environments.
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection") ?? "Data Source=visionary.db";
builder.Services.AddDbContext<AppDbContext>(options =>
{
    var isPostgres = connectionString.Contains("Host=", StringComparison.OrdinalIgnoreCase) ||
                     connectionString.Contains("Username=", StringComparison.OrdinalIgnoreCase) ||
                     connectionString.StartsWith("postgres://", StringComparison.OrdinalIgnoreCase) ||
                     connectionString.StartsWith("postgresql://", StringComparison.OrdinalIgnoreCase);

    if (isPostgres)
    {
        var connStr = connectionString;
        if (connStr.StartsWith("postgres://", StringComparison.OrdinalIgnoreCase) ||
            connStr.StartsWith("postgresql://", StringComparison.OrdinalIgnoreCase))
        {
            try
            {
                var uri = new Uri(connStr);
                var userInfo = uri.UserInfo.Split(':');
                var user = userInfo.Length > 0 ? Uri.UnescapeDataString(userInfo[0]) : "";
                var pass = userInfo.Length > 1 ? Uri.UnescapeDataString(userInfo[1]) : "";
                var port = uri.Port > 0 ? uri.Port : 5432;
                var dbName = uri.AbsolutePath.TrimStart('/');
                connStr = $"Host={uri.Host};Port={port};Database={dbName};Username={user};Password={pass};SSL Mode=Require;Trust Server Certificate=true";
            }
            catch
            {
                // Use original string if URI parsing fails
            }
        }
        options.UseNpgsql(connStr);
    }
    else
    {
        if (builder.Environment.IsProduction())
        {
            throw new InvalidOperationException("CRITICAL ERROR: Production environment mandates a valid PostgreSQL connection string (DefaultConnection). Silent fallback to SQLite/InMemory is strictly disabled to prevent database divergence and data loss.");
        }
        options.UseSqlite(connectionString);
    }
});

builder.Services.AddScoped<IAppDbContext>(provider => provider.GetRequiredService<AppDbContext>());

// Add Services
builder.Services.AddMemoryCache();
builder.Services.AddHttpClient();
builder.Services.AddScoped<IPasswordHasher, PasswordHasher>();
builder.Services.AddScoped<IJwtService, JwtService>();
builder.Services.AddScoped<ICacheService, CacheService>();
builder.Services.AddScoped<IDataAutomationService, DataAutomationService>();

// Configure JWT Authentication: Read from JWT_SECRET or config, enforce strong key in production
var rawJwtKey = Environment.GetEnvironmentVariable("JWT_SECRET")
    ?? builder.Configuration["Jwt:Key"]
    ?? builder.Configuration["Jwt:SigningKey"];

if (string.IsNullOrWhiteSpace(rawJwtKey) ||
    rawJwtKey.Contains("YOUR_DEVELOPMENT_JWT", StringComparison.OrdinalIgnoreCase) ||
    rawJwtKey.Contains("YOUR_SECURE_JWT", StringComparison.OrdinalIgnoreCase))
{
    if (builder.Environment.IsProduction())
    {
        throw new InvalidOperationException("CRITICAL SECURITY ERROR: In production environment, JWT_SECRET or Jwt:Key environment variable must be explicitly configured with at least 32 characters. Default or placeholder keys are prohibited.");
    }
    rawJwtKey = "DevOnlyJwtSecureSecretKeyForTestingAndLocalDevelopmentOnly32Chars!";
}

if (rawJwtKey.Length < 32)
{
    throw new InvalidOperationException("CRITICAL SECURITY ERROR: JWT Secret Key must be at least 32 characters (256 bits) for HMAC-SHA256.");
}
var jwtKey = rawJwtKey;
var issuer = builder.Configuration["Jwt:Issuer"] ?? "VisionaryApi";
var audience = builder.Configuration["Jwt:Audience"] ?? "VisionaryClients";

builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.RequireHttpsMetadata = builder.Environment.IsProduction();
    options.SaveToken = true;
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey)),
        ValidateIssuer = true,
        ValidIssuer = issuer,
        ValidateAudience = true,
        ValidAudience = audience,
        ValidateLifetime = true,
        ClockSkew = TimeSpan.Zero
    };
});

builder.Services.AddAuthorization();

// Configure CORS: Strictly allow validated web origins, preview branches, and local development
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.SetIsOriginAllowed(origin =>
        {
            if (string.IsNullOrEmpty(origin)) return true;
            try
            {
                var uri = new Uri(origin);
                return uri.Host.Equals("visionary-platform.vercel.app", StringComparison.OrdinalIgnoreCase) ||
                       uri.Host.Equals("visionary-global.vercel.app", StringComparison.OrdinalIgnoreCase) ||
                       uri.Host.EndsWith(".vercel.app", StringComparison.OrdinalIgnoreCase) ||
                       uri.Host.Equals("localhost", StringComparison.OrdinalIgnoreCase) ||
                       uri.Host.Equals("127.0.0.1", StringComparison.OrdinalIgnoreCase);
            }
            catch
            {
                return false;
            }
        })
        .AllowAnyHeader()
        .AllowAnyMethod();
    });
});

// Configure Swagger / OpenAPI
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "VISIONARY API – Hệ thống Quản lý Hoạt động Hội nhập DNTU",
        Version = "v1",
        Description = "RESTful API cung cấp dữ liệu thống nhất cho Web Next.js, Windows Forms C# và Android Java.\nNhóm phát triển: VISIONARY API (Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàn Nguyên Khang, Đào Trí Khang)."
    });

    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "Nhập mã JWT theo định dạng: Bearer {token}",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });

    c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            Array.Empty<string>()
        }
    });
});

var app = builder.Build();

// Seed initial database
try
{
    using (var scope = app.Services.CreateScope())
    {
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var hasher = scope.ServiceProvider.GetRequiredService<IPasswordHasher>();
        await DbInitializer.SeedAsync(db, hasher);
    }
}
catch (Exception ex)
{
    Console.WriteLine($"[DB INIT ERROR] Seeding warning or retry needed: {ex.Message}");
    if (ex.InnerException != null)
    {
        Console.WriteLine($"[DB INIT INNER ERROR] {ex.InnerException.Message}");
    }
}

// Pipeline Configuration
app.UseMiddleware<ExceptionHandlingMiddleware>();

app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "VISIONARY API v1");
    c.RoutePrefix = "swagger";
});

// Apply CORS policy
app.UseCors();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

// Health Check Endpoints
app.MapGet("/", () => Results.Ok(new
{
    service = "VISIONARY API – English, Technology & Global Integration Platform",
    status = "Healthy",
    version = "1.0.0",
    documentation = "/swagger",
    timestamp = DateTime.UtcNow
}));

app.MapGet("/health/live", () => Results.Ok(new
{
    status = "Alive",
    service = "VISIONARY ASP.NET Core Web API",
    timestamp = DateTime.UtcNow
}));

app.MapGet("/health/ready", async (AppDbContext db) =>
{
    try
    {
        var canConnect = await db.Database.CanConnectAsync();
        if (canConnect)
        {
            return Results.Ok(new
            {
                status = "Ready",
                database = "Connected",
                timestamp = DateTime.UtcNow
            });
        }
        return Results.StatusCode(503);
    }
    catch
    {
        return Results.Json(new
        {
            status = "NotReady",
            database = "Disconnected",
            timestamp = DateTime.UtcNow
        }, statusCode: 503);
    }
});

app.Run();

public partial class Program { }
