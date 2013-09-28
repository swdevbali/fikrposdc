function deleteUser(userId)
{
    bootbox.confirm("Are you sure?", function(result){
        if(result){
            window.open("/manage/users/delete/" + userId, "_self");
        }
    }
                   );
                 
}