
// gets id of appliance element
function getApplianceId(appliance){
    var id = parseFloat(appliance.attr("id").split("_")[1]);
    return id;
}

var removedApplianceIds = []

// removes appliance element
function removeApplianceElement(applianceElement){
    var applianceElem = $(applianceElement).parent().parent().parent().parent().parent().parent();
    var applianceId =  getApplianceId(applianceElem);
    removedApplianceIds.push(applianceId)
    
    // get all appliance elements
    var appliances = $("#appliance_container").children();
    // change appliance ids
    for(var i=applianceId-1; i<appliances.length; i++){
        appliances[i].setAttribute("id", "appliance_"+applianceId);
    }

    // remove appliance that had the specific remove button
    applianceElem.remove();
}

// gets all appliance data, returns dictionary with its values
function getAllAppliancesData(type){
    var allAppliancesData=[];
    $("#appliance_container").find(".appliance").each(function(){
        var applianceData=[];
        $(this).find(".applianceData").each(function(index){
            if (type == "form"){
                applianceData.push({name:$(this).attr('name'), value:$(this).val()});
            } else {
                applianceData.push({name:$(this).attr('name'), value:$(this).html()});
            }
        });
        allAppliancesData.push(applianceData);
    });

    return allAppliancesData
}



// when edit button clicked 
function editAppliances(){
    var appliancesData = getAllAppliancesData();
    // hide edit button, show update button
    $("#edit_btn").prop('hidden', true);
    $("#update_btn").removeAttr("hidden");
    // remove all appliances in the container
    $('#appliance_container').empty();

    // populate container with editable appliances by cloning appliance template
    var appliance_template = $('#appliance_template');
    for(var i=0; i<appliancesData.length; i++){
        var appliance_card = appliance_template.clone();
        appliance_card.find(".applianceData").each(function(index){
            $(this).attr("value", appliancesData[i][index]['value']);
        })
        var applianceId =  appliance_card.find(".applianceID").first().attr("value");
        appliance_card.attr("id", "appliance_"+applianceId);
        appliance_card.removeAttr("hidden");
        $('#appliance_container').append(appliance_card);
    }
}


// when update button clicked
function updateAppliances(){
    var appliancesData = getAllAppliancesData("form");

    // save to database
    $.ajax({
        url: '/updateAppliances',
        type: 'POST',
        data: JSON.stringify({appliancesData: appliancesData, removedApplianceIds: removedApplianceIds}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response){
            console.log(response);
            removedApplianceIds = []
        
        },
        error: function(error){
            console.log(error);
        }
    });
}





