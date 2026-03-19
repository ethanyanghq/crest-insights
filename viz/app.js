const state = {
  mode: "current",
  showAllLabels: false,
  filters: {
    domain: "all",
    archetype: "all",
    status: "all",
  },
  hoveredId: null,
  selectedId: null,
};

const archetypeColors = {
  control_plane: "#000000",
  integration_layer: "#222222",
  data_infrastructure: "#444444",
  workflow_automation: "#666666",
  migration_tool: "#888888",
  compliance_system: "#aaaaaa",
  domain_ai: "#cccccc",
};

const statusLabels = {
  strong_keep: "Strong Keep",
  alive: "Alive",
  faint_pulse: "Faint Pulse",
};

const svg = d3.select("#phase-space");
const rootGroup = svg.append("g");
const defs = svg.append("defs");
const plotGroup = rootGroup.append("g");
const gridGroup = plotGroup.append("g").attr("class", "grid");
const quadrantGroup = plotGroup.append("g");
const axisGroupX = plotGroup.append("g");
const axisGroupY = plotGroup.append("g");
const trajectoryGroup = plotGroup.append("g");
const ghostGroup = plotGroup.append("g");
const nodeGroup = plotGroup.append("g");
const labelGroup = plotGroup.append("g");

defs
  .append("marker")
  .attr("id", "trajectory-arrow")
  .attr("viewBox", "0 0 10 10")
  .attr("refX", 8)
  .attr("refY", 5)
  .attr("markerWidth", 5)
  .attr("markerHeight", 5)
  .attr("orient", "auto-start-reverse")
  .append("path")
  .attr("d", "M 0 0 L 10 5 L 0 10 z")
  .attr("fill", "#777");

let ideas = [];

const radiusScale = d3.scaleSqrt().domain([0, 1]).range([7, 24]);
const haloScale = d3.scaleLinear().domain([0, 1]).range([2, 10]);

bootstrap();

function bootstrap() {
  const bundledIdeas = Array.isArray(window.__SHORTLIST_ONTOLOGY__)
    ? window.__SHORTLIST_ONTOLOGY__
    : null;

  if (bundledIdeas && bundledIdeas.length) {
    initializeApp(bundledIdeas);
    return;
  }

  fetch("./data/ontology.shortlist.json")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Could not load ontology file.");
      }
      return response.json();
    })
    .then(initializeApp)
    .catch((error) => {
      document.getElementById("detail-card").innerHTML = `
        <p class="detail-kicker">Load Error</p>
        <h2 class="detail-title">Could not render the phase space.</h2>
        <p class="detail-copy">${error.message}</p>
        <p class="detail-copy">Try opening the app through <code>python3 -m http.server</code> at <code>/viz/</code>, or use the bundled local data file.</p>
      `;
    });
}

function initializeApp(data) {
  ideas = data;
  state.selectedId = ideas[0]?.id ?? null;
  buildControls();
  wireEvents();
  render();
  window.addEventListener("resize", render);
}

function wireEvents() {
  document.getElementById("mode-toggle").addEventListener("click", (event) => {
    const button = event.target.closest("button[data-mode]");
    if (!button) {
      return;
    }
    state.mode = button.dataset.mode;
    syncModeButtons();
    render();
  });

  document.getElementById("show-all-labels").addEventListener("change", (event) => {
    state.showAllLabels = event.target.checked;
    render();
  });
}

function buildControls() {
  buildFilterGroup("domain", sortByLabel(uniqueValues("domain")));
  buildFilterGroup("archetype", sortByLabel(uniqueValues("archetype")));
  buildFilterGroup("status", ["strong_keep", "alive", "faint_pulse"]);
  syncModeButtons();
}

function buildFilterGroup(key, options) {
  const host = document.getElementById(`${key}-filter`);
  const label = document.createElement("span");
  label.className = "control-label";
  label.textContent = humanize(key);
  host.appendChild(label);

  const row = document.createElement("div");
  row.className = "pill-row";
  row.dataset.filterKey = key;

  [["all", "All"], ...options.map((option) => [option, humanize(option)])].forEach(
    ([value, text]) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = value === "all" ? "pill is-active" : "pill";
      button.dataset.value = value;
      button.textContent = text;
      button.addEventListener("click", () => {
        state.filters[key] = value;
        syncFilterButtons(key);
        render();
      });
      row.appendChild(button);
    }
  );

  host.appendChild(row);
}

function render() {
  const visibleIdeas = getVisibleIdeas();
  ensureSelection(visibleIdeas);

  const { width, height, margin } = getLayout();
  svg.attr("viewBox", `0 0 ${width} ${height}`);
  rootGroup.attr("transform", `translate(${margin.left},${margin.top})`);

  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const xScale = d3.scaleLinear().domain([0, 1]).range([0, innerWidth]);
  const yScale = d3.scaleLinear().domain([0, 1]).range([innerHeight, 0]);

  drawQuadrants(innerWidth, innerHeight);
  drawAxes(xScale, yScale, innerWidth, innerHeight);
  drawTrajectories(visibleIdeas, xScale, yScale);
  drawNodes(visibleIdeas, xScale, yScale);
  drawLabels(visibleIdeas, xScale, yScale);
  renderDetailCard(visibleIdeas);
}

function getLayout() {
  const bounds = svg.node().getBoundingClientRect();
  const width = Math.max(bounds.width || 960, 760);
  const height = Math.max(bounds.height || 620, 520);
  const compact = width < 820;
  return {
    width,
    height,
    margin: {
      top: 30,
      right: compact ? 22 : 42,
      bottom: compact ? 72 : 78,
      left: compact ? 54 : 72,
    },
  };
}

function drawQuadrants(innerWidth, innerHeight) {
  quadrantGroup.selectAll("*").remove();

  quadrantGroup
    .append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", innerWidth)
    .attr("height", innerHeight)
    .attr("fill", "none")
    .attr("stroke", "#000");

  quadrantGroup
    .append("line")
    .attr("x1", innerWidth / 2)
    .attr("x2", innerWidth / 2)
    .attr("y1", 0)
    .attr("y2", innerHeight)
    .attr("stroke", "#999")
    .attr("stroke-dasharray", "6 6");

  quadrantGroup
    .append("line")
    .attr("x1", 0)
    .attr("x2", innerWidth)
    .attr("y1", innerHeight / 2)
    .attr("y2", innerHeight / 2)
    .attr("stroke", "#999")
    .attr("stroke-dasharray", "6 6");

  const quadrantLabels = [
    { text: "Lower Leverage", x: 16, y: innerHeight - 16, anchor: "start" },
    { text: "More Independent", x: innerWidth - 16, y: 24, anchor: "end" },
  ];

  quadrantGroup
    .selectAll("text.quadrant-label")
    .data(quadrantLabels)
    .join("text")
    .attr("class", "quadrant-label")
    .attr("x", (d) => d.x)
    .attr("y", (d) => d.y)
    .attr("text-anchor", (d) => d.anchor)
    .text((d) => d.text);
}

function drawAxes(xScale, yScale, innerWidth, innerHeight) {
  gridGroup
    .attr("transform", "translate(0,0)")
    .call(
      d3
        .axisLeft(yScale)
        .tickSize(-innerWidth)
        .tickFormat("")
        .ticks(5)
    );

  axisGroupX
    .attr("transform", `translate(0,${innerHeight})`)
    .call(
      d3
        .axisBottom(xScale)
        .ticks(5)
        .tickFormat((d) => d3.format(".1f")(d))
    );

  axisGroupY.call(
    d3
      .axisLeft(yScale)
      .ticks(5)
      .tickFormat((d) => d3.format(".1f")(d))
  );

  axisGroupX.selectAll(".axis-title, .axis-subtitle").remove();
  axisGroupY.selectAll(".axis-title, .axis-subtitle").remove();

  axisGroupX
    .append("text")
    .attr("class", "axis-title")
    .attr("x", innerWidth / 2)
    .attr("y", 54)
    .attr("text-anchor", "middle")
    .text("Product Leverage");

  axisGroupX
    .append("text")
    .attr("class", "axis-subtitle")
    .attr("x", innerWidth / 2)
    .attr("y", 68)
    .attr("text-anchor", "middle")
    .text("services-heavy → standalone");

  axisGroupY
    .append("text")
    .attr("class", "axis-title")
    .attr("x", -innerHeight / 2)
    .attr("y", -50)
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("Independence");

  axisGroupY
    .append("text")
    .attr("class", "axis-subtitle")
    .attr("x", -innerHeight / 2)
    .attr("y", -68)
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("platform-dependent → durable");
}

function drawTrajectories(visibleIdeas, xScale, yScale) {
  const showTrajectories = state.mode === "current";
  const transition = d3.transition().duration(650).ease(d3.easeCubicOut);

  const trajectories = trajectoryGroup
    .selectAll("line.trajectory")
    .data(showTrajectories ? visibleIdeas : [], (d) => d.id)
    .join(
      (enter) =>
        enter
          .append("line")
          .attr("class", "trajectory")
          .attr("marker-end", "url(#trajectory-arrow)")
          .attr("x1", (d) => xScale(d.current.product_leverage))
          .attr("y1", (d) => yScale(d.current.independence))
          .attr("x2", (d) => xScale(d.current.product_leverage))
          .attr("y2", (d) => yScale(d.current.independence))
          .call((enterSelection) =>
            enterSelection.transition(transition)
              .attr("x2", (d) => xScale(d.reframed.product_leverage))
              .attr("y2", (d) => yScale(d.reframed.independence))
          ),
      (update) => update.call((updateSelection) =>
        updateSelection.transition(transition)
          .attr("x1", (d) => xScale(d.current.product_leverage))
          .attr("y1", (d) => yScale(d.current.independence))
          .attr("x2", (d) => xScale(d.reframed.product_leverage))
          .attr("y2", (d) => yScale(d.reframed.independence))
      ),
      (exit) => exit.transition(transition).style("opacity", 0).remove()
    );

  trajectories.style("opacity", (d) => {
    const improvement = distance(
      d.current.product_leverage,
      d.current.independence,
      d.reframed.product_leverage,
      d.reframed.independence
    );
    return 0.28 + improvement * 0.9;
  });

  ghostGroup
    .selectAll("circle.ghost")
    .data(showTrajectories ? visibleIdeas : [], (d) => d.id)
    .join(
      (enter) =>
        enter
          .append("circle")
          .attr("class", "ghost")
          .attr("cx", (d) => xScale(d.reframed.product_leverage))
          .attr("cy", (d) => yScale(d.reframed.independence))
          .attr("r", 0)
          .call((enterSelection) =>
            enterSelection.transition(transition).attr("r", (d) => radiusScale(d.current.upside) + 4)
          ),
      (update) => update.call((updateSelection) =>
        updateSelection.transition(transition)
          .attr("cx", (d) => xScale(d.reframed.product_leverage))
          .attr("cy", (d) => yScale(d.reframed.independence))
          .attr("r", (d) => radiusScale(d.current.upside) + 4)
      ),
      (exit) => exit.transition(transition).attr("r", 0).remove()
    );
}

function drawNodes(visibleIdeas, xScale, yScale) {
  const transition = d3.transition().duration(650).ease(d3.easeCubicOut);

  const nodes = nodeGroup
    .selectAll("g.node")
    .data(visibleIdeas, (d) => d.id)
    .join((enter) => {
      const g = enter
        .append("g")
        .attr("class", "node")
        .attr("transform", (d) => translateForIdea(d, xScale, yScale, "current"));

      g.append("circle").attr("class", "halo");
      g.append("circle").attr("class", "core");
      return g;
    });

  nodes
    .on("mouseenter", (_, d) => {
      state.hoveredId = d.id;
      render();
    })
    .on("mouseleave", () => {
      state.hoveredId = null;
      render();
    })
    .on("click", (_, d) => {
      state.selectedId = d.id;
      render();
    });

  nodes
    .classed("is-highlighted", (d) => d.id === state.hoveredId)
    .classed("is-selected", (d) => d.id === state.selectedId)
    .classed("is-dimmed", (d) => isDimmed(d.id));

  nodes
    .transition(transition)
    .attr("transform", (d) => translateForIdea(d, xScale, yScale, state.mode));

  nodes
    .select("circle.halo")
    .transition(transition)
    .attr("r", (d) => radiusScale(d.current.upside) + haloScale(d.current.adjacency))
    .attr("stroke", (d) => archetypeColors[d.archetype])
    .attr("stroke-width", (d) => haloScale(d.current.adjacency))
    .attr("stroke-opacity", (d) => 0.12 + d.current.adjacency * 0.38);

  nodes
    .select("circle.core")
    .transition(transition)
    .attr("r", (d) => radiusScale(d.current.upside))
    .attr("fill", (d) => archetypeColors[d.archetype]);
}

function drawLabels(visibleIdeas, xScale, yScale) {
  const labels = visibleIdeas.filter(shouldLabel);
  const transition = d3.transition().duration(650).ease(d3.easeCubicOut);

  labelGroup
    .selectAll("text.label")
    .data(labels, (d) => d.id)
    .join(
      (enter) =>
        enter
          .append("text")
          .attr("class", "label")
          .attr("x", (d) => xScale(positionForIdea(d, "current").x))
          .attr("y", (d) => yScale(positionForIdea(d, "current").y) - radiusScale(d.current.upside) - 12)
          .attr("text-anchor", "middle")
          .style("opacity", 0)
          .text((d) => d.label)
          .call((enterSelection) =>
            enterSelection.transition(transition)
              .style("opacity", 1)
              .attr("x", (d) => xScale(positionForIdea(d, state.mode).x))
              .attr("y", (d) => yScale(positionForIdea(d, state.mode).y) - radiusScale(d.current.upside) - 12)
          ),
      (update) =>
        update.call((updateSelection) =>
          updateSelection.transition(transition)
            .style("opacity", 1)
            .attr("x", (d) => xScale(positionForIdea(d, state.mode).x))
            .attr("y", (d) => yScale(positionForIdea(d, state.mode).y) - radiusScale(d.current.upside) - 12)
        ),
      (exit) => exit.transition(transition).style("opacity", 0).remove()
    );
}

function renderDetailCard(visibleIdeas) {
  const card = document.getElementById("detail-card");
  const idea = activeIdea(visibleIdeas);

  if (!idea) {
    card.innerHTML = `
      <p class="detail-kicker">No Match</p>
      <h2 class="detail-title">No ideas match the current filters.</h2>
      <p class="empty-state">Relax one of the filters to bring ideas back into the phase space.</p>
    `;
    return;
  }

  const sourcePath = firstSourcePath(idea.sources);
  const currentPoint = `${idea.current.product_leverage.toFixed(2)}, ${idea.current.independence.toFixed(2)}`;
  const reframedPoint = `${idea.reframed.product_leverage.toFixed(2)}, ${idea.reframed.independence.toFixed(2)}`;

  card.innerHTML = `
    <p class="detail-kicker">${humanize(idea.domain)} · ${humanize(idea.archetype)}</p>
    <h2 class="detail-title">${idea.label}</h2>
    <div class="status-pill status-${idea.status}">${statusLabels[idea.status]}</div>
    <p class="detail-copy"><strong>Hidden wedge:</strong> ${idea.hidden_wedge}</p>
    <p class="detail-copy"><strong>Reason alive:</strong> ${idea.reason_alive}</p>

    <section class="detail-section">
      <h3>Read</h3>
      <p class="detail-row"><strong>Buyer</strong>: ${idea.buyer}</p>
      <p class="detail-row"><strong>Option</strong>: ${humanize(idea.option_value)}</p>
      <p class="detail-row"><strong>Current</strong>: ${currentPoint}</p>
      <p class="detail-row"><strong>Reframed</strong>: ${reframedPoint}</p>
    </section>

    <section class="detail-section">
      <h3>Source</h3>
      <p class="detail-row"><a class="detail-link" href="../${sourcePath}" target="_blank" rel="noreferrer">${sourcePath}</a></p>
    </section>
  `;
}

function activeIdea(visibleIdeas) {
  return (
    visibleIdeas.find((idea) => idea.id === state.hoveredId) ||
    visibleIdeas.find((idea) => idea.id === state.selectedId) ||
    visibleIdeas[0] ||
    null
  );
}

function ensureSelection(visibleIdeas) {
  if (!visibleIdeas.some((idea) => idea.id === state.selectedId)) {
    state.selectedId = visibleIdeas[0]?.id ?? null;
  }
  if (!visibleIdeas.some((idea) => idea.id === state.hoveredId)) {
    state.hoveredId = null;
  }
}

function shouldLabel(idea) {
  if (state.showAllLabels) {
    return true;
  }

  const visibleCount = getVisibleIdeas().length;
  if (visibleCount <= 8) {
    return true;
  }

  return idea.id === state.hoveredId || idea.id === state.selectedId;
}

function isDimmed(ideaId) {
  if (!state.hoveredId) {
    return false;
  }
  return ideaId !== state.hoveredId && ideaId !== state.selectedId;
}

function getVisibleIdeas() {
  return ideas.filter((idea) =>
    Object.entries(state.filters).every(
      ([key, value]) => value === "all" || idea[key] === value
    )
  );
}

function positionForIdea(idea, mode) {
  if (mode === "reframed") {
    return {
      x: idea.reframed.product_leverage,
      y: idea.reframed.independence,
    };
  }
  return {
    x: idea.current.product_leverage,
    y: idea.current.independence,
  };
}

function translateForIdea(idea, xScale, yScale, mode) {
  const point = positionForIdea(idea, mode);
  return `translate(${xScale(point.x)},${yScale(point.y)})`;
}

function reframingGain(idea) {
  return distance(
    idea.current.product_leverage,
    idea.current.independence,
    idea.reframed.product_leverage,
    idea.reframed.independence
  );
}

function distance(x1, y1, x2, y2) {
  return Math.hypot(x2 - x1, y2 - y1);
}

function uniqueValues(key) {
  return [...new Set(ideas.map((idea) => idea[key]))];
}

function sortByLabel(values) {
  return [...values].sort((a, b) => humanize(a).localeCompare(humanize(b)));
}

function humanize(value) {
  return String(value)
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function firstSourcePath(sourceMap) {
  const values = Object.values(sourceMap || {});
  return values[0] || "";
}

function syncModeButtons() {
  document.querySelectorAll("#mode-toggle button").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.mode === state.mode);
  });
}

function syncFilterButtons(key) {
  document
    .querySelectorAll(`#${key}-filter [data-value]`)
    .forEach((button) => button.classList.toggle("is-active", button.dataset.value === state.filters[key]));
}
