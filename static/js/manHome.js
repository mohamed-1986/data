var delBtn = document.querySelector('#btn-del-man');
var trashes = document.querySelectorAll('#img-trash');

function toggeler() {
    for (let index = 0; index < trashes.length; index++) {
        const element = trashes[index];
        if (element.style.display === 'none'){
            element.style.display = 'block'
        }else{
            element.style.display = 'none'
        };
    };
};

delBtn.addEventListener('click', toggeler);