# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
WORKDIR /source

# Copy csproj files for API and required dependencies
COPY src/Visionary.Core/*.csproj src/Visionary.Core/
COPY src/Visionary.Infrastructure/*.csproj src/Visionary.Infrastructure/
COPY src/Visionary.Api/*.csproj src/Visionary.Api/

# Restore dependencies directly for Visionary.Api (avoids restoring desktop project)
RUN dotnet restore src/Visionary.Api/Visionary.Api.csproj

# Copy all source files and publish
COPY . .
WORKDIR /source/src/Visionary.Api
RUN dotnet publish -c Release -o /app/publish --no-restore

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS runtime
WORKDIR /app
COPY --from=build /app/publish .

ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
EXPOSE 8080

ENTRYPOINT ["dotnet", "Visionary.Api.dll"]
