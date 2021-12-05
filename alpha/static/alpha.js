$(document).ready(function() {
    $('.draggable').draggable(
        {
            // containment: $('.draggable-receptacle'),
            helper: 'clone'
        }
    );
    $('.draggable').css('cursor', 'pointer');
    $('#scenario-selector').on('change', function() {
        $('.years').children('th[data-other-year]').each(function() {
            // debugger;
            var old_year = $(this).html()
            var new_year = $(this).attr('data-other-year')
            $(this).html(new_year)
            $(this).attr('data-other-year', old_year)
        });
            // debugger;
    });
    var svg = d3.select("svg"),
        width = svg.attr("width"),
        height = svg.attr("height"),
        radius = Math.min(width, height) / 2;

    debugger;

     var g = svg.append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

     var color = d3.scaleOrdinal([
        'gray', 'green', 'brown', 'orange', 'yellow', 'red', 'purple'
     ]);

     var pie = d3.pie().value(function(d) {
        return d.percent;
     });

     var path = d3.arc()
        .outerRadius(radius - 10).innerRadius(0);

     var label = d3.arc()
        .outerRadius(radius).innerRadius(radius - 80);

     d3.csv("populations.csv", function(error, data) {
        if (error) {
           throw error;
        }

        var arc = g.selectAll(".arc")
           .data(pie(data))
           .enter()
           .append("g")
           .attr("class", "arc");

        arc.append("path")
           .attr("d", path)
           .attr("fill", function(d) { return color(d.data.states); });

        console.log(arc)

        arc.append("text").attr("transform", function(d) {
           return "translate(" + label.centroid(d) + ")";
        })

        .text(function(d) { return d.data.states; });
     });

     svg.append("g")
        .attr("transform", "translate(" + (width / 2 - 120) + "," + 20 + ")")
        .append("text").text("Top population states in india")
        .attr("class", "title")
})