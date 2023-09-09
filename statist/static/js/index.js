
function addPlayer(element){

    let form = document.querySelector('form');
    let confirmButton = document.querySelector('form input[type="submit"]');

    // if (element.previousElementSibling.value.trim() === '') {
    // return false;
    // }
    let maxNumbers = []
    let maxValue = document.querySelectorAll('input.players');
    maxValue.forEach((e) => {

        maxNumbers.push(parseInt(e.getAttribute('name')))
    })

    let max = Math.max(...maxNumbers) + 1





    let div = document.createElement('div')
    div.setAttribute('class', 'player')



    form.insertBefore(div, confirmButton)

    // div.insertAdjacentHTML('afterbegin', '<span class="test">')
    let field = document.createElement('input')
    field.setAttribute('type', 'text')
    field.setAttribute('name', max)
    field.classList.add('players')

    let plus = document.createElement('span')
    plus.setAttribute('onclick', 'addPlayer(this)')
    let plusText = document.createTextNode('+')
    plus.appendChild(plusText)

    let minus = document.createElement('span')
    minus.setAttribute('onclick', 'removePlayer(this)')
    let minusText = document.createTextNode('-')
    minus.appendChild(minusText)


    div.appendChild(field)
    div.appendChild(plus)
    div.appendChild(minus)

    element.nextElementSibling.style.display = 'inline'

    element.style.display = 'none'


}




function removePlayer(element) {
    if(element.previousElementSibling.previousElementSibling.value) {
        let conf = confirm('В строке введено значение, удалить?')

        if (conf) {
            element.parentNode.remove()
        }

    }

    else {
            element.parentNode.remove()
        }



}