function addAction(element) {
    const actionsDiv = element.previousElementSibling;
    console.log(actionsDiv)
    const action = document.querySelector('#empty-form .action').cloneNode(true);
    actionsDiv.appendChild(action)
    action.setAttribute('draggable', true)
    action.setAttribute('role', 'option')
    action.setAttribute('aria-grabbed', false)


    const totalForms = actionsDiv.querySelector(`[name$="TOTAL_FORMS"]`);
    const totalFormsNumber = totalForms.getAttribute('value');

    const actionIdRegex = new RegExp('actions-\\d', 'g');
    const totalActions = totalFormsNumber;
    action.innerHTML = action.innerHTML.replace(actionIdRegex, `actions-${totalActions}`)
    console.log(action)

    const regex = new RegExp('__prefix__', 'g');
    const currentPartDiv = element.parentNode
    const numberOfParts = document.querySelectorAll('.part')
    const currentPartId = Array.from(numberOfParts).findIndex((element) => {
        return element === currentPartDiv;
    }) - 1
    action.innerHTML = action.innerHTML.replace(regex, currentPartId)

    const new_value = parseInt(totalFormsNumber) + 1
    totalForms.setAttribute('value', new_value)



}


function removeAction(element) {

    const actionsDiv = element.parentNode.parentNode;
    const action = element.parentNode

    // const totalForms = actionsDiv.querySelector(`[name$="TOTAL_FORMS"]`)
    // const totalFormsNumber = totalForms.getAttribute('value')
    // const new_value = parseInt(totalFormsNumber) - 1;
    // totalForms.setAttribute('value', new_value)

    //    mark DELETE field as 'on'
    const deleteField = action.querySelector('[name$="DELETE"]')
    console.log(deleteField)
    deleteField.setAttribute('value', 'on')
    action.style.display = 'none'

    // element.parentNode.remove()
}

