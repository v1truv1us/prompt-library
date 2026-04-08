#!/usr/bin/env python3
"""
Cost Tracker - TailClaude-style cost visibility for all coding harnesses
Tracks usage across OpenClaw sessions + ACP harnesses (Claude Code, Codex, OpenCode, etc.)
"""

import json
import os
import sys
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import re

# Paths
OPENCLAW_DIR = Path.home() / ".openclaw"
WORKSPACE = OPENCLAW_DIR / "workspace"
CLAUDE_DIR = Path.home() / ".claude"
CODEX_DIR = Path.home() / ".codex"
OPENCODE_DIR = Path.home() / ".opencode"
OPENCODE_DATA_DIR = Path.home() / ".local" / "share" / "opencode"

# Pricing per 1M tokens (as of 2026-04)
PRICING = {
    # GLM models (z.ai) - mostly free
    "glm-5": {"input": 0.0, "output": 0.0},
    "glm-5.1": {"input": 0.0, "output": 0.0},
    "glm-5-free": {"input": 0.0, "output": 0.0},
    "glm-4.7": {"input": 0.0, "output": 0.0},
    
    # OpenAI GPT models
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-5": {"input": 2.50, "output": 10.00},
    "gpt-5.4": {"input": 2.50, "output": 10.00},
    "gpt-5.3-codex": {"input": 3.00, "output": 15.00},
    "gpt-5-codex": {"input": 3.00, "output": 15.00},
    
    # Claude models
    "claude-3-opus": {"input": 15.00, "output": 75.00},
    "claude-3-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
    "claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "claude-opus-4": {"input": 15.00, "output": 75.00},
    "claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-opus-4.5": {"input": 15.00, "output": 75.00},
    
    # OpenCode specific models
    "big-pickle": {"input": 3.00, "output": 15.00},  # OpenCode's model
    
    # MiniMax models
    "mimo-v2-pro-free": {"input": 0.0, "output": 0.0},
    "mimo-v2-omni-free": {"input": 0.0, "output": 0.0},
    "minimax-m2.5-free": {"input": 0.0, "output": 0.0},
    
    # Kimi models
    "kimi-k2.5-free": {"input": 0.0, "output": 0.0},
    
    # NVIDIA/Nemotron models
    "nemotron-3-super-free": {"input": 0.0, "output": 0.0},
    
    # Qwen models
    "qwen3.6-plus-free": {"input": 0.0, "output": 0.0},
    
    # Grok models
    "grok-code": {"input": 3.00, "output": 15.00},
    
    # Gemini models
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    
    # Default fallback
    "default": {"input": 3.00, "output": 15.00},
}


def get_pricing(model_id):
    """Get pricing for a model, with fallback"""
    if not model_id:
        return PRICING["default"]
    
    model_lower = model_id.lower()
    for key, pricing in PRICING.items():
        if key in model_lower:
            return pricing
    return PRICING["default"]


def calculate_cost(usage, model_id):
    """Calculate cost from usage data"""
    if not usage:
        return 0.0
    
    pricing = get_pricing(model_id)
    input_tokens = usage.get("input", 0) or 0
    output_tokens = usage.get("output", 0) or 0
    
    cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000
    return cost


def parse_openclaw_sessions():
    """Parse OpenClaw session JSONL files"""
    sessions = []
    session_dirs = [
        OPENCLAW_DIR / "agents" / "main" / "sessions",
        OPENCLAW_DIR / "agents" / "default" / "sessions",
    ]
    
    for session_dir in session_dirs:
        if not session_dir.exists():
            continue
        
        for jsonl_file in session_dir.glob("*.jsonl"):
            try:
                session_data = {
                    "source": "openclaw",
                    "file": str(jsonl_file),
                    "messages": [],
                    "total_cost": 0,
                    "total_input": 0,
                    "total_output": 0,
                    "model": None,
                    "date": None,
                }
                
                with open(jsonl_file, 'r') as f:
                    for line in f:
                        if not line.strip():
                            continue
                        
                        try:
                            entry = json.loads(line)
                            
                            # Get session date from first entry
                            if not session_data["date"] and "timestamp" in entry:
                                ts = entry["timestamp"]
                                if isinstance(ts, str):
                                    session_data["date"] = ts[:10]  # YYYY-MM-DD
                            
                            # Track model
                            if entry.get("type") == "model_change":
                                session_data["model"] = entry.get("modelId", "unknown")
                            
                            # Parse messages with usage
                            if entry.get("type") == "message" and "message" in entry:
                                msg = entry["message"]
                                if msg.get("role") == "assistant" and "usage" in msg:
                                    usage = msg["usage"]
                                    model = msg.get("model", session_data["model"])
                                    
                                    # Calculate cost
                                    cost_data = usage.get("cost", {})
                                    if cost_data and cost_data.get("total"):
                                        cost = cost_data["total"]
                                    else:
                                        cost = calculate_cost(usage, model)
                                    
                                    msg_data = {
                                        "timestamp": msg.get("timestamp"),
                                        "input": usage.get("input", 0) or 0,
                                        "output": usage.get("output", 0) or 0,
                                        "cache_read": usage.get("cacheRead", 0) or 0,
                                        "cost": cost,
                                        "model": model,
                                    }
                                    
                                    session_data["messages"].append(msg_data)
                                    session_data["total_cost"] += cost
                                    session_data["total_input"] += msg_data["input"]
                                    session_data["total_output"] += msg_data["output"]
                        except json.JSONDecodeError:
                            continue
                
                if session_data["messages"]:
                    sessions.append(session_data)
            except Exception as e:
                print(f"Error reading {jsonl_file}: {e}", file=sys.stderr)
    
    return sessions


def parse_claude_code_sessions():
    """Parse Claude Code session files from ~/.claude/projects/"""
    sessions = []
    projects_dir = CLAUDE_DIR / "projects"
    
    if not projects_dir.exists():
        return sessions
    
    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue
        
        for session_file in project_dir.glob("*.jsonl"):
            try:
                session_data = {
                    "source": "claude-code",
                    "project": project_dir.name.replace("-Users-johnferguson-", "~/").replace("-", "/").lstrip("/"),
                    "file": str(session_file),
                    "messages": [],
                    "total_cost": 0,
                    "total_input": 0,
                    "total_output": 0,
                    "model": None,
                    "date": None,
                }
                
                with open(session_file, 'r') as f:
                    for line in f:
                        if not line.strip():
                            continue
                        
                        try:
                            entry = json.loads(line)
                            
                            # Get timestamp
                            if "timestamp" in entry:
                                ts = entry["timestamp"]
                                if isinstance(ts, str):
                                    session_data["date"] = ts[:10]
                                elif isinstance(ts, (int, float)):
                                    dt = datetime.fromtimestamp(ts / 1000)
                                    session_data["date"] = dt.strftime("%Y-%m-%d")
                            
                            # Parse usage from assistant messages (Claude Code format)
                            if entry.get("type") == "assistant" and "message" in entry:
                                msg = entry["message"]
                                usage = msg.get("usage", {})
                                model = msg.get("model", "claude-sonnet-4")
                                
                                if usage:
                                    # Claude Code uses: input_tokens, output_tokens, cache_read_input_tokens
                                    input_tokens = usage.get("input_tokens", 0) or 0
                                    cache_read = usage.get("cache_read_input_tokens", 0) or 0
                                    output_tokens = usage.get("output_tokens", 0) or 0
                                    cache_creation = usage.get("cache_creation_input_tokens", 0) or 0
                                    
                                    # Total input includes cache reads
                                    total_input = input_tokens + cache_read
                                    
                                    # Build usage dict for cost calculation
                                    cost_usage = {
                                        "input": total_input,
                                        "output": output_tokens,
                                    }
                                    cost = calculate_cost(cost_usage, model)
                                    
                                    session_data["model"] = model
                                    
                                    msg_data = {
                                        "timestamp": entry.get("timestamp"),
                                        "input": total_input,
                                        "output": output_tokens,
                                        "cache_read": cache_read,
                                        "cache_creation": cache_creation,
                                        "cost": cost,
                                        "model": model,
                                    }
                                    session_data["messages"].append(msg_data)
                                    session_data["total_cost"] += cost
                                    session_data["total_input"] += total_input
                                    session_data["total_output"] += output_tokens
                        except json.JSONDecodeError:
                            continue
                
                if session_data["messages"]:
                    sessions.append(session_data)
            except Exception as e:
                print(f"Error reading {session_file}: {e}", file=sys.stderr)
    
    return sessions


def parse_opencode_sessions():
    """Parse OpenCode sessions from SQLite database"""
    sessions = []
    db_path = OPENCODE_DATA_DIR / "opencode.db"
    
    if not db_path.exists():
        return sessions
    
    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all sessions that have messages
        cursor.execute("""
            SELECT DISTINCT m.session_id, s.directory, s.time_created
            FROM message m
            LEFT JOIN session s ON m.session_id = s.id
            WHERE json_extract(m.data, '$.tokens') IS NOT NULL
            ORDER BY s.time_created DESC
        """)
        
        sessions_data = cursor.fetchall()
        
        for row in sessions_data:
            session_data = {
                "source": "opencode",
                "file": str(db_path),
                "project": Path(row["directory"]).name if row["directory"] else "unknown",
                "messages": [],
                "total_cost": 0,
                "total_input": 0,
                "total_output": 0,
                "model": None,
                "date": None,
                "session_id": row["session_id"],
            }
            
            # Convert timestamp to date
            if row["time_created"]:
                dt = datetime.fromtimestamp(row["time_created"] / 1000)
                session_data["date"] = dt.strftime("%Y-%m-%d")
            
            # Get all messages for this session with usage data
            cursor2 = conn.cursor()
            cursor2.execute("""
                SELECT id, data, time_created
                FROM message
                WHERE session_id = ?
                AND json_extract(data, '$.tokens') IS NOT NULL
                ORDER BY time_created
            """, (row["session_id"],))
            
            for msg_row in cursor2.fetchall():
                try:
                    data = json.loads(msg_row["data"])
                    
                    # OpenCode stores tokens in the message data
                    tokens = data.get("tokens", {})
                    model_id = data.get("modelID", "unknown")
                    cost = data.get("cost", 0) or 0
                    
                    if tokens:
                        input_tokens = tokens.get("input", 0) or 0
                        output_tokens = tokens.get("output", 0) or 0
                        cache_read = tokens.get("cache", {}).get("read", 0) or 0
                        cache_write = tokens.get("cache", {}).get("write", 0) or 0
                        
                        total_input = input_tokens + cache_read
                        
                        # If cost not provided, calculate it
                        if cost == 0:
                            cost_usage = {"input": total_input, "output": output_tokens}
                            cost = calculate_cost(cost_usage, model_id)
                        
                        # Track model
                        if not session_data["model"]:
                            session_data["model"] = model_id
                        
                        msg_data = {
                            "timestamp": msg_row["time_created"],
                            "input": total_input,
                            "output": output_tokens,
                            "cache_read": cache_read,
                            "cache_write": cache_write,
                            "cost": cost,
                            "model": model_id,
                        }
                        
                        session_data["messages"].append(msg_data)
                        session_data["total_cost"] += cost
                        session_data["total_input"] += total_input
                        session_data["total_output"] += output_tokens
                except (json.JSONDecodeError, KeyError) as e:
                    continue
            
            if session_data["messages"]:
                sessions.append(session_data)
        
        conn.close()
    except Exception as e:
        print(f"Error reading OpenCode database: {e}", file=sys.stderr)
    
    return sessions


def parse_codex_sessions():
    """Parse Codex session files"""
    sessions = []
    sessions_dir = CODEX_DIR / "sessions"
    
    if not sessions_dir.exists():
        return sessions
    
    for session_file in sessions_dir.glob("*.jsonl"):
        try:
            session_data = {
                "source": "codex",
                "file": str(session_file),
                "messages": [],
                "total_cost": 0,
                "total_input": 0,
                "total_output": 0,
                "model": None,
                "date": None,
            }
            
            with open(session_file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    
                    try:
                        entry = json.loads(line)
                        
                        if "timestamp" in entry:
                            ts = entry["timestamp"]
                            if isinstance(ts, str):
                                session_data["date"] = ts[:10]
                            elif isinstance(ts, (int, float)):
                                dt = datetime.fromtimestamp(ts / 1000)
                                session_data["date"] = dt.strftime("%Y-%m-%d")
                        
                        # Extract usage from responses
                        if entry.get("type") == "response" and "usage" in entry:
                            usage = entry["usage"]
                            model = entry.get("model", "gpt-4o")
                            session_data["model"] = model
                            cost = calculate_cost(usage, model)
                            
                            msg_data = {
                                "timestamp": entry.get("timestamp"),
                                "input": usage.get("input_tokens", usage.get("prompt_tokens", 0)) or 0,
                                "output": usage.get("output_tokens", usage.get("completion_tokens", 0)) or 0,
                                "cache_read": 0,
                                "cost": cost,
                                "model": model,
                            }
                            session_data["messages"].append(msg_data)
                            session_data["total_cost"] += cost
                            session_data["total_input"] += msg_data["input"]
                            session_data["total_output"] += msg_data["output"]
                    except json.JSONDecodeError:
                        continue
            
            if session_data["messages"]:
                sessions.append(session_data)
        except Exception as e:
            print(f"Error reading {session_file}: {e}", file=sys.stderr)
    
    return sessions


def aggregate_by_day(sessions):
    """Aggregate sessions by day"""
    daily = defaultdict(lambda: {
        "cost": 0,
        "input": 0,
        "output": 0,
        "messages": 0,
        "sources": defaultdict(int),
        "models": defaultdict(int),
    })
    
    for session in sessions:
        date = session.get("date")
        if not date:
            continue
        
        day = daily[date]
        day["cost"] += session["total_cost"]
        day["input"] += session["total_input"]
        day["output"] += session["total_output"]
        day["messages"] += len(session["messages"])
        day["sources"][session["source"]] += 1
        
        # Track all models used in this session
        for msg in session.get("messages", []):
            model = msg.get("model")
            if model:
                day["models"][model] += 1
    
    return dict(daily)


def aggregate_by_model(sessions):
    """Aggregate by model across all sessions"""
    by_model = defaultdict(lambda: {
        "cost": 0,
        "input": 0,
        "output": 0,
        "messages": 0,
        "sources": set(),
    })
    
    for session in sessions:
        for msg in session.get("messages", []):
            model = msg.get("model", "unknown")
            by_model[model]["cost"] += msg.get("cost", 0)
            by_model[model]["input"] += msg.get("input", 0)
            by_model[model]["output"] += msg.get("output", 0)
            by_model[model]["messages"] += 1
            by_model[model]["sources"].add(session.get("source", "unknown"))
    
    # Convert sets to strings for JSON serialization
    for model in by_model:
        by_model[model]["sources"] = list(by_model[model]["sources"])
    
    return dict(by_model)


def print_report(sessions, daily, days=7):
    """Print cost visibility report"""
    print("💰 **Cost Tracker - TailClaude for All Harnesses**\n")
    
    # Overall stats
    total_cost = sum(s["total_cost"] for s in sessions)
    total_input = sum(s["total_input"] for s in sessions)
    total_output = sum(s["total_output"] for s in sessions)
    total_messages = sum(len(s["messages"]) for s in sessions)
    
    print(f"📊 **All Time**")
    print(f"  Cost: **${total_cost:.4f}**")
    print(f"  Tokens: {total_input:,} in / {total_output:,} out")
    print(f"  Messages: {total_messages}")
    print()
    
    # By source
    by_source = defaultdict(lambda: {"cost": 0, "input": 0, "output": 0, "messages": 0})
    for session in sessions:
        source = session["source"]
        by_source[source]["cost"] += session["total_cost"]
        by_source[source]["input"] += session["total_input"]
        by_source[source]["output"] += session["total_output"]
        by_source[source]["messages"] += len(session["messages"])
    
    print("📁 **By Source**")
    for source, stats in sorted(by_source.items(), key=lambda x: x[1]["cost"], reverse=True):
        print(f"  **{source}**: ${stats['cost']:.4f} ({stats['messages']} msgs)")
    print()
    
    # By model
    by_model = aggregate_by_model(sessions)
    print("🤖 **By Model**")
    for model, stats in sorted(by_model.items(), key=lambda x: x[1]["cost"], reverse=True)[:10]:
        sources_str = ", ".join(stats["sources"])
        print(f"  **{model}**: ${stats['cost']:.4f} ({stats['messages']} msgs) [{sources_str}]");
    print()
    
    # Daily trend
    today = datetime.now().date()
    print(f"📈 **{days}-Day Trend**\n")
    print("| Date | Cost | Tokens | Messages | Sources |")
    print("|------|------|--------|----------|---------|")
    
    for i in range(days - 1, -1, -1):
        date = (today - timedelta(days=i)).isoformat()
        if date in daily:
            day = daily[date]
            cost_str = f"${day['cost']:.4f}" if day['cost'] >= 0.01 else f"${day['cost']:.6f}"
            tokens = f"{day['input']:,}/{day['output']:,}"
            sources = ", ".join(day['sources'].keys())
            print(f"| {date} | {cost_str} | {tokens} | {day['messages']} | {sources} |")
        else:
            print(f"| {date} | $0 | 0/0 | 0 | - |")
    
    print()
    
    # Recent sessions
    print("📋 **Recent Sessions**\n")
    recent = sorted(sessions, key=lambda s: s.get("date") or "", reverse=True)[:10]
    
    for session in recent:
        source = session["source"]
        cost = session["total_cost"]
        msgs = len(session["messages"])
        date = session.get("date", "unknown")
        project = session.get("project", "")
        
        # Get all unique models from this session
        models = set()
        for msg in session.get("messages", []):
            if msg.get("model"):
                models.add(msg["model"])
        models_str = ", ".join(sorted(models)) if models else "unknown"
        
        cost_str = f"${cost:.4f}" if cost >= 0.01 else f"${cost:.6f}"
        proj_str = f" ({project})" if project else ""
        
        print(f"  • **{date}** [{source}{proj_str}]")
        print(f"    {models_str}: {cost_str} ({msgs} msgs)")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Cost visibility for OpenClaw + ACP harnesses")
    parser.add_argument("--days", type=int, default=7, help="Days to show in trend")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--source", choices=["openclaw", "claude-code", "codex", "opencode"], help="Filter by source")
    args = parser.parse_args()
    
    # Parse all sessions
    sessions = []
    
    if not args.source or args.source == "openclaw":
        sessions.extend(parse_openclaw_sessions())
    
    if not args.source or args.source == "claude-code":
        sessions.extend(parse_claude_code_sessions())
    
    if not args.source or args.source == "codex":
        sessions.extend(parse_codex_sessions())
    
    if not args.source or args.source == "opencode":
        sessions.extend(parse_opencode_sessions())
    
    # Aggregate by day
    daily = aggregate_by_day(sessions)
    
    if args.json:
        output = {
            "sessions": sessions,
            "daily": daily,
            "by_model": aggregate_by_model(sessions),
            "total_cost": sum(s["total_cost"] for s in sessions),
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(sessions, daily, days=args.days)
    
    # Save to file
    report_path = WORKSPACE / "reports" / "cost-tracker.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "sessions": sessions,
            "daily": daily,
            "by_model": aggregate_by_model(sessions),
        }, f, indent=2)
    
    print(f"\n📁 Full report saved to: reports/cost-tracker.json")


if __name__ == "__main__":
    main()
