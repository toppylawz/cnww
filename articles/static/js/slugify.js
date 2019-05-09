const titleinput = document.querySelector('input[name=title]');
const sluginput = document.querySelector('input[name=slug]');

const slugify= (val)=>
{ return val.toString().toLowerCase().trim()
    .replace(/&/g, '-and-') //this replaces & with '-and'
    .replace(/[\s\W-]+/g, '-')  //this replaces spaces, non word chars and dashes with 'single dash'
};

titleinput.addEventListener('keyup',(e) =>{
  sluginput.setAttribute('value', slugify(titleinput.value));

});
