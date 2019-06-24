
addEventListenerAll('.btn-spn-up', 'click', event => this.spinUp(event))
addEventListenerAll('.btn-spn-down', 'click', event => this.spinDown(event))
  
function spinUp(event) {  
  var spinRoot = event.currentTarget.parentElement.parentElement  // .btn-spn
  var spinInput = spinRoot.children[1]    
  if (!spinInput.value || spinInput.value==="" || isNaN(parseInt(spinInput.value)))
    spinInput.value = 0
  var spinValue = parseInt(spinInput.value)
  
  var max = spinInput.getAttribute('max')
  if (!max || spinValue < max)
    spinInput.value = spinValue+1
  else if (max && spinValue > max)
    spinInput.value = max
}

function spinDown(event) {
  var spinRoot = event.currentTarget.parentElement.parentElement  // .btn-spn
  var spinInput = spinRoot.children[1]
  if (!spinInput.value || spinInput.value==="" || isNaN(parseInt(spinInput.value)))
    spinInput.value = 0
  var spinValue = parseInt(spinInput.value)
  
  var min = spinInput.getAttribute('min')
  if (!min || spinValue > min)
    spinInput.value = spinValue-1
  else if (min && spinValue < min)
    spinInput.value = min
}

function addEventListenerAll(selector, eventName, eventHandler) {
  var elements = document.querySelectorAll(selector)
  for(var i = 0; i<elements.length; i++) {
      elements[i].addEventListener(eventName, eventHandler) 
  }
}