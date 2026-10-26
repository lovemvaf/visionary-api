using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using Visionary.Core.Entities;
using Visionary.Core.Interfaces;

namespace Visionary.Infrastructure.Services
{
    public class JwtService : IJwtService
    {
        private const string LocalDevFallbackKey = "DevOnlyJwtSecureSecretKeyForTestingAndLocalDevelopmentOnly32Chars!";
        private readonly IConfiguration _configuration;

        public JwtService(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        private string ResolveSigningKey()
        {
            var key = Environment.GetEnvironmentVariable("JWT_SECRET")
                ?? _configuration["Jwt:Key"]
                ?? _configuration["Jwt:SigningKey"];

            if (string.IsNullOrWhiteSpace(key) ||
                key.Contains("YOUR_DEVELOPMENT_JWT", StringComparison.OrdinalIgnoreCase) ||
                key.Contains("YOUR_SECURE_JWT", StringComparison.OrdinalIgnoreCase))
            {
                var env = Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT");
                if (string.Equals(env, "Production", StringComparison.OrdinalIgnoreCase))
                {
                    throw new InvalidOperationException("CRITICAL SECURITY ERROR: Production environment mandates an explicitly configured JWT_SECRET environment variable with at least 32 characters.");
                }
                return LocalDevFallbackKey;
            }

            if (key.Length < 32)
            {
                throw new InvalidOperationException("CRITICAL SECURITY ERROR: JWT Secret Key must be at least 32 characters (256 bits) for HMAC-SHA256.");
            }

            return key;
        }

        public string GenerateToken(User user, IEnumerable<string> roles)
        {
            var jwtKey = ResolveSigningKey();
            var issuer = _configuration["Jwt:Issuer"] ?? "VisionaryApi";
            var audience = _configuration["Jwt:Audience"] ?? "VisionaryClients";
            var expiryMinutes = double.TryParse(_configuration["Jwt:ExpiryMinutes"], out var mins) ? mins : 1440; // 24 hours

            var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey));
            var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

            var claims = new List<Claim>
            {
                new(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
                new(JwtRegisteredClaimNames.Email, user.Email),
                new(ClaimTypes.NameIdentifier, user.Id.ToString()),
                new(ClaimTypes.Name, user.FullName),
                new("StudentId", user.StudentId ?? string.Empty),
                new(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
            };

            foreach (var role in roles)
            {
                claims.Add(new Claim(ClaimTypes.Role, role));
            }

            var token = new JwtSecurityToken(
                issuer: issuer,
                audience: audience,
                claims: claims,
                expires: DateTime.UtcNow.AddMinutes(expiryMinutes),
                signingCredentials: credentials);

            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        public bool ValidateToken(string token)
        {
            var jwtKey = ResolveSigningKey();
            var issuer = _configuration["Jwt:Issuer"] ?? "VisionaryApi";
            var audience = _configuration["Jwt:Audience"] ?? "VisionaryClients";

            var tokenHandler = new JwtSecurityTokenHandler();
            var validationParameters = new TokenValidationParameters
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

            try
            {
                tokenHandler.ValidateToken(token, validationParameters, out _);
                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}
