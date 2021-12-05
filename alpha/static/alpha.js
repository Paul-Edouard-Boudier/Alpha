$(document).ready(function() {
    $('.draggable').draggable(
        {
            // containment: $('.draggable-receptacle'),
            helper: 'clone',
            containment: 'window',
        }
    );
    $('.draggable').css('cursor', 'pointer');
    
    $('.draggable-receptacle').droppable( 
    {
    	drop: handleDropEvent
    } );
    
    $('.trash').droppable( 
    {
    	drop: handleDropEventSuppr
    } );
    
})


function handleDropEvent( event, ui ) 
{
  var draggable = ui.draggable;	
  if (draggable.hasClass("removable"))
  	return;
  $(this).html('<div class="removable">'+draggable.text()+'</div>');
  $('.removable').draggable ({helper: 'original', containment: 'window', revert:true});
  $('.removable').css('cursor', 'pointer');
  if (draggable.data("rang") == "T")
  	$(this).css("background-color","#82c167");
  else if (g=draggable.data("rang") == "C")
  	$(this).css("background-color", "#5eb03a");
  else if (draggable.data("rang") == "F")
  	$(this).css("background-color", "#cade75");
  else
  	$(this).css("background-color", "#cfacac");
  	
  var donnees = '{"cellule":"' + $(this).attr('id') + '", "culture":"'+draggable.text()+'"}';
  alert (donnees);
   /*$.ajax({
		url: ,
		type: "POST",
		dataType: 'json',
		data: donnees,
		success: function(resData){
		  	
			//console.log(dataw);					
		},
			error:function(exception){
				
			}
		});
		
  */	
  	
}

function handleDropEventSuppr( event, ui ) {
	ui.draggable.parent().css("background-color","white");
	
	if (ui.draggable.hasClass("removable"))
		ui.draggable.remove();
	

}
