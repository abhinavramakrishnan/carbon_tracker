
// gets id of user element
function getUserId(user){
    var id = parseFloat(user.attr("id").split("_")[1]);
    return id;
}

var removedUserIds = []

// removes user element
function removeUserElement(userElement){
    var userElem = $(userElement).parent().parent().parent().parent().parent().parent();
    var userId =  getUserId(userElem);
    removedUserIds.push(userId)
    
    // get all user elements
    var users = $("#user_container").children();
    // change user ids
    for(var i=userId-1; i<users.length; i++){
        users[i].setAttribute("id", "user_"+userId);
    }

    // remove user that had the specific remove button
    userElem.remove();
}

// gets all user data, returns dictionary with its values
function getAllUsersData(){
    var allUsersData=[];
    $("#user_container").find(".user").each(function(){
        var userData=[];
        $(this).find(".userData").each(function(index){
            userData.push({name:$(this).attr('name'), value:$(this).val()});
        });
        allUsersData.push(userData);
    });

    return allUsersData
}


// when update button clicked
function updateUsers(){
    var usersData = getAllUsersData("form");
    console.log(usersData);

    // save to database
    $.ajax({
        url: '/updateUsers',
        type: 'POST',
        data: JSON.stringify({usersData: usersData, removedUserIds: removedUserIds}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response){
            console.log(response);
            removedUserIds = []
        
        },
        error: function(error){
            console.log(error);
        }
    });
}





