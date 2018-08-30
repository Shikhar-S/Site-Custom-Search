$( function() {
    $( "#dialog" ).dialog({
      autoOpen: false,
      show: {
        effect: "blind",
        duration: 1000
      },
      hide: {
        effect: "explode",
        duration: 1000
      },
      width: "90%",
   maxWidth: "768px"
    });
    })



window.onload = function() {
	// setup the button click

	document.getElementById("search_query").onsubmit=function(){getsearchresults();};
}


function getsearchresults() {
event.preventDefault();

  var query=document.getElementById("search_term").value;
  console.log(query);
  $("#searchresults").empty().append(query);
     $( "#dialog" ).dialog( "open" );
 var data = { "search_term":query, csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),'crawlername':' rishabh5 '}; alert('hello');
     event.preventDefault();
   $.post("getresultpop", data, function(resp){
   console.log("hello");
     var content=$(resp);
      $("#searchresults").empty().append(resp);
        $( "#dialog" ).dialog( "open" );




	});

 event.preventDefault();
}

