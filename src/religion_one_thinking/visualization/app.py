from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
from datetime import datetime
import markdown2  # Add this dependency to pyproject.toml

app = FastAPI()

# Get the current directory
current_dir = Path(__file__).parent

# Mount static files
app.mount("/static", StaticFiles(directory=str(current_dir / "static")), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(current_dir / "templates"))

@app.get("/")
async def read_logs(request: Request):
    logs_dir = Path("logs")
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = logs_dir / f"conversation_log_{today}.jsonl"
    
    if not log_file.exists():
        raise HTTPException(status_code=404, detail="No logs found for today")
        
    conversations = []
    with open(log_file, "r") as f:
        for line in f:
            conversations.append(json.loads(line))
    
    # Group conversations by round
    rounds = {}
    for conv in conversations:
        round_num = conv["metadata"]["round"]
        if round_num not in rounds:
            rounds[round_num] = []
        rounds[round_num].append(conv)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "rounds": rounds
        }
    )

@app.get("/conversation")
async def view_conversation(request: Request):
    """Display conversation in chat room format."""
    logs_dir = Path("logs")
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = logs_dir / f"conversation_log_{today}.jsonl"
    
    if not log_file.exists():
        raise HTTPException(status_code=404, detail="No logs found for today")
        
    conversations = []
    with open(log_file, "r") as f:
        for line in f:
            entry = json.loads(line)
            
            # Handle response content
            if "response" in entry and entry["response"]:
                try:
                    entry["response_html"] = markdown2.markdown(entry["response"])
                except Exception as e:
                    entry["response_html"] = f"<p>Error rendering markdown: {str(e)}</p>"
            else:
                entry["response_html"] = ""
                
            # Handle error content
            if "error" in entry and entry["error"]:
                try:
                    entry["error_html"] = markdown2.markdown(entry["error"])
                except Exception as e:
                    entry["error_html"] = f"<p>Error rendering markdown: {str(e)}</p>"
            else:
                entry["error_html"] = ""
                
            conversations.append(entry)
    
    return templates.TemplateResponse(
        "conversation.html",
        {
            "request": request,
            "conversations": conversations
        }
    )

@app.get("/conversation/export")
async def export_conversation():
    """Export conversation as markdown."""
    logs_dir = Path("logs")
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = logs_dir / f"conversation_log_{today}.jsonl"
    
    if not log_file.exists():
        raise HTTPException(status_code=404, detail="No logs found for today")
    
    markdown_content = f"# Religion One Conversation Log - {today}\n\n"
    
    with open(log_file, "r") as f:
        for line in f:
            entry = json.loads(line)
            timestamp = entry["timestamp"].split("T")[1].split(".")[0]
            thinker = entry["thinker"]
            round_num = entry["metadata"]["round"]
            
            markdown_content += f"## Round {round_num} - {thinker} ({timestamp})\n\n"
            
            if "error" in entry and entry["error"]:
                markdown_content += f"**Error:**\n\n```\n{entry['error']}\n```\n\n"
            elif "response" in entry and entry["response"]:
                markdown_content += f"{entry['response']}\n\n"
            
            markdown_content += "---\n\n"
    
    filename = f"religion_one_conversation_{today}.md"
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    
    return Response(
        content=markdown_content,
        media_type='text/markdown',
        headers=headers
    ) 