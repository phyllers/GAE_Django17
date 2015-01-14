d3.tsv("../clinMut_10054_56_02.tsv")
    .header("Content-Type", "application/json")
    .get(function(error, data){
      circleg.mutation_array_data = data;
      console.log(circleg.mutation_array_data);       
      draw_circle_graphs();
    });


 var circleg = circleg || {};