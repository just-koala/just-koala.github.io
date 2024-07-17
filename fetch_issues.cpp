#include <iostream>
#include <string>
#include <nlohmann/json.hpp>
#include <cpr/cpr.h>
#include <fstream>
#include <vector>
#include <htmlcxx/html/ParserDom.h>

// configurations
const std::string GITHUB_REPO = "just-koala/just-koala.github.io";
const std::string GITHUB_TOKEN = getenv("KOALA_TOKEN");

nlohmann::json fetch_issues(const std::string &repo)
{
    std::string url = "https://api.github.com/repos/" + repo + "/issues";
    cpr::Response r = cpr::Get(cpr::Url{url}, cpr::Header{{"Authorization", "token " + GITHUB_TOKEN}});
    return nlohmann::json::parse(r.text);
}

// Generate blog posts from issues
std::string generate_post(const nlohmann::json &issue)
{
    std::ifstream template_file("template.html");
    std::string template_str((std::istreambuf_iterator<char>(template_file)), std::istreambuf_iterator<char>());

    std::string title = issue["title"];
    std::string body = issue["body"];

    size_t title_pos = template_str.find("{{ title }}");
    if (title_pos != std::string::npos)
    {
        template_str.replace(title_pos, 10, title);
    }

    size_t content_pos = template_str.find("{{ content }}");
    if (content_pos != std::string::npos)
    {
        template_str.replace(content_pos, 12, body);
    }

    return template_str;
}

int main()
{
    nlohmann::json issues = fetch_issues(GITHUB_REPO);
    std::ofstream posts_dir("posts");

    for (auto &issue : issues)
    {
        for (auto &label : issue["labels"])
        {
            if (label["name"] == "blog")
            {
                std::string filename = "posts/" + issue["title"].get<std::string>() + ".html";
                std::ofstream post_file(filename);
                post_file << generate_post(issue);
            }
        }
    }
    return 0;
}