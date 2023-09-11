
function addPlayer(element=null){
    let form = document.querySelector('form');
    let confirmButton = document.querySelector('form input[type="submit"]');

    let divCopied = document.querySelector('div.player-form').cloneNode(true)

    divCopied.style.display = 'block'
    form.insertBefore(divCopied, confirmButton)

    let minus = divCopied.childNodes[5]

    let players = document.querySelectorAll('.player-form')
    if (players.length > 2) {
        minus.style.display = 'inline'

    }
    if (element) {
        element.nextElementSibling.style.display = 'inline'
        element.style.display = 'none'
    }
    const inputFields = divCopied.querySelectorAll('.count-field')
    for (let el of inputFields) {
        createPlusMinusButtons(el)
    }
}




function removePlayer(element) {
    let conf
    let flag = false
    const parentDiv = element.previousElementSibling.previousElementSibling
    for (let field of parentDiv.children) {
        if (field.tagName === 'INPUT' && field.value && !flag){
            conf = confirm('В строке введено значение, удалить?')
            flag = true
            break

        }
    }

    if (conf || !flag) {
        element.parentNode.remove()
    }

    let buttons = document.querySelectorAll('.add-player')
     let LastButton = buttons[buttons.length - 1];
    if (buttons.length === 2) {
        LastButton.nextElementSibling.style.display = 'none'
    }
    LastButton.style.display = 'inline'

}


