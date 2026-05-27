let directions = [true, true, true];
const SORT_STORAGE_KEY = 'recent-transactions-sort';

function sortTransactions(colIdx, type, asc=undefined) {
    const container = document.getElementById("transactions-container");
    const rows = Array.from(container.getElementsByClassName("transaction-row"));
    const isAsc = asc !== undefined ? asc : directions[colIdx];

    rows.sort((a, b) => {
        let valA = a.children[colIdx].getAttribute("data-val") || a.children[colIdx].innerText;
        let valB = b.children[colIdx].getAttribute("data-val") || b.children[colIdx].innerText;

        if (type === 'number') return isAsc ? parseFloat(valA) - parseFloat(valB) : parseFloat(valB) - parseFloat(valA);
        if (type === 'date') return isAsc ? new Date(valA) - new Date(valB) : new Date(valB) - new Date(valA);
        return isAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
    });

    directions[colIdx] = !isAsc;
    saveState(SORT_DIRECTION_KEY, {
        "colIdx": colIdx,
        "type": type,
        "isAsc": isAsc
    });
    rows.forEach(row => container.appendChild(row));

    for (let i = 0; i < 3; i++) {
        document.getElementById(`sort-${i}`).innerHTML = (i === colIdx) ? (isAsc ? "↑" : "↓") : "";
    }
}