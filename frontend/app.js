const form = document.getElementById("analyze-form");
const graphTitle = document.getElementById("graph-title");
const graphModeHint = document.getElementById("graph-mode-hint");
const graphSummary = document.getElementById("graph-summary");
const graphSvg = document.getElementById("graph");
const detailEmpty = document.getElementById("detail-empty");
const detailContent = document.getElementById("detail-content");
const llmCheckbox = document.getElementById("with-llm");
const expandButton = document.getElementById("expand-node");
const jumpButton = document.getElementById("jump-node");
const overviewFile = document.getElementById("overview-file");
const overviewNote = document.getElementById("overview-note");
const metricNodes = document.getElementById("metric-nodes");
const metricEdges = document.getElementById("metric-edges");
const metricUnresolved = document.getElementById("metric-unresolved");
const readingAnchors = document.getElementById("reading-anchors");
const filterChips = Array.from(document.querySelectorAll(".filter-chip"));

const FILTER_LABELS = {
  all: "全部节点",
  focus: "主干优先",
  confirmed: "仅看已确认",
};

const STATUS_LABELS = {
  resolved: "已确认",
  ambiguous: "有歧义",
  unresolved: "未解析",
};

const UI_COPY = {
  emptyAnchors: "分析后会在这里给出优先节点。",
  emptyGraphTitle: "当前过滤条件下没有可显示的节点",
  emptyGraphSubtitle: "可以切回“全部”或“主干优先”，再继续阅读。",
};

let currentGraph = null;
let selectedNodeId = null;
let selectedSymbol = null;
let currentFilter = "all";

hydrateInputsFromQuery();
bindEvents();

function hydrateInputsFromQuery() {
  const params = new URLSearchParams(window.location.search);
  if (params.get("repo_root")) {
    document.getElementById("repo-root").value = params.get("repo_root");
  }
  if (params.get("target_file")) {
    document.getElementById("target-file").value = params.get("target_file");
  }
}

function bindEvents() {
  filterChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      currentFilter = chip.dataset.filter;
      syncFilterChips();
      if (currentGraph) {
        refreshCurrentGraph();
      }
    });
  });

  form.addEventListener("submit", handleAnalyzeSubmit);
  expandButton.addEventListener("click", handleExpandNode);
  jumpButton.addEventListener("click", handleJumpToDefinition);
}

async function handleAnalyzeSubmit(event) {
  event.preventDefault();
  const repoRoot = document.getElementById("repo-root").value;
  const targetFile = document.getElementById("target-file").value;
  const search = new URLSearchParams({ repo_root: repoRoot, target_file: targetFile });
  window.history.replaceState({}, "", `/?${search.toString()}`);
  const response = await fetch(`/api/graph?${search.toString()}`);
  currentGraph = await response.json();
  selectedNodeId = null;
  selectedSymbol = null;
  graphTitle.textContent = currentGraph.center_file;
  showEmpty();
  refreshCurrentGraph();
}

async function handleExpandNode() {
  if (!selectedNodeId) return;
  const response = await fetch(`/api/expand?symbol_id=${encodeURIComponent(selectedNodeId)}`);
  const delta = await response.json();
  mergeGraph(delta);
  refreshCurrentGraph();
}

async function handleJumpToDefinition() {
  if (!selectedSymbol || isSyntheticNode(selectedSymbol)) return;
  const repoRoot = document.getElementById("repo-root").value.replace(/[\\/]+$/, "");
  document.getElementById("target-file").value = `${repoRoot}/${selectedSymbol.file_path}`;
  form.requestSubmit();
}

function refreshCurrentGraph() {
  if (!currentGraph) return;
  const view = buildGraphView(currentGraph);
  updateOverview(currentGraph, view);
  updateGraphMeta(currentGraph, view);
  renderGraph(currentGraph, view);
}

function syncFilterChips() {
  filterChips.forEach((item) => item.classList.toggle("active", item.dataset.filter === currentFilter));
}

function mergeGraph(delta) {
  const existingNodeIds = new Set(currentGraph.nodes.map((node) => node.symbol_id));
  delta.nodes.forEach((node) => {
    if (!existingNodeIds.has(node.symbol_id)) {
      currentGraph.nodes.push(node);
    }
  });

  const existingEdgeIds = new Set(currentGraph.edges.map((edge) => edge.edge_id));
  delta.edges.forEach((edge) => {
    if (!existingEdgeIds.has(edge.edge_id)) {
      currentGraph.edges.push(edge);
    }
  });

  const unresolvedIds = new Set(currentGraph.unresolved_ids);
  delta.unresolved_ids.forEach((symbolId) => unresolvedIds.add(symbolId));
  currentGraph.unresolved_ids = Array.from(unresolvedIds);
}

async function selectNode(symbolId) {
  selectedNodeId = symbolId;
  selectedSymbol = findNodeById(symbolId);
  expandButton.disabled = false;
  jumpButton.disabled = !selectedSymbol || isSyntheticNode(selectedSymbol);
  const withLlm = llmCheckbox.checked ? "1" : "0";
  const response = await fetch(`/api/node?symbol_id=${encodeURIComponent(symbolId)}&with_llm=${withLlm}`);
  const detail = await response.json();
  renderDetail(detail);
  refreshCurrentGraph();
}

function findNodeById(symbolId) {
  return currentGraph?.nodes.find((node) => node.symbol_id === symbolId) || null;
}

function buildGraphView(graph) {
  const centerIds = new Set(graph.center_symbol_ids);
  const rankedAllNodes = rankNodes(graph.nodes, graph.edges, centerIds);
  const focusIds = new Set(rankedAllNodes.slice(0, 8).map((node) => node.symbol_id));
  centerIds.forEach((symbolId) => focusIds.add(symbolId));

  let visibleNodes = graph.nodes.slice();
  let visibleEdges = graph.edges.slice();

  if (currentFilter === "confirmed") {
    visibleEdges = visibleEdges.filter((edge) => edge.status === "resolved");
    const keepIds = collectConnectedNodeIds(visibleEdges);
    visibleNodes = visibleNodes.filter((node) => keepIds.has(node.symbol_id));
  }

  if (currentFilter === "focus") {
    visibleNodes = visibleNodes.filter((node) => focusIds.has(node.symbol_id));
    const keepIds = new Set(visibleNodes.map((node) => node.symbol_id));
    visibleEdges = visibleEdges.filter((edge) => keepIds.has(edge.caller_id) && keepIds.has(edge.callee_id));
  }

  const visibleNodeIds = new Set(visibleNodes.map((node) => node.symbol_id));
  const visibleUnresolvedCount = visibleNodes.filter((node) => node.symbol_type === "unresolved").length;
  const rankedVisibleNodes = rankNodes(visibleNodes, visibleEdges, centerIds);

  return {
    visibleNodes,
    visibleEdges,
    visibleNodeIds,
    visibleUnresolvedCount,
    centerIds,
    focusIds,
    rankedVisibleNodes,
  };
}

function collectConnectedNodeIds(edges) {
  const keepIds = new Set();
  edges.forEach((edge) => {
    keepIds.add(edge.caller_id);
    keepIds.add(edge.callee_id);
  });
  return keepIds;
}

function rankNodes(nodes, edges, centerIds) {
  const scores = new Map();
  nodes.forEach((node) => {
    scores.set(node.symbol_id, centerIds.has(node.symbol_id) ? 8 : 2);
  });

  edges.forEach((edge) => {
    if (scores.has(edge.caller_id)) {
      scores.set(edge.caller_id, (scores.get(edge.caller_id) || 0) + 2);
    }
    if (scores.has(edge.callee_id)) {
      scores.set(edge.callee_id, (scores.get(edge.callee_id) || 0) + 1);
      if (edge.status !== "resolved") {
        scores.set(edge.callee_id, (scores.get(edge.callee_id) || 0) - 1);
      }
    }
  });

  return nodes
    .slice()
    .sort((a, b) => {
      const scoreDiff = (scores.get(b.symbol_id) || 0) - (scores.get(a.symbol_id) || 0);
      if (scoreDiff !== 0) return scoreDiff;
      return a.qualname.localeCompare(b.qualname);
    });
}

function updateOverview(graph, view) {
  overviewFile.textContent = graph.center_file;
  metricNodes.textContent = String(view.visibleNodes.length);
  metricEdges.textContent = String(view.visibleEdges.length);
  metricUnresolved.textContent = String(view.visibleUnresolvedCount);
  overviewNote.textContent = buildOverviewNote(graph, view);

  const anchorNodes = view.rankedVisibleNodes.slice(0, 5);
  if (!anchorNodes.length) {
    readingAnchors.innerHTML = `<span class="anchor-empty">${UI_COPY.emptyAnchors}</span>`;
    return;
  }

  readingAnchors.innerHTML = anchorNodes
    .map(
      (node, index) => `
        <button class="anchor-chip" type="button" data-symbol-id="${escapeHtml(node.symbol_id)}">
          <span class="anchor-rank">${index + 1}</span>
          <span>${escapeHtml(shortNodeLabel(node))}</span>
        </button>
      `,
    )
    .join("");

  Array.from(readingAnchors.querySelectorAll(".anchor-chip")).forEach((button) => {
    button.addEventListener("click", () => selectNode(button.dataset.symbolId));
  });
}

function buildOverviewNote(graph, view) {
  const centerCount = view.visibleNodes.filter((node) => view.centerIds.has(node.symbol_id)).length;
  const externalCount = view.visibleNodes.length - centerCount;
  const anchorLabel = view.rankedVisibleNodes[0] ? shortNodeLabel(view.rankedVisibleNodes[0]) : "暂无";
  if (view.visibleNodes.length === 0) {
    return "当前过滤结果为空。可以切回“全部”或“主干优先”，重新找入口。";
  }
  if (view.visibleNodes.length > 14) {
    return `这是一个偏大的单文件视图：当前展示 ${centerCount} 个目标文件节点、${externalCount} 个支撑节点。建议先从 ${anchorLabel} 开始，再逐步展开。`;
  }
  return `当前模式是“${FILTER_LABELS[currentFilter]}”。建议从 ${anchorLabel} 起步，优先读目标文件主干，再看跨文件支撑节点。`;
}

function updateGraphMeta(graph, view) {
  const centerCount = view.visibleNodes.filter((node) => view.centerIds.has(node.symbol_id)).length;
  const noisyCount = view.visibleEdges.filter((edge) => edge.status !== "resolved").length;
  graphSummary.textContent =
    view.visibleNodes.length === 0
      ? "当前过滤条件下没有可读节点。"
      : `当前显示 ${view.visibleNodes.length} 个节点，其中 ${centerCount} 个来自目标文件；${noisyCount} 条边仍带不确定性。`;
  graphModeHint.textContent =
    view.visibleNodes.length > 10
      ? "当前是分栏阅读布局：中间优先看目标文件主干，两侧看支撑或跨文件节点。"
      : "当前是轻量分栏布局：节点较少，建议按“建议先读”顺序逐个打开。";
}

function renderGraph(graph, view) {
  graphSvg.innerHTML = "";

  const width = 1280;
  const rowHeight = 94;
  const paddingTop = 90;
  const positions = new Map();

  if (!view.visibleNodes.length) {
    renderGraphEmptyState(width);
    graphSvg.setAttribute("viewBox", `0 0 ${width} 820`);
    return;
  }

  const centerNodes = view.rankedVisibleNodes.filter((node) => view.centerIds.has(node.symbol_id));
  const supportNodes = view.rankedVisibleNodes.filter((node) => !view.centerIds.has(node.symbol_id));
  const lanes = splitSupportLanes(supportNodes);

  centerNodes.forEach((node, index) => {
    positions.set(node.symbol_id, {
      x: width * 0.5,
      y: paddingTop + index * rowHeight,
    });
  });

  lanes.left.forEach((node, index) => {
    positions.set(node.symbol_id, {
      x: width * 0.2,
      y: paddingTop + index * rowHeight,
    });
  });

  lanes.right.forEach((node, index) => {
    positions.set(node.symbol_id, {
      x: width * 0.8,
      y: paddingTop + index * rowHeight,
    });
  });

  const maxRows = Math.max(centerNodes.length, lanes.left.length, lanes.right.length, 1);
  const dynamicHeight = Math.max(820, paddingTop + maxRows * rowHeight + 120);
  graphSvg.setAttribute("viewBox", `0 0 ${width} ${dynamicHeight}`);

  renderLaneTitle("支撑节点", width * 0.2, 48);
  renderLaneTitle("目标文件主干", width * 0.5, 48);
  renderLaneTitle("跨文件节点", width * 0.8, 48);

  view.visibleEdges.forEach((edge) => renderEdge(edge, positions));
  view.visibleNodes.forEach((node) => renderNode(node, positions, view));
}

function splitSupportLanes(nodes) {
  const left = [];
  const right = [];
  nodes.forEach((node, index) => {
    if (index % 2 === 0) {
      left.push(node);
    } else {
      right.push(node);
    }
  });
  return { left, right };
}

function renderGraphEmptyState(width) {
  const title = document.createElementNS("http://www.w3.org/2000/svg", "text");
  title.setAttribute("x", width / 2);
  title.setAttribute("y", 350);
  title.setAttribute("text-anchor", "middle");
  title.setAttribute("class", "graph-empty");
  title.textContent = UI_COPY.emptyGraphTitle;
  graphSvg.appendChild(title);

  const subtitle = document.createElementNS("http://www.w3.org/2000/svg", "text");
  subtitle.setAttribute("x", width / 2);
  subtitle.setAttribute("y", 386);
  subtitle.setAttribute("text-anchor", "middle");
  subtitle.setAttribute("class", "graph-empty-subtitle");
  subtitle.textContent = UI_COPY.emptyGraphSubtitle;
  graphSvg.appendChild(subtitle);
}

function renderLaneTitle(label, x, y) {
  const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute("x", x);
  text.setAttribute("y", y);
  text.setAttribute("text-anchor", "middle");
  text.setAttribute("class", "lane-title");
  text.textContent = label;
  graphSvg.appendChild(text);
}

function renderEdge(edge, positions) {
  const from = positions.get(edge.caller_id);
  const to = positions.get(edge.callee_id);
  if (!from || !to) return;
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("d", buildEdgePath(from, to));
  path.setAttribute("class", buildEdgeClass(edge));
  graphSvg.appendChild(path);
}

function buildEdgePath(from, to) {
  const dx = Math.abs(to.x - from.x);
  const curveOffset = Math.max(56, dx * 0.3);
  return `M ${from.x} ${from.y} C ${from.x} ${from.y + curveOffset}, ${to.x} ${to.y - curveOffset}, ${to.x} ${to.y}`;
}

function buildEdgeClass(edge) {
  if (edge.status === "ambiguous") return "edge ambiguous";
  if (edge.status === "unresolved") return "edge unresolved";
  return "edge";
}

function renderNode(node, positions, view) {
  const pos = positions.get(node.symbol_id);
  if (!pos) return;

  const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
  group.setAttribute("class", buildNodeClass(node, view));
  group.addEventListener("click", () => selectNode(node.symbol_id));

  const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  rect.setAttribute("x", pos.x - 108);
  rect.setAttribute("y", pos.y - 30);
  rect.setAttribute("rx", "18");
  rect.setAttribute("ry", "18");
  rect.setAttribute("width", "216");
  rect.setAttribute("height", "60");
  group.appendChild(rect);

  const title = document.createElementNS("http://www.w3.org/2000/svg", "text");
  title.setAttribute("x", pos.x);
  title.setAttribute("y", pos.y - 3);
  title.setAttribute("text-anchor", "middle");
  title.setAttribute("class", "node-title");
  title.textContent = truncateText(shortNodeLabel(node), 22);
  group.appendChild(title);

  const subtitle = document.createElementNS("http://www.w3.org/2000/svg", "text");
  subtitle.setAttribute("x", pos.x);
  subtitle.setAttribute("y", pos.y + 17);
  subtitle.setAttribute("text-anchor", "middle");
  subtitle.setAttribute("class", "node-subtitle");
  subtitle.textContent = view.centerIds.has(node.symbol_id) ? "目标文件" : basename(node.file_path);
  group.appendChild(subtitle);

  graphSvg.appendChild(group);
}

function buildNodeClass(node, view) {
  const classes = ["node"];
  if (!view.centerIds.has(node.symbol_id)) classes.push("external");
  if (node.symbol_type === "unresolved") classes.push("unresolved");
  if (node.symbol_type === "ambiguous") classes.push("ambiguous");
  if (view.focusIds.has(node.symbol_id)) classes.push("focus");
  if (selectedNodeId === node.symbol_id) classes.push("selected");
  return classes.join(" ");
}

function renderDetail(detail) {
  detailEmpty.hidden = true;
  detailContent.hidden = false;

  const symbol = detail.symbol;
  const insight = detail.insight;
  const outboundEdges = detail.outbound_edges || [];
  const inboundEdges = detail.inbound_edges || [];
  const advisorySuggestions = detail.advisory_suggestions || [];
  const source = symbol.source || "未解析占位节点，没有源码可显示。";
  const previewSource = buildSourcePreview(source);
  const counts = {
    inbound: inboundEdges.length,
    outbound: outboundEdges.length,
    advisory: advisorySuggestions.length,
  };

  detailContent.innerHTML = `
    <div class="detail-hero">
      <div>
        <p class="eyebrow">节点详情</p>
        <h2>${escapeHtml(symbol.qualname)}</h2>
        <p class="detail-signature">${escapeHtml(symbol.signature || "无签名信息")}</p>
      </div>
      <div class="detail-badges">
        <span class="badge">${escapeHtml(symbol.symbol_type)}</span>
        <span class="badge soft">${escapeHtml(symbol.file_path)}:${symbol.start_line}-${symbol.end_line}</span>
      </div>
    </div>

    <section class="detail-summary-grid">
      <article class="summary-card">
        <span class="summary-label">调入</span>
        <strong>${counts.inbound}</strong>
      </article>
      <article class="summary-card">
        <span class="summary-label">调出</span>
        <strong>${counts.outbound}</strong>
      </article>
      <article class="summary-card">
        <span class="summary-label">建议项</span>
        <strong>${counts.advisory}</strong>
      </article>
    </section>

    <section class="detail-section">
      <h3>阅读提示</h3>
      <p>${escapeHtml(buildReadingHint(symbol, outboundEdges))}</p>
    </section>

    <section class="detail-section">
      <h3>说明</h3>
      <p>${escapeHtml(symbol.docstring || "没有 docstring，建议先看调出关系和源码前几行。")}</p>
    </section>

    <section class="detail-section">
      <h3>调入节点</h3>
      <ul class="detail-list">${renderStringList(detail.callers)}</ul>
    </section>

    <section class="detail-section">
      <h3>调出节点</h3>
      <ul class="detail-list">${renderStringList(detail.callees)}</ul>
    </section>

    <section class="detail-section">
      <h3>解析依据</h3>
      <ul class="detail-list detail-edge-list">${outboundEdges.map(renderEdgeDetail).join("") || "<li>暂无</li>"}</ul>
    </section>

    ${advisorySuggestions.length ? `
      <section class="detail-section">
        <h3>建议与不确定项</h3>
        ${advisorySuggestions.map(renderSuggestion).join("")}
      </section>
    ` : ""}

    ${insight ? renderInsight(insight) : ""}

    <section class="detail-section">
      <h3>源码预览</h3>
      <div class="source-card">
        <pre>${escapeHtml(previewSource.preview)}</pre>
        ${renderSourceToggle(previewSource.remaining)}
      </div>
    </section>
  `;

  bindSourceToggle();
}

function renderInsight(insight) {
  return `
    <section class="detail-section">
      <h3>Insight</h3>
      <p>${escapeHtml(insight.summary || "")}</p>
      <ul class="detail-list">${renderStringList(insight.responsibilities || [])}</ul>
    </section>
  `;
}

function renderSourceToggle(remainingSource) {
  if (!remainingSource) return "";
  return `
    <button class="source-toggle" type="button" data-source-toggle>展开完整源码</button>
    <pre class="source-more" hidden>${escapeHtml(remainingSource)}</pre>
  `;
}

function bindSourceToggle() {
  const sourceToggle = detailContent.querySelector("[data-source-toggle]");
  if (!sourceToggle) return;
  const extra = detailContent.querySelector(".source-more");
  sourceToggle.addEventListener("click", () => {
    const isHidden = extra.hasAttribute("hidden");
    if (isHidden) {
      extra.removeAttribute("hidden");
      sourceToggle.textContent = "收起额外源码";
    } else {
      extra.setAttribute("hidden", "");
      sourceToggle.textContent = "展开完整源码";
    }
  });
}

function showEmpty() {
  detailEmpty.hidden = false;
  detailContent.hidden = true;
  detailContent.innerHTML = "";
  expandButton.disabled = true;
  jumpButton.disabled = true;
}

function renderStringList(items) {
  if (!items || !items.length) {
    return "<li>暂无</li>";
  }
  return items.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
}

function renderEdgeDetail(edge) {
  const statusLabel = STATUS_LABELS[edge.status] || edge.status;
  return `
    <li>
      <strong>${escapeHtml(edge.call_expr || "未知调用")}</strong>
      <span class="edge-note">${statusLabel} · ${escapeHtml(edge.reason || "无原因说明")}</span>
    </li>
  `;
}

function renderSuggestion(item) {
  const title = item.edge_status === "ambiguous" ? "存在多个可能目标" : "暂时无法静态确认";
  return `
    <div class="detail-callout ${escapeHtml(item.edge_status || "unresolved")}">
      <strong>${escapeHtml(item.call_expr || "未知调用")}</strong>
      <p>${escapeHtml(title)}</p>
      <p>${escapeHtml(item.summary || "暂无补充说明。")}</p>
      <p>原因：${escapeHtml(item.reason || "未提供")}</p>
      ${item.candidate_symbol_ids && item.candidate_symbol_ids.length
        ? `<p>候选目标：${item.candidate_symbol_ids.map((value) => escapeHtml(value)).join("、")}</p>`
        : ""}
    </div>
  `;
}

function buildReadingHint(symbol, outboundEdges) {
  if (symbol.symbol_type === "unresolved" || symbol.symbol_type === "ambiguous") {
    return "这个节点本身是不确定项，优先回到它的调用方，看上下文是否能帮助你判断。";
  }
  if (outboundEdges.length === 0) {
    return "这是一个叶子节点，适合在主干看完之后再确认细节。";
  }
  const unresolvedCount = outboundEdges.filter((edge) => edge.status !== "resolved").length;
  if (unresolvedCount > 0) {
    return `这个节点会继续调用 ${outboundEdges.length} 个下游，其中 ${unresolvedCount} 个还不确定，建议先看已确认边，再处理不确定项。`;
  }
  return `这个节点会继续调用 ${outboundEdges.length} 个下游，适合作为主干阅读中的下一跳。`;
}

function buildSourcePreview(source) {
  const lines = source.split("\n");
  if (lines.length <= 14) {
    return { preview: source, remaining: "" };
  }
  return {
    preview: lines.slice(0, 14).join("\n"),
    remaining: lines.slice(14).join("\n"),
  };
}

function shortNodeLabel(node) {
  const parts = String(node.qualname || "").split("::");
  return parts[parts.length - 1] || node.symbol_id;
}

function basename(filePath) {
  return String(filePath || "").split("/").slice(-1)[0] || "外部节点";
}

function isSyntheticNode(symbol) {
  return symbol.symbol_type === "unresolved" || symbol.symbol_type === "ambiguous";
}

function truncateText(value, maxChars) {
  return value.length > maxChars ? `${value.slice(0, maxChars - 1)}…` : value;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}
