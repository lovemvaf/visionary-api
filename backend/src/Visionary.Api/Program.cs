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
                     connectionString.StartsWith("postgres://", StringComparison.OrdinalIgnoreCase);

    if (isPostgres)
    {
        options.UseNpgsql(connectionString);
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

// Configure JWT Authentication
var jwtKey = builder.Configuration["Jwt:Key"] ?? "VisionaryPlatformSecretKey2026MasterExecutionSecureKeyDNTU_TH71108_API";
var issuer = builder.Configuration["Jwt:Issuer"] ?? "VisionaryApi";
var audience = builder.Configuration["Jwt:Audience"] ?? "VisionaryClients";

builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.RequireHttpsMetadata = false;
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

// Configure CORS: Support both specific production origins and desktop/mobile clients
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.WithOrigins(
                "https://visionary-platform.vercel.app",
                "https://visionary-global.vercel.app",
                "http://localhost:3000",
                "http://127.0.0.1:3000")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
    options.AddPolicy("PublicMobileDesktop", policy =>
    {
        policy.AllowAnyOrigin()
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
        Description = "RESTful API cung cấp dữ liệu thống nhất cho Web Next.js, Windows Forms C# và Android Java.\nNhóm phát triển: VISIONARY API (Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàng Nguyên Khang, Đào Trí Khang)."
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
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    var hasher = scope.ServiceProvider.GetRequiredService<IPasswordHasher>();
    await DbInitializer.SeedAsync(db, hasher);
}

// Pipeline Configuration
app.UseMiddleware<ExceptionHandlingMiddleware>();

app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "VISIONARY API v1");
    c.RoutePrefix = "swagger";
});

// Support both web and native clients
app.UseCors(policy => policy.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod());

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

// Health Check Endpoints
app.MapGet("/", () => Results.Ok(new
{
    Name = "VISIONARY API – English, Technology & Global Integration Platform",
    Team = "VISIONARY API",
    Members = new[] { "Quách Khoa Đức", "Võ Ngọc Minh Đạt", "Hồ Đoàng Nguyên Khang", "Đào Trí Khang" },
    Status = "Healthy",
    Documentation = "/swagger",
    Timestamp = DateTime.UtcNow
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
                provider = db.Database.ProviderName,
                timestamp = DateTime.UtcNow
            });
        }
        return Results.StatusCode(503);
    }
    catch (Exception ex)
    {
        return Results.Json(new
        {
            status = "NotReady",
            database = "Disconnected",
            error = ex.Message,
            timestamp = DateTime.UtcNow
        }, statusCode: 503);
    }
});

app.Run();

public partial class Program { }
