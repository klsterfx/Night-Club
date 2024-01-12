function increment(){
    const radioButtons = document.querySelectorAll('input[name="club"]');
    var check = 0;

        for (const radioButton of radioButtons) {
            const box = document.getElementById(radioButton.id + " details");
            if (radioButton.checked) {
                if (parseInt(radioButton.value)  < parseInt(box.getAttribute('yellow'))){
                    check = 1;
                    radioButton.value = parseInt(radioButton.value) +1;
                }
                else if (parseInt(radioButton.value)  < parseInt(box.getAttribute('capacity'))){
                    check = 2;
                    radioButton.value = parseInt(radioButton.value) +1;
                }
                else {
                    check = 3;
                }
                display(radioButton, box, check);
                //display(radioButton, box);
                break;
            }
        }
}


function decrement(){
    const radioButtons = document.querySelectorAll('input[name="club"]');
    var check = 0;

        for (const radioButton of radioButtons) {
            const box = document.getElementById(radioButton.id + " details");
            if (radioButton.checked) {
                if (parseInt(radioButton.value)  > parseInt(box.getAttribute('yellow'))){
                    check = 2;
                    radioButton.value = parseInt(radioButton.value) -1;
                }
                else if (parseInt(radioButton.value)  > 0){
                    check = 1;
                    radioButton.value = parseInt(radioButton.value) -1;
                }
                display(radioButton, box, check);
                //display(radioButton, box);
                break;
            }
        }
}


function display(radioButton, box, check){
    if (check==1){
        box.innerHTML = radioButton.id +"<br> Welcome" ;
        box.style.backgroundColor= "#80e780";
    }
    else if (check==2){
        box.innerHTML = radioButton.id +"<br>  Warn the bouncers…" ;
        box.style.backgroundColor= "yellow";
    }
    else if (check ==3){
        box.innerHTML = radioButton.id +"<br>  No one allowed in!" ;
        box.style.backgroundColor= "red";
    }
    
}
