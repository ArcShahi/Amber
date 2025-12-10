import praw
from html import escape
import sys

# Reddit API credentials 
reddit = praw.Reddit(
    client_id="<CLIENT_ID>",
    client_secret="<CLIENT_SECRET>",
    user_agent="<USER_AGENT>"
)


def archive_post(url, output="archive.html"):
    post = reddit.submission(url=url)
    post.comments.replace_more(limit=None)
    
    html_data = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{escape(post.title)}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>{escape(post.title)}</h1>
    <p><span class='author'>{escape(str(post.author))}</span> | Score: {post.score}</p>
    <div>{escape(post.selftext).replace(chr(10), '<br>')}</div>
    
"""
    
    # Include post media if any
    if post.url != post.permalink:
        html_data += f"<p>Media / Link: <a href='{escape(post.url)}'>{escape(post.url)}</a></p>"
        
    html_data += "<hr><h2>Comments</h2>"
    
    def parse_comment(comments, depth=0):
        html = ""
        for comment in comments:
            html += f"<div class='comment' style='margin-left:{depth*20}px'>"
            html += f"<p><span class='author'>{escape(str(comment.author))}</span> | Score: {comment.score}</p>"
            html += f"<p>{escape(comment.body).replace(chr(10), '<br>')}</p>"
            
            # Recursively parse replies
            html += parse_comment(comment.replies, depth + 1)
            html += "</div>"
        return html
    
    html_data += parse_comment(post.comments)
    html_data += "</body></html>"
    
    with open(output, "w", encoding="utf-8") as f:
        f.write(html_data)
        
    print(f"Archived '{post.title}' to {output}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python amber.py <reddit_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    archive_post(url)