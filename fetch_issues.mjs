import { Octokit } from "@octokit/rest";
import fs from 'fs';
import path from 'path';

// Configuration
const GITHUB_TOKEN = process.env.MY_GITHUB_TOKEN;
const GITHUB_REPO = 'just-koala/just-koala.github.io';
const [owner, repo] = GITHUB_REPO.split('/');

// Initialize Octokit
const octokit = new Octokit({
  auth: GITHUB_TOKEN
});

// Fetch issues with the label 'blogpost'
async function fetchIssues() {
  const { data: issues } = await octokit.issues.listForRepo({
    owner,
    repo,
    labels: 'blogpost',
    state: 'open'
  });
  return issues;
}

// Generate HTML from issue data
function generateHtml(issue) {
    const title = issue.title;
    const body = issue.body;
  
    const html = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>${title}</title>
    </head>
    <body>
      <h1>${title}</h1>
      <div>${body}</div>
    </body>
    </html>
    `;
    return html;
  }

// Main function
(async () => {
    const issues = await fetchIssues();
    if (!fs.existsSync('posts')) {
      fs.mkdirSync('posts');
    }
    for (const issue of issues) {
      const filename = `posts/${issue.title.replace(/\s+/g, '_')}.html`;
      const html = generateHtml(issue);
      fs.writeFileSync(filename, html);
      console.log(`Generated ${filename}`);
    }
  })();
