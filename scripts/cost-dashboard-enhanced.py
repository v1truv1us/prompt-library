#!/usr/bin/env python3
"""
Cost Dashboard Enhanced - Interactive dashboard with insights
"""

import json
import http.server
import socketserver
import subprocess
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
from collections import defaultdict

WORKSPACE = Path(__file__).parent.parent
SCRIPTS_DIR = WORKSPACE / "scripts"
REPORTS_DIR = WORKSPACE / "reports"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cost Tracker Dashboard - Insights</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container { max-width: 1500px; margin: 0 auto; }
        
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        header h1 {
            font-size: 2.2rem;
            background: linear-gradient(90deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        
        header p { color: #888; font-size: 1rem; }
        
        .filters {
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 20px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .filter-group {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .filter-group label {
            font-size: 0.85rem;
            color: #888;
        }
        
        select, input[type="date"] {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 6px;
            padding: 8px 12px;
            color: #e0e0e0;
            font-size: 0.9rem;
        }
        
        select:focus, input:focus {
            outline: none;
            border-color: #7c3aed;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .stat-card h3 {
            font-size: 0.8rem;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }
        
        .stat-card .value {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(90deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-card .change {
            font-size: 0.85rem;
            margin-top: 4px;
        }
        
        .change.up { color: #ef4444; }
        .change.down { color: #10b981; }
        .change.neutral { color: #888; }
        
        /* Insights Section */
        .insights-section {
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .insights-section h2 {
            font-size: 1.3rem;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .insights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
        }
        
        .insight-card {
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            padding: 16px;
            border-left: 3px solid;
        }
        
        .insight-card.achievement { border-color: #10b981; }
        .insight-card.warning { border-color: #f59e0b; }
        .insight-card.info { border-color: #00d4ff; }
        .insight-card.tip { border-color: #8b5cf6; }
        
        .insight-card h4 {
            font-size: 0.95rem;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .insight-card p {
            font-size: 0.85rem;
            color: #aaa;
            line-height: 1.5;
        }
        
        .insight-card .metric {
            font-size: 1.5rem;
            font-weight: 700;
            color: #e0e0e0;
            margin-top: 8px;
        }
        
        /* Charts */
        .charts-row {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }
        
        @media (max-width: 900px) {
            .charts-row { grid-template-columns: 1fr; }
        }
        
        .chart-card {
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .chart-card h3 {
            font-size: 1rem;
            margin-bottom: 16px;
            color: #e0e0e0;
        }
        
        .chart-container {
            position: relative;
            height: 250px;
        }
        
        /* Model List */
        .model-list {
            max-height: 300px;
            overflow-y: auto;
        }
        
        .model-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 12px;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.2s;
        }
        
        .model-item:hover {
            background: rgba(255,255,255,0.08);
        }
        
        .model-item.active {
            background: rgba(124, 58, 237, 0.2);
            border: 1px solid rgba(124, 58, 237, 0.5);
        }
        
        .model-item .name { font-size: 0.9rem; }
        .model-item .msgs { font-size: 0.8rem; color: #666; margin-left: 8px; }
        
        .cost-high { color: #ef4444; }
        .cost-medium { color: #f59e0b; }
        .cost-low { color: #10b981; }
        .cost-free { color: #06b6d4; }
        
        /* Sessions Table */
        .sessions-section {
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .sessions-section h3 {
            font-size: 1rem;
            margin-bottom: 16px;
        }
        
        .sessions-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .sessions-table th, .sessions-table td {
            text-align: left;
            padding: 10px 12px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .sessions-table th {
            font-size: 0.8rem;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 500;
        }
        
        .sessions-table tr:hover td {
            background: rgba(255,255,255,0.03);
        }
        
        .prompt-preview {
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-size: 0.85rem;
            color: #aaa;
        }
        
        .tag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        .tag.openclaw { background: rgba(0, 212, 255, 0.2); color: #00d4ff; }
        .tag.claude-code { background: rgba(124, 58, 237, 0.2); color: #a78bfa; }
        .tag.opencode { background: rgba(249, 115, 22, 0.2); color: #fb923c; }
        .tag.codex { background: rgba(16, 185, 129, 0.2); color: #34d399; }
        
        .last-updated {
            text-align: center;
            color: #666;
            font-size: 0.85rem;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>💰 Cost Tracker + Insights</h1>
            <p>TailClaude-style visibility for all coding harnesses</p>
        </header>
        
        <div class="filters">
            <div class="filter-group">
                <label>Model:</label>
                <select id="modelFilter">
                    <option value="all">All Models</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Source:</label>
                <select id="sourceFilter">
                    <option value="all">All Sources</option>
                    <option value="claude-code">Claude Code</option>
                    <option value="opencode">OpenCode</option>
                    <option value="openclaw">OpenClaw</option>
                    <option value="codex">Codex</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Period:</label>
                <select id="periodFilter">
                    <option value="7">Last 7 days</option>
                    <option value="30">Last 30 days</option>
                    <option value="90">Last 90 days</option>
                    <option value="all">All time</option>
                </select>
            </div>
        </div>
        
        <div class="stats-grid" id="statsGrid">
            <div class="stat-card">
                <h3>Total Cost</h3>
                <div class="value" id="totalCost">$0.00</div>
                <div class="change" id="costChange">-</div>
            </div>
            <div class="stat-card">
                <h3>Messages</h3>
                <div class="value" id="totalMessages">0</div>
                <div class="change" id="msgChange">-</div>
            </div>
            <div class="stat-card">
                <h3>Avg Cost/Day</h3>
                <div class="value" id="avgDaily">$0.00</div>
                <div class="change neutral" id="avgChange">-</div>
            </div>
            <div class="stat-card">
                <h3>Cache Hit Rate</h3>
                <div class="value" id="cacheRate">0%</div>
                <div class="change neutral">Higher = better</div>
            </div>
        </div>
        
        <div class="insights-section">
            <h2>💡 Insights</h2>
            <div class="insights-grid" id="insightsGrid">
                <div class="insight-card info">
                    <h4>📊 Loading insights...</h4>
                    <p>Analyzing your usage patterns</p>
                </div>
            </div>
        </div>
        
        <div class="charts-row">
            <div class="chart-card">
                <h3>📈 Cost Trend</h3>
                <div class="chart-container">
                    <canvas id="trendChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h3>🤖 By Model</h3>
                <div class="chart-container">
                    <canvas id="modelChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="sessions-section">
            <h3>📋 Recent Sessions</h3>
            <table class="sessions-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Source</th>
                        <th>Model</th>
                        <th>Prompt Preview</th>
                        <th>Cost</th>
                        <th>Tokens</th>
                    </tr>
                </thead>
                <tbody id="sessionsBody">
                </tbody>
            </table>
        </div>
        
        <div class="last-updated" id="lastUpdated">Loading...</div>
    </div>
    
    <script>
        let rawData = null;
        let filteredData = null;
        let trendChart = null;
        let modelChart = null;
        
        async function loadData() {
            try {
                const response = await fetch('/api/data');
                if (!response.ok) throw new Error('Failed to load data');
                rawData = await response.json();
                populateFilters();
                applyFilters();
            } catch (error) {
                document.getElementById('lastUpdated').innerHTML = 
                    `<div style="color: #ef4444;">Error: ${error.message}</div>`;
            }
        }
        
        function populateFilters() {
            const models = new Set();
            rawData.sessions.forEach(s => {
                (s.messages || []).forEach(m => {
                    if (m.model) models.add(m.model);
                });
            });
            
            const select = document.getElementById('modelFilter');
            [...models].sort().forEach(model => {
                const opt = document.createElement('option');
                opt.value = model;
                opt.textContent = model;
                select.appendChild(opt);
            });
        }
        
        function applyFilters() {
            const modelFilter = document.getElementById('modelFilter').value;
            const sourceFilter = document.getElementById('sourceFilter').value;
            const periodDays = parseInt(document.getElementById('periodFilter').value);
            
            const cutoffDate = periodDays < 9999 ? 
                new Date(Date.now() - periodDays * 24 * 60 * 60 * 1000).toISOString().split('T')[0] : 
                null;
            
            filteredData = {
                sessions: rawData.sessions.filter(s => {
                    if (sourceFilter !== 'all' && s.source !== sourceFilter) return false;
                    if (cutoffDate && s.date < cutoffDate) return false;
                    if (modelFilter !== 'all') {
                        const hasModel = (s.messages || []).some(m => m.model === modelFilter);
                        if (!hasModel) return false;
                    }
                    return true;
                }),
                by_model: rawData.by_model || {}
            };
            
            updateDashboard();
        }
        
        function updateDashboard() {
            const sessions = filteredData.sessions;
            
            // Calculate stats
            let totalCost = 0, totalMessages = 0, totalInput = 0, totalOutput = 0, totalCache = 0;
            
            sessions.forEach(s => {
                totalCost += s.total_cost || 0;
                totalMessages += (s.messages || []).length;
                (s.messages || []).forEach(m => {
                    totalInput += m.input || 0;
                    totalOutput += m.output || 0;
                    totalCache += m.cache_read || 0;
                });
            });
            
            const days = new Set(sessions.map(s => s.date)).size || 1;
            const avgDaily = totalCost / days;
            const cacheRate = totalInput > 0 ? (totalCache / totalInput * 100) : 0;
            
            document.getElementById('totalCost').textContent = formatCurrency(totalCost);
            document.getElementById('totalMessages').textContent = totalMessages.toLocaleString();
            document.getElementById('avgDaily').textContent = formatCurrency(avgDaily);
            document.getElementById('cacheRate').textContent = cacheRate.toFixed(1) + '%';
            
            // Update charts
            updateCharts(sessions);
            
            // Update insights
            updateInsights(sessions, totalCost, totalMessages, avgDaily, cacheRate);
            
            // Update sessions table
            updateSessionsTable(sessions.slice(0, 20));
            
            document.getElementById('lastUpdated').textContent = 
                `Last updated: ${new Date(rawData.generated_at).toLocaleString()}`;
        }
        
        function updateCharts(sessions) {
            // Daily trend
            const byDay = {};
            sessions.forEach(s => {
                if (!byDay[s.date]) byDay[s.date] = { cost: 0, msgs: 0 };
                byDay[s.date].cost += s.total_cost || 0;
                byDay[s.date].msgs += (s.messages || []).length;
            });
            
            const sortedDays = Object.keys(byDay).sort();
            const last14Days = sortedDays.slice(-14);
            
            if (trendChart) trendChart.destroy();
            trendChart = new Chart(document.getElementById('trendChart'), {
                type: 'line',
                data: {
                    labels: last14Days,
                    datasets: [{
                        label: 'Cost ($)',
                        data: last14Days.map(d => byDay[d].cost),
                        borderColor: '#7c3aed',
                        backgroundColor: 'rgba(124, 58, 237, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#888' } },
                        x: { grid: { display: false }, ticks: { color: '#888' } }
                    }
                }
            });
            
            // By model
            const byModel = {};
            sessions.forEach(s => {
                (s.messages || []).forEach(m => {
                    if (!byModel[m.model]) byModel[m.model] = { cost: 0, msgs: 0 };
                    byModel[m.model].cost += m.cost || 0;
                    byModel[m.model].msgs += 1;
                });
            });
            
            const sortedModels = Object.entries(byModel)
                .filter(([_, s]) => s.cost > 0)
                .sort((a, b) => b[1].cost - a[1].cost)
                .slice(0, 8);
            
            if (modelChart) modelChart.destroy();
            modelChart = new Chart(document.getElementById('modelChart'), {
                type: 'bar',
                data: {
                    labels: sortedModels.map(([m, _]) => m),
                    datasets: [{
                        label: 'Cost ($)',
                        data: sortedModels.map(([_, s]) => s.cost),
                        backgroundColor: ['#7c3aed', '#00d4ff', '#10b981', '#f97316', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16'],
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#888' } },
                        y: { grid: { display: false }, ticks: { color: '#888' } }
                    }
                }
            });
        }
        
        function updateInsights(sessions, totalCost, totalMessages, avgDaily, cacheRate) {
            const insights = [];
            
            // Top model
            const byModel = {};
            sessions.forEach(s => {
                (s.messages || []).forEach(m => {
                    if (!byModel[m.model]) byModel[m.model] = { cost: 0, msgs: 0 };
                    byModel[m.model].cost += m.cost || 0;
                    byModel[m.model].msgs += 1;
                });
            });
            const topModel = Object.entries(byModel).sort((a, b) => b[1].cost - a[1].cost)[0];
            if (topModel) {
                insights.push({
                    type: 'info',
                    title: '🤖 Top Model',
                    text: `${topModel[0]} accounts for ${((topModel[1].cost / totalCost) * 100).toFixed(1)}% of your costs`,
                    metric: formatCurrency(topModel[1].cost)
                });
            }
            
            // Free tier usage
            const freeModels = Object.entries(byModel).filter(([m, s]) => s.cost === 0 && s.msgs > 10);
            if (freeModels.length > 0) {
                const freeMsgs = freeModels.reduce((sum, [_, s]) => sum + s.msgs, 0);
                insights.push({
                    type: 'achievement',
                    title: '🎯 Free Tier Usage',
                    text: `${freeModels.length} free model(s) used for ${freeMsgs.toLocaleString()} messages`,
                    metric: '$0.00'
                });
            }
            
            // Cache efficiency
            if (cacheRate > 50) {
                insights.push({
                    type: 'achievement',
                    title: '⚡ Cache Efficiency',
                    text: `Great cache hit rate! You're reusing context effectively.`,
                    metric: `${cacheRate.toFixed(1)}%`
                });
            } else if (cacheRate < 20 && totalMessages > 100) {
                insights.push({
                    type: 'tip',
                    title: '💡 Cache Tip',
                    text: 'Consider longer sessions or using CLAUDE.md files to increase cache hits.',
                    metric: `${cacheRate.toFixed(1)}%`
                });
            }
            
            // Spending trend
            const byDay = {};
            sessions.forEach(s => {
                if (s.date) {
                    if (!byDay[s.date]) byDay[s.date] = 0;
                    byDay[s.date] += s.total_cost || 0;
                }
            });
            const days = Object.keys(byDay).sort();
            if (days.length >= 7) {
                const last7 = days.slice(-7).reduce((sum, d) => sum + byDay[d], 0);
                const prev7 = days.slice(-14, -7).reduce((sum, d) => sum + byDay[d], 0);
                const change = prev7 > 0 ? ((last7 - prev7) / prev7 * 100) : 0;
                
                if (change > 20) {
                    insights.push({
                        type: 'warning',
                        title: '📈 Spending Up',
                        text: `Costs increased ${change.toFixed(0)}% compared to previous week`,
                        metric: `+${change.toFixed(0)}%`
                    });
                } else if (change < -20) {
                    insights.push({
                        type: 'achievement',
                        title: '📉 Spending Down',
                        text: `Costs decreased ${Math.abs(change).toFixed(0)}% compared to previous week`,
                        metric: `${change.toFixed(0)}%`
                    });
                }
            }
            
            // Most active project
            const byProject = {};
            sessions.forEach(s => {
                const proj = s.project || 'unknown';
                if (!byProject[proj]) byProject[proj] = { cost: 0, sessions: 0 };
                byProject[proj].cost += s.total_cost || 0;
                byProject[proj].sessions += 1;
            });
            const topProject = Object.entries(byProject).sort((a, b) => b[1].sessions - a[1].sessions)[0];
            if (topProject && topProject[1].sessions > 5) {
                insights.push({
                    type: 'info',
                    title: '📁 Most Active Project',
                    text: `${topProject[0]} - ${topProject[1].sessions} sessions`,
                    metric: formatCurrency(topProject[1].cost)
                });
            }
            
            // Cost efficiency
            const costPerMsg = totalMessages > 0 ? totalCost / totalMessages : 0;
            if (costPerMsg < 0.10) {
                insights.push({
                    type: 'achievement',
                    title: '💰 Cost Efficient',
                    text: `Average cost per message is very low`,
                    metric: `${formatCurrency(costPerMsg)}/msg`
                });
            }
            
            const grid = document.getElementById('insightsGrid');
            grid.innerHTML = insights.map(i => `
                <div class="insight-card ${i.type}">
                    <h4>${i.title}</h4>
                    <p>${i.text}</p>
                    <div class="metric">${i.metric}</div>
                </div>
            `).join('');
        }
        
        function updateSessionsTable(sessions) {
            const tbody = document.getElementById('sessionsBody');
            tbody.innerHTML = sessions.map(s => {
                const costClass = s.total_cost > 10 ? 'cost-high' : 
                                  s.total_cost > 1 ? 'cost-medium' : 
                                  s.total_cost > 0 ? 'cost-low' : 'cost-free';
                const models = [...new Set((s.messages || []).map(m => m.model).filter(Boolean))];
                const tagClass = s.source.replace('-', '');
                
                return `
                    <tr>
                        <td>${s.date || 'Unknown'}</td>
                        <td><span class="tag ${tagClass}">${s.source}</span></td>
                        <td style="font-size: 0.85em">${models[0] || 'unknown'}</td>
                        <td class="prompt-preview">${s.prompt_preview || '-'}</td>
                        <td class="${costClass}">${formatCurrency(s.total_cost)}</td>
                        <td>${formatTokens(s.total_input + s.total_output)}</td>
                    </tr>
                `;
            }).join('');
        }
        
        function formatCurrency(value) {
            if (value >= 100) return '$' + value.toFixed(2);
            if (value >= 1) return '$' + value.toFixed(3);
            if (value > 0) return '$' + value.toFixed(4);
            return '$0.00';
        }
        
        function formatTokens(value) {
            if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M';
            if (value >= 1000) return (value / 1000).toFixed(1) + 'K';
            return value.toString();
        }
        
        // Event listeners
        document.getElementById('modelFilter').addEventListener('change', applyFilters);
        document.getElementById('sourceFilter').addEventListener('change', applyFilters);
        document.getElementById('periodFilter').addEventListener('change', applyFilters);
        
        // Load on start
        loadData();
        setInterval(loadData, 5 * 60 * 1000);
    </script>
</body>
</html>
"""


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SCRIPTS_DIR), **kwargs)
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
            return
        
        elif parsed.path == "/api/data":
            self.generate_data()
            data = self.read_data()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            return
        
        elif parsed.path == "/api/insights":
            self.generate_data()
            data = self.read_data()
            insights = self.generate_insights(data)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(insights).encode())
            return
        
        return super().do_GET()
    
    def generate_data(self):
        """Run the cost tracker to generate fresh data"""
        try:
            subprocess.run(
                ["python3", str(SCRIPTS_DIR / "cost-tracker.py")],
                capture_output=True,
                cwd=str(WORKSPACE),
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error generating data: {e.stderr.decode()}")
    
    def read_data(self):
        """Read the generated JSON data"""
        data_path = REPORTS_DIR / "cost-tracker.json"
        if data_path.exists():
            with open(data_path) as f:
                return json.load(f)
        return {"error": "No data available", "sessions": [], "daily": {}, "by_model": {}}
    
    def generate_insights(self, data):
        """Generate insights from the data"""
        insights = []
        
        # Add more sophisticated insights here
        sessions = data.get("sessions", [])
        by_model = data.get("by_model", {})
        
        # ... insight generation logic
        
        return insights
    
    def log_message(self, format, *args):
        print(f"[Dashboard] {args[0]}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Cost Dashboard Server with Insights")
    parser.add_argument("--port", type=int, default=8765, help="Port to serve on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    args = parser.parse_args()
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("📊 Generating initial cost data...")
    subprocess.run(
        ["python3", str(SCRIPTS_DIR / "cost-tracker.py")],
        cwd=str(WORKSPACE),
        capture_output=True
    )
    
    with socketserver.TCPServer((args.host, args.port), DashboardHandler) as httpd:
        url = f"http://{args.host}:{args.port}"
        print(f"\n💰 Cost Dashboard with Insights running at {url}")
        print(f"   Press Ctrl+C to stop\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped")


if __name__ == "__main__":
    main()
