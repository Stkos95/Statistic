function createPart(element) {
    let value;
    const targetDiv = document.querySelector('#parts');
    console.log(targetDiv)

    if (targetDiv.children.length > 1) {
        const typeTextFilled = Array.from(targetDiv.children).at(-1).querySelector('input');

        value = typeTextFilled.value
    }
    else {
        value = '1';
    }
    if (!value) {

        console.log('Название предыдущего раздела не заполнено!')
    }
    else {
        console.log('11111')
            const emptyForm = document.querySelector('#empty-form').cloneNode(true);
    emptyForm.removeAttribute('id');
    // change prefix affter i added new part.;
        const regex = new RegExp('__prefix__', 'g')
        const numberOfParts = document.querySelectorAll('.part').length
        emptyForm.innerHTML = emptyForm.innerHTML.replace(regex, numberOfParts - 1) // because empty_form has 'parts' and it counts as well.
    //    add +1 form to management form
        const totalFormsParts = document.querySelector('#id_parts-TOTAL_FORMS')
        totalFormsParts.setAttribute('value', numberOfParts)





    targetDiv.appendChild(emptyForm);
    }
}

function removePart(element) {
    const currentDiv = element.parentNode.addEventListener('sortupdate');
    const text = currentDiv.querySelector('input').value;
    console.log(currentDiv.id)
    if (currentDiv.id === 'empty-form') {
        return
    }
    const d = confirm(`Вы хотите удалить раздел ${text}?`)
    if (d) {
        currentDiv.remove()
    }
}