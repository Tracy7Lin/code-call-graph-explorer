const form = document.getElementById("analyze-form");
const graphTitle = document.getElementById("graph-title");
const graphSvg = document.getElementById("graph");
const detailEmpty = document.getElementById("detail-empty");
const detailContent = document.getElementById("detail-content");
const llmCheckbox = document.getElementById("with-llm");
const expandButton = document.getElementById("expand-node");
const jumpButton = document.getElementById("jump-node");

let currentGraph = null;
let selectedNodeId = null;
let selectedSymbol = null;

const params = new URLSearchParams(window.location.search);
if (params.get("repo_root")) {
  document.getElementById("repo-root").value = params.get("repo_root");
}
if (params.get("target_file")) {
  document.getElementById("target-file").value = params.get("target_file");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const repoRoot = document.getElementById("repo-root").value;
  const targetFile = document.getElementById("target-file").value;
  const search = new URLSearchParams({ repo_root: repoRoot, target_file: targetFile });
  window.history.replaceState({}, "", `/?${search.toString()}`);
  const response = await fetch(`/api/graph?${search.toString()}`);
  currentGraph = await response.json();
  selectedNodeId = null;
  selectedSymbol = null;
  expandButton.disabled = true;
  jumpButton.disabled = true;
  graphTitle.textContent = currentGraph.center_file;
  renderGraph(currentGraph);
  showEmpty();
});

expandButton.addEventListener("click", async () => {
  if (!selectedNodeId) return;
  const response = await fetch(`/api/expand?symbol_id=${encodeURIComponent(selectedNodeId)}`);
  const delta = await response.json();
  mergeGraph(delta);
  renderGraph(currentGraph);
});

jumpButton.addEventListener("click", async () => {
  if (!selectedSymbol || selectedSymbol.symbol_type === "unresolved") return;
  const repoRoot = document.getElementById("repo-root").value.replace(/[\\/]+$/, "");
  document.getElementById("target-file").value = `${repoRoot}/${selectedSymbol.file_path}`;
  form.requestSubmit();
});

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
  selectedSymbol = currentGraph.nodes.find((node) => node.symbol_id === symbolId) || null;
  expandButton.disabled = false;
  jumpButton.disabled = !selectedSymbol || selectedSymbol.symbol_type === "unresolved";
  const withLlm = llmCheckbox.checked ? "1" : "0";
  const response = await fetch(`/api/node?symbol_id=${encodeURIComponent(symbolId)}&with_llm=${withLlm}`);
  const detail = await response.json();
  renderDetail(detail);
}

function renderGraph(graph) {
  graphSvg.innerHTML = "";
  const width = 1200;
  const height = 720;
  const centerIds = new Set(graph.center_symbol_ids);
  const positions = new Map();
  const centerNodes = graph.nodes.filter((node) => centerIds.has(node.symbol_id));
  const externalNodes = graph.nodes.filter((node) => !centerIds.has(node.symbol_id));
  const ringLayouts = [
    { nodes: centerNodes, radius: 110, cx: width * 0.33, cy: height * 0.5 },
    { nodes: externalNodes, radius: 230, cx: width * 0.67, cy: height * 0.5 },
  ];

  ringLayouts.forEach(({ nodes, radius, cx, cy }) => {
    nodes.forEach((node, index) => {
      const angle = (Math.PI * 2 * index) / Math.max(nodes.length, 1);
      positions.set(node.symbol_id, {
        x: cx + Math.cos(angle) * radius,
        y: cy + Math.sin(angle) * radius,
      });
    });
  });

  graph.edges.forEach((edge) => {
    const from = positions.get(edge.caller_id);
    const to = positions.get(edge.callee_id);
    if (!from || !to) return;
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", from.x);
    line.setAttribute("y1", from.y);
    line.setAttribute("x2", to.x);
    line.setAttribute("y2", to.y);
    line.setAttribute("class", edge.resolved ? "edge" : "edge unresolved");
    graphSvg.appendChild(line);
  });

  graph.nodes.forEach((node) => {
    const pos = positions.get(node.symbol_id);
    if (!pos) return;
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
    const classes = ["node"];
    if (!centerIds.has(node.symbol_id)) classes.push("external");
    if (node.symbol_type === "unresolved") classes.push("unresolved");
    group.setAttribute("class", classes.join(" "));
    group.addEventListener("click", () => selectNode(node.symbol_id));

    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", pos.x);
    circle.setAttribute("cy", pos.y);
    circle.setAttribute("r", "38");
    group.appendChild(circle);

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", pos.x);
    text.setAttribute("y", pos.y + 5);
    text.setAttribute("text-anchor", "middle");
    text.textContent = node.qualname.split(".").slice(-1)[0];
    group.appendChild(text);

    graphSvg.appendChild(group);
  });
}

function renderDetail(detail) {
  detailEmpty.hidden = true;
  detailContent.hidden = false;
  const symbol = detail.symbol;
  const insight = detail.insight;
  detailContent.innerHTML = `
    <h2>${symbol.qualname}</h2>
    <p><strong>${symbol.signature}</strong></p>
    <p>${symbol.file_path}:${symbol.start_line}-${symbol.end_line}</p>
    <p>${symbol.docstring || "No docstring available."}</p>
    <h3>Callers</h3>
    <ul class="detail-list">${detail.callers.map((item) => `<li>${item}</li>`).join("") || "<li>None</li>"}</ul>
    <h3>Callees</h3>
    <ul class="detail-list">${detail.callees.map((item) => `<li>${item}</li>`).join("") || "<li>None</li>"}</ul>
    ${insight ? `
      <h3>Insight</h3>
      <p>${insight.summary}</p>
      <ul class="detail-list">${insight.responsibilities.map((item) => `<li>${item}</li>`).join("")}</ul>
    ` : ""}
    <h3>Source</h3>
    <pre>${escapeHtml(symbol.source || "Unresolved call placeholder")}</pre>
  `;
}

function showEmpty() {
  detailEmpty.hidden = false;
  detailContent.hidden = true;
  expandButton.disabled = true;
  jumpButton.disabled = true;
  detailContent.innerHTML = "";
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}
