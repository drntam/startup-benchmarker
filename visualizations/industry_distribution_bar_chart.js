// Configuration and dimensions
const margin = { top: 60, right: 40, bottom: 100, left: 80 };
const width = 1000 - margin.left - margin.right;
const height = 600 - margin.top - margin.bottom;

// State management
let currentData = [];
let selectedBar = null;
let sortMode = 'descending'; // 'descending' (high to low) or 'ascending' (low to high)

// Create SVG container
const svg = d3.select("#chart-container")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Create tooltip
const tooltip = d3.select("body")
    .append("div")
    .attr("class", "chart-tooltip")
    .style("opacity", 0);

// Create scales
const xScale = d3.scaleBand()
    .range([0, width])
    .padding(0.2);

const yScale = d3.scaleLinear()
    .range([height, 0]);

// Color scale for industries (vibrant colors)
const colorScale = d3.scaleOrdinal()
    .range(['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#FFD93D', '#A29BFE', '#74B9FF', '#FD79A8', '#FDCB6E']);

// Create axes
const xAxis = d3.axisBottom(xScale);
const yAxis = d3.axisLeft(yScale);

// Add X axis
const xAxisGroup = svg.append("g")
    .attr("class", "x-axis")
    .attr("transform", `translate(0,${height})`);

// Add Y axis
const yAxisGroup = svg.append("g")
    .attr("class", "y-axis");

// Add chart title
svg.append("text")
    .attr("class", "chart-title")
    .attr("x", width / 2)
    .attr("y", -30)
    .attr("text-anchor", "middle")
    .text("Industry Distribution of SaaS Startups");

// Add Y axis label
svg.append("text")
    .attr("class", "axis-label")
    .attr("transform", "rotate(-90)")
    .attr("x", -height / 2)
    .attr("y", -60)
    .attr("text-anchor", "middle")
    .text("Number of Startups");

// Load and process data
d3.csv("data/saas_financial_market_dataset_with_country.csv").then(data => {
    // Group by industry and count
    const industryCounts = d3.rollup(
        data,
        v => v.length,
        d => d.Industry
    );

    // Convert to array format
    currentData = Array.from(industryCounts, ([industry, count]) => ({
        industry,
        count
    }));

    // Initial sort by count (high to low)
    currentData.sort((a, b) => d3.descending(a.count, b.count));

    // Set color scale domain once (fixed mapping of colors to industries)
    colorScale.domain(currentData.map(d => d.industry));

    // Initial render
    updateChart(false);
}).catch(error => {
    console.error("Error loading data:", error);
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", height / 2)
        .attr("text-anchor", "middle")
        .attr("class", "error-text")
        .text("Error loading data. Please check the file path.");
});

// Update chart function
function updateChart(animate = true) {
    // Update scales
    xScale.domain(currentData.map(d => d.industry));
    yScale.domain([0, d3.max(currentData, d => d.count) * 1.1]);

    // Update axes with transition
    const transition = d3.transition()
        .duration(animate ? 750 : 0)
        .ease(d3.easeCubicInOut);

    xAxisGroup
        .transition(transition)
        .call(xAxis)
        .selectAll("text")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end");

    yAxisGroup
        .transition(transition)
        .call(yAxis);

    // Bind data to bars
    const bars = svg.selectAll(".bar")
        .data(currentData, d => d.industry);

    // Exit old bars
    bars.exit()
        .transition(transition)
        .attr("y", height)
        .attr("height", 0)
        .remove();

    // Enter new bars
    const barsEnter = bars.enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", d => xScale(d.industry))
        .attr("y", height)
        .attr("width", xScale.bandwidth())
        .attr("height", 0)
        .attr("rx", 4)
        .attr("ry", 4);

    // Merge enter and update selections
    const barsMerge = barsEnter.merge(bars);

    // Update all bars with transition
    barsMerge
        .transition(transition)
        .attr("x", d => xScale(d.industry))
        .attr("y", d => yScale(d.count))
        .attr("width", xScale.bandwidth())
        .attr("height", d => height - yScale(d.count))
        .attr("fill", d => colorScale(d.industry));

    // Add interaction handlers
    barsMerge
        .on("mouseover", handleMouseOver)
        .on("mousemove", handleMouseMove)
        .on("mouseout", handleMouseOut)
        .on("click", handleClick);

    // Update selected bar styling
    barsMerge.classed("selected", d => selectedBar === d.industry);
}

// Mouse over handler - show tooltip
function handleMouseOver(event, d) {
    tooltip.transition()
        .duration(200)
        .style("opacity", 1);

    tooltip.html(`
        <div class="tooltip-content">
            <strong>${d.industry}</strong><br/>
            <span class="tooltip-count">${d.count.toLocaleString()} startups</span>
        </div>
    `);

    // Highlight bar on hover (if not selected)
    if (selectedBar !== d.industry) {
        d3.select(event.currentTarget)
            .classed("hovered", true);
    }
}

// Mouse move handler - update tooltip position
function handleMouseMove(event) {
    tooltip
        .style("left", (event.pageX + 15) + "px")
        .style("top", (event.pageY - 28) + "px");
}

// Mouse out handler - hide tooltip
function handleMouseOut(event, d) {
    tooltip.transition()
        .duration(500)
        .style("opacity", 0);

    // Remove hover styling
    d3.select(event.currentTarget)
        .classed("hovered", false);
}

// Click handler - toggle selection
function handleClick(event, d) {
    if (selectedBar === d.industry) {
        // Deselect if clicking the same bar
        selectedBar = null;
    } else {
        // Select new bar
        selectedBar = d.industry;
    }

    // Update all bars
    svg.selectAll(".bar")
        .classed("selected", bar => bar.industry === selectedBar);
}

// Sort button handler
d3.select("#sort-button").on("click", function() {
    if (sortMode === 'descending') {
        // Sort by count (low to high)
        currentData.sort((a, b) => d3.ascending(a.count, b.count));
        sortMode = 'ascending';
        d3.select(this).text("Sort: High → Low");
    } else {
        // Sort by count (high to low)
        currentData.sort((a, b) => d3.descending(a.count, b.count));
        sortMode = 'descending';
        d3.select(this).text("Sort: Low → High");
    }

    updateChart(true);
});
