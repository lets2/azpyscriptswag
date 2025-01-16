# base image for building the application
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

# copy and restore dependencies
COPY weatherapi.csproj ./
RUN dotnet restore

# copy the rest of the application and build
COPY . ./
RUN dotnet publish PrimeiroProjDotnet.sln -c Release -o /app/out

# base image for running the application
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/out .

EXPOSE 5074

ENTRYPOINT ["dotnet", "weatherapi.dll"]




