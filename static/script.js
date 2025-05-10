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
    current = (current + 1) % flashcards.length;
    showCard();
}

window.onload = loadFlashcards;
