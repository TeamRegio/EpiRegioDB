
/*  DEFAULT, NOMENCLATURE SWITCH, CLEANUPS **************************************** **************************************** */


function setDefaultGeneID() {
    document.getElementById("geneID_symbolic").type = "hidden";
    document.getElementById("geneID_numeric").type = "text";
    document.getElementById("geneHeader").textContent = "Ensembl gene ID:";
    document.getElementById("container_geneSymbolHeader").style.visibility = "hidden";
    document.getElementById('csv_upload').value = '';
    document.getElementById('container_geneSymbol').innerHTML = '';
    document.getElementById('container_cellTypes').innerHTML = '';
}

function setDefaultDropdown() {
    document.getElementById("chrField").selectedIndex = -1;
    document.getElementById('csv_upload').value = '';
}

function setDefaultREM() {
    document.getElementById('csv_upload').value = '';
}

//function switchGeneIDField(){
//   var current = document.getElementById("gene_format").value;
//    if (current === 'symbol_format') {
//        document.getElementById("geneID_symbolic").type = "text";
//        document.getElementById("geneID_numeric").type = "hidden";
//        document.getElementById("geneHeader").textContent = "Gene symbol:";
//        document.getElementById("container_geneSymbolHeader").style.visibility = "visible";
//
//// This here hides the error message when switching to the geneSymbol select. Otherwise
//// it would be displayed constantly
//        var validator = $( "#geneQueryForm" ).validate();
//        validator.showErrors({
//              "geneID_numeric": ""
//        });
//        validateGeneQueryForm_symbolic();
//        document.getElementById("geneID_numeric").className = "inputForm";
//    }
//
//    if (current === 'id_format') {
//    document.getElementById("geneID_symbolic").type = "hidden";
//    document.getElementById("geneID_numeric").type = "text";
//    document.getElementById("geneHeader").textContent = "Ensembl gene ID:";
//    document.getElementById("container_geneSymbolHeader").style.visibility = "hidden";
//
//    var validator = $( "#geneQueryForm" ).validate();
//    validator.showErrors({
//          "geneID_symbolic": ""
//        });
//    validateGeneQueryForm_numeric();
//    document.getElementById("geneID_symbolic").className = "inputForm";
//    }
//}

function clearFileInputField(tagId) {

    document.getElementById(tagId).innerHTML =

        document.getElementById(tagId).innerHTML;

}

function display_threshold(){
    container = document.getElementById("container_cellTypes").children;
    current = container.length;
    thresh_div = document.getElementById("threshold_div");
    if (current === 0){
        thresh_div.style.visibility = "hidden";
    }
    if (current !== 0){
        thresh_div.style.visibility = "visible";
    }
}


/*  Switch format to button **************************************** **************************************** */

function id_formatClick(){

    document.getElementById("geneID_symbolic").type = "hidden";
    document.getElementById("geneID_numeric").type = "text";
    document.getElementById("geneHeader").textContent = "Ensembl gene ID:";
    document.getElementById("container_geneSymbolHeader").style.visibility = "hidden";
    document.getElementById('id_format').className = 'format_active';
    document.getElementById('symbol_format').className = 'format_inactive';
    document.getElementById('gene_format').value = 'id_format';

    var validator = $( "#geneQueryForm" ).validate();
    validator.showErrors({
          "geneID_symbolic": ""
        });
    validateGeneQueryForm_numeric();
    document.getElementById("geneID_symbolic").className = "inputForm";

}

function symbol_formatClick(){

    document.getElementById("geneID_symbolic").type = "text";
    document.getElementById("geneID_numeric").type = "hidden";
    document.getElementById("geneHeader").textContent = "Gene symbol:";
    document.getElementById("container_geneSymbolHeader").style.visibility = "visible";
    document.getElementById('id_format').className = 'format_inactive';
    document.getElementById('symbol_format').className = 'format_active';
    document.getElementById('gene_format').value = 'symbol_format';

// This here hides the error message when switching to the geneSymbol select. Otherwise
// it would be displayed constantly
    var validator = $( "#geneQueryForm" ).validate();
    validator.showErrors({
          "geneID_numeric": ""
    });
    validateGeneQueryForm_symbolic();
    document.getElementById("geneID_numeric").className = "inputForm";
}



/*  BUTTON FUNCTIONS **************************************** **************************************** */
function chooseButton(clicked_id, containerID, if_empty_value){

    var container = document.getElementById(containerID);
    var existent_chosen = !!document.getElementById(clicked_id+'added');
    var existent_insearch = !!document.getElementById(clicked_id)
    if (existent_chosen === false) {
        var button_add = document.createElement("input");
        button_add.type = "button";
        if (existent_insearch === false){
            button_add.value = if_empty_value;
        }
        else
            button_add.value = document.getElementById(clicked_id).textContent;
        button_add.id = clicked_id+'added';
        button_add.className = "chosenButtons";
        container.appendChild(button_add);
        button_add.onclick = function(){
            $(this).remove();
            display_threshold();
        }
    if (containerID === "container_cellTypes"){
        display_threshold();
    }
    }
}

function ButtonsToInput(containerID, hiddenID){
    var container = document.getElementById(containerID).children;
    var txtc = "";
    var i;
    for (i=0; i < container.length; i++) {
        txtc = txtc + container[i].value + ", ";
    }
    $("#"+hiddenID).val(txtc);
}

function chooseRegion(example_chr, example_start, example_end, is_example){

    var container = document.getElementById("container_geneRegions");
    chr = document.getElementById("chrField").value;
    start = document.getElementById("chrStart").value;
    end = document.getElementById("chrEnd").value;
    if (is_example === 1) {
        chr = example_chr;
        start = example_start;
        end = example_end;
    }
    id_str = chr + "-" + start + "-" + end;
    var existent = !!document.getElementById(id_str);

    if (existent === false) {
        var button_add = document.createElement("input");
        button_add.type = "button";
        button_add.value = chr + ":" + start + "-" + end;
        button_add.id = id_str;
        button_add.className = "chosenButtons";
        container.appendChild(button_add);
        button_add.onclick = function(){
            $(this).remove();
        }
    }
}


/* SLIDER FUNCTIONS **************************************** **************************************** */
function sliderToField(slider_id, field_id) {
    var inputField = document.getElementById(field_id);
    var slider = document.getElementById(slider_id);
    inputField.value = parseInt(slider.value);
}
function changeSlider(slider_id, field_id){
    var slider = document.getElementById(slider_id);
    var inputField = document.getElementById(field_id);
    slider.value = parseInt(inputField.value);
};



/* CUSTOM DROPDOWN LIST **************************************** **************************************** */


var chr_start_end = {chr1: [8000, 248944655],
                    chr2: [14154, 242175634],
                    chr3: [173346, 198230196],
                    chr4: [100650, 190206737],
                    chr5: [58198, 181472430],
                    chr6: [95124, 170745982],
                    chr7: [8000, 159233377],
                    chr8: [60001, 145070549],
                    chr9: [10154, 138286430],
                    chr10: [14061, 133778699],
                    chr11: [75780, 135075899],
                    chr12: [10000, 133238549],
                    chr13: [18171247, 114351402],
                    chr14: [16057472, 106879812],
                    chr15: [19878555, 101981208],
                    chr16: [8000, 90226646],
                    chr17: [61649, 83245396],
                    chr18: [11103, 80247546],
                    chr19: [59993, 58607252],
                    chr20: [87250, 64330704],
                    chr21: [5008799, 46691226],
                    chr22: [10736171, 50808150],
                    chrX: [253252, 156029695],
                    chrY: [2784749, 56875803]}

function createDropdown(){
    var x, i, j, selElmnt, a, b, c;
    /*look for any elements with the class "custom-select":*/
    x = document.getElementsByClassName("custom-select");
    for (i = 0; i < x.length; i++) {
      selElmnt = x[i].getElementsByTagName("select")[0];
      /*for each element, create a new DIV that will act as the selected item:*/
      a = document.createElement("DIV");
      a.setAttribute("class", "select-selected");
      a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
      x[i].appendChild(a);
      /*for each element, create a new DIV that will contain the option list:*/
      b = document.createElement("DIV");
      b.setAttribute("class", "select-items select-hide");
      for (j = 1; j < selElmnt.length; j++) {
        /*for each option in the original select element,
        create a new DIV that will act as an option item:*/
        c = document.createElement("DIV");
        c.innerHTML = selElmnt.options[j].innerHTML;
        c.addEventListener("click", function(e) {
            /*when an item is clicked, update the original select box,
            and the selected item:*/
                dropdown = document.getElementById("chrField");
                chr = dropdown.options[dropdown.selectedIndex].value;

            var y, i, k, s, h;
            s = this.parentNode.parentNode.getElementsByTagName("select")[0];
            h = this.parentNode.previousSibling;


            for (i = 0; i < s.length; i++) {
              if (s.options[i].innerHTML == this.innerHTML) {
                s.selectedIndex = i;
                h.innerHTML = this.innerHTML;
                y = this.parentNode.getElementsByClassName("same-as-selected");
                for (k = 0; k < y.length; k++) {
                  y[k].removeAttribute("class");
                }
                this.setAttribute("class", "same-as-selected");
                break;
              }
            }
            h.click();
        });

        c.addEventListener("click", function(){
            dropdown = document.getElementById("chrField");
            chr = dropdown.options[dropdown.selectedIndex].value;
            document.getElementById("start_range").min = chr_start_end[chr][0];
            document.getElementById("start_range").max = chr_start_end[chr][1]-1;
            document.getElementById("end_range").min = chr_start_end[chr][0]+1;
            document.getElementById("end_range").max = chr_start_end[chr][1];
            hideError();
        });
        b.appendChild(c);
      }
      x[i].appendChild(b);
      a.addEventListener("click", function(e) {
          /*when the select box is clicked, close any other select boxes,
          and open/close the current select box:*/
          e.stopPropagation();
          closeAllSelect(this);
          this.nextSibling.classList.toggle("select-hide");
          this.classList.toggle("select-arrow-active");
        });
    }

    function closeAllSelect(elmnt) {
      /*a function that will close all select boxes in the document,
      except the current select box:*/
      var x, y, i, arrNo = [];
      x = document.getElementsByClassName("select-items");
      y = document.getElementsByClassName("select-selected");
      for (i = 0; i < y.length; i++) {
        if (elmnt == y[i]) {
          arrNo.push(i)
        } else {
          y[i].classList.remove("select-arrow-active");
        }
      }
      for (i = 0; i < x.length; i++) {
        if (arrNo.indexOf(i)) {
          x[i].classList.add("select-hide");
        }
      }
    }
    /*if the user clicks anywhere outside the select box,
    then close all select boxes:*/
    document.addEventListener("click", closeAllSelect);
}



/* EXEMPLARY QUERIES **************************************** **************************************** */

function exemplaryGeneIDQuery(){
    var current = document.getElementById("gene_format").value;

    if (current === 'id_format') {
        document.getElementById("geneID_numeric").value = "ENSG00000139874, ENSG00000274220";
        chooseButton("CTID_00000064", "container_cellTypes", "pancreas");
        chooseButton("CTID_0000038", "container_cellTypes", "skin fibroblast");
        chooseButton("CTID_0000052", "container_cellTypes", "heart");
        errorMsg = document.getElementById("geneID_numeric-error")
        errorMsg.parentNode.removeChild(errorMsg);
    };
    if (current === 'symbol_format') {
        chooseButton("SSTR1", 'container_geneSymbol', "SSTR1");
        chooseButton("DBR1", 'container_geneSymbol', "DBR1");
        chooseButton("RP11-77K12.9", 'container_geneSymbol', "RP11-77K12.9");
        chooseButton("CTID_00000064", "container_cellTypes", "pancreas");
        chooseButton("CTID_0000038", "container_cellTypes", "skin fibroblast");
        chooseButton("CTID_0000052", "container_cellTypes", "heart");
        errorMsg = document.getElementById("geneID_symbolic-error")
        errorMsg.parentNode.removeChild(errorMsg);
    };
}

function exemplaryREMQuery(){
    document.getElementById("REMIDs").value = "REM0595948, REM0236120, REM0236139 ";
    chooseButton("CTID_00000064", "container_cellTypes", "pancreas");
    chooseButton("CTID_0000038", "container_cellTypes", "skin fibroblast");
    chooseButton("CTID_0000052", "container_cellTypes", "heart");
    errorMsg = document.getElementById("REMIDs-error")
    errorMsg.parentNode.removeChild(errorMsg);
}

function exemplaryRegionQuery(){
    chooseRegion("chr4", "100650", "120123", 1);
    chooseRegion("chr2", "1369428", "2056742", 1);
    chooseButton("CTID_00000064", "container_cellTypes", "pancreas");
    chooseButton("CTID_0000038", "container_cellTypes", "skin fibroblast");
    chooseButton("CTID_0000052", "container_cellTypes", "heart");
}


/* UPLOAD CSV **************************************** **************************************** */

function uploadCSV(){
    document.getElementById('csv_upload').addEventListener('change', upload, false);

     function upload(evt) {

        var data = null;
        var file = evt.target.files[0];
        var reader = new FileReader();
        reader.readAsText(file);
        reader.onload = function(event) {
            var csvData = event.target.result;
             var results = Papa.parse(csvData);

            console.log(results);
            $("#csvFile").val(results.data);
            $("#csvFileRows").val(results.data.length);
        };

        reader.onerror = function() {
            alert('Unable to read ' + file.fileName);
        };
    };
}



/* VALIDATION **************************************** **************************************** */


function validateGeneQueryForm_numeric(){
    var validator = $("#geneQueryForm").validate();  //First destroying it, for the case we just
    // switched from the symbol choice to numeric
    validator.destroy();

    jQuery.validator.addMethod("checkENSG",function(value,element,param)
    {
       csv_val = document.getElementById('csv_upload').value;
      if(/ENSG+[0-9]{10}.*$/.test(value) || csv_val.substr(csv_val.length-3, csv_val.length-1)==='csv')
        {
          return true;
        }
        return false;
    },"Please enter an ID, written as 'ENSG' followed by ten digits. Separate multiple by comma. Or upload a valid csv-file.");

    $('#geneQueryForm').validate(
    {
          rules:
            {
              geneID_numeric:{checkENSG:true }
            },
            messages: {geneID_numeric: { required:  "Please enter an ID, written as 'ENSG' followed by ten digits. Separate multiple by comma. Or upload a valid csv-file."}},
            errorElement : 'div',
            errorClass: "formError",
            highlight: function(element, errorClass) {
                 $(element).removeClass(errorClass);}
          });
}

function validateGeneQueryForm_symbolic(){
        var validator = $("#geneQueryForm").validate();
        validator.destroy();

        jQuery.validator.addMethod("checkSymbol", function(value,element,param)
    {
        csv_val = document.getElementById('csv_upload').value;
      if (document.getElementById("container_geneSymbol").children.length > 0 || document.getElementById("geneID_symbolic").value.length > 1 || csv_val.substr(csv_val.length-3, csv_val.length-1)==='csv')
        {
          return true;
        }
        return false;
    },"Please select a gene symbol or upload a valid csv-file.");

    $('#geneQueryForm').validate(
      {
      rules:
        {
          geneID_symbolic:{ checkSymbol:true }
        },
        messages: {geneID_symbolic: { required:  "Please select a gene symbol or upload a valid csv-file."}},
        errorElement : 'div',
        errorClass: "formError",
        highlight: function(element, errorClass) {
         $(element).removeClass(errorClass);}
      });
}


function validateREMQueryForm(){
    jQuery.validator.addMethod("checkREM",function(value,element,param)
    {
   csv_val = document.getElementById('csv_upload').value;
      if(/REM+[0-9]{7}.*$/i.test(value) || csv_val.substr(csv_val.length-3, csv_val.length-1)==='csv')
        {
          return true;
        }
        return false;
    },"Please enter an ID, written as 'REM' followed by seven digits. Separate multiple by comma. Or upload a valid csv-file.");

    $('#remQueryForm').validate(
      {
      rules:
        {
          REMIDs:{checkREM:true}
        },
        errorElement : 'div',
        errorClass: "formError",
        highlight: function(element, errorClass) {
             $(element).removeClass(errorClass);}
      });
}


function testingFunction(){
    alert(131244698 > 56115629);
}



// check if we got something in the fields or alternatively a selected region as button

function validateRegionQueryForm(){
    jQuery.validator.addMethod("checkSubmission",function(value,element,param)
    {
    csv_val = document.getElementById('csv_upload').value;
      if(csv_val.substr(csv_val.length-3, csv_val.length-1).toLowerCase() ==='csv' || csv_val.substr(csv_val.length-3, csv_val.length-1).toLowerCase() ==='bed' || document.getElementById("container_geneRegions").children.length > 0)
        {
          return true;
        }
      else if(document.getElementById("chrField").value !== "default" && document.getElementById("chrStart").value !== '' && document.getElementById("chrEnd").value !=='')
        {
        return true;
        }
        return false;
    },"Please select a region or upload a valid csv-file");

    $('#regionQueryForm').validate(
      {
      rules:
        {
          chrStart:{checkSubmission:true}
        },
        onkeyup: false,
        onclick: false,
        onfocusout: false,
        errorElement : 'div',
        errorClass: "formError",
        errorLabelContainer: ".errorMessage",
        highlight: function(element, errorClass) {
             $(element).removeClass(errorClass);}
      });
}


function validateRegion(){
        chr = document.getElementById("chrField");
        start = document.getElementById("chrStart");
        end = document.getElementById("chrEnd");
        regionErrors = document.getElementById('regionErrors');

        if(chr.value === 'default')
        {
        regionErrors.innerHTML = regionErrors.innerHTML  + 'Please select a chromosome' + '<br>';
        regionErrors.style.visibility = "visible";
        }
        if(start.value === '')
        {
        regionErrors.innerHTML = regionErrors.innerHTML  + 'Please select a start position' + '<br>';
        regionErrors.style.visibility = "visible";
        }
        if(end.value === '')
        {
        regionErrors.innerHTML = regionErrors.innerHTML  + 'Please select an end position' + '<br>';
        regionErrors.style.visibility = "visible";
        }

        if(start.value !== '' && end.value !== '' && parseInt(start.value) >= parseInt(end.value))
        {
        regionErrors.innerHTML = regionErrors.innerHTML  + 'The start has to be lower than the end' + '<br>';
        regionErrors.style.visibility = "visible";
        }
        if(end.value > chr_start_end[chr.value][1])
        {
        regionErrors.innerHTML = regionErrors.innerHTML  + 'Please select a lower end position' + '<br>';
        regionErrors.style.visibility = "visible";
        }
        if(start.value < chr_start_end[chr.value][0])
        {
        regionErrors.innerHTML = regionErrors.innerHTML  + 'Please select a higher start position' + '<br>';
        regionErrors.style.visibility = "visible";
        }

        // If now error is there, meaning our error div is empty, we can create the button
        if(regionErrors.innerHTML==='')
        {
            chooseRegion();
         }
}

function hideError(){
  document.getElementById('regionErrors').innerHTML = '';
  document.getElementById('regionErrors').style.visibility = 'hidden';
}

