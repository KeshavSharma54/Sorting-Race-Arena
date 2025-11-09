// 🎲 Generate random array based on selected data type
document.getElementById("generateArray").addEventListener("click", () => {
  const dataType = document.getElementById("dataType").value;
  let arr;

  if (dataType === "int") {
    arr = Array.from({ length: 30 }, () => Math.floor(Math.random() * 100));
  } else if (dataType === "float") {
    arr = Array.from({ length: 30 }, () => (Math.random() * 100).toFixed(2));
  } else {
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    arr = Array.from({ length: 30 }, () => letters[Math.floor(Math.random() * letters.length)]);
  }

  document.getElementById("arrayInput").value = arr.join(", ");
});


// 🏁 Start the Sorting Race
document.getElementById("startRace").addEventListener("click", async () => {
  const rawInput = document.getElementById("arrayInput").value.split(",").map(v => v.trim());
  const dataType = document.getElementById("dataType").value;

  let arr;
  if (dataType === "int") {
    arr = rawInput.map(Number);
  } else if (dataType === "float") {
    arr = rawInput.map(parseFloat);
  } else {
    arr = rawInput.map(String);
  }

  const betAlgo = document.getElementById("betAlgo").value;

  document.getElementById("raceArena").innerHTML = "🏁 Racing...";

  // 🚀 Send dataType to Flask backend
  const response = await fetch("/race", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ array: arr, dataType })  // ✅ updated here
  });

  const data = await response.json();
  document.getElementById("raceArena").innerHTML = "";

  const maxTime = Math.max(...data.results.map(r => r[1]));
  let winner = data.results[0][0];

  // 🏎️ Animate race lanes
  
  data.results.forEach(([algo, time]) => {
  const lane = document.createElement("div");
  lane.classList.add("lane");
  lane.style.setProperty("--final-width", `${(1 - time / maxTime) * 90}%`);
  lane.innerHTML = `
    ${algo}: ${time.toFixed(5)}s
    <div class="tooltip">
      <b>${algo}</b><br>
      ${getExplanation(algo)}
    </div>`;
  document.getElementById("raceArena").appendChild(lane);
});


  // 🎯 Betting result
  let resultMsg = (betAlgo === winner)
    ? `🎉 You guessed right! ${winner} won!`
    : `😢 ${winner} won. Better luck next time!`;
  document.getElementById("leaderboard").innerText = resultMsg;

  // 📜 Load race history
  loadHistory();
});


// 📘 Explanation tooltips
function getExplanation(algo) {
  const info = {
    "Bubble Sort": "Repeatedly swaps adjacent elements. Best O(n), Worst O(n²).",
    "Selection Sort": "Finds min and places it. O(n²) time, O(1) space.",
    "Insertion Sort": "Inserts elements into correct position. Best O(n).",
    "Merge Sort": "Divide and conquer, O(n log n) always.",
    "Quick Sort": "Uses pivot partitioning, O(n log n) average.",
    "Heap Sort": "Builds heap and extracts min, O(n log n).",
    "Shell Sort": "Improved insertion with gaps, O(n log² n) avg."
  };
  return info[algo] || "Efficient sorting algorithm.";
}


// 🕒 History loader
async function loadHistory() {
  const res = await fetch("/history");
  const history = await res.json();
  const div = document.getElementById("history");
  div.innerHTML = "<h3>Last Races:</h3>";
  history.forEach(h => {
    div.innerHTML += `<p>${h.time} — Winner: ${h.results[0][0]}</p>`;
  });
}

window.onload = loadHistory;

