function createPlusMinusButtons(element) {
    const plus = createButton('plus-button', '+')
    // const minus = createButton('minus-button', '-')

    // element.parentNode.insertBefore(minus, element)
    element.after(plus)

    // plus button event
    plus.addEventListener('click', (element) => {
        let number = plus.previousElementSibling;


        number.stepUp();
        let change = new Event("change");
        number.dispatchEvent(change)
    })

    // minus button event
    // minus.addEventListener('click', (element) => {
    //     let number = minus.nextElementSibling;
    //     number.stepDown()
    //     let change = new Event('change');
    //     number.dispatchEvent(change)
    // })

}


function createButton(cl, text) {
    let button = document.createElement('button')
    button.setAttribute('class', cl)
    button.setAttribute('type', 'button')

    let buttonText = document.createTextNode(text)
    button.appendChild(buttonText)

    return button

}

