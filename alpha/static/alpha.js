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
  var cellule = $(this);
  var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
  var donnees = {"cellule":$(this).attr('id'), "culture":draggable.text()};
  //alert (donnees);
  $.ajax({
		url: 'updateassol',
		type: "POST",
		dataType: 'json',
		data: donnees,
		headers: {'X-CSRFToken': csrftoken},
		success: function(resData){
			bh = " ";
			if(!resData.bilanhydrique)
				bh = '<img src=/static/images/drop.png width="30px" height="30px">';
			st = " ";
			if (!resData.besointemperature)
				st = '<img src=/static/images/snow.png width="30px" height="30px">';
		  	cellule.html('<div class="removable">'+draggable.text()+bh+st+'</div>');
		  	cellule.attr ('data-culture', draggable.text());
		  	if (resData.note_rotation > -1)
		  		$('#as'+cellule.data ('idparc')).html(resData.alpha_score);
		  	camenbert (cellule.data ('annee'));
		},
			error:function(exception){

			}
		});

}

function handleDropEventSuppr( event, ui ) {
	ui.draggable.parent().css("background-color","white");

	if (ui.draggable.hasClass("removable"))
		ui.draggable.remove();


}


function camenbert (annee)
{
	var cumuls ={};
	$('*[data-annee="'+annee+'"]').each(function () {
		//debugger;
		var culture = $(this).attr('data-culture');
		if (culture in cumuls)
			{
				cumuls[culture] += parseInt($(this).attr('data-surface'));
			}
		else
		{
			cumuls[culture] = parseInt($(this).attr('data-surface'));
		}
	});
	
	 

// set the dimensions and margins of the graph
const width = 300,
    height = 300,
    margin = 40;

// The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
const radius = Math.min(width, height) / 2 - margin;

$('#svg'+annee).html("");

// append the svg object to the div called 'my_dataviz'


const svg = d3.select('#svg'+annee)
  .append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", `translate(${width/2}, ${height/2})`);


// set the color scale
const color = d3.scaleOrdinal()
  .domain(["a", "b", "c", "d", "e", "f"])
  .range(d3.schemeDark2);

// A function that create / update the plot for a given variable:
function update(data) {

  // Compute the position of each group on the pie:
  const pie = d3.pie()
    .value(function(d) {return d[1]; })
    .sort(function(a, b) { return d3.ascending(a.key, b.key);} ) // This make sure that group order remains the same in the pie chart
  const data_ready = pie(Object.entries(data))

  // map to data
  const u = svg.selectAll("path")
    .data(data_ready)
	
  // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
  u    
    .join('path')
    .transition()
    .duration(1000)
    .attr('d', d3.arc()
      .innerRadius(0)
      .outerRadius(radius)
    )
    .attr('fill', function(d){ return(color(d.data[0])) })
    .attr("stroke", "white")
    .style("stroke-width", "2px")
    .style("opacity", 1)
	.append('text')
  	.text(function(d){ return d.data[0]})
  	.attr("transform", function(d) { return "translate(" + arcGenerator.centroid(d) + ")";  })
  .style("text-anchor", "middle")
  .style("font-size", 17)

}

// Initialize the plot with the first dataset
update(cumuls)
	
	
	
	
	
	
}
