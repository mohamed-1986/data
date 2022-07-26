
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
        options += '<option value = '+ PidItems[index].pk +'>Unit '+ PidItems[index].fields.unit ;
        options += ' ' + PidItems[index].fields.name + '</option>\n';
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
    let old_sel_datasheet = document.querySelectorAll('#id_datasheet option');
    // sel_datasheet is what we write the final options in
    let sel_datasheet = document.querySelector('#id_datasheet');
    let optionWithSel = [];
    let oldSelValues = [];
    for (let index = 0; index < old_sel_datasheet.length; index++) {
        if(old_sel_datasheet[index].hasAttribute('selected')){
            optionWithSel.push(old_sel_datasheet[index]);
            oldSelValues.push(old_sel_datasheet[index].value)
        };
    };
    let options3 = '';
    // Add the previously selected
    // console.log(optionItem.length);
    for (let index = 0; index < optionWithSel.length ; index++) {
        options3 += '<option value = '+ optionWithSel[index].value +' selected>';
        options3 += optionWithSel[index].text + '</option>\n';
    };
    // Initiate option text to add previously selected and the returned from the API.
    let options2 = '';
    // Add the previously selected
    // console.log(optionItem.length);
    console.log(oldSelValues);
    for (let index = 0; index < datasheetItems.length ; index++) {
        
        if (oldSelValues.includes(String(datasheetItems[index].pk))){
            console.log(String(datasheetItems[index].pk));
        }else{
            options2 += '<option value = '+ datasheetItems[index].pk +'>';
            if (datasheetItems[index].fields.type === 'gn'){
                options2 += 'General '
            };
            options2 += datasheetItems[index].fields.name+ '</option>\n';
            };
    };

    console.log('Datasheet length '+datasheetItems.length);
    // updata only if there are data
    if (datasheetItems.length > 0){
        sel_datasheet.innerHTML = options3 + options2;
    }
};


//***************************************************************************************** */

// Here we will update category and type of queryset drop list by editing 
// cat list and typ list in the filter section

let catFilter = document.getElementById('id_cat');
let typeFilter = document.getElementById('id_type');


// here we want to reselect the previously selected options
// so this func will be called to loop through all possible options of the manual drop down
// and select the only 'selected' attribute.
text = '';
var PSarray = [];
function scanMe(item, index) {
    if( item.hasAttribute('selected')){
        PSarray.push(item.value)
        text += '<option value=' + item.value + ' selected >' + item.text + '</option>\n'
        return PSarray
    };
};

//the default value of catfilter and typFilter is 'na'
//whover changed manual drop list must be updated according to both of them

async function manualUpdate() {
    let catFilter = document.getElementById('id_cat');
    let typeFilter = document.getElementById('id_type');

    let url = window.location.protocol + "//" + window.location.host;
    url += '/api/manual/cat=' + catFilter.value + '/type=' + typeFilter.value;
    // console.log(url);
    const data = await fetch(url);
    const res = await data.json();
    // console.log(res);

    var manualItems = JSON.parse(res.manual_queryset);
    // console.log('length of manualItems API is '+ manualItems.length)    

    let sel_man = document.querySelector('#id_manual');
    
    //first we put the previously selected options then add to them the response from the API
    const arr = document.querySelectorAll('#id_manual option');
    // console.log('the length of selected previously is ' + arr.length);
    // Convert manuals of API from array to text
    //loop for each option in arr list to select the wanted option and write them to text
    // PSarray = []
    if (PSarray.length === 0){
        arr.forEach(scanMe);
    };
    
    let finalArray = [];

    // console.log(optionItem.length);
    // all manuals returned from API  manualItems  >>>>>manualItems  (150)
    // Previously Selected >>>>>>>  PSarray (2)
    // final array conatins PS then all manualItems excluding PS. 


    // Make a copy from the api maualitems in order to delete the repetetion from it
    var modiManualItem = manualItems;
    // looping through all api manualItems then delete the repeated from manualItems
    for (let index = 0; index < manualItems.length ; index++) {
        // Remove the repeated options from api that is already selected 
        if(PSarray.includes(String(manualItems[index].pk))){
            modiManualItem = modiManualItem.filter(item => item !== manualItems[index]);
        }
    };

    var txt_api = '';

    for (let index1 = 0; index1 < modiManualItem.length; index1++) {
        txt_api += '<Option value = '+ modiManualItem[index1].pk + '>' + modiManualItem[index1].fields.name + '</Option>';
    
    };
    const fullText = text + txt_api;
    // console.log(manualItems.length);
    // updata only if there are data
    // const fullText = text + options;
    sel_man.innerHTML = fullText;
};

catFilter.addEventListener('change', manualUpdate, false);
typeFilter.addEventListener('change', manualUpdate, false);
