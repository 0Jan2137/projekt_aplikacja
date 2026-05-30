// Sorting - requires table component present in tables/transactions_table.html

let directions = [true, true, true];
const SORT_STORAGE_KEY = 'recent-transactions-sort';

function sortTransactions(colIdx, type, asc=undefined) {
    const container = document.getElementById("transactions-container");
    const rows = Array.from(container.getElementsByClassName("transaction-row"));
    const isAsc = asc !== undefined ? asc : directions[colIdx];

    var rows2 = rows.sort((a, b) => {
        // Account for the hidden bulk-delete-column at index 0
        let colElement = colIdx + 1;
        let valA = a.children[colElement].getAttribute("data-val") || a.children[colElement].innerText.trim();
        let valB = b.children[colElement].getAttribute("data-val") || b.children[colElement].innerText.trim();
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
    console.log(rows)
    console.log(rows2)

    for (let i = 0; i < 3; i++) {
        document.getElementById(`sort-${i}`).innerHTML = (i === colIdx) ? (isAsc ? "↑" : "↓") : "";
    }
}