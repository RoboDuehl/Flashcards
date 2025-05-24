let flashcards = [];
let current = 0;

async function loadFlashcards() {
    const res = await fetch('/api/flashcards');
    flashcards = await res.json();
    showCard();
}

function showCard() {
    if (flashcards.length === 0) return;
    const card = flashcards[current];
    document.getElementById('word').textContent = card.word;
    document.getElementById('meaning').textContent = card.meaning;
    document.getElementById('example').textContent = card.example || '';
}

function nextCard() {
    let next;
    do {
        next = Math.floor(Math.random() * flashcards.length);
    } while (next === current);
    current = next;
    showCard();
}


window.onload = loadFlashcards;
