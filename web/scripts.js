/**
 * Created by susperius on 11.07.15.
 */

FUZZERS


function changeFuzzer(){
    var x = -1;
    var fuzz_table = document.getElementById("fuzz_table");
    var old_inputs = document.getElementById("fuzz_config");
    var new_inputs = document.createElement("div");
    var fuzz_select = document.getElementById("fuzzers");
    new_inputs.id = "fuzz_config";
    for(i=0; i<fuzzers.length; i+=2){
        if(fuzzers[i] == fuzz_select.value){
            x = i + 1;
        }
    }

    for(i=0; i<fuzzers[x].length; i++){
        var input = document.createElement("input");
        input.type = "text";
        input.name = fuzzers[x][i];
        new_inputs.appendChild(input);
    }
    old_inputs.parentNode.replaceChild(new_inputs, old_inputs);
}

function set_select_value(name){
    var fuzz_select = document.getElementById("fuzzers");
    fuzz_select.value = name;
}

//