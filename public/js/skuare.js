const gameSizeOptions = [3, 4, 5, 6, 7, 8, 9, 10];
let size = gameSizeOptions[0];
let cells = [];

// init game
const game = document.createElement("div");
document.currentScript.parentElement.appendChild(game);

// init size selector
const sizeSelector = document.createElement("select");
sizeSelector.innerHTML = gameSizeOptions.map((o) => `<option>${o}</option>`);
sizeSelector.addEventListener("change", (e) => {
    size = parseInt(e.target.value);
    reset();
});
game.appendChild(sizeSelector);

// init table
const table = document.createElement("table");
game.appendChild(table);

// init msg
const msg = document.createElement("p");
game.appendChild(msg);

// init reset btn
const resetBtn = document.createElement("button");
resetBtn.innerHTML = "reset";
resetBtn.addEventListener("click", reset);
game.appendChild(resetBtn);

// -------------------------- GAME LOGIC -------------------------- //

class Cell {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.isOn = false;
    }

    setElt(elt) {
        elt.classList.add(this.isOn ? "on" : "off");
        elt.addEventListener("click", () => this.onClick());
        elt.addEventListener("mouseover", () => this.onMouseOver());
        elt.addEventListener("mouseout", () => this.onMouseOut());
        this.elt = elt;
    }

    onClick() {
        // toggles this and neighbours
        this.isOn = !this.isOn;
        const neighbours = getNeighbourCells(this);
        for (const n of neighbours) n.isOn = !n.isOn;

        // updates UI
        refreshCells();

        // checks for win
        checkWin();
    }

    onMouseOver() {
        this.elt.classList.add("hover");
        const neighbours = getNeighbourCells(this);
        for (const n of neighbours) n.elt.classList.add("hover");
    }

    onMouseOut() {
        this.elt.classList.remove("hover");
        const neighbours = getNeighbourCells(this);
        for (const n of neighbours) n.elt.classList.remove("hover");
    }
}

function refreshCells() {
    table.innerHTML = "";
    for (let y = 0; y < size; y++) {
        if (!cells[y]) cells[y] = [];
        const row = document.createElement("tr");
        for (let x = 0; x < size; x++) {
            const elt = document.createElement("td");
            if (!cells[y][x]) cells[y][x] = new Cell(x, y);
            cells[y][x].setElt(elt);
            row.appendChild(elt);
        }
        table.appendChild(row);
    }
    checkWin();
}

// -------------------------- HELPERS -------------------------- //

// gets adjacent cells
function getNeighbourCells(cell) {
    const neighbours = [];
    if (cell.x - 1 >= 0) neighbours.push(cells[cell.y][cell.x - 1]);
    if (cell.x + 1 < size) neighbours.push(cells[cell.y][cell.x + 1]);
    if (cell.y - 1 >= 0) neighbours.push(cells[cell.y - 1][cell.x]);
    if (cell.y + 1 < size) neighbours.push(cells[cell.y + 1][cell.x]);
    return neighbours;
}

function checkWin() {
    let onCount = 0;
    for (let y = 0; y < size; y++) {
        for (let x = 0; x < size; x++) {
            onCount += cells[y][x].isOn;
        }
    }

    if (onCount === size * size) {
        table.classList.add("win");
        msg.innerHTML = "YOU WIN!";
    } else {
        table.classList.remove("win");
        msg.innerHTML = "";
    }
}

function reset() {
    cells = [];
    refreshCells();
}

// -------------------------- BEGIN -------------------------- //

refreshCells();
