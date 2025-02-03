import uvicorn

def main():
    """Run the visualization server."""
    uvicorn.run(
        "religion_one_thinking.visualization.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"]
    )

if __name__ == "__main__":
    main() 