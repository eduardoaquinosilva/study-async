function flip_card(cardId) {
    card = document.getElementById(cardId)
    if (card.style.display == "none" || card.style.display == "") {
        card.style.display = "block"
    } else {
        card.style.display = "none"
    }
}
