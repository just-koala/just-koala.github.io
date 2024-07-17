using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using HtmlAgilityPack;

// Configuration
const string GITHUB_REPO = "your-username/your-repo-name";
string GITHUB_TOKEN = Environment.GetEnvironmentVariable("KOALA_TOKEN");

// Fetch issues from GitHub
async Task<JArray> FetchIssues(string repo)
{
    string url = $"https://api.github.com/repos/{repo}/issues";
    using var client = new HttpClient();
    client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("token", GITHUB_TOKEN);
    client.DefaultRequestHeaders.UserAgent.ParseAdd("Mozilla/5.0 (compatible; GrandCircus/1.0)");
    var response = await client.GetStringAsync(url);
    return JArray.Parse(response);
}

// Generate blog post from issue
string GeneratePost(JObject issue)
{
    string template = File.ReadAllText("template.html");
    string title = issue["title"].ToString();
    string body = issue["body"].ToString();

    var doc = new HtmlDocument();
    doc.LoadHtml(template);
    doc.DocumentNode.SelectSingleNode("//title").InnerHtml = title;
    doc.DocumentNode.SelectSingleNode("//h1").InnerHtml = title;
    doc.DocumentNode.SelectSingleNode("//div").InnerHtml = body;

    return doc.DocumentNode.OuterHtml;
}

// Main function
async Task Main()
{
    var issues = await FetchIssues(GITHUB_REPO);
    Directory.CreateDirectory("posts");

    foreach (JObject issue in issues)
    {
        if (issue["labels"].ToString().Contains("blog"))
        {
            string filename = $"posts/{issue["title"].ToString().Replace(' ', '_')}.html";
            File.WriteAllText(filename, GeneratePost(issue));
        }
    }
}

await Main();
