// change link and add id for equations

document.querySelectorAll(`a.eq`).forEach( (el) => {
  'use strict';
  el.parentNode.id = "eq:"+el.id
  el.href = "#eq:"+el.id
});

document.querySelectorAll(`a.aeq`).forEach( (el) => {
  'use strict';
  el.href = el.href.replace(/#/,"#eq:");
});


