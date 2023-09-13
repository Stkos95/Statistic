function addPlayer(element = null) {
    let form = document.forms[0];
    let table = document.querySelector('table')
    let confirmButton = document.querySelector('form input[type="submit"]');


    let rowCopied = document.querySelector('.field-row').cloneNode(true)

    rowCopied.style.display = 'table-row'
    let c = table.insertRow(-1)
    c.classList.add('field-row')

    c.innerHTML = rowCopied.innerHTML

    let minus = c.querySelector('.remove-player')

    let players = document.querySelectorAll('.field-row')
    if (players.length > 2) {
        minus.style.display = 'inline'

    }
    if (element) {
        element.nextElementSibling.style.display = 'inline'
        element.style.display = 'none'
    }
    // const inputFields = divCopied.querySelectorAll('.count-field')
    // for (let el of inputFields) {
    //     createPlusMinusButtons(el)
    // }

}

//
// function removePlayer(element) {
//     let conf
//     let flag = false
//     const parentDiv = element.parentNode.parentNode
//     // console.log(parentDiv.children[0].childNodes[0])
//     parentDiv.remove()
//     //
//     for (let field of parentDiv.children) {
//         console.log(field.childNodes[0])
//
//
//     }
//         // if (field.childNodes[0].tagName === 'INPUT' && field.value && !flag){
//     //         conf = confirm('В строке введено значение, удалить?')
//     //         flag = true
//     //         break
//     //
//     //     }
//     // }
//     //
//     // if (conf || !flag) {
//     //     element.parentNode.remove()
//     // }
//     //
let buttons = document.querySelectorAll('.add-player')
let LastButton = buttons[buttons.length - 1];
if (buttons.length === 2) {
    LastButton.nextElementSibling.style.display = 'none'
}
LastButton.style.display = 'inline'
//
// }


function removePlayer(element) {
    let conf = true
    const parentElement = element.parentNode.parentNode

    for (let field of parentElement.children) {
        if (field.children[0].tagName === 'INPUT' && field.children[0].value) {
            conf = confirm('В строке введено значение, удалить?')
            break
        }

    }


    if (conf) {
        parentElement.remove()
    }

    let buttons = document.querySelectorAll('.add-player')
    let LastButton = buttons[buttons.length - 1];
    if (buttons.length === 2) {
        LastButton.nextElementSibling.style.display = 'none'
    }
    LastButton.style.display = 'inline'


}
