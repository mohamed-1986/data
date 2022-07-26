
// If we add a new tag that is already in database a message appears beside tag input field
let x = document.getElementById('id_tag');

x.addEventListener('change', async function checkIt(){
    const url = window.location.protocol + "//" + window.location.host + '/check/' + x.value +'/';

    const y = await fetch(url);

    const z = await y.json();

    console.log(z.response);
    let node = 'Already in database!';
    if (z.response === 'Found'){
        
        x.insertAdjacentText('afterend', node);
    }
}
);

//******************************************************************************************** */

// Update pid drop down by changing filter unit drop down.
// api/unit-option/<slug>/
let unitChangePid = document.getElementById('id_unit');

unitChangePid.addEventListener('change' , unitOptions);

async function unitOptions(){
    let unitChangePid00 = document.getElementById('id_unit');
    const url = window.location.protocol + "//" + window.location.host + '/api/unit-option/' + unitChangePid00.value +'/';
    const data = await fetch(url);
    
    // Here (res) is the response js object replied by the get request containing PID, 2Wire, datasheet updates.
    const res = await data.json();

    //************************************************************************
    //select the pid response from the whole response:
    const PidItems = JSON.parse(res.pid_options);

    let sel_pid = document.querySelector('#id_pid');

    let options = '<option value selected>---------</option>\n';
    // console.log(optionItem.length);
    for (let index = 0; index < PidItems.length ; index++) {
        // console.log('id is ' + optionItem[index].pk + '  and name is ' + optionItem[index].fields.name);
        options += '<option value = '+ PidItems[index].pk +'>'+ PidItems[index].fields.name+ '</option>\n';
    }

    console.log('P&ID length '+PidItems.length);
    // updata only if there are data
    if (PidItems.length > 0){
        sel_pid.innerHTML = options;
    }
    //*************************************************************************** */
    //select the two wire response from the whole response:
    const wireItems = JSON.parse(res.twoWire_options);
     
    let sel_wire = document.querySelector('#id_wire');

    let options1 = '<option value selected>---------</option>\n';
    // console.log(optionItem.length);
    for (let index = 0; index < wireItems.length ; index++) {
        // console.log('id is ' + optionItem[index].pk + '  and name is ' + optionItem[index].fields.name);
        options1 += '<option value = '+ wireItems[index].pk +'>'+ wireItems[index].fields.tag+ '</option>\n';
    }

    console.log('2 wire length '+ wireItems.length);
    // updata only if there are data
    if (wireItems.length > 0){
        sel_wire.innerHTML = options1;
    }
    //*************************************************************************** */
    //select the Datasheet response from the whole response:
    const datasheetItems = JSON.parse(res.datasheet_options);
    // const det = JSON.parse(datasheetItems[0].fields);
    
    let sel_datasheet = document.querySelector('#id_datasheet');

    let options2 = '';
    // console.log(optionItem.length);
    for (let index = 0; index < datasheetItems.length ; index++) {
        // console.log('id is ' + optionItem[index].pk + '  and name is ' + optionItem[index].fields.name);
        options2 += '<option value = '+ datasheetItems[index].pk +'>'
        if (datasheetItems[index].fields.type === 'gn'){
            options2 += 'General '
        }
        options2 += datasheetItems[index].fields.name+ '</option>\n';
    }

    console.log('Datasheet length '+datasheetItems.length);
    // updata only if there are data
    if (datasheetItems.length > 0){
        sel_datasheet.innerHTML = options2;
    }
};


// Here we will update category and type of queryset drop list by editing 
// cat list and typ list in the filter section

let catFilter = document.getElementById('id_cat');
let typeFilter = document.getElementById('id_type');

//the default value of catfilter and typFilter is 'na'
//whover changed manual drop list must be updated according to both of them

async function manualUpdate() {
    let catFilter = document.getElementById('id_cat');
    let typeFilter = document.getElementById('id_type');

    let url = window.location.protocol + "//" + window.location.host;
    url += '/api/manual/cat=' + catFilter.value + '/type=' + typeFilter.value;
    console.log(url);
    const data = await fetch(url);
    const res = await data.json();
    console.log(res);

    const manualItems = JSON.parse(res.manual_queryset);
    
    let sel_man = document.querySelector('#id_manual');

    let options = '';
    // console.log(optionItem.length);
    for (let index = 0; index < manualItems.length ; index++) {
        options += '<option value = '+ manualItems[index].pk +'>'+ manualItems[index].fields.name+ '</option>\n';
    }

    console.log(manualItems.length);
    // updata only if there are data
    if (manualItems.length > 0){
        sel_man.innerHTML = options;
    }
}

catFilter.addEventListener('change', manualUpdate, false);
typeFilter.addEventListener('change', manualUpdate, false);
