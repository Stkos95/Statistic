function createPart(element) {
    let value;
    const targetDiv = document.querySelector('#part');
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
            const emptyForm = document.querySelector('#empty-form').cloneNode(true);
    emptyForm.removeAttribute('id');
    // ---- add button, add its text "X", add onclick function removePart  to be able to remove one part -------
    const removeButton = document.createElement("span");

    const removeButtonText = document.createTextNode('X');
    removeButton.appendChild(removeButtonText);
    removeButton.setAttribute('onclick', 'removePart(this)')
    const label = emptyForm.childNodes[0];
    emptyForm.insertBefore(removeButton, label);
    // -----

    targetDiv.appendChild(emptyForm)
    }
}

function removePart(element) {
    const currentDiv = element.parentNode;
    const text = currentDiv.querySelector('input').value;
    console.log(text)
    const d = confirm(`Вы хотите удалить раздел ${text}?`)
    if (d) {
        currentDiv.remove()
    }
}



