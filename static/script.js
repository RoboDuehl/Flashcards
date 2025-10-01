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
    if (flashcards.length === 0) return;
    current = Math.floor(Math.random() * flashcards.length);
    console.log("Flashcards length:", flashcards.length);
    console.log("Current index:", current);
    console.log("Card:", flashcards[current]);

    showCard();
}

function updateFlashcard() {
    const word = document.getElementById("word").innerText;
    const meaning = prompt("Enter new meaning:");
    const example = prompt("Enter new example:");

    fetch("/api/flashcards/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ word, meaning, example })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Flashcard updated successfully!");
            // Optionally update UI:
            document.getElementById("meaning").innerText = meaning;
            document.getElementById("example").innerText = example;
        } else {
            alert("Error: " + (data.error || "Unknown error"));
        }
    })
    .catch(error => {
        console.error("Update failed:", error);
        alert("Failed to update flashcard.");
    });
}


window.onload = loadFlashcards;
